import json
import urllib.parse
import urllib.request
from typing import Optional

from .models import utc_now_iso
from .storage import ReportStore


QUOTE_URL = "https://query1.finance.yahoo.com/v7/finance/quote"
CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
NASDAQ_SUMMARY_URL = "https://api.nasdaq.com/api/quote/{symbol}/summary?assetclass=stocks"
NASDAQ_DIVIDENDS_URL = "https://api.nasdaq.com/api/quote/{symbol}/dividends?assetclass=stocks"
EASTMONEY_QUOTE_URL = "https://push2.eastmoney.com/api/qt/stock/get"
EASTMONEY_FIELDS = "f57,f58,f116,f162"


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


def _fetch_nasdaq_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://www.nasdaq.com",
            "Referer": "https://www.nasdaq.com/",
        },
    )
    with urllib.request.urlopen(request, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))


def _fetch_eastmoney_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 local-private-finance-research/1.0",
            "Referer": "https://quote.eastmoney.com/",
        },
    )
    with urllib.request.urlopen(request, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))


def _parse_number(value) -> float | None:
    if value in (None, "", "N/A", "NA", "--"):
        return None
    text = str(value).replace("$", "").replace(",", "").strip()
    if text.endswith("%"):
        text = text[:-1].strip()
    try:
        return float(text)
    except ValueError:
        return None


def _parse_percent_ratio(value) -> float | None:
    parsed = _parse_number(value)
    if parsed is None:
        return None
    return round(parsed / 100, 6)


def _parse_scaled_number(value, divisor: float = 100) -> float | None:
    parsed = _parse_number(value)
    if parsed is None:
        return None
    return round(parsed / divisor, 4)


def _find_header_value(items: list[dict], label: str) -> str | None:
    target = label.lower()
    for item in items:
        if str(item.get("label", "")).lower() == target:
            return item.get("value")
    return None


def fetch_quote(symbol: str) -> dict:
    yahoo_symbol = normalize_yahoo_symbol(symbol)
    params = urllib.parse.urlencode({"symbols": yahoo_symbol})
    payload = _fetch_json(f"{QUOTE_URL}?{params}")
    results = payload.get("quoteResponse", {}).get("result", [])
    if not results:
        raise ValueError(f"Yahoo Finance returned no quote for {symbol}")
    return results[0]


def fetch_nasdaq_fundamentals(symbol: str) -> dict:
    if "." in symbol:
        return {}
    encoded = urllib.parse.quote(symbol.upper(), safe="")
    summary = _fetch_nasdaq_json(NASDAQ_SUMMARY_URL.format(symbol=encoded))
    dividends = _fetch_nasdaq_json(NASDAQ_DIVIDENDS_URL.format(symbol=encoded))
    return parse_nasdaq_fundamentals(summary, dividends)


def fetch_eastmoney_fundamentals(symbol: str) -> dict:
    market = _eastmoney_market_id(symbol)
    if market is None:
        return {}
    code = symbol.split(".", 1)[0]
    params = urllib.parse.urlencode({"secid": f"{market}.{code}", "fields": EASTMONEY_FIELDS})
    payload = _fetch_eastmoney_json(f"{EASTMONEY_QUOTE_URL}?{params}")
    return parse_eastmoney_fundamentals(payload)


def fetch_fallback_fundamentals(symbol: str) -> dict:
    if symbol.endswith((".SZ", ".SH")):
        return fetch_eastmoney_fundamentals(symbol)
    return fetch_nasdaq_fundamentals(symbol)


def _eastmoney_market_id(symbol: str) -> str | None:
    if symbol.endswith(".SH"):
        return "1"
    if symbol.endswith(".SZ"):
        return "0"
    return None


def parse_eastmoney_fundamentals(payload: dict) -> dict:
    data = payload.get("data") or {}
    if not data:
        return {}
    return {
        "market_cap": _parse_number(data.get("f116")),
        "trailing_pe": _parse_scaled_number(data.get("f162")),
        "forward_pe": None,
        "dividend_yield": None,
        "fifty_two_week_high": None,
        "fifty_two_week_low": None,
        "source": "东方财富单股行情接口",
    }


def parse_nasdaq_fundamentals(summary: dict, dividends: dict) -> dict:
    summary_data = summary.get("data", {}).get("summaryData", {})
    dividend_headers = dividends.get("data", {}).get("dividendHeaderValues", [])
    high_low = summary_data.get("FiftTwoWeekHighLow", {}).get("value")
    high = low = None
    if high_low and "/" in high_low:
        high_text, low_text = high_low.split("/", 1)
        high = _parse_number(high_text)
        low = _parse_number(low_text)

    dividend_yield = _parse_percent_ratio(_find_header_value(dividend_headers, "Dividend Yield"))
    if dividend_yield is None:
        dividend_yield = _parse_percent_ratio(summary_data.get("Yield", {}).get("value"))

    market_cap_float = _parse_number(summary_data.get("MarketCap", {}).get("value"))
    return {
        "market_cap": int(market_cap_float) if market_cap_float is not None else None,
        "trailing_pe": _parse_number(_find_header_value(dividend_headers, "P/E Ratio")),
        "forward_pe": None,
        "dividend_yield": dividend_yield,
        "fifty_two_week_high": high,
        "fifty_two_week_low": low,
        "source": "NASDAQ public quote summary/dividends endpoints",
    }


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
        fundamentals = {}
        fundamentals_error = None
        if quote_error:
            try:
                fundamentals = fetch_fallback_fundamentals(symbol)
            except Exception as exc:
                fundamentals_error = str(exc)

        chart = fetch_chart(symbol)
        meta = chart.get("meta", {})
        closes = chart.get("indicators", {}).get("quote", [{}])[0].get("close", []) or []
        sources = ["Yahoo Finance public chart endpoint"]
        if quote:
            sources.append("Yahoo Finance public quote endpoint")
        if fundamentals:
            sources.append(fundamentals.get("source", "NASDAQ public endpoints"))
        payload = {
            "symbol": symbol,
            "yahoo_symbol": normalize_yahoo_symbol(symbol),
            "name": name or quote.get("longName") or quote.get("shortName") or meta.get("longName") or meta.get("shortName") or meta.get("symbol") or symbol,
            "price": quote.get("regularMarketPrice") or meta.get("regularMarketPrice"),
            "previous_close": meta.get("chartPreviousClose"),
            "currency": quote.get("currency") or meta.get("currency"),
            "market_cap": quote.get("marketCap") or fundamentals.get("market_cap"),
            "trailing_pe": quote.get("trailingPE") or fundamentals.get("trailing_pe"),
            "forward_pe": quote.get("forwardPE") or fundamentals.get("forward_pe"),
            "dividend_yield": quote.get("dividendYield") or fundamentals.get("dividend_yield"),
            "fifty_two_week_high": quote.get("fiftyTwoWeekHigh") or meta.get("fiftyTwoWeekHigh") or fundamentals.get("fifty_two_week_high"),
            "fifty_two_week_low": quote.get("fiftyTwoWeekLow") or meta.get("fiftyTwoWeekLow") or fundamentals.get("fifty_two_week_low"),
            "returns": compute_returns(closes),
            "fetched_at": utc_now_iso(),
            "source": "; ".join(sources),
            "stale": False,
            "error": (
                "Yahoo quote 接口暂时不可用，已尝试用备用公开接口补齐市值/PE/股息率；"
                f"价格、涨跌幅和可用区间数据来自 chart endpoint。原始错误：{quote_error}"
                + (f"；备用源错误：{fundamentals_error}" if fundamentals_error else "")
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
