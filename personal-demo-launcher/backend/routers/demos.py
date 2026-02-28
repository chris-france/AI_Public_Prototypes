"""API endpoints for demo management."""

from fastapi import APIRouter, HTTPException

from apps import DEMOS, DEMOS_BY_ID
from process_manager import get_status, start_demo, stop_demo, stop_all

router = APIRouter(prefix="/api/apps", tags=["demos"])


def _serialize(demo: dict) -> dict:
    """Build the JSON representation of a demo app."""
    return {
        "id": demo["id"],
        "name": demo["name"],
        "description": demo["description"],
        "tech": demo["tech"],
        "port": demo["port"],
        "type": demo["type"],
        "placeholder": demo.get("placeholder", False),
        "status": get_status(demo),
    }


@router.get("")
def list_apps():
    """Return all demo apps with their current status."""
    return [_serialize(d) for d in DEMOS]


# Static routes MUST come before parameterized routes to avoid
# FastAPI matching "start-all" as an {app_id} value.


@router.post("/start-all")
def start_all_apps():
    """Start all non-placeholder demo apps."""
    results = []
    for demo in DEMOS:
        if not demo.get("placeholder"):
            start_demo(demo)
        results.append(_serialize(demo))
    return results


@router.post("/stop-all")
def stop_all_apps():
    """Stop all running demos."""
    stop_all()
    return [_serialize(d) for d in DEMOS]


@router.post("/{app_id}/start")
def start_app(app_id: str):
    """Start a single demo app."""
    demo = DEMOS_BY_ID.get(app_id)
    if not demo:
        raise HTTPException(status_code=404, detail="App not found")
    error = start_demo(demo)
    if error:
        raise HTTPException(status_code=500, detail=error)
    return _serialize(demo)


@router.post("/{app_id}/stop")
def stop_app(app_id: str):
    """Stop a single demo app."""
    demo = DEMOS_BY_ID.get(app_id)
    if not demo:
        raise HTTPException(status_code=404, detail="App not found")
    stop_demo(demo)
    return _serialize(demo)
