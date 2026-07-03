import unittest

from finance_app.analyzer import build_market_report
from finance_app.config import MARKET_CONFIGS
from finance_app.intraday_brief import build_intraday_brief


class IntradayBriefTests(unittest.TestCase):
    def test_builds_five_short_term_modules_without_deterministic_predictions(self):
        reports = [
            build_market_report(
                MARKET_CONFIGS["ch"],
                [
                    {
                        "url": "https://example.com/a",
                        "title": "存储芯片、CPO、先进封装和电子特气活跃",
                        "text": "深科技 通富微电 存储芯片 HBM CPO 先进封装 电子特气 光刻胶 刻蚀材料。",
                    }
                ],
            ).to_dict(),
            build_market_report(
                MARKET_CONFIGS["us"],
                [
                    {
                        "url": "https://example.com/us",
                        "title": "Micron and optical stocks guide AI hardware sentiment",
                        "text": "Micron HBM DRAM CPO optical transceiver semiconductor packaging.",
                    }
                ],
            ).to_dict(),
        ]

        brief = build_intraday_brief(reports)

        self.assertEqual(
            set(brief),
            {"radar", "holdings", "signals", "predictions", "logic_chains"},
        )
        self.assertEqual(
            [group["name"] for group in brief["radar"]],
            ["低位埋伏", "强势接力", "风险释放", "不能碰"],
        )
        self.assertGreaterEqual(len(brief["holdings"]), 4)
        self.assertTrue(any(item["name"] == "深科技" for item in brief["holdings"]))
        self.assertTrue(all(item["action"] in {"留", "减", "清", "观察"} for item in brief["holdings"]))
        shenkeji = next(item for item in brief["holdings"] if item["name"] == "深科技")
        self.assertIn("stop_loss", shenkeji)
        self.assertIn("trigger", shenkeji)
        self.assertLess(shenkeji["stop_loss"], shenkeji["cost"])
        self.assertTrue(shenkeji["trigger"])
        self.assertTrue(brief["signals"])
        self.assertTrue(brief["logic_chains"])

        prediction = brief["predictions"][0]
        self.assertEqual(set(prediction["horizons"]), {"1d", "3d", "5d"})
        self.assertIn("probability", prediction["horizons"]["1d"])
        self.assertNotIn("确定", prediction["summary"])


if __name__ == "__main__":
    unittest.main()
