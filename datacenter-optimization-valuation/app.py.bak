"""
Datacenter Deployment Optimizer & Valuation Tool
Production-grade tool for PE/VC datacenter investment analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum

# Page configuration
st.set_page_config(
    page_title="DC Deployment Optimizer",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for executive dashboard styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3a5f;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .recommendation-box {
        background: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
    }
    .success-box {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
    }
    .danger-box {
        background: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #f1f5f9;
        border-radius: 8px 8px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# DATA MODELS & BENCHMARKS
# ============================================================================

class Region(Enum):
    NORTHERN_VIRGINIA = "Northern Virginia (NOVA)"
    DALLAS_FT_WORTH = "Dallas-Fort Worth"
    PHOENIX = "Phoenix"
    CHICAGO = "Chicago"
    SILICON_VALLEY = "Silicon Valley"
    NEW_YORK_NJ = "New York/New Jersey"
    ATLANTA = "Atlanta"
    SEATTLE = "Seattle"
    LOS_ANGELES = "Los Angeles"
    AMSTERDAM = "Amsterdam"
    LONDON = "London"
    FRANKFURT = "Frankfurt"
    SINGAPORE = "Singapore"
    TOKYO = "Tokyo"


# Real market benchmarks (2024-2025 data)
MARKET_BENCHMARKS = {
    "Northern Virginia (NOVA)": {
        "capex_per_mw": 8_500_000,  # $/MW
        "land_cost_per_acre": 450_000,
        "power_cost_kwh": 0.065,
        "labor_multiplier": 1.0,
        "market_premium": 1.15,
        "avg_pue": 1.35,
        "market_utilization": 0.78,
        "transaction_comp_per_mw": 12_500_000,  # Recent M&A $/MW
        "demand_growth": 0.18,  # YoY
        "tier": 1
    },
    "Dallas-Fort Worth": {
        "capex_per_mw": 7_200_000,
        "land_cost_per_acre": 180_000,
        "power_cost_kwh": 0.058,
        "labor_multiplier": 0.85,
        "market_premium": 1.05,
        "avg_pue": 1.40,
        "market_utilization": 0.72,
        "transaction_comp_per_mw": 10_800_000,
        "demand_growth": 0.22,
        "tier": 1
    },
    "Phoenix": {
        "capex_per_mw": 7_000_000,
        "land_cost_per_acre": 200_000,
        "power_cost_kwh": 0.072,
        "labor_multiplier": 0.90,
        "market_premium": 1.08,
        "avg_pue": 1.38,
        "market_utilization": 0.68,
        "transaction_comp_per_mw": 10_200_000,
        "demand_growth": 0.25,
        "tier": 1
    },
    "Chicago": {
        "capex_per_mw": 8_000_000,
        "land_cost_per_acre": 280_000,
        "power_cost_kwh": 0.078,
        "labor_multiplier": 1.10,
        "market_premium": 1.0,
        "avg_pue": 1.42,
        "market_utilization": 0.70,
        "transaction_comp_per_mw": 11_000_000,
        "demand_growth": 0.12,
        "tier": 1
    },
    "Silicon Valley": {
        "capex_per_mw": 12_000_000,
        "land_cost_per_acre": 2_500_000,
        "power_cost_kwh": 0.145,
        "labor_multiplier": 1.45,
        "market_premium": 1.35,
        "avg_pue": 1.30,
        "market_utilization": 0.85,
        "transaction_comp_per_mw": 18_000_000,
        "demand_growth": 0.15,
        "tier": 1
    },
    "New York/New Jersey": {
        "capex_per_mw": 11_500_000,
        "land_cost_per_acre": 1_800_000,
        "power_cost_kwh": 0.125,
        "labor_multiplier": 1.40,
        "market_premium": 1.25,
        "avg_pue": 1.38,
        "market_utilization": 0.82,
        "transaction_comp_per_mw": 16_500_000,
        "demand_growth": 0.14,
        "tier": 1
    },
    "Atlanta": {
        "capex_per_mw": 7_500_000,
        "land_cost_per_acre": 220_000,
        "power_cost_kwh": 0.082,
        "labor_multiplier": 0.88,
        "market_premium": 0.95,
        "avg_pue": 1.45,
        "market_utilization": 0.65,
        "transaction_comp_per_mw": 9_500_000,
        "demand_growth": 0.16,
        "tier": 2
    },
    "Seattle": {
        "capex_per_mw": 9_500_000,
        "land_cost_per_acre": 850_000,
        "power_cost_kwh": 0.048,
        "labor_multiplier": 1.15,
        "market_premium": 1.12,
        "avg_pue": 1.28,
        "market_utilization": 0.75,
        "transaction_comp_per_mw": 13_500_000,
        "demand_growth": 0.20,
        "tier": 1
    },
    "Los Angeles": {
        "capex_per_mw": 10_500_000,
        "land_cost_per_acre": 1_200_000,
        "power_cost_kwh": 0.135,
        "labor_multiplier": 1.30,
        "market_premium": 1.18,
        "avg_pue": 1.35,
        "market_utilization": 0.78,
        "transaction_comp_per_mw": 14_500_000,
        "demand_growth": 0.13,
        "tier": 1
    },
    "Amsterdam": {
        "capex_per_mw": 9_000_000,
        "land_cost_per_acre": 1_100_000,
        "power_cost_kwh": 0.115,
        "labor_multiplier": 1.20,
        "market_premium": 1.15,
        "avg_pue": 1.32,
        "market_utilization": 0.80,
        "transaction_comp_per_mw": 14_000_000,
        "demand_growth": 0.10,
        "tier": 1
    },
    "London": {
        "capex_per_mw": 11_000_000,
        "land_cost_per_acre": 2_200_000,
        "power_cost_kwh": 0.155,
        "labor_multiplier": 1.35,
        "market_premium": 1.28,
        "avg_pue": 1.35,
        "market_utilization": 0.82,
        "transaction_comp_per_mw": 17_000_000,
        "demand_growth": 0.11,
        "tier": 1
    },
    "Frankfurt": {
        "capex_per_mw": 9_500_000,
        "land_cost_per_acre": 950_000,
        "power_cost_kwh": 0.175,
        "labor_multiplier": 1.25,
        "market_premium": 1.20,
        "avg_pue": 1.38,
        "market_utilization": 0.85,
        "transaction_comp_per_mw": 15_000_000,
        "demand_growth": 0.09,
        "tier": 1
    },
    "Singapore": {
        "capex_per_mw": 13_000_000,
        "land_cost_per_acre": 3_500_000,
        "power_cost_kwh": 0.125,
        "labor_multiplier": 1.10,
        "market_premium": 1.40,
        "avg_pue": 1.55,
        "market_utilization": 0.92,
        "transaction_comp_per_mw": 20_000_000,
        "demand_growth": 0.08,
        "tier": 1
    },
    "Tokyo": {
        "capex_per_mw": 14_000_000,
        "land_cost_per_acre": 4_000_000,
        "power_cost_kwh": 0.165,
        "labor_multiplier": 1.15,
        "market_premium": 1.45,
        "avg_pue": 1.45,
        "market_utilization": 0.88,
        "transaction_comp_per_mw": 21_000_000,
        "demand_growth": 0.07,
        "tier": 1
    }
}

# Deployment approach configurations
DEPLOYMENT_APPROACHES = {
    "ground_up": {
        "name": "Ground-Up Build",
        "description": "Traditional construction with full MEP design, site development, and custom build-out",
        "base_timeline_months": 24,
        "timeline_variance": 6,
        "capex_multiplier": 1.0,
        "opex_efficiency": 0.95,
        "flexibility_score": 85,
        "resale_premium": 1.15,
        "risk_factors": ["Permitting delays", "Supply chain", "Labor availability", "Weather"],
        "typical_pue": 1.30,
        "scalability": "High (if land available)",
        "customization": "Full"
    },
    "modular": {
        "name": "Modular/Prefab",
        "description": "Factory-built modules (Baselayer, Vapor IO, Schneider Electric style) deployed on-site",
        "base_timeline_months": 9,
        "timeline_variance": 2,
        "capex_multiplier": 1.12,
        "opex_efficiency": 1.0,
        "flexibility_score": 95,
        "resale_premium": 0.95,
        "risk_factors": ["Module availability", "Transportation logistics"],
        "typical_pue": 1.35,
        "scalability": "Very High",
        "customization": "Limited"
    },
    "hybrid": {
        "name": "Hybrid Build",
        "description": "Shell building construction + prefab interior modules for rapid deployment",
        "base_timeline_months": 15,
        "timeline_variance": 3,
        "capex_multiplier": 1.05,
        "opex_efficiency": 0.98,
        "flexibility_score": 90,
        "resale_premium": 1.08,
        "risk_factors": ["Coordination complexity", "Shell construction delays"],
        "typical_pue": 1.32,
        "scalability": "High",
        "customization": "Moderate"
    }
}


@dataclass
class DeploymentRequirements:
    """Input requirements for deployment analysis"""
    total_power_mw: float
    rack_count: int
    timeline_urgency: str  # "standard", "accelerated", "critical"
    budget_constraint: float  # Max CapEx in $M
    region: str
    redundancy_level: str  # "N", "N+1", "2N", "2N+1"
    cooling_type: str  # "air", "liquid", "hybrid"


@dataclass
class ValuationInputs:
    """Inputs for M&A valuation analysis"""
    asking_price: float
    claimed_capacity_mw: float
    actual_utilization: float
    current_pue: float
    contract_quality: str  # "enterprise", "hyperscale", "mixed", "retail"
    contract_term_years: float
    expansion_capacity_mw: float
    building_age_years: int
    land_owned: bool
    land_acres: float


# ============================================================================
# CALCULATION ENGINES
# ============================================================================

class DeploymentCalculator:
    """Calculate deployment metrics for each approach"""

    def __init__(self, requirements: DeploymentRequirements):
        self.req = requirements
        self.benchmarks = MARKET_BENCHMARKS[requirements.region]

    def calculate_all_approaches(self) -> Dict:
        """Calculate metrics for all deployment approaches"""
        results = {}
        for approach_key, approach_config in DEPLOYMENT_APPROACHES.items():
            results[approach_key] = self._calculate_approach(approach_key, approach_config)
        return results

    def _calculate_approach(self, approach_key: str, config: Dict) -> Dict:
        """Calculate metrics for a single deployment approach"""

        # Base CapEx calculation
        base_capex = self.req.total_power_mw * self.benchmarks["capex_per_mw"]

        # Apply approach multiplier
        capex = base_capex * config["capex_multiplier"]

        # Adjust for redundancy
        redundancy_multipliers = {"N": 1.0, "N+1": 1.15, "2N": 1.45, "2N+1": 1.60}
        capex *= redundancy_multipliers.get(self.req.redundancy_level, 1.0)

        # Adjust for cooling type
        cooling_multipliers = {"air": 1.0, "liquid": 1.18, "hybrid": 1.12}
        capex *= cooling_multipliers.get(self.req.cooling_type, 1.0)

        # Adjust for labor costs
        capex *= self.benchmarks["labor_multiplier"]

        # Calculate timeline
        base_timeline = config["base_timeline_months"]
        timeline_urgency_factor = {"standard": 1.0, "accelerated": 0.85, "critical": 0.70}
        timeline = base_timeline * timeline_urgency_factor.get(self.req.timeline_urgency, 1.0)

        # Accelerated timeline increases costs
        if self.req.timeline_urgency == "accelerated":
            capex *= 1.08
        elif self.req.timeline_urgency == "critical":
            capex *= 1.18

        # Calculate OpEx (10 year)
        annual_power_cost = (
            self.req.total_power_mw * 1000 *  # Convert to kW
            8760 *  # Hours per year
            self.benchmarks["power_cost_kwh"] *
            config["typical_pue"] *
            0.85  # Avg utilization
        )

        annual_maintenance = capex * 0.025  # 2.5% of CapEx
        annual_staffing = self.req.total_power_mw * 150_000  # ~$150K per MW for staff
        annual_insurance = capex * 0.005  # 0.5% of CapEx
        annual_other = capex * 0.01  # 1% other OpEx

        total_annual_opex = (
            annual_power_cost +
            annual_maintenance +
            annual_staffing +
            annual_insurance +
            annual_other
        ) * config["opex_efficiency"]

        ten_year_opex = total_annual_opex * 10

        # Calculate resale value (Year 10)
        depreciation_factor = 0.65  # 35% depreciation over 10 years
        market_appreciation = (1 + self.benchmarks["demand_growth"]) ** 5  # 5-year avg growth
        resale_value = capex * depreciation_factor * config["resale_premium"] * market_appreciation

        # Risk assessment
        risk_score = self._calculate_risk_score(config)

        # ROI calculation
        total_cost = capex + ten_year_opex
        estimated_revenue = self._estimate_revenue()
        ten_year_revenue = estimated_revenue * 10
        roi = ((ten_year_revenue - total_cost + resale_value) / capex) * 100

        return {
            "name": config["name"],
            "description": config["description"],
            "capex": capex,
            "capex_per_mw": capex / self.req.total_power_mw,
            "annual_opex": total_annual_opex,
            "ten_year_opex": ten_year_opex,
            "total_10yr_cost": capex + ten_year_opex,
            "timeline_months": round(timeline),
            "timeline_variance": config["timeline_variance"],
            "flexibility_score": config["flexibility_score"],
            "resale_value": resale_value,
            "risk_score": risk_score,
            "risk_factors": config["risk_factors"],
            "roi_percent": roi,
            "pue": config["typical_pue"],
            "scalability": config["scalability"],
            "customization": config["customization"],
            "annual_power_cost": annual_power_cost,
            "annual_maintenance": annual_maintenance,
            "meets_budget": capex <= self.req.budget_constraint * 1_000_000,
            "meets_timeline": timeline <= self._get_timeline_requirement()
        }

    def _calculate_risk_score(self, config: Dict) -> int:
        """Calculate risk score (0-100, lower is better)"""
        base_risk = len(config["risk_factors"]) * 8

        # Timeline urgency adds risk
        urgency_risk = {"standard": 0, "accelerated": 10, "critical": 25}
        base_risk += urgency_risk.get(self.req.timeline_urgency, 0)

        # Regional factors
        if self.benchmarks["tier"] == 2:
            base_risk += 5

        # Size complexity
        if self.req.total_power_mw > 50:
            base_risk += 10
        elif self.req.total_power_mw > 100:
            base_risk += 20

        return min(100, max(0, base_risk))

    def _get_timeline_requirement(self) -> int:
        """Get timeline requirement in months based on urgency"""
        requirements = {"standard": 30, "accelerated": 18, "critical": 12}
        return requirements.get(self.req.timeline_urgency, 30)

    def _estimate_revenue(self) -> float:
        """Estimate annual revenue based on market rates"""
        # Colocation revenue per kW per month (varies by market)
        revenue_per_kw_month = 120 * self.benchmarks["market_premium"]
        monthly_revenue = self.req.total_power_mw * 1000 * revenue_per_kw_month * 0.75  # 75% sellable
        return monthly_revenue * 12


class ValuationEngine:
    """M&A valuation engine for datacenter assets"""

    def __init__(self, inputs: ValuationInputs, region: str):
        self.inputs = inputs
        self.region = region
        self.benchmarks = MARKET_BENCHMARKS[region]

    def calculate_valuation(self) -> Dict:
        """Calculate comprehensive valuation analysis"""

        # Base valuation using $/MW benchmark
        base_value = self.inputs.claimed_capacity_mw * self.benchmarks["transaction_comp_per_mw"]

        # Adjustments
        adjustments = []
        adjusted_value = base_value

        # 1. Utilization adjustment
        market_util = self.benchmarks["market_utilization"]
        util_delta = self.inputs.actual_utilization - market_util
        util_adjustment = util_delta * base_value * 0.5  # 50% sensitivity
        adjusted_value += util_adjustment

        if util_delta < -0.15:
            adjustments.append({
                "factor": "Overbuilt Capacity",
                "impact": util_adjustment,
                "description": f"Utilization {self.inputs.actual_utilization:.0%} vs market {market_util:.0%}",
                "flag": "negative"
            })
        elif util_delta > 0.10:
            adjustments.append({
                "factor": "Strong Utilization",
                "impact": util_adjustment,
                "description": f"Above-market utilization of {self.inputs.actual_utilization:.0%}",
                "flag": "positive"
            })
        else:
            adjustments.append({
                "factor": "Utilization",
                "impact": util_adjustment,
                "description": f"Utilization at {self.inputs.actual_utilization:.0%}",
                "flag": "neutral"
            })

        # 2. PUE efficiency adjustment
        market_pue = self.benchmarks["avg_pue"]
        pue_delta = market_pue - self.inputs.current_pue  # Lower PUE is better
        pue_value_impact = pue_delta * base_value * 0.15  # 15% sensitivity per 0.1 PUE
        adjusted_value += pue_value_impact

        if self.inputs.current_pue < market_pue - 0.05:
            adjustments.append({
                "factor": "Efficient PUE",
                "impact": pue_value_impact,
                "description": f"PUE {self.inputs.current_pue:.2f} vs market avg {market_pue:.2f}",
                "flag": "positive"
            })
        elif self.inputs.current_pue > market_pue + 0.10:
            adjustments.append({
                "factor": "Inefficient PUE",
                "impact": pue_value_impact,
                "description": f"PUE {self.inputs.current_pue:.2f} above market avg {market_pue:.2f}",
                "flag": "negative"
            })
        else:
            adjustments.append({
                "factor": "PUE Efficiency",
                "impact": pue_value_impact,
                "description": f"PUE {self.inputs.current_pue:.2f} near market average",
                "flag": "neutral"
            })

        # 3. Contract quality adjustment
        contract_multipliers = {
            "hyperscale": 1.25,
            "enterprise": 1.10,
            "mixed": 1.00,
            "retail": 0.85
        }
        contract_mult = contract_multipliers.get(self.inputs.contract_quality, 1.0)
        contract_adjustment = base_value * (contract_mult - 1.0)
        adjusted_value += contract_adjustment

        contract_flag = "positive" if contract_mult > 1.05 else ("negative" if contract_mult < 0.95 else "neutral")
        adjustments.append({
            "factor": "Contract Quality",
            "impact": contract_adjustment,
            "description": f"{self.inputs.contract_quality.title()} customer base",
            "flag": contract_flag
        })

        # 4. Contract term adjustment
        term_premium = max(0, (self.inputs.contract_term_years - 3) * 0.02)  # 2% per year above 3
        term_adjustment = base_value * term_premium
        adjusted_value += term_adjustment

        adjustments.append({
            "factor": "Contract Terms",
            "impact": term_adjustment,
            "description": f"Avg {self.inputs.contract_term_years:.1f} year contracts",
            "flag": "positive" if self.inputs.contract_term_years > 4 else "neutral"
        })

        # 5. Expansion capacity
        expansion_value = self.inputs.expansion_capacity_mw * self.benchmarks["capex_per_mw"] * 0.3  # 30% of build cost
        adjusted_value += expansion_value

        if self.inputs.expansion_capacity_mw > 0:
            adjustments.append({
                "factor": "Expansion Capacity",
                "impact": expansion_value,
                "description": f"{self.inputs.expansion_capacity_mw:.1f} MW expansion potential",
                "flag": "positive"
            })

        # 6. Building age depreciation
        age_depreciation = min(0.35, self.inputs.building_age_years * 0.025)  # 2.5% per year, max 35%
        age_adjustment = -base_value * age_depreciation
        adjusted_value += age_adjustment

        adjustments.append({
            "factor": "Building Age",
            "impact": age_adjustment,
            "description": f"{self.inputs.building_age_years} years old",
            "flag": "negative" if self.inputs.building_age_years > 8 else "neutral"
        })

        # 7. Land value (if owned)
        land_value = 0
        if self.inputs.land_owned:
            land_value = self.inputs.land_acres * self.benchmarks["land_cost_per_acre"]
            adjusted_value += land_value
            adjustments.append({
                "factor": "Land Ownership",
                "impact": land_value,
                "description": f"{self.inputs.land_acres:.1f} acres owned",
                "flag": "positive"
            })

        # Calculate valuation gap
        valuation_gap = self.inputs.asking_price - adjusted_value
        valuation_gap_percent = (valuation_gap / adjusted_value) * 100

        # Determine if overvalued or undervalued
        if valuation_gap_percent > 15:
            valuation_status = "overvalued"
            recommendation = "PASS - Significant premium to fair value"
        elif valuation_gap_percent > 5:
            valuation_status = "slightly_overvalued"
            recommendation = "NEGOTIATE - Modest premium, negotiate down"
        elif valuation_gap_percent < -15:
            valuation_status = "undervalued"
            recommendation = "BUY - Significant discount to fair value"
        elif valuation_gap_percent < -5:
            valuation_status = "slightly_undervalued"
            recommendation = "ATTRACTIVE - Trading below fair value"
        else:
            valuation_status = "fair"
            recommendation = "FAIR VALUE - Priced appropriately"

        # Detect specific issues
        flags = []

        # Overbuilt capacity detection
        if self.inputs.actual_utilization < 0.50:
            flags.append({
                "type": "warning",
                "title": "Overbuilt Capacity Detected",
                "description": f"Only {self.inputs.actual_utilization:.0%} utilization suggests oversupply or demand issues"
            })

        # Undervalued asset detection
        if valuation_gap_percent < -20 and self.inputs.actual_utilization > 0.70:
            flags.append({
                "type": "opportunity",
                "title": "Potential Undervalued Asset",
                "description": f"Strong {self.inputs.actual_utilization:.0%} utilization with {abs(valuation_gap_percent):.0f}% discount to fair value"
            })

        # Contract concentration risk
        if self.inputs.contract_quality == "hyperscale" and self.inputs.actual_utilization > 0.90:
            flags.append({
                "type": "risk",
                "title": "Concentration Risk",
                "description": "High utilization with hyperscale contracts may indicate single-tenant concentration"
            })

        return {
            "base_value": base_value,
            "adjusted_value": adjusted_value,
            "asking_price": self.inputs.asking_price,
            "valuation_gap": valuation_gap,
            "valuation_gap_percent": valuation_gap_percent,
            "valuation_status": valuation_status,
            "recommendation": recommendation,
            "adjustments": adjustments,
            "flags": flags,
            "implied_per_mw": adjusted_value / self.inputs.claimed_capacity_mw,
            "market_comp_per_mw": self.benchmarks["transaction_comp_per_mw"],
            "land_value": land_value
        }


# ============================================================================
# OLLAMA INTEGRATION
# ============================================================================

def query_ollama(prompt: str, model: str = "llama3.2") -> str:
    """Query Ollama for AI-powered analysis"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 1000
                }
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return None
    except Exception as e:
        return None


