# Datacenter Demand Simulator

**Enterprise datacenter capacity forecasting with AI-powered strategic analysis.**

A Streamlit dashboard that models datacenter demand across compute, storage, power, and cooling dimensions. Run multi-scenario projections with configurable growth rates, see decision timelines for capacity upgrades, and get AI-generated strategic recommendations via local Ollama models.

---

## Key Features

- **Multi-dimensional forecasting** — Model compute, storage, power, and cooling capacity simultaneously
- **Scenario comparison** — Run conservative, moderate, and aggressive growth scenarios side by side
- **Decision timeline** — See when each resource hits capacity thresholds with recommended action dates
- **AI strategic analysis** — Get automated recommendations from local Ollama LLMs (no API keys required)
- **Industry baselines** — Pre-configured profiles for enterprise, hyperscale, colocation, and edge deployments
- **Interactive charts** — Plotly visualizations with drill-down capability

## Tech Stack

Streamlit, Plotly, Pandas, NumPy, Ollama

## Quick Start

```bash
cd datacenter-demand-simulator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Opens at [http://localhost:8602](http://localhost:8602).

AI analysis requires [Ollama](https://ollama.ai) running locally with a pulled model (e.g., `ollama pull llama3.2:3b`).

## License

[MIT](LICENSE)
