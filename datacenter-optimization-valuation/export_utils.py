"""
Export utilities for generating PE/VC presentation-ready reports
"""

import pandas as pd
import io
from datetime import datetime
from typing import Dict, Optional


def generate_executive_summary(
    deployment_results: Optional[Dict] = None,
    valuation_results: Optional[Dict] = None,
    requirements: Optional[Dict] = None
) -> str:
    """Generate executive summary text for reports"""

    summary_parts = []
    summary_parts.append("=" * 60)
    summary_parts.append("DATACENTER INVESTMENT ANALYSIS - EXECUTIVE SUMMARY")
    summary_parts.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    summary_parts.append("=" * 60)
    summary_parts.append("")

    if requirements:
        summary_parts.append("PROJECT PARAMETERS")
        summary_parts.append("-" * 40)
        summary_parts.append(f"Capacity: {requirements.get('total_power_mw', 'N/A')} MW")
        summary_parts.append(f"Region: {requirements.get('region', 'N/A')}")
        summary_parts.append(f"Timeline: {requirements.get('timeline_urgency', 'N/A')}")
        summary_parts.append(f"Budget: ${requirements.get('budget_constraint', 0)}M")
        summary_parts.append("")

    if deployment_results:
        summary_parts.append("DEPLOYMENT ANALYSIS")
        summary_parts.append("-" * 40)

        for approach, data in deployment_results.items():
            summary_parts.append(f"\n{data['name']}:")
            summary_parts.append(f"  CapEx: ${data['capex']/1e6:.1f}M")
            summary_parts.append(f"  Timeline: {data['timeline_months']} months")
            summary_parts.append(f"  10yr ROI: {data['roi_percent']:.1f}%")
            summary_parts.append(f"  Risk Score: {data['risk_score']}/100")

        summary_parts.append("")

    if valuation_results:
        summary_parts.append("VALUATION ANALYSIS")
        summary_parts.append("-" * 40)
        summary_parts.append(f"Asking Price: ${valuation_results['asking_price']/1e6:.1f}M")
        summary_parts.append(f"Fair Value: ${valuation_results['adjusted_value']/1e6:.1f}M")
        summary_parts.append(f"Gap: {valuation_results['valuation_gap_percent']:+.1f}%")
        summary_parts.append(f"Recommendation: {valuation_results['recommendation']}")
        summary_parts.append("")

    summary_parts.append("=" * 60)

    return "\n".join(summary_parts)


def export_to_excel(
    deployment_results: Optional[Dict] = None,
    valuation_results: Optional[Dict] = None,
    benchmarks: Optional[Dict] = None
) -> bytes:
    """Export analysis to Excel workbook"""

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Deployment comparison sheet
        if deployment_results:
            deployment_data = []
            for approach, data in deployment_results.items():
                deployment_data.append({
                    'Approach': data['name'],
                    'CapEx ($M)': data['capex'] / 1e6,
                    'CapEx/MW ($M)': data['capex_per_mw'] / 1e6,
                    'Annual OpEx ($M)': data['annual_opex'] / 1e6,
                    '10yr OpEx ($M)': data['ten_year_opex'] / 1e6,
                    'Total 10yr Cost ($M)': data['total_10yr_cost'] / 1e6,
                    'Timeline (months)': data['timeline_months'],
                    'PUE': data['pue'],
                    'Flexibility Score': data['flexibility_score'],
                    'Risk Score': data['risk_score'],
                    '10yr ROI (%)': data['roi_percent'],
                    'Resale Value ($M)': data['resale_value'] / 1e6,
                    'Meets Budget': data['meets_budget'],
                    'Meets Timeline': data['meets_timeline']
                })

            df_deployment = pd.DataFrame(deployment_data)
            df_deployment.to_excel(writer, sheet_name='Deployment Analysis', index=False)

        # Valuation sheet
        if valuation_results:
            valuation_summary = pd.DataFrame([{
                'Metric': 'Asking Price',
                'Value ($M)': valuation_results['asking_price'] / 1e6
            }, {
                'Metric': 'Base Value',
                'Value ($M)': valuation_results['base_value'] / 1e6
            }, {
                'Metric': 'Adjusted Fair Value',
                'Value ($M)': valuation_results['adjusted_value'] / 1e6
            }, {
                'Metric': 'Valuation Gap ($M)',
                'Value ($M)': valuation_results['valuation_gap'] / 1e6
            }, {
                'Metric': 'Gap (%)',
                'Value ($M)': valuation_results['valuation_gap_percent']
            }])

            valuation_summary.to_excel(writer, sheet_name='Valuation Summary', index=False)

            # Adjustments detail
            adj_data = [{
                'Factor': adj['factor'],
                'Impact ($M)': adj['impact'] / 1e6,
                'Description': adj['description'],
                'Assessment': adj['flag']
            } for adj in valuation_results['adjustments']]

            df_adj = pd.DataFrame(adj_data)
            df_adj.to_excel(writer, sheet_name='Valuation Adjustments', index=False)

        # Benchmarks sheet
        if benchmarks:
            benchmark_data = []
            for region, data in benchmarks.items():
                benchmark_data.append({
                    'Region': region,
                    'Tier': data['tier'],
                    'CapEx/MW ($M)': data['capex_per_mw'] / 1e6,
                    'Transaction Comp/MW ($M)': data['transaction_comp_per_mw'] / 1e6,
                    'Power Cost ($/kWh)': data['power_cost_kwh'],
                    'Avg PUE': data['avg_pue'],
                    'Market Utilization': data['market_utilization'],
                    'Demand Growth': data['demand_growth'],
                    'Land Cost ($/acre)': data['land_cost_per_acre']
                })

            df_benchmarks = pd.DataFrame(benchmark_data)
            df_benchmarks.to_excel(writer, sheet_name='Market Benchmarks', index=False)

    output.seek(0)
    return output.getvalue()


