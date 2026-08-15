-- Grant app user access to ODS and DW schemas.
-- Run manually if DW load fails with "permission denied for schema orion_dw":
--   psql -d orion -f .cursor/db/grants.sql

GRANT ALL ON SCHEMA orion_ods TO orion_user;
GRANT ALL ON ALL TABLES IN SCHEMA orion_ods TO orion_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA orion_ods TO orion_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA orion_ods TO orion_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA orion_ods GRANT ALL ON TABLES TO orion_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA orion_ods GRANT ALL ON SEQUENCES TO orion_user;

GRANT USAGE ON SCHEMA orion_dw TO orion_user;
GRANT ALL ON ALL TABLES IN SCHEMA orion_dw TO orion_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA orion_dw TO orion_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA orion_dw TO orion_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA orion_dw GRANT ALL ON TABLES TO orion_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA orion_dw GRANT ALL ON SEQUENCES TO orion_user;
