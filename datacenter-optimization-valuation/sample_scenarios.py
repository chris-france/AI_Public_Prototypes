"""
Sample scenarios for demonstration and testing
"""

# Deployment Scenarios
DEPLOYMENT_SCENARIOS = {
    "hyperscale_nova": {
        "name": "Hyperscale Campus - Northern Virginia",
        "description": "Large-scale hyperscale deployment for cloud provider",
        "requirements": {
            "total_power_mw": 100.0,
            "rack_count": 2500,
            "timeline_urgency": "accelerated",
            "budget_constraint": 950.0,
            "region": "Northern Virginia (NOVA)",
            "redundancy_level": "2N",
            "cooling_type": "hybrid"
        }
    },
    "enterprise_dallas": {
        "name": "Enterprise Colocation - Dallas",
        "description": "Mid-size enterprise colocation facility",
        "requirements": {
            "total_power_mw": 20.0,
            "rack_count": 500,
            "timeline_urgency": "standard",
            "budget_constraint": 200.0,
            "region": "Dallas-Fort Worth",
            "redundancy_level": "N+1",
            "cooling_type": "air"
        }
    },
    "edge_phoenix": {
        "name": "Edge Deployment - Phoenix",
        "description": "Rapid edge deployment for latency-sensitive workloads",
        "requirements": {
            "total_power_mw": 5.0,
            "rack_count": 120,
            "timeline_urgency": "critical",
            "budget_constraint": 75.0,
            "region": "Phoenix",
            "redundancy_level": "N+1",
            "cooling_type": "air"
        }
    },
    "ai_cluster_silicon_valley": {
        "name": "AI/ML Training Cluster - Silicon Valley",
        "description": "High-density AI training facility",
        "requirements": {
            "total_power_mw": 50.0,
            "rack_count": 400,
            "timeline_urgency": "accelerated",
            "budget_constraint": 750.0,
            "region": "Silicon Valley",
            "redundancy_level": "2N",
            "cooling_type": "liquid"
        }
    },
    "european_expansion": {
        "name": "European Hub - Frankfurt",
        "description": "GDPR-compliant European data center",
        "requirements": {
            "total_power_mw": 30.0,
            "rack_count": 750,
            "timeline_urgency": "standard",
            "budget_constraint": 350.0,
            "region": "Frankfurt",
            "redundancy_level": "2N",
            "cooling_type": "air"
        }
    }
}

# M&A Scenarios
MA_SCENARIOS = {
    "undervalued_opportunity": {
        "name": "Undervalued Asset - Chicago",
        "description": "Well-operated facility with below-market asking price",
        "inputs": {
            "asking_price": 180.0,  # $M
            "claimed_capacity_mw": 18.0,
            "actual_utilization": 0.78,
            "current_pue": 1.38,
            "contract_quality": "enterprise",
            "contract_term_years": 5.2,
            "expansion_capacity_mw": 12.0,
            "building_age_years": 5,
            "land_owned": True,
            "land_acres": 10.0
        },
        "region": "Chicago"
    },
    "overbuilt_warning": {
        "name": "Overbuilt Capacity - Atlanta",
        "description": "Large facility with utilization concerns",
        "inputs": {
            "asking_price": 350.0,
            "claimed_capacity_mw": 40.0,
            "actual_utilization": 0.42,
            "current_pue": 1.52,
            "contract_quality": "mixed",
            "contract_term_years": 2.8,
            "expansion_capacity_mw": 20.0,
            "building_age_years": 8,
            "land_owned": True,
            "land_acres": 15.0
        },
        "region": "Atlanta"
    },
    "premium_hyperscale": {
        "name": "Premium Hyperscale Asset - NOVA",
        "description": "Fully leased to hyperscaler, premium pricing",
        "inputs": {
            "asking_price": 520.0,
            "claimed_capacity_mw": 32.0,
            "actual_utilization": 0.95,
            "current_pue": 1.28,
            "contract_quality": "hyperscale",
            "contract_term_years": 12.0,
            "expansion_capacity_mw": 8.0,
            "building_age_years": 3,
            "land_owned": True,
            "land_acres": 12.0
        },
        "region": "Northern Virginia (NOVA)"
    },
    "distressed_asset": {
        "name": "Distressed Asset - LA",
        "description": "Older facility with operational challenges",
        "inputs": {
            "asking_price": 85.0,
            "claimed_capacity_mw": 12.0,
            "actual_utilization": 0.55,
            "current_pue": 1.65,
            "contract_quality": "retail",
            "contract_term_years": 1.5,
            "expansion_capacity_mw": 0.0,
            "building_age_years": 14,
            "land_owned": False,
            "land_acres": 0.0
        },
        "region": "Los Angeles"
    },
    "apac_expansion": {
        "name": "APAC Growth Asset - Singapore",
        "description": "Strategic APAC gateway facility",
        "inputs": {
            "asking_price": 420.0,
            "claimed_capacity_mw": 20.0,
            "actual_utilization": 0.88,
            "current_pue": 1.48,
            "contract_quality": "enterprise",
            "contract_term_years": 4.5,
            "expansion_capacity_mw": 5.0,
            "building_age_years": 4,
            "land_owned": True,
            "land_acres": 3.0
        },
        "region": "Singapore"
    }
}

