import unittest

from finance_app.theme_discovery import discover_themes


class ThemeDiscoveryTests(unittest.TestCase):
    def test_discovers_us_emerging_themes_from_documents(self):
        documents = [
            {
                "url": "https://example.com/quantum",
                "title": "Quantum computing stocks surge after new policy support",
                "text": "IonQ Rigetti D-Wave quantum computing stocks rallied after executive orders.",
                "error": None,
            },
            {
                "url": "https://example.com/power",
                "title": "AI power demand lifts nuclear and grid stocks",
                "text": "AI data centers need nuclear power, grid equipment, utilities and energy infrastructure.",
                "error": None,
            },
        ]

        themes = discover_themes("us", documents)
        names = [theme["name"] for theme in themes]

        self.assertIn("量子计算", names)
        self.assertIn("AI 电力/核能", names)
        self.assertTrue(themes[0]["evidence_sources"])

    def test_discovers_chinese_market_themes(self):
        documents = [
            {
                "url": "https://example.com/a",
                "title": "固态电池与商业航天概念活跃",
                "text": "固态电池 商业航天 低空经济 人形机器人 存储芯片 CPO",
                "error": None,
            }
        ]

        themes = discover_themes("ch", documents)
        names = [theme["name"] for theme in themes]

        self.assertIn("固态电池", names)
        self.assertIn("商业航天/低空经济", names)


if __name__ == "__main__":
    unittest.main()
