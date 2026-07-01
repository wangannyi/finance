import unittest

from finance_app.portfolio import build_default_portfolio_plan


class PortfolioPlanTests(unittest.TestCase):
    def test_builds_default_3_1_1_allocation_for_500k_capital(self):
        plan = build_default_portfolio_plan()

        self.assertEqual(plan["total_capital"], 500000)
        self.assertEqual(plan["markets"]["ch"]["target_amount"], 300000)
        self.assertEqual(plan["markets"]["hk"]["target_amount"], 100000)
        self.assertEqual(plan["markets"]["us"]["target_amount"], 100000)

    def test_includes_beginner_risk_guardrails(self):
        plan = build_default_portfolio_plan()

        self.assertEqual(plan["guardrails"]["max_single_position_amount"], 25000)
        self.assertEqual(plan["guardrails"]["max_theme_amount"], 75000)
        self.assertEqual(plan["guardrails"]["suggested_batches"], 4)
        self.assertTrue(plan["questions"])


if __name__ == "__main__":
    unittest.main()
