"""M&A valuation engine — ported from original ValuationEngine class."""

from market_data import MARKET_BENCHMARKS


def calculate_valuation(asking_price, claimed_capacity_mw, actual_utilization, current_pue, contract_quality, contract_term_years, expansion_capacity_mw, building_age_years, land_owned, land_acres, region):
    benchmarks = MARKET_BENCHMARKS[region]
    base_value = claimed_capacity_mw * benchmarks["transaction_comp_per_mw"]
    adjustments = []
    adjusted_value = base_value

    # 1. Utilization
    market_util = benchmarks["market_utilization"]
    util_delta = actual_utilization - market_util
    util_adj = util_delta * base_value * 0.5
    adjusted_value += util_adj
    flag = "negative" if util_delta < -0.15 else ("positive" if util_delta > 0.10 else "neutral")
    adjustments.append({"factor": "Utilization", "impact": round(util_adj, 2), "description": f"{actual_utilization:.0%} vs market {market_util:.0%}", "flag": flag})

    # 2. PUE
    market_pue = benchmarks["avg_pue"]
    pue_delta = market_pue - current_pue
    pue_adj = pue_delta * base_value * 0.15
    adjusted_value += pue_adj
    flag = "positive" if current_pue < market_pue - 0.05 else ("negative" if current_pue > market_pue + 0.10 else "neutral")
    adjustments.append({"factor": "PUE Efficiency", "impact": round(pue_adj, 2), "description": f"PUE {current_pue:.2f} vs market {market_pue:.2f}", "flag": flag})

    # 3. Contract quality
    contract_mults = {"hyperscale": 1.25, "enterprise": 1.10, "mixed": 1.00, "retail": 0.85}
    cm = contract_mults.get(contract_quality, 1.0)
    contract_adj = base_value * (cm - 1.0)
    adjusted_value += contract_adj
    flag = "positive" if cm > 1.05 else ("negative" if cm < 0.95 else "neutral")
    adjustments.append({"factor": "Contract Quality", "impact": round(contract_adj, 2), "description": f"{contract_quality.title()} customer base", "flag": flag})

    # 4. Contract term
    term_premium = max(0, (contract_term_years - 3) * 0.02)
    term_adj = base_value * term_premium
    adjusted_value += term_adj
    adjustments.append({"factor": "Contract Terms", "impact": round(term_adj, 2), "description": f"Avg {contract_term_years:.1f} year contracts", "flag": "positive" if contract_term_years > 4 else "neutral"})

    # 5. Expansion
    expansion_val = expansion_capacity_mw * benchmarks["capex_per_mw"] * 0.3
    adjusted_value += expansion_val
    if expansion_capacity_mw > 0:
        adjustments.append({"factor": "Expansion Capacity", "impact": round(expansion_val, 2), "description": f"{expansion_capacity_mw:.1f} MW expansion", "flag": "positive"})

    # 6. Building age
    age_dep = min(0.35, building_age_years * 0.025)
    age_adj = -base_value * age_dep
    adjusted_value += age_adj
    adjustments.append({"factor": "Building Age", "impact": round(age_adj, 2), "description": f"{building_age_years} years old", "flag": "negative" if building_age_years > 8 else "neutral"})

    # 7. Land
    land_value = 0
    if land_owned:
        land_value = land_acres * benchmarks["land_cost_per_acre"]
        adjusted_value += land_value
        adjustments.append({"factor": "Land Ownership", "impact": round(land_value, 2), "description": f"{land_acres:.1f} acres owned", "flag": "positive"})

    gap = asking_price - adjusted_value
    gap_pct = (gap / adjusted_value) * 100 if adjusted_value else 0

    if gap_pct > 15: status, rec = "overvalued", "PASS - Significant premium to fair value"
    elif gap_pct > 5: status, rec = "slightly_overvalued", "NEGOTIATE - Modest premium"
    elif gap_pct < -15: status, rec = "undervalued", "BUY - Significant discount"
    elif gap_pct < -5: status, rec = "slightly_undervalued", "ATTRACTIVE - Below fair value"
    else: status, rec = "fair", "FAIR VALUE - Priced appropriately"

    flags = []
    if actual_utilization < 0.50:
        flags.append({"type": "warning", "title": "Overbuilt Capacity", "description": f"Only {actual_utilization:.0%} utilization"})
    if gap_pct < -20 and actual_utilization > 0.70:
        flags.append({"type": "opportunity", "title": "Potential Undervalued Asset", "description": f"{actual_utilization:.0%} util with {abs(gap_pct):.0f}% discount"})
    if contract_quality == "hyperscale" and actual_utilization > 0.90:
        flags.append({"type": "risk", "title": "Concentration Risk", "description": "High util with hyperscale may indicate single-tenant"})

    return {
        "base_value": round(base_value, 2),
        "adjusted_value": round(adjusted_value, 2),
        "asking_price": asking_price,
        "valuation_gap": round(gap, 2),
        "valuation_gap_percent": round(gap_pct, 1),
        "valuation_status": status,
        "recommendation": rec,
        "adjustments": adjustments,
        "flags": flags,
        "implied_per_mw": round(adjusted_value / claimed_capacity_mw, 2),
        "market_comp_per_mw": benchmarks["transaction_comp_per_mw"],
    }
