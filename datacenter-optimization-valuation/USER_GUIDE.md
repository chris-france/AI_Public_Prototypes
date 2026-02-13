# Datacenter Deployment Optimizer & Valuation — User Guide

**Enterprise Deployment Analysis & M&A Valuation for PE/VC**

---

## What Is This Tool?

The Datacenter Deployment Optimizer answers two questions central to datacenter capital allocation:

1. **Build decisions:** Given a capacity requirement, region, budget, and timeline, which deployment approach — ground-up construction, modular/prefab, or hybrid — delivers the best risk-adjusted return?

2. **Buy decisions:** Given an acquisition target, what is its fair market value, how does the asking price compare, and should you buy, negotiate, or pass?

The tool models 14 global markets with region-specific construction costs, land prices, power rates, labor multipliers, PUE benchmarks, utilization rates, and recent M&A transaction comparables. It calculates CapEx, 10-year OpEx, projected ROI, resale value, risk scores, and timeline feasibility across three deployment approaches simultaneously.

For acquisitions, it runs a seven-factor valuation model that adjusts for utilization, efficiency, contract quality, contract duration, expansion potential, building age, and land ownership.

An optional Ollama integration generates natural-language strategic recommendations using a local LLM.

**Who should use this:**
- Private equity and infrastructure fund teams evaluating datacenter investments
- VC firms diligencing datacenter platform companies
- REITs analyzing acquisition targets
- Datacenter developers comparing build approaches and regional economics
- Corporate infrastructure teams making build-vs-lease decisions
- Investment bankers preparing deal memoranda and valuation decks

---

## Getting Started

### What You Need

- Python 3.9+ (3.10 or 3.11 recommended)
- Ollama (optional) — enables AI-powered strategic recommendations

### Quick Start

```bash
cd datacenter-deployment-optimizer
chmod +x run.sh
./run.sh
```

The script handles virtual environment setup, dependency installation, Ollama detection, and app launch. Opens in your browser at `http://localhost:8501`.

Without Ollama, the tool generates rule-based recommendations using built-in decision logic. With Ollama running, it produces richer narrative-style strategic analysis. Any Ollama model works — default is `llama3.2`.

---

## How to Use the Tool

Unlike a traditional dashboard with a shared sidebar, this tool places inputs directly within each tab. The Deployment Analysis tab and M&A Valuation tab each have their own dedicated input forms with a "Run Analysis" button.

---

## Tab 1: Deployment Analysis

This tab compares three deployment approaches for a new datacenter build: ground-up construction, modular/prefab, and hybrid.

### Inputs

**Total Power Capacity (MW)** — The critical IT load you need to deploy (1–500 MW, default 20). This is the primary scaling factor for every cost calculation. A 50 MW facility is not simply 2.5x the cost of 20 MW — some costs scale sub-linearly (land, permitting) while others scale super-linearly (power infrastructure complexity).

**Rack Count** — Number of rack positions required (10–10,000, default 500). A high MW-to-rack ratio signals high-density deployment favoring liquid cooling. A low ratio indicates conventional density where air cooling suffices.

**Geographic Region** — 14 global markets, each with its own cost structure:

| Region | CapEx/MW | Power Rate | Key Characteristics |
|--------|:-:|:-:|------------|
| Northern Virginia | $8.5M | $0.065 | Largest US market, hyperscale hub |
| Dallas-Fort Worth | $7.2M | $0.058 | Lowest power cost in Tier 1 |
| Phoenix | $7.0M | $0.072 | Fastest demand growth (25% YoY) |
| Chicago | $8.0M | $0.078 | Financial services hub |
| Silicon Valley | $12.0M | $0.145 | Highest US land costs |
| New York/New Jersey | $11.5M | $0.125 | Premium market, high labor |
| Atlanta | $7.5M | $0.082 | Only Tier 2 market |
| Seattle | $9.5M | $0.048 | Cheapest power (hydro) |
| Los Angeles | $10.5M | $0.135 | Content/media hub |
| Amsterdam | $9.0M | $0.115 | European interconnection hub |
| London | $11.0M | $0.155 | Premium European market |
| Frankfurt | $9.5M | $0.175 | Highest European power cost |
| Singapore | $13.0M | $0.125 | Constrained supply, highest utilization |
| Tokyo | $14.0M | $0.165 | Most expensive construction |

