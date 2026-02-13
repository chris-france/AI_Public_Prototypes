"""
Visualization components for datacenter demand simulator.
Executive-quality charts using Plotly.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Executive color palette
COLORS = {
    "primary": "#1E3A5F",
    "secondary": "#3D5A80",
    "accent": "#4ECDC4",
    "warning": "#FF6B6B",
    "success": "#2ECC71",
    "neutral": "#95A5A6",
    "conservative": "#3498DB",
    "base": "#2C3E50",
    "aggressive": "#E74C3C",
    "disruption": "#9B59B6",
}

SCENARIO_COLORS = {
    "Conservative": COLORS["conservative"],
    "Base Case": COLORS["base"],
    "Aggressive": COLORS["aggressive"],
    "Technology Disruption": COLORS["disruption"],
}


def create_capacity_timeline(scenarios: dict, metric: str, title: str, unit: str) -> go.Figure:
    """Create a multi-scenario timeline chart for a specific metric."""
    fig = go.Figure()

    column_map = {
        "compute": "Compute_Cores",
        "storage": "Storage_TB",
        "power": "Power_MW",
        "cooling": "Cooling_Tons",
        "network": "Network_Gbps",
    }

    col = column_map.get(metric, metric)

    for scenario_name, df in scenarios.items():
        color = SCENARIO_COLORS.get(scenario_name, COLORS["neutral"])

        # Main line
        fig.add_trace(
            go.Scatter(
                x=df["Year"],
                y=df[col],
                mode="lines+markers",
                name=scenario_name,
                line=dict(color=color, width=3 if scenario_name == "Base Case" else 2),
                marker=dict(size=8 if scenario_name == "Base Case" else 6),
                hovertemplate=f"<b>{scenario_name}</b><br>"
                + "Year: %{x}<br>"
                + f"{title}: %{{y:,.1f}} {unit}<extra></extra>",
            )
        )

    # Add confidence band for base case
    if "Base Case" in scenarios and "Conservative" in scenarios and "Aggressive" in scenarios:
        base_df = scenarios["Base Case"]
        cons_df = scenarios["Conservative"]
        aggr_df = scenarios["Aggressive"]

        fig.add_trace(
            go.Scatter(
                x=list(base_df["Year"]) + list(base_df["Year"])[::-1],
                y=list(cons_df[col]) + list(aggr_df[col])[::-1],
                fill="toself",
                fillcolor="rgba(52, 152, 219, 0.1)",
                line=dict(color="rgba(255,255,255,0)"),
                hoverinfo="skip",
                showlegend=False,
                name="Confidence Band",
            )
        )

    fig.update_layout(
        title=dict(
            text=f"<b>{title} Projection</b>",
            font=dict(size=20, color=COLORS["primary"]),
            x=0.5,
        ),
        xaxis=dict(
            title="Year",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            tickfont=dict(size=12),
        ),
        yaxis=dict(
            title=f"{title} ({unit})",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            tickfont=dict(size=12),
            tickformat=",.0f" if metric != "power" else ",.2f",
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=11)
        ),
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=400,
        margin=dict(l=60, r=40, t=80, b=60),
    )

    return fig


def create_summary_dashboard(summary: dict) -> go.Figure:
    """Create a summary dashboard with key metrics."""
    fig = make_subplots(
        rows=2,
        cols=2,
        specs=[
            [{"type": "indicator"}, {"type": "indicator"}],
            [{"type": "indicator"}, {"type": "indicator"}],
        ],
        vertical_spacing=0.3,
        horizontal_spacing=0.2,
    )

    # Compute Growth
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=summary["projected_compute"],
            number=dict(suffix=" cores", font=dict(size=32, color=COLORS["primary"])),
            title=dict(text="<b>Compute Capacity</b><br><span style='font-size:12px'>End of Projection</span>", font=dict(size=14)),
            delta=dict(
                reference=summary["baseline_compute"],
                relative=True,
                valueformat=".0%",
                increasing=dict(color=COLORS["accent"]),
            ),
        ),
        row=1,
        col=1,
    )

    # Storage Growth
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=summary["projected_storage"],
            number=dict(suffix=" TB", font=dict(size=32, color=COLORS["primary"])),
            title=dict(text="<b>Storage Capacity</b><br><span style='font-size:12px'>End of Projection</span>", font=dict(size=14)),
            delta=dict(
                reference=summary["baseline_storage"],
                relative=True,
                valueformat=".0%",
                increasing=dict(color=COLORS["accent"]),
            ),
        ),
        row=1,
        col=2,
    )

    # Power Requirement
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=summary["projected_power"],
            number=dict(suffix=" MW", font=dict(size=32, color=COLORS["primary"])),
            title=dict(text="<b>Power Requirement</b><br><span style='font-size:12px'>End of Projection</span>", font=dict(size=14)),
            delta=dict(
                reference=summary["baseline_power"],
                relative=True,
                valueformat=".0%",
                increasing=dict(color=COLORS["warning"]),
            ),
        ),
        row=2,
        col=1,
    )

    # Cooling Load
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=summary["projected_cooling"],
            number=dict(suffix=" tons", font=dict(size=32, color=COLORS["primary"])),
            title=dict(text="<b>Cooling Load</b><br><span style='font-size:12px'>End of Projection</span>", font=dict(size=14)),
            delta=dict(
                reference=summary["baseline_cooling"],
                relative=True,
                valueformat=".0%",
                increasing=dict(color=COLORS["warning"]),
            ),
        ),
        row=2,
        col=2,
    )

    fig.update_layout(
        height=400,
        paper_bgcolor="white",
        margin=dict(l=30, r=30, t=30, b=30),
    )

    return fig


def create_scenario_comparison_bar(scenarios: dict) -> go.Figure:
    """Create a grouped bar chart comparing scenarios at end of projection."""
    metrics = ["Compute_Cores", "Storage_TB", "Power_MW"]
    metric_names = ["Compute (cores)", "Storage (TB)", "Power (MW)"]

    # Get final year values for each scenario
    data = []
    for scenario_name in ["Conservative", "Base Case", "Aggressive", "Technology Disruption"]:
        if scenario_name in scenarios:
            final = scenarios[scenario_name].iloc[-1]
            data.append(
                {
                    "Scenario": scenario_name,
                    "Compute (cores)": final["Compute_Cores"],
                    "Storage (TB)": final["Storage_TB"],
                    "Power (MW)": final["Power_MW"] * 100,  # Scale for visibility
                }
            )

    df = pd.DataFrame(data)

    fig = go.Figure()

    bar_colors = [SCENARIO_COLORS[s] for s in df["Scenario"]]

    for i, metric in enumerate(["Compute (cores)", "Storage (TB)", "Power (MW)"]):
        fig.add_trace(
            go.Bar(
                name=metric.replace(" (MW)", " (MW×100)") if "MW" in metric else metric,
                x=df["Scenario"],
                y=df[metric],
                marker_color=[SCENARIO_COLORS[s] for s in df["Scenario"]],
                opacity=1 - (i * 0.25),
                text=[f"{v:,.0f}" for v in df[metric]],
                textposition="outside",
                textfont=dict(size=10),
            )
        )

    fig.update_layout(
        title=dict(
            text="<b>End-State Scenario Comparison</b>",
            font=dict(size=18, color=COLORS["primary"]),
            x=0.5,
        ),
        barmode="group",
        xaxis=dict(title="Scenario", tickfont=dict(size=11)),
        yaxis=dict(
            title="Capacity Units", showgrid=True, gridcolor="rgba(0,0,0,0.1)", tickformat=",.0f"
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=450,
        margin=dict(l=60, r=40, t=100, b=60),
    )

    return fig


def create_decision_timeline(decision_points: list, horizon_years: int) -> go.Figure:
    """Create a Gantt-style timeline for decision points."""
    from datetime import datetime

    current_year = datetime.now().year

    if not decision_points:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No critical decision points identified within the projection horizon",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=14, color=COLORS["neutral"]),
        )
        fig.update_layout(height=200, paper_bgcolor="white", plot_bgcolor="white")
        return fig

    # Sort by urgency for display
    urgency_colors = {
        "CRITICAL": COLORS["warning"],
        "HIGH": "#F39C12",
        "MEDIUM": COLORS["accent"],
        "LOW": COLORS["neutral"],
    }

    fig = go.Figure()

    for i, dp in enumerate(decision_points):
        warning_year = dp.get("warning_year", current_year + 1)
        critical_year = dp.get("critical_year", warning_year + 1)
        color = urgency_colors.get(dp["urgency"], COLORS["neutral"])

        # Planning phase bar
        fig.add_trace(
            go.Bar(
                name=f"{dp['capacity_type']}",
                y=[dp["capacity_type"]],
                x=[warning_year - current_year],
                base=[0],
                orientation="h",
                marker=dict(color=color, opacity=0.4),
                text=[f"Plan: {dp['decision_deadline']}"],
                textposition="inside",
                hovertemplate=f"<b>{dp['capacity_type']}</b><br>"
                + f"Urgency: {dp['urgency']}<br>"
                + f"Decision By: {dp['decision_deadline']}<br>"
                + f"Warning Year: {warning_year}<br>"
                + f"Lead Time: {dp['lead_time_months']} months<extra></extra>",
                showlegend=False,
            )
        )

        # Critical phase bar
        if critical_year:
            fig.add_trace(
                go.Bar(
                    y=[dp["capacity_type"]],
                    x=[critical_year - warning_year if critical_year else 0.5],
                    base=[warning_year - current_year],
                    orientation="h",
                    marker=dict(color=color, opacity=0.8),
                    text=["Critical"],
                    textposition="inside",
                    showlegend=False,
                    hovertemplate=f"<b>{dp['capacity_type']} - Critical Phase</b><br>"
                    + f"Utilization hits 85%: {critical_year}<extra></extra>",
                )
            )

    fig.update_layout(
        title=dict(
            text="<b>Capacity Decision Timeline</b>",
            font=dict(size=18, color=COLORS["primary"]),
            x=0.5,
        ),
        xaxis=dict(
            title="Years from Now",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, horizon_years + 1],
            tickvals=list(range(horizon_years + 2)),
        ),
        yaxis=dict(title="", showgrid=False, autorange="reversed"),
        barmode="stack",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=max(200, len(decision_points) * 60 + 100),
        margin=dict(l=120, r=40, t=80, b=60),
    )

    return fig


def create_growth_waterfall(summary: dict) -> go.Figure:
    """Create a waterfall chart showing capacity growth drivers."""
    baseline = summary["baseline_compute"]
    projected = summary["projected_compute"]
    growth = projected - baseline

    # Estimate growth components (simplified breakdown)
    organic_growth = growth * 0.4
    ai_growth = growth * 0.35
    efficiency_offset = -growth * 0.1
    compliance_overhead = growth * 0.15
    other = growth - organic_growth - ai_growth - efficiency_offset - compliance_overhead

    fig = go.Figure(
        go.Waterfall(
            name="Capacity",
            orientation="v",
            measure=["absolute", "relative", "relative", "relative", "relative", "total"],
            x=[
                "Current<br>Baseline",
                "Organic<br>Growth",
                "AI/ML<br>Workloads",
                "Efficiency<br>Gains",
                "Compliance<br>Overhead",
                "Projected<br>Total",
            ],
            y=[baseline, organic_growth, ai_growth, efficiency_offset, compliance_overhead, 0],
            text=[
                f"{baseline:,.0f}",
                f"+{organic_growth:,.0f}",
                f"+{ai_growth:,.0f}",
                f"{efficiency_offset:,.0f}",
                f"+{compliance_overhead:,.0f}",
                f"{projected:,.0f}",
            ],
            textposition="outside",
            connector=dict(line=dict(color="rgba(0,0,0,0.3)")),
            increasing=dict(marker=dict(color=COLORS["accent"])),
            decreasing=dict(marker=dict(color=COLORS["success"])),
            totals=dict(marker=dict(color=COLORS["primary"])),
        )
    )

    fig.update_layout(
        title=dict(
            text="<b>Compute Capacity Growth Drivers</b>",
            font=dict(size=18, color=COLORS["primary"]),
            x=0.5,
        ),
        yaxis=dict(
            title="Compute Cores", showgrid=True, gridcolor="rgba(0,0,0,0.1)", tickformat=",.0f"
        ),
        xaxis=dict(title="", tickfont=dict(size=11)),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=400,
        margin=dict(l=80, r=40, t=80, b=80),
        showlegend=False,
    )

    return fig


def create_risk_heatmap(scenarios: dict) -> go.Figure:
    """Create a risk heatmap across scenarios and metrics."""
    metrics = ["Compute_Cores", "Storage_TB", "Power_MW", "Network_Gbps"]
    metric_labels = ["Compute", "Storage", "Power", "Network"]
    scenario_names = ["Conservative", "Base Case", "Aggressive", "Technology Disruption"]

    # Calculate growth rates for each scenario/metric combination
    z_values = []
    for metric in metrics:
        row = []
        for scenario in scenario_names:
            if scenario in scenarios:
                df = scenarios[scenario]
                start = df.iloc[0][metric]
                end = df.iloc[-1][metric]
                growth_rate = ((end / start) - 1) * 100 if start > 0 else 0
                row.append(growth_rate)
            else:
                row.append(0)
        z_values.append(row)

    fig = go.Figure(
        data=go.Heatmap(
            z=z_values,
            x=scenario_names,
            y=metric_labels,
            colorscale=[
                [0, COLORS["success"]],
                [0.5, COLORS["accent"]],
                [1, COLORS["warning"]],
            ],
            text=[[f"{v:.0f}%" for v in row] for row in z_values],
            texttemplate="%{text}",
            textfont=dict(size=14, color="white"),
            hovertemplate="<b>%{y}</b><br>Scenario: %{x}<br>Growth: %{z:.1f}%<extra></extra>",
            colorbar=dict(title="Growth %", ticksuffix="%"),
        )
    )

    fig.update_layout(
        title=dict(
            text="<b>Growth Rate by Scenario & Metric</b>",
            font=dict(size=18, color=COLORS["primary"]),
            x=0.5,
        ),
        xaxis=dict(title="Scenario", tickfont=dict(size=11)),
        yaxis=dict(title="Metric", tickfont=dict(size=11)),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=350,
        margin=dict(l=80, r=100, t=80, b=60),
    )

    return fig
