import streamlit as st


def render_home():
    st.title("🚀 Orion Platform")
    st.markdown("### Choose where you want to go")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div style="padding:30px;border-radius:15px;background-color:#1f77b4;color:white;text-align:center">
            <h2>📊 Dashboard</h2>
            <p>View KPIs, Revenue, Expense & Analytics</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("Open Dashboard"):
            st.session_state.page = "dashboard"

    with col2:
        st.markdown(
            """
        <div style="padding:30px;border-radius:15px;background-color:#ff7f0e;color:white;text-align:center">
            <h2>🛠️ Data Management</h2>
            <p>Create, Update & Manage Data</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("Open Data Management"):
            st.session_state.page = "data"
