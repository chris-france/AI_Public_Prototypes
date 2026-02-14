#!/bin/bash
# AI Inference Cost Calculator - Launch Script

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting Inference Cost Calculator..."
echo ""

streamlit run app.py --server.headless true --browser.gatherUsageStats false
