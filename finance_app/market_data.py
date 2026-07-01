import json
import urllib.parse
import urllib.request
from typing import Optional

from .models import utc_now_iso
from .storage import ReportStore


QUOTE_URL = "https://query1.finance.yahoo.com/v7/finance/quote"
CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"


def normalize_yahoo_symbol(symbol: str) -> str:
    symbol = symbol.strip()
    if symbol.endswith(".SH"):
        return f"{symbol[:-3]}.SS"
    return symbol


def _pct_change(current: float, previous: float) -> Optional[float]:
    if previous == 0:
        return None
    return round((current - previous) / previous * 100, 2)


def compute_returns(closes: list[float]) -> dict:
    cleaned = [value for value in closes if isinstance(value, (int, float))]
    if not cleaned:
        return {"three_day": None, "one_week": None, "one_month": None}
    current = cleaned[-1]

    def by_offset(days: int) -> Optional[float]:
        if len(cleaned) > days:
            return _pct_change(current, cleaned[-1 - days])
        return _pct_change(current, cleaned[0])

    return {
        "three_day": by_offset(3),
        "one_week": by_offset(5),
        "one_month": _pct_change(current, cleaned[0]),
    }


def _fetch_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 local-private-finance-research/1.0"},
    )
    with urllib.request.urlopen(request, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_quote(symbol: str) -> dict:
    yahoo_symbol = normalize_yahoo_symbol(symbol)
    params = urllib.parse.urlencode({"symbols": yahoo_symbol})
    payload = _fetch_json(f"{QUOTE_URL}?{params}")
    results = payload.get("quoteResponse", {}).get("result", [])
    if not results:
        raise ValueError(f"Yahoo Finance returned no quote for {symbol}")
    return results[0]


def fetch_chart_closes(symbol: str) -> list[float]:
    yahoo_symbol = urllib.parse.quote(normalize_yahoo_symbol(symbol), safe="")
    url = CHART_URL.format(symbol=yahoo_symbol) + "?range=1mo&interval=1d"
    payload = _fetch_json(url)
    results = payload.get("chart", {}).get("result", [])
    if not results:
        return []
    quote = results[0].get("indicators", {}).get("quote", [{}])[0]
    return quote.get("close", []) or []


def fetch_chart(symbol: str) -> dict:
    yahoo_symbol = urllib.parse.quote(normalize_yahoo_symbol(symbol), safe="")
    url = CHART_URL.format(symbol=yahoo_symbol) + "?range=1mo&interval=1d"
    payload = _fetch_json(url)
    results = payload.get("chart", {}).get("result", [])
    if not results:
        raise ValueError(f"Yahoo Finance returned no chart for {symbol}")
    return results[0]


def get_company_metrics(symbol: str, name: str = "", db_path: str = "data/reports.sqlite3") -> dict:
    store = ReportStore(db_path)
    cached = store.get_company_metrics(symbol)

    try:
        quote = {}
        quote_error = None
        try:
            quote = fetch_quote(symbol)
        except Exception as exc:
            quote_error = str(exc)

        chart = fetch_chart(symbol)
        meta = chart.get("meta", {})
        closes = chart.get("indicators", {}).get("quote", [{}])[0].get("close", []) or []
        payload = {
            "symbol": symbol,
            "yahoo_symbol": normalize_yahoo_symbol(symbol),
            "name": name or quote.get("longName") or quote.get("shortName") or meta.get("longName") or meta.get("shortName") or meta.get("symbol") or symbol,
            "price": quote.get("regularMarketPrice") or meta.get("regularMarketPrice"),
            "previous_close": meta.get("chartPreviousClose"),
            "currency": quote.get("currency") or meta.get("currency"),
            "market_cap": quote.get("marketCap"),
            "trailing_pe": quote.get("trailingPE"),
            "forward_pe": quote.get("forwardPE"),
            "dividend_yield": quote.get("dividendYield"),
            "fifty_two_week_high": quote.get("fiftyTwoWeekHigh") or meta.get("fiftyTwoWeekHigh"),
            "fifty_two_week_low": quote.get("fiftyTwoWeekLow") or meta.get("fiftyTwoWeekLow"),
            "returns": compute_returns(closes),
            "fetched_at": utc_now_iso(),
            "source": "Yahoo Finance public chart endpoint; quote fields when available",
            "stale": False,
            "error": (
                "Yahoo quote 接口暂时不可用，市值/PE/股息率等估值字段可能缺失；"
                f"价格、涨跌幅和可用区间数据来自 chart endpoint。原始错误：{quote_error}"
                if quote_error
                else None
            ),
        }
        store.save_company_metrics(symbol, payload)
        return payload
    except Exception as exc:
        if cached is not None:
            cached["stale"] = True
            cached["error"] = f"实时更新失败，显示缓存数据：{exc}"
            return cached
        return {
            "symbol": symbol,
            "yahoo_symbol": normalize_yahoo_symbol(symbol),
            "name": name or symbol,
            "price": None,
            "currency": None,
            "market_cap": None,
            "trailing_pe": None,
            "forward_pe": None,
            "dividend_yield": None,
            "fifty_two_week_high": None,
            "fifty_two_week_low": None,
            "returns": {"three_day": None, "one_week": None, "one_month": None},
            "fetched_at": utc_now_iso(),
            "source": "Yahoo Finance public quote/chart endpoints",
            "stale": True,
            "error": str(exc),
        }