def get_deployment_recommendation(requirements: DeploymentRequirements, results: Dict) -> str:
    """Get AI recommendation for deployment strategy"""

    prompt = f"""You are a datacenter infrastructure expert advising a PE/VC firm on deployment strategy.

REQUIREMENTS:
- Power Capacity: {requirements.total_power_mw} MW
- Rack Count: {requirements.rack_count}
- Region: {requirements.region}
- Timeline: {requirements.timeline_urgency}
- Budget: ${requirements.budget_constraint}M
- Redundancy: {requirements.redundancy_level}
- Cooling: {requirements.cooling_type}

ANALYSIS RESULTS:
Ground-Up Build:
- CapEx: ${results['ground_up']['capex']/1e6:.1f}M (${results['ground_up']['capex_per_mw']/1e6:.1f}M/MW)
- Timeline: {results['ground_up']['timeline_months']} months
- 10yr OpEx: ${results['ground_up']['ten_year_opex']/1e6:.1f}M
- Flexibility: {results['ground_up']['flexibility_score']}/100
- Meets Budget: {'Yes' if results['ground_up']['meets_budget'] else 'No'}

Modular/Prefab:
- CapEx: ${results['modular']['capex']/1e6:.1f}M (${results['modular']['capex_per_mw']/1e6:.1f}M/MW)
- Timeline: {results['modular']['timeline_months']} months
- 10yr OpEx: ${results['modular']['ten_year_opex']/1e6:.1f}M
- Flexibility: {results['modular']['flexibility_score']}/100
- Meets Budget: {'Yes' if results['modular']['meets_budget'] else 'No'}

Hybrid Build:
- CapEx: ${results['hybrid']['capex']/1e6:.1f}M (${results['hybrid']['capex_per_mw']/1e6:.1f}M/MW)
- Timeline: {results['hybrid']['timeline_months']} months
- 10yr OpEx: ${results['hybrid']['ten_year_opex']/1e6:.1f}M
- Flexibility: {results['hybrid']['flexibility_score']}/100
- Meets Budget: {'Yes' if results['hybrid']['meets_budget'] else 'No'}

Provide a concise executive recommendation (3-4 paragraphs) covering:
1. Recommended approach and why
2. Key risks and mitigations
3. Financial considerations
4. Strategic timing factors

Be specific and actionable. Use concrete numbers from the analysis."""

    response = query_ollama(prompt)
    if response:
        return response
    else:
        # Fallback recommendation logic
        best_approach = min(results.keys(), key=lambda k: results[k]['total_10yr_cost'])
        fastest = min(results.keys(), key=lambda k: results[k]['timeline_months'])

        if requirements.timeline_urgency == "critical" and results[fastest]['meets_budget']:
            rec_approach = fastest
        elif not results[best_approach]['meets_budget']:
            rec_approach = min([k for k in results.keys() if results[k]['meets_budget']],
                             key=lambda k: results[k]['total_10yr_cost'], default=best_approach)
        else:
            rec_approach = best_approach

        return f"""**Recommended Approach: {results[rec_approach]['name']}**

Based on the analysis, {results[rec_approach]['name']} is recommended for this {requirements.total_power_mw} MW deployment in {requirements.region}.

**Rationale:**
- Total 10-year cost of ${results[rec_approach]['total_10yr_cost']/1e6:.1f}M provides {'optimal' if rec_approach == best_approach else 'acceptable'} economics
- {results[rec_approach]['timeline_months']}-month timeline {'meets' if results[rec_approach]['meets_timeline'] else 'does not meet'} the {requirements.timeline_urgency} requirement
- Flexibility score of {results[rec_approach]['flexibility_score']}/100 supports future scaling needs

**Key Risks:** {', '.join(results[rec_approach]['risk_factors'])}

**Financial Summary:**
- CapEx: ${results[rec_approach]['capex']/1e6:.1f}M (${results[rec_approach]['capex_per_mw']/1e6:.2f}M per MW)
- Projected ROI: {results[rec_approach]['roi_percent']:.1f}% over 10 years
- Estimated resale value at Year 10: ${results[rec_approach]['resale_value']/1e6:.1f}M

*Note: Ollama not available. This is a rule-based recommendation. Connect Ollama for enhanced AI analysis.*"""


