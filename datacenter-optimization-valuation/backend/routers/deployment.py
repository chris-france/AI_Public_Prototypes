"""Deployment analysis API routes."""

import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from market_data import MARKET_BENCHMARKS, DEPLOYMENT_APPROACHES
from config import REDUNDANCY_SPECS, COOLING_SPECS
from deployment_calculator import calculate_all_approaches
from ollama_client import is_ollama_available, get_models, stream_ollama

router = APIRouter(prefix="/api")


@router.get("/deployment/config")
def deployment_config():
    return {
        "regions": list(MARKET_BENCHMARKS.keys()),
        "redundancy": {k: v["description"] for k, v in REDUNDANCY_SPECS.items()},
        "cooling": {k: v["description"] for k, v in COOLING_SPECS.items()},
        "approaches": {k: v["name"] for k, v in DEPLOYMENT_APPROACHES.items()},
        "ollama_available": is_ollama_available(),
        "ollama_models": get_models(),
    }


class DeploymentRequest(BaseModel):
    total_power_mw: float = Field(default=20.0, ge=1)
    rack_count: int = Field(default=500, ge=10)
    timeline_urgency: str = "standard"
    budget_constraint: float = Field(default=200.0, ge=10)
    region: str = "Northern Virginia (NOVA)"
    redundancy_level: str = "N+1"
    cooling_type: str = "air"


@router.post("/deployment/analyze")
def analyze_deployment(req: DeploymentRequest):
    return calculate_all_approaches(
        req.total_power_mw, req.rack_count, req.timeline_urgency,
        req.budget_constraint, req.region, req.redundancy_level, req.cooling_type,
    )


class AIRequest(BaseModel):
    prompt: str
    model: str = "llama3.2"


@router.post("/deployment/ai-recommendation")
def ai_recommendation(req: AIRequest):
    def generate():
        for token in stream_ollama(req.prompt, model=req.model):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
