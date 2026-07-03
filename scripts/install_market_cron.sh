#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUNNER="$ROOT_DIR/scripts/run_pipeline_slot.sh"

mkdir -p "$ROOT_DIR/data"

install_line() {
  local minute="$1"
  local hour="$2"
  local slot="$3"
  echo "$minute $hour * * * $RUNNER $slot >> $ROOT_DIR/data/${slot}.log 2>&1"
}

CRON_LINES="$(
  install_line 0 8 morning
  install_line 25 9 auction
  install_line 40 11 midday
  install_line 15 15 close
  install_line 0 21 us_premarket
)"

(crontab -l 2>/dev/null | grep -v "$RUNNER" | grep -v "$ROOT_DIR/scripts/refresh_reports.sh" || true; echo "$CRON_LINES") | crontab -

echo "Installed layered private finance refresh:"
echo "$CRON_LINES"