Choosing Dallas versus Tokyo can change CapEx by nearly 2x.

**Timeline Urgency** — How fast you need the facility online:

| Level | Target Window | Cost Impact | Risk Impact |
|-------|:-:|:-:|:-:|
| Standard | 24–30 months | None | None |
| Accelerated | 15–20 months | +8% CapEx | +10 risk points |
| Critical | Under 12 months | +18% CapEx | +25 risk points |

Only modular deployment can typically deliver under 12 months.

**Maximum CapEx Budget ($M)** — Your capital ceiling ($10M–$5B). The tool flags each approach as "Meets Budget: Yes/No" so you know immediately if rescoping is needed.

**Redundancy Level** — Uptime requirements drive major cost differences:

| Level | Uptime | Cost Multiplier | Equivalent |
|-------|:-:|:-:|:-:|
| N | 99.50% | 1.00x | Tier I |
| N+1 | 99.82% | 1.15x | Tier II/III |
| 2N | 99.95% | 1.45x | Tier III+ |
| 2N+1 | 99.99% | 1.60x | Tier IV |

Moving from N+1 to 2N adds 30 percentage points to the CapEx multiplier — on a $170M base, that's $51M in additional cost.

**Cooling Strategy** — Impacts both upfront cost and long-term efficiency:

| Type | Max Density | Cost Multiplier | PUE Improvement |
|------|:-:|:-:|:-:|
| Air Cooling | 15 kW/rack | 1.00x | Baseline |
| Liquid Cooling | 100 kW/rack | 1.18x | -0.15 PUE |
| Hybrid | 50 kW/rack | 1.12x | -0.08 PUE |

AI/ML workloads increasingly require liquid cooling for rack densities above 30 kW. The higher upfront cost is offset by lower long-term power bills.

### Understanding the Results

After clicking **Run Deployment Analysis**, results appear in five sections:

**Executive Summary** — Four metric cards showing the winner in each category: Lowest Total Cost, Fastest Deployment, Best ROI, and Most Flexible. These may not all point to the same approach — that tension is the core of the build decision.

**Comparison Dashboard** — Side-by-side charts for CapEx, Timeline, 10-Year Total Cost, and Risk Score across all three approaches.

**Detailed Comparison Table** — One row per approach with CapEx, CapEx/MW, Annual OpEx, 10-Year OpEx, Total 10-Year Cost, Timeline, PUE, Flexibility Score, Risk Score, ROI, Resale Value, and whether it meets your budget and timeline constraints.

**Risk Assessment** — Three panels listing specific risk factors for each approach. Ground-up risks include permitting delays and labor availability. Modular risks include module availability and transportation logistics. Hybrid risks include coordination complexity.

**AI Strategy Recommendation** — A narrative recommendation covering suggested approach, rationale, key risks with mitigations, financial considerations, and timing factors.

---

## Tab 2: M&A Valuation

This tab evaluates datacenter acquisition targets using a seven-factor valuation model.

### Inputs

**Deal Parameters:**

- **Asking Price ($M)** — The seller's listed price, compared against calculated fair value
- **Claimed Capacity (MW)** — Total IT load capacity as stated by the seller
- **Actual Utilization (%)** — Percentage of capacity currently occupied and generating revenue (default 72%)
- **Current PUE** — Power Usage Effectiveness (default 1.42). Lower is better
- **Asset Region** — Same 14 markets as deployment tab, sets benchmark comparables

**Asset Details:**

- **Contract Quality** — Creditworthiness of the tenant base:

| Quality | Typical Tenants | Valuation Impact |
|---------|----------------|:-:|
| Hyperscale | AWS, Azure, Google, Meta | +25% |
| Enterprise | Fortune 500 | +10% |
| Mixed | Diverse portfolio | Baseline |
| Retail/SMB | Small businesses | -15% |

- **Average Contract Term (years)** — Contracts longer than 3 years earn a 2% premium per additional year. A 10-year average term adds 14% to base value.
- **Expansion Capacity (MW)** — Additional MW buildable on the site, valued at 30% of regional construction cost
- **Building Age (years)** — 2.5% depreciation per year, capped at 35% total
- **Land Owned** — If checked, land is valued at regional cost per acre and added to fair value
- **Land Size (acres)** — Larger parcels in expensive markets can represent significant value (Singapore at $3.5M/acre, Tokyo at $4M/acre)

