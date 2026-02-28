"""Simulation API routes."""

import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from config import INDUSTRY_BASELINES, WORKLOAD_MULTIPLIERS, COMPLIANCE_REQUIREMENTS, SCENARIOS
from simulator import DatacenterSimulator
from ollama_client import is_ollama_available, get_available_models, stream_ollama, build_capacity_prompt

router = APIRouter(prefix="/api")


@router.get("/config")
def get_config():
    return {
        "industries": list(INDUSTRY_BASELINES.keys()),
        "workloads": list(WORKLOAD_MULTIPLIERS.keys()),
        "compliance": {k: v["description"] for k, v in COMPLIANCE_REQUIREMENTS.items()},
        "scenarios": {k: v["description"] for k, v in SCENARIOS.items()},
        "ollama_available": is_ollama_available(),
        "ollama_models": get_available_models(),
    }


class SimulateRequest(BaseModel):
    industry: str = "Technology"
    employees: int = Field(default=5000, ge=100)
    growth_rate: float = Field(default=0.15, ge=0, le=1)
    workloads: list[str] = ["General Compute", "Database Operations", "AI/ML Inference"]
    compliance: list[str] = ["SOC 2 Type II"]
    horizon_years: int = Field(default=5, ge=3, le=10)
    ai_intensity: float = Field(default=0.5, ge=0, le=1)


@router.post("/simulate")
def simulate(req: SimulateRequest):
    sim = DatacenterSimulator(
        industry=req.industry,
        employees=req.employees,
        growth_rate=req.growth_rate,
        workloads=req.workloads,
        compliance=req.compliance,
        horizon_years=req.horizon_years,
        ai_intensity=req.ai_intensity,
    )
    return {
        "scenarios": sim.run_all_scenarios(),
        "summary": sim.get_summary_stats(),
        "comparison": sim.get_scenario_comparison(),
        "decision_points": sim.calculate_decision_points(),
    }


class AnalysisRequest(BaseModel):
    summary: dict
    model: str = "qwen2.5:14b"


@router.post("/ai-analysis")
def ai_analysis(req: AnalysisRequest):
    prompt = build_capacity_prompt(req.summary)

    def generate():
        for token in stream_ollama(prompt, model=req.model):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
