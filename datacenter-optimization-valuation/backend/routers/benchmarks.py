"""Benchmarks API routes."""

from fastapi import APIRouter
from market_data import MARKET_BENCHMARKS

router = APIRouter(prefix="/api")


@router.get("/benchmarks")
def get_benchmarks():
    return {
        region: {
            "region": region,
            "capex_per_mw": data["capex_per_mw"],
            "power_cost_kwh": data["power_cost_kwh"],
            "avg_pue": data["avg_pue"],
            "market_utilization": data["market_utilization"],
            "transaction_comp_per_mw": data["transaction_comp_per_mw"],
            "demand_growth": data["demand_growth"],
            "tier": data["tier"],
            "land_cost_per_acre": data["land_cost_per_acre"],
        }
        for region, data in MARKET_BENCHMARKS.items()
    }
