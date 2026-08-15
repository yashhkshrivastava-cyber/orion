#!/usr/bin/env bash
# Per-boot reconciliation: ensure PostgreSQL is running and the database exists.
# Must tolerate restarts and reach a clear ready state before returning.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Start the cluster if it is not already online.
sudo pg_ctlcluster 16 main start 2>/dev/null || true

for _ in $(seq 1 30); do
    if sudo -u postgres pg_isready -q; then break; fi
    sleep 1
done

# Reconcile role/database/schema in case the data directory is fresh.
bash "$REPO_ROOT/.cursor/db/init_db.sh"

echo "PostgreSQL is ready on port 5432."
