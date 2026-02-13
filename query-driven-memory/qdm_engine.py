"""
QDM Engine — Query-Driven Memory
All Qdrant and Ollama operations: store, retrieve, decay, prune, stats.
Connects to EXISTING infrastructure (Qdrant :6333, Ollama :11434).
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Optional

import requests
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
)

OLLAMA_URL = "http://localhost:11434"
QDRANT_URL = "http://localhost:6333"
COLLECTION = "qdm_memories"
EMBED_MODEL = "nomic-embed-text"
EMBED_DIM = 768


# ---------------------------------------------------------------------------
# Client helpers
# ---------------------------------------------------------------------------

_qdrant: QdrantClient | None = None


def get_qdrant() -> QdrantClient:
    global _qdrant
    if _qdrant is None:
        _qdrant = QdrantClient(url=QDRANT_URL, timeout=10)
    return _qdrant


def check_qdrant() -> bool:
    """Return True if Qdrant is reachable."""
    try:
        get_qdrant().get_collections()
        return True
    except Exception:
        return False


def check_ollama() -> bool:
    """Return True if Ollama is reachable."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def list_ollama_models() -> list[str]:
    """Return list of model names available in Ollama."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        r.raise_for_status()
        return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Collection management
# ---------------------------------------------------------------------------

def ensure_collection():
    """Create qdm_memories collection if it does not exist."""
    client = get_qdrant()
    names = [c.name for c in client.get_collections().collections]
    if COLLECTION not in names:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
        )


# ---------------------------------------------------------------------------
# Embedding
# ---------------------------------------------------------------------------

def get_embedding(text: str) -> list[float]:
    """Get embedding from Ollama nomic-embed-text."""
    r = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["embedding"]


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------

def store_memory(
    text: str,
    role: str,
    conversation_id: str,
    pinned: bool = False,
) -> str:
    """Store a single message as a memory in Qdrant. Returns the point ID."""
    ensure_collection()
    embedding = get_embedding(text)
    point_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    payload = {
        "text": text,
        "role": role,
        "timestamp": now,
        "conversation_id": conversation_id,
        "access_count": 0,
        "last_accessed": now,
        "relevance_score": 10.0,
        "pinned": pinned,
        "user_notes": "",
    }

    get_qdrant().upsert(
        collection_name=COLLECTION,
        points=[PointStruct(id=point_id, vector=embedding, payload=payload)],
    )
    return point_id


# ---------------------------------------------------------------------------
# Retrieve
# ---------------------------------------------------------------------------

def retrieve_memories(query: str, top_k: int = 5) -> list[dict]:
    """
    Search for relevant memories, filter by relevance_score >= 2.0,
    boost retrieved memories, and return them.
    """
    ensure_collection()
    embedding = get_embedding(query)

    results = get_qdrant().query_points(
        collection_name=COLLECTION,
        query=embedding,
        limit=top_k * 2,  # fetch extra to allow filtering
        with_payload=True,
        score_threshold=0.0,
    )

    memories = []
    now = datetime.now(timezone.utc).isoformat()

    for point in results.points:
        p = point.payload
        if p.get("relevance_score", 0) < 2.0:
            continue

        # Boost: access_count++, last_accessed=now, relevance_score+=1.0
        new_access = p.get("access_count", 0) + 1
        new_relevance = p.get("relevance_score", 10.0) + 1.0

        get_qdrant().set_payload(
            collection_name=COLLECTION,
            payload={
                "access_count": new_access,
                "last_accessed": now,
                "relevance_score": new_relevance,
            },
            points=[point.id],
        )

        memories.append({
            "id": point.id,
            "text": p["text"],
            "role": p.get("role", "unknown"),
            "timestamp": p.get("timestamp", ""),
            "relevance_score": new_relevance,
            "similarity": round(point.score, 4),
            "access_count": new_access,
            "pinned": p.get("pinned", False),
        })

        if len(memories) >= top_k:
            break

    return memories


# ---------------------------------------------------------------------------
# Decay
# ---------------------------------------------------------------------------

def run_decay(rate: float = 0.1) -> dict:
    """
    Decay all non-pinned memories:
    relevance_score -= days_since_last_accessed * rate
    Minimum score is 0.0. Returns stats.
    """
    ensure_collection()
    client = get_qdrant()
    now = datetime.now(timezone.utc)

    all_points, _ = client.scroll(
        collection_name=COLLECTION,
        limit=100_000,
        with_payload=True,
        with_vectors=False,
    )

    decayed = 0
    for point in all_points:
        p = point.payload
        if p.get("pinned", False):
            continue

        last_accessed_str = p.get("last_accessed", p.get("timestamp", ""))
        try:
            last_accessed = datetime.fromisoformat(last_accessed_str)
            if last_accessed.tzinfo is None:
                last_accessed = last_accessed.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            last_accessed = now

        days_since = max(0.0, (now - last_accessed).total_seconds() / 86400)
        decay_amount = days_since * rate
        old_score = p.get("relevance_score", 10.0)
        new_score = max(0.0, old_score - decay_amount)

        if new_score != old_score:
            client.set_payload(
                collection_name=COLLECTION,
                payload={"relevance_score": new_score},
                points=[point.id],
            )
            decayed += 1

    return {"total_checked": len(all_points), "decayed": decayed}


# ---------------------------------------------------------------------------
# Prune
# ---------------------------------------------------------------------------

def run_prune() -> dict:
    """
    Delete non-pinned memories where relevance_score < 1.0
    AND last_accessed > 90 days ago.
    """
    ensure_collection()
    client = get_qdrant()
    now = datetime.now(timezone.utc)
    cutoff = 90 * 86400  # 90 days in seconds

    all_points, _ = client.scroll(
        collection_name=COLLECTION,
        limit=100_000,
        with_payload=True,
        with_vectors=False,
    )

    to_delete = []
    for point in all_points:
        p = point.payload
        if p.get("pinned", False):
            continue
        if p.get("relevance_score", 10.0) >= 1.0:
            continue

        last_accessed_str = p.get("last_accessed", p.get("timestamp", ""))
        try:
            last_accessed = datetime.fromisoformat(last_accessed_str)
            if last_accessed.tzinfo is None:
                last_accessed = last_accessed.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            continue

        if (now - last_accessed).total_seconds() > cutoff:
            to_delete.append(point.id)

    if to_delete:
        client.delete(
            collection_name=COLLECTION,
            points_selector=to_delete,
        )

    return {"pruned": len(to_delete)}


# ---------------------------------------------------------------------------
# Memory management helpers
# ---------------------------------------------------------------------------

def get_all_memories(pinned_only: bool = False) -> list[dict]:
    """Return all memories, optionally filtered to pinned only."""
    ensure_collection()
    client = get_qdrant()

    scroll_filter = None
    if pinned_only:
        scroll_filter = Filter(
            must=[FieldCondition(key="pinned", match=MatchValue(value=True))]
        )

    all_points, _ = client.scroll(
        collection_name=COLLECTION,
        limit=100_000,
        with_payload=True,
        with_vectors=False,
        scroll_filter=scroll_filter,
    )

    memories = []
    for point in all_points:
        p = point.payload
        memories.append({
            "id": point.id,
            "text": p.get("text", ""),
            "role": p.get("role", "unknown"),
            "timestamp": p.get("timestamp", ""),
            "conversation_id": p.get("conversation_id", ""),
            "access_count": p.get("access_count", 0),
            "last_accessed": p.get("last_accessed", ""),
            "relevance_score": p.get("relevance_score", 0.0),
            "pinned": p.get("pinned", False),
            "user_notes": p.get("user_notes", ""),
        })

    # Sort by timestamp descending
    memories.sort(key=lambda m: m["timestamp"], reverse=True)
    return memories


def toggle_pin(point_id: str, pinned: bool):
    """Set the pinned status of a memory."""
    get_qdrant().set_payload(
        collection_name=COLLECTION,
        payload={"pinned": pinned},
        points=[point_id],
    )


def update_user_notes(point_id: str, notes: str):
    """Update user notes on a memory."""
    get_qdrant().set_payload(
        collection_name=COLLECTION,
        payload={"user_notes": notes},
        points=[point_id],
    )


def delete_memory(point_id: str):
    """Delete a single memory."""
    get_qdrant().delete(
        collection_name=COLLECTION,
        points_selector=[point_id],
    )


def pin_exchange(conversation_id: str, user_text: str, assistant_text: str):
    """Pin both messages of a user/assistant exchange by matching text."""
    client = get_qdrant()
    results, _ = client.scroll(
        collection_name=COLLECTION,
        scroll_filter=Filter(
            must=[FieldCondition(key="conversation_id", match=MatchValue(value=conversation_id))]
        ),
        limit=100_000,
        with_payload=True,
        with_vectors=False,
    )

    for point in results:
        text = point.payload.get("text", "")
        if text == user_text or text == assistant_text:
            client.set_payload(
                collection_name=COLLECTION,
                payload={"pinned": True},
                points=[point.id],
            )


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

def get_stats() -> dict:
    """Get memory statistics."""
    ensure_collection()
    client = get_qdrant()

    all_points, _ = client.scroll(
        collection_name=COLLECTION,
        limit=100_000,
        with_payload=True,
        with_vectors=False,
    )

    total = len(all_points)
    if total == 0:
        return {
            "total": 0,
            "pinned": 0,
            "avg_relevance": 0.0,
        }

    pinned = sum(1 for p in all_points if p.payload.get("pinned", False))
    scores = [p.payload.get("relevance_score", 0.0) for p in all_points]
    avg = sum(scores) / len(scores) if scores else 0.0

    return {
        "total": total,
        "pinned": pinned,
        "avg_relevance": round(avg, 2),
    }


# ---------------------------------------------------------------------------
# Chat (Ollama streaming)
# ---------------------------------------------------------------------------

def build_prompt(
    retrieved_memories: list[dict],
    session_messages: list[dict],
    user_message: str,
) -> list[dict]:
    """Build the messages list for Ollama chat API."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant with persistent memory. "
                "The following context is from relevant past conversations. "
                "Use it naturally to inform your responses, but don't explicitly "
                "reference 'your memory' unless asked."
            ),
        }
    ]

    # Inject retrieved memories as context
    if retrieved_memories:
        context_parts = []
        for mem in retrieved_memories:
            role_label = "User" if mem["role"] == "user" else "Assistant"
            ts = mem.get("timestamp", "")[:16].replace("T", " ")
            context_parts.append(f"[{role_label} — {ts}]: {mem['text']}")
        context_block = "\n\n".join(context_parts)
        messages.append({
            "role": "system",
            "content": f"## Relevant past context:\n\n{context_block}",
        })

    # Current session history
    for msg in session_messages:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # New user message
    messages.append({"role": "user", "content": user_message})

    return messages


def chat_stream(messages: list[dict], model: str = "llama3.2:3b"):
    """Stream chat response from Ollama. Yields token strings."""
    r = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={"model": model, "messages": messages, "stream": True},
        stream=True,
        timeout=120,
    )
    r.raise_for_status()
    for line in r.iter_lines():
        if line:
            data = json.loads(line)
            token = data.get("message", {}).get("content", "")
            if token:
                yield token
            if data.get("done", False):
                break
