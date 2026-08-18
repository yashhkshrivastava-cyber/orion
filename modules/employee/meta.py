TABLE = "orion_ods.employee"

PRIMARY_KEY = "employee_code"

DISPLAY_COLUMN = "employee_name"

FORM_FIELDS = {
    "employee_name": {
        "label": "Employee Name",
        "type": "text",
        "required": True,
    },
    "employee_status": {
        "label": "Status",
        "type": "select",
        "options": ["Active", "Inactive"],
    },
    "emp_start_date": {
        "label": "Start Date",
        "type": "date",
    },
    "emp_end_date": {
        "label": "End Date",
        "type": "date",
    },
    "employee_type": {
        "label": "Employee Type",
        "type": "select",
        "options": ["Full-time", "Part-time", "Contract", "Intern"],
    },
    "client_facing": {
        "label": "Client Facing",
        "type": "boolean",
    },
    "employee_designation": {
        "label": "Designation",
        "type": "text",
    },
    "manager_code": {
        "label": "Manager",
        "type": "select",
        "source_table": "orion_ods.employee",
        "source_display_column": "employee_name",
        "source_pk_column": "employee_code",
        "optional": True,
    },
    "employee_case_code": {
        "label": "Case",
        "type": "select",
        "source_table": "orion_ods.case",
        "source_display_column": "case_name",
        "source_pk_column": "case_code",
        "optional": True,
    },
}
