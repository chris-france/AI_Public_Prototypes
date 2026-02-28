"""AI Inference Cost Calculator.

Interactive Streamlit tool that compares the total cost of ownership (TCO) of
local GPU hardware against four cloud inference providers (RunPod, Lambda Labs,
AWS, GCP) over a 36-month window.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="AI Inference Cost Calculator", layout="wide")
st.title("AI Inference Cost Calculator")
st.caption("Compare TCO for local GPU builds vs cloud providers over 36 months")

# --- GPU and Cloud Data ---
GPUS = {
    "RTX 4090": {"cost": 1600, "watts": 350, "vram": 24},
    "RTX 3090": {"cost": 900, "watts": 350, "vram": 24},
    "A6000": {"cost": 4500, "watts": 300, "vram": 48},
    "A100 40GB": {"cost": 10000, "watts": 400, "vram": 40},
    "A100 80GB": {"cost": 15000, "watts": 400, "vram": 80},
    "H100": {"cost": 30000, "watts": 700, "vram": 80},
}

CLOUD_PROVIDERS = {
    "RunPod": {"rtx4090": 0.39, "rtx3090": 0.31, "a6000": 0.79, "a100_40gb": 1.64, "a100_80gb": 1.94, "h100": 2.49},
    "Lambda Labs": {"rtx4090": 0.50, "rtx3090": 0.40, "a6000": 0.80, "a100_40gb": 1.29, "a100_80gb": 1.79, "h100": 2.49},
    "AWS": {"rtx4090": 0.80, "rtx3090": 0.65, "a6000": 1.10, "a100_40gb": 2.06, "a100_80gb": 2.48, "h100": 3.99},
    "GCP": {"rtx4090": 0.75, "rtx3090": 0.60, "a6000": 1.05, "a100_40gb": 1.94, "a100_80gb": 2.35, "h100": 3.74},
}

GPU_KEY_MAP = {
    "RTX 4090": "rtx4090",
    "RTX 3090": "rtx3090",
    "A6000": "a6000",
    "A100 40GB": "a100_40gb",
    "A100 80GB": "a100_80gb",
    "H100": "h100",
}

PRESETS = {
    "Custom": None,
    "Hobbyist (100/day)": 100,
    "Startup (10k/day)": 10_000,
    "Enterprise (1M/day)": 1_000_000,
}

# --- Sidebar Inputs ---
st.sidebar.header("Configuration")

preset = st.sidebar.selectbox("Preset", list(PRESETS.keys()))

if PRESETS[preset] is not None:
    queries_per_day = st.sidebar.number_input("Queries per day", value=PRESETS[preset], min_value=1)
else:
    queries_per_day = st.sidebar.number_input("Queries per day", value=1000, min_value=1)

model_vram = st.sidebar.number_input("Model VRAM requirement (GB)", value=16, min_value=1)
electricity_rate = st.sidebar.number_input("Electricity rate ($/kWh)", value=0.12, min_value=0.0, step=0.01, format="%.2f")
gpu_type = st.sidebar.selectbox("GPU Type", list(GPUS.keys()))

gpu = GPUS[gpu_type]

# Hardware cost input
if preset == "Custom":
    hardware_cost = st.sidebar.number_input(
        "Local Hardware Cost ($)", value=gpu["cost"], min_value=0, step=100
    )
else:
    hardware_cost = gpu["cost"]
    st.sidebar.markdown(f"**Hardware: {gpu_type} @ ${hardware_cost:,}**")

# Seconds per inference to derive GPU hours from query volume
secs_per_inference = st.sidebar.number_input("Seconds per inference", value=2.0, min_value=0.1, step=0.1, format="%.1f")

gpus_needed = max(1, -(-model_vram // gpu["vram"]))  # ceiling division

# --- Calculations ---
queries_per_month = queries_per_day * 30
gpu_hours_per_month = (queries_per_month * secs_per_inference) / 3600

# Local costs
hardware_upfront = hardware_cost * gpus_needed
power_monthly = (gpu["watts"] * gpus_needed * gpu_hours_per_month / 1000) * electricity_rate
hardware_monthly = hardware_upfront / 36
local_monthly = hardware_monthly + power_monthly
local_3yr = hardware_upfront + power_monthly * 36

# Cloud costs
cloud_monthly = {}
cloud_3yr = {}
for provider, rates in CLOUD_PROVIDERS.items():
    hourly = rates[GPU_KEY_MAP[gpu_type]]
    monthly = hourly * gpu_hours_per_month * gpus_needed
    cloud_monthly[provider] = monthly
    cloud_3yr[provider] = monthly * 36

# Cost per 1000 inferences
local_per_1k = (local_monthly / queries_per_month * 1000) if queries_per_month > 0 else 0
cloud_per_1k = {}
for provider, monthly in cloud_monthly.items():
    cloud_per_1k[provider] = (monthly / queries_per_month * 1000) if queries_per_month > 0 else 0

# Break-even month vs cheapest cloud
cheapest_cloud_name = min(cloud_monthly, key=cloud_monthly.get)
cheapest_cloud_monthly = cloud_monthly[cheapest_cloud_name]

local_recurring = power_monthly  # monthly power only (after upfront)

if cheapest_cloud_monthly > local_recurring and cheapest_cloud_monthly > 0:
    breakeven_month = hardware_upfront / (cheapest_cloud_monthly - local_recurring)
    breakeven_month = round(breakeven_month, 1)
else:
    breakeven_month = None

# --- Display Metrics ---
st.subheader("Monthly Cost Summary")
if gpus_needed > 1:
    st.info(f"Model requires {model_vram} GB VRAM — **{gpus_needed}x {gpu_type}** needed.")

cols = st.columns(2 + len(CLOUD_PROVIDERS))
cols[0].metric("Local (monthly)", f"${local_monthly:,.2f}")
cols[1].metric("Local (3-yr TCO)", f"${local_3yr:,.2f}")
for i, (provider, monthly) in enumerate(cloud_monthly.items()):
    cols[2 + i].metric(f"{provider} (monthly)", f"${monthly:,.2f}")

if breakeven_month is not None and breakeven_month > 0:
    if breakeven_month <= 36:
        st.success(f"Break-even vs {cheapest_cloud_name} at **month {breakeven_month}**")
    else:
        st.warning(f"Break-even vs {cheapest_cloud_name} at month {breakeven_month} (beyond 3-year window)")
else:
    st.error("Local option does not break even against cloud at this usage level.")

# --- Charts ---
col_left, col_right = st.columns(2)

# Line chart: cumulative cost over 36 months
months = list(range(0, 37))
local_cumulative = [hardware_upfront + local_recurring * m for m in months]

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=months, y=local_cumulative, name=f"Local ({gpu_type})", mode="lines"))
for provider, monthly in cloud_monthly.items():
    cumulative = [monthly * m for m in months]
    fig_line.add_trace(go.Scatter(x=months, y=cumulative, name=provider, mode="lines"))
fig_line.update_layout(title="Cumulative Cost Over 36 Months", xaxis_title="Month", yaxis_title="Total Cost ($)", height=450)

with col_left:
    st.plotly_chart(fig_line, use_container_width=True)

# Bar chart: cost per 1000 inferences
labels = [f"Local ({gpu_type})"] + list(cloud_per_1k.keys())
values = [local_per_1k] + list(cloud_per_1k.values())

fig_bar = go.Figure(go.Bar(x=labels, y=values, text=[f"${v:.4f}" for v in values], textposition="auto"))
fig_bar.update_layout(title="Cost per 1,000 Inferences", yaxis_title="Cost ($)", height=450)

with col_right:
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Detailed Table ---
st.subheader("Detailed Comparison")
rows = [
    {"Option": f"Local ({gpu_type})", "Monthly": f"${local_monthly:,.2f}", "3-Year TCO": f"${local_3yr:,.2f}", "Per 1k Inferences": f"${local_per_1k:,.4f}"},
]
for provider in CLOUD_PROVIDERS:
    rows.append({
        "Option": provider,
        "Monthly": f"${cloud_monthly[provider]:,.2f}",
        "3-Year TCO": f"${cloud_3yr[provider]:,.2f}",
        "Per 1k Inferences": f"${cloud_per_1k[provider]:,.4f}",
    })
st.table(pd.DataFrame(rows))

# --- Local Cost Breakdown ---
gpu_label = f"{gpus_needed}x {gpu_type}" if gpus_needed > 1 else gpu_type
st.info(
    f"**Local Cost Breakdown ({gpu_label})**\n\n"
    f"- **Hardware Purchase:** ${hardware_upfront:,.0f} (one-time)\n"
    f"- **Monthly Electricity:** ${power_monthly:,.2f} "
    f"({gpu['watts']}W x {gpu_hours_per_month:,.1f} hrs x ${electricity_rate}/kWh"
    f"{f' x {gpus_needed} GPUs' if gpus_needed > 1 else ''})\n"
    f"- **Monthly Amortized Hardware:** ${hardware_monthly:,.2f} "
    f"(${hardware_upfront:,.0f} / 36 months)\n"
    f"- **Total Monthly Cost:** ${local_monthly:,.2f}\n"
    f"- **3-Year TCO:** ${local_3yr:,.2f} "
    f"(hardware + 36 months of electricity)"
)

# --- Hardware Reference Table ---
st.subheader("Hardware Assumptions")
if preset == "Custom" and hardware_cost != gpu["cost"]:
    st.caption(f"Selected GPU: {gpu_type} — using custom price ${hardware_cost:,} (default ${gpu['cost']:,})")
else:
    st.caption(f"Selected GPU: {gpu_type}")

gpu_ref_rows = []
for name, specs in GPUS.items():
    gpu_ref_rows.append({
        "GPU Model": name,
        "Purchase Price": f"${specs['cost']:,}",
        "TDP (Watts)": specs["watts"],
        "VRAM (GB)": specs["vram"],
    })
gpu_ref_df = pd.DataFrame(gpu_ref_rows)


def highlight_selected(row):
    """Highlight the currently selected GPU row in the reference table."""
    if row["GPU Model"] == gpu_type:
        return ["background-color: #2d5f8a; color: white; font-weight: bold"] * len(row)
    return [""] * len(row)


st.dataframe(
    gpu_ref_df.style.apply(highlight_selected, axis=1),
    use_container_width=False,
    hide_index=True,
)
