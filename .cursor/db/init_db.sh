#!/usr/bin/env bash
# Create the Orion role/database and apply schema + seed data.
# Idempotent: safe to run on every install. Runs as the local postgres superuser.
set -euo pipefail

DB_NAME="${ORION_DB_NAME:-orion}"
DB_USER="${ORION_DB_USER:-orion_app}"
DB_PASSWORD="${ORION_DB_PASSWORD:-orion_dev_password}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

run_pg() { sudo -u postgres psql -v ON_ERROR_STOP=1 "$@"; }

ensure_role() {
    local user="$1"
    local password="$2"
    if [ "$(run_pg -tAc "SELECT 1 FROM pg_roles WHERE rolname='${user}'")" != "1" ]; then
        run_pg -c "CREATE ROLE ${user} LOGIN PASSWORD '${password}';"
    else
        run_pg -c "ALTER ROLE ${user} LOGIN PASSWORD '${password}';"
    fi
}

ensure_role "${DB_USER}" "${DB_PASSWORD}"
ensure_role "orion_app" "${DB_PASSWORD}"
ensure_role "orion_user" "${DB_PASSWORD}"

if [ "$(run_pg -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'")" != "1" ]; then
    run_pg -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"
fi

run_pg -d "${DB_NAME}" -f "${SCRIPT_DIR}/schema.sql"
run_pg -d "${DB_NAME}" -f "${SCRIPT_DIR}/dw_schema.sql"
run_pg -d "${DB_NAME}" -f "${SCRIPT_DIR}/seed.sql"
run_pg -d "${DB_NAME}" -f "${SCRIPT_DIR}/grants.sql"

echo "Orion database '${DB_NAME}' ready for user '${DB_USER}'."
