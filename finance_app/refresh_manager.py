import threading
from datetime import datetime, timezone
from typing import Callable

from .crawler import refresh_reports


class RefreshManager:
    def __init__(self, db_path: str, runner: Callable[[str], list[dict]] = refresh_reports):
        self.db_path = db_path
        self.runner = runner
        self._lock = threading.Lock()
        self._thread: threading.Thread | None = None
        self._status = {
            "status": "idle",
            "message": "等待刷新",
            "started_at": None,
            "finished_at": None,
            "saved_count": 0,
            "error": None,
        }

    def start(self) -> dict:
        with self._lock:
            if self._thread and self._thread.is_alive():
                return {**self._status, "message": "刷新已在运行"}
            self._status = {
                "status": "running",
                "message": "后台刷新中",
                "started_at": _now_iso(),
                "finished_at": None,
                "saved_count": 0,
                "error": None,
            }
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
            return dict(self._status)

    def status(self) -> dict:
        with self._lock:
            return dict(self._status)

    def _run(self) -> None:
        try:
            reports = self.runner(self.db_path)
            with self._lock:
                self._status.update(
                    {
                        "status": "complete",
                        "message": "刷新完成",
                        "finished_at": _now_iso(),
                        "saved_count": len(reports),
                        "error": None,
                    }
                )
        except Exception as exc:  # pragma: no cover - defensive for background worker
            with self._lock:
                self._status.update(
                    {
                        "status": "error",
                        "message": "刷新失败",
                        "finished_at": _now_iso(),
                        "error": str(exc),
                    }
                )


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
