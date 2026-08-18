from html import escape
from typing import List, Optional

import pandas as pd
import streamlit as st

AUDIT_COLUMNS = {"created_timestamp", "last_updated_timestamp"}


def humanize_column(name: str) -> str:
    return name.replace("_", " ").title()


def format_display_value(value) -> str:
    if value is None:
        return "—"
    if value is True:
        return "Yes"
    if value is False:
        return "No"
    if hasattr(value, "strftime"):
        return value.strftime("%d %b %Y")
    return str(value)


def build_record_options(records):
    """Map primary key -> display label for selectors."""
    return {r[0]: f"{r[1]}  ·  {r[0]}" for r in records}


def select_record(records, label="Record", key: Optional[str] = None):
    if not records:
        return None

    labels = build_record_options(records)
    codes = [r[0] for r in sorted(records, key=lambda row: str(row[1]).lower())]

    st.markdown(f"**{label}**")
    selected_code = st.selectbox(
        label,
        options=codes,
        format_func=lambda code: labels[code],
        label_visibility="collapsed",
        key=key,
    )
    return selected_code


def preview_column_order(meta) -> List[str]:
    pk = getattr(meta, "PRIMARY_KEY", "id")
    order = []
    if pk:
        order.append(pk)
    display = getattr(meta, "DISPLAY_COLUMN", None)
    if display and display not in order:
        order.append(display)
    for col in meta.FORM_FIELDS:
        if col not in order:
            order.append(col)
    for col in AUDIT_COLUMNS:
        if col not in order:
            order.append(col)
    return order


def format_preview_dataframe(df: pd.DataFrame, meta) -> pd.DataFrame:
    order = [col for col in preview_column_order(meta) if col in df.columns]
    extra = [col for col in df.columns if col not in order]
    df = df[order + extra].copy()

    rename = {
        col: meta.FORM_FIELDS[col]["label"]
        for col in df.columns
        if col in meta.FORM_FIELDS
    }
    for col in df.columns:
        rename.setdefault(col, humanize_column(col))
    return df.rename(columns=rename)


def render_entity_preview(record, meta):
    """Compact, labelled snapshot of the selected record."""
    if not record:
        return

    pk = getattr(meta, "PRIMARY_KEY", "id")
    form_fields = meta.FORM_FIELDS

    with st.expander("View current values", expanded=False):
        if pk and record.get(pk):
            st.markdown(f"**{humanize_column(pk)}:** `{record[pk]}`")

        items = [(cfg["label"], record[col]) for col, cfg in form_fields.items() if col in record]
        if not items:
            st.info("No editable fields to preview.")
            return

        left, right = st.columns(2)
        for index, (label, value) in enumerate(items):
            with left if index % 2 == 0 else right:
                st.markdown(
                    f'<p style="margin:0 0 0.15rem;font-size:0.72rem;font-weight:600;'
                    f'letter-spacing:0.05em;text-transform:uppercase;color:#94a3b8;">'
                    f"{escape(str(label))}</p>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p style="margin:0 0 0.85rem;font-size:0.9rem;color:#e2e8f0;">'
                    f"{escape(format_display_value(value))}</p>",
                    unsafe_allow_html=True,
                )

        audit = [(humanize_column(col), record[col]) for col in AUDIT_COLUMNS if col in record]
        if audit:
            st.divider()
            audit_left, audit_right = st.columns(2)
            for index, (label, value) in enumerate(audit):
                with audit_left if index % 2 == 0 else audit_right:
                    st.caption(label)
                    st.write(format_display_value(value))


def render_record_preview(record, meta=None):
    if meta is not None:
        render_entity_preview(record, meta)
        return

    if record:
        render_entity_preview(
            record,
            type("Meta", (), {"FORM_FIELDS": {}, "PRIMARY_KEY": None})(),
        )
