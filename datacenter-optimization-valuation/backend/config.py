"""Configuration — ported from original."""

FINANCIAL_ASSUMPTIONS = {
    "discount_rate": 0.10, "inflation_rate": 0.025, "power_escalation": 0.03,
    "labor_escalation": 0.035, "depreciation_years": 15, "tax_rate": 0.25,
    "debt_ratio": 0.60, "cost_of_debt": 0.065,
}

REDUNDANCY_SPECS = {
    "N": {"description": "No redundancy", "uptime_target": 0.9950, "tier_equivalent": "Tier I", "cost_multiplier": 1.0},
    "N+1": {"description": "Single redundant component", "uptime_target": 0.9982, "tier_equivalent": "Tier II/III", "cost_multiplier": 1.15},
    "2N": {"description": "Full redundancy", "uptime_target": 0.9995, "tier_equivalent": "Tier III+", "cost_multiplier": 1.45},
    "2N+1": {"description": "Full redundancy plus spare", "uptime_target": 0.9999, "tier_equivalent": "Tier IV", "cost_multiplier": 1.60},
}

COOLING_SPECS = {
    "air": {"description": "Traditional air cooling", "max_density_kw": 15, "pue_impact": 0.0, "cost_multiplier": 1.0},
    "liquid": {"description": "Liquid cooling", "max_density_kw": 100, "pue_impact": -0.15, "cost_multiplier": 1.18},
    "hybrid": {"description": "Combined air and liquid", "max_density_kw": 50, "pue_impact": -0.08, "cost_multiplier": 1.12},
}
