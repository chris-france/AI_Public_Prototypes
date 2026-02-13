# AI Public Prototypes

**A portfolio of AI demo applications — datacenter analytics, security testing, RAG systems, and workflow automation.**

Each project runs locally and is designed to showcase practical AI capabilities for enterprise use cases. Most use [Ollama](https://ollama.ai) for local LLM inference — no cloud API keys required unless noted.

---

## Projects

| Project | Description | Tech |
|---------|-------------|------|
| [AI Inference Cost Calculator](ai-inference-cost-calculator/) | GPU vs cloud TCO comparison over 36 months with break-even analysis | Streamlit, Plotly, Pandas |
| [Datacenter Demand Simulator](datacenter-demand-simulator/) | Capacity forecasting across compute, storage, power, and cooling with AI-powered analysis | Streamlit, Plotly, Ollama |
| [Datacenter Optimization & Valuation](datacenter-optimization-valuation/) | PE/VC datacenter investment analysis with M&A valuation across 14 global markets | Streamlit, Plotly, Ollama |
| [Model Security Scanner](model-security-scanner/) | LLM vulnerability testing across 10 attack categories for Ollama and Claude models | Streamlit, Plotly, Ollama |
| [Local RAG System](local-rag-system/) | Private AI chat with persistent document memory — fully local, no API keys | Docker, FastAPI, Qdrant, Ollama |
| [Query-Driven Memory](query-driven-memory/) | Persistent AI memory with automatic retrieval — memories reinforce with use and decay over time | Streamlit, Qdrant, Ollama |
| [Personal Demo Launcher](personal-demo-launcher/) | Single dashboard to start, stop, and monitor all demo projects | Streamlit |

## Quick Start

Each project has its own README with setup instructions. The **Personal Demo Launcher** can manage all projects from a single dashboard:

```bash
cd personal-demo-launcher
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Opens at [http://localhost:8501](http://localhost:8501).

## License

[MIT](LICENSE)
