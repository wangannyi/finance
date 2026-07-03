#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

SLOT="${1:-morning}"
python -m finance_app.pipeline_runner "$SLOT" data/reports.sqlite3
