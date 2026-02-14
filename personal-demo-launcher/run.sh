#!/bin/bash
# Personal Demo Launcher - Launch Script

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Set base directory to repo root (parent of this script's directory)
export DEMO_BASE_DIR="$(cd .. && pwd)"

echo ""
echo "Starting Personal Demo Launcher..."
echo "Demo base directory: $DEMO_BASE_DIR"
echo ""

streamlit run app.py --server.headless true --browser.gatherUsageStats false
