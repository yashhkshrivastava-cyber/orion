-- Orion ODS schema for local development.
-- Idempotent: safe to run repeatedly.

CREATE SCHEMA IF NOT EXISTS orion_ods;

CREATE SEQUENCE IF NOT EXISTS orion_ods.business_domain_seq START 1;

CREATE TABLE IF NOT EXISTS orion_ods.business_domain (
    business_domain_code   TEXT PRIMARY KEY DEFAULT (
        'BD-' || LPAD(nextval('orion_ods.business_domain_seq')::TEXT, 4, '0')
    ),
    business_domain_name   TEXT NOT NULL,
    created_timestamp      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE IF NOT EXISTS orion_ods.capability_seq START 1;

CREATE TABLE IF NOT EXISTS orion_ods.capability (
    capability_code        TEXT PRIMARY KEY DEFAULT (
        'CAP-' || LPAD(nextval('orion_ods.capability_seq')::TEXT, 4, '0')
    ),
    capability_name        TEXT NOT NULL,
    capability_head        TEXT,
    created_timestamp      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE IF NOT EXISTS orion_ods.expense_type_seq START 1;

CREATE TABLE IF NOT EXISTS orion_ods.expense_type (
    expense_type_code      TEXT PRIMARY KEY DEFAULT (
        'EXP-' || LPAD(nextval('orion_ods.expense_type_seq')::TEXT, 4, '0')
    ),
    expense_type_name      TEXT NOT NULL,
    created_timestamp      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE IF NOT EXISTS orion_ods.client_seq START 1;

CREATE TABLE IF NOT EXISTS orion_ods.client (
    client_code            TEXT PRIMARY KEY DEFAULT (
        'CL-' || LPAD(nextval('orion_ods.client_seq')::TEXT, 4, '0')
    ),
    client_name            TEXT NOT NULL,
    client_status          TEXT CHECK (client_status IN ('Active', 'Inactive')),
    client_start_date      DATE,
    client_end_date        DATE,
    client_location_state  TEXT,
    client_location_city   TEXT,
    client_type            TEXT,
    firm_priority          TEXT,
    client_onboarded       DATE,
    created_timestamp      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orion_ods.app_user (
    id                 SERIAL PRIMARY KEY,
    username           TEXT NOT NULL UNIQUE,
    display_name       TEXT NOT NULL,
    password_hash      TEXT NOT NULL,
    role               TEXT NOT NULL DEFAULT 'viewer',
    is_active          BOOLEAN NOT NULL DEFAULT TRUE,
    ods_access         BOOLEAN NOT NULL DEFAULT FALSE,
    dw_access          BOOLEAN NOT NULL DEFAULT FALSE,
    created_timestamp  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE orion_ods.app_user ALTER COLUMN role SET DEFAULT 'viewer';

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'app_user_role_check'
          AND conrelid = 'orion_ods.app_user'::regclass
    ) THEN
        ALTER TABLE orion_ods.app_user
            ADD CONSTRAINT app_user_role_check
            CHECK (role IN ('admin', 'editor', 'viewer'));
    END IF;
END $$;

CREATE SEQUENCE IF NOT EXISTS orion_ods.case_seq START 1;

CREATE TABLE IF NOT EXISTS orion_ods.case (
    case_code                TEXT PRIMARY KEY DEFAULT (
        'CS-' || LPAD(nextval('orion_ods.case_seq')::TEXT, 4, '0')
    ),
    case_name                TEXT NOT NULL,
    client_code              TEXT REFERENCES orion_ods.client(client_code),
    case_start_date          DATE,
    case_status              TEXT CHECK (case_status IN ('Active', 'Inactive')),
    case_end_date            DATE,
    capability_code          TEXT REFERENCES orion_ods.capability(capability_code),
    monthly_expected_revenue NUMERIC,
    monthly_allowed_km       INTEGER,
    business_domain_code     TEXT REFERENCES orion_ods.business_domain(business_domain_code),
    case_onboarded           BOOLEAN DEFAULT FALSE,
    created_timestamp        TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated_timestamp   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE IF NOT EXISTS orion_ods.employee_seq START 1;

CREATE TABLE IF NOT EXISTS orion_ods.employee (
    employee_code        TEXT PRIMARY KEY DEFAULT (
        'EMP-' || LPAD(nextval('orion_ods.employee_seq')::TEXT, 4, '0')
    ),
    employee_name        TEXT NOT NULL,
    employee_status      TEXT CHECK (employee_status IN ('Active', 'Inactive')),
    emp_start_date       DATE,
    emp_end_date         DATE,
    employee_type        TEXT,
    client_facing        BOOLEAN DEFAULT FALSE,
    employee_designation TEXT,
    manager_code         TEXT REFERENCES orion_ods.employee(employee_code),
    employee_case_code   TEXT REFERENCES orion_ods.case(case_code),
    created_timestamp    TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
