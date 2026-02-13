# Local RAG System

**Private AI chat with persistent document memory — fully local, no API keys.**

A retrieval-augmented generation system that runs entirely on your machine. Upload PDFs, Word docs, or text files, then chat with an AI that grounds its responses in your actual documents. Uses Qdrant for enterprise-grade vector storage, Ollama for local LLM inference, and Open WebUI for the chat interface.

---

## Key Features

- **Document-grounded answers** — Responses cite your actual files, not hallucinated facts
- **Persistent memory** — Documents and conversations survive restarts via Qdrant vector database
- **Fully local** — No API keys, no cloud calls, no data leaving your machine
- **Multiple LLM support** — Swap Ollama models in config.yaml based on hardware
- **Custom frontend** — Next.js/React chat UI with document sidebar and context viewer
- **FastAPI backend** — REST API for upload, chat (streaming), and document management
- **Docker Compose stack** — One command starts Qdrant + Open WebUI

## Architecture

| Component | Role | Port |
|-----------|------|:----:|
| Ollama | LLM inference + embeddings | 11434 |
| Qdrant | Vector database | 6333 |
| Open WebUI | Chat interface | 8605 |
| FastAPI Backend | RAG API | 8000 |
| Next.js Frontend | Custom chat UI | 3000 |

## Tech Stack

Docker, FastAPI, Next.js, React, Qdrant, Ollama, Open WebUI

## Quick Start

```bash
# Start Ollama and pull models
ollama serve
ollama pull llama3.2:3b
ollama pull nomic-embed-text

# Start the Docker stack
cd local-rag-system
docker compose up -d

# Open the chat interface
open http://localhost:8605
```

See [USER_GUIDE.md](USER_GUIDE.md) for detailed setup and usage instructions.

## License

[MIT](LICENSE)
