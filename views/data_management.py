import importlib
from datetime import datetime

import pandas as pd
import streamlit as st

from db.db_utils import delete_record, fetch_by_id, fetch_dropdown, fetch_top_n, insert, update
from db.connection import get_connection
from dw.registry import DW_SYNC
from modules.registry import MODULES
from services.auth_service import can_access_dw, can_access_ods, get_current_user
from services.dw_loader import run_dw_load
from services.form_processor import apply_auto_date_fields
from ui.components import format_display_value, format_preview_dataframe, humanize_column, render_entity_preview, select_record
from ui.form_renderer import render_form_fields
from ui.panels import action_selector, orion_panel
from ui.styles import back_button, page_header, section_title

LAYER_ODS = "Operational Database"
LAYER_DW = "Data Warehouse"

ODS_FLASH_KEY = "ods_flash_message"

DW_TABLE_QUERIES = {
    "Business Domain": """
        SELECT business_domain_sk, business_domain_code, business_domain_name,
               is_current, is_expired,
               CASE
                   WHEN is_expired THEN 'Deleted from ODS'
                   WHEN is_current THEN 'Current'
                   ELSE 'Historical'
               END AS record_status,
               effective_from,
               COALESCE(effective_to::TEXT, 'Open') AS effective_to,
               dw_created_timestamp,
               dw_last_updated_timestamp
        FROM orion_dw.dim_business_domain
        ORDER BY business_domain_code, effective_from DESC
        LIMIT 50
    """,
}


def _load_entity_meta(dataset):
    module_path = MODULES[dataset]
    return importlib.import_module(f"{module_path}.meta")


def _pk_column(meta):
    return getattr(meta, "PRIMARY_KEY", "id")


def _available_layers(user):
    layers = []
    if can_access_ods(user):
        layers.append(LAYER_ODS)
    if can_access_dw(user):
        layers.append(LAYER_DW)
    return layers


def _has_scope_fields(form_fields, scope):
    from ui.form_renderer import _partition_fields

    regular, dependent = _partition_fields(form_fields, scope)
    return bool(regular or dependent)


def _collect_form_inputs(form_fields, record, key_prefix, submit_label="Save changes"):
    inputs = {}

    section_title("Details")
    inputs.update(render_form_fields(form_fields, record, key_prefix, scope="core"))

    if _has_scope_fields(form_fields, "location"):
        with st.expander("Location", expanded=True):
            inputs.update(render_form_fields(form_fields, record, key_prefix, scope="location"))

    submitted = st.button(submit_label, type="primary", use_container_width=True, key=f"submit_{key_prefix}")
    return submitted, inputs


def _flash_after_rerun(message):
    """Queue a message so it survives the rerun that refreshes the preview."""
    st.session_state[ODS_FLASH_KEY] = message


def _render_flash():
    message = st.session_state.pop(ODS_FLASH_KEY, None)
    if message:
        st.success(message)


def _render_ods_preview(meta):
    with orion_panel("ODS preview", "Latest 10 records from orion_ods"):
        cols, data = fetch_top_n(meta.TABLE, 10)
        if not data:
            st.info("No records yet — create one below.")
            return

        df = format_preview_dataframe(pd.DataFrame(data, columns=cols), meta)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=min(42 + len(df) * 35, 380),
        )
        st.caption(f"Updated {datetime.now().strftime('%H:%M:%S')}")


def _render_create_form(meta, dataset):
    with orion_panel("Create record", f"Add a new {dataset.lower()} entry"):
        key_prefix = f"create_{dataset}"
        submitted, inputs = _collect_form_inputs(
            meta.FORM_FIELDS, None, key_prefix, submit_label="Create record"
        )

        if submitted:
            apply_auto_date_fields(inputs, meta.FORM_FIELDS)
            try:
                insert(meta.TABLE, list(inputs.keys()), list(inputs.values()))
            except Exception as exc:
                st.error(f"Could not create record: {exc}")
            else:
                _flash_after_rerun("Record created successfully.")
                st.rerun()


def _render_update_form(meta, dataset):
    pk = _pk_column(meta)
    records = fetch_dropdown(meta.TABLE, meta.DISPLAY_COLUMN, pk)
    if not records:
        st.warning("No records available to update.")
        return

    with orion_panel("Update record", "Choose a record, review it, then edit"):
        selected_id = select_record(records, key=f"update_select_{dataset}")
        record = fetch_by_id(meta.TABLE, selected_id, pk)
        render_entity_preview(record, meta)

        st.divider()
        key_prefix = f"update_{dataset}_{selected_id}"
        submitted, inputs = _collect_form_inputs(meta.FORM_FIELDS, record, key_prefix)

        if submitted:
            apply_auto_date_fields(inputs, meta.FORM_FIELDS, record=record)
            try:
                update(meta.TABLE, list(inputs.keys()), list(inputs.values()), selected_id, pk)
            except Exception as exc:
                st.error(f"Could not update record: {exc}")
            else:
                _flash_after_rerun("Record updated successfully.")
                st.rerun()


