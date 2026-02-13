"""Personal Demo Launcher.

Streamlit dashboard to manage and launch personal demo projects from a single
interface. Starts and stops Streamlit apps, Docker containers, and other
services. Kills all managed processes on exit or Ctrl+C.

Configure the base directory for demo projects via the DEMO_BASE_DIR environment
variable. Defaults to the current user's home directory.
"""

import atexit
import os
import signal
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# Base directory — all demo paths are relative to this
# ---------------------------------------------------------------------------

BASE_DIR = Path(os.environ.get("DEMO_BASE_DIR", Path.home()))

# ---------------------------------------------------------------------------
# Managed ports — killed on launcher exit
# ---------------------------------------------------------------------------

_MANAGED_PORTS = [8601, 8602, 8603, 8604, 8605, 8606, 8607]
_DOCKER_PROJECTS = [str(BASE_DIR / "local-rag")]


def _get_pids_on_port(port: int) -> list[int]:
    """Return all PIDs listening on a given port."""
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True, text=True, timeout=5,
        )
        return [int(p) for p in result.stdout.strip().split("\n") if p.strip()]
    except Exception:
        return []


def _cleanup_all():
    """Kill all managed processes and stop Docker containers on exit."""
    for port in _MANAGED_PORTS:
        for pid in _get_pids_on_port(port):
            try:
                os.kill(pid, signal.SIGKILL)
            except (OSError, ProcessLookupError):
                pass

    for path in _DOCKER_PROJECTS:
        try:
            subprocess.run(
                ["docker", "compose", "down"],
                cwd=path,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10,
            )
        except Exception:
            pass


# Register cleanup on exit
atexit.register(_cleanup_all)

# Handle Ctrl+C
if threading.current_thread() is threading.main_thread():
    def _sigint_handler(signum, frame):
        """Gracefully shut down all demos before exiting."""
        _cleanup_all()
        sys.exit(0)

    signal.signal(signal.SIGINT, _sigint_handler)
    signal.signal(signal.SIGTERM, _sigint_handler)


# ---------------------------------------------------------------------------
# Page config (must be first Streamlit call)
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Personal Demos",
    page_icon="⚡",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Demo registry
# ---------------------------------------------------------------------------

DEMOS = [
    {
        "name": "Inference Cost Calculator",
        "path": str(BASE_DIR / "ai-inference-calculator"),
        "description": "Compare TCO for local GPU inference vs cloud providers over 36 months. Break-even analysis, hardware amortization, and cost-per-1K inference comparison.",
        "tech": ["Streamlit", "Plotly", "Pandas"],
        "port": 8601,
        "cmd": "python3 -m streamlit run app.py --server.port {port} --server.headless true",
        "type": "streamlit",
    },
    {
        "name": "Datacenter Demand Simulator",
        "path": str(BASE_DIR / "datacenter-demand-simulator"),
        "description": "Forecast enterprise datacenter capacity across compute, storage, power, and cooling. Multi-scenario projections with decision timeline and AI-powered strategic analysis.",
        "tech": ["Streamlit", "Plotly", "Pandas", "NumPy", "Ollama"],
        "port": 8602,
        "cmd": "python3 -m streamlit run app.py --server.port {port} --server.headless true",
        "type": "streamlit",
    },
    {
        "name": "Datacenter Optimization & Valuation",
        "path": str(BASE_DIR / "datacenter-deployment-optimizer"),
        "description": "PE/VC datacenter investment analysis. Compare ground-up, modular, and hybrid builds with M&A asset valuation across 14 global markets.",
        "tech": ["Streamlit", "Plotly", "Pandas", "NumPy", "Ollama"],
        "port": 8603,
        "cmd": "python3 -m streamlit run app.py --server.port {port} --server.headless true",
        "type": "streamlit",
    },
    {
        "name": "Model Security Scanner",
        "path": str(BASE_DIR / "ai-security-validator"),
        "description": "Test LLM security across 10 attack categories. Scans Ollama models and Claude API for vulnerabilities.",
        "tech": ["Streamlit", "Plotly", "Ollama", "Anthropic API"],
        "port": 8604,
        "cmd": "python3 -m streamlit run app.py --server.port {port} --server.headless true",
        "type": "streamlit",
    },
    {
        "name": "Local RAG System",
        "path": str(BASE_DIR / "local-rag"),
        "description": "Open WebUI + Qdrant for persistent memory. Chat with Ollama models, upload docs, memory persists across sessions.",
        "tech": ["Open WebUI", "Qdrant", "Ollama", "Docker"],
        "port": 8605,
        "type": "docker",
    },
    {
        "name": "n8n Workflow Canvas",
        "path": str(BASE_DIR),
        "description": "Visual workflow automation. Connect APIs, build automations, and orchestrate tasks with a node-based canvas.",
        "tech": ["n8n", "Docker", "Node.js"],
        "port": 8606,
        "cmd": "N8N_PORT={port} npx n8n start",
        "type": "n8n",
        "placeholder": True,
    },
    {
        "name": "Query-Driven Memory (QDM)",
        "path": str(BASE_DIR / "qdmem"),
        "description": "Persistent AI memory system. Automatically retrieves relevant past conversations on every query — no manual selection needed. Memories reinforce with use and decay over time.",
        "tech": ["Streamlit", "Qdrant", "Ollama"],
        "port": 8607,
        "cmd": "python3 -m streamlit run app.py --server.port {port} --server.headless true",
        "type": "streamlit",
        "requires": [
            {"port": 6333, "docker_project": str(BASE_DIR / "local-rag"), "service": "qdrant", "label": "Qdrant"},
        ],
    },
]

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

