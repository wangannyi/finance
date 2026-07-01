#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REFRESH_CMD="$ROOT_DIR/scripts/refresh_reports.sh"
CRON_LINE="30 8 * * * $REFRESH_CMD >> $ROOT_DIR/data/refresh.log 2>&1"

mkdir -p "$ROOT_DIR/data"

(crontab -l 2>/dev/null | grep -v "$REFRESH_CMD" || true; echo "$CRON_LINE") | crontab -

echo "Installed daily private finance refresh:"
echo "$CRON_LINE"
