# Datacenter Demand Simulator — User Guide

**Version 1.0 | Strategic Capacity Planning for Enterprise Infrastructure**

---

## What Is This Tool?

The Datacenter Demand Simulator helps infrastructure leaders answer a simple question: **"How much datacenter capacity will we need over the next 3–10 years?"**

You provide your company's profile — industry, size, growth rate, workload types, AI adoption level, and compliance requirements — and the simulator projects future demand across five dimensions: compute, storage, power, cooling, and network bandwidth.

It runs four scenarios simultaneously so you can plan for best case, worst case, and everything in between.

**Who should use this:**
- Infrastructure VPs and CTOs planning capacity expansions
- Datacenter operations teams sizing power, cooling, and compute
- Capacity planning analysts modeling demand under different assumptions
- Consultants and sales engineers presenting growth trajectories to prospects
- PE/VC teams performing diligence on datacenter investments

---

## Getting Started

### What You Need

- **Python 3.9+** (3.10 or 3.11 recommended)
- **Ollama** (optional) — only needed if you want AI-powered strategic analysis

### Quick Start

```bash
cd datacenter-demand-simulator
chmod +x run.sh
./run.sh
```

The launch script handles everything — creates a virtual environment, installs dependencies, checks for Ollama, and opens the app in your browser at `http://localhost:8501`.

If you prefer to run manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## How to Use the Simulator

Everything is controlled from the left sidebar. Change any setting and the projections update instantly.

### Business Parameters

**Industry Sector** — Choose your industry. Each one has different baseline capacity needs per employee. For example, Technology companies need roughly 2.5x the compute per employee compared to Manufacturing. This also affects how aggressively AI workloads scale your demand.

**Employee Count** — Your current headcount (100–500,000). All capacity baselines scale linearly with this number.

**Annual Growth Rate** — Expected year-over-year growth (0–50%). This compounds annually and drives organic demand growth across all dimensions.

### Workload Profile

**Primary Workload Types** — Select the workloads your datacenter supports. Each workload type has different resource multipliers. For example:

| Workload | Impact on Compute | Impact on Storage | Impact on Power |
|----------|:-:|:-:|:-:|
| General Compute | Baseline | Baseline | Baseline |
| AI/ML Training | 5x | 2x | 4x |
| AI/ML Inference | 2.5x | Baseline | 2x |
| Big Data Analytics | 2x | 4x | 1.8x |
| High-Performance Computing | 3x | 1.5x | 2.5x |
| Database Operations | 1.5x | 3x | 1.3x |

When you select multiple workloads, their multipliers are averaged together.

**AI/ML Intensity** — A slider from 0.0 to 1.0 that controls how much AI amplifies your demand. At 0.0, no AI multiplier is applied. At 1.0, the full industry AI multiplier takes effect. For a Technology company at 1.0, this means a 2.5x boost to compute and power.

### Compliance Requirements

Select the compliance frameworks you must meet. Each one adds redundancy and security overhead to your capacity projections:

| Framework | Capacity Overhead |
|-----------|:-:|
| ISO 27001 | ~1.2x |
| SOC 2 Type II | ~1.3x |
| GDPR | ~1.3x |
| PCI DSS | ~1.5x |
| HIPAA | ~1.5x |
| FedRAMP | ~1.8x |

These compound — running both HIPAA and FedRAMP means roughly 1.7x overhead on infrastructure capacity.

### Projection Settings

**Projection Horizon** — How far out to project, from 3 to 10 years. Longer horizons amplify the gap between conservative and aggressive scenarios.

### AI Analysis

**Enable AI-Powered Analysis** — Turns on the AI Analysis tab, which uses a local Ollama model to generate strategic recommendations. All processing happens on your machine — no data leaves your network.

**Ollama Model** — Which local model to use. Default is `qwen2.5:14b`. Larger models give better analysis but take longer.

---

## Understanding the Output

The main area shows a summary bar with your configuration, a metrics row with end-of-horizon projections and growth percentages, and four tabs.

### Tab 1: Capacity Projections

This is your primary planning view. It shows how each resource dimension (compute, storage, power, cooling) grows over time across all four scenarios.

The key visual is a set of timeline charts with a shaded confidence band spanning the Conservative-to-Aggressive range. If that band is wide, you have significant planning uncertainty and should consider sizing infrastructure for the aggressive case.

A **Growth Waterfall** chart breaks down what's driving compute growth — typically organic headcount growth (~40%), AI/ML workloads (~35%), compliance overhead (~15%), offset by technology efficiency gains (~-10%).

### Tab 2: Risk Scenarios

A heatmap view that quickly shows which scenario/dimension combinations carry the highest risk. Red cells with 400%+ growth in Power mean you may need new utility feeds or generator capacity.

The four scenarios are:

- **Conservative** — 0.7x growth, 0.5x AI adoption, higher efficiency
- **Base Case** — Your inputs as entered
- **Aggressive** — 1.4x growth, 1.5x AI adoption, lower efficiency gains
- **Technology Disruption** — 1.2x growth, 2.5x AI adoption (the "what if AI explodes" scenario)

### Tab 3: Decision Timeline

This answers **"when do I need to act?"** It shows decision deadlines for each capacity type, factoring in procurement lead times:

| Resource | Lead Time |
|----------|:-:|
| Storage | 2 months |
| Compute | 3 months |
| Network | 4 months |
| Power | 18 months |
| Cooling | 18 months |

