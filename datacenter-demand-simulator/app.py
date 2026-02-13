"""
Datacenter Demand Simulator - Executive Dashboard
A strategic planning tool for datacenter capacity forecasting.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from simulator import DatacenterSimulator
from ollama_client import OllamaClient
from visualizations import (
    create_capacity_timeline,
    create_summary_dashboard,
    create_scenario_comparison_bar,
    create_decision_timeline,
    create_growth_waterfall,
    create_risk_heatmap,
)
from config import (
    INDUSTRY_BASELINES,
    WORKLOAD_MULTIPLIERS,
    COMPLIANCE_REQUIREMENTS,
    SCENARIOS,
)

# Page configuration
st.set_page_config(
    page_title="Datacenter Demand Simulator",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for executive styling
st.markdown(
    """
<style>
    /* Main styling */
    .main > div {
        padding: 2rem 3rem;
    }

    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1E3A5F 0%, #3D5A80 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }

    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 600;
    }

    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #4ECDC4;
    }

    .metric-card h3 {
        margin: 0;
        color: #1E3A5F;
        font-size: 1rem;
        font-weight: 500;
    }

    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: #1E3A5F;
        margin: 0.5rem 0;
    }

    .metric-card .delta {
        font-size: 0.9rem;
        color: #4ECDC4;
    }

    /* Section headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1E3A5F;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #4ECDC4;
    }

    /* Decision point cards */
    .decision-card {
        background: white;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }

    .decision-card.critical {
        border-left: 4px solid #FF6B6B;
    }

    .decision-card.high {
        border-left: 4px solid #F39C12;
    }

    .decision-card.medium {
        border-left: 4px solid #4ECDC4;
    }

    .decision-card.low {
        border-left: 4px solid #95A5A6;
    }

    /* AI Analysis box */
    .ai-analysis {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }

    .ai-analysis h4 {
        color: #1E3A5F;
        margin-top: 0;
    }

    /* Sidebar styling */
    .css-1d391kg {
        padding: 2rem 1rem;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        font-weight: 500;
        color: #1E3A5F;
    }
</style>
""",
    unsafe_allow_html=True,
)


def render_header():
    """Render the main header."""
    st.markdown(
        """
    <div class="main-header">
        <h1>Datacenter Demand Simulator</h1>
        <p>Strategic Capacity Planning for Enterprise Infrastructure</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    """Render the input sidebar and return parameters."""
    with st.sidebar:
        st.markdown("### 📊 Business Parameters")

        # Industry selection
        industry = st.selectbox(
            "Industry Sector",
            options=list(INDUSTRY_BASELINES.keys()),
            index=2,  # Default to Technology
            help="Select your industry for baseline capacity assumptions",
        )

        st.markdown("---")

        # Company size
        employees = st.number_input(
            "Employee Count",
            min_value=100,
            max_value=500000,
            value=5000,
            step=100,
            help="Total number of employees in the organization",
        )

        # Growth rate
        growth_rate = st.slider(
            "Annual Growth Rate (%)",
            min_value=0,
            max_value=50,
            value=15,
            help="Expected year-over-year growth rate",
        )

        st.markdown("---")
        st.markdown("### 🖥️ Workload Profile")

        # Workload types
        workloads = st.multiselect(
            "Primary Workload Types",
            options=list(WORKLOAD_MULTIPLIERS.keys()),
            default=["General Compute", "Database Operations", "AI/ML Inference"],
            help="Select all applicable workload types",
        )

        # AI intensity
        ai_intensity = st.slider(
            "AI/ML Intensity",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1,
            help="How central is AI/ML to your operations? (0=None, 1=Core)",
        )

        st.markdown("---")
        st.markdown("### 🔒 Compliance Requirements")

        # Compliance
        compliance = st.multiselect(
            "Compliance Frameworks",
            options=list(COMPLIANCE_REQUIREMENTS.keys()),
            default=["SOC 2 Type II"],
            help="Select all applicable compliance requirements",
        )

        st.markdown("---")
        st.markdown("### 📅 Projection Settings")

        # Projection horizon
        horizon = st.slider(
            "Projection Horizon (Years)",
            min_value=3,
            max_value=10,
            value=5,
            help="Number of years to project forward",
        )

        st.markdown("---")
        st.markdown("### 🤖 AI Analysis")

        # Ollama settings
        ollama_enabled = st.checkbox(
            "Enable AI-Powered Analysis",
            value=True,
            help="Use local Ollama for strategic recommendations",
        )

        ollama_model = "qwen2.5:14b"
        if ollama_enabled:
            ollama_model = st.text_input(
                "Ollama Model",
                value="qwen2.5:14b",
                help="Model name for Ollama (e.g., qwen2.5:14b, llama3.2, mistral)",
            )

        return {
            "industry": industry,
            "employees": employees,
            "growth_rate": growth_rate / 100,
            "workloads": workloads,
            "compliance": compliance,
            "horizon": horizon,
            "ai_intensity": ai_intensity,
            "ollama_enabled": ollama_enabled,
            "ollama_model": ollama_model,
        }


