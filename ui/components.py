def build_record_options(records):
    """Build display label -> id mapping from dropdown query results."""
    return {f"{r[1]} ({r[0]})": r[0] for r in records}


def render_record_preview(record):
    from ui.styles import panel_header, render_kv_preview

    if record:
        panel_header("Selected record", "Review the current values before saving")
        render_kv_preview(record)


def select_record(records, label="Select record"):
    import streamlit as st

    if not records:
        return None

    options = build_record_options(records)
    selected_label = st.selectbox(label, list(options.keys()))
    return options[selected_label]
