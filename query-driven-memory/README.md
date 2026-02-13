# Query-Driven Memory (QDM)

**Persistent AI memory with automatic retrieval — memories reinforce with use and decay over time.**

A Streamlit chat application that automatically retrieves relevant past conversations on every query. No manual selection needed — QDM searches all stored memories, injects relevant context, and adapts over time. Frequently accessed memories strengthen; unused memories gradually fade and get pruned.

---

## Key Features

- **Automatic retrieval** — Every query searches all stored memories for relevant context
- **Memory reinforcement** — Frequently accessed memories get stronger relevance scores
- **Decay and pruning** — Unused memories fade over time, keeping the knowledge base focused
- **Pin important memories** — Flag critical information as permanent (never decays)
- **Memory browser** — View, search, and manage all stored memories with metadata
- **Session continuity** — Pick up conversations days later with full context preserved

## How It Works

1. You ask a question
2. QDM searches Qdrant for semantically similar past conversations
3. Relevant memories are injected into the prompt as context
4. Ollama generates a response grounded in your history
5. Both your question and the response are stored as new memories
6. Retrieved memories get a relevance boost; untouched memories decay

## Tech Stack

Streamlit, Qdrant, Ollama

## Prerequisites

- [Ollama](https://ollama.ai) running locally with `llama3.2:3b` and `nomic-embed-text` pulled
- [Qdrant](https://qdrant.tech) running on port 6333 (started automatically by the Personal Demo Launcher, or via `docker compose up -d` in the local-rag-system project)

## Quick Start

```bash
cd query-driven-memory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Opens at [http://localhost:8607](http://localhost:8607).

## License

[MIT](LICENSE)
