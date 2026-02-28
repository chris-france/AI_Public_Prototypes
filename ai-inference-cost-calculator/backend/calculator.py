"""Pure calculation logic for inference cost comparison."""

from __future__ import annotations

from typing import Optional

from config import GPUS, CLOUD_PROVIDERS, GPU_KEY_MAP


def calculate(
    gpu_type: str,
    queries_per_day: int,
    model_vram: int,
    electricity_rate: float,
    hardware_cost: Optional[int],
    secs_per_inference: float,
) -> dict:
    gpu = GPUS[gpu_type]
    if hardware_cost is None:
        hardware_cost = gpu["cost"]

    gpus_needed = max(1, -(-model_vram // gpu["vram"]))

    queries_per_month = queries_per_day * 30
    gpu_hours_per_month = (queries_per_month * secs_per_inference) / 3600

    # Local costs
    hardware_upfront = hardware_cost * gpus_needed
    power_monthly = (gpu["watts"] * gpus_needed * gpu_hours_per_month / 1000) * electricity_rate
    hardware_monthly = hardware_upfront / 36
    local_monthly = hardware_monthly + power_monthly
    local_3yr = hardware_upfront + power_monthly * 36

    # Cloud costs
    cloud_monthly = {}
    cloud_3yr = {}
    cloud_per_1k = {}
    for provider, rates in CLOUD_PROVIDERS.items():
        hourly = rates[GPU_KEY_MAP[gpu_type]]
        monthly = hourly * gpu_hours_per_month * gpus_needed
        cloud_monthly[provider] = monthly
        cloud_3yr[provider] = monthly * 36
        cloud_per_1k[provider] = (monthly / queries_per_month * 1000) if queries_per_month > 0 else 0

    # Cost per 1k inferences (local)
    local_per_1k = (local_monthly / queries_per_month * 1000) if queries_per_month > 0 else 0

    # Break-even
    cheapest_cloud_name = min(cloud_monthly, key=cloud_monthly.get)
    cheapest_cloud_monthly = cloud_monthly[cheapest_cloud_name]
    local_recurring = power_monthly

    breakeven_month = None
    if cheapest_cloud_monthly > local_recurring and cheapest_cloud_monthly > 0:
        breakeven_month = round(hardware_upfront / (cheapest_cloud_monthly - local_recurring), 1)

    # Cumulative cost series (0..36)
    months = list(range(0, 37))
    cumulative = {"months": months}
    cumulative["local"] = [hardware_upfront + local_recurring * m for m in months]
    for provider, monthly in cloud_monthly.items():
        cumulative[provider] = [monthly * m for m in months]

    return {
        "gpus_needed": gpus_needed,
        "gpu_hours_per_month": round(gpu_hours_per_month, 2),
        "queries_per_month": queries_per_month,
        "local": {
            "monthly": round(local_monthly, 2),
            "three_year_tco": round(local_3yr, 2),
            "per_1k": round(local_per_1k, 4),
            "hardware_upfront": hardware_upfront,
            "power_monthly": round(power_monthly, 2),
            "hardware_monthly": round(hardware_monthly, 2),
        },
        "cloud": {
            provider: {
                "monthly": round(cloud_monthly[provider], 2),
                "three_year_tco": round(cloud_3yr[provider], 2),
                "per_1k": round(cloud_per_1k[provider], 4),
            }
            for provider in CLOUD_PROVIDERS
        },
        "breakeven": {
            "month": breakeven_month,
            "vs_provider": cheapest_cloud_name,
        },
        "cumulative": cumulative,
    }
