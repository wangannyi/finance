import unittest

from finance_app.skill_pipeline import (
    ALL_FINANCE_SKILLS,
    PIPELINE_SLOTS,
    build_pipeline_status,
    get_slot_plan,
)


class SkillPipelineTests(unittest.TestCase):
    def test_slots_use_layered_skills_without_running_everything_each_time(self):
        self.assertEqual(set(PIPELINE_SLOTS), {"morning", "auction", "midday", "close", "us_premarket"})

        for slot_name in PIPELINE_SLOTS:
            with self.subTest(slot=slot_name):
                plan = get_slot_plan(slot_name)
                self.assertTrue(plan["time"])
                self.assertTrue(plan["output"])
                self.assertLess(len(plan["skills"]), len(ALL_FINANCE_SKILLS))

        self.assertEqual(
            get_slot_plan("morning")["skills"],
            [
                "alphaear-news",
                "alphaear-search",
                "alphaear-stock",
                "alphaear-sentiment",
                "alphaear-signal-tracker",
                "alphaear-reporter",
            ],
        )
        self.assertIn("alphaear-predictor", get_slot_plan("us_premarket")["skills"])
        self.assertTrue(get_slot_plan("us_premarket")["async_only"])

    def test_pipeline_status_reports_layers_and_installed_skills(self):
        status = build_pipeline_status()

        self.assertEqual(
            [layer["name"] for layer in status["layers"]],
            ["数据层", "判断层", "预测层", "表达层"],
        )
        self.assertEqual(len(status["all_skills"]), 9)
        self.assertEqual(status["slots"][0]["key"], "morning")
        self.assertEqual(status["slots"][0]["time"], "08:00")
        self.assertTrue(all("installed" in skill for layer in status["layers"] for skill in layer["skills"]))


if __name__ == "__main__":
    unittest.main()