if "pids" not in st.session_state:
    st.session_state.pids = {}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def is_port_open(port: int) -> bool:
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", port)) == 0


def is_docker_running(project_path: str) -> bool:
    """Check if Docker Compose containers for a project are running."""
    try:
        result = subprocess.run(
            ["docker", "compose", "ps", "-q"],
            cwd=project_path,
            capture_output=True, text=True, timeout=5,
        )
        return bool(result.stdout.strip())
    except Exception:
        return False


def is_docker_available() -> bool:
    """Check if the Docker daemon is running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True, timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False


def ensure_docker_running() -> bool:
    """Start Docker Desktop if not running. Return True when Docker is ready."""
    if is_docker_available():
        return True

    subprocess.run(["open", "-a", "Docker"], capture_output=True)

    for _ in range(30):
        time.sleep(1)
        if is_docker_available():
            return True

    return False


def ensure_dependencies(demo: dict) -> str | None:
    """Start any required infrastructure for a demo. Return error or None."""
    for dep in demo.get("requires", []):
        if is_port_open(dep["port"]):
            continue
        if not ensure_docker_running():
            return f"Failed to start Docker Desktop (needed for {dep['label']})."
        subprocess.Popen(
            ["docker", "compose", "up", "-d", dep["service"]],
            cwd=dep["docker_project"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for _ in range(30):
            if is_port_open(dep["port"]):
                break
            time.sleep(0.5)
        else:
            return f"{dep['label']} failed to start on port {dep['port']}."
    return None


def start_demo(demo: dict, wait: bool = True) -> str | None:
    """Start a demo. Return error message on failure, None on success."""
    port = demo["port"]

    dep_error = ensure_dependencies(demo)
    if dep_error:
        return dep_error

    if demo["type"] == "docker":
        if is_docker_running(demo["path"]) or is_port_open(port):
            return None
    elif is_port_open(port):
        st.session_state.pids[port] = "external"
        return None

    if demo["type"] == "docker":
        if not ensure_docker_running():
            return "Failed to start Docker Desktop. Please start it manually."
        subprocess.Popen(
            ["docker", "compose", "up", "-d"],
            cwd=demo["path"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        st.session_state.pids[port] = "docker"
    else:
        cmd = demo["cmd"].format(port=port)
        proc = subprocess.Popen(
            cmd,
            shell=True,
            cwd=demo["path"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid,
        )
        st.session_state.pids[port] = proc.pid

    if wait:
        for _ in range(20):
            if is_port_open(port):
                break
            time.sleep(0.5)

    return None


def stop_demo(demo: dict):
    """Stop a running demo by port or Docker Compose project."""
    port = demo["port"]

    if demo["type"] == "docker":
        subprocess.run(
            ["docker", "compose", "down"],
            cwd=demo["path"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30,
        )
    else:
        pid = st.session_state.pids.get(port)
        if pid and pid not in ("external", "docker"):
            try:
                os.killpg(os.getpgid(pid), signal.SIGTERM)
            except (ProcessLookupError, PermissionError, OSError):
                pass

        subprocess.run(
            f"lsof -ti:{port} | xargs kill -9 2>/dev/null",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    st.session_state.pids.pop(port, None)

    for _ in range(10):
        if not is_port_open(port):
            break
        time.sleep(0.3)


def stop_all_demos():
    """Stop all running demos aggressively."""
    for port in _MANAGED_PORTS:
        for pid in _get_pids_on_port(port):
            try:
                os.kill(pid, signal.SIGKILL)
            except (OSError, ProcessLookupError):
                pass

    for demo in DEMOS:
        if demo["type"] == "docker":
            try:
                subprocess.run(
                    ["docker", "compose", "down"],
                    cwd=demo["path"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=10,
                )
            except Exception:
                pass

    st.session_state.pids = {}


def is_demo_running(demo: dict) -> bool:
    """Check if a demo is currently running."""
    if demo["type"] == "docker":
        return is_docker_running(demo["path"]) or is_port_open(demo["port"])
    return is_port_open(demo["port"])


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

st.markdown("""
<style>
    .status-running { color: #22c55e; font-weight: 600; }
    .status-stopped { color: #6b7280; }
    .status-coming { color: #f59e0b; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Personal Demos")
st.caption("Manage and launch personal demo projects — port 8501")

# Global controls
gcol1, gcol2, _ = st.columns([1, 1, 4])
with gcol1:
    if st.button("▶ Start All", use_container_width=True, type="primary"):
        for d in DEMOS:
            if not d.get("placeholder", False):
                start_demo(d, wait=False)
        time.sleep(5)
        st.rerun()

with gcol2:
    if st.button("⏹ Stop All", use_container_width=True, type="secondary"):
        stop_all_demos()
        time.sleep(1)
        st.rerun()

st.divider()

# Demo grid
cols_per_row = 4
for i in range(0, len(DEMOS), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, col in enumerate(cols):
        idx = i + j
        if idx >= len(DEMOS):
            break

        demo = DEMOS[idx]
        port = demo["port"]
        is_placeholder = demo.get("placeholder", False)
        running = is_demo_running(demo) if not is_placeholder else False

        with col:
            with st.container(border=True):
                if is_placeholder:
                    status = "🔜 Coming Soon"
                    status_color = "orange"
                elif running:
                    status = "🟢 Running"
                    status_color = "green"
                else:
                    status = "⚫ Stopped"
                    status_color = "gray"

                st.markdown(f"### {demo['name']}")
                st.caption(f":{status_color}[{status}]  `port {port}`")

                st.markdown(
                    f"<p style='font-size:0.85rem;color:#9ca3af;margin:0.5rem 0'>{demo['description']}</p>",
                    unsafe_allow_html=True,
                )

                tags = " ".join(f"`{t}`" for t in demo["tech"])
                st.markdown(tags)

                b1, b2, b3 = st.columns(3)
                with b1:
                    if running:
                        st.button(
                            ":white_check_mark: Running",
                            key=f"start_{idx}",
                            disabled=True,
                            use_container_width=True,
                        )
                    else:
                        start_disabled = is_placeholder
                        if st.button(
                            ":rocket: Start",
                            key=f"start_{idx}",
                            type="primary",
                            disabled=start_disabled,
                            use_container_width=True,
                        ):
                            with st.spinner("Starting..."):
                                error = start_demo(demo, wait=True)
                            if error:
                                st.error(error)
                            else:
                                st.rerun()

                with b2:
                    stop_disabled = not running or is_placeholder
                    if st.button(
                        ":stop_sign: Stop",
                        key=f"stop_{idx}",
                        disabled=stop_disabled,
                        use_container_width=True,
                    ):
                        with st.spinner("Stopping..."):
                            stop_demo(demo)
                        st.rerun()

                with b3:
                    url = f"http://localhost:{port}"
                    if running:
                        st.link_button(
                            ":globe_with_meridians: Open",
                            url=url,
                            use_container_width=True,
                        )
                    else:
                        st.button(
                            ":globe_with_meridians: Open",
                            key=f"open_{idx}",
                            disabled=True,
                            use_container_width=True,
                        )

# Footer
st.divider()
st.caption("💡 Press Ctrl+C in terminal to stop launcher and all demos")
