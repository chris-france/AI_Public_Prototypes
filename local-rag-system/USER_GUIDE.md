# Local RAG System — User Guide

**Private AI Chat with Persistent Document Memory**

---

## What Is This Tool?

The Local RAG System gives you a private, local AI chat that can answer questions from your uploaded documents. Upload PDFs, Word docs, or text files, and the AI will ground its responses in your actual content — not hallucinated facts.

Everything runs on your machine. No API keys, no cloud calls, no data leaving your network.

**What makes it different from a regular chatbot:**
- **Document-grounded answers** — responses come from your actual files, with source citations
- **Persistent memory** — conversations and documents survive browser refreshes and restarts
- **Qdrant vector database** — enterprise-grade storage that scales to thousands of documents
- **Multiple LLM options** — switch between Ollama models depending on your speed/quality needs

**Who should use this:**
- Teams that need AI-powered Q&A over internal documentation
- Organizations with sensitive data that can't touch cloud APIs
- Anyone who wants a private ChatGPT-like experience with their own documents
- Developers prototyping RAG applications

---

## Getting Started

### What You Need

- **Docker Desktop** — runs the Qdrant and Open WebUI containers
- **Ollama** — runs the AI models locally

### Quick Start

```bash
# 1. Start Ollama and pull the required models
ollama serve
ollama pull llama3.2:3b
ollama pull nomic-embed-text

# 2. Start the stack
cd ~/local-rag
docker compose up -d

# 3. Open the chat interface
open http://localhost:8605
```

On first launch, Open WebUI will ask you to create an admin account (local only — no external registration).

Docker Compose starts two containers:
- **Qdrant** — vector database on ports 6333/6334
- **Open WebUI** — chat interface on port 8605

The Personal Demos launcher (port 8501) can also start and stop this with one click.

---

## Architecture

Three components work together, all running locally:

**Ollama** — The AI brain. Runs the language models (for chat responses) and the embedding model (for converting text into searchable vectors). Runs directly on your machine, not in Docker.

**Open WebUI** — The interface. Handles chat, document upload, chunking, and embedding. When you upload a document, Open WebUI splits it into chunks, generates vector embeddings via Ollama, and stores them in Qdrant.

**Qdrant** — The memory. A production-grade vector database that stores document embeddings and enables semantic search. When you ask a question, Qdrant finds the most relevant document chunks based on meaning, not just keyword matching.

### Why Qdrant Instead of the Default

Open WebUI ships with a built-in ChromaDB for basic RAG. We replaced it with Qdrant because:

- **Scale** — ChromaDB works for a handful of docs. Qdrant handles millions of vectors with optimized indexing.
- **Persistence** — Qdrant runs as its own container with dedicated storage. The app can restart without losing any data.
- **Filtering** — Qdrant supports rich metadata filtering, which becomes critical for advanced features like session-scoped memory retrieval.
- **Production path** — If this grows beyond a demo, Qdrant scales without rearchitecting (distributed mode, replication, snapshots).

For a demo with 5 documents, you wouldn't notice the difference. For an enterprise with 5,000 documents, you absolutely would.

---

## How to Use It

### Chatting

Select a model from the dropdown in the top left corner. Type your question in the message box. Responses stream in real-time.

### Uploading Documents to a Knowledge Collection

This is how you enable RAG — document-grounded answers:

1. Click the **Workspace** icon in the left sidebar
2. Go to the **Knowledge** tab
3. Click **+ New Knowledge** (top right)
4. Name your collection (e.g., "User Guides", "Policy Docs", "Project Specs")
5. Upload files into the collection — supports PDF, DOCX, TXT, and MD

The system automatically chunks your documents, generates embeddings via Ollama, and stores them in Qdrant.

### Querying Your Documents

1. Start a new chat
2. In the message box, type `#` — your knowledge collections will appear
3. Select the collection you want to query
4. Ask your question — the AI will pull relevant content from your documents and ground its response in that content

You can reference multiple collections by typing `#` multiple times.

### Switching Models

Click the model name in the top left to switch between any models you've pulled in Ollama. The model change takes effect immediately for the next message.

---

## Model Recommendations

### Chat Models

