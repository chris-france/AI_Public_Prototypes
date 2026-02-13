# AI Inference Cost Calculator

**Should you run AI inference on your own hardware or pay a cloud provider?**

This interactive tool compares the total cost of ownership (TCO) of purchasing local GPUs against four major cloud inference providers — RunPod, Lambda Labs, AWS, and GCP — over a 36-month window. It calculates break-even timing, amortized hardware costs, monthly spend, and cost per inference to support data-driven infrastructure decisions.

Built with [Streamlit](https://streamlit.io/) for instant, interactive analysis.

---

## Key Features

- **Build vs. Buy analysis** — Side-by-side comparison of local GPU ownership against four cloud providers
- **Break-even calculation** — Pinpoints the exact month when owning hardware becomes cheaper than renting
- **Preset workload profiles** — Hobbyist (100/day), Startup (10K/day), Enterprise (1M/day), or fully custom
- **Six GPU tiers** — RTX 3090, RTX 4090, A6000, A100 40GB, A100 80GB, H100
- **Multi-GPU auto-scaling** — Automatically provisions additional GPUs when model VRAM exceeds a single card
- **Interactive charts** — Cumulative cost curves and per-inference unit economics, powered by Plotly

## Quick Start

```bash
git clone git@github.com:chris-france/AI_Public_Prototypes.git
cd AI_Public_Prototypes/ai-inference-cost-calculator

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

streamlit run app.py
```

Opens at [http://localhost:8501](http://localhost:8501).

## Who This Is For

| Role | Use Case |
|------|----------|
| **ML Engineers** | Decide whether to buy a GPU or keep using cloud endpoints |
| **Startup Founders** | Evaluate infrastructure strategy as query volume scales |
| **Infrastructure Teams** | Build the business case for GPU procurement |
| **Finance Teams** | Model CapEx vs. OpEx trade-offs for AI workloads |

## Documentation

See [USER_GUIDE.md](USER_GUIDE.md) for detailed configuration options, output interpretation, example scenarios, and known limitations.

## License

[MIT](LICENSE)
