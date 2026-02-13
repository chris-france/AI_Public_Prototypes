"""
Ollama integration for AI-powered analysis and recommendations.
"""

import json
import requests
from typing import Optional


class OllamaClient:
    """Client for interacting with local Ollama instance."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2.5:14b"):
        self.base_url = base_url
        self.model = model
        self._available = None

    def is_available(self) -> bool:
        """Check if Ollama is running and accessible."""
        if self._available is not None:
            return self._available
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            self._available = response.status_code == 200
        except requests.exceptions.RequestException:
            self._available = False
        return self._available

    def get_available_models(self) -> list:
        """Get list of available models."""
        if not self.is_available():
            return []
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
        except requests.exceptions.RequestException:
            pass
        return []

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """Generate a response from the model."""
        if not self.is_available():
            return self._fallback_response(prompt)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60,
            )
            if response.status_code == 200:
                return response.json().get("response", "")
        except requests.exceptions.RequestException:
            pass

        return self._fallback_response(prompt)

    def _fallback_response(self, prompt: str) -> str:
        """Provide fallback analysis when Ollama is unavailable."""
        return "AI analysis unavailable. Please ensure Ollama is running locally."

    def analyze_capacity_plan(self, simulation_data: dict) -> str:
        """Analyze simulation results and provide strategic recommendations."""
        system_prompt = """You are a senior datacenter infrastructure consultant providing
strategic analysis for C-level executives. Your analysis should be:
- Concise and actionable
- Focused on business impact and ROI
- Include specific recommendations with timelines
- Highlight key risks and mitigation strategies
Format your response with clear sections and bullet points."""

        prompt = f"""Analyze this datacenter capacity projection and provide strategic recommendations:

**Business Context:**
- Industry: {simulation_data.get('industry', 'Unknown')}
- Current Employees: {simulation_data.get('employees', 0):,}
- Annual Growth Rate: {simulation_data.get('growth_rate', 0):.1%}
- Projection Horizon: {simulation_data.get('horizon_years', 5)} years

**Current Baseline Requirements:**
- Compute Cores: {simulation_data.get('baseline_compute', 0):,.0f}
- Storage: {simulation_data.get('baseline_storage', 0):,.1f} TB
- Power: {simulation_data.get('baseline_power', 0):,.2f} MW
- Cooling: {simulation_data.get('baseline_cooling', 0):,.0f} tons

**Year {simulation_data.get('horizon_years', 5)} Projected Requirements (Base Case):**
- Compute Cores: {simulation_data.get('projected_compute', 0):,.0f}
- Storage: {simulation_data.get('projected_storage', 0):,.1f} TB
- Power: {simulation_data.get('projected_power', 0):,.2f} MW
- Cooling: {simulation_data.get('projected_cooling', 0):,.0f} tons

**Growth Multipliers:**
- Compute: {simulation_data.get('compute_growth', 0):.1f}x
- Storage: {simulation_data.get('storage_growth', 0):.1f}x
- Power: {simulation_data.get('power_growth', 0):.1f}x

**Key Workloads:** {', '.join(simulation_data.get('workloads', []))}
**Compliance Requirements:** {', '.join(simulation_data.get('compliance', []))}

Provide:
1. Executive Summary (2-3 sentences)
2. Critical Decision Points (with recommended timing)
3. Risk Assessment (top 3 risks)
4. Investment Prioritization
5. Alternative Strategies to Consider"""

        return self.generate(prompt, system_prompt)

    def generate_scenario_insights(self, scenario_comparison: dict) -> str:
        """Generate insights comparing different growth scenarios."""
        system_prompt = """You are a datacenter strategy consultant analyzing growth scenarios.
Provide clear, executive-level insights comparing scenarios. Focus on:
- Key differences between scenarios
- Decision triggers and inflection points
- Hedging strategies"""

        prompt = f"""Compare these datacenter capacity scenarios:

**Conservative Scenario (Year {scenario_comparison.get('horizon', 5)}):**
- Compute: {scenario_comparison.get('conservative_compute', 0):,.0f} cores
- Storage: {scenario_comparison.get('conservative_storage', 0):,.1f} TB
- Power: {scenario_comparison.get('conservative_power', 0):,.2f} MW

**Base Case Scenario:**
- Compute: {scenario_comparison.get('base_compute', 0):,.0f} cores
- Storage: {scenario_comparison.get('base_storage', 0):,.1f} TB
- Power: {scenario_comparison.get('base_power', 0):,.2f} MW

**Aggressive Scenario:**
- Compute: {scenario_comparison.get('aggressive_compute', 0):,.0f} cores
- Storage: {scenario_comparison.get('aggressive_storage', 0):,.1f} TB
- Power: {scenario_comparison.get('aggressive_power', 0):,.2f} MW

**Technology Disruption Scenario:**
- Compute: {scenario_comparison.get('disruption_compute', 0):,.0f} cores
- Storage: {scenario_comparison.get('disruption_storage', 0):,.1f} TB
- Power: {scenario_comparison.get('disruption_power', 0):,.2f} MW

Provide a brief (150 words max) executive insight on:
1. Range of outcomes and planning implications
2. Key decision triggers to monitor
3. Recommended hedging strategy"""

        return self.generate(prompt, system_prompt)

    def generate_decision_recommendation(self, decision_point: dict) -> str:
        """Generate recommendation for a specific capacity decision point."""
        system_prompt = """You are a datacenter infrastructure advisor.
Provide a brief, actionable recommendation for the decision point."""

        prompt = f"""Decision Point Analysis:

**Capacity Type:** {decision_point.get('capacity_type', 'Unknown')}
**Trigger:** {decision_point.get('trigger', 'Unknown')}
**Timeline:** {decision_point.get('timeline', 'Unknown')}
**Current Utilization:** {decision_point.get('utilization', 0):.0%}
**Lead Time Required:** {decision_point.get('lead_time', 0)} months

Provide a 2-3 sentence recommendation including:
- Immediate action required
- Key stakeholders to engage
- Primary risk if action is delayed"""

        return self.generate(prompt, system_prompt)
