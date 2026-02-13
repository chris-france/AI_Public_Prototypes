"""
RAG Engine with Persistent Chat Memory
Handles document retrieval and conversation memory via Qdrant.
"""

import uuid
import time
import json
from typing import AsyncIterator, Optional
from datetime import datetime

import httpx
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
)

from config import settings

# Globals initialized lazily
_qdrant: QdrantClient | None = None
_embedding_dim: int | None = None


def get_qdrant() -> QdrantClient:
    """Get Qdrant client (lazy initialization)."""
    global _qdrant
    if _qdrant is None:
        _qdrant = QdrantClient(url=settings.qdrant.url)
    return _qdrant


def get_embedding(text: str) -> list[float]:
    """Get embedding from Ollama embedding endpoint."""
    response = httpx.post(
        f"{settings.ollama.base_url}/api/embeddings",
        json={
            "model": settings.embedding.model,
            "prompt": text
        },
        timeout=60.0
    )
    response.raise_for_status()
    return response.json()["embedding"]


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Get embeddings for multiple texts."""
    return [get_embedding(text) for text in texts]


def get_embedding_dimension() -> int:
    """Get the dimension of embeddings from the model."""
    global _embedding_dim
    if _embedding_dim is None:
        test_embedding = get_embedding("test")
        _embedding_dim = len(test_embedding)
    return _embedding_dim


def ensure_collection(collection_name: str):
    """Ensure a Qdrant collection exists."""
    client = get_qdrant()
    collections = [c.name for c in client.get_collections().collections]
    if collection_name not in collections:
        dim = get_embedding_dimension()
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )


def ensure_all_collections():
    """Ensure all required collections exist."""
    ensure_collection(settings.qdrant.documents_collection)
    ensure_collection(settings.qdrant.chat_memory_collection)


# ---------------------------------------------------------------------------
# Document Processing
# ---------------------------------------------------------------------------

def chunk_text(text: str) -> list[tuple[str, int]]:
    """Split text into chunks. Returns (chunk_text, char_offset) pairs."""
    chunk_size = settings.chunking.size
    overlap = settings.chunking.overlap

    # Simple character-based chunking (approximate tokens)
    chars_per_token = 4  # rough estimate
    chunk_chars = chunk_size * chars_per_token
    overlap_chars = overlap * chars_per_token

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_chars, len(text))
        chunk = text[start:end]
        chunks.append((chunk, start))
        if end >= len(text):
            break
        start += chunk_chars - overlap_chars

    return chunks


def store_document_chunks(
    chunks: list[tuple[str, int]],
    filename: str,
    metadata: Optional[dict] = None
) -> int:
    """Store document chunks in Qdrant."""
    ensure_collection(settings.qdrant.documents_collection)

    texts = [c[0] for c in chunks]
    embeddings = get_embeddings(texts)

    points = []
    for i, ((text, char_offset), embedding) in enumerate(zip(chunks, embeddings)):
        payload = {
            "text": text,
            "filename": filename,
            "chunk_index": i,
            "char_offset": char_offset,
            "timestamp": int(time.time()),
        }
        if metadata:
            payload.update(metadata)

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload=payload,
            )
        )

    get_qdrant().upsert(
        collection_name=settings.qdrant.documents_collection,
        points=points
    )
    return len(points)


def retrieve_documents(query: str, top_k: Optional[int] = None) -> list[dict]:
    """Retrieve relevant document chunks."""
    ensure_collection(settings.qdrant.documents_collection)

    k = top_k or settings.retrieval.top_k_documents
    query_embedding = get_embedding(query)

    results = get_qdrant().query_points(
        collection_name=settings.qdrant.documents_collection,
        query=query_embedding,
        limit=k,
        with_payload=True,
        score_threshold=settings.retrieval.score_threshold,
    )

    return [
        {
            "text": point.payload["text"],
            "filename": point.payload["filename"],
            "chunk_index": point.payload.get("chunk_index"),
            "score": point.score,
            "type": "document"
        }
        for point in results.points
    ]


# ---------------------------------------------------------------------------
# Chat Memory (Persistent across sessions)
# ---------------------------------------------------------------------------

def store_chat_message(
    message: str,
    role: str,  # "user" or "assistant"
    session_id: Optional[str] = None,
    conversation_id: Optional[str] = None
) -> str:
    """Store a chat message in persistent memory."""
    ensure_collection(settings.qdrant.chat_memory_collection)

    embedding = get_embedding(message)
    point_id = str(uuid.uuid4())

    payload = {
        "text": message,
        "role": role,
        "session_id": session_id or "default",
        "conversation_id": conversation_id or str(uuid.uuid4()),
        "timestamp": int(time.time()),
        "datetime": datetime.now().isoformat(),
    }

    get_qdrant().upsert(
        collection_name=settings.qdrant.chat_memory_collection,
        points=[
            PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload,
            )
        ]
    )
    return point_id


def retrieve_relevant_memories(
    query: str,
    top_k: Optional[int] = None,
    session_id: Optional[str] = None
) -> list[dict]:
    """Retrieve relevant past conversations."""
    ensure_collection(settings.qdrant.chat_memory_collection)

    k = top_k or settings.retrieval.top_k_memory
    query_embedding = get_embedding(query)

    # Optional filter by session
    query_filter = None
    if session_id:
        query_filter = Filter(
            must=[FieldCondition(key="session_id", match=MatchValue(value=session_id))]
        )

    results = get_qdrant().query_points(
        collection_name=settings.qdrant.chat_memory_collection,
        query=query_embedding,
        limit=k,
        with_payload=True,
        query_filter=query_filter,
        score_threshold=settings.retrieval.score_threshold,
    )

    return [
        {
            "text": point.payload["text"],
            "role": point.payload["role"],
            "session_id": point.payload.get("session_id"),
            "datetime": point.payload.get("datetime"),
            "score": point.score,
            "type": "memory"
        }
        for point in results.points
    ]


def get_recent_conversation(
    session_id: str,
    limit: int = 10
) -> list[dict]:
    """Get recent messages from a session (ordered by time)."""
    ensure_collection(settings.qdrant.chat_memory_collection)

    results, _ = get_qdrant().scroll(
        collection_name=settings.qdrant.chat_memory_collection,
        scroll_filter=Filter(
            must=[FieldCondition(key="session_id", match=MatchValue(value=session_id))]
        ),
        limit=1000,
        with_payload=True,
        with_vectors=False,
    )

    messages = [
        {
            "text": point.payload["text"],
            "role": point.payload["role"],
            "timestamp": point.payload.get("timestamp", 0),
        }
        for point in results
    ]

    # Sort by timestamp and return most recent
    messages.sort(key=lambda x: x["timestamp"])
    return messages[-limit:]


# ---------------------------------------------------------------------------
# RAG Query with Memory
# ---------------------------------------------------------------------------

def build_rag_prompt(
    query: str,
    document_chunks: list[dict],
    memory_chunks: list[dict]
) -> str:
    """Build prompt with document context and conversation memory."""
    parts = []

    # Add document context
    if document_chunks:
        doc_context = []
        for i, chunk in enumerate(document_chunks):
            source = chunk.get("filename", "Unknown")
            doc_context.append(f"[Document {i+1}: {source}]\n{chunk['text']}")
        parts.append("## Relevant Documents:\n" + "\n\n".join(doc_context))

    # Add memory context
    if memory_chunks:
        mem_context = []
        for chunk in memory_chunks:
            role = chunk.get("role", "unknown")
            dt = chunk.get("datetime", "")
            mem_context.append(f"[{role.title()} - {dt[:16]}]: {chunk['text'][:500]}")
        parts.append("## Relevant Past Conversations:\n" + "\n".join(mem_context))

    context = "\n\n".join(parts) if parts else "No relevant context found."

    return f"""You are a helpful AI assistant with access to documents and conversation history.

