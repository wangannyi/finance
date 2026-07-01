import unittest

from finance_app.analyzer import build_market_report
from finance_app.config import MARKET_CONFIGS
from finance_app.storage import ReportStore


class MarketReportTests(unittest.TestCase):
    def test_builds_top_ten_for_each_horizon_with_company_groups(self):
        documents = [
            "AI 算力 CPO PCB 半导体 创新药 机器人 中报预增 红利 电力",
            "SEC EDGAR FRED Nasdaq AI semiconductor biotech ETF",
        ]

        report = build_market_report(MARKET_CONFIGS["ch"], documents)

        self.assertEqual(report.market, "ch")
        self.assertEqual(set(report.horizons), {"day", "week", "month"})

        for horizon, items in report.horizons.items():
            self.assertEqual(len(items), 10)
            for item in items:
                self.assertTrue(item.name)
                self.assertGreaterEqual(item.score, 0)
                self.assertTrue(item.evidence)
                self.assertEqual(len(item.leaders), 5)
                self.assertEqual(len(item.challengers), 5)
                leader_symbols = {leader.ticker for leader in item.leaders}
                challenger_symbols = {company.ticker for company in item.challengers}
                self.assertFalse(leader_symbols & challenger_symbols)

    def test_company_groups_are_theme_specific_not_market_padding(self):
        ch_report = build_market_report(MARKET_CONFIGS["ch"], ["固态电池 硫化物电解质"]).to_dict()
        solid_state = next(item for item in ch_report["horizons"]["day"] if item["name"] == "固态电池")
        solid_state_symbols = {item["ticker"] for item in solid_state["leaders"] + solid_state["challengers"]}

        self.assertIn("300750.SZ", solid_state_symbols)
        self.assertNotIn("300308.SZ", solid_state_symbols)

        us_report = build_market_report(MARKET_CONFIGS["us"], ["quantum IonQ Rigetti D-Wave QUBT"]).to_dict()
        quantum = next(item for item in us_report["horizons"]["day"] if item["name"] == "量子计算")
        quantum_symbols = {item["ticker"] for item in quantum["leaders"] + quantum["challengers"]}

        self.assertIn("IONQ", quantum_symbols)
        self.assertNotIn("NVDA", quantum_symbols)

        hk_report = build_market_report(MARKET_CONFIGS["hk"], ["高股息 股息 dividend yield 中国移动 中国海洋石油"]).to_dict()
        dividend = next(item for item in hk_report["horizons"]["month"] if item["name"] == "高股息央国企")
        dividend_symbols = {item["ticker"] for item in dividend["leaders"] + dividend["challengers"]}

        self.assertIn("1088.HK", dividend_symbols)
        self.assertNotIn("0700.HK", dividend_symbols)

    def test_us_quantum_challengers_are_pure_theme_not_platform_megacaps(self):
        report = build_market_report(MARKET_CONFIGS["us"], ["quantum IonQ Rigetti D-Wave QUBT"]).to_dict()
        quantum = next(item for item in report["horizons"]["day"] if item["name"] == "量子计算")
        challenger_symbols = {item["ticker"] for item in quantum["challengers"]}

        self.assertIn("IONQ", challenger_symbols)
        self.assertNotIn("MSFT", challenger_symbols)
        self.assertNotIn("AMZN", challenger_symbols)

    def test_store_saves_and_loads_latest_report(self):
        store = ReportStore(":memory:")
        report = build_market_report(MARKET_CONFIGS["us"], ["AI semiconductor ETF Fed rate"])

        store.save_report(report)
        loaded = store.get_latest_report("us")

        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["market"], "us")
        self.assertIn("month", loaded["horizons"])
        self.assertEqual(len(loaded["horizons"]["month"]), 10)

    def test_us_report_surfaces_memory_and_cpo_when_documents_mention_them(self):
        documents = [
            "AI memory HBM DRAM NAND storage Micron SanDisk Western Digital Seagate",
            "CPO co-packaged optics optical networking transceiver silicon photonics Coherent Lumentum Marvell Broadcom",
        ]

        report = build_market_report(MARKET_CONFIGS["us"], documents).to_dict()
        month_names = [item["name"] for item in report["horizons"]["month"]]

        self.assertIn("AI 存储/HBM", month_names)
        self.assertIn("CPO/光通信", month_names)

    def test_report_includes_direction_level_evidence_sources(self):
        documents = [
            {
                "url": "https://example.com/cpo",
                "title": "CPO optical transceiver demand accelerates",
                "text": "CPO co-packaged optics optical transceiver silicon photonics Coherent Lumentum Marvell",
                "error": None,
            }
        ]

        report = build_market_report(MARKET_CONFIGS["us"], documents).to_dict()
        cpo = next(item for item in report["horizons"]["month"] if item["name"] == "CPO/光通信")

        self.assertEqual(cpo["evidence_sources"][0]["url"], "https://example.com/cpo")
        self.assertEqual(cpo["evidence_sources"][0]["title"], "CPO optical transceiver demand accelerates")
        self.assertIn("CPO", cpo["evidence_sources"][0]["matched_keywords"])

    def test_report_includes_proactive_discovered_themes(self):
        documents = [
            {
                "url": "https://example.com/quantum",
                "title": "Quantum computing stocks rally",
                "text": "IonQ Rigetti D-Wave quantum computing stocks rally.",
                "error": None,
            }
        ]

        report = build_market_report(MARKET_CONFIGS["us"], documents).to_dict()
        names = [theme["name"] for theme in report["discovered_themes"]]

        self.assertIn("量子计算", names)

    def test_uses_horizon_specific_direction_pools(self):
        market_config = {
            "code": "demo",
            "name": "测试市场",
            "summary": "测试不同周期粒度。",
            "sources": [],
            "directions": [],
            "horizon_directions": {
                "day": [
                    {
                        "name": "CPO商业化催化",
                        "keywords": ["CPO", "商业化"],
                        "risk": "短线催化波动大。",
                        "leaders": [("日度龙头", "DAY", "日度交易线索。")],
                    }
                ],
                "week": [
                    {
                        "name": "光模块订单链",
                        "keywords": ["光模块", "订单"],
                        "risk": "订单兑现需要验证。",
                        "leaders": [("周度龙头", "WEEK", "周度产业链线索。")],
                    }
                ],
                "month": [
                    {
                        "name": "AI算力基础设施",
                        "keywords": ["AI", "算力"],
                        "risk": "估值和资本开支风险。",
                        "leaders": [("月度龙头", "MONTH", "月度主线配置。")],
                    }
                ],
            },
        }

        report = build_market_report(
            market_config,
            ["AI 算力 光模块 订单 CPO 商业化"],
        ).to_dict()

        self.assertEqual(report["horizons"]["day"][0]["name"], "CPO商业化催化")
        self.assertEqual(report["horizons"]["week"][0]["name"], "光模块订单链")
        self.assertEqual(report["horizons"]["month"][0]["name"], "AI算力基础设施")

    def test_a_share_config_uses_finer_granularity_for_shorter_horizons(self):
        report = build_market_report(
            MARKET_CONFIGS["ch"],
            [
                "CPO 商业化 光模块 资金流入 存储芯片 模拟芯片 功率半导体 涨价 PCB AI服务器",
                "AI 算力 半导体国产替代 创新药 红利 机器人",
            ],
        ).to_dict()

        day_names = [item["name"] for item in report["horizons"]["day"]]
        week_names = [item["name"] for item in report["horizons"]["week"]]
        month_names = [item["name"] for item in report["horizons"]["month"]]

        self.assertNotEqual(day_names, week_names)
        self.assertNotEqual(week_names, month_names)
        self.assertIn("CPO商业化/光模块资金", day_names)
        self.assertIn("PCB/AI服务器链", week_names)
        self.assertIn("AI 算力硬件", month_names)

    def test_all_market_configs_keep_horizon_names_distinct(self):
        documents = [
            "CPO 光模块 PCB AI服务器 存储芯片 模拟芯片 功率半导体 涨价 机器人",
            "AI boom fundraising share sales IPO dividend buyback biotech semiconductor chip",
            "Micron HBM CPO Coherent nuclear grid defense SpaceX stablecoin tokenization AI data center",
        ]

        for market_code, config in MARKET_CONFIGS.items():
            with self.subTest(market=market_code):
                report = build_market_report(config, documents, market_code=market_code).to_dict()
                day_names = [item["name"] for item in report["horizons"]["day"]]
                week_names = [item["name"] for item in report["horizons"]["week"]]
                month_names = [item["name"] for item in report["horizons"]["month"]]

                self.assertNotEqual(day_names, week_names)
                self.assertNotEqual(week_names, month_names)


if __name__ == "__main__":
    unittest.main()
