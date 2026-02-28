"""Calculator API routes."""

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from config import GPUS, CLOUD_PROVIDERS, GPU_KEY_MAP, PRESETS
from calculator import calculate

router = APIRouter(prefix="/api")


@router.get("/config")
def get_config():
    return {
        "gpus": {name: specs for name, specs in GPUS.items()},
        "cloud_providers": list(CLOUD_PROVIDERS.keys()),
        "presets": {k: v for k, v in PRESETS.items()},
        "gpu_types": list(GPUS.keys()),
    }


class CalcRequest(BaseModel):
    gpu_type: str = "RTX 4090"
    queries_per_day: int = Field(default=1000, ge=1)
    model_vram: int = Field(default=16, ge=1)
    electricity_rate: float = Field(default=0.12, ge=0)
    hardware_cost: Optional[int] = None
    secs_per_inference: float = Field(default=2.0, ge=0.1)


@router.post("/calculate")
def run_calculation(req: CalcRequest):
    return calculate(
        gpu_type=req.gpu_type,
        queries_per_day=req.queries_per_day,
        model_vram=req.model_vram,
        electricity_rate=req.electricity_rate,
        hardware_cost=req.hardware_cost,
        secs_per_inference=req.secs_per_inference,
    )
