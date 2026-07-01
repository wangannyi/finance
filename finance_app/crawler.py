import re
import sys
import urllib.error
import urllib.request
from html import unescape
from typing import Iterable

from .analyzer import build_market_report
from .config import MARKET_CONFIGS
from .storage import ReportStore


def fetch_url(url: str, timeout: int = 12) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 local-private-finance-research/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read(500_000)
        charset = response.headers.get_content_charset() or "utf-8"
        return data.decode(charset, errors="ignore")


def extract_text(html: str) -> str:
    title_matches = re.findall(r"<title[^>]*>(.*?)</title>", html, flags=re.I | re.S)
    heading_matches = re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", html, flags=re.I | re.S)
    meta_matches = re.findall(r'<meta[^>]+(?:name|property)=["\'](?:description|og:title)["\'][^>]+content=["\'](.*?)["\']', html, flags=re.I | re.S)
    chunks = title_matches + heading_matches + meta_matches
    cleaned = []
    for chunk in chunks:
        text = re.sub(r"<[^>]+>", " ", chunk)
        text = re.sub(r"\s+", " ", unescape(text)).strip()
        if text:
            cleaned.append(text)
    return "\n".join(cleaned)


def collect_documents(urls: Iterable[str]) -> list[str]:
    documents = []
    for url in urls:
        try:
            documents.append(extract_text(fetch_url(url)))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            documents.append(f"抓取失败 {url}: {exc}")
    return documents


def refresh_reports(db_path: str = "data/reports.sqlite3") -> list[dict]:
    store = ReportStore(db_path)
    saved = []
    for market, config in MARKET_CONFIGS.items():
        documents = collect_documents(config["sources"])
        report = build_market_report(config, documents, market_code=market)
        store.save_report(report)
        saved.append(report.to_dict())
    return saved


def main() -> int:
    db_path = sys.argv[1] if len(sys.argv) > 1 else "data/reports.sqlite3"
    reports = refresh_reports(db_path)
    print(f"saved {len(reports)} market reports to {db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
