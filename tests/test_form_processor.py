from datetime import date

from services.form_processor import apply_auto_date_fields, validate_form_inputs


def test_validate_required_text_rejects_blank():
    fields = {
        "client_name": {"label": "Client Name", "type": "text", "required": True},
        "client_type": {"label": "Client Type", "type": "select"},
    }
    assert validate_form_inputs({"client_name": "  ", "client_type": "Govt"}, fields) == [
        "Client Name is required."
    ]


def test_validate_optional_text_allows_blank():
    fields = {
        "capability_head": {"label": "Capability Head", "type": "text"},
    }
    assert validate_form_inputs({"capability_head": ""}, fields) == []


def test_validate_required_none():
    fields = {
        "case_name": {"label": "Case Name", "type": "text", "required": True},
    }
    assert validate_form_inputs({"case_name": None}, fields) == ["Case Name is required."]


def test_auto_date_sets_today_on_create_when_flagged():
    fields = {
        "onboarded": {"type": "boolean"},
        "onboarded_date": {"type": "auto_date", "depends_on": "onboarded"},
    }
    inputs = {"onboarded": True}
    apply_auto_date_fields(inputs, fields)
    assert inputs["onboarded_date"] == date.today()


def test_auto_date_clears_when_flag_off():
    fields = {
        "onboarded": {"type": "boolean"},
        "onboarded_date": {"type": "auto_date", "depends_on": "onboarded"},
    }
    inputs = {"onboarded": False, "onboarded_date": date.today()}
    apply_auto_date_fields(inputs, fields, record={"onboarded_date": date.today()})
    assert inputs["onboarded_date"] is None
