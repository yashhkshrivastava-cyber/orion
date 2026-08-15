-- Seed reference data for local development so dropdowns and previews are populated.
-- Idempotent: only inserts when the tables are empty.

INSERT INTO orion_ods.business_domain (business_domain_name)
SELECT v FROM (VALUES ('Banking'), ('Healthcare'), ('Retail')) AS s(v)
WHERE NOT EXISTS (SELECT 1 FROM orion_ods.business_domain);

INSERT INTO orion_ods.capability (capability_name, capability_head)
SELECT v, h FROM (VALUES
    ('Data Engineering', 'Asha Rao'),
    ('Analytics', 'Vikram Singh')
) AS s(v, h)
WHERE NOT EXISTS (SELECT 1 FROM orion_ods.capability);

INSERT INTO orion_ods.client (
    client_name, client_status, client_location_state, client_location_city,
    client_type, firm_priority, client_onboarded
)
SELECT n, st, stt, ct, tp, pr, ob FROM (VALUES
    ('Acme Corp', 'Active', 'Maharashtra', 'Mumbai',    'Private', 'P1', CURRENT_DATE),
    ('Globex',    'Active', 'Karnataka',   'Bangalore', 'Govt',    'P2', NULL::date)
) AS s(n, st, stt, ct, tp, pr, ob)
WHERE NOT EXISTS (SELECT 1 FROM orion_ods.client);
