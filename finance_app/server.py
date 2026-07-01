import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .akshare_provider import AkshareProvider
from .candidates import build_candidate_pool
from .market_data import get_company_metrics
from .portfolio import build_default_portfolio_plan
from .refresh_manager import RefreshManager
from .storage import ReportStore


ROOT = Path(__file__).resolve().parent.parent
PUBLIC_DIR = ROOT / "public"
DB_PATH = ROOT / "data" / "reports.sqlite3"
REFRESH_MANAGER = RefreshManager(str(DB_PATH))


class FinanceHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: object, status: int = 200) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self.send_error(404)
            return
        content = path.read_bytes()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/reports":
            self._send_json(ReportStore(str(DB_PATH)).get_latest_reports())
            return
        if parsed.path == "/api/history":
            self._send_json(ReportStore(str(DB_PATH)).get_history())
            return
        if parsed.path == "/api/portfolio":
            self._send_json(build_default_portfolio_plan())
            return
        if parsed.path == "/api/data-snapshot":
            self._send_json(AkshareProvider().market_snapshot())
            return
        if parsed.path == "/api/candidates":
            store = ReportStore(str(DB_PATH))
            self._send_json(build_candidate_pool(store.get_latest_reports(), build_default_portfolio_plan()))
            return
        if parsed.path == "/api/company":
            query = parse_qs(parsed.query)
            symbol = (query.get("symbol") or [""])[0].strip()
            name = (query.get("name") or [""])[0].strip()
            if not symbol:
                self._send_json({"error": "missing symbol"}, status=400)
                return
            self._send_json(get_company_metrics(symbol, name=name, db_path=str(DB_PATH)))
            return
        if parsed.path == "/api/refresh":
            self._send_json(REFRESH_MANAGER.start())
            return
        if parsed.path == "/api/refresh-status":
            self._send_json(REFRESH_MANAGER.status())
            return
        if parsed.path in ("", "/"):
            self._send_file(PUBLIC_DIR / "index.html")
            return
        self._send_file(PUBLIC_DIR / parsed.path.lstrip("/"))

    def log_message(self, format: str, *args) -> None:
        print(f"{self.address_string()} - {format % args}")


def run(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = ThreadingHTTPServer((host, port), FinanceHandler)
    print(f"Local private finance dashboard: http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
