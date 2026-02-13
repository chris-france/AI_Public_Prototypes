# Personal Demo Launcher

**One dashboard to manage and launch all AI demo projects.**

A Streamlit-based control panel that starts, stops, and monitors multiple demo applications from a single interface. Supports Streamlit apps, Docker Compose services, and custom processes — each on its own port with live status indicators.

---

## Key Features

- **Single-pane management** — Start, stop, and open any demo from one dashboard
- **Start All / Stop All** — Launch or tear down the entire portfolio in one click
- **Live status indicators** — Green (running), gray (stopped), orange (coming soon)
- **Docker integration** — Automatically starts Docker Desktop when needed, manages Compose services
- **Dependency orchestration** — Starts prerequisite services (e.g., Qdrant) before dependent demos
- **Clean shutdown** — Kills all managed processes on Ctrl+C or exit

## Managed Demos

| Demo | Port | Type | Description |
|------|:----:|------|-------------|
| Inference Cost Calculator | 8601 | Streamlit | GPU vs cloud TCO comparison over 36 months |
| Datacenter Demand Simulator | 8602 | Streamlit | Capacity forecasting with AI-powered analysis |
| Datacenter Optimization & Valuation | 8603 | Streamlit | PE/VC datacenter investment analysis across 14 markets |
| Model Security Scanner | 8604 | Streamlit | LLM vulnerability testing across 10 attack categories |
| Local RAG System | 8605 | Docker | Open WebUI + Qdrant with persistent memory |
| n8n Workflow Canvas | 8606 | n8n | Visual workflow automation (coming soon) |
| Query-Driven Memory (QDM) | 8607 | Streamlit | Persistent AI memory with automatic retrieval |

## Quick Start

```bash
cd personal-demo-launcher

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

streamlit run app.py
```

Opens at [http://localhost:8501](http://localhost:8501).

## Configuration

The launcher looks for demo projects relative to a base directory. By default this is your home directory (`~/`). Override it with the `DEMO_BASE_DIR` environment variable:

```bash
export DEMO_BASE_DIR=/path/to/your/projects
streamlit run app.py
```

## License

[MIT](LICENSE)