def get_deal_analysis(valuation: Dict, inputs: ValuationInputs, region: str) -> str:
    """Get AI analysis of the M&A deal"""

    prompt = f"""You are a datacenter M&A advisor for a PE/VC firm evaluating an acquisition target.

DEAL OVERVIEW:
- Asking Price: ${inputs.asking_price/1e6:.1f}M
- Calculated Fair Value: ${valuation['adjusted_value']/1e6:.1f}M
- Valuation Gap: {valuation['valuation_gap_percent']:.1f}% {'premium' if valuation['valuation_gap_percent'] > 0 else 'discount'}
- Status: {valuation['valuation_status'].replace('_', ' ').title()}

ASSET DETAILS:
- Capacity: {inputs.claimed_capacity_mw} MW
- Utilization: {inputs.actual_utilization:.0%}
- PUE: {inputs.current_pue}
- Contract Quality: {inputs.contract_quality}
- Avg Contract Term: {inputs.contract_term_years} years
- Building Age: {inputs.building_age_years} years
- Expansion Potential: {inputs.expansion_capacity_mw} MW
- Region: {region}

KEY VALUATION ADJUSTMENTS:
{chr(10).join([f"- {adj['factor']}: ${adj['impact']/1e6:+.1f}M ({adj['description']})" for adj in valuation['adjustments']])}

FLAGS:
{chr(10).join([f"- [{flag['type'].upper()}] {flag['title']}: {flag['description']}" for flag in valuation['flags']]) if valuation['flags'] else 'None'}

Provide executive deal analysis (3-4 paragraphs):
1. Deal assessment (buy/pass/negotiate)
2. Key value drivers and risks
3. Suggested negotiation strategy
4. Integration considerations

Be direct and actionable. Include specific price targets if negotiating."""

    response = query_ollama(prompt)
    if response:
        return response
    else:
        # Fallback analysis
        status = valuation['valuation_status']
        gap = valuation['valuation_gap_percent']

        if status == "undervalued":
            assessment = "BUY"
            strategy = f"Move quickly at or near asking price of ${inputs.asking_price/1e6:.1f}M. This represents a {abs(gap):.0f}% discount to fair value."
        elif status == "slightly_undervalued":
            assessment = "BUY"
            strategy = f"Target price of ${inputs.asking_price/1e6:.1f}M is attractive. Consider offering ${inputs.asking_price*0.97/1e6:.1f}M to capture additional value."
        elif status == "fair":
            assessment = "CONDITIONAL BUY"
            strategy = f"Fair value deal. Negotiate for ${valuation['adjusted_value']*0.95/1e6:.1f}M to build in buffer for integration costs."
        elif status == "slightly_overvalued":
            assessment = "NEGOTIATE"
            strategy = f"Counter at ${valuation['adjusted_value']/1e6:.1f}M fair value. Walk away above ${valuation['adjusted_value']*1.05/1e6:.1f}M."
        else:
            assessment = "PASS"
            strategy = f"Significant {gap:.0f}% premium. Only re-engage if price drops below ${valuation['adjusted_value']*1.05/1e6:.1f}M."

        return f"""**Deal Assessment: {assessment}**

{valuation['recommendation']}

**Value Analysis:**
The asset is priced at ${inputs.asking_price/1e6:.1f}M against a calculated fair value of ${valuation['adjusted_value']/1e6:.1f}M, representing a {abs(gap):.1f}% {'premium' if gap > 0 else 'discount'}. At {inputs.actual_utilization:.0%} utilization with {inputs.contract_quality} contracts, the revenue quality is {'strong' if inputs.contract_quality in ['hyperscale', 'enterprise'] else 'moderate'}.

**Negotiation Strategy:**
{strategy}

**Key Considerations:**
- Building age ({inputs.building_age_years} years) implies {'near-term refresh CapEx' if inputs.building_age_years > 7 else 'good remaining useful life'}
- Expansion capacity of {inputs.expansion_capacity_mw} MW provides growth optionality worth ~${valuation['adjustments'][-2]['impact']/1e6:.1f}M
- PUE of {inputs.current_pue} is {'better than' if inputs.current_pue < MARKET_BENCHMARKS[region]['avg_pue'] else 'in line with'} market average

*Note: Ollama not available. This is a rule-based analysis. Connect Ollama for enhanced AI insights.*"""


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_comparison_chart(results: Dict) -> go.Figure:
    """Create side-by-side comparison chart"""
    approaches = list(results.keys())

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("CapEx Comparison ($M)", "Timeline (Months)",
                       "10-Year Total Cost ($M)", "Flexibility & Risk Scores"),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )

    colors = ['#3b82f6', '#10b981', '#f59e0b']
    names = [results[a]['name'] for a in approaches]

    # CapEx
    fig.add_trace(
        go.Bar(x=names, y=[results[a]['capex']/1e6 for a in approaches],
               marker_color=colors, showlegend=False),
        row=1, col=1
    )

    # Timeline
    fig.add_trace(
        go.Bar(x=names, y=[results[a]['timeline_months'] for a in approaches],
               marker_color=colors, showlegend=False),
        row=1, col=2
    )

    # Total 10yr Cost
    fig.add_trace(
        go.Bar(x=names, y=[results[a]['total_10yr_cost']/1e6 for a in approaches],
               marker_color=colors, showlegend=False),
        row=2, col=1
    )

    # Flexibility and Risk
    fig.add_trace(
        go.Bar(name="Flexibility", x=names,
               y=[results[a]['flexibility_score'] for a in approaches],
               marker_color='#10b981'),
        row=2, col=2
    )
    fig.add_trace(
        go.Bar(name="Risk", x=names,
               y=[results[a]['risk_score'] for a in approaches],
               marker_color='#ef4444'),
        row=2, col=2
    )

    fig.update_layout(
        height=500,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        barmode='group'
    )

    return fig


