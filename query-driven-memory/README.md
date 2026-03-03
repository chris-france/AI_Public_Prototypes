# Query-Driven Memory (QDM)

**Persistent AI memory with automatic retrieval — memories reinforce with use and decay over time.**

A React + FastAPI application that automatically retrieves relevant past conversations on every query. No manual selection needed — QDM searches all stored memories, injects relevant context, and adapts over time. Frequently accessed memories strengthen; unused memories gradually fade and get pruned.

> **Source code available upon request.** QDM is a proprietary implementation demonstrated as part of this portfolio. Contact me directly for a live demo or code walkthrough.

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

## Architecture

QDM sits between the user and Ollama, adding a persistent memory layer powered by Qdrant vector search. The memory system mirrors human memory — frequently recalled information stays sharp, unused information gradually fades, and critical information can be permanently preserved.

### Memory Lifecycle

| Event | Effect |
|-------|--------|
| New memory stored | Starts at relevance 10.0 |
| Memory retrieved as context | Score increases by 1.0 |
| Memory sits unused | Score decreases by (days idle x decay rate) |
| Score drops below 1.0, 90+ days old | Eligible for pruning |
| Memory is pinned | Immune to decay and pruning forever |

## Tech Stack

React, FastAPI, Tailwind CSS, Qdrant, Ollama

## What Makes QDM Different from RAG

| | RAG | QDM |
|---|---|---|
| **What it stores** | Documents you upload | Everything you discuss, automatically |
| **How you select context** | Manually choose with `#` | Automatic on every query |
| **Mental model** | A filing cabinet you open manually | An assistant that checks the cabinet for you |
| **Session continuity** | Each session starts fresh | Every session accesses all past sessions |

See [USER_GUIDE.md](USER_GUIDE.md) for the full feature walkthrough, interface guide, and v2.0 roadmap.