### Understanding the Results

**Key Metrics** — Fair Market Value, Asking Price, Valuation Gap (dollar difference), and Market Comp (regional $/MW).

**Recommendation Banner:**
- **Green (BUY/ATTRACTIVE)** — Asset is undervalued, proceed
- **Yellow (FAIR VALUE/NEGOTIATE)** — Priced near fair value, negotiate terms
- **Red (PASS)** — Significant premium to fair value, walk away

**Key Findings** — Automatically detected flags like "Overbuilt Capacity" (utilization below 50%), "Potential Undervalued Asset" (strong utilization with 20%+ discount), or "Concentration Risk" (hyperscale contracts at 90%+ utilization indicating single-tenant dependency).

**Valuation Waterfall** — A waterfall chart showing how fair value was built: base value (MW × regional comparable), then each of the seven adjustment factors adding or subtracting value, ending at the final fair value with the asking price plotted alongside for comparison. The gap between these bars is your negotiation territory.

**Valuation Adjustments Table** — Each factor with its dollar impact and assessment indicator. Use this to understand which factors drive the most value — and which represent negotiation leverage.

**AI Deal Analysis** — Narrative analysis covering deal assessment, key value drivers and risks, suggested negotiation strategy with specific price targets, and integration considerations.

---

## Tab 3: Market Benchmarks & Transaction Comps

A read-only reference library with no inputs. Contains:

- **Regional Cost Benchmarks** — All 14 markets with CapEx/MW, transaction comps, power costs, PUE, utilization, demand growth, and land costs
- **Regional Comparison Charts** — Construction cost per MW and M&A transaction comp per MW by region. Where transaction comps significantly exceed construction cost (e.g., Singapore), investor demand is strong and supply is constrained
- **Deployment Approach Characteristics** — Reference table comparing ground-up, modular, and hybrid on timeline, cost premium, flexibility, resale premium, PUE, and scalability
- **Data Sources & Methodology** — Benchmark sources include JLL, CBRE, Cushman & Wakefield, Uptime Institute, and public M&A filings

---

## Example Scenarios

### Scenario A: 10 MW Build Decision in Dallas (18-Month Window)

A mid-market colo provider needs 10 MW in Dallas with an 18-month deadline, $100M budget, N+1 redundancy, air cooling.

**What to look for:** Dallas has the second-lowest CapEx/MW ($7.2M), so all three approaches should come in well under budget. Check the Decision Timeline — ground-up at 24 months won't meet the 18-month window even with acceleration. Modular delivers in about 8 months; hybrid in about 13 months. Both meet the deadline.

Compare 10-Year Total Cost: ground-up has the lowest lifecycle cost but fails the timeline. The AI recommendation will likely suggest hybrid — it meets the accelerated timeline, costs less than modular, and offers more customization for tenant fit-out.

**Takeaway:** In a cost-effective market with a tight timeline, hybrid often emerges as the best balance. Ground-up is cheapest but too slow; modular is fastest but the CapEx premium may not be justified when hybrid also meets the deadline.

### Scenario B: PE Firm Valuing a 20 MW Acquisition in Chicago

A PE firm is evaluating a 20 MW facility. Seller asking $250M. The facility is 6 years old, 72% utilized, PUE of 1.42, mixed enterprise/retail contracts averaging 4.5 years, 10 MW expansion capacity on 8 owned acres.

**What to look for:** Chicago's transaction comparable is $11M/MW, so the base value is $220M. The valuation waterfall shows each adjustment — utilization is slightly positive (72% vs. 70% market average), PUE is neutral (matches market), mixed contracts get no premium, 4.5-year terms earn a small premium (+3%), expansion capacity adds ~$24M, building age subtracts ~15%, land adds ~$2.2M.

Compare the fair value against the $250M ask. If fair value comes in around $240–260M, it's a fair deal and the recommendation is to negotiate. Below $210M means it's overvalued.

