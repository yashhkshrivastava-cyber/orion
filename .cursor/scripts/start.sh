#!/usr/bin/env bash
set -euo pipefail

DB_TUNNEL_PORT="${DB_TUNNEL_PORT:-15432}"
DB_REMOTE_HOST="${DB_REMOTE_HOST:-100.71.92.51}"
DB_REMOTE_PORT="${DB_REMOTE_PORT:-5432}"

start_tailscale() {
  if pgrep -x tailscaled >/dev/null 2>&1; then
    echo "tailscaled already running"
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
    echo "tailscale already connected"
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
    echo "DB tunnel already listening on port ${DB_TUNNEL_PORT}"
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

  echo "DB tunnel listening on 127.0.0.1:${DB_TUNNEL_PORT}"
}

start_tailscale
connect_tailscale
start_db_tunnel

echo "Start complete."
