#!/usr/bin/env bash
# Idempotent environment bootstrap for the Orion Streamlit app.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -qq
sudo apt-get install -y -qq postgresql postgresql-contrib python3-venv proxychains4 socat

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

if ! command -v tailscale >/dev/null 2>&1; then
  curl -fsSL https://tailscale.com/install.sh | sh
fi

PROXYCHAINS=/etc/proxychains4.conf
sudo sed -i 's/^strict_chain/#strict_chain/' "$PROXYCHAINS"
sudo sed -i 's/^#dynamic_chain/dynamic_chain/' "$PROXYCHAINS"
sudo sed -i 's/^#proxy_dns/proxy_dns/' "$PROXYCHAINS"
sudo sed -i 's/^# localnet 127\.0\.0\.0\/255\.0\.0\.0/localnet 127.0.0.0\/255.0.0.0/' "$PROXYCHAINS"
grep -q '127.0.0.1 1055' "$PROXYCHAINS" || echo 'socks5 127.0.0.1 1055' | sudo tee -a "$PROXYCHAINS" >/dev/null

sudo pg_ctlcluster 16 main start 2>/dev/null || true
for _ in $(seq 1 30); do
  if sudo -u postgres pg_isready -q; then break; fi
  sleep 1
done

bash "$REPO_ROOT/.cursor/db/init_db.sh"

echo "Install complete."
