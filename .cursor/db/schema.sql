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

CREATE TABLE IF NOT EXISTS orion_ods.capability (
    id                 SERIAL PRIMARY KEY,
    capability_name    TEXT NOT NULL,
    capability_head    TEXT,
    created_timestamp  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orion_ods.client (
    id                     SERIAL PRIMARY KEY,
    client_name            TEXT NOT NULL,
    client_status          TEXT,
    client_start_date      DATE,
    client_end_date        DATE,
    client_location_state  TEXT,
    client_location_city   TEXT,
    client_type            TEXT,
    firm_priority          TEXT,
    client_onboarded       BOOLEAN DEFAULT FALSE,
    client_onboarded_date  DATE,
    created_timestamp      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orion_ods.app_user (
    id                 SERIAL PRIMARY KEY,
    username           TEXT NOT NULL UNIQUE,
    display_name       TEXT NOT NULL,
    password_hash      TEXT NOT NULL,
    role               TEXT NOT NULL DEFAULT 'admin',
    is_active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_timestamp  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orion_ods.case (
    id                       SERIAL PRIMARY KEY,
    case_name                TEXT NOT NULL,
    client_id                INTEGER REFERENCES orion_ods.client(id),
    capability_id            INTEGER REFERENCES orion_ods.capability(id),
    business_domain_id       INTEGER REFERENCES orion_ods.business_domain(id),
    case_start_date          DATE,
    case_end_date            DATE,
    case_status              TEXT,
    monthly_expected_revenue NUMERIC,
    monthly_allowed_km       NUMERIC,
    case_onboarded           BOOLEAN DEFAULT FALSE,
    case_onboarded_date      DATE,
    created_timestamp        TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp        TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
