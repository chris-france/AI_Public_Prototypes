#!/bin/bash
# Local RAG System - Launch Script

cd "$(dirname "$0")"

echo "🔍 Local RAG System"
echo "==================="
echo ""

# Check Docker
if docker info > /dev/null 2>&1; then
    echo "✓ Docker is running"
else
    echo "→ Starting Docker Desktop..."
    open -a Docker
    for i in $(seq 1 30); do
        if docker info > /dev/null 2>&1; then break; fi
        sleep 1
    done
    if ! docker info > /dev/null 2>&1; then
        echo "✗ Docker failed to start. Please open Docker Desktop manually."
        exit 1
    fi
    echo "✓ Docker is running"
fi

# Check Ollama
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama is running"
else
    echo "⚠ Ollama not running. Start it with: ollama serve"
    echo "  Then pull models: ollama pull llama3.2:3b && ollama pull nomic-embed-text"
fi

# Start containers
echo ""
echo "Starting Qdrant + Open WebUI..."
docker compose up -d

echo ""
echo "✓ Open WebUI available at http://localhost:8605"
echo "✓ Qdrant available at http://localhost:6333"
echo ""
echo "Run 'docker compose down' to stop."
