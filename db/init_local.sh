#!/usr/bin/env bash
# Create the Orion role/database and apply schema + seed data on localhost.
# Idempotent: safe to run repeatedly. Runs as the local postgres superuser.
set -euo pipefail

DB_NAME="${ORION_DB_NAME:-orion}"
DB_USER="${ORION_DB_USER:-orion_user}"
DB_PASSWORD="${ORION_DB_PASSWORD:-orion_dev_password}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

run_pg() { sudo -u postgres psql -v ON_ERROR_STOP=1 "$@"; }

# Role
if [ "$(run_pg -tAc "SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}'")" != "1" ]; then
    run_pg -c "CREATE ROLE ${DB_USER} LOGIN PASSWORD '${DB_PASSWORD}';"
else
    run_pg -c "ALTER ROLE ${DB_USER} LOGIN PASSWORD '${DB_PASSWORD}';"
fi

# Database
if [ "$(run_pg -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'")" != "1" ]; then
    run_pg -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"
fi

# Schema + seed (run as superuser, then grant privileges to the app user)
run_pg -d "${DB_NAME}" -f "${SCRIPT_DIR}/schema.sql"
run_pg -d "${DB_NAME}" -f "${SCRIPT_DIR}/seed.sql"

run_pg -d "${DB_NAME}" -c "GRANT ALL ON SCHEMA orion_ods TO ${DB_USER};"
run_pg -d "${DB_NAME}" -c "GRANT ALL ON ALL TABLES IN SCHEMA orion_ods TO ${DB_USER};"
run_pg -d "${DB_NAME}" -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA orion_ods TO ${DB_USER};"
run_pg -d "${DB_NAME}" -c "ALTER DEFAULT PRIVILEGES IN SCHEMA orion_ods GRANT ALL ON TABLES TO ${DB_USER};"
run_pg -d "${DB_NAME}" -c "ALTER DEFAULT PRIVILEGES IN SCHEMA orion_ods GRANT ALL ON SEQUENCES TO ${DB_USER};"

echo "Orion database '${DB_NAME}' ready on localhost for user '${DB_USER}'."
