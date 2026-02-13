# AI Inference Cost Calculator — User Guide

**Build vs. Buy for GPU Inference Infrastructure**

---

## What Is This Tool?

The AI Inference Cost Calculator answers a question every AI team faces: **"Should we run inference on our own hardware or pay a cloud provider?"**

You enter your workload profile — query volume, model size, GPU preference, and electricity rate — and the tool compares the total cost of ownership (TCO) of buying local GPUs against four cloud providers (RunPod, Lambda Labs, AWS, GCP) over 36 months.

It shows you exactly when (or whether) owning hardware becomes cheaper than renting it.

**Who should use this:**
- ML engineers deciding whether to buy a GPU or keep using cloud endpoints
- Startup founders evaluating infrastructure strategy as query volume scales
- Infrastructure teams building the business case for a GPU procurement
- Finance teams modeling CapEx vs. OpEx trade-offs for AI workloads
- Consultants advising clients on AI infrastructure spend

---

## Getting Started

### What You Need

- Python 3.9+ (3.10 or 3.11 recommended)

### Quick Start

```bash
cd ai-inference-cost-calculator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`. All inputs are in the left sidebar; outputs update instantly.

---

## How to Use the Calculator

Everything is controlled from the left sidebar. Change any setting and all charts and tables recalculate immediately.

### Presets

Quick-start configurations that set your daily query volume:

| Preset | Queries/Day | Who It's For |
|--------|:-:|-------------|
| Custom | You choose | Enter any value manually |
| Hobbyist | 100 | Personal projects, dev/test |
| Startup | 10,000 | Production SaaS product |
| Enterprise | 1,000,000 | High-volume platform |

For Hobbyist, Startup, and Enterprise presets, the hardware cost is locked to the selected GPU's list price and shown in the sidebar. The Custom preset unlocks a manual hardware cost field so you can model used hardware, bulk discounts, or bundled system pricing.

### Queries per Day

**This is the single most important input.** Small changes in daily volume compound over 36 months and dramatically shift the break-even point. Enter the number of inference requests your workload generates per day.

### Model VRAM Requirement (GB)

How much VRAM your model needs to run. If the model exceeds the selected GPU's VRAM, the calculator automatically provisions multiple GPUs. For example, a 70 GB model on an A6000 (48 GB) needs 2 GPUs, which doubles all hardware and electricity costs. A banner appears when this happens.

### Electricity Rate ($/kWh)

Your local electricity cost. Default is $0.12/kWh (roughly US average). For reference:

- $0.07–0.09 — Low-cost US states (Texas, Louisiana)
- $0.10–0.14 — US national average
- $0.15–0.20 — California, Northeast US
- $0.25–0.40 — Western Europe

This has minimal impact at low query volumes but becomes significant at enterprise scale with high-wattage GPUs.

### GPU Type

Six options spanning consumer to datacenter:

| GPU | Price | Power Draw | VRAM |
|-----|:-:|:-:|:-:|
| RTX 3090 | $900 | 350W | 24 GB |
| RTX 4090 | $1,600 | 350W | 24 GB |
| A6000 | $4,500 | 300W | 48 GB |
| A100 40GB | $10,000 | 400W | 40 GB |
| A100 80GB | $15,000 | 400W | 80 GB |
| H100 | $30,000 | 700W | 80 GB |

The GPU selection drives everything — hardware cost, electricity consumption, VRAM capacity, and the cloud hourly rates used for comparison.

### Seconds per Inference

Average time for a single inference request. This converts your query volume into GPU-hours. Some guidance:

- **0.5–1.0s** — Small models (7B), short prompts, quantized weights
- **1.5–3.0s** — Medium models (13B–30B), typical chat or RAG queries
- **3.0–8.0s** — Large models (70B+), long-context generation
- **8.0–30.0s** — Image generation, batch processing, multi-step pipelines

---

## Understanding the Output

### Break-Even Banner

The colored banner at the top tells you the headline:

- **Green** — "Break-even vs RunPod at month X." Local hardware pays for itself within 36 months. Lower is better.
- **Yellow** — "Break-even at month X (beyond 3-year window)." Local eventually wins, but not within a typical hardware lifecycle.
- **Red** — "Local option does not break even." Cloud is cheaper at every point. Usually means query volume is too low.

### Cumulative Cost Over 36 Months (Line Chart)

The left chart plots total dollars spent over time for each option.

The **local line starts at the hardware purchase price** on month 0 — that's your upfront CapEx — and climbs gradually as electricity accrues. Cloud lines start at $0 and climb at each provider's monthly rate.

Where a cloud line crosses above the local line is the break-even month for that provider. If the local line stays above all cloud lines for the full 36 months, cloud is cheaper.

### Cost per 1,000 Inferences (Bar Chart)

The right chart shows unit economics — what each option costs per 1,000 queries. The shortest bar is the cheapest on a per-query basis.

Local hardware typically wins here at high volumes because the fixed hardware cost gets spread across millions of queries. At low volumes, the hardware amortization per query is high and cloud wins.

### Detailed Comparison Table

One row per option showing:

| Column | What It Means |
|--------|--------------|
| Monthly | Total monthly cost for that option |
| 3-Year TCO | Total cost over 36 months |
| Per 1k Inferences | Cost per 1,000 queries |

**How to use it:** If you're optimizing for monthly cash flow, compare the Monthly column. If you're optimizing for total spend over a hardware lifecycle, compare 3-Year TCO. If you're pricing an API product, use Per 1k Inferences to set your margin.

### Local Cost Breakdown

Below the comparison table, an info box breaks out exactly what makes up the local TCO so there's no mystery about why a $1,600 GPU shows a $26,800 three-year cost:

