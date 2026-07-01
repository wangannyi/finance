import unittest

from finance_app.market_data import compute_returns, normalize_yahoo_symbol
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


if __name__ == "__main__":
    unittest.main()