def render_metrics_row(summary: dict):
    """Render the top metrics row."""
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        growth = (summary["compute_growth"] - 1) * 100
        st.metric(
            "Compute Cores",
            f"{summary['projected_compute']:,.0f}",
            f"+{growth:.0f}% growth",
        )

    with col2:
        growth = (summary["storage_growth"] - 1) * 100
        st.metric(
            "Storage (TB)",
            f"{summary['projected_storage']:,.0f}",
            f"+{growth:.0f}% growth",
        )

    with col3:
        growth = (summary["power_growth"] - 1) * 100
        st.metric(
            "Power (MW)",
            f"{summary['projected_power']:,.2f}",
            f"+{growth:.0f}% growth",
        )

    with col4:
        st.metric(
            "Cooling (Tons)",
            f"{summary['projected_cooling']:,.0f}",
            f"+{growth:.0f}% growth",
        )

    with col5:
        st.metric(
            "Network (Gbps)",
            f"{summary['projected_network']:,.1f}",
            f"Year {summary['horizon_years']}",
        )


def render_decision_points(decision_points: list, ollama_client: OllamaClient):
    """Render decision points section."""
    st.markdown('<div class="section-header">📋 Recommended Decision Points</div>', unsafe_allow_html=True)

    if not decision_points:
        st.info("No critical decision points identified within the projection horizon.")
        return

    for dp in decision_points[:5]:  # Show top 5
        urgency_class = dp["urgency"].lower()
        urgency_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(
            urgency_class, "⚪"
        )

        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(
                    f"""
                **{urgency_emoji} {dp['capacity_type']}** — {dp['urgency']} Priority

                Decision Deadline: **{dp['decision_deadline']}**
                """,
                )

            with col2:
                st.metric(
                    "Current Utilization",
                    f"{dp['current_utilization']:.0%}",
                    f"Warning: Year {dp['warning_year']}",
                )

            with col3:
                st.metric(
                    "Expansion Needed",
                    f"+{dp['expansion_percentage']:.0f}%",
                    f"Lead Time: {dp['lead_time_months']}mo",
                )

            st.markdown("---")


def render_ai_analysis(summary: dict, scenario_comparison: dict, ollama_client: OllamaClient):
    """Render AI-powered analysis section."""
    st.markdown('<div class="section-header">🤖 AI Strategic Analysis</div>', unsafe_allow_html=True)

    if not ollama_client.is_available():
        st.warning(
            """
            **Ollama is not available.** To enable AI-powered analysis:
            1. Install Ollama from https://ollama.ai
            2. Run `ollama serve` in your terminal
            3. Pull a model: `ollama pull llama3.2`
            """
        )
        return

    with st.spinner("Generating strategic analysis..."):
        # Get capacity plan analysis
        analysis = ollama_client.analyze_capacity_plan(summary)

        if analysis and "unavailable" not in analysis.lower():
            st.markdown(
                f"""
            <div class="ai-analysis">
                <h4>📊 Strategic Capacity Assessment</h4>
                {analysis}
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Get scenario insights
            insights = ollama_client.generate_scenario_insights(scenario_comparison)
            if insights and "unavailable" not in insights.lower():
                st.markdown(
                    f"""
                <div class="ai-analysis">
                    <h4>🎯 Scenario Planning Insights</h4>
                    {insights}
                </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("AI analysis not available. Ensure Ollama is running with a compatible model.")


def render_data_tables(scenarios: dict):
    """Render detailed data tables."""
    st.markdown('<div class="section-header">📑 Detailed Projections</div>', unsafe_allow_html=True)

    scenario_tabs = st.tabs(list(scenarios.keys()))

    for tab, (scenario_name, df) in zip(scenario_tabs, scenarios.items()):
        with tab:
            # Format the dataframe for display
            display_df = df.copy()
            display_df["Compute_Cores"] = display_df["Compute_Cores"].apply(lambda x: f"{x:,.0f}")
            display_df["Storage_TB"] = display_df["Storage_TB"].apply(lambda x: f"{x:,.1f}")
            display_df["Power_MW"] = display_df["Power_MW"].apply(lambda x: f"{x:,.3f}")
            display_df["Cooling_Tons"] = display_df["Cooling_Tons"].apply(lambda x: f"{x:,.0f}")
            display_df["Network_Gbps"] = display_df["Network_Gbps"].apply(lambda x: f"{x:,.1f}")
            display_df["Employees"] = display_df["Employees"].apply(lambda x: f"{x:,}")

            display_df.columns = [
                "Year",
                "Employees",
                "Compute (Cores)",
                "Storage (TB)",
                "Power (MW)",
                "Cooling (Tons)",
                "Network (Gbps)",
            ]

            st.dataframe(display_df, use_container_width=True, hide_index=True)

            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label=f"📥 Download {scenario_name} Data",
                data=csv,
                file_name=f"datacenter_projection_{scenario_name.lower().replace(' ', '_')}.csv",
                mime="text/csv",
            )


