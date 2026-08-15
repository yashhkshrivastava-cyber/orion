#!/usr/bin/env bash
# Start the Orion Streamlit app (loads .env if present).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"
# shellcheck disable=SC1091
source "$REPO_ROOT/scripts/macos_python_env.sh"
# shellcheck disable=SC1091
source "$REPO_ROOT/scripts/tailscale_cmd.sh"

if [ -f ".env" ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

PORT="${ORION_PORT:-8501}"
BIND="${ORION_BIND:-0.0.0.0}"

if ! pg_isready -h "${ORION_DB_HOST:-localhost}" -p "${ORION_DB_PORT:-5432}" -q; then
  echo "PostgreSQL is not running. Start it with: brew services start postgresql@18" >&2
  exit 1
fi

if [ ! -x ".venv/bin/streamlit" ]; then
  echo "Virtualenv missing. Run: bash scripts/install-mac.sh" >&2
  exit 1
fi

echo "Starting Orion on http://${BIND}:${PORT}"
if [ -n "$TAILSCALE_BIN" ] && tailscale_cmd status --peers=false >/dev/null 2>&1; then
  TS_IP="$(tailscale_cmd ip -4 2>/dev/null || true)"
  if [ -n "$TS_IP" ]; then
    echo "Tailscale URL: http://${TS_IP}:${PORT}"
    echo "Optional HTTPS: bash scripts/tailscale-serve.sh"
  fi
fi

exec ./.venv/bin/streamlit run app.py \
  --server.port "$PORT" \
  --server.address "$BIND" \
  --server.headless true