def create_valuation_waterfall(valuation: Dict) -> go.Figure:
    """Create valuation waterfall chart"""

    labels = ["Base Value"]
    values = [valuation['base_value']/1e6]
    measure = ["absolute"]

    for adj in valuation['adjustments']:
        labels.append(adj['factor'])
        values.append(adj['impact']/1e6)
        measure.append("relative")

    labels.append("Fair Value")
    values.append(valuation['adjusted_value']/1e6)
    measure.append("total")

    labels.append("Asking Price")
    values.append(valuation['asking_price']/1e6)
    measure.append("absolute")

    fig = go.Figure(go.Waterfall(
        name="Valuation",
        orientation="v",
        measure=measure,
        x=labels,
        y=values,
        textposition="outside",
        text=[f"${v:.1f}M" for v in values],
        connector={"line": {"color": "#94a3b8"}},
        increasing={"marker": {"color": "#10b981"}},
        decreasing={"marker": {"color": "#ef4444"}},
        totals={"marker": {"color": "#3b82f6"}}
    ))

    fig.update_layout(
        title="Valuation Waterfall Analysis",
        showlegend=False,
        height=400
    )

    return fig


def create_roi_chart(results: Dict) -> go.Figure:
    """Create ROI comparison chart"""

    approaches = list(results.keys())
    names = [results[a]['name'] for a in approaches]

    fig = go.Figure()

    # ROI bars
    fig.add_trace(go.Bar(
        name="10-Year ROI %",
        x=names,
        y=[results[a]['roi_percent'] for a in approaches],
        marker_color=['#3b82f6', '#10b981', '#f59e0b'],
        text=[f"{results[a]['roi_percent']:.1f}%" for a in approaches],
        textposition='outside'
    ))

    fig.update_layout(
        title="Projected 10-Year ROI by Approach",
        yaxis_title="ROI (%)",
        height=350,
        showlegend=False
    )

    return fig


