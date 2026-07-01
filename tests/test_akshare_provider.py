import unittest

from finance_app.akshare_provider import AkshareProvider


class FakeFrame:
    def __init__(self, rows):
        self._rows = rows

    def head(self, count):
        return FakeFrame(self._rows[:count])

    def to_dict(self, orient):
        if orient != "records":
            raise ValueError("unsupported orient")
        return self._rows


class FakeAkshare:
    def stock_zh_a_spot_em(self):
        return FakeFrame(
            [
                {"代码": "600900", "名称": "长江电力", "最新价": 26.64, "涨跌幅": -0.04, "市盈率-动态": 21.5},
                {"代码": "300308", "名称": "中际旭创", "最新价": 180.0, "涨跌幅": 2.2, "市盈率-动态": 48.6},
            ]
        )

    def stock_hk_spot_em(self):
        return FakeFrame(
            [
                {"代码": "00700", "名称": "腾讯控股", "最新价": 429.8, "涨跌幅": 1.99, "市盈率": 18.2},
            ]
        )


class BrokenAkshare:
    def stock_zh_a_spot_em(self):
        raise ConnectionError("remote disconnected")

    def stock_hk_spot_em(self):
        raise ConnectionError("remote disconnected")


class AkshareProviderTests(unittest.TestCase):
    def test_reports_unavailable_when_akshare_is_missing(self):
        provider = AkshareProvider(ak_module=None)

        status = provider.status()

        self.assertFalse(status["available"])
        self.assertIn("pip install", status["message"])

    def test_fetches_normalized_a_share_snapshot(self):
        provider = AkshareProvider(ak_module=FakeAkshare())

        rows = provider.a_share_snapshot(limit=2)

        self.assertEqual(rows[0]["symbol"], "600900.SH")
        self.assertEqual(rows[0]["name"], "长江电力")
        self.assertEqual(rows[0]["price"], 26.64)
        self.assertEqual(rows[0]["pe"], 21.5)

    def test_fetches_normalized_hk_snapshot(self):
        provider = AkshareProvider(ak_module=FakeAkshare())

        rows = provider.hk_snapshot(limit=1)

        self.assertEqual(rows[0]["symbol"], "0700.HK")
        self.assertEqual(rows[0]["name"], "腾讯控股")
        self.assertEqual(rows[0]["change_pct"], 1.99)

    def test_market_snapshot_reports_source_errors_without_raising(self):
        provider = AkshareProvider(ak_module=BrokenAkshare())

        snapshot = provider.market_snapshot()

        self.assertTrue(snapshot["status"]["available"])
        self.assertEqual(snapshot["a_share"], [])
        self.assertEqual(snapshot["hk"], [])
        self.assertTrue(snapshot["errors"])


if __name__ == "__main__":
    unittest.main()
