import unittest

from finance_app.analyzer import build_market_report
from finance_app.candidates import build_candidate_pool
from finance_app.config import MARKET_CONFIGS
from finance_app.portfolio import build_default_portfolio_plan


class CandidatePoolTests(unittest.TestCase):
    def test_builds_unique_candidates_from_latest_reports(self):
        reports = [
            build_market_report(MARKET_CONFIGS["ch"], ["AI 算力 半导体 创新药"]).to_dict(),
            build_market_report(MARKET_CONFIGS["us"], ["AI semiconductor ETF"]).to_dict(),
        ]
        plan = build_default_portfolio_plan()

        pool = build_candidate_pool(reports, plan)

        symbols = [item["symbol"] for item in pool["candidates"]]
        self.assertIn("300308.SZ", symbols)
        self.assertIn("NVDA", symbols)
        self.assertEqual(len(symbols), len(set(symbols)))

    def test_candidates_include_guardrails_and_no_buy_instruction(self):
        reports = [build_market_report(MARKET_CONFIGS["ch"], ["AI 算力 半导体"]).to_dict()]
        plan = build_default_portfolio_plan()

        pool = build_candidate_pool(reports, plan)
        first = pool["candidates"][0]

        self.assertEqual(first["max_observation_amount"], 25000)
        self.assertIn(first["action"], {"观察", "等待回调", "暂不参与"})
        self.assertNotEqual(first["action"], "买入")
        self.assertTrue(first["pre_trade_checks"])
        self.assertEqual(pool["limits"]["max_single_position_amount"], 25000)


if __name__ == "__main__":
    unittest.main()
