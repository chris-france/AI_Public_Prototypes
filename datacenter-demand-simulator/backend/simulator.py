"""Core simulation engine — adapted to return dicts instead of DataFrames."""

from datetime import datetime
from config import (
    INDUSTRY_BASELINES, WORKLOAD_MULTIPLIERS, COMPLIANCE_REQUIREMENTS,
    TECHNOLOGY_TRENDS, POWER_COOLING, SCENARIOS, EXPANSION_THRESHOLDS,
)


class DatacenterSimulator:
    def __init__(self, industry, employees, growth_rate, workloads, compliance, horizon_years=5, ai_intensity=0.5):
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
        scale = self.employees / 100
        self.base_compute = self.baseline["compute_cores"] * scale
        self.base_storage = self.baseline["storage_tb"] * scale
        self.base_power_kw = self.baseline["power_kw"] * scale
        self.base_network = self.baseline["network_gbps"] * scale

        if self.workloads:
            n = len(self.workloads)
            cm = sm = pm = nm = 0
            for w in self.workloads:
                wl = WORKLOAD_MULTIPLIERS.get(w, WORKLOAD_MULTIPLIERS["General Compute"])
                cm += wl["compute"]; sm += wl["storage"]; pm += wl["power"]; nm += wl["network"]
            self.base_compute *= cm / n
            self.base_storage *= sm / n
            self.base_power_kw *= pm / n
            self.base_network *= nm / n

        ai_mult = 1 + (self.ai_intensity * (self.baseline["ai_multiplier"] - 1))
        self.base_compute *= ai_mult
        self.base_power_kw *= ai_mult

        compliance_factor = 1.0
        for c in self.compliance:
            if c in COMPLIANCE_REQUIREMENTS:
                compliance_factor *= COMPLIANCE_REQUIREMENTS[c]["redundancy_factor"]
        self.base_compute *= compliance_factor
        self.base_storage *= compliance_factor
        self.base_power_kw *= compliance_factor

        self.base_power_mw = self.base_power_kw / 1000
        self.base_cooling = self.base_power_mw * POWER_COOLING["cooling_tons_per_mw"]

    def simulate_scenario(self, scenario_name="Base Case"):
        scenario = SCENARIOS.get(scenario_name, SCENARIOS["Base Case"])
        n = self.horizon_years + 1
        compute = [0.0] * n
        storage = [0.0] * n
        power = [0.0] * n
        cooling = [0.0] * n
        network = [0.0] * n
        emps = [0.0] * n

        compute[0] = self.base_compute
        storage[0] = self.base_storage
        power[0] = self.base_power_mw
        cooling[0] = self.base_cooling
        network[0] = self.base_network
        emps[0] = self.employees

        adjusted_growth = self.growth_rate * scenario["growth_modifier"]

        for i in range(1, n):
            emps[i] = emps[i - 1] * (1 + adjusted_growth)
            organic = emps[i] / emps[i - 1]
            ai_f = 1 + (TECHNOLOGY_TRENDS["ai_adoption_rate"] * scenario["ai_adoption_modifier"] * self.ai_intensity)
            s_eff = 1 - (TECHNOLOGY_TRENDS["storage_efficiency_gain"] * scenario["efficiency_modifier"])
            c_eff = 1 - (TECHNOLOGY_TRENDS["compute_efficiency_gain"] * scenario["efficiency_modifier"])
            p_eff = 1 - (TECHNOLOGY_TRENDS["power_efficiency_gain"] * scenario["efficiency_modifier"])
            n_growth = 1 + TECHNOLOGY_TRENDS["network_demand_growth"]

            compute[i] = compute[i - 1] * organic * ai_f * c_eff
            storage[i] = storage[i - 1] * organic * s_eff * 1.15
            power[i] = power[i - 1] * organic * ai_f * p_eff
            cooling[i] = power[i] * POWER_COOLING["cooling_tons_per_mw"]
            network[i] = network[i - 1] * organic * n_growth

        current_year = datetime.now().year
        return {
            "years": [current_year + y for y in range(n)],
            "employees": [int(e) for e in emps],
            "compute": [round(v, 1) for v in compute],
            "storage": [round(v, 1) for v in storage],
            "power": [round(v, 4) for v in power],
            "cooling": [round(v, 1) for v in cooling],
            "network": [round(v, 2) for v in network],
        }

    def run_all_scenarios(self):
        return {name: self.simulate_scenario(name) for name in SCENARIOS}

    def get_summary_stats(self):
        base = self.simulate_scenario("Base Case")
        return {
            "industry": self.industry,
            "employees": self.employees,
            "growth_rate": self.growth_rate,
            "horizon_years": self.horizon_years,
            "workloads": self.workloads,
            "compliance": self.compliance,
            "baseline_compute": base["compute"][0],
            "baseline_storage": base["storage"][0],
            "baseline_power": base["power"][0],
            "baseline_cooling": base["cooling"][0],
            "baseline_network": base["network"][0],
            "projected_compute": base["compute"][-1],
            "projected_storage": base["storage"][-1],
            "projected_power": base["power"][-1],
            "projected_cooling": base["cooling"][-1],
            "projected_network": base["network"][-1],
            "compute_growth": round(base["compute"][-1] / base["compute"][0], 2) if base["compute"][0] else 1,
            "storage_growth": round(base["storage"][-1] / base["storage"][0], 2) if base["storage"][0] else 1,
            "power_growth": round(base["power"][-1] / base["power"][0], 2) if base["power"][0] else 1,
        }

    def get_scenario_comparison(self):
        scenarios = self.run_all_scenarios()
        return {
            "horizon": self.horizon_years,
            "scenarios": {
                name: {
                    "compute": data["compute"][-1],
                    "storage": data["storage"][-1],
                    "power": data["power"][-1],
                }
                for name, data in scenarios.items()
            },
        }

    def calculate_decision_points(self):
        current_capacity = {
            "compute": self.base_compute * 1.3,
            "storage": self.base_storage * 1.3,
            "power": self.base_power_mw * 1.3,
            "cooling": self.base_cooling * 1.3,
            "network": self.base_network * 1.3,
        }
        base = self.simulate_scenario("Base Case")
        aggressive = self.simulate_scenario("Aggressive")
        current_year = datetime.now().year

        types = [
            ("compute", "compute", "Compute Cores"),
            ("storage", "storage", "Storage (TB)"),
            ("power", "power", "Power (MW)"),
            ("cooling", "cooling", "Cooling (Tons)"),
            ("network", "network", "Network (Gbps)"),
        ]

        points = []
        for cap_key, col_key, display in types:
            cap = current_capacity[cap_key]
            lead = EXPANSION_THRESHOLDS["lead_time_months"].get(cap_key, 6)
            warn_thresh = cap * EXPANSION_THRESHOLDS["utilization_warning"]
            crit_thresh = cap * EXPANSION_THRESHOLDS["utilization_critical"]

            warning_year = critical_year = agg_warning = None
            for i, val in enumerate(base[col_key]):
                if val >= warn_thresh and warning_year is None:
                    warning_year = base["years"][i]
                if val >= crit_thresh and critical_year is None:
                    critical_year = base["years"][i]
            for i, val in enumerate(aggressive[col_key]):
                if val >= warn_thresh and agg_warning is None:
                    agg_warning = aggressive["years"][i]

            if warning_year:
                decision_year = warning_year - (lead / 12)
                months_until = (decision_year - current_year) * 12
                if months_until <= 6: urgency = "CRITICAL"
                elif months_until <= 12: urgency = "HIGH"
                elif months_until <= 24: urgency = "MEDIUM"
                else: urgency = "LOW"

                utilization = base[col_key][0] / cap if cap > 0 else 0
                points.append({
                    "capacity_type": display,
                    "current_capacity": round(cap, 2),
                    "current_utilization": round(utilization, 2),
                    "warning_year": warning_year,
                    "critical_year": critical_year,
                    "aggressive_warning": agg_warning,
                    "decision_deadline": f"Q{int((decision_year % 1) * 4) + 1} {int(decision_year)}",
                    "lead_time_months": lead,
                    "urgency": urgency,
                    "expansion_needed": round(base[col_key][-1] - cap, 2),
                    "expansion_percentage": round((base[col_key][-1] - cap) / cap * 100, 1) if cap > 0 else 0,
                })

        urgency_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        points.sort(key=lambda x: urgency_order.get(x["urgency"], 4))
        return points
