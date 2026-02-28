"""Process manager for demo apps.

Handles starting, stopping, and status-checking of subprocess-based demos,
Docker Compose projects, and their infrastructure dependencies.
"""

import os
import signal
import socket
import subprocess
import time
import urllib.request
from typing import Optional

# Module-level state — process PIDs keyed by port number.
# Values: int (PID), "docker", or "external" (pre-existing process).
_pids = {}  # port -> PID (int), "docker", or "external"

MANAGED_PORTS = [8601, 8602, 8603, 8604, 8605, 8606, 8607]


def is_port_open(port: int) -> bool:
    """Check if a port is accepting connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", port)) == 0


def _is_http_ready(port: int) -> bool:
    """Check if port returns a real HTTP response (not just TCP open)."""
    try:
        resp = urllib.request.urlopen(
            f"http://127.0.0.1:{port}/", timeout=2,
        )
        return resp.status < 500
    except Exception:
        return False


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
    """Start Docker Desktop if not running. Return True when ready."""
    if is_docker_available():
        return True

    subprocess.run(["open", "-a", "Docker"], capture_output=True)

    for _ in range(30):
        time.sleep(1)
        if is_docker_available():
            return True

    return False


def _ensure_dependencies(demo: dict) -> Optional[str]:
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


def get_status(demo: dict) -> str:
    """Return 'running', 'stopped', or 'coming_soon'."""
    if demo.get("placeholder"):
        return "coming_soon"
    if demo["type"] == "docker":
        if is_docker_running(demo["path"]) or is_port_open(demo["port"]):
            return "running"
        return "stopped"
    return "running" if is_port_open(demo["port"]) else "stopped"


def start_demo(demo: dict) -> Optional[str]:
    """Start a demo. Return error message on failure, None on success."""
    if demo.get("placeholder"):
        return "This demo is not yet available."

    port = demo["port"]

    dep_error = _ensure_dependencies(demo)
    if dep_error:
        return dep_error

    if demo["type"] == "docker":
        if is_docker_running(demo["path"]) or is_port_open(port):
            return None
    elif is_port_open(port):
        _pids[port] = "external"
        return None

    if demo["type"] == "docker":
        if not ensure_docker_running():
            return "Failed to start Docker Desktop. Please start it manually."
        _start_docker_containers(demo)
        _pids[port] = "docker"
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
        _pids[port] = proc.pid

    # Wait for the service to be ready.
    # Docker containers bind the port instantly via the Docker proxy,
    # but the app inside may take seconds to boot. Use HTTP check for those.
    if demo["type"] == "docker":
        for _ in range(40):
            if _is_http_ready(port):
                break
            time.sleep(0.5)
    else:
        for _ in range(20):
            if is_port_open(port):
                break
            time.sleep(0.5)

    return None


def _stop_docker_containers(demo: dict) -> None:
    """Stop Docker containers by name, falling back to compose down."""
    containers = demo.get("containers", [])
    if containers:
        for name in containers:
            subprocess.run(
                ["docker", "stop", name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30,
            )
    else:
        subprocess.run(
            ["docker", "compose", "down"],
            cwd=demo["path"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30,
        )


def _start_docker_containers(demo: dict) -> None:
    """Start Docker containers by name, falling back to compose up."""
    containers = demo.get("containers", [])
    if containers:
        for name in containers:
            subprocess.run(
                ["docker", "start", name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30,
            )
    else:
        subprocess.Popen(
            ["docker", "compose", "up", "-d"],
            cwd=demo["path"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def stop_demo(demo: dict) -> None:
    """Stop a running demo."""
    port = demo["port"]

    if demo["type"] == "docker":
        _stop_docker_containers(demo)
    else:
        pid = _pids.get(port)
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

    _pids.pop(port, None)

    for _ in range(10):
        if not is_port_open(port):
            break
        time.sleep(0.3)


def stop_all() -> None:
    """Stop all managed demos aggressively."""
    for port in MANAGED_PORTS:
        for pid in _get_pids_on_port(port):
            try:
                os.kill(pid, signal.SIGKILL)
            except (OSError, ProcessLookupError):
                pass

    # Import here to avoid circular dependency at module load time
    from apps import DEMOS

    for demo in DEMOS:
        if demo["type"] == "docker":
            try:
                _stop_docker_containers(demo)
            except Exception:
                pass

    _pids.clear()


def cleanup_all() -> None:
    """Cleanup on server shutdown — same as stop_all."""
    stop_all()
