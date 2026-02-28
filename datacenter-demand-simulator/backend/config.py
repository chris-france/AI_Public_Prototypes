"""Configuration — direct copy from original."""

INDUSTRY_BASELINES = {
    "Financial Services": {"compute_cores": 150, "storage_tb": 25, "power_kw": 45, "network_gbps": 5, "ai_multiplier": 1.8, "compliance_overhead": 1.25, "growth_volatility": 0.15},
    "Healthcare": {"compute_cores": 100, "storage_tb": 40, "power_kw": 35, "network_gbps": 3, "ai_multiplier": 2.0, "compliance_overhead": 1.35, "growth_volatility": 0.10},
    "Technology": {"compute_cores": 250, "storage_tb": 50, "power_kw": 75, "network_gbps": 10, "ai_multiplier": 2.5, "compliance_overhead": 1.10, "growth_volatility": 0.25},
    "Manufacturing": {"compute_cores": 80, "storage_tb": 20, "power_kw": 30, "network_gbps": 2, "ai_multiplier": 1.5, "compliance_overhead": 1.15, "growth_volatility": 0.12},
    "Retail": {"compute_cores": 120, "storage_tb": 35, "power_kw": 40, "network_gbps": 4, "ai_multiplier": 1.6, "compliance_overhead": 1.20, "growth_volatility": 0.18},
    "Government": {"compute_cores": 90, "storage_tb": 30, "power_kw": 32, "network_gbps": 2.5, "ai_multiplier": 1.3, "compliance_overhead": 1.40, "growth_volatility": 0.08},
    "Media & Entertainment": {"compute_cores": 200, "storage_tb": 100, "power_kw": 60, "network_gbps": 15, "ai_multiplier": 2.2, "compliance_overhead": 1.05, "growth_volatility": 0.22},
}

WORKLOAD_MULTIPLIERS = {
    "General Compute": {"compute": 1.0, "storage": 1.0, "power": 1.0, "network": 1.0},
    "High-Performance Computing": {"compute": 3.0, "storage": 1.5, "power": 2.5, "network": 2.0},
    "Big Data Analytics": {"compute": 2.0, "storage": 4.0, "power": 1.8, "network": 2.5},
    "AI/ML Training": {"compute": 5.0, "storage": 2.0, "power": 4.0, "network": 3.0},
    "AI/ML Inference": {"compute": 2.5, "storage": 1.0, "power": 2.0, "network": 2.0},
    "Database Operations": {"compute": 1.5, "storage": 3.0, "power": 1.3, "network": 1.5},
    "Web Services": {"compute": 1.2, "storage": 1.5, "power": 1.1, "network": 3.0},
    "Disaster Recovery": {"compute": 0.8, "storage": 2.5, "power": 0.7, "network": 1.5},
}

COMPLIANCE_REQUIREMENTS = {
    "SOC 2 Type II": {"redundancy_factor": 1.15, "security_overhead": 1.10, "description": "Service Organization Control"},
    "HIPAA": {"redundancy_factor": 1.25, "security_overhead": 1.20, "description": "Health Insurance Portability and Accountability Act"},
    "PCI DSS": {"redundancy_factor": 1.20, "security_overhead": 1.25, "description": "Payment Card Industry Data Security Standard"},
    "GDPR": {"redundancy_factor": 1.15, "security_overhead": 1.15, "description": "General Data Protection Regulation"},
    "FedRAMP": {"redundancy_factor": 1.35, "security_overhead": 1.30, "description": "Federal Risk and Authorization Management Program"},
    "ISO 27001": {"redundancy_factor": 1.10, "security_overhead": 1.10, "description": "Information Security Management System standard"},
}

TECHNOLOGY_TRENDS = {
    "ai_adoption_rate": 0.25,
    "storage_efficiency_gain": 0.10,
    "compute_efficiency_gain": 0.08,
    "power_efficiency_gain": 0.05,
    "network_demand_growth": 0.20,
}

POWER_COOLING = {
    "pue_baseline": 1.6,
    "pue_efficient": 1.2,
    "cooling_tons_per_mw": 285,
    "watts_per_core": 15,
    "watts_per_tb_storage": 8,
}

SCENARIOS = {
    "Conservative": {"growth_modifier": 0.7, "ai_adoption_modifier": 0.5, "efficiency_modifier": 1.2, "description": "Slower growth, conservative AI adoption, better efficiency gains"},
    "Base Case": {"growth_modifier": 1.0, "ai_adoption_modifier": 1.0, "efficiency_modifier": 1.0, "description": "Expected growth trajectory based on industry norms"},
    "Aggressive": {"growth_modifier": 1.4, "ai_adoption_modifier": 1.5, "efficiency_modifier": 0.8, "description": "Accelerated growth, rapid AI adoption, slower efficiency gains"},
    "Technology Disruption": {"growth_modifier": 1.2, "ai_adoption_modifier": 2.5, "efficiency_modifier": 0.9, "description": "Major technology shift driving exponential AI/ML demands"},
}

EXPANSION_THRESHOLDS = {
    "utilization_warning": 0.70,
    "utilization_critical": 0.85,
    "lead_time_months": {"compute": 3, "storage": 2, "power": 18, "cooling": 18, "network": 4},
}