**Takeaway:** The seven-factor model decomposes the valuation into defensible adjustments. Each waterfall line item becomes a negotiation point — point to specific factors (age depreciation, no contract premium) as justification for your counter-offer.

### Scenario C: Comparing Regions for a 50 MW Hyperscale Build

A cloud provider evaluating Northern Virginia, Phoenix, and Frankfurt. 50 MW, 2N redundancy, hybrid cooling, $750M budget, standard timeline.

Run three separate analyses with identical settings except region.

**What to compare:**
- **CapEx:** NOVA ($8.5M/MW) vs. Phoenix ($7.0M/MW) vs. Frankfurt ($9.5M/MW). The absolute difference between Phoenix and NOVA could be $100M+.
- **10-Year OpEx:** Power rates dominate. Frankfurt at $0.175/kWh is nearly 3x Phoenix at $0.072/kWh. NOVA's $0.065/kWh is the best of the three.
- **ROI:** NOVA has the highest market premium (1.15x) and strong demand growth. Phoenix has the fastest growth (25% YoY). Frankfurt's growth is slower but utilization is very high (85%), signaling supply constraints with pricing power.
- **Resale Value:** Custom-built facilities in premium markets (NOVA) command better exit multiples than modular builds.

**Takeaway:** The lowest CapEx market isn't necessarily the best investment. When you factor in revenue premiums, demand growth, and 10-year OpEx, a more expensive market like NOVA may deliver superior risk-adjusted returns.

---

## Known Limitations

- **Static market data** — Benchmarks reflect 2024–2025 conditions and are hardcoded. Validate against current broker reports before making decisions.
- **Single-facility scope** — Models one facility at a time. Cannot optimize across a portfolio or model phased multi-campus deployments.
- **Simplified revenue model** — Revenue estimated at $120/kW/month adjusted by market premium. Actual revenue depends on contract-level pricing, TI allowances, and metered power margins.
- **No DCF or IRR** — Uses simple ROI, not discounted cash flow. Does not model time value of money, debt financing, or tax shields.
- **Fixed OpEx ratios** — Maintenance at 2.5% of CapEx, staffing at $150K/MW, insurance at 0.5%. Actual figures vary by operator.
- **No construction phasing** — Assumes single-phase build. Large deployments are typically phased, which changes cash flow timing.
- **No lease-vs-own comparison** — Evaluates three build approaches but doesn't compare against leasing from a wholesale provider.
- **Valuation weights not adjustable** — The seven-factor sensitivities are fixed. Users can't adjust weights to reflect their own investment thesis.
- **AI variability** — LLM recommendations vary between runs. They should inform discussion, not replace underwriting.

---

## V2.0 Roadmap

**Financial Sensitivity Analysis** — Interactive sensitivity controls for key assumptions (power rate, utilization, contract rate, discount rate, exit cap rate). A sensitivity matrix showing IRR across a grid of utilization rates and pricing scenarios to identify break-even utilization for any given CapEx.

**Discounted Cash Flow & IRR Modeling** — Full 10-year DCF replacing simple ROI. Configurable debt/equity splits, interest rates, tax rates, depreciation schedules, and terminal value. Output includes levered/unlevered IRR, equity multiple, cash-on-cash returns, and DSCR — the metrics PE investment committees actually use.

**Multi-Site Portfolio Optimization** — Model a portfolio of deployments with shared capital budget. Allocate MW across regions to maximize portfolio-level returns given CapEx constraints, diversification requirements, and timeline sequencing.

**Demand Simulator Integration** — Feed capacity growth projections from the companion Datacenter Demand Simulator to automatically determine when new capacity is needed, how much, in which region, and via which approach.

**Enhanced AI Analysis** — Targeted recommendations including negotiation scripts for M&A deals, risk mitigation playbooks, comparable transaction commentary, and integration checklists. Conversational follow-up to ask clarifying questions about the analysis.

**Export & Reporting** — One-click export of investment committee deal memoranda (PDF), deployment comparison decks (PowerPoint), and full data packages (Excel) with charts, tables, and narrative analysis.

---

*The Datacenter Deployment Optimizer is an analytical planning tool. Market benchmarks are derived from published industry research and should be validated against current broker data, engineering estimates, and legal diligence before making capital allocation decisions.*
