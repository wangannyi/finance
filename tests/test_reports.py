import unittest

from finance_app.analyzer import build_market_report
from finance_app.config import MARKET_CONFIGS
from finance_app.storage import ReportStore


class MarketReportTests(unittest.TestCase):
    def test_builds_top_five_for_each_horizon_with_evidence_and_leaders(self):
        documents = [
            "AI 算力 CPO PCB 半导体 创新药 机器人 中报预增 红利 电力",
            "SEC EDGAR FRED Nasdaq AI semiconductor biotech ETF",
        ]

        report = build_market_report(MARKET_CONFIGS["ch"], documents)

        self.assertEqual(report.market, "ch")
        self.assertEqual(set(report.horizons), {"day", "week", "month"})

        for horizon, items in report.horizons.items():
            self.assertEqual(len(items), 5)
            for item in items:
                self.assertTrue(item.name)
                self.assertGreaterEqual(item.score, 0)
                self.assertTrue(item.evidence)
                self.assertTrue(item.leaders)

    def test_store_saves_and_loads_latest_report(self):
        store = ReportStore(":memory:")
        report = build_market_report(MARKET_CONFIGS["us"], ["AI semiconductor ETF Fed rate"])

        store.save_report(report)
        loaded = store.get_latest_report("us")

        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["market"], "us")
        self.assertIn("month", loaded["horizons"])
        self.assertEqual(len(loaded["horizons"]["month"]), 5)

    def test_us_report_surfaces_memory_and_cpo_when_documents_mention_them(self):
        documents = [
            "AI memory HBM DRAM NAND storage Micron SanDisk Western Digital Seagate",
            "CPO co-packaged optics optical networking transceiver silicon photonics Coherent Lumentum Marvell Broadcom",
        ]

        report = build_market_report(MARKET_CONFIGS["us"], documents).to_dict()
        month_names = [item["name"] for item in report["horizons"]["month"]]

        self.assertIn("AI 存储/HBM", month_names)
        self.assertIn("CPO/光通信", month_names)


if __name__ == "__main__":
    unittest.main()
