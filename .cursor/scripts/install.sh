#!/usr/bin/env bash
set -euo pipefail

cd /workspace

pip install -r requirements.txt

if ! command -v tailscale >/dev/null 2>&1; then
  curl -fsSL https://tailscale.com/install.sh | sh
fi

sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq proxychains4 socat

PROXYCHAINS=/etc/proxychains4.conf
sudo sed -i 's/^strict_chain/#strict_chain/' "$PROXYCHAINS"
sudo sed -i 's/^#dynamic_chain/dynamic_chain/' "$PROXYCHAINS"
sudo sed -i 's/^#proxy_dns/proxy_dns/' "$PROXYCHAINS"
sudo sed -i 's/^# localnet 127\.0\.0\.0\/255\.0\.0\.0/localnet 127.0.0.0\/255.0.0.0/' "$PROXYCHAINS"
grep -q '127.0.0.1 1055' "$PROXYCHAINS" || echo 'socks5 127.0.0.1 1055' | sudo tee -a "$PROXYCHAINS" >/dev/null

echo "Install complete."
