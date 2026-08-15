def build_record_options(records):
    """Build display label -> id mapping from dropdown query results."""
    return {f"{r[1]} ({r[0]})": r[0] for r in records}


def render_record_preview(record):
    import pandas as pd
    import streamlit as st

    if record:
        st.subheader("📄 Selected Record Preview")
        df = pd.DataFrame([record])
        st.dataframe(df, use_container_width=True)


def select_record(records, label="Select Record"):
    import streamlit as st

    if not records:
        return None

    options = build_record_options(records)
    selected_label = st.selectbox(label, list(options.keys()))
    return options[selected_label]
