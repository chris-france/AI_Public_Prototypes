# Datacenter Optimization & Valuation

**PE/VC datacenter investment analysis across 14 global markets.**

A Streamlit application for comparing ground-up builds, modular deployments, and hybrid datacenter strategies. Includes M&A asset valuation with transaction comps, sensitivity analysis, and AI-generated deal memos. Designed for private equity and venture capital due diligence workflows.

---

## Key Features

- **Three deployment strategies** — Ground-up, modular, and hybrid builds with full cost modeling
- **M&A valuation engine** — Asset-based valuation with market multiples and transaction comps
- **14 global markets** — Location-specific costs for power, labor, land, and connectivity
- **Sensitivity analysis** — Tornado charts and scenario matrices for key assumptions
- **AI deal memos** — Automated investment summaries via local Ollama models
- **Excel export** — One-click export of financial models and analysis
- **Sample scenarios** — Pre-built deployment and acquisition scenarios for quick demos

## Tech Stack

Streamlit, Plotly, Pandas, NumPy, Ollama

## Quick Start

```bash
cd datacenter-optimization-valuation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Opens at [http://localhost:8603](http://localhost:8603).

AI deal memos require [Ollama](https://ollama.ai) running locally with a pulled model (e.g., `ollama pull llama3.2:3b`).

## License

[MIT](LICENSE)
