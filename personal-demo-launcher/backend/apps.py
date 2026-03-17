"""Demo app registry.

Each entry defines a demo application that can be managed by the launcher.
Paths are resolved relative to DEMO_BASE_DIR (defaults to $HOME).
"""

import os
from pathlib import Path

BASE_DIR = Path(os.environ.get("DEMO_BASE_DIR", Path.home()))

DEMOS = [
    {
        "id": "inference-cost-calculator",
        "name": "Inference Cost Calculator",
        "path": str(BASE_DIR / "AI_Public_Prototypes" / "ai-inference-cost-calculator"),
        "description": (
            "Compare TCO for local GPU inference vs cloud providers over "
            "36 months. Break-even analysis, hardware amortization, and "
            "cost-per-1K inference comparison."
        ),
        "tech": ["React", "FastAPI", "Recharts", "Tailwind"],
        "port": 8601,
        "cmd": "bash run.sh --headless",
        "type": "react-fastapi",
    },
    {
        "id": "datacenter-demand-simulator",
        "name": "Datacenter Demand Simulator",
        "path": str(BASE_DIR / "AI_Public_Prototypes" / "datacenter-demand-simulator"),
        "description": (
            "Forecast enterprise datacenter capacity across compute, storage, "
            "power, and cooling. Multi-scenario projections with decision "
            "timeline and AI-powered strategic analysis."
        ),
        "tech": ["React", "FastAPI", "Recharts", "Tailwind", "Ollama"],
        "port": 8602,
        "cmd": "bash run.sh --headless",
        "type": "react-fastapi",
    },
    {
        "id": "datacenter-optimization-valuation",
        "name": "Datacenter Optimization & Valuation",
        "path": str(BASE_DIR / "AI_Public_Prototypes" / "datacenter-optimization-valuation"),
        "description": (
            "PE/VC datacenter investment analysis. Compare ground-up, modular, "
            "and hybrid builds with M&A asset valuation across 14 global markets."
        ),
        "tech": ["React", "FastAPI", "Recharts", "Tailwind", "Ollama"],
        "port": 8603,
        "cmd": "bash run.sh --headless",
        "type": "react-fastapi",
    },
    {
        "id": "model-security-scanner",
        "name": "Model Security Scanner",
        "path": str(BASE_DIR / "AI_Public_Prototypes" / "model-security-scanner"),
        "description": (
            "Test LLM security across 10 attack categories. Scans Ollama "
            "models and Claude API for vulnerabilities."
        ),
        "tech": ["React", "FastAPI", "Recharts", "Tailwind", "Ollama"],
        "port": 8604,
        "cmd": "bash run.sh --headless",
        "type": "react-fastapi",
    },
    {
        "id": "local-rag-system",
        "name": "Local RAG System",
        "path": str(BASE_DIR / "AI_Public_Prototypes" / "local-rag-system"),
        "description": (
            "Open WebUI + Qdrant for persistent memory. Chat with Ollama "
            "models, upload docs, memory persists across sessions."
        ),
        "tech": ["Open WebUI", "Qdrant", "Ollama", "Docker"],
        "port": 8605,
        "type": "docker",
        "containers": ["local-rag-webui", "local-rag-qdrant"],
    },
    {
        "id": "n8n-workflow-canvas",
        "name": "n8n Workflow Canvas",
        "path": str(BASE_DIR),
        "description": (
            "Visual workflow automation. Connect APIs, build automations, "
            "and orchestrate tasks with a node-based canvas."
        ),
        "tech": ["n8n", "Docker", "Node.js"],
        "port": 8606,
        "cmd": "N8N_PORT={port} npx n8n start",
        "type": "n8n",
        "placeholder": True,
    },
    {
        "id": "query-driven-memory",
        "name": "Query-Driven Memory (QDM)",
        "path": str(BASE_DIR / "AI_Confidential_Code" / "query-driven-memory"),
        "description": (
            "Persistent AI memory system. Automatically retrieves relevant "
            "past conversations on every query — no manual selection needed. "
            "Memories reinforce with use and decay over time."
        ),
        "tech": ["React", "FastAPI", "Tailwind", "Qdrant", "Ollama"],
        "port": 8607,
        "cmd": "bash run.sh --headless",
        "type": "react-fastapi",
        "requires": [
            {
                "port": 6333,
                "docker_project": str(BASE_DIR / "AI_Public_Prototypes" / "local-rag-system"),
                "service": "qdrant",
                "label": "Qdrant",
            },
        ],
    },
    {
        "id": "betty-email-assistant",
        "name": "Betty — Email Assistant",
        "path": str(BASE_DIR / "AI_Confidential_Code" / "betty"),
        "description": (
            "CJ's executive assistant module. Monitors all 3 email accounts "
            "(AECOM, christopherfrance.com, Gmail), classifies with Ollama, "
            "sends prioritized briefs to Outlook, and pushes urgent items to phone."
        ),
        "tech": ["Python", "Ollama", "SQLite", "IMAP", "Pushover"],
        "port": 8608,
        "cmd": "bash run.sh --headless",
        "type": "react-fastapi",
        "placeholder": True,
    },
]

DEMOS_BY_ID = {d["id"]: d for d in DEMOS}
