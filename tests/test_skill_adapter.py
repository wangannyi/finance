import unittest

from finance_app.skill_adapter import _skill_code, execute_skill_adapter, run_slot_skill_adapters
from finance_app.skill_pipeline import get_slot_plan


class SkillAdapterTests(unittest.TestCase):
    def test_runs_only_slot_skills_and_records_results(self):
        calls = []

        def fake_executor(skill, context):
            calls.append(skill)
            return {"status": "ok", "summary": f"ran {skill}", "items": []}

        plan = get_slot_plan("auction")
        results = run_slot_skill_adapters(plan, {"symbols": ["000021.SZ"]}, executor=fake_executor)

        self.assertEqual(calls, ["alphaear-stock", "alphaear-news", "alphaear-sentiment"])
        self.assertEqual([item["skill"] for item in results], calls)
        self.assertTrue(all(item["status"] == "ok" for item in results))

    def test_predictor_is_queued_async_in_us_premarket(self):
        calls = []

        def fake_executor(skill, context):
            calls.append(skill)
            return {"status": "ok", "summary": f"ran {skill}", "items": []}

        plan = get_slot_plan("us_premarket")
        results = run_slot_skill_adapters(plan, {"symbols": ["MU", "NVDA", "000021.SZ"]}, executor=fake_executor)

        predictor = next(item for item in results if item["skill"] == "alphaear-predictor")
        self.assertEqual(predictor["status"], "queued_async")
        self.assertEqual(predictor["symbols"], ["MU", "NVDA", "000021.SZ"])
        self.assertNotIn("alphaear-predictor", calls)

    def test_news_adapter_uses_fast_direct_requests_for_intraday_slots(self):
        code = _skill_code("alphaear-news", {"slot": "us_premarket"})

        self.assertIn("newsnow.busiyi.world", code)
        self.assertIn("timeout=6", code)
        self.assertNotIn("NewsNowTools", code)

    def test_search_adapter_uses_lightweight_search_without_local_rag_model_import(self):
        code = _skill_code("alphaear-search", {"slot": "morning", "signals": [{"name": "CPO"}]})

        self.assertIn("DDGS", code)
        self.assertNotIn("SearchTools", code)
        self.assertNotIn("sentence_transformers", code)

    def test_execute_adapter_converts_subprocess_timeout_to_degraded_result(self):
        result = execute_skill_adapter("alphaear-search", {"signals": [{"name": "CPO 光通信"}]}, timeout_seconds=0.001)

        self.assertEqual(result["status"], "degraded")
        self.assertIn("timed out", result["summary"])


if __name__ == "__main__":
    unittest.main()