def main():
    """Main application entry point."""
    render_header()

    # Get sidebar inputs
    params = render_sidebar()

    # Initialize simulator
    simulator = DatacenterSimulator(
        industry=params["industry"],
        employees=params["employees"],
        growth_rate=params["growth_rate"],
        workloads=params["workloads"],
        compliance=params["compliance"],
        horizon_years=params["horizon"],
        ai_intensity=params["ai_intensity"],
    )

    # Initialize Ollama client
    ollama_client = OllamaClient(model=params["ollama_model"])

    # Run simulations
    scenarios = simulator.run_all_scenarios()
    summary = simulator.get_summary_stats()
    scenario_comparison = simulator.get_scenario_comparison()
    decision_points = simulator.calculate_decision_points()

    # Configuration summary
    st.markdown("### Configuration Summary")
    config_col1, config_col2, config_col3 = st.columns(3)

    with config_col1:
        st.markdown(f"**Industry:** {params['industry']}")
        st.markdown(f"**Employees:** {params['employees']:,}")

    with config_col2:
        st.markdown(f"**Growth Rate:** {params['growth_rate']:.0%} annually")
        st.markdown(f"**AI Intensity:** {params['ai_intensity']:.0%}")

    with config_col3:
        st.markdown(f"**Projection:** {params['horizon']} years")
        st.markdown(f"**Workloads:** {len(params['workloads'])} types")

    st.markdown("---")

    # Metrics row
    render_metrics_row(summary)

    st.markdown("---")

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Capacity Projections", "⚠️ Risk Scenarios", "📋 Decision Timeline", "🤖 AI Analysis"]
    )

    with tab1:
        # Summary dashboard
        st.plotly_chart(create_summary_dashboard(summary), use_container_width=True)

        # Timeline charts
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(
                create_capacity_timeline(scenarios, "compute", "Compute Capacity", "Cores"),
                use_container_width=True,
            )

        with col2:
            st.plotly_chart(
                create_capacity_timeline(scenarios, "storage", "Storage Capacity", "TB"),
                use_container_width=True,
            )

        col3, col4 = st.columns(2)

        with col3:
            st.plotly_chart(
                create_capacity_timeline(scenarios, "power", "Power Requirement", "MW"),
                use_container_width=True,
            )

        with col4:
            st.plotly_chart(
                create_capacity_timeline(scenarios, "network", "Network Bandwidth", "Gbps"),
                use_container_width=True,
            )

        # Growth waterfall
        st.plotly_chart(create_growth_waterfall(summary), use_container_width=True)

    with tab2:
        st.markdown("### Scenario Analysis")
        st.markdown(
            """
        Compare outcomes across different growth scenarios to understand the range of
        potential capacity requirements and plan for uncertainty.
        """
        )

        # Scenario comparison bar chart
        st.plotly_chart(create_scenario_comparison_bar(scenarios), use_container_width=True)

        # Risk heatmap
        st.plotly_chart(create_risk_heatmap(scenarios), use_container_width=True)

        # Scenario descriptions
        st.markdown("### Scenario Definitions")
        for scenario_name, scenario_params in SCENARIOS.items():
            with st.expander(f"**{scenario_name}**"):
                st.markdown(f"_{scenario_params['description']}_")
                st.markdown(
                    f"""
                - Growth Modifier: {scenario_params['growth_modifier']:.1f}x
                - AI Adoption Modifier: {scenario_params['ai_adoption_modifier']:.1f}x
                - Efficiency Modifier: {scenario_params['efficiency_modifier']:.1f}x
                """
                )

    with tab3:
        # Decision timeline visualization
        st.plotly_chart(
            create_decision_timeline(decision_points, params["horizon"]),
            use_container_width=True,
        )

        # Decision points details
        render_decision_points(decision_points, ollama_client)

    with tab4:
        if params["ollama_enabled"]:
            render_ai_analysis(summary, scenario_comparison, ollama_client)
        else:
            st.info("Enable AI-Powered Analysis in the sidebar to see strategic recommendations.")

    # Detailed data tables
    with st.expander("📊 View Detailed Data Tables"):
        render_data_tables(scenarios)

    # Footer
    st.markdown("---")
    st.markdown(
        f"""
    <div style="text-align: center; color: #95A5A6; font-size: 0.9rem;">
        Datacenter Demand Simulator | Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} |
        Industry assumptions based on market research benchmarks
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
