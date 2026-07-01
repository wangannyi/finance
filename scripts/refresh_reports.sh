#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python -m finance_app.crawler data/reports.sqlite3
