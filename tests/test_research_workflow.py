import unittest

from finance_app.analyzer import build_market_report
from finance_app.config import MARKET_CONFIGS
from finance_app.research_workflow import build_research_workflow


class ResearchWorkflowTests(unittest.TestCase):
    def test_builds_skill_backed_theme_tracking_from_reports(self):
        reports = [
            build_market_report(
                MARKET_CONFIGS["ch"],
                [
                    {
                        "url": "https://example.com/materials",
                        "title": "半导体材料走强",
                        "text": "电子特气 光刻胶 刻蚀材料 氟化工 半导体材料 多股活跃。",
                    }
                ],
            ).to_dict(),
            build_market_report(
                MARKET_CONFIGS["us"],
                [
                    {
                        "url": "https://example.com/cpo",
                        "title": "CPO and memory stocks attract AI infrastructure flows",
                        "text": "CPO optical transceiver HBM DRAM NAND memory Micron Coherent Lumentum.",
                    }
                ],
            ).to_dict(),
        ]

        workflow = build_research_workflow(reports)

        self.assertEqual(workflow["refresh_cadence"], "08:00 daily")
        self.assertEqual(
            [stage["name"] for stage in workflow["stages"]],
            ["发现", "核验", "跟踪", "成稿"],
        )
        self.assertIn("alphaear-news", workflow["stages"][0]["skills"])
        self.assertIn("alphaear-signal-tracker", workflow["stages"][2]["skills"])
        self.assertGreaterEqual(len(workflow["tracked_signals"]), 3)

        names = [signal["name"] for signal in workflow["tracked_signals"]]
        self.assertIn("电子特气/六氟化钨", names)
        self.assertIn("CPO/光通信", names)

        gas = next(signal for signal in workflow["tracked_signals"] if signal["name"] == "电子特气/六氟化钨")
        self.assertEqual(gas["market"], "ch")
        self.assertIn(gas["status"], {"增强", "观察", "待核验"})
        self.assertTrue(gas["next_action"])
        self.assertTrue(gas["evidence_sources"])


if __name__ == "__main__":
    unittest.main()