# Recent Market Transactions (anonymized/illustrative)
TRANSACTION_COMPS = [
    {
        "date": "Q4 2024",
        "region": "Northern Virginia",
        "capacity_mw": 48,
        "price_m": 720,
        "price_per_mw": 15.0,
        "buyer_type": "Infrastructure Fund",
        "asset_type": "Hyperscale",
        "utilization": 0.92
    },
    {
        "date": "Q3 2024",
        "region": "Dallas",
        "capacity_mw": 25,
        "price_m": 275,
        "price_per_mw": 11.0,
        "buyer_type": "REIT",
        "asset_type": "Enterprise",
        "utilization": 0.75
    },
    {
        "date": "Q3 2024",
        "region": "Chicago",
        "capacity_mw": 15,
        "price_m": 165,
        "price_per_mw": 11.0,
        "buyer_type": "Private Equity",
        "asset_type": "Colocation",
        "utilization": 0.68
    },
    {
        "date": "Q2 2024",
        "region": "Phoenix",
        "capacity_mw": 60,
        "price_m": 612,
        "price_per_mw": 10.2,
        "buyer_type": "Hyperscaler",
        "asset_type": "Build-to-Suit",
        "utilization": 0.0
    },
    {
        "date": "Q2 2024",
        "region": "London",
        "capacity_mw": 22,
        "price_m": 385,
        "price_per_mw": 17.5,
        "buyer_type": "Sovereign Wealth",
        "asset_type": "Enterprise",
        "utilization": 0.82
    },
    {
        "date": "Q1 2024",
        "region": "Frankfurt",
        "capacity_mw": 18,
        "price_m": 279,
        "price_per_mw": 15.5,
        "buyer_type": "Infrastructure Fund",
        "asset_type": "Colocation",
        "utilization": 0.85
    },
    {
        "date": "Q1 2024",
        "region": "Singapore",
        "capacity_mw": 12,
        "price_m": 252,
        "price_per_mw": 21.0,
        "buyer_type": "REIT",
        "asset_type": "Carrier Hotel",
        "utilization": 0.90
    },
    {
        "date": "Q4 2023",
        "region": "Silicon Valley",
        "capacity_mw": 8,
        "price_m": 152,
        "price_per_mw": 19.0,
        "buyer_type": "Private Equity",
        "asset_type": "Enterprise",
        "utilization": 0.78
    }
]

# Industry KPIs for benchmarking
INDUSTRY_KPIS = {
    "pue": {
        "best_in_class": 1.15,
        "top_quartile": 1.30,
        "median": 1.45,
        "bottom_quartile": 1.60
    },
    "utilization": {
        "best_in_class": 0.90,
        "top_quartile": 0.80,
        "median": 0.70,
        "bottom_quartile": 0.55
    },
    "revenue_per_kw": {
        "hyperscale": 85,  # $/kW/month
        "enterprise": 120,
        "colocation": 150,
        "retail": 180
    },
    "opex_ratio": {
        "best_in_class": 0.35,  # OpEx as % of revenue
        "top_quartile": 0.42,
        "median": 0.50,
        "bottom_quartile": 0.60
    }
}
