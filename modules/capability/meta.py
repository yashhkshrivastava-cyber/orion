TABLE = "orion_ods.capability"

PRIMARY_KEY = "capability_code"

DISPLAY_COLUMN = "capability_name"

FORM_FIELDS = {
    "capability_name": {
        "label": "Capability Name",
        "type": "text",
        "required": True,
    },
    "capability_head": {
        "label": "Capability Head",
        "type": "text"
    }
}