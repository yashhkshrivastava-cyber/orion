TABLE = "orion_ods.case"

PRIMARY_KEY = "case_code"

DISPLAY_COLUMN = "case_name"

FORM_FIELDS = {
    "case_name": {
        "label": "Case Name",
        "type": "text",
    },
    "client_code": {
        "label": "Client",
        "type": "select",
        "source_table": "orion_ods.client",
        "source_display_column": "client_name",
        "source_pk_column": "client_code",
    },
    "case_start_date": {
        "label": "Start Date",
        "type": "date",
    },
    "case_status": {
        "label": "Status",
        "type": "select",
        "options": ["Active", "Inactive"],
    },
    "case_end_date": {
        "label": "End Date",
        "type": "date",
    },
    "capability_code": {
        "label": "Capability",
        "type": "select",
        "source_table": "orion_ods.capability",
        "source_display_column": "capability_name",
        "source_pk_column": "capability_code",
    },
    "monthly_expected_revenue": {
        "label": "Monthly Expected Revenue",
        "type": "number",
    },
    "monthly_allowed_km": {
        "label": "Monthly Allowed KM",
        "type": "integer",
    },
    "business_domain_code": {
        "label": "Business Domain",
        "type": "select",
        "source_table": "orion_ods.business_domain",
        "source_display_column": "business_domain_name",
        "source_pk_column": "business_domain_code",
    },
    "case_onboarded": {
        "label": "Onboarded",
        "type": "boolean",
    },
}