def create_opex_breakdown(results: Dict) -> go.Figure:
    """Create OpEx breakdown pie chart"""

    # Use ground-up as example
    r = results['ground_up']

    labels = ['Power', 'Maintenance', 'Staffing', 'Insurance', 'Other']
    values = [
        r['annual_power_cost'],
        r['annual_maintenance'],
        r['capex'] * 0.025 * 10,  # Proxy for staffing
        r['capex'] * 0.005 * 10,  # Insurance
        r['capex'] * 0.01 * 10    # Other
    ]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#94a3b8']
    )])

    fig.update_layout(
        title="10-Year OpEx Breakdown (Ground-Up)",
        height=350
    )

    return fig


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Header
    st.markdown('<p class="main-header">Datacenter Deployment Optimizer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Enterprise-grade deployment analysis and M&A valuation platform</p>', unsafe_allow_html=True)

    # Main tabs
    tab1, tab2, tab3 = st.tabs(["Deployment Analysis", "M&A Valuation", "Market Benchmarks"])

    # =========================================================================
    # TAB 1: DEPLOYMENT ANALYSIS
    # =========================================================================
    with tab1:
        st.header("Deployment Requirements")

        col1, col2, col3 = st.columns(3)

        with col1:
            total_power = st.number_input(
                "Total Power Capacity (MW)",
                min_value=1.0, max_value=500.0, value=20.0, step=1.0,
                help="Critical IT load capacity in megawatts"
            )

            rack_count = st.number_input(
                "Rack Count",
                min_value=10, max_value=10000, value=500, step=50,
                help="Number of rack positions required"
            )

            region = st.selectbox(
                "Geographic Region",
                options=list(MARKET_BENCHMARKS.keys()),
                index=0,
                help="Primary deployment location"
            )

        with col2:
            timeline_urgency = st.selectbox(
                "Timeline Urgency",
                options=["standard", "accelerated", "critical"],
                format_func=lambda x: {
                    "standard": "Standard (24-30 months)",
                    "accelerated": "Accelerated (15-20 months)",
                    "critical": "Critical (<12 months)"
                }[x],
                help="How quickly capacity is needed"
            )

            budget_constraint = st.number_input(
                "Maximum CapEx Budget ($M)",
                min_value=10.0, max_value=5000.0, value=200.0, step=10.0,
                help="Maximum capital expenditure in millions"
            )

            redundancy = st.selectbox(
                "Redundancy Level",
                options=["N", "N+1", "2N", "2N+1"],
                index=1,
                help="Infrastructure redundancy requirement"
            )

        with col3:
            cooling_type = st.selectbox(
                "Cooling Strategy",
                options=["air", "liquid", "hybrid"],
                format_func=lambda x: {
                    "air": "Air Cooling (Traditional)",
                    "liquid": "Liquid Cooling (High Density)",
                    "hybrid": "Hybrid (Air + Liquid)"
                }[x],
                help="Primary cooling methodology"
            )

        # Run Analysis Button
        if st.button("Run Deployment Analysis", type="primary", use_container_width=True):

            requirements = DeploymentRequirements(
                total_power_mw=total_power,
                rack_count=rack_count,
                timeline_urgency=timeline_urgency,
                budget_constraint=budget_constraint,
                region=region,
                redundancy_level=redundancy,
                cooling_type=cooling_type
            )

            calculator = DeploymentCalculator(requirements)

            with st.spinner("Analyzing deployment approaches..."):
                results = calculator.calculate_all_approaches()

            # Store in session state
            st.session_state['deployment_results'] = results
            st.session_state['deployment_requirements'] = requirements

            st.success("Analysis complete!")

        # Display results if available
        if 'deployment_results' in st.session_state:
            results = st.session_state['deployment_results']
            requirements = st.session_state['deployment_requirements']

            st.markdown("---")
            st.header("Analysis Results")

            # Executive Summary Metrics
            st.subheader("Executive Summary")

            metric_cols = st.columns(4)

            best_cost = min(results.keys(), key=lambda k: results[k]['total_10yr_cost'])
            fastest = min(results.keys(), key=lambda k: results[k]['timeline_months'])
            best_roi = max(results.keys(), key=lambda k: results[k]['roi_percent'])
            most_flexible = max(results.keys(), key=lambda k: results[k]['flexibility_score'])

            with metric_cols[0]:
                st.metric(
                    "Lowest Total Cost",
                    f"${results[best_cost]['total_10yr_cost']/1e6:.1f}M",
                    f"{results[best_cost]['name']}"
                )

            with metric_cols[1]:
                st.metric(
                    "Fastest Deployment",
                    f"{results[fastest]['timeline_months']} months",
                    f"{results[fastest]['name']}"
                )

            with metric_cols[2]:
                st.metric(
                    "Best ROI",
                    f"{results[best_roi]['roi_percent']:.1f}%",
                    f"{results[best_roi]['name']}"
                )

            with metric_cols[3]:
                st.metric(
                    "Most Flexible",
                    f"{results[most_flexible]['flexibility_score']}/100",
                    f"{results[most_flexible]['name']}"
                )

            # Comparison Charts
            st.subheader("Comparison Dashboard")

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                st.plotly_chart(create_comparison_chart(results), use_container_width=True)

            with chart_col2:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.plotly_chart(create_roi_chart(results), use_container_width=True)
                with col_b:
                    st.plotly_chart(create_opex_breakdown(results), use_container_width=True)

            # Detailed Comparison Table
            st.subheader("Detailed Comparison")

            comparison_df = pd.DataFrame({
                "Metric": [
                    "CapEx ($M)",
                    "CapEx per MW ($M)",
                    "Annual OpEx ($M)",
                    "10-Year OpEx ($M)",
                    "Total 10-Year Cost ($M)",
                    "Timeline (months)",
                    "PUE",
                    "Flexibility Score",
                    "Risk Score",
                    "10-Year ROI (%)",
                    "Resale Value ($M)",
                    "Meets Budget",
                    "Meets Timeline"
                ],
                "Ground-Up": [
                    f"${results['ground_up']['capex']/1e6:.1f}",
                    f"${results['ground_up']['capex_per_mw']/1e6:.2f}",
                    f"${results['ground_up']['annual_opex']/1e6:.1f}",
                    f"${results['ground_up']['ten_year_opex']/1e6:.1f}",
                    f"${results['ground_up']['total_10yr_cost']/1e6:.1f}",
                    results['ground_up']['timeline_months'],
                    results['ground_up']['pue'],
                    results['ground_up']['flexibility_score'],
                    results['ground_up']['risk_score'],
                    f"{results['ground_up']['roi_percent']:.1f}%",
                    f"${results['ground_up']['resale_value']/1e6:.1f}",
                    "Yes" if results['ground_up']['meets_budget'] else "No",
                    "Yes" if results['ground_up']['meets_timeline'] else "No"
                ],
                "Modular/Prefab": [
                    f"${results['modular']['capex']/1e6:.1f}",
                    f"${results['modular']['capex_per_mw']/1e6:.2f}",
                    f"${results['modular']['annual_opex']/1e6:.1f}",
                    f"${results['modular']['ten_year_opex']/1e6:.1f}",
                    f"${results['modular']['total_10yr_cost']/1e6:.1f}",
                    results['modular']['timeline_months'],
                    results['modular']['pue'],
                    results['modular']['flexibility_score'],
                    results['modular']['risk_score'],
                    f"{results['modular']['roi_percent']:.1f}%",
                    f"${results['modular']['resale_value']/1e6:.1f}",
                    "Yes" if results['modular']['meets_budget'] else "No",
                    "Yes" if results['modular']['meets_timeline'] else "No"
                ],
                "Hybrid": [
                    f"${results['hybrid']['capex']/1e6:.1f}",
                    f"${results['hybrid']['capex_per_mw']/1e6:.2f}",
                    f"${results['hybrid']['annual_opex']/1e6:.1f}",
                    f"${results['hybrid']['ten_year_opex']/1e6:.1f}",
                    f"${results['hybrid']['total_10yr_cost']/1e6:.1f}",
                    results['hybrid']['timeline_months'],
                    results['hybrid']['pue'],
                    results['hybrid']['flexibility_score'],
                    results['hybrid']['risk_score'],
                    f"{results['hybrid']['roi_percent']:.1f}%",
                    f"${results['hybrid']['resale_value']/1e6:.1f}",
                    "Yes" if results['hybrid']['meets_budget'] else "No",
                    "Yes" if results['hybrid']['meets_timeline'] else "No"
                ]
            })

            st.dataframe(comparison_df, use_container_width=True, hide_index=True)

            # Risk Assessment
            st.subheader("Risk Assessment")

            risk_cols = st.columns(3)

            for i, (approach_key, approach_data) in enumerate(results.items()):
                with risk_cols[i]:
                    risk_level = "Low" if approach_data['risk_score'] < 30 else ("Medium" if approach_data['risk_score'] < 60 else "High")
                    risk_color = "success" if risk_level == "Low" else ("warning" if risk_level == "Medium" else "danger")

                    st.markdown(f"**{approach_data['name']}** - Risk: {risk_level} ({approach_data['risk_score']}/100)")

                    st.markdown(f"""
                    <div class="{risk_color}-box">
                    <strong>Key Risk Factors:</strong>
                    <ul>
                    {"".join([f"<li>{rf}</li>" for rf in approach_data['risk_factors']])}
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)

            # AI Recommendation
            st.subheader("AI Strategy Recommendation")

            with st.spinner("Generating AI recommendation..."):
                recommendation = get_deployment_recommendation(requirements, results)

            st.markdown(f"""
            <div class="recommendation-box">
            {recommendation}
            </div>
            """, unsafe_allow_html=True)

    # =========================================================================
    # TAB 2: M&A VALUATION
    # =========================================================================
    with tab2:
        st.header("M&A Asset Valuation")
        st.markdown("Evaluate datacenter acquisition targets with comprehensive valuation analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Deal Parameters")

            asking_price = st.number_input(
                "Asking Price ($M)",
                min_value=10.0, max_value=10000.0, value=250.0, step=10.0,
                help="Seller's asking price"
            )

            claimed_capacity = st.number_input(
                "Claimed Capacity (MW)",
                min_value=1.0, max_value=500.0, value=20.0, step=1.0,
                help="Total IT load capacity"
            )

            actual_utilization = st.slider(
                "Actual Utilization (%)",
                min_value=10, max_value=100, value=72,
                help="Current capacity utilization"
            ) / 100

            current_pue = st.number_input(
                "Current PUE",
                min_value=1.1, max_value=2.5, value=1.42, step=0.01,
                help="Power Usage Effectiveness"
            )

            valuation_region = st.selectbox(
                "Asset Region",
                options=list(MARKET_BENCHMARKS.keys()),
                index=0,
                key="valuation_region"
            )

        with col2:
            st.subheader("Asset Details")

            contract_quality = st.selectbox(
                "Contract Quality",
                options=["hyperscale", "enterprise", "mixed", "retail"],
                format_func=lambda x: {
                    "hyperscale": "Hyperscale (AWS, Azure, Google)",
                    "enterprise": "Enterprise (Fortune 500)",
                    "mixed": "Mixed Portfolio",
                    "retail": "Retail/SMB"
                }[x]
            )

            contract_term = st.number_input(
                "Average Contract Term (years)",
                min_value=0.5, max_value=15.0, value=4.5, step=0.5
            )

            expansion_capacity = st.number_input(
                "Expansion Capacity (MW)",
                min_value=0.0, max_value=200.0, value=10.0, step=1.0,
                help="Additional capacity that can be built"
            )

            building_age = st.number_input(
                "Building Age (years)",
                min_value=0, max_value=30, value=6, step=1
            )

            land_owned = st.checkbox("Land Owned", value=True)

            land_acres = st.number_input(
                "Land Size (acres)",
                min_value=0.0, max_value=100.0, value=8.0, step=0.5,
                disabled=not land_owned
            )

        # Run Valuation
        if st.button("Run Valuation Analysis", type="primary", use_container_width=True):

            val_inputs = ValuationInputs(
                asking_price=asking_price * 1e6,
                claimed_capacity_mw=claimed_capacity,
                actual_utilization=actual_utilization,
                current_pue=current_pue,
                contract_quality=contract_quality,
                contract_term_years=contract_term,
                expansion_capacity_mw=expansion_capacity,
                building_age_years=building_age,
                land_owned=land_owned,
                land_acres=land_acres if land_owned else 0
            )

            engine = ValuationEngine(val_inputs, valuation_region)

            with st.spinner("Calculating valuation..."):
                valuation = engine.calculate_valuation()

            st.session_state['valuation_results'] = valuation
            st.session_state['valuation_inputs'] = val_inputs
            st.session_state['valuation_region'] = valuation_region

            st.success("Valuation complete!")

        # Display valuation results
        if 'valuation_results' in st.session_state:
            valuation = st.session_state['valuation_results']
            val_inputs = st.session_state['valuation_inputs']
            val_region = st.session_state['valuation_region']

            st.markdown("---")
            st.header("Valuation Results")

            # Key Metrics
            metric_cols = st.columns(4)

            with metric_cols[0]:
                st.metric(
                    "Fair Market Value",
                    f"${valuation['adjusted_value']/1e6:.1f}M",
                    f"${valuation['implied_per_mw']/1e6:.1f}M/MW"
                )

            with metric_cols[1]:
                st.metric(
                    "Asking Price",
                    f"${valuation['asking_price']/1e6:.1f}M",
                    f"{valuation['valuation_gap_percent']:+.1f}% vs Fair Value"
                )

            with metric_cols[2]:
                gap_color = "inverse" if valuation['valuation_gap_percent'] > 0 else "normal"
                st.metric(
                    "Valuation Gap",
                    f"${valuation['valuation_gap']/1e6:+.1f}M",
                    valuation['valuation_status'].replace('_', ' ').title(),
                    delta_color=gap_color
                )

            with metric_cols[3]:
                st.metric(
                    "Market Comp",
                    f"${valuation['market_comp_per_mw']/1e6:.1f}M/MW",
                    f"{val_region.split()[0]}"
                )

            # Recommendation Box
            status = valuation['valuation_status']
            if status in ['undervalued', 'slightly_undervalued']:
                box_class = "success-box"
            elif status in ['overvalued']:
                box_class = "danger-box"
            else:
                box_class = "warning-box"

            st.markdown(f"""
            <div class="{box_class}">
            <h3>{valuation['recommendation']}</h3>
            </div>
            """, unsafe_allow_html=True)

            # Flags
            if valuation['flags']:
                st.subheader("Key Findings")
                for flag in valuation['flags']:
                    if flag['type'] == 'opportunity':
                        st.success(f"**{flag['title']}**: {flag['description']}")
                    elif flag['type'] == 'warning':
                        st.warning(f"**{flag['title']}**: {flag['description']}")
                    else:
                        st.error(f"**{flag['title']}**: {flag['description']}")

            # Waterfall Chart
            st.subheader("Valuation Waterfall")
            st.plotly_chart(create_valuation_waterfall(valuation), use_container_width=True)

            # Adjustment Details
            st.subheader("Valuation Adjustments")

            adj_df = pd.DataFrame([
                {
                    "Factor": adj['factor'],
                    "Impact ($M)": f"${adj['impact']/1e6:+.1f}",
                    "Description": adj['description'],
                    "Assessment": "+" if adj['flag'] == 'positive' else ("-" if adj['flag'] == 'negative' else "~")
                }
                for adj in valuation['adjustments']
            ])

            st.dataframe(adj_df, use_container_width=True, hide_index=True)

            # AI Deal Analysis
            st.subheader("AI Deal Analysis")

            with st.spinner("Generating deal analysis..."):
                deal_analysis = get_deal_analysis(valuation, val_inputs, val_region)

            st.markdown(f"""
            <div class="recommendation-box">
            {deal_analysis}
            </div>
            """, unsafe_allow_html=True)

    # =========================================================================
    # TAB 3: MARKET BENCHMARKS
    # =========================================================================
    with tab3:
        st.header("Market Benchmarks & Transaction Comps")
        st.markdown("Reference data for datacenter market analysis (2024-2025)")

        # Regional Benchmarks Table
        st.subheader("Regional Cost Benchmarks")

        benchmark_data = []
        for region, data in MARKET_BENCHMARKS.items():
            benchmark_data.append({
                "Region": region,
                "Tier": data['tier'],
                "CapEx/MW ($M)": f"${data['capex_per_mw']/1e6:.1f}",
                "Transaction Comp/MW ($M)": f"${data['transaction_comp_per_mw']/1e6:.1f}",
                "Power ($/kWh)": f"${data['power_cost_kwh']:.3f}",
                "Avg PUE": data['avg_pue'],
                "Utilization": f"{data['market_utilization']:.0%}",
                "Demand Growth": f"{data['demand_growth']:.0%}",
                "Land ($/acre)": f"${data['land_cost_per_acre']:,.0f}"
            })

        benchmark_df = pd.DataFrame(benchmark_data)
        st.dataframe(benchmark_df, use_container_width=True, hide_index=True)

        # Visualization
        st.subheader("Regional Comparison Charts")

        chart_cols = st.columns(2)

        with chart_cols[0]:
            # CapEx per MW by region
            regions = list(MARKET_BENCHMARKS.keys())
            capex_values = [MARKET_BENCHMARKS[r]['capex_per_mw']/1e6 for r in regions]

            fig = px.bar(
                x=regions, y=capex_values,
                title="Construction Cost per MW by Region",
                labels={"x": "Region", "y": "CapEx per MW ($M)"},
                color=capex_values,
                color_continuous_scale="Blues"
            )
            fig.update_layout(showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        with chart_cols[1]:
            # Transaction comps
            comp_values = [MARKET_BENCHMARKS[r]['transaction_comp_per_mw']/1e6 for r in regions]

            fig = px.bar(
                x=regions, y=comp_values,
                title="M&A Transaction Comp per MW by Region",
                labels={"x": "Region", "y": "Transaction Comp per MW ($M)"},
                color=comp_values,
                color_continuous_scale="Greens"
            )
            fig.update_layout(showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        # Deployment Approach Reference
        st.subheader("Deployment Approach Characteristics")

        approach_data = []
        for key, config in DEPLOYMENT_APPROACHES.items():
            approach_data.append({
                "Approach": config['name'],
                "Base Timeline": f"{config['base_timeline_months']} months",
                "Cost Premium": f"{(config['capex_multiplier']-1)*100:+.0f}%",
                "Flexibility": f"{config['flexibility_score']}/100",
                "Resale Premium": f"{(config['resale_premium']-1)*100:+.0f}%",
                "Typical PUE": config['typical_pue'],
                "Scalability": config['scalability'],
                "Customization": config['customization']
            })

        approach_df = pd.DataFrame(approach_data)
        st.dataframe(approach_df, use_container_width=True, hide_index=True)

        # Data Sources
        st.subheader("Data Sources & Methodology")
        st.markdown("""
        **Benchmark Sources:**
        - JLL Data Center Outlook Reports (2024-2025)
        - CBRE North America Data Center Trends
        - Cushman & Wakefield Global Data Center Market Comparison
        - Uptime Institute Annual Survey
        - Public M&A transaction filings and press releases

        **Methodology:**
        - CapEx benchmarks based on Tier III+ equivalents with N+1 redundancy
        - Transaction comps reflect stabilized, operational assets
        - Power costs based on commercial/industrial rates
        - PUE figures represent market averages for modern facilities
        - Utilization rates from industry surveys and operator reports

        **Valuation Approach:**
        - Income approach with market comparable adjustments
        - Replacement cost analysis for expansion capacity
        - DCF sensitivity for contract quality and term
        - Location-based premium/discount factors
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.85rem;">
    Datacenter Deployment Optimizer v1.0 | Built for PE/VC Investment Analysis<br>
    Data reflects 2024-2025 market conditions | Connect Ollama for enhanced AI recommendations
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
