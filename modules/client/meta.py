TABLE = "orion_ods.client"

DISPLAY_COLUMN = "client_name"

FORM_FIELDS = {
    "client_name": {
        "label": "Client Name",
        "type": "text"
    },

    "client_status": {
        "label": "Status",
        "type": "select",
        "options": ["Active", "Inactive"]
    },

    "client_start_date": {
        "label": "Start Date",
        "type": "date"
    },

    "client_end_date": {
        "label": "End Date",
        "type": "date"
    },

    "client_location_state": {
        "label": "State",
        "type": "select",
        "options": [
            "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "UP","MP"
        ]
    },

    "client_location_city": {
        "label": "City",
        "type": "dependent_select",   # 🔥 special type
        "depends_on": "client_location_state"
    },

    "client_type": {
        "label": "Client Type",
        "type": "select",
        "options": ["Govt", "Private", "MSME"]
    },

    "firm_priority": {
        "label": "Priority",
        "type": "select",
        "options": ["P1", "P2", "P3", None]
    },

    "client_onboarded": {
        "label": "Onboarded",
        "type": "boolean"
    },

    "client_onboarded_date": {
        "label": "Onboarded Date",
        "type": "auto_date",
        "depends_on": "client_onboarded"
    }
}