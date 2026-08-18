from datetime import date


def apply_auto_date_fields(inputs, form_fields, record=None):
    """
    Populate auto_date fields based on their depends_on boolean fields.

    Used for onboarding date logic on create and update.
    """
    for col, config in form_fields.items():
        if config.get("type") != "auto_date":
            continue

        depends_on = config.get("depends_on")
        if not depends_on or depends_on not in inputs:
            continue

        if inputs.get(depends_on):
            if record is None:
                inputs[col] = date.today()
            elif not record.get(col):
                inputs[col] = date.today()
        else:
            inputs[col] = None

    return inputs


def validate_form_inputs(inputs, form_fields):
    """Return user-facing error messages for required/blank fields."""
    errors = []
    for col, config in form_fields.items():
        if config.get("type") == "auto_date":
            continue
        value = inputs.get(col)
        required = config.get("required", False)
        if not required:
            continue
        if value is None:
            errors.append(f"{config['label']} is required.")
        elif isinstance(value, str) and not value.strip():
            errors.append(f"{config['label']} is required.")
    return errors
