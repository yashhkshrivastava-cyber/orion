import streamlit as st

from db.db_utils import fetch_dropdown
from utils.location_data import STATE_CITY_MAP


def _is_truthy(value):
    return value in [True, 1, "true", "True"]


def _field_key(col, key_prefix):
    return f"{key_prefix}_{col}" if key_prefix else col


def _render_single_field(col, config, record, key_prefix, inputs):
    field_type = config["type"]
    default_val = record.get(col) if record else None
    field_key = _field_key(col, key_prefix)

    if field_type == "auto_date":
        return None

    if field_type == "text":
        if record is not None:
            return st.text_input(
                config["label"],
                value=str(default_val) if default_val else "",
                key=field_key,
            )
        return st.text_input(config["label"], key=field_key)

    if field_type == "number":
        return st.number_input(config["label"], key=field_key)

    if field_type == "date":
        if record is None:
            use_date = st.checkbox(f"Set {config['label']}", key=f"{field_key}_check")
            return st.date_input(config["label"], key=field_key) if use_date else None
        has_value = default_val is not None
        use_date = st.checkbox(
            f"Set {config['label']}",
            value=has_value,
            key=f"{field_key}_check",
        )
        return st.date_input(config["label"], value=default_val, key=field_key) if use_date else None

    if field_type == "boolean":
        if record is None:
            return st.checkbox(config["label"], key=field_key)
        return st.checkbox(config["label"], value=_is_truthy(default_val), key=field_key)

    if field_type == "select" and "options" in config:
        options_list = config["options"]
        if record is None:
            return st.selectbox(config["label"], options_list, key=field_key)
        return st.selectbox(
            config["label"],
            options_list,
            index=options_list.index(default_val) if default_val in options_list else 0,
            key=field_key,
        )

    if field_type == "select" and "source_table" in config:
        fk_data = fetch_dropdown(config["source_table"], config["source_display_column"])
        fk_options = {f"{r[1]} ({r[0]})": r[0] for r in fk_data}
        if record is None:
            selected_label = st.selectbox(config["label"], list(fk_options.keys()), key=field_key)
            return fk_options[selected_label]
        reverse = {v: k for k, v in fk_options.items()}
        selected_display = reverse.get(default_val)
        selected_label = st.selectbox(
            config["label"],
            list(fk_options.keys()),
            index=list(fk_options.keys()).index(selected_display)
            if selected_display in fk_options
            else 0,
            key=field_key,
        )
        return fk_options[selected_label]

    if field_type == "dependent_select":
        depends_on = config.get("depends_on", "client_location_state")
        state = inputs.get(depends_on)
        cities = STATE_CITY_MAP.get(state, [])
        if record is None:
            return st.selectbox(config["label"], cities, key=field_key)
        return st.selectbox(
            config["label"],
            cities,
            index=cities.index(default_val) if default_val in cities else 0,
            key=field_key,
        )

    return None


def render_form_fields(form_fields, record=None, key_prefix=""):
    """
    Render form fields from entity metadata in a two-column layout.

    Returns a dict of column name -> user input value.
    """
    inputs = {}
    regular = []
    dependent = []

    for col, config in form_fields.items():
        if config["type"] == "dependent_select":
            dependent.append((col, config))
        elif config["type"] != "auto_date":
            regular.append((col, config))

    if regular:
        col_left, col_right = st.columns(2)
        for idx, (col, config) in enumerate(regular):
            with col_left if idx % 2 == 0 else col_right:
                inputs[col] = _render_single_field(col, config, record, key_prefix, inputs)

    for col, config in dependent:
        inputs[col] = _render_single_field(col, config, record, key_prefix, inputs)

    return inputs
