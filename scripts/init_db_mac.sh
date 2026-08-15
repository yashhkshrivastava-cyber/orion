#!/usr/bin/env bash
# Create the Orion role/database and apply schema + seed data (macOS / Homebrew PostgreSQL).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCHEMA_DIR="$REPO_ROOT/.cursor/db"

DB_NAME="${ORION_DB_NAME:-orion}"
DB_USER="${ORION_DB_USER:-orion_user}"
DB_PASSWORD="${ORION_DB_PASSWORD:-orion_dev_password}"

run_pg() { psql -d postgres -v ON_ERROR_STOP=1 "$@"; }

if ! pg_isready -h "${ORION_DB_HOST:-localhost}" -p "${ORION_DB_PORT:-5432}" -q; then
  echo "PostgreSQL is not accepting connections. Start it with:" >&2
  echo "  brew services start postgresql@18" >&2
  exit 1
fi

if [ "$(run_pg -tAc "SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}'")" != "1" ]; then
  run_pg -c "CREATE ROLE ${DB_USER} LOGIN PASSWORD '${DB_PASSWORD}';"
else
  run_pg -c "ALTER ROLE ${DB_USER} LOGIN PASSWORD '${DB_PASSWORD}';"
fi

if [ "$(run_pg -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'")" != "1" ]; then
  run_pg -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"
fi

run_pg -d "${DB_NAME}" -f "${SCHEMA_DIR}/schema.sql"
run_pg -d "${DB_NAME}" -f "${SCHEMA_DIR}/seed.sql"

run_pg -d "${DB_NAME}" -c "GRANT ALL ON SCHEMA orion_ods TO ${DB_USER};"
run_pg -d "${DB_NAME}" -c "GRANT ALL ON ALL TABLES IN SCHEMA orion_ods TO ${DB_USER};"
run_pg -d "${DB_NAME}" -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA orion_ods TO ${DB_USER};"
run_pg -d "${DB_NAME}" -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA orion_ods TO ${DB_USER};"
run_pg -d "${DB_NAME}" -c "ALTER DEFAULT PRIVILEGES IN SCHEMA orion_ods GRANT ALL ON TABLES TO ${DB_USER};"
run_pg -d "${DB_NAME}" -c "ALTER DEFAULT PRIVILEGES IN SCHEMA orion_ods GRANT ALL ON SEQUENCES TO ${DB_USER};"

echo "Orion database '${DB_NAME}' ready for user '${DB_USER}'."
