TABLE = "orion_ods.case"

DISPLAY_COLUMN = "case_name"

FORM_FIELDS = {
    "case_name": {
        "label": "Case Name",
        "type": "text"
    },

    # 🔥 FK → CLIENT
    "client_id": {
        "label": "Client",
        "type": "select",
        "source_table": "orion_ods.client",
        "source_display_column": "client_name"
    },

    # 🔥 FK → CAPABILITY
    "capability_id": {
        "label": "Capability",
        "type": "select",
        "source_table": "orion_ods.capability",
        "source_display_column": "capability_name"
    },

    # 🔥 FK → BUSINESS DOMAIN
    "business_domain_id": {
        "label": "Business Domain",
        "type": "select",
        "source_table": "orion_ods.business_domain",
        "source_display_column": "business_domain_name"
    },

    "case_start_date": {
        "label": "Start Date",
        "type": "date"
    },

    "case_end_date": {
        "label": "End Date",
        "type": "date"
    },

    "case_status": {
        "label": "Status",
        "type": "select",
        "options": ["Active", "Inactive"]
    },

    "monthly_expected_revenue": {
        "label": "Expected Revenue",
        "type": "number"
    },

    "monthly_allowed_km": {
        "label": "Allowed KM",
        "type": "number"
    },

    "case_onboarded": {
        "label": "Onboarded",
        "type": "boolean"
    },

    "case_onboarded_date": {
        "label": "Onboarded Date",
        "type": "auto_date",
        "depends_on": "case_onboarded"
    }
}