| Model | RAM Needed | Speed | Best For |
|-------|:-:|:-:|---------|
| `llama3.2:3b` | ~4 GB | Fast | Quick tests, simple Q&A. Default. |
| `mistral:7b` | ~6 GB | Fast | Good balance of speed and reasoning |
| `qwen2.5:14b` | ~12 GB | Moderate | Best accuracy for RAG queries |
| `qwen2.5:32b` | ~24 GB | Slow | Deep analysis, 32GB+ RAM required |

**Important finding from testing:** The 3B model is too small to reliably extract answers from retrieved document chunks. It finds the right section but can't parse the details. For production RAG use, 14B or larger is recommended.

### Embedding Model

The system uses `nomic-embed-text` for converting text to vectors. This is a good general-purpose embedding model that runs quickly on any hardware.

**Note:** If you ever switch embedding models, you must re-upload all documents. Vectors from different models are incompatible.

---

## Example Use Cases

### Company Documentation Library

Upload your organization's policies, procedures, technical specs, and compliance docs into a Knowledge collection. Any employee can ask questions and get accurate answers sourced from actual company documents — no cloud, no API fees, no data leaving the building.

"What is our data retention policy for client records?"
"What are the steps for requesting infrastructure access?"

### Cross-Document Analysis

Load multiple related documents into the same collection. Ask questions that require synthesizing information across documents:

"Compare the V2.0 roadmaps across all three tools"
"Which of our demos use Ollama and what do they use it for?"

### Compliance and Audit Prep

Upload compliance frameworks, audit reports, and policy docs. Get instant answers to auditor questions grounded in your actual documentation:

"What controls do we have in place for SOC 2 Type II requirement CC6.1?"
"When was our last penetration test according to the security report?"

### Persistent Research Context

The memory persists across sessions. Monday you ask about a topic, Wednesday you come back and ask a follow-up — the system remembers the context because everything is stored in Qdrant, not browser state.

---

## Known Limitations

- **No OCR** — PDFs must contain selectable text. Scanned images won't be extracted.
- **No duplicate detection** — Re-uploading the same file creates duplicate vectors. Delete the old version first.
- **Memory grows unbounded** — Chat memory and document collections grow with every interaction. No automatic cleanup.
- **Cold start** — First query after restart is slow while Ollama loads the model into memory.
- **Context window limits** — Very large documents may exceed the model's context window after RAG injection. Smaller, focused documents work better.
- **No document updates** — Editing a source file requires deleting and re-uploading.
- **Manual collection selection** — You must use `#` to reference a knowledge collection in each chat. There's no automatic search across all stored knowledge.
- **Embedding model lock-in** — Changing the embedding model requires re-indexing all documents.
- **Single-user** — Open WebUI supports user accounts, but the system is designed for local single-user or small team use.

---

## V2.0 Roadmap — Query-Driven Memory (QDM)

The current system is powerful but passive — you upload docs, manually select them with `#`, and ask questions. V2.0 evolves this into **Query-Driven Memory (QDM)**, a fundamentally different approach to AI memory.

### The Problem

Today's RAG requires you to tell the AI where to look. QDM flips this — the AI automatically searches all stored knowledge on every query, with no manual selection needed.

### How QDM Works

QDM is a separate application that sits between you and Ollama. Every time you ask a question, QDM automatically searches all stored memories (past conversations and documents) for relevant context, injects that context into your query, and sends the enriched prompt to the model. After the response, both your question and the answer are stored as new memories.

### Key QDM Features

**Automatic retrieval** — No `#` needed. QDM searches all stored knowledge on every query.

**Memory reinforcement** — Memories that get retrieved frequently become stronger (higher relevance scores). Memories that are never accessed gradually fade.

**Decay and pruning** — Unused memories lose relevance over time and are eventually pruned. This prevents infinite growth and keeps the knowledge base focused on what actually matters.

**Pin important memories** — Flag critical information as permanent so it's never subject to decay. Investment decisions, key dates, strategic plans — pinned memories persist forever.

**Memory browser** — View, search, and manage all stored memories with metadata: when it was stored, how often it's been accessed, its current relevance score, and whether it's pinned.

### Why This Matters

The difference between RAG and QDM is the difference between a filing cabinet and an assistant. RAG is a filing cabinet — organized, searchable, but you have to know which drawer to open. QDM is an assistant who checks every relevant file automatically and brings you what you need before you ask.

This is the foundation for how AI should work with people — persistent, adaptive memory that mirrors how humans actually remember things.

---

*The Local RAG System runs entirely on your machine. No data is sent to external services. All models, embeddings, and vector storage operate locally.*
