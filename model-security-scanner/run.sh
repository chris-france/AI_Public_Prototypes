#!/bin/bash
# Model Security Scanner - Launch Script

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check Ollama status
echo ""
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama is running"
else
    echo "⚠ Ollama not running — local model scanning will be unavailable"
    echo "  To enable: ollama serve"
fi

echo ""
echo "Starting Model Security Scanner..."
echo ""

streamlit run app.py --server.headless true --browser.gatherUsageStats false