def _render_delete_form(meta, dataset):
    pk = _pk_column(meta)
    records = fetch_dropdown(meta.TABLE, meta.DISPLAY_COLUMN, pk)
    if not records:
        st.warning("No records available to delete.")
        return

    with orion_panel("Delete record", "This action cannot be undone"):
        selected_id = select_record(records, label="Record to delete", key=f"delete_select_{dataset}")
        record = fetch_by_id(meta.TABLE, selected_id, pk)
        render_entity_preview(record, meta)

        st.divider()
        confirm = st.checkbox("I understand this deletion is permanent")
        if st.button("Delete record", type="primary", use_container_width=True):
            if not confirm:
                st.warning("Please confirm deletion first.")
            else:
                try:
                    delete_record(meta.TABLE, selected_id, pk)
                except Exception as exc:
                    st.error(f"Could not delete record: {exc}")
                else:
                    _flash_after_rerun("Record deleted.")
                    st.rerun()


def _render_ods_section():
    with orion_panel("Operational dataset", "Choose an entity in orion_ods"):
        dataset = st.selectbox("Entity", list(MODULES.keys()), key="ods_entity")

    meta = _load_entity_meta(dataset)
    _render_flash()
    _render_ods_preview(meta)

    action = action_selector(["Create", "Update", "Delete"], key=f"ods_action_{dataset}")

    if action == "Create":
        _render_create_form(meta, dataset)
    elif action == "Update":
        _render_update_form(meta, dataset)
    else:
        _render_delete_form(meta, dataset)


def _fetch_dw_preview(table_name):
    query = DW_TABLE_QUERIES.get(table_name)
    if not query:
        return None, None

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        return cols, rows
    finally:
        cur.close()
        conn.close()


def _render_dw_preview(table_name):
    with orion_panel("DW preview", "Latest versions in orion_dw"):
        cols, rows = _fetch_dw_preview(table_name)
        if not rows:
            st.info("No DW rows yet — run a load from ODS.")
            return

        df = pd.DataFrame(rows, columns=cols)
        for col in ("is_current", "is_expired"):
            if col in df.columns:
                df[col] = df[col].apply(format_display_value)
        df = df.rename(columns={col: humanize_column(col) for col in df.columns})
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=min(42 + len(df) * 35, 420),
        )
        st.caption(
            "Is Expired = Yes only after the record is deleted from ODS and you run DW load. "
            "Renamed records stay Historical with Is Expired = No."
        )


def _render_dw_section():
    with orion_panel("Data warehouse", "Load ODS into orion_dw (SCD Type 2)"):
        dw_table = st.selectbox("Dimension", list(DW_SYNC.keys()), key="dw_load_table")

    _render_dw_preview(dw_table)

    with orion_panel("Run load", "Compare ODS and apply SCD Type 2 changes"):
        if st.button("Run DW load", type="primary", use_container_width=True, key="run_dw_load"):
            try:
                stats = run_dw_load(dw_table)
                st.success(
                    f"DW load complete — "
                    f"{stats['inserted']} new, "
                    f"{stats['versioned']} versioned, "
                    f"{stats['expired']} expired, "
                    f"{stats['unchanged']} unchanged."
                )
                st.rerun()
            except Exception as exc:
                st.error(f"DW load failed: {exc}")


def render_data_management():
    if back_button():
        st.session_state.page = "home"
        st.rerun()

    user = get_current_user()
    layers = _available_layers(user)

    page_header(
        "Data Management",
        "Manage operational data or run warehouse loads.",
        theme_key="data",
    )

    if not layers:
        st.warning("Your account does not have ODS or DW access. Contact an admin.")
        return

    with orion_panel("Database layer", "Choose where you want to work"):
        if len(layers) == 1:
            layer = layers[0]
            st.markdown(f"**{layer}**")
        else:
            layer = st.radio(
                "Layer",
                layers,
                horizontal=True,
                label_visibility="collapsed",
                key="data_layer",
            )

    if layer == LAYER_ODS:
        _render_ods_section()
    else:
        _render_dw_section()
