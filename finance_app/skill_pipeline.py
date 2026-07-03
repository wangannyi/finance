from pathlib import Path


CODEX_SKILLS_DIR = Path.home() / ".codex" / "skills"

SKILL_LAYERS = [
    {
        "name": "数据层",
        "purpose": "抓新闻、全网补证据、拉行情和基本面。",
        "skills": ["alphaear-news", "alphaear-search", "alphaear-stock"],
    },
    {
        "name": "判断层",
        "purpose": "给文本打情绪分，判断主题强化、弱化或证伪，并参考外部高频信号。",
        "skills": ["alphaear-sentiment", "alphaear-signal-tracker", "alphaear-deepear-lite"],
    },
    {
        "name": "预测层",
        "purpose": "只对重点股票异步跑 1 日、3 日、5 日概率预测，不阻塞网站刷新。",
        "skills": ["alphaear-predictor"],
    },
    {
        "name": "表达层",
        "purpose": "生成日报、持仓去留、短线机会报告和涨跌传导链。",
        "skills": ["alphaear-logic-visualizer", "alphaear-reporter"],
    },
]

ALL_FINANCE_SKILLS = [skill for layer in SKILL_LAYERS for skill in layer["skills"]]

PIPELINE_SLOTS = {
    "morning": {
        "time": "08:00",
        "title": "全市场晨报",
        "skills": [
            "alphaear-news",
            "alphaear-search",
            "alphaear-stock",
            "alphaear-sentiment",
            "alphaear-signal-tracker",
            "alphaear-reporter",
        ],
        "output": "A 股/港股/美股热点、持仓风险、今日观察票。",
    },
    "auction": {
        "time": "09:25",
        "title": "A 股竞价快照",
        "skills": ["alphaear-stock", "alphaear-news", "alphaear-sentiment"],
        "output": "是否高开低走、是否需要减仓或暂停追高。",
    },
    "midday": {
        "time": "11:40",
        "title": "午间复盘",
        "skills": ["alphaear-signal-tracker", "alphaear-reporter"],
        "output": "上午热点是否强化，哪些主题转弱。",
    },
    "close": {
        "time": "15:15",
        "title": "收盘复盘",
        "skills": ["alphaear-stock", "alphaear-signal-tracker", "alphaear-logic-visualizer", "alphaear-reporter"],
        "output": "今天为什么涨跌、明天重点、上涨/下跌传导链。",
    },
    "us_premarket": {
        "time": "21:00",
        "title": "美股盘前",
        "skills": ["alphaear-news", "alphaear-stock", "alphaear-sentiment", "alphaear-predictor"],
        "output": "今晚美股方向、对明天 A 股的映射。",
        "async_only": True,
    },
}


def get_slot_plan(slot_name: str) -> dict:
    if slot_name not in PIPELINE_SLOTS:
        raise KeyError(f"unknown pipeline slot: {slot_name}")
    plan = dict(PIPELINE_SLOTS[slot_name])
    plan["key"] = slot_name
    plan.setdefault("async_only", False)
    plan["layers"] = _layers_for_skills(plan["skills"])
    return plan


def build_pipeline_status() -> dict:
    return {
        "all_skills": ALL_FINANCE_SKILLS,
        "layers": [
            {
                **layer,
                "skills": [_skill_status(skill) for skill in layer["skills"]],
            }
            for layer in SKILL_LAYERS
        ],
        "slots": [get_slot_plan(slot_name) for slot_name in PIPELINE_SLOTS],
        "rules": [
            "任一时点只跑该时点需要的 skill，不全量跑 9 个。",
            "alphaear-predictor 只对重点股票异步运行，不阻塞页面刷新。",
            "所有输出都必须保留来源、时间和待核验标记。",
        ],
    }


def _skill_status(skill: str) -> dict:
    path = CODEX_SKILLS_DIR / skill / "SKILL.md"
    return {
        "name": skill,
        "installed": path.exists(),
        "path": str(path) if path.exists() else "",
    }


def _layers_for_skills(skills: list[str]) -> list[str]:
    layers = []
    for layer in SKILL_LAYERS:
        if any(skill in layer["skills"] for skill in skills):
            layers.append(layer["name"])
    return layers
