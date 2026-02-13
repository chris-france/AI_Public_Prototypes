"""
FastAPI application for the Local RAG System.
Provides REST endpoints for document upload, chat (streaming), and document management.
"""

import os
import json
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from config import settings
from ingest import extract_text, get_page_map
from rag import (
    ensure_collection,
    chunk_text,
    store_chunks,
    retrieve,
    generate_stream,
    list_documents,
    delete_document,
)

SAMPLE_DIR = Path(__file__).parent.parent / "sample_docs"


def ingest_sample_docs():
    """Load sample documents on first run if collection is empty."""
    docs = list_documents()
    if docs:
        return
    if not SAMPLE_DIR.exists():
        return
    for f in SAMPLE_DIR.iterdir():
        if f.suffix in (".txt", ".pdf", ".docx"):
            content = f.read_bytes()
            text = extract_text(f.name, content)
            page_map = get_page_map(f.name, content)
            chunks = chunk_text(text)
            store_chunks(chunks, f.name, page_map)
            print(f"Ingested sample: {f.name}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_collection()
    ingest_sample_docs()
    yield


app = FastAPI(title="Local RAG System", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_EXTENSIONS = {"pdf", "txt", "docx"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = file.filename.rsplit(".", 1)[-1].lower() if file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported file type. Allowed: {ALLOWED_EXTENSIONS}")

    content = await file.read()
    try:
        text = extract_text(file.filename, content)
    except Exception as e:
        raise HTTPException(400, f"Failed to parse file: {e}")

    page_map = get_page_map(file.filename, content)
    chunks = chunk_text(text)
    count = store_chunks(chunks, file.filename, page_map)
    return {"filename": file.filename, "chunks": count}


class ChatRequest(BaseModel):
    query: str
    top_k: int = 5
    temperature: float = 0.7
    chunk_size: int = 512


@app.post("/chat")
async def chat(req: ChatRequest):
    if not req.query.strip():
        raise HTTPException(400, "Query cannot be empty")

    context_chunks = retrieve(req.query, top_k=req.top_k)

    async def stream():
        # First send context as a JSON line
        yield json.dumps({"type": "context", "chunks": context_chunks}) + "\n"
        # Then stream the response
        async for token in generate_stream(
            req.query, context_chunks, temperature=req.temperature
        ):
            yield json.dumps({"type": "token", "content": token}) + "\n"
        yield json.dumps({"type": "done"}) + "\n"

    return StreamingResponse(stream(), media_type="application/x-ndjson")


@app.get("/collections")
async def get_collections():
    return {"documents": list_documents()}


@app.delete("/collections/{filename}")
async def remove_document(filename: str):
    count = delete_document(filename)
    if count == 0:
        raise HTTPException(404, "Document not found")
    return {"deleted": count, "filename": filename}


@app.get("/health")
async def health():
    return {"status": "ok"}
