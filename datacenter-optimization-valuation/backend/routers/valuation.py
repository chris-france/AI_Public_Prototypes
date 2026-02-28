"""Valuation API routes."""

import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from valuation_engine import calculate_valuation
from ollama_client import stream_ollama

router = APIRouter(prefix="/api")


class ValuationRequest(BaseModel):
    asking_price: float = Field(default=250_000_000, ge=1)
    claimed_capacity_mw: float = Field(default=20.0, ge=1)
    actual_utilization: float = Field(default=0.72, ge=0, le=1)
    current_pue: float = Field(default=1.42, ge=1.0, le=3.0)
    contract_quality: str = "mixed"
    contract_term_years: float = Field(default=4.5, ge=0.5)
    expansion_capacity_mw: float = Field(default=10.0, ge=0)
    building_age_years: int = Field(default=6, ge=0)
    land_owned: bool = True
    land_acres: float = Field(default=15.0, ge=0)
    region: str = "Northern Virginia (NOVA)"


@router.post("/valuation/analyze")
def analyze_valuation(req: ValuationRequest):
    return calculate_valuation(
        req.asking_price, req.claimed_capacity_mw, req.actual_utilization,
        req.current_pue, req.contract_quality, req.contract_term_years,
        req.expansion_capacity_mw, req.building_age_years, req.land_owned,
        req.land_acres, req.region,
    )


class ValuationAIRequest(BaseModel):
    prompt: str
    model: str = "llama3.2"


@router.post("/valuation/ai-analysis")
def ai_analysis(req: ValuationAIRequest):
    def generate():
        for token in stream_ollama(req.prompt, model=req.model):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
