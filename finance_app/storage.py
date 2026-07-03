import json
import sqlite3
from pathlib import Path
from typing import Optional

from .models import MarketReport, utc_now_iso


class ReportStore:
    def __init__(self, db_path: str = "data/reports.sqlite3"):
        self.db_path = db_path
        if db_path != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                market TEXT NOT NULL,
                generated_at TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """
        )
        self.connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_reports_market_time ON reports(market, generated_at DESC)"
        )
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS company_metrics (
                symbol TEXT PRIMARY KEY,
                fetched_at TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """
        )
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slot TEXT NOT NULL,
                generated_at TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """
        )
        self.connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_pipeline_runs_slot_time ON pipeline_runs(slot, generated_at DESC)"
        )
        self.connection.commit()

    def save_report(self, report: MarketReport) -> None:
        self.connection.execute(
            "INSERT INTO reports (market, generated_at, payload) VALUES (?, ?, ?)",
            (report.market, report.generated_at, json.dumps(report.to_dict(), ensure_ascii=False)),
        )
        self.connection.commit()

    def get_latest_report(self, market: str) -> Optional[dict]:
        row = self.connection.execute(
            "SELECT payload FROM reports WHERE market = ? ORDER BY generated_at DESC LIMIT 1",
            (market,),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row["payload"])

    def get_latest_reports(self) -> list[dict]:
        rows = self.connection.execute(
            """
            SELECT payload FROM reports r
            WHERE generated_at = (
                SELECT MAX(generated_at) FROM reports WHERE market = r.market
            )
            ORDER BY market
            """
        ).fetchall()
        return [json.loads(row["payload"]) for row in rows]

    def get_history(self, limit: int = 30) -> list[dict]:
        rows = self.connection.execute(
            "SELECT payload FROM reports ORDER BY generated_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [json.loads(row["payload"]) for row in rows]

    def save_company_metrics(self, symbol: str, payload: dict) -> None:
        payload = dict(payload)
        payload.setdefault("fetched_at", utc_now_iso())
        self.connection.execute(
            """
            INSERT INTO company_metrics (symbol, fetched_at, payload)
            VALUES (?, ?, ?)
            ON CONFLICT(symbol) DO UPDATE SET
                fetched_at = excluded.fetched_at,
                payload = excluded.payload
            """,
            (symbol, payload["fetched_at"], json.dumps(payload, ensure_ascii=False)),
        )
        self.connection.commit()

    def get_company_metrics(self, symbol: str) -> Optional[dict]:
        row = self.connection.execute(
            "SELECT payload FROM company_metrics WHERE symbol = ?",
            (symbol,),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row["payload"])

    def save_pipeline_run(self, slot: str, payload: dict) -> None:
        payload = dict(payload)
        payload.setdefault("generated_at", utc_now_iso())
        self.connection.execute(
            "INSERT INTO pipeline_runs (slot, generated_at, payload) VALUES (?, ?, ?)",
            (slot, payload["generated_at"], json.dumps(payload, ensure_ascii=False)),
        )
        self.connection.commit()

    def get_pipeline_runs(self, limit: int = 20) -> list[dict]:
        rows = self.connection.execute(
            "SELECT slot, generated_at, payload FROM pipeline_runs ORDER BY generated_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [
            {
                "slot": row["slot"],
                "generated_at": row["generated_at"],
                "payload": json.loads(row["payload"]),
            }
            for row in rows
        ]