def generate_deal_memo(
    valuation_results: Dict,
    inputs: Dict,
    region: str,
    ai_analysis: str = ""
) -> str:
    """Generate investment committee deal memo"""

    memo = []
    memo.append("=" * 70)
    memo.append("INVESTMENT COMMITTEE DEAL MEMORANDUM")
    memo.append("CONFIDENTIAL")
    memo.append("=" * 70)
    memo.append("")
    memo.append(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    memo.append(f"Subject: Datacenter Acquisition - {region}")
    memo.append("")
    memo.append("-" * 70)
    memo.append("TRANSACTION SUMMARY")
    memo.append("-" * 70)
    memo.append(f"Asking Price:          ${inputs.get('asking_price', 0)/1e6:.1f}M")
    memo.append(f"Calculated Fair Value: ${valuation_results['adjusted_value']/1e6:.1f}M")
    memo.append(f"Valuation Gap:         {valuation_results['valuation_gap_percent']:+.1f}%")
    memo.append(f"Recommendation:        {valuation_results['recommendation']}")
    memo.append("")
    memo.append("-" * 70)
    memo.append("ASSET PROFILE")
    memo.append("-" * 70)
    memo.append(f"Capacity:              {inputs.get('claimed_capacity_mw', 0)} MW")
    memo.append(f"Utilization:           {inputs.get('actual_utilization', 0):.0%}")
    memo.append(f"PUE:                   {inputs.get('current_pue', 0)}")
    memo.append(f"Contract Quality:      {inputs.get('contract_quality', 'N/A')}")
    memo.append(f"Avg Contract Term:     {inputs.get('contract_term_years', 0)} years")
    memo.append(f"Building Age:          {inputs.get('building_age_years', 0)} years")
    memo.append(f"Expansion Capacity:    {inputs.get('expansion_capacity_mw', 0)} MW")
    memo.append("")
    memo.append("-" * 70)
    memo.append("VALUATION ADJUSTMENTS")
    memo.append("-" * 70)

    for adj in valuation_results['adjustments']:
        impact_str = f"${adj['impact']/1e6:+.1f}M"
        memo.append(f"{adj['factor']:25} {impact_str:>12}  ({adj['description']})")

    memo.append("")

    if valuation_results['flags']:
        memo.append("-" * 70)
        memo.append("KEY FINDINGS")
        memo.append("-" * 70)
        for flag in valuation_results['flags']:
            memo.append(f"[{flag['type'].upper()}] {flag['title']}")
            memo.append(f"    {flag['description']}")
        memo.append("")

    if ai_analysis:
        memo.append("-" * 70)
        memo.append("INVESTMENT ANALYSIS")
        memo.append("-" * 70)
        memo.append(ai_analysis)
        memo.append("")

    memo.append("=" * 70)
    memo.append("END OF MEMORANDUM")
    memo.append("=" * 70)

    return "\n".join(memo)


def calculate_sensitivity_matrix(
    base_capex: float,
    base_utilization: float,
    base_price_per_kw: float
) -> pd.DataFrame:
    """Generate sensitivity analysis matrix"""

    utilization_range = [0.60, 0.70, 0.80, 0.90, 1.00]
    price_range = [80, 100, 120, 140, 160]  # $/kW/month

    data = []
    for util in utilization_range:
        row = {'Utilization': f"{util:.0%}"}
        for price in price_range:
            annual_revenue = base_capex / 8.5 * util * price * 12 / 1000  # Simplified
            row[f"${price}/kW"] = f"${annual_revenue/1e6:.1f}M"
        data.append(row)

    return pd.DataFrame(data)
