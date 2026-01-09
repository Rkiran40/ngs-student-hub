#!/usr/bin/env bash
# Helper script to copy a local env file to /etc/studenthub.env (for manual use), secure it, and restart the systemd service.
# Usage: sudo ./scripts/reload_service.sh /path/to/backend/.env
set -euo pipefail
if [ "$#" -ne 1 ]; then
  echo "Usage: sudo $0 /path/to/backend/.env"
  exit 2
fi
SRC="$1"
DEST="/etc/studenthub.env"
cp "$SRC" "$DEST"
chown root:root "$DEST"
chmod 600 "$DEST"
systemctl daemon-reload
systemctl restart studenthub
echo "studenthub restarted. Check logs: sudo journalctl -u studenthub -f"