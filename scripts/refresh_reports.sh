#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python -m finance_app.crawler data/reports.sqlite3
python - <<'PY'
from finance_app.market_data import preload_company_metrics

result = preload_company_metrics("data/reports.sqlite3", refresh_cached=True)
print(f"preloaded {result['updated']}/{result['requested']} company metrics")
PY