{context}

## Current Question:
{query}

## Instructions:
- Answer based on the provided context when relevant
- Cite document sources using [Document N] notation
- If referencing past conversations, mention it naturally
- If the context doesn't help, answer from your general knowledge

## Response:"""


async def query_with_rag(
    query: str,
    session_id: Optional[str] = None,
    include_documents: bool = True,
    include_memory: bool = True
) -> AsyncIterator[str]:
    """
    Query with RAG - retrieves documents and memory, then streams response.
    Also stores the conversation in memory.
    """
    # Retrieve context
    document_chunks = []
    memory_chunks = []

    if include_documents:
        document_chunks = retrieve_documents(query)

    if include_memory:
        memory_chunks = retrieve_relevant_memories(query, session_id=session_id)

    # Build prompt
    prompt = build_rag_prompt(query, document_chunks, memory_chunks)

    # Store user query in memory
    conversation_id = str(uuid.uuid4())
    store_chat_message(query, "user", session_id, conversation_id)

    # Stream response from Ollama
    full_response = []
    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream(
            "POST",
            f"{settings.ollama.base_url}/api/generate",
            json={
                "model": settings.model.name,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": settings.model.temperature,
                    "num_predict": settings.model.max_tokens,
                },
            },
        ) as response:
            async for line in response.aiter_lines():
                if line.strip():
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            chunk = data["response"]
                            full_response.append(chunk)
                            yield chunk
                        if data.get("done"):
                            break
                    except json.JSONDecodeError:
                        continue

    # Store assistant response in memory
    assistant_response = "".join(full_response)
    store_chat_message(assistant_response, "assistant", session_id, conversation_id)


