"""Deployment calculator — ported from original DeploymentCalculator class."""

from market_data import MARKET_BENCHMARKS, DEPLOYMENT_APPROACHES


def calculate_all_approaches(total_power_mw, rack_count, timeline_urgency, budget_constraint, region, redundancy_level, cooling_type):
    benchmarks = MARKET_BENCHMARKS[region]
    results = {}
    for key, config in DEPLOYMENT_APPROACHES.items():
        results[key] = _calc(key, config, total_power_mw, rack_count, timeline_urgency, budget_constraint, region, redundancy_level, cooling_type, benchmarks)
    return results


def _calc(key, config, total_power_mw, rack_count, timeline_urgency, budget_constraint, region, redundancy_level, cooling_type, benchmarks):
    capex = total_power_mw * benchmarks["capex_per_mw"] * config["capex_multiplier"]
    redundancy_mults = {"N": 1.0, "N+1": 1.15, "2N": 1.45, "2N+1": 1.60}
    capex *= redundancy_mults.get(redundancy_level, 1.0)
    cooling_mults = {"air": 1.0, "liquid": 1.18, "hybrid": 1.12}
    capex *= cooling_mults.get(cooling_type, 1.0)
    capex *= benchmarks["labor_multiplier"]

    urgency_factor = {"standard": 1.0, "accelerated": 0.85, "critical": 0.70}
    timeline = config["base_timeline_months"] * urgency_factor.get(timeline_urgency, 1.0)
    if timeline_urgency == "accelerated": capex *= 1.08
    elif timeline_urgency == "critical": capex *= 1.18

    annual_power = total_power_mw * 1000 * 8760 * benchmarks["power_cost_kwh"] * config["typical_pue"] * 0.85
    annual_maintenance = capex * 0.025
    annual_staffing = total_power_mw * 150_000
    annual_insurance = capex * 0.005
    annual_other = capex * 0.01
    total_annual_opex = (annual_power + annual_maintenance + annual_staffing + annual_insurance + annual_other) * config["opex_efficiency"]
    ten_year_opex = total_annual_opex * 10

    depreciation_factor = 0.65
    market_appreciation = (1 + benchmarks["demand_growth"]) ** 5
    resale_value = capex * depreciation_factor * config["resale_premium"] * market_appreciation

    risk_score = len(config["risk_factors"]) * 8
    urgency_risk = {"standard": 0, "accelerated": 10, "critical": 25}
    risk_score += urgency_risk.get(timeline_urgency, 0)
    if benchmarks["tier"] == 2: risk_score += 5
    if total_power_mw > 100: risk_score += 20
    elif total_power_mw > 50: risk_score += 10
    risk_score = min(100, max(0, risk_score))

    revenue_per_kw_month = 120 * benchmarks["market_premium"]
    annual_revenue = total_power_mw * 1000 * revenue_per_kw_month * 0.75 * 12
    ten_year_revenue = annual_revenue * 10
    total_cost = capex + ten_year_opex
    roi = ((ten_year_revenue - total_cost + resale_value) / capex) * 100

    timeline_reqs = {"standard": 30, "accelerated": 18, "critical": 12}

    return {
        "name": config["name"],
        "capex": round(capex, 2),
        "capex_per_mw": round(capex / total_power_mw, 2),
        "annual_opex": round(total_annual_opex, 2),
        "ten_year_opex": round(ten_year_opex, 2),
        "total_10yr_cost": round(capex + ten_year_opex, 2),
        "timeline_months": round(timeline),
        "timeline_variance": config["timeline_variance"],
        "flexibility_score": config["flexibility_score"],
        "resale_value": round(resale_value, 2),
        "risk_score": risk_score,
        "risk_factors": config["risk_factors"],
        "roi_percent": round(roi, 1),
        "pue": config["typical_pue"],
        "scalability": config["scalability"],
        "customization": config["customization"],
        "annual_power_cost": round(annual_power, 2),
        "annual_maintenance": round(annual_maintenance, 2),
        "meets_budget": capex <= budget_constraint * 1_000_000,
        "meets_timeline": timeline <= timeline_reqs.get(timeline_urgency, 30),
    }
