-- Orion DW schema (SCD Type 2 dimensions and facts).

CREATE SCHEMA IF NOT EXISTS orion_dw;

CREATE TABLE IF NOT EXISTS orion_dw.dim_business_domain (
    business_domain_sk            BIGSERIAL PRIMARY KEY,
    business_domain_code          TEXT NOT NULL,
    business_domain_name          TEXT NOT NULL,
    effective_from                TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    effective_to                  TIMESTAMPTZ,
    is_current                    BOOLEAN NOT NULL DEFAULT TRUE,
    is_expired                    BOOLEAN NOT NULL DEFAULT FALSE,
    source_created_timestamp      TIMESTAMPTZ,
    source_last_updated_timestamp TIMESTAMPTZ,
    dw_created_timestamp          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dw_last_updated_timestamp     TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_dim_business_domain_current
    ON orion_dw.dim_business_domain (business_domain_code)
    WHERE is_current = TRUE;
