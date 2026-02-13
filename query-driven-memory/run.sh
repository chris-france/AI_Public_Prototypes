#!/bin/bash
# QDM — Query-Driven Memory launcher
# Checks dependencies then starts Streamlit on port 8607

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "🧠 QDM — Query-Driven Memory"
echo "=============================="

# Check Ollama
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Ollama is running"
else
    echo -e "${RED}✗${NC} Ollama not running. Start it with: ollama serve"
    exit 1
fi

# Check nomic-embed-text model
if ollama list 2>/dev/null | grep -q "nomic-embed-text"; then
    echo -e "${GREEN}✓${NC} nomic-embed-text model available"
else
    echo -e "${RED}✗${NC} nomic-embed-text not found. Pulling..."
    ollama pull nomic-embed-text
fi

# Check Qdrant
if curl -s http://localhost:6333/collections > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Qdrant is running"
else
    echo -e "${RED}✗${NC} Qdrant not running. Start it with: cd ~/local-rag && docker compose up -d"
    exit 1
fi

echo ""
echo "Starting QDM on http://localhost:8607"
echo ""

python3 -m streamlit run app.py --server.port 8607 --server.headless true
