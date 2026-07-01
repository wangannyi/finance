import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from finance_app.market_data import (
    compute_returns,
    get_company_metrics,
    normalize_yahoo_symbol,
    parse_eastmoney_fundamentals,
    parse_nasdaq_fundamentals,
    report_companies,
)
from finance_app.storage import ReportStore


class MarketDataTests(unittest.TestCase):
    def test_normalizes_symbols_for_yahoo_finance(self):
        self.assertEqual(normalize_yahoo_symbol("600900.SH"), "600900.SS")
        self.assertEqual(normalize_yahoo_symbol("300308.SZ"), "300308.SZ")
        self.assertEqual(normalize_yahoo_symbol("0700.HK"), "0700.HK")
        self.assertEqual(normalize_yahoo_symbol("NVDA"), "NVDA")

    def test_computes_returns_from_daily_closes(self):
        closes = [100, 102, 101, 105, 110, 108, 120, 125]

        returns = compute_returns(closes)

        self.assertAlmostEqual(returns["three_day"], 13.64, places=2)
        self.assertAlmostEqual(returns["one_week"], 23.76, places=2)
        self.assertAlmostEqual(returns["one_month"], 25.0, places=2)

    def test_store_saves_and_loads_company_metrics(self):
        store = ReportStore(":memory:")
        payload = {
            "symbol": "NVDA",
            "name": "NVIDIA",
            "market_cap": 1000000000,
            "trailing_pe": 42.5,
        }

        store.save_company_metrics("NVDA", payload)
        loaded = store.get_company_metrics("NVDA")

        self.assertEqual(loaded["symbol"], "NVDA")
        self.assertEqual(loaded["trailing_pe"], 42.5)

    def test_company_metrics_returns_cache_without_network_by_default(self):
        store = ReportStore(":memory:")
        store.save_company_metrics(
            "NVDA",
            {
                "symbol": "NVDA",
                "name": "NVIDIA",
                "price": 120.0,
                "fetched_at": "2026-07-01T00:00:00+00:00",
            },
        )

        with (
            patch("finance_app.market_data.fetch_quote") as fetch_quote,
            patch("finance_app.market_data.fetch_chart") as fetch_chart,
        ):
            metrics = get_company_metrics("NVDA", db_path=":memory:", store=store)

        self.assertEqual(metrics["price"], 120.0)
        self.assertTrue(metrics["cache_hit"])
        fetch_quote.assert_not_called()
        fetch_chart.assert_not_called()

    def test_company_metrics_can_force_refresh_cache(self):
        store = ReportStore(":memory:")
        store.save_company_metrics("NVDA", {"symbol": "NVDA", "price": 120.0})
        chart = {
            "meta": {"symbol": "NVDA", "regularMarketPrice": 130.0, "currency": "USD"},
            "indicators": {"quote": [{"close": [120.0, 130.0]}]},
        }

        with (
            patch("finance_app.market_data.fetch_quote", return_value={"regularMarketPrice": 131.0, "currency": "USD"}),
            patch("finance_app.market_data.fetch_chart", return_value=chart),
        ):
            metrics = get_company_metrics("NVDA", db_path=":memory:", store=store, prefer_cache=False)

        self.assertEqual(metrics["price"], 131.0)
        self.assertFalse(metrics["cache_hit"])

    def test_report_companies_deduplicates_visible_company_groups(self):
        reports = [
            {
                "horizons": {
                    "day": [
                        {
                            "leaders": [{"name": "NVIDIA", "ticker": "NVDA"}],
                            "challengers": [{"name": "NVIDIA", "ticker": "NVDA"}, {"name": "Micron", "ticker": "MU"}],
                        }
                    ]
                }
            }
        ]

        companies = report_companies(reports)

        self.assertEqual(companies, [("NVDA", "NVIDIA"), ("MU", "Micron")])

    def test_preload_company_metrics_uses_cache_by_default(self):
        from finance_app.market_data import preload_company_metrics

        reports = [{"horizons": {"day": [{"leaders": [{"name": "NVIDIA", "ticker": "NVDA"}], "challengers": []}]}}]
        with TemporaryDirectory() as tmpdir:
            db_path = f"{tmpdir}/reports.sqlite3"
            store = ReportStore(db_path)
            store.save_company_metrics("NVDA", {"symbol": "NVDA", "price": 120.0})

            with (
                patch("finance_app.market_data.fetch_quote") as fetch_quote,
                patch("finance_app.market_data.fetch_chart") as fetch_chart,
            ):
                result = preload_company_metrics(db_path, reports=reports)

        self.assertEqual(result["requested"], 1)
        self.assertEqual(result["updated"], 1)
        fetch_quote.assert_not_called()
        fetch_chart.assert_not_called()

    def test_company_metrics_falls_back_to_chart_meta_when_quote_is_blocked(self):
        chart = {
            "meta": {
                "symbol": "CEG",
                "regularMarketPrice": 248.37,
                "currency": "USD",
                "fiftyTwoWeekHigh": 350.0,
                "fiftyTwoWeekLow": 155.0,
                "chartPreviousClose": 260.0,
            },
            "indicators": {
                "quote": [
                    {
                        "close": [260.0, 255.0, 250.0, 248.37],
                    }
                ]
            },
        }

        with (
            patch("finance_app.market_data.fetch_quote", side_effect=Exception("HTTP Error 401: Unauthorized")),
            patch("finance_app.market_data.fetch_chart", return_value=chart),
        ):
            metrics = get_company_metrics("CEG", name="Constellation Energy", db_path=":memory:")

        self.assertEqual(metrics["price"], 248.37)
        self.assertEqual(metrics["currency"], "USD")
        self.assertEqual(metrics["fifty_two_week_high"], 350.0)
        self.assertEqual(metrics["fifty_two_week_low"], 155.0)
        self.assertIn("Yahoo quote 接口暂时不可用", metrics["error"])

    def test_company_metrics_uses_fallback_fundamentals_when_quote_is_blocked(self):
        chart = {
            "meta": {
                "symbol": "300661.SZ",
                "regularMarketPrice": 137.21,
                "currency": "CNY",
            },
            "indicators": {"quote": [{"close": [120.0, 137.21]}]},
        }
        fallback = {
            "market_cap": 92841300065.03,
            "trailing_pe": 187.64,
            "forward_pe": None,
            "dividend_yield": None,
            "source": "东方财富单股行情接口",
        }

        with (
            patch("finance_app.market_data.fetch_quote", side_effect=Exception("HTTP Error 401: Unauthorized")),
            patch("finance_app.market_data.fetch_chart", return_value=chart),
            patch("finance_app.market_data.fetch_fallback_fundamentals", return_value=fallback),
        ):
            metrics = get_company_metrics("300661.SZ", name="圣邦股份", db_path=":memory:")

        self.assertEqual(metrics["market_cap"], 92841300065.03)
        self.assertEqual(metrics["trailing_pe"], 187.64)
        self.assertIn("东方财富单股行情接口", metrics["source"])

    def test_parses_nasdaq_fundamentals_for_blocked_yahoo_quote_fields(self):
        summary = {
            "data": {
                "summaryData": {
                    "MarketCap": {"value": "89,708,775,947"},
                    "Yield": {"value": "0.69%"},
                    "FiftTwoWeekHighLow": {"value": "$412.7/$240.51"},
                }
            }
        }
        dividends = {
            "data": {
                "dividendHeaderValues": [
                    {"label": "Dividend Yield", "value": "0.66%"},
                    {"label": "P/E Ratio", "value": "47.67"},
                ]
            }
        }

        fundamentals = parse_nasdaq_fundamentals(summary, dividends)

        self.assertEqual(fundamentals["market_cap"], 89708775947)
        self.assertEqual(fundamentals["trailing_pe"], 47.67)
        self.assertEqual(fundamentals["dividend_yield"], 0.0066)
        self.assertEqual(fundamentals["fifty_two_week_high"], 412.7)
        self.assertEqual(fundamentals["fifty_two_week_low"], 240.51)

    def test_parses_eastmoney_a_share_fundamentals(self):
        payload = {
            "data": {
                "f57": "300661",
                "f58": "圣邦股份",
                "f116": 92841300065.03,
                "f162": 18764,
            }
        }

        fundamentals = parse_eastmoney_fundamentals(payload)

        self.assertEqual(fundamentals["market_cap"], 92841300065.03)
        self.assertEqual(fundamentals["trailing_pe"], 187.64)
        self.assertEqual(fundamentals["source"], "东方财富单股行情接口")


if __name__ == "__main__":
    unittest.main()
