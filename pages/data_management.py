import importlib
from datetime import datetime

import pandas as pd
import streamlit as st

from db.db_utils import delete_record, fetch_by_id, fetch_dropdown, fetch_top_n, insert, update
from modules.registry import MODULES
from services.form_processor import apply_auto_date_fields
from ui.components import render_record_preview, select_record
from ui.form_renderer import render_form_fields


def _load_entity_meta(dataset):
    module_path = MODULES[dataset]
    return importlib.import_module(f"{module_path}.meta")


def _render_data_preview(meta):
    st.subheader("📊 Latest Data Preview")

    cols, data = fetch_top_n(meta.TABLE, 10)

    if data:
        df = pd.DataFrame(data, columns=cols)
        st.dataframe(df)
        st.caption(f"Last refreshed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.warning("No data available")


def _render_create_form(meta):
    st.subheader("Create Record")

    inputs = render_form_fields(meta.FORM_FIELDS)

    if st.button("Create"):
        apply_auto_date_fields(inputs, meta.FORM_FIELDS)
        insert(meta.TABLE, list(inputs.keys()), list(inputs.values()))
        st.success("Record Created Successfully")


def _render_update_form(meta):
    st.subheader("Update Record")

    records = fetch_dropdown(meta.TABLE, meta.DISPLAY_COLUMN)

    if not records:
        st.warning("No records available")
        st.stop()

    selected_id = select_record(records)
    record = fetch_by_id(meta.TABLE, selected_id)

    render_record_preview(record)

    inputs = render_form_fields(meta.FORM_FIELDS, record=record)

    if st.button("Update"):
        apply_auto_date_fields(inputs, meta.FORM_FIELDS, record=record)
        update(meta.TABLE, list(inputs.keys()), list(inputs.values()), selected_id)
        st.success("Record Updated Successfully")


def _render_delete_form(meta):
    st.subheader("Delete Record")

    records = fetch_dropdown(meta.TABLE, meta.DISPLAY_COLUMN)

    if not records:
        st.warning("No records available")
        st.stop()

    selected_id = select_record(records, label="Select Record to Delete")
    record = fetch_by_id(meta.TABLE, selected_id)

    render_record_preview(record)

    confirm = st.checkbox("I confirm deletion")

    if st.button("Delete"):
        if confirm:
            delete_record(meta.TABLE, selected_id)
            st.success("Deleted successfully")
        else:
            st.warning("Please confirm deletion")


def render_data_management():
    if st.button("⬅️ Back"):
        st.session_state.page = "home"

    st.title("🛠️ Data Management")
    st.title("🚀 Orion Platform")

    dataset = st.selectbox("Select Dataset", list(MODULES.keys()))
    meta = _load_entity_meta(dataset)

    _render_data_preview(meta)

    action = st.radio("Select Action", ["Create", "Update", "Delete"])

    if action == "Create":
        _render_create_form(meta)
    elif action == "Update":
        _render_update_form(meta)
    elif action == "Delete":
        _render_delete_form(meta)
