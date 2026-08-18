#!/usr/bin/env bash
# Per-boot reconciliation: local PostgreSQL or Tailscale remote DB tunnel.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME_ENV="$REPO_ROOT/.cursor/runtime.env"
DB_TUNNEL_PORT="${DB_TUNNEL_PORT:-15432}"
DB_REMOTE_HOST="${DB_REMOTE_HOST:-100.71.92.51}"
DB_REMOTE_PORT="${DB_REMOTE_PORT:-5432}"

write_runtime_env() {
  cat >"$RUNTIME_ENV" <<EOF
ORION_DB_HOST=$1
ORION_DB_PORT=$2
ORION_DB_PASSWORD=${3}
EOF
}

start_local_postgres() {
  sudo pg_ctlcluster 16 main start 2>/dev/null || true

  for _ in $(seq 1 30); do
    if sudo -u postgres pg_isready -q; then break; fi
    sleep 1
  done

  bash "$REPO_ROOT/.cursor/db/init_db.sh"
  write_runtime_env "localhost" "5432" "${ORION_DB_PASSWORD:-orion_dev_password}"
  echo "PostgreSQL is ready on port 5432."
}

start_tailscale() {
  if pgrep -x tailscaled >/dev/null 2>&1; then
    return 0
  fi

  sudo mkdir -p /var/run/tailscale /var/lib/tailscale
  sudo tailscaled \
    --state=/var/lib/tailscale/tailscaled.state \
    --socket=/var/run/tailscale/tailscaled.sock \
    --tun=userspace-networking \
    --socks5-server=127.0.0.1:1055 &
  sleep 2
}

connect_tailscale() {
  if tailscale status --peers=false >/dev/null 2>&1; then
    return 0
  fi

  if [ -z "${TAILSCALE_AUTHKEY:-}" ]; then
    echo "TAILSCALE_AUTHKEY is not set. Add it as a Cursor environment secret." >&2
    exit 1
  fi

  sudo tailscale up --authkey="$TAILSCALE_AUTHKEY" --accept-routes --reset
}

start_db_tunnel() {
  if ss -tln | grep -q ":${DB_TUNNEL_PORT} "; then
    return 0
  fi

  proxychains4 -q socat \
    "TCP-LISTEN:${DB_TUNNEL_PORT},fork,reuseaddr" \
    "TCP:${DB_REMOTE_HOST}:${DB_REMOTE_PORT}" &
  sleep 1

  if ! ss -tln | grep -q ":${DB_TUNNEL_PORT} "; then
    echo "Failed to start DB tunnel on port ${DB_TUNNEL_PORT}" >&2
    exit 1
  fi
}

start_remote_postgres() {
  start_tailscale
  connect_tailscale
  start_db_tunnel
  write_runtime_env "127.0.0.1" "$DB_TUNNEL_PORT" "${ORION_DB_PASSWORD:-orion_dev_password}"
  echo "Remote DB tunnel ready on 127.0.0.1:${DB_TUNNEL_PORT}."
}

if [ -n "${TAILSCALE_AUTHKEY:-}" ]; then
  start_remote_postgres
else
  start_local_postgres
fi

echo "Start complete."
