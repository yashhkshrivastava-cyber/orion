import streamlit as st

from db.db_utils import fetch_dropdown
from utils.location_data import STATE_CITY_MAP


def _is_truthy(value):
    return value in [True, 1, "true", "True"]


def render_form_fields(form_fields, record=None):
    """
    Render form fields from entity metadata.

    Returns a dict of column name -> user input value.
    """
    inputs = {}

    for col, config in form_fields.items():
        field_type = config["type"]
        default_val = record.get(col) if record else None

        if field_type == "auto_date":
            continue

        if field_type == "text":
            inputs[col] = st.text_input(
                config["label"],
                value=str(default_val) if default_val else "",
            ) if record is not None else st.text_input(config["label"])

        elif field_type == "number":
            inputs[col] = st.number_input(config["label"])

        elif field_type == "date":
            if record is None:
                use_date = st.checkbox(f"Set {config['label']}", key=f"{col}_check")
                inputs[col] = (
                    st.date_input(config["label"], key=col) if use_date else None
                )
            else:
                has_value = default_val is not None
                use_date = st.checkbox(
                    f"Set {config['label']}",
                    value=has_value,
                    key=f"{col}_check",
                )
                inputs[col] = (
                    st.date_input(config["label"], value=default_val, key=col)
                    if use_date
                    else None
                )

        elif field_type == "boolean":
            if record is None:
                inputs[col] = st.checkbox(config["label"])
            else:
                inputs[col] = st.checkbox(
                    config["label"],
                    value=_is_truthy(default_val),
                )

        elif field_type == "select" and "options" in config:
            options_list = config["options"]
            if record is None:
                inputs[col] = st.selectbox(config["label"], options_list)
            else:
                inputs[col] = st.selectbox(
                    config["label"],
                    options_list,
                    index=options_list.index(default_val)
                    if default_val in options_list
                    else 0,
                )

        elif field_type == "select" and "source_table" in config:
            fk_data = fetch_dropdown(
                config["source_table"],
                config["source_display_column"],
            )
            fk_options = {f"{r[1]} ({r[0]})": r[0] for r in fk_data}

            if record is None:
                selected_label = st.selectbox(config["label"], list(fk_options.keys()))
                inputs[col] = fk_options[selected_label]
            else:
                reverse = {v: k for k, v in fk_options.items()}
                selected_display = reverse.get(default_val)
                selected_label = st.selectbox(
                    config["label"],
                    list(fk_options.keys()),
                    index=list(fk_options.keys()).index(selected_display)
                    if selected_display in fk_options
                    else 0,
                )
                inputs[col] = fk_options[selected_label]

        elif field_type == "dependent_select":
            depends_on = config.get("depends_on", "client_location_state")
            state = inputs.get(depends_on)
            cities = STATE_CITY_MAP.get(state, [])

            if record is None:
                inputs[col] = st.selectbox(config["label"], cities)
            else:
                inputs[col] = st.selectbox(
                    config["label"],
                    cities,
                    index=cities.index(default_val) if default_val in cities else 0,
                )

    return inputs
