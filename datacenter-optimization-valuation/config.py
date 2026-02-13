"""
Configuration settings for Datacenter Deployment Optimizer
"""

# Ollama Configuration
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",
    "default_model": "llama3.2",
    "fallback_models": ["llama3.1", "mistral", "codellama"],
    "timeout": 60,
    "temperature": 0.7,
    "max_tokens": 1000
}

# Financial Assumptions
FINANCIAL_ASSUMPTIONS = {
    "discount_rate": 0.10,  # 10% for DCF
    "inflation_rate": 0.025,  # 2.5% annual
    "power_escalation": 0.03,  # 3% annual power cost increase
    "labor_escalation": 0.035,  # 3.5% annual labor cost increase
    "depreciation_years": 15,  # Straight-line depreciation period
    "tax_rate": 0.25,  # Corporate tax rate
    "debt_ratio": 0.60,  # Typical leverage for DC acquisitions
    "cost_of_debt": 0.065,  # 6.5% interest rate
}

# Redundancy Configurations
REDUNDANCY_SPECS = {
    "N": {
        "description": "No redundancy - single path",
        "uptime_target": 0.9950,  # 99.5%
        "tier_equivalent": "Tier I",
        "cost_multiplier": 1.0
    },
    "N+1": {
        "description": "Single redundant component",
        "uptime_target": 0.9982,  # 99.82%
        "tier_equivalent": "Tier II/III",
        "cost_multiplier": 1.15
    },
    "2N": {
        "description": "Full redundancy - dual path",
        "uptime_target": 0.9995,  # 99.95%
        "tier_equivalent": "Tier III+",
        "cost_multiplier": 1.45
    },
    "2N+1": {
        "description": "Full redundancy plus spare",
        "uptime_target": 0.9999,  # 99.99%
        "tier_equivalent": "Tier IV",
        "cost_multiplier": 1.60
    }
}

# Cooling System Configurations
COOLING_SPECS = {
    "air": {
        "description": "Traditional CRAC/CRAH air cooling",
        "max_density_kw": 15,  # kW per rack
        "pue_impact": 0.0,
        "cost_multiplier": 1.0,
        "maintenance_factor": 1.0
    },
    "liquid": {
        "description": "Direct-to-chip or rear-door liquid cooling",
        "max_density_kw": 100,  # kW per rack
        "pue_impact": -0.15,  # Reduces PUE
        "cost_multiplier": 1.18,
        "maintenance_factor": 1.10
    },
    "hybrid": {
        "description": "Combined air and liquid cooling",
        "max_density_kw": 50,  # kW per rack
        "pue_impact": -0.08,
        "cost_multiplier": 1.12,
        "maintenance_factor": 1.05
    }
}

# Market Tier Definitions
MARKET_TIERS = {
    1: {
        "description": "Primary markets with deep liquidity",
        "characteristics": [
            "Multiple hyperscale deployments",
            "Strong fiber connectivity",
            "Robust power infrastructure",
            "Deep talent pool",
            "Active M&A market"
        ],
        "risk_premium": 0.0
    },
    2: {
        "description": "Secondary markets with growing demand",
        "characteristics": [
            "Emerging hyperscale interest",
            "Developing connectivity",
            "Power availability varies",
            "Growing talent base",
            "Selective M&A activity"
        ],
        "risk_premium": 0.02
    },
    3: {
        "description": "Tertiary markets for specific use cases",
        "characteristics": [
            "Limited hyperscale presence",
            "Basic connectivity",
            "Power constraints common",
            "Limited talent pool",
            "Rare M&A transactions"
        ],
        "risk_premium": 0.05
    }
}

# Contract Quality Profiles
CONTRACT_PROFILES = {
    "hyperscale": {
        "description": "Cloud providers (AWS, Azure, Google, Meta, etc.)",
        "credit_quality": "Investment Grade",
        "typical_term_years": (5, 15),
        "renewal_probability": 0.85,
        "pricing_power": "Low",
        "valuation_premium": 1.25
    },
    "enterprise": {
        "description": "Fortune 500 and large enterprises",
        "credit_quality": "Mixed IG/HY",
        "typical_term_years": (3, 7),
        "renewal_probability": 0.75,
        "pricing_power": "Moderate",
        "valuation_premium": 1.10
    },
    "mixed": {
        "description": "Diverse customer base",
        "credit_quality": "Mixed",
        "typical_term_years": (2, 5),
        "renewal_probability": 0.65,
        "pricing_power": "Moderate",
        "valuation_premium": 1.00
    },
    "retail": {
        "description": "SMB and retail colocation",
        "credit_quality": "Non-rated",
        "typical_term_years": (1, 3),
        "renewal_probability": 0.55,
        "pricing_power": "High",
        "valuation_premium": 0.85
    }
}

# Risk Factor Weights
RISK_WEIGHTS = {
    "permitting_delays": 15,
    "supply_chain": 12,
    "labor_availability": 10,
    "weather": 8,
    "module_availability": 10,
    "transportation_logistics": 8,
    "coordination_complexity": 10,
    "shell_construction_delays": 12,
    "power_availability": 15,
    "regulatory_changes": 10,
    "market_demand": 10,
    "competition": 8
}

# Export Formats
EXPORT_CONFIG = {
    "formats": ["pdf", "xlsx", "pptx"],
    "include_charts": True,
    "include_raw_data": True,
    "branding": {
        "primary_color": "#1e3a5f",
        "secondary_color": "#3b82f6",
        "accent_color": "#10b981"
    }
}
