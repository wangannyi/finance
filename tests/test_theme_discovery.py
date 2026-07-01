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

    def test_discovers_broader_current_theme_radar(self):
        documents = [
            {
                "url": "https://example.com/themes",
                "title": "AI infrastructure, defense and tokenization shape markets",
                "text": "Infrastructure, defense, tokenization, stablecoins, nuclear energy, humanoid robotics, gold and silver miners are attracting flows.",
                "error": None,
            }
        ]

        names = [theme["name"] for theme in discover_themes("us", documents)]

        self.assertIn("国防/航天", names)
        self.assertIn("稳定币/代币化", names)
        self.assertIn("贵金属/矿业", names)

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

    def test_discovers_a_share_hot_chip_supply_chain_themes(self):
        documents = [
            {
                "url": "https://example.com/a-share-hot",
                "title": "A股热炒题材：CPO、PCB、存储芯片与模拟功率半导体涨价",
                "text": "CPO概念、PCB概念、光模块、硅光、AI服务器、模拟芯片、功率半导体和MLCC涨价潮继续吸引资金关注。",
                "error": None,
            }
        ]

        names = [theme["name"] for theme in discover_themes("ch", documents)]

        self.assertIn("AI光互联/CPO光模块", names)
        self.assertIn("AI服务器PCB/玻璃基板", names)
        self.assertIn("模拟/功率半导体", names)

    def test_discovers_a_share_semiconductor_material_micro_themes(self):
        documents = [
            {
                "url": "https://www.cls.cn/detail/2411836",
                "title": "半导体材料持续强势，电子特气、光刻胶方向活跃",
                "text": "电子特气 六氟化钨 光刻胶 湿电子化学品 刻蚀材料 氟化工 含氟电子材料 靶材 半导体硅片 资金关注。",
                "error": None,
            }
        ]

        names = [theme["name"] for theme in discover_themes("ch", documents)]

        self.assertIn("电子特气/六氟化钨", names)
        self.assertIn("光刻胶/湿电子化学品", names)
        self.assertIn("刻蚀材料/设备", names)
        self.assertIn("氟化工/含氟电子材料", names)

    def test_discovers_hk_ai_fundraising_theme(self):
        documents = [
            {
                "url": "https://example.com/hk",
                "title": "Hong Kong share sales hit five-year high as AI boom fuels fundraising",
                "text": "Hong Kong equity capital markets raised nearly $44 billion as artificial intelligence-related companies attracted investor demand.",
                "error": None,
            }
        ]

        themes = discover_themes("hk", documents)
        names = [theme["name"] for theme in themes]

        self.assertIn("AI软件/云服务", names)


if __name__ == "__main__":
    unittest.main()
