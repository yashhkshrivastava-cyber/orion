#!/usr/bin/env bash
# Idempotent environment bootstrap for the Orion Streamlit app.
# Installs system packages, Python dependencies, and prepares the local database.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# --- System packages: PostgreSQL + Python venv support ---
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -qq
sudo apt-get install -y -qq postgresql postgresql-contrib python3-venv

# --- Python virtual environment + dependencies ---
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

# --- Start PostgreSQL so we can initialize the database during install ---
sudo pg_ctlcluster 16 main start 2>/dev/null || true
# Wait for the server socket to accept connections.
for _ in $(seq 1 30); do
    if sudo -u postgres pg_isready -q; then break; fi
    sleep 1
done

# --- Create role, database, schema, and seed data (idempotent) ---
bash "$REPO_ROOT/.cursor/db/init_db.sh"

echo "Install complete."
