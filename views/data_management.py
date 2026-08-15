import importlib
from datetime import datetime

import pandas as pd
import streamlit as st

from db.db_utils import delete_record, fetch_by_id, fetch_dropdown, fetch_top_n, insert, update
from modules.registry import MODULES
from services.form_processor import apply_auto_date_fields
from ui.components import render_record_preview, select_record
from ui.form_renderer import render_form_fields
from ui.panels import action_selector, orion_panel
from ui.styles import back_button, page_header


def _load_entity_meta(dataset):
    module_path = MODULES[dataset]
    return importlib.import_module(f"{module_path}.meta")


def _render_data_preview(meta):
    with orion_panel("Data preview", "Latest 10 records from the selected dataset"):
        cols, data = fetch_top_n(meta.TABLE, 10)
        if data:
            df = pd.DataFrame(data, columns=cols)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Refreshed {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            st.info("No records yet — create one below.")


def _render_create_form(meta, dataset):
    with orion_panel("Create record", f"Add a new entry to {dataset}"):
        key_prefix = f"create_{dataset}"
        outside_inputs = render_form_fields(
            meta.FORM_FIELDS, key_prefix=key_prefix, scope="outside_form"
        )
        with st.form(f"create_{meta.TABLE}"):
            inside_inputs = render_form_fields(
                meta.FORM_FIELDS, key_prefix=key_prefix, scope="inside_form"
            )
            submitted = st.form_submit_button("Create record", type="primary", use_container_width=True)

        if submitted:
            inputs = {**outside_inputs, **inside_inputs}
            apply_auto_date_fields(inputs, meta.FORM_FIELDS)
            insert(meta.TABLE, list(inputs.keys()), list(inputs.values()))
            st.success("Record created successfully.")


def _render_update_form(meta, dataset):
    records = fetch_dropdown(meta.TABLE, meta.DISPLAY_COLUMN)
    if not records:
        st.warning("No records available to update.")
        return

    with orion_panel("Update record", "Select a record and edit its fields"):
        selected_id = select_record(records)
        record = fetch_by_id(meta.TABLE, selected_id)
        render_record_preview(record)

        key_prefix = f"update_{dataset}_{selected_id}"
        outside_inputs = render_form_fields(
            meta.FORM_FIELDS,
            record=record,
            key_prefix=key_prefix,
            scope="outside_form",
        )
        with st.form(f"update_{meta.TABLE}"):
            inside_inputs = render_form_fields(
                meta.FORM_FIELDS,
                record=record,
                key_prefix=key_prefix,
                scope="inside_form",
            )
            submitted = st.form_submit_button("Save changes", type="primary", use_container_width=True)

        if submitted:
            inputs = {**outside_inputs, **inside_inputs}
            apply_auto_date_fields(inputs, meta.FORM_FIELDS, record=record)
            update(meta.TABLE, list(inputs.keys()), list(inputs.values()), selected_id)
            st.success("Record updated successfully.")


def _render_delete_form(meta):
    records = fetch_dropdown(meta.TABLE, meta.DISPLAY_COLUMN)
    if not records:
        st.warning("No records available to delete.")
        return

    with orion_panel("Delete record", "This action cannot be undone"):
        selected_id = select_record(records, label="Record to delete")
        record = fetch_by_id(meta.TABLE, selected_id)
        render_record_preview(record)

        confirm = st.checkbox("I understand this deletion is permanent")
        if st.button("Delete record", type="primary", use_container_width=True):
            if confirm:
                delete_record(meta.TABLE, selected_id)
                st.success("Record deleted.")
            else:
                st.warning("Please confirm deletion first.")


def render_data_management():
    if back_button():
        st.session_state.page = "home"
        st.rerun()

    page_header(
        "Data Management",
        "Create, update, and maintain platform records.",
        theme_key="data",
    )

    with orion_panel("Dataset", "Choose which entity type to work with"):
        dataset = st.selectbox("Entity", list(MODULES.keys()), label_visibility="collapsed")

    meta = _load_entity_meta(dataset)
    _render_data_preview(meta)

    action = action_selector(["Create", "Update", "Delete"], key=f"data_action_{dataset}")

    if action == "Create":
        _render_create_form(meta, dataset)
    elif action == "Update":
        _render_update_form(meta, dataset)
    else:
        _render_delete_form(meta)
