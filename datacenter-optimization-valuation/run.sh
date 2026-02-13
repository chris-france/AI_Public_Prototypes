#!/bin/bash

# Datacenter Deployment Optimizer - Launch Script

echo "=============================================="
echo "  Datacenter Deployment Optimizer"
echo "  PE/VC Investment Analysis Platform"
echo "=============================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Checking dependencies..."
pip install -q -r requirements.txt

# Check Ollama status
echo ""
echo "Checking Ollama status..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama is running"
    echo "  Available models:"
    curl -s http://localhost:11434/api/tags | python3 -c "import sys, json; models = json.load(sys.stdin).get('models', []); [print(f'    - {m[\"name\"]}') for m in models]" 2>/dev/null || echo "    (unable to list models)"
else
    echo "⚠ Ollama not detected at localhost:11434"
    echo "  AI recommendations will use fallback logic"
    echo "  To enable AI: brew install ollama && ollama serve"
fi

echo ""
echo "Starting Streamlit application..."
echo "=============================================="
echo ""

# Run Streamlit
streamlit run app.py --server.headless true --browser.gatherUsageStats false
