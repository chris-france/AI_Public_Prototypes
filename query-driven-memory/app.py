"""
QDM — Query-Driven Memory
Streamlit chat interface with persistent vector memory via Qdrant.
Port 8607
"""

import uuid
import streamlit as st
import qdm_engine as engine

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Query-Driven Memory",
    page_icon="🧠",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Connection checks
# ---------------------------------------------------------------------------

qdrant_ok = engine.check_qdrant()
ollama_ok = engine.check_ollama()

if not qdrant_ok or not ollama_ok:
    st.title("🧠 Query-Driven Memory")
    if not qdrant_ok:
        st.error("**Qdrant not reachable** at localhost:6333. Start it with `docker compose up -d` in `~/local-rag`.")
    if not ollama_ok:
        st.error("**Ollama not reachable** at localhost:11434. Start it with `ollama serve`.")
    st.info("QDM connects to existing infrastructure — it does not start its own instances.")
    st.stop()

# Ensure collection exists
engine.ensure_collection()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role", "content", "memories"}

if "startup_decay_done" not in st.session_state:
    engine.run_decay(rate=0.1)
    st.session_state.startup_decay_done = True

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### 🧠 QDM Settings")

    # Model selector
    models = engine.list_ollama_models()
    default_model = "llama3.2:3b"
    if default_model not in models and models:
        default_model = models[0]
    model_idx = models.index(default_model) if default_model in models else 0
    selected_model = st.selectbox("Ollama Model", models, index=model_idx) if models else "llama3.2:3b"

    st.divider()

    # Memory stats
    st.markdown("### Memory Stats")
    stats = engine.get_stats()
    c1, c2 = st.columns(2)
    c1.metric("Total", stats["total"])
    c2.metric("Pinned", stats["pinned"])
    st.metric("Avg Relevance", f"{stats['avg_relevance']:.2f}")

    st.divider()

    # Decay / Prune controls
    decay_rate = st.slider("Decay rate", 0.01, 0.5, 0.1, 0.01)

    col_d, col_p = st.columns(2)
    with col_d:
        if st.button("Run Decay", use_container_width=True):
            result = engine.run_decay(rate=decay_rate)
            st.toast(f"Decayed {result['decayed']} / {result['total_checked']} memories")
            st.rerun()
    with col_p:
        if st.button("Prune Old", use_container_width=True):
            result = engine.run_prune()
            st.toast(f"Pruned {result['pruned']} memories")
            st.rerun()

    st.divider()

    # Memory Browser
    st.markdown("### Memory Browser")
    tab_all, tab_pinned = st.tabs(["All Memories", "Pinned Only"])

    def _render_memory_list(memories: list[dict], tab_key: str):
        if not memories:
            st.caption("No memories yet.")
            return
        for i, mem in enumerate(memories):
            key_prefix = f"{tab_key}_{mem['id']}"
            preview = mem["text"][:100] + ("..." if len(mem["text"]) > 100 else "")
            role_icon = "👤" if mem["role"] == "user" else "🤖"
            ts_short = mem["timestamp"][:16].replace("T", " ") if mem["timestamp"] else ""

            with st.container(border=True):
                st.markdown(f"{role_icon} {preview}")
                st.caption(
                    f"{ts_short} · "
                    f"accessed {mem['access_count']}x · "
                    f"relevance {mem['relevance_score']:.1f}"
                    f"{' · 📌' if mem['pinned'] else ''}"
                )

                bc1, bc2 = st.columns(2)
                with bc1:
                    pin_label = "Unpin" if mem["pinned"] else "Pin"
                    if st.button(pin_label, key=f"{key_prefix}_pin", use_container_width=True):
                        engine.toggle_pin(mem["id"], not mem["pinned"])
                        st.rerun()
                with bc2:
                    if st.button("Delete", key=f"{key_prefix}_del", use_container_width=True):
                        engine.delete_memory(mem["id"])
                        st.rerun()

                notes = st.text_input(
                    "Notes",
                    value=mem.get("user_notes", ""),
                    key=f"{key_prefix}_notes",
                    label_visibility="collapsed",
                    placeholder="Add a note...",
                )
                if notes != mem.get("user_notes", ""):
                    engine.update_user_notes(mem["id"], notes)

    with tab_all:
        all_mems = engine.get_all_memories(pinned_only=False)
        _render_memory_list(all_mems, "all")

    with tab_pinned:
        pinned_mems = engine.get_all_memories(pinned_only=True)
        _render_memory_list(pinned_mems, "pin")


# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------

st.title("🧠 Query-Driven Memory")
st.caption(f"Session `{st.session_state.conversation_id[:8]}...` — Every message is remembered. Relevant past context is retrieved automatically.")

# New conversation button
if st.button("New Conversation"):
    st.session_state.conversation_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.rerun()

# Display chat history
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        # Pin button on assistant messages
        if msg["role"] == "assistant":
            if st.button("📌 Pin this exchange", key=f"pin_exchange_{i}"):
                # Find the preceding user message
                user_text = ""
                for j in range(i - 1, -1, -1):
                    if st.session_state.messages[j]["role"] == "user":
                        user_text = st.session_state.messages[j]["content"]
                        break
                engine.pin_exchange(
                    st.session_state.conversation_id,
                    user_text,
                    msg["content"],
                )
                st.toast("Exchange pinned!")
                st.rerun()

        # Show retrieved memories context
        if msg.get("memories"):
            with st.expander(f"Used {len(msg['memories'])} memories as context"):
                for mem in msg["memories"]:
                    role_label = "User" if mem["role"] == "user" else "Assistant"
                    ts = mem.get("timestamp", "")[:16].replace("T", " ")
                    st.markdown(
                        f"**{role_label}** ({ts}) — "
                        f"similarity {mem['similarity']:.4f} · "
                        f"relevance {mem['relevance_score']:.1f}"
                    )
                    st.caption(mem["text"][:300])
                    st.markdown("---")


# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------

if user_input := st.chat_input("Type a message..."):
    # Display user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Retrieve relevant memories
    retrieved = engine.retrieve_memories(user_input, top_k=5)

    # Build prompt
    session_history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]  # exclude the just-added user msg
    ]
    prompt_messages = engine.build_prompt(retrieved, session_history, user_input)

    # Stream response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        for token in engine.chat_stream(prompt_messages, model=selected_model):
            full_response += token
            response_placeholder.markdown(full_response + "▌")
        response_placeholder.markdown(full_response)

        # Pin button (will appear on rerun)
        # Show retrieved context
        if retrieved:
            with st.expander(f"Used {len(retrieved)} memories as context"):
                for mem in retrieved:
                    role_label = "User" if mem["role"] == "user" else "Assistant"
                    ts = mem.get("timestamp", "")[:16].replace("T", " ")
                    st.markdown(
                        f"**{role_label}** ({ts}) — "
                        f"similarity {mem['similarity']:.4f} · "
                        f"relevance {mem['relevance_score']:.1f}"
                    )
                    st.caption(mem["text"][:300])
                    st.markdown("---")

    # Store messages in session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "memories": retrieved,
    })

    # Store both messages in Qdrant
    engine.store_memory(
        text=user_input,
        role="user",
        conversation_id=st.session_state.conversation_id,
    )
    engine.store_memory(
        text=full_response,
        role="assistant",
        conversation_id=st.session_state.conversation_id,
    )

    st.rerun()
