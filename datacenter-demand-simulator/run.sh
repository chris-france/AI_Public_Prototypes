#!/bin/bash
# Datacenter Demand Simulator - Launch Script

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check Ollama status
echo ""
echo "Checking Ollama status..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama is running"
    MODELS=$(curl -s http://localhost:11434/api/tags | python3 -c "import sys, json; data=json.load(sys.stdin); print(', '.join([m['name'] for m in data.get('models', [])]))" 2>/dev/null)
    if [ -n "$MODELS" ]; then
        echo "  Available models: $MODELS"
    fi
else
    echo "⚠ Ollama is not running (AI analysis will be disabled)"
    echo "  To enable: run 'ollama serve' and 'ollama pull qwen2.5:14b'"
fi

echo ""
echo "Starting Datacenter Demand Simulator..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run Streamlit
streamlit run app.py --server.headless true --browser.gatherUsageStats false