Urgency levels: **CRITICAL** = decision needed within 6 months, **HIGH** = within 12 months.

Power and cooling have 18-month lead times, so the tool will often flag these as the earliest decision points. This is by design — ordering switchgear, transformers, and cooling plants takes far longer than racking servers.

### Tab 4: AI Analysis

When Ollama is running, this tab generates a strategic assessment covering executive summary, critical decision points, top risks, investment priorities, and alternative strategies.

The analysis is generated by a local LLM and will vary between runs. Treat it as a starting point for discussion, not a deterministic recommendation.

### Data Tables

Below the tabs, an expandable section contains year-by-year projection tables for each scenario with CSV download buttons.

---

## Example Scenarios

### Planning a 10 MW Expansion (Growing Tech Company)

A 15,000-employee SaaS company growing at 20% annually with heavy AI adoption.

**Settings:** Technology, 15K employees, 20% growth, AI/ML Training + Inference workloads, 0.8 AI intensity, SOC 2 + GDPR, 7-year horizon.

**What to look for:** Check the Power timeline — expect multi-MW growth under Base Case. Look at the Decision Timeline for power and cooling deadlines; with 18-month lead times, you may already be inside the ordering window. The Aggressive scenario is your stress-test ceiling — size electrical infrastructure for this case, not Base Case, since AI adoption has historically outpaced forecasts.

### Healthcare System: Colocation vs. On-Premises

A 3,000-employee hospital network with HIPAA and SOC 2 compliance.

**Settings:** Healthcare, 3K employees, 8% growth, General Compute + Database + DR workloads, 0.3 AI intensity, HIPAA + SOC 2, 5-year horizon.

**What to look for:** Note the compliance overhead — HIPAA + SOC 2 compounds to roughly 1.4x on all capacity. Healthcare's lower growth volatility means the scenario fan is narrow, which is good for planning certainty. With moderate growth and low AI intensity, power decisions are likely LOW urgency, giving you time to evaluate colo pricing.

### Media Company: AI Content Production Stress Test

A 1,200-employee media company going all-in on AI-generated content.

**Settings:** Media & Entertainment, 1.2K employees, 12% growth, AI/ML Training + Inference + Big Data workloads, 1.0 AI intensity (max), SOC 2, 5-year horizon.

**What to look for:** Storage is the standout metric — Media carries 100 TB per 100 employees baseline plus Big Data's 4x multiplier. The Technology Disruption scenario with 2.5x AI adoption on top of the already-high AI intensity creates exponential compute and power growth. This validates that AI adoption pace, not headcount growth, is your primary capacity driver.

---

## AI Analysis Setup

If the AI Analysis tab shows "AI analysis not available," Ollama isn't running.

**To set up:**

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Start the server: `ollama serve`
3. Pull a model: `ollama pull qwen2.5:14b`

**Recommended models:**

| Model | RAM Needed | Speed | Best For |
|-------|:-:|:-:|---------|
| `llama3.2` (3B) | 4GB+ | Fast | Quick iterations, lower-end hardware |
| `mistral` (7B) | 8GB+ | Fast | Good balance on modest hardware |
| `qwen2.5:14b` (14B) | 16GB+ | Moderate | Default — best quality/speed tradeoff |
| `qwen2.5:32b` (32B) | 32GB+ | Slow | Deep analysis |

**Troubleshooting:**

- "Ollama is not available" → Run `ollama serve` in a terminal
- Spinner hangs → Model not pulled. Run `ollama list` to check, then `ollama pull <model>`
- Slow responses (30+ sec) → Model too large for your RAM. Try a smaller one
- Low quality analysis → Model too small. Upgrade to 14B or larger

---

## Known Limitations

- **No cost modeling** — Projects capacity (cores, TB, MW) but not dollars. You need to apply your own unit economics.
- **Averaged workload multipliers** — Selecting multiple workloads averages them, which can understate demand if one extreme workload dominates your actual load.
- **Linear scaling** — A 50,000-person company doesn't necessarily consume 10x what a 5,000-person company does, but the model assumes it does.
- **Smooth growth** — Real demand arrives in steps (acquisitions, product launches, seasonal surges), not smooth curves.
- **Fixed capacity headroom** — Assumes current capacity is 30% above today's baseline. You can't input your actual installed capacity.
- **Single-site scope** — Models aggregate demand without multi-site distribution or geographic redundancy.

---

## V2.0 Roadmap

**Financial Modeling** — CapEx/OpEx estimation, build-vs-colo-vs-cloud TCO comparison, sensitivity analysis on power rates and hardware refresh cycles.

**Custom Capacity Inputs** — User-defined installed capacity, per-workload percentage allocation instead of averaged multipliers, custom industry baselines.

**Multi-Site Planning** — Model capacity across multiple datacenters, latency-constrained workload placement, regional power cost differences.

**Scenario Customization** — User-defined scenario modifiers, import/export configurations, Monte Carlo simulation with randomized growth paths.

**Enhanced AI Analysis** — Decision-point-specific recommendations, industry benchmark comparisons, natural-language Q&A over projection data.

**Export & Reporting** — PDF executive summaries, PowerPoint slide deck export, scheduled reports.

---

*Datacenter Demand Simulator is an open planning tool. Industry baselines are derived from market research benchmarks and should be validated against your organization's actual telemetry before making procurement decisions.*
