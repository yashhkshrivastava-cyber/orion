import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from ui.styles import back_button, page_header, render_metric_card, section_title
from ui.theme import CHART_COLORS, CHART_LAYOUT


def _apply_chart_theme(fig):
    fig.update_layout(**CHART_LAYOUT)
    return fig


def _chart_block(title, fig):
    with st.container(border=True):
        section_title(title)
        st.plotly_chart(_apply_chart_theme(fig), use_container_width=True)


def render_dashboard():
    if back_button():
        st.session_state.page = "home"
        st.rerun()

    page_header("Command Center", "Real-time overview of your business metrics", theme_key="dashboard")

    section_title("Key Metrics")

    metrics = [
        ("Revenue", "₹12.4L", "+12%", "positive"),
        ("Expense", "₹8.1L", "-4%", "negative"),
        ("Headcount", "124", "+3", "positive"),
        ("Active Cases", "32", "", "neutral"),
        ("KM Today", "328", "", "neutral"),
        ("Open Opportunities", "18", "", "neutral"),
    ]

    metric_cols = st.columns(6)
    for col, (label, value, delta, delta_type) in zip(metric_cols, metrics):
        with col:
            render_metric_card(label, value, delta, delta_type)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    rng = np.random.default_rng(42)

    revenue = pd.DataFrame(
        {
            "Month": months,
            "Prospective": rng.integers(4000, 1200000, 6),
            "Committed": rng.integers(80000, 2000000, 6),
        }
    )

    expense = pd.DataFrame(
        {
            "Month": months,
            "Prospective": rng.integers(200000, 800000, 6),
            "Committed": rng.integers(60000, 140000, 6),
        }
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            revenue,
            x="Month",
            y=["Prospective", "Committed"],
            barmode="stack",
            color_discrete_sequence=[CHART_COLORS[0], CHART_COLORS[2]],
        )
        fig.update_layout(title=None, showlegend=True)
        _chart_block("Revenue Breakdown", fig)

    with col2:
        fig = px.bar(
            expense,
            x="Month",
            y=["Prospective", "Committed"],
            barmode="stack",
            color_discrete_sequence=[CHART_COLORS[4], CHART_COLORS[1]],
        )
        fig.update_layout(title=None, showlegend=True)
        _chart_block("Expense Breakdown", fig)

    col1, col2 = st.columns(2)

    with col1:
        headcount = pd.DataFrame({"Type": ["Active", "Inactive"], "Count": [96, 28]})
        fig = px.pie(
            headcount,
            names="Type",
            values="Count",
            hole=0.65,
            color_discrete_sequence=[CHART_COLORS[3], CHART_COLORS[5]],
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(title=None)
        _chart_block("Headcount Distribution", fig)

    with col2:
        opp = pd.DataFrame(
            {
                "Stage": ["Proposal", "Financial Bid", "Technical Bid"],
                "Count": [8, 5, 5],
            }
        )
        fig = px.funnel(
            opp,
            x="Count",
            y="Stage",
            color="Stage",
            color_discrete_sequence=CHART_COLORS[:3],
        )
        fig.update_layout(title=None, showlegend=False)
        _chart_block("Opportunity Pipeline", fig)

    case_rev = pd.DataFrame(
        {
            "Case": ["Case A", "Case B", "Case C", "Case D", "Case E"],
            "Revenue": rng.integers(100, 500, 5),
        }
    )

    fig = px.bar(
        case_rev,
        x="Case",
        y="Revenue",
        color="Revenue",
        color_continuous_scale=[[0, CHART_COLORS[0]], [1, CHART_COLORS[2]]],
    )
    fig.update_layout(title=None, coloraxis_showscale=False)
    _chart_block("Case-wise Revenue (YTD)", fig)

    section_title("Performance Snapshot")

    snap_cols = st.columns(3)
    snapshot = [
        ("Top Performing Case", "Case B"),
        ("Highest Revenue Month", "March"),
        ("Efficiency Score", "87%"),
    ]
    for col, (label, value) in zip(snap_cols, snapshot):
        with col:
            render_metric_card(label, value)
