# Query-Driven Memory (QDM) — User Guide

**A Chat Interface That Actually Remembers**

---

## What Is This Tool?

Query-Driven Memory is a chat interface with automatic persistent memory. Unlike standard chatbots that forget everything between sessions, QDM automatically searches all past conversations for relevant context on every query — no manual selection, no special commands, no document tagging. It just remembers.

Every message you send and every response you receive is stored as a memory. The next time you ask something related — whether it's five minutes later or five weeks later — QDM finds the relevant past exchanges and gives them to the model as context. The model responds with full awareness of your history, and you never have to tell it what to remember.

| Standard Chatbot | QDM |
|---|---|
| Forgets everything when you close the tab | Remembers every conversation permanently |
| Each session starts from scratch | Each session has access to all past sessions |
| You repeat yourself constantly | You pick up where you left off |
| No awareness of what you discussed last week | Automatically retrieves relevant history |

**Who should use this:**
- Knowledge workers who want an AI assistant that maintains continuity across sessions
- Researchers exploring topics over days or weeks who need the model to track evolving context
- Project managers documenting decisions and checking back on them later
- Anyone tired of re-explaining context to a chatbot that forgets everything

---

## Getting Started

### What You Need

- **Ollama** — runs the language model and generates embeddings locally
- **Qdrant** — vector database that stores and searches memories (runs in Docker)
- **Docker Desktop** — hosts the Qdrant container

QDM connects to existing infrastructure — it doesn't start its own instances. Ollama and Qdrant should already be running before you launch QDM.

### Quick Start

**From the Personal Demos launcher (port 8501):** Click the Start button on the QDM card. Done.

**Manually:**

```bash
# 1. Make sure Ollama is running
ollama serve

# 2. Make sure Qdrant is running
cd ~/local-rag && docker compose up -d qdrant

# 3. Pull the embedding model (first time only)
ollama pull nomic-embed-text

# 4. Launch QDM
cd ~/qdmem && ./run.sh
```

Open **http://localhost:8607** in your browser. Start chatting — memories accumulate naturally as you use it.

---

## How It Works

Every time you send a message, QDM performs the following steps automatically:

1. **You type a message** and hit enter
2. **QDM searches all stored memories** for anything semantically related — not keyword matching, but meaning-based similarity
3. **It bundles the most relevant memories** (up to 5) as context alongside your message
4. **The model receives your message plus that context** and responds with full awareness of your history
5. **The response streams in real-time**, token by token
6. **Both your message and the model's response are stored** as new memories for future retrieval

There is no manual step. You don't select documents, tag conversations, or tell the system what to remember. Every exchange is automatically indexed and available for future retrieval based on relevance.

### What "Relevant" Means

When QDM searches for memories, it compares the meaning of your current message against the meaning of everything stored. If you previously discussed project timelines and now ask "when is the deadline?", QDM finds those earlier messages even though the exact words are different. This is semantic search — it matches concepts, not keywords.

---

## The Memory System

QDM's memory is designed to work like human memory: frequently recalled things stay sharp, unused things gradually fade, and important things can be permanently preserved.

### Relevance Scoring

Every memory starts with a relevance score of 10.0. Each time a memory is retrieved as context for a new query, its score increases by 1.0. Memories that are frequently useful become stronger over time — the more you revisit a topic, the more readily those memories surface.

### Decay

Memories that haven't been accessed gradually lose relevance. For each day since a memory was last retrieved, its score drops by the decay rate (default 0.1 per day). A memory with a score of 10.0 that sits untouched for 30 days drops to 7.0. After 100 days of disuse, it reaches 0.0.

Decay runs automatically when QDM launches and can be triggered manually from the sidebar. The decay rate is adjustable — lower values preserve memories longer, higher values are more aggressive about fading old content.

### Pruning

Memories that have decayed below a relevance score of 1.0 and haven't been accessed in over 90 days are eligible for automatic deletion. Pruning is triggered manually via the sidebar — it never runs without your explicit action.

This prevents the memory pool from growing indefinitely with stale content while ensuring nothing recent or actively used is ever removed.

### Pinning

Any memory can be pinned. Pinned memories are permanently exempt from both decay and pruning — their relevance score never drops, and they are never auto-deleted regardless of age or access patterns.

Use pinning for things that should never be forgotten: key decisions, critical facts, foundational context, or any exchange you want permanently available.

### How It All Comes Together

| Memory Behavior | What Happens |
|---|---|
| New memory stored | Starts at relevance 10.0 |
| Memory retrieved as context | Score increases by 1.0, access count goes up, last-accessed updates |
| Memory sits unused | Score decreases by (days idle × decay rate) per decay pass |
| Memory drops below 1.0 and is 90+ days old | Eligible for pruning |
| Memory is pinned | Immune to decay and pruning forever |

The result: your most-used knowledge stays strong, rarely-used tangents gradually fade, and critical information persists permanently when you flag it.

---

## Using the Interface

### Chat Area

The main panel is a standard chat interface. Type a message and press Enter. Responses stream in real-time.

**Pin button** — Every assistant response has a "Pin this exchange" button. Clicking it pins both your question and the model's answer as permanent memories exempt from decay.

**"Used X memories as context"** — Below each response, an expandable section shows which past memories were retrieved. Expand it to see the memory text, when it was originally stored, its similarity to your current query, and its current relevance score. Full transparency into what the model "remembered" for each response.

**New Conversation** — Starts a fresh session. The chat area clears, but all memories remain searchable. Previous conversations are still retrievable by relevance.

### Sidebar

**Model Selector** — Dropdown of all models available in Ollama. Switch models at any time without losing memories.

**Memory Stats** — Three metrics updated on each page load: total memories stored, pinned count, and average relevance score across all memories.

