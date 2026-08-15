import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


def render_dashboard():
    if st.button("⬅️ Back"):
        st.session_state.page = "home"

    st.title("📊 Orion Command Center")

    st.markdown("### 📌 Key Metrics")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric("💰 Revenue", "₹12.4L", "+12%")
    col2.metric("💸 Expense", "₹8.1L", "-4%")
    col3.metric("👥 Headcount", "124", "+3")
    col4.metric("📂 Active Cases", "32")
    col5.metric("🚗 KM Today", "328")
    col6.metric("📈 Open Opp", "18")

    st.divider()

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

    revenue = pd.DataFrame(
        {
            "Month": months,
            "Prospective": np.random.randint(4000, 1200000, 6),
            "Committed": np.random.randint(80000, 2000000, 6),
        }
    )

    expense = pd.DataFrame(
        {
            "Month": months,
            "Prospective": np.random.randint(200000, 800000, 6),
            "Committed": np.random.randint(60000, 140000, 6),
        }
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Revenue Breakdown")

        fig = px.bar(
            revenue,
            x="Month",
            y=["Prospective", "Committed"],
            barmode="stack",
            title="Monthly Revenue",
            color_discrete_sequence=["#636EFA", "#00CC96"],
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 💸 Expense Breakdown")

        fig = px.bar(
            expense,
            x="Month",
            y=["Prospective", "Committed"],
            barmode="stack",
            title="Monthly Expense",
            color_discrete_sequence=["#EF553B", "#AB63FA"],
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👥 Headcount Distribution")

        headcount = pd.DataFrame({"Type": ["Active", "Inactive"], "Count": [96, 28]})

        fig = px.pie(headcount, names="Type", values="Count", hole=0.6)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 📊 Opportunity Pipeline")

        opp = pd.DataFrame(
            {
                "Stage": ["Proposal", "Financial Bid", "Technical Bid"],
                "Count": [8, 5, 5],
            }
        )

        fig = px.funnel(opp, x="Count", y="Stage", color="Stage")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("### 💼 Case-wise Revenue (YTD)")

    case_rev = pd.DataFrame(
        {
            "Case": ["Case A", "Case B", "Case C", "Case D", "Case E"],
            "Revenue": np.random.randint(100, 500, 5),
        }
    )

    fig = px.bar(
        case_rev,
        x="Case",
        y="Revenue",
        color="Revenue",
        color_continuous_scale="blues",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("### 🔥 Performance Snapshot")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Top Performing Case", "Case B")

    with col2:
        st.metric("Highest Revenue Month", "March")

    with col3:
        st.metric("Efficiency Score", "87%")
