#!/bin/bash
set -m

echo "========================================"
echo "  AI Inference Cost Calculator"
echo "  Chris France — AI & Infrastructure"
echo "========================================"

# Resolve symlinks to find the real project directory
SOURCE="$0"
while [ -L "$SOURCE" ]; do
  DIR="$(cd "$(dirname "$SOURCE")" && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ "$SOURCE" != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$(cd "$(dirname "$SOURCE")" && pwd)"

BACKEND_PORT=3901
FRONTEND_PORT=8601
HEADLESS=false

for arg in "$@"; do
  case "$arg" in
    --headless) HEADLESS=true ;;
  esac
done

cleanup() {
  echo ""
  echo "Shutting down AI Inference Cost Calculator..."
  lsof -ti :"$BACKEND_PORT" 2>/dev/null | xargs kill -9 2>/dev/null
  lsof -ti :"$FRONTEND_PORT" 2>/dev/null | xargs kill -9 2>/dev/null
  pkill -f "uvicorn main:app.*--port $BACKEND_PORT" 2>/dev/null
  pkill -f "vite.*--port $FRONTEND_PORT" 2>/dev/null
  echo "Stopped."
}
trap cleanup INT TERM EXIT

# Kill anything already on these ports
lsof -ti :"$BACKEND_PORT" | xargs kill 2>/dev/null
lsof -ti :"$FRONTEND_PORT" | xargs kill 2>/dev/null
sleep 1

# Backend
echo ""
echo "[1/2] Starting backend (FastAPI on :$BACKEND_PORT)..."
(
  cd "$DIR/backend"
  pip3 install -r requirements.txt -q 2>/dev/null
  exec python3 -m uvicorn main:app --reload --port "$BACKEND_PORT"
) &

# Frontend
echo "[2/2] Starting frontend (Vite on :$FRONTEND_PORT)..."
(
  cd "$DIR/frontend"
  npm install --silent 2>/dev/null
  exec npx vite --host --port "$FRONTEND_PORT"
) &

# Wait for Vite to be ready, then open browser
for i in $(seq 1 30); do
  if curl -s http://localhost:"$FRONTEND_PORT" > /dev/null 2>&1; then
    echo ""
    echo "  AI Inference Cost Calculator is ready:"
    echo "    Local:  http://localhost:$FRONTEND_PORT"
    echo ""
    echo "    Press Ctrl+C to stop."
    echo ""
    if [ "$HEADLESS" = false ]; then
      open "http://localhost:$FRONTEND_PORT"
    fi
    break
  fi
  sleep 1
done

wait
