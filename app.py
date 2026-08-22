import streamlit as st

st.set_page_config(page_title="Orion", layout="wide")

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"


# ---------------- HOME PAGE (CARDS) ----------------
if st.session_state.page == "home":

    st.title("🚀 Orion Platform")

    st.markdown("### Choose where you want to go")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="padding:30px;border-radius:15px;background-color:#1f77b4;color:white;text-align:center">
            <h2>📊 Dashboard</h2>
            <p>View KPIs, Revenue, Expense & Analytics</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Dashboard"):
            st.session_state.page = "dashboard"

    with col2:
        st.markdown("""
        <div style="padding:30px;border-radius:15px;background-color:#ff7f0e;color:white;text-align:center">
            <h2>🛠️ Data Management</h2>
            <p>Create, Update & Manage Data</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Data Management"):
            st.session_state.page = "data"


# ---------------- DASHBOARD ----------------
elif st.session_state.page == "dashboard":

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

    import streamlit as st
    import pandas as pd
    import numpy as np
    import plotly.express as px

    st.title("📊 Orion Command Center")

    # ---------------- KPI ROW ----------------
    st.markdown("### 📌 Key Metrics")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric("💰 Revenue", "₹12.4L", "+12%")
    col2.metric("💸 Expense", "₹8.1L", "-4%")
    col3.metric("👥 Headcount", "124", "+3")
    col4.metric("📂 Active Cases", "32")
    col5.metric("🚗 KM Today", "328")
    col6.metric("📈 Open Opp", "18")

    st.divider()

    # ---------------- DATA ----------------
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

    revenue = pd.DataFrame({
        "Month": months,
        "Prospective": np.random.randint(4000, 1200000, 6),
        "Committed": np.random.randint(80000, 2000000, 6)
    })

    expense = pd.DataFrame({
        "Month": months,
        "Prospective": np.random.randint(200000, 800000, 6),
        "Committed": np.random.randint(60000, 140000, 6)
    })

    # ---------------- CHART ROW 1 ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Revenue Breakdown")

        fig = px.bar(
            revenue,
            x="Month",
            y=["Prospective", "Committed"],
            barmode="stack",
            title="Monthly Revenue",
            color_discrete_sequence=["#636EFA", "#00CC96"]
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
            color_discrete_sequence=["#EF553B", "#AB63FA"]
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---------------- CHART ROW 2 ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👥 Headcount Distribution")

        headcount = pd.DataFrame({
            "Type": ["Active", "Inactive"],
            "Count": [96, 28]
        })

        fig = fig = px.pie(
            headcount,
            names="Type",
            values="Count",
            hole=0.6   # 🔥 this makes it donut
        )
        st.plotly_chart(fig, use_container_width=True)


    with col2:
        st.markdown("### 📊 Opportunity Pipeline")

        opp = pd.DataFrame({
            "Stage": ["Proposal", "Financial Bid", "Technical Bid"],
            "Count": [8, 5, 5]
        })

        fig = px.funnel(
            opp,
            x="Count",
            y="Stage",
            color="Stage"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---------------- CASE REVENUE ----------------
    st.markdown("### 💼 Case-wise Revenue (YTD)")

    case_rev = pd.DataFrame({
        "Case": ["Case A", "Case B", "Case C", "Case D", "Case E"],
        "Revenue": np.random.randint(100, 500, 5)
    })

    fig = px.bar(
        case_rev,
        x="Case",
        y="Revenue",
        color="Revenue",
        color_continuous_scale="blues"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---------------- EXTRA (🔥 WOW FACTOR) ----------------
    st.markdown("### 🔥 Performance Snapshot")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Top Performing Case", "Case B")

    with col2:
        st.metric("Highest Revenue Month", "March")

    with col3:
        st.metric("Efficiency Score", "87%")


# ---------------- DATA MANAGEMENT ----------------
elif st.session_state.page == "data":

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

    st.title("🛠️ Data Management")
    #my tested code#######-----
    import streamlit as st
    import importlib
    from modules.registry import MODULES
    from db.db_utils import *
    import pandas as pd
    from datetime import datetime
    from utils.location_data import STATE_CITY_MAP

    st.title("🚀 Orion Platform")

    # Dataset select
    dataset = st.selectbox("Select Dataset", list(MODULES.keys()))


    module_path = MODULES[dataset]
    meta = importlib.import_module(f"{module_path}.meta")

    st.subheader("📊 Latest Data Preview")

    cols, data = fetch_top_n(meta.TABLE, 10)

    if data:
        df = pd.DataFrame(data, columns=cols)
        st.dataframe(df)

        st.caption(f"Last refreshed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.warning("No data available")

    # Action
    action = st.radio("Select Action", ["Create", "Update", "Delete"])

    # ---------------- CREATE ----------------
    if action == "Create":
        st.subheader("Create Record")

        inputs = {}

        for col, config in meta.FORM_FIELDS.items():

            field_type = config["type"]

            if config["type"] == "auto_date":
                continue

            # TEXT
            if field_type == "text":
                inputs[col] = st.text_input(config["label"])

            elif field_type == "number":
                inputs[col] = st.number_input(config["label"])

            # DATE
            elif field_type == "date":

                use_date = st.checkbox(f"Set {config['label']}", key=f"{col}_check")

                if use_date:
                    inputs[col] = st.date_input(config["label"], key=col)
                else:
                    inputs[col] = None

            # BOOLEAN
            elif field_type == "boolean":
                inputs[col] = st.checkbox(config["label"])

            # STATIC SELECT
            elif field_type == "select" and "options" in config:
                selected = st.selectbox(config["label"], config["options"])
                inputs[col] = selected

            # FK SELECT
            elif field_type == "select" and "source_table" in config:
                data = fetch_dropdown(
                    config["source_table"],
                    config["source_display_column"]
                )

                options = {f"{r[1]} ({r[0]})": r[0] for r in data}

                selected = st.selectbox(config["label"], list(options.keys()))
                inputs[col] = options[selected]

            # DEPENDENT SELECT (STATE → CITY)
            elif field_type == "dependent_select":
                state = inputs.get("client_location_state")

                from utils.location_data import STATE_CITY_MAP

                cities = STATE_CITY_MAP.get(state, [])

                selected = st.selectbox(config["label"], cities)
                inputs[col] = selected

        if st.button("Create"):

            from datetime import date

            # 🔥 CLIENT logic
            if "client_onboarded" in inputs:
                if inputs.get("client_onboarded"):
                    inputs["client_onboarded_date"] = date.today()
                else:
                    inputs["client_onboarded_date"] = None

            # 🔥 CASE logic
            if "case_onboarded" in inputs:
                if inputs.get("case_onboarded"):
                    inputs["case_onboarded_date"] = date.today()
                else:
                    inputs["case_onboarded_date"] = None

            # ✅ SINGLE INSERT ONLY
            insert(meta.TABLE, list(inputs.keys()), list(inputs.values()))

            st.success("Record Created Successfully")


    # ---------------- UPDATE ----------------
    elif action == "Update":
        st.subheader("Update Record")

        data = fetch_dropdown(meta.TABLE, meta.DISPLAY_COLUMN)

        if not data:
            st.warning("No records available")
            st.stop()

        options = {f"{r[1]} ({r[0]})": r[0] for r in data}
        selected = st.selectbox("Select Record", list(options.keys()))
        selected_id = options[selected]

        record = fetch_by_id(meta.TABLE, selected_id)

        if record:
            st.subheader("📄 Selected Record Preview")

            df = pd.DataFrame([record])
            st.dataframe(df,use_container_width=True)

        # 🔥 Fetch record for pre-fill
        record = fetch_by_id(meta.TABLE, selected_id)

        inputs = {}

        for col, config in meta.FORM_FIELDS.items():

            field_type = config["type"]
            default_val = record.get(col) if record else None

            if config["type"] == "auto_date":
                continue

            # TEXT
            if field_type == "text":
                inputs[col] = st.text_input(
                    config["label"],
                    value=str(default_val) if default_val else ""
                )

            elif field_type == "number":
                inputs[col] = st.number_input(config["label"])

            # DATE
            elif field_type == "date":

                has_value = default_val is not None

                use_date = st.checkbox(
                    f"Set {config['label']}",
                    value=has_value,
                    key=f"{col}_check"
                )

                if use_date:
                    inputs[col] = st.date_input(
                        config["label"],
                        value=default_val,
                        key=col
                    )
                else:
                    inputs[col] = None

            # BOOLEAN
            elif field_type == "boolean":
                inputs[col] = st.checkbox(
                config["label"],
                value=True if default_val in [True, 1, 'true', 'True'] else False
                )

            # STATIC SELECT
            elif field_type == "select" and "options" in config:
                options_list = config["options"]

                selected = st.selectbox(
                    config["label"],
                    options_list,
                    index=options_list.index(default_val)
                    if default_val in options_list else 0
                )

                inputs[col] = selected

            # FK SELECT
            elif field_type == "select" and "source_table" in config:
                data = fetch_dropdown(
                    config["source_table"],
                    config["source_display_column"]
                )

                options = {f"{r[1]} ({r[0]})": r[0] for r in data}
                reverse = {v: k for k, v in options.items()}

                selected_display = reverse.get(default_val)

                selected = st.selectbox(
                    config["label"],
                    list(options.keys()),
                    index=list(options.keys()).index(selected_display)
                    if selected_display in options else 0
                )

                inputs[col] = options[selected]

            # DEPENDENT SELECT
            elif field_type == "dependent_select":
                from utils.location_data import STATE_CITY_MAP

                state = inputs.get("client_location_state")
                cities = STATE_CITY_MAP.get(state, [])

                selected = st.selectbox(
                    config["label"],
                    cities,
                    index=cities.index(default_val)
                    if default_val in cities else 0
                )

                inputs[col] = selected

        if st.button("Update"):

            from datetime import date

            # CLIENT
            if "client_onboarded" in inputs:
                if inputs.get("client_onboarded"):
                    if not record.get("client_onboarded_date"):
                        inputs["client_onboarded_date"] = date.today()
                else:
                    inputs["client_onboarded_date"] = None

            # CASE
            if "case_onboarded" in inputs:
                if inputs.get("case_onboarded"):
                    if not record.get("case_onboarded_date"):
                        inputs["case_onboarded_date"] = date.today()
                else:
                    inputs["case_onboarded_date"] = None

            update(meta.TABLE, list(inputs.keys()), list(inputs.values()), selected_id)

            st.success("Record Updated Successfully")

            


    # ---------------- DELETE ----------------
    elif action == "Delete":
        st.subheader("Delete Record")

        data = fetch_dropdown(meta.TABLE, meta.DISPLAY_COLUMN)

        if not data:
            st.warning("No records available")
            st.stop()

        options = {f"{r[1]} ({r[0]})": r[0] for r in data}

        selected = st.selectbox("Select Record to Delete", list(options.keys()))
        selected_id = options[selected]

        record = fetch_by_id(meta.TABLE, selected_id)

        if record:
            st.subheader("📄 Selected Record Preview")

            df = pd.DataFrame([record])
            st.dataframe(df,use_container_width=True)

        confirm = st.checkbox("I confirm deletion")

        if st.button("Delete"):
            if confirm:
                delete_record(meta.TABLE, selected_id)
                st.success("Deleted successfully")
            else:
                st.warning("Please confirm deletion")