- **Hardware Purchase** — One-time GPU cost
- **Monthly Electricity** — GPU wattage x hours running x your electricity rate
- **Monthly Amortized Hardware** — Purchase price / 36 months
- **Total Monthly Cost** — Amortized hardware + electricity
- **3-Year TCO** — Hardware + 36 months of electricity

### Hardware Assumptions Table

A reference table showing all six GPUs with price, power draw, and VRAM. The currently selected GPU is highlighted. Use this to compare options before switching.

---

## Example Scenarios

### Hobbyist: Personal Chatbot (100 queries/day, RTX 4090)

At 100 queries/day with 2-second inference, the GPU runs about 1.7 hours/month. Monthly electricity is under $0.10. But the $1,600 hardware amortizes to ~$44/month.

Cloud cost at this volume is negligible — RunPod runs about $0.65/month. The break-even calculation will show local hardware **does not break even** within 36 months.

**Takeaway:** At hobbyist volumes, cloud is dramatically cheaper. The case for owning hardware at this tier is privacy, latency, and freedom to experiment — not cost savings.

### Startup: Scaling an AI Product (10K queries/day, A6000)

At 10,000 queries/day the A6000 runs about 208 GPU-hours/month. Monthly electricity is around $9. Cloud costs range from $165/month (RunPod) to $229/month (AWS).

The local monthly cost is approximately $134/month. Break-even versus RunPod occurs around month 25–35 — right at the edge of the 3-year window.

Switch to the RTX 4090 ($1,600, same 24 GB VRAM) and break-even drops to roughly month 8–12. The tradeoff is the A6000's professional-grade reliability and ECC memory versus the 4090's consumer positioning.

**Takeaway:** At startup volumes, local hardware is competitive. The decision hinges on whether you have the staff to maintain a GPU server and handle failures.

### Enterprise: Cloud Migration Savings (1M queries/day, A100 80GB)

At 1M queries/day with a 70 GB model on an A100 80GB, cloud costs are enormous — AWS runs ~$62,000/month, GCP ~$58,750/month.

The local monthly cost is approximately $1,417/month. Break-even occurs in **month 1** — the hardware pays for itself almost immediately.

The 3-Year TCO difference is staggering: ~$51,000 local vs. ~$1.7M+ cloud. That's over **$1.6 million in savings**.

**Takeaway:** At enterprise volumes, buying hardware is an overwhelming financial win. The real question becomes operational — can you build and staff a GPU cluster? Use these numbers as the ceiling on cloud savings to justify an infrastructure build proposal.

---

## V2.0 Roadmap — Right-Size Your AI Spend

Version 1.0 answers "build or buy?" for a single model at a fixed query rate. Version 2.0 will answer the harder question: **"What is the optimal inference strategy for your actual workload mix?"**

### Workload Analysis

Most production AI systems don't run a single model at a uniform rate. A customer support platform might handle 80% of queries with a fast 7B model, route 15% to a 30B model for nuanced responses, and escalate 5% to a 70B model for complex reasoning. V2.0 will let users define a workload distribution by query complexity, then calculate the blended cost across the mix.

### Multi-Model Routing Recommendations

Given a workload distribution, the calculator will recommend which model to assign to each tier and whether each tier should run locally or in the cloud. A startup might run its high-volume simple tier on a local RTX 4090 while routing its low-volume complex tier to a cloud H100 on demand — paying for the expensive GPU only when it's truly needed.

### Cost Optimization: Single-Model vs. Optimized Mix

The core V2.0 output will be a side-by-side comparison: the cost of running every query through a single large model (today's common approach) versus an optimized multi-model pipeline. This surfaces the savings from intelligent routing — often 40–70% at scale — and gives teams a concrete dollar figure to justify the engineering investment.

### Performance vs. Cost Tradeoff

Not every query needs the best model. V2.0 will visualize the frontier of cost and quality: how much does response quality degrade as you shift queries from a 70B model to a 13B? Where is the knee in the curve — the point where further savings require unacceptable quality loss? This turns infrastructure decisions into product decisions, letting teams set quality-per-dollar thresholds aligned with user experience goals.

---

## Known Limitations

- **Static cloud pricing** — Hourly rates are hardcoded snapshots. Actual cloud pricing varies by region, commitment tier, and changes over time. Check provider pricing pages before making decisions.
- **On-demand rates only** — Spot instances (50–70% cheaper) and reserved commitments (20–40% cheaper) are not modeled. Cloud TCO in practice may be lower than shown.
- **Single-query throughput** — Assumes one query at a time per GPU. Real inference servers batch requests, increasing throughput. Local hardware's advantage may be larger than shown.
- **No multi-GPU parallelism** — When a model exceeds one GPU's VRAM, the calculator provisions multiple complete GPUs. Tensor parallelism and pipeline parallelism strategies are not modeled.
- **Electricity only** — Local TCO doesn't include server chassis, networking, cooling, rack space, maintenance, or downtime. True self-hosting costs are higher.
- **No cooling or space costs** — Colo fees (power + cooling + space) typically run 2–3x raw electricity. Adjust your electricity rate upward if modeling a colo deployment.
- **Smooth utilization** — GPU hours are averaged from daily queries. Real workloads spike and idle. Cloud's ability to scale to zero during quiet periods isn't captured.
- **Fixed 36-month window** — Hardware may last longer or need replacement sooner.
- **No tax modeling** — Hardware may qualify for accelerated depreciation (Section 179). Cloud is fully OpEx. The tax treatment difference isn't modeled.

---

*The AI Inference Cost Calculator is a planning tool. GPU pricing, cloud rates, and electricity costs should be validated against current market data before making infrastructure investments.*
