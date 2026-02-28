"""Ollama client adapted for streaming SSE responses."""

import requests


SYSTEM_PROMPT = """You are a senior datacenter infrastructure consultant providing
strategic analysis for C-level executives. Your analysis should be:
- Concise and actionable
- Focused on business impact and ROI
- Include specific recommendations with timelines
- Highlight key risks and mitigation strategies
Format your response with clear sections and bullet points."""


def is_ollama_available(base_url="http://localhost:11434"):
    try:
        r = requests.get(f"{base_url}/api/tags", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def get_available_models(base_url="http://localhost:11434"):
    try:
        r = requests.get(f"{base_url}/api/tags", timeout=5)
        if r.status_code == 200:
            return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        pass
    return []


def stream_ollama(prompt, model="qwen2.5:14b", system=None, base_url="http://localhost:11434"):
    """Generator that yields text chunks from Ollama streaming response."""
    try:
        r = requests.post(
            f"{base_url}/api/generate",
            json={"model": model, "prompt": prompt, "system": system or SYSTEM_PROMPT, "stream": True},
            stream=True,
            timeout=120,
        )
        r.raise_for_status()
        import json
        for line in r.iter_lines():
            if line:
                data = json.loads(line)
                token = data.get("response", "")
                if token:
                    yield token
                if data.get("done"):
                    break
    except Exception as e:
        yield f"\n\n[Error: {str(e)}]"


def build_capacity_prompt(summary):
    return f"""Analyze this datacenter capacity projection and provide strategic recommendations:

**Business Context:**
- Industry: {summary.get('industry', 'Unknown')}
- Current Employees: {summary.get('employees', 0):,}
- Annual Growth Rate: {summary.get('growth_rate', 0):.1%}
- Projection Horizon: {summary.get('horizon_years', 5)} years

**Current Baseline Requirements:**
- Compute Cores: {summary.get('baseline_compute', 0):,.0f}
- Storage: {summary.get('baseline_storage', 0):,.1f} TB
- Power: {summary.get('baseline_power', 0):,.2f} MW

**Projected Requirements (Base Case):**
- Compute Cores: {summary.get('projected_compute', 0):,.0f}
- Storage: {summary.get('projected_storage', 0):,.1f} TB
- Power: {summary.get('projected_power', 0):,.2f} MW

**Growth Multipliers:** Compute: {summary.get('compute_growth', 0):.1f}x | Storage: {summary.get('storage_growth', 0):.1f}x | Power: {summary.get('power_growth', 0):.1f}x
**Key Workloads:** {', '.join(summary.get('workloads', []))}
**Compliance:** {', '.join(summary.get('compliance', []))}

Provide: 1) Executive Summary 2) Critical Decision Points 3) Top 3 Risks 4) Investment Prioritization 5) Alternative Strategies"""
