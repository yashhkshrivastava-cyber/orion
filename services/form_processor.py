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