def query_sync(
    query: str,
    session_id: Optional[str] = None,
    include_documents: bool = True,
    include_memory: bool = True
) -> str:
    """Synchronous query (non-streaming)."""
    # Retrieve context
    document_chunks = []
    memory_chunks = []

    if include_documents:
        document_chunks = retrieve_documents(query)

    if include_memory:
        memory_chunks = retrieve_relevant_memories(query, session_id=session_id)

    # Build prompt
    prompt = build_rag_prompt(query, document_chunks, memory_chunks)

    # Store user query
    conversation_id = str(uuid.uuid4())
    store_chat_message(query, "user", session_id, conversation_id)

    # Query Ollama
    response = httpx.post(
        f"{settings.ollama.base_url}/api/generate",
        json={
            "model": settings.model.name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": settings.model.temperature,
                "num_predict": settings.model.max_tokens,
            },
        },
        timeout=120.0
    )
    response.raise_for_status()
    result = response.json()["response"]

    # Store assistant response
    store_chat_message(result, "assistant", session_id, conversation_id)

    return result


# ---------------------------------------------------------------------------
# Document Management
# ---------------------------------------------------------------------------

def list_documents() -> list[dict]:
    """List all indexed documents."""
    ensure_collection(settings.qdrant.documents_collection)

    results, _ = get_qdrant().scroll(
        collection_name=settings.qdrant.documents_collection,
        limit=10000,
        with_payload=True,
        with_vectors=False,
    )

    docs = {}
    for point in results:
        fname = point.payload["filename"]
        if fname not in docs:
            docs[fname] = {
                "filename": fname,
                "chunks": 0,
                "timestamp": point.payload.get("timestamp", 0),
            }
        docs[fname]["chunks"] += 1

    return list(docs.values())


def delete_document(filename: str) -> int:
    """Delete a document from the index."""
    results, _ = get_qdrant().scroll(
        collection_name=settings.qdrant.documents_collection,
        scroll_filter=Filter(
            must=[FieldCondition(key="filename", match=MatchValue(value=filename))]
        ),
        limit=10000,
        with_payload=False,
        with_vectors=False,
    )

    ids = [point.id for point in results]
    if ids:
        get_qdrant().delete(
            collection_name=settings.qdrant.documents_collection,
            points_selector=ids,
        )
    return len(ids)


def clear_chat_memory(session_id: Optional[str] = None) -> int:
    """Clear chat memory (optionally for a specific session)."""
    if session_id:
        results, _ = get_qdrant().scroll(
            collection_name=settings.qdrant.chat_memory_collection,
            scroll_filter=Filter(
                must=[FieldCondition(key="session_id", match=MatchValue(value=session_id))]
            ),
            limit=10000,
            with_payload=False,
            with_vectors=False,
        )
        ids = [point.id for point in results]
    else:
        results, _ = get_qdrant().scroll(
            collection_name=settings.qdrant.chat_memory_collection,
            limit=100000,
            with_payload=False,
            with_vectors=False,
        )
        ids = [point.id for point in results]

    if ids:
        get_qdrant().delete(
            collection_name=settings.qdrant.chat_memory_collection,
            points_selector=ids,
        )
    return len(ids)


def get_memory_stats() -> dict:
    """Get statistics about stored memories."""
    ensure_all_collections()

    doc_info = get_qdrant().get_collection(settings.qdrant.documents_collection)
    mem_info = get_qdrant().get_collection(settings.qdrant.chat_memory_collection)

    return {
        "documents": {
            "collection": settings.qdrant.documents_collection,
            "vectors": doc_info.vectors_count,
        },
        "chat_memory": {
            "collection": settings.qdrant.chat_memory_collection,
            "vectors": mem_info.vectors_count,
        },
        "model": settings.model.name,
        "embedding_model": settings.embedding.model,
    }
