"""
Core simulation engine for datacenter demand forecasting.
"""

import numpy as np
import pandas as pd
from datetime import datetime
from typing import Optional
from config import (
    INDUSTRY_BASELINES,
    WORKLOAD_MULTIPLIERS,
    COMPLIANCE_REQUIREMENTS,
    TECHNOLOGY_TRENDS,
    POWER_COOLING,
    SCENARIOS,
    EXPANSION_THRESHOLDS,
)


class DatacenterSimulator:
    """Simulates datacenter capacity demands over time."""

    def __init__(
        self,
        industry: str,
        employees: int,
        growth_rate: float,
        workloads: list,
        compliance: list,
        horizon_years: int = 5,
        ai_intensity: float = 0.5,
    ):
        self.industry = industry
        self.employees = employees
        self.growth_rate = growth_rate
        self.workloads = workloads
        self.compliance = compliance
        self.horizon_years = horizon_years
        self.ai_intensity = ai_intensity
        self.baseline = INDUSTRY_BASELINES.get(industry, INDUSTRY_BASELINES["Technology"])
        self._calculate_baseline_requirements()

    def _calculate_baseline_requirements(self):
        """Calculate current baseline requirements."""
        scale = self.employees / 100

        # Base requirements from industry
        self.base_compute = self.baseline["compute_cores"] * scale
        self.base_storage = self.baseline["storage_tb"] * scale
        self.base_power_kw = self.baseline["power_kw"] * scale
        self.base_network = self.baseline["network_gbps"] * scale

        # Apply workload multipliers
        compute_mult = 0
        storage_mult = 0
        power_mult = 0
        network_mult = 0

        if self.workloads:
            for workload in self.workloads:
                wl = WORKLOAD_MULTIPLIERS.get(workload, WORKLOAD_MULTIPLIERS["General Compute"])
                compute_mult += wl["compute"]
                storage_mult += wl["storage"]
                power_mult += wl["power"]
                network_mult += wl["network"]

            # Average the multipliers
            n = len(self.workloads)
            compute_mult /= n
            storage_mult /= n
            power_mult /= n
            network_mult /= n
        else:
            compute_mult = storage_mult = power_mult = network_mult = 1.0

        self.base_compute *= compute_mult
        self.base_storage *= storage_mult
        self.base_power_kw *= power_mult
        self.base_network *= network_mult

        # Apply AI intensity modifier
        ai_mult = 1 + (self.ai_intensity * (self.baseline["ai_multiplier"] - 1))
        self.base_compute *= ai_mult
        self.base_power_kw *= ai_mult

        # Apply compliance overhead
        compliance_factor = 1.0
        for comp in self.compliance:
            if comp in COMPLIANCE_REQUIREMENTS:
                req = COMPLIANCE_REQUIREMENTS[comp]
                compliance_factor *= req["redundancy_factor"]

        self.base_compute *= compliance_factor
        self.base_storage *= compliance_factor
        self.base_power_kw *= compliance_factor

        # Convert power to MW
        self.base_power_mw = self.base_power_kw / 1000

        # Calculate cooling (tons of refrigeration)
        self.base_cooling = self.base_power_mw * POWER_COOLING["cooling_tons_per_mw"]

    def simulate_scenario(self, scenario_name: str = "Base Case") -> pd.DataFrame:
        """Run simulation for a specific scenario."""
        scenario = SCENARIOS.get(scenario_name, SCENARIOS["Base Case"])
        years = list(range(self.horizon_years + 1))

        # Initialize arrays
        compute = np.zeros(len(years))
        storage = np.zeros(len(years))
        power = np.zeros(len(years))
        cooling = np.zeros(len(years))
        network = np.zeros(len(years))
        employees = np.zeros(len(years))

        # Year 0 = current state
        compute[0] = self.base_compute
        storage[0] = self.base_storage
        power[0] = self.base_power_mw
        cooling[0] = self.base_cooling
        network[0] = self.base_network
        employees[0] = self.employees

        # Modified growth rate for scenario
        adjusted_growth = self.growth_rate * scenario["growth_modifier"]

        for i, year in enumerate(years[1:], 1):
            # Employee growth
            employees[i] = employees[i - 1] * (1 + adjusted_growth)

            # Organic growth based on employees
            organic_factor = employees[i] / employees[i - 1]

            # Technology trend impacts
            ai_factor = 1 + (
                TECHNOLOGY_TRENDS["ai_adoption_rate"]
                * scenario["ai_adoption_modifier"]
                * self.ai_intensity
            )
            storage_eff = 1 - (
                TECHNOLOGY_TRENDS["storage_efficiency_gain"] * scenario["efficiency_modifier"]
            )
            compute_eff = 1 - (
                TECHNOLOGY_TRENDS["compute_efficiency_gain"] * scenario["efficiency_modifier"]
            )
            power_eff = 1 - (
                TECHNOLOGY_TRENDS["power_efficiency_gain"] * scenario["efficiency_modifier"]
            )
            network_growth = 1 + TECHNOLOGY_TRENDS["network_demand_growth"]

            # Calculate new values
            compute[i] = compute[i - 1] * organic_factor * ai_factor * compute_eff
            storage[i] = storage[i - 1] * organic_factor * storage_eff * 1.15  # Data accumulation
            power[i] = power[i - 1] * organic_factor * ai_factor * power_eff
            cooling[i] = power[i] * POWER_COOLING["cooling_tons_per_mw"]
            network[i] = network[i - 1] * organic_factor * network_growth

        # Create DataFrame
        current_year = datetime.now().year
        df = pd.DataFrame(
            {
                "Year": [current_year + y for y in years],
                "Employees": employees.astype(int),
                "Compute_Cores": compute,
                "Storage_TB": storage,
                "Power_MW": power,
                "Cooling_Tons": cooling,
                "Network_Gbps": network,
            }
        )

        return df

    def run_all_scenarios(self) -> dict:
        """Run all scenarios and return results."""
        results = {}
        for scenario_name in SCENARIOS.keys():
            results[scenario_name] = self.simulate_scenario(scenario_name)
        return results

    def calculate_decision_points(
        self, current_capacity: Optional[dict] = None
    ) -> list:
        """Identify recommended decision points for capacity expansion."""
        if current_capacity is None:
            # Assume current capacity = baseline * 1.3 (30% headroom)
            current_capacity = {
                "compute": self.base_compute * 1.3,
                "storage": self.base_storage * 1.3,
                "power": self.base_power_mw * 1.3,
                "cooling": self.base_cooling * 1.3,
                "network": self.base_network * 1.3,
            }

        # Run base case simulation
        base_sim = self.simulate_scenario("Base Case")
        aggressive_sim = self.simulate_scenario("Aggressive")

        decision_points = []
        current_year = datetime.now().year

        capacity_types = [
            ("compute", "Compute_Cores", "Compute Cores"),
            ("storage", "Storage_TB", "Storage (TB)"),
            ("power", "Power_MW", "Power (MW)"),
            ("cooling", "Cooling_Tons", "Cooling (Tons)"),
            ("network", "Network_Gbps", "Network (Gbps)"),
        ]

        for cap_key, col_name, display_name in capacity_types:
            cap = current_capacity[cap_key]
            lead_time = EXPANSION_THRESHOLDS["lead_time_months"][cap_key]

            # Find when warning threshold is hit
            warning_threshold = cap * EXPANSION_THRESHOLDS["utilization_warning"]
            critical_threshold = cap * EXPANSION_THRESHOLDS["utilization_critical"]

            # Check base case
            warning_year = None
            critical_year = None

            for idx, row in base_sim.iterrows():
                if row[col_name] >= warning_threshold and warning_year is None:
                    warning_year = row["Year"]
                if row[col_name] >= critical_threshold and critical_year is None:
                    critical_year = row["Year"]

            # Check aggressive case for earlier trigger
            aggressive_warning = None
            for idx, row in aggressive_sim.iterrows():
                if row[col_name] >= warning_threshold and aggressive_warning is None:
                    aggressive_warning = row["Year"]

            if warning_year:
                # Calculate decision date (account for lead time)
                decision_year = warning_year - (lead_time / 12)
                months_until = (decision_year - current_year) * 12

                # Determine urgency
                if months_until <= 6:
                    urgency = "CRITICAL"
                elif months_until <= 12:
                    urgency = "HIGH"
                elif months_until <= 24:
                    urgency = "MEDIUM"
                else:
                    urgency = "LOW"

                current_value = base_sim.iloc[0][col_name]
                utilization = current_value / cap if cap > 0 else 0

                decision_points.append(
                    {
                        "capacity_type": display_name,
                        "current_capacity": cap,
                        "current_utilization": utilization,
                        "warning_year": warning_year,
                        "critical_year": critical_year,
                        "aggressive_warning": aggressive_warning,
                        "decision_deadline": f"Q{int((decision_year % 1) * 4) + 1} {int(decision_year)}",
                        "lead_time_months": lead_time,
                        "urgency": urgency,
                        "expansion_needed": base_sim.iloc[-1][col_name] - cap,
                        "expansion_percentage": (
                            (base_sim.iloc[-1][col_name] - cap) / cap * 100 if cap > 0 else 0
                        ),
                    }
                )

        # Sort by urgency
        urgency_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        decision_points.sort(key=lambda x: urgency_order.get(x["urgency"], 4))

        return decision_points

    def get_summary_stats(self) -> dict:
        """Get summary statistics for the simulation."""
        scenarios = self.run_all_scenarios()
        base = scenarios["Base Case"]

        final_year = base.iloc[-1]
        first_year = base.iloc[0]

        return {
            "industry": self.industry,
            "employees": self.employees,
            "growth_rate": self.growth_rate,
            "horizon_years": self.horizon_years,
            "workloads": self.workloads,
            "compliance": self.compliance,
            "baseline_compute": first_year["Compute_Cores"],
            "baseline_storage": first_year["Storage_TB"],
            "baseline_power": first_year["Power_MW"],
            "baseline_cooling": first_year["Cooling_Tons"],
            "baseline_network": first_year["Network_Gbps"],
            "projected_compute": final_year["Compute_Cores"],
            "projected_storage": final_year["Storage_TB"],
            "projected_power": final_year["Power_MW"],
            "projected_cooling": final_year["Cooling_Tons"],
            "projected_network": final_year["Network_Gbps"],
            "compute_growth": final_year["Compute_Cores"] / first_year["Compute_Cores"],
            "storage_growth": final_year["Storage_TB"] / first_year["Storage_TB"],
            "power_growth": final_year["Power_MW"] / first_year["Power_MW"],
        }

    def get_scenario_comparison(self) -> dict:
        """Get comparison data across scenarios."""
        scenarios = self.run_all_scenarios()

        return {
            "horizon": self.horizon_years,
            "conservative_compute": scenarios["Conservative"].iloc[-1]["Compute_Cores"],
            "conservative_storage": scenarios["Conservative"].iloc[-1]["Storage_TB"],
            "conservative_power": scenarios["Conservative"].iloc[-1]["Power_MW"],
            "base_compute": scenarios["Base Case"].iloc[-1]["Compute_Cores"],
            "base_storage": scenarios["Base Case"].iloc[-1]["Storage_TB"],
            "base_power": scenarios["Base Case"].iloc[-1]["Power_MW"],
            "aggressive_compute": scenarios["Aggressive"].iloc[-1]["Compute_Cores"],
            "aggressive_storage": scenarios["Aggressive"].iloc[-1]["Storage_TB"],
            "aggressive_power": scenarios["Aggressive"].iloc[-1]["Power_MW"],
            "disruption_compute": scenarios["Technology Disruption"].iloc[-1]["Compute_Cores"],
            "disruption_storage": scenarios["Technology Disruption"].iloc[-1]["Storage_TB"],
            "disruption_power": scenarios["Technology Disruption"].iloc[-1]["Power_MW"],
        }