**Decay Rate Slider** — Adjusts how aggressively unused memories fade. Range is 0.01 to 0.5 points per day. Default of 0.1 means an untouched memory loses 1 point every 10 days.

**Run Decay** — Manually triggers a decay pass across all non-pinned memories.

**Prune Old** — Deletes memories that have decayed below 1.0 and haven't been accessed in over 90 days. Never deletes pinned memories.

### Memory Browser

Located in the sidebar below the controls, with two tabs:

**All Memories** — Every stored memory, sorted by most recent. Each entry shows text preview, timestamp, access count, relevance score, and pin status. You can pin/unpin, delete, or add personal notes to any memory.

**Pinned Only** — Same view filtered to pinned memories only.

---

## How QDM Is Different from RAG

RAG and QDM both give a language model access to external information, but they work in fundamentally different ways.

| | RAG | QDM |
|---|---|---|
| **What it stores** | Documents you upload | Everything you discuss, automatically |
| **How you select context** | Manually choose with `#` | Automatic on every query |
| **Mental model** | A filing cabinet you open manually | An assistant that checks the cabinet for you |
| **Primary use** | Document question-answering | Persistent conversational memory |
| **Session continuity** | Each session starts fresh | Every session accesses all past sessions |

**RAG is document retrieval.** Upload a PDF, select it, ask questions. No upload or selection means no context.

**QDM is conversation memory.** Every exchange is automatically stored and indexed. Come back days later and ask a related question — the relevant history is already there.

They're complementary. RAG is ideal for querying specific documents. QDM is ideal when knowledge accumulates through conversation over time.

---

## Model Recommendations

QDM works with any Ollama model. Larger models generally do better at synthesizing retrieved context into coherent responses.

| Model | Best For | Trade-off |
|---|---|---|
| `llama3.2:3b` | Fast responses, simple recall | May struggle synthesizing multiple memories |
| `mistral:7b` | Good balance of speed and quality | Handles most memory-augmented conversations well |
| `qwen2.5:14b` | Best accuracy for complex context | Slower, requires more RAM |

For quick back-and-forth on recent context, 3B is fine. For sessions where QDM is pulling in memories from weeks ago and the model needs to weave them together, 7B or 14B produces noticeably better results.

---

## Example Use Cases

### Personal Knowledge Management

Tell QDM about your goals, strategies, and key decisions as they happen. Come back days or weeks later and it remembers the context. "What approach did we settle on for the migration?" works even if you discussed it three weeks ago in a different session.

### Meeting Notes and Decisions

After a meeting, summarize key outcomes in a QDM conversation. Pin the critical decisions. When someone asks "what did we decide about the vendor selection?" weeks later, ask QDM — it retrieves the relevant discussion with full context.

### Research Continuity

Explore a topic across multiple sessions over days or weeks. On Monday you discuss transformer architectures, Wednesday you explore attention mechanisms, Friday you ask "how does what we discussed about attention relate to the scaling issues?" — QDM connects the dots because all three sessions are in its memory pool.

### Strategic Planning

Use QDM as a sounding board for long-term planning. Pin your core frameworks and strategic principles so they're always available. As you iterate over multiple sessions, QDM tracks the evolution — you can ask "how has our approach changed since we started?" and get an answer grounded in your actual conversation history.

### Learning and Study

Work through complex material over multiple sessions. QDM remembers what you've already covered, what confused you, and what explanations worked. Instead of restarting from scratch each time, you build on previous understanding.

---

## Known Limitations

- **Single user** — No multi-user authentication. All memories are in one shared pool.
- **Memory grows with every message** — Both sides of every exchange are stored. Heavy use accumulates thousands of memories. Use decay and pruning to manage growth.
- **No document upload** — QDM stores conversations, not files. You can paste text into the chat, but there's no drag-and-drop file upload (planned for V2.0).
- **Embedding model must match** — All memories use the same embedding model. Switching models requires re-indexing all stored memories.
- **Cold start** — First message after launching may be slow while the model loads into memory.
- **Context window limits** — If many long memories are retrieved, the combined context may approach the model's token limit. Larger models handle this better.
- **No memory editing** — You can add notes and delete memories, but you can't edit stored text.
- **Requires Qdrant running** — If Qdrant is stopped, QDM shows an error until it's restarted.
- **Similarity is not understanding** — Semantic search finds related text, but it can retrieve tangentially related memories that aren't useful. Larger models are better at ignoring irrelevant context.

---

## V2.0 Roadmap

**Document Upload** — Drop in PDFs, Markdown, and Word documents that get embedded into the same memory pool as conversations. Search across both docs and chat history automatically. One unified memory space.

**Image and Multimodal Memory** — Store and recall visual content alongside text. Share a diagram in one session, reference it weeks later. Images become first-class searchable objects.

**Memory Consolidation** — Periodically merge related memories, resolve contradictions, and compress stale entries into summaries. Instead of 50 individual messages about the same topic, consolidation produces a single rich memory capturing the essential knowledge.

**Knowledge Graph Extraction** — Extract entities and relationships into a structured graph. Answer questions like "what are all the decisions we've made about X?" by traversing connected concepts — deeper reasoning over accumulated knowledge.

**Role-Based Access** — Multi-user support with separate memory spaces. Each user gets their own pool with optional shared spaces for team knowledge.

**Custom Model Integration** — Pair QDM with a domain-specific fine-tuned model for specialized persistent AI. A legal assistant that remembers case history. A medical advisor that tracks patient context. The memory system stays the same — the model becomes specialized.

---

*QDM runs entirely on your machine. No data is sent to external services. All models, embeddings, and memory storage operate locally.*
