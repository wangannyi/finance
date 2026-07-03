import unittest

from finance_app.pipeline_runner import run_pipeline_slot
from finance_app.storage import ReportStore


class PipelineRunnerTests(unittest.TestCase):
    def test_runner_saves_slot_output_without_requiring_all_skills(self):
        store = ReportStore(":memory:")
        result = run_pipeline_slot("auction", store=store)

        self.assertEqual(result["slot"], "auction")
        self.assertEqual(result["time"], "09:25")
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["skills"], ["alphaear-stock", "alphaear-news", "alphaear-sentiment"])
        self.assertLess(len(result["skills"]), 9)

        runs = store.get_pipeline_runs(limit=1)
        self.assertEqual(runs[0]["slot"], "auction")
        self.assertEqual(runs[0]["payload"]["title"], "A 股竞价快照")

    def test_runner_can_persist_skill_execution_results(self):
        store = ReportStore(":memory:")

        def fake_executor(skill, context):
            return {"status": "ok", "summary": f"ran {skill}", "items": []}

        result = run_pipeline_slot("auction", store=store, execute_skills=True, skill_executor=fake_executor)

        self.assertEqual([item["skill"] for item in result["skill_results"]], result["skills"])
        self.assertTrue(all(item["status"] == "ok" for item in result["skill_results"]))
        self.assertEqual(store.get_pipeline_runs(limit=1)[0]["payload"]["skill_results"][0]["summary"], "ran alphaear-stock")

    def test_morning_runner_does_not_block_on_company_preload_by_default(self):
        store = ReportStore(":memory:")
        reports = [
            {
                "market": "ch",
                "market_name": "A 股",
                "generated_at": "2026-07-03T00:00:00+00:00",
                "horizons": {"day": [], "week": [], "month": []},
                "discovered_themes": [],
            }
        ]

        result = run_pipeline_slot("morning", store=store, report_runner=lambda db_path: reports)

        self.assertEqual(result["preload"]["status"], "skipped_async")


if __name__ == "__main__":
    unittest.main()
