from .research_workflow import build_research_workflow


DEFAULT_HOLDINGS = [
    {"name": "士兰微", "symbol": "600460.SH", "cost": 50.701, "shares": 500},
    {"name": "深科技", "symbol": "000021.SZ", "cost": 55.010, "shares": 500},
    {"name": "美的集团", "symbol": "000333.SZ", "cost": 78.017, "shares": 300},
    {"name": "通富微电", "symbol": "002156.SZ", "cost": 72.611, "shares": 500},
]


def build_intraday_brief(reports: list[dict], holdings: list[dict] | None = None) -> dict:
    workflow = build_research_workflow(reports, limit=20)
    signals = workflow["tracked_signals"]
    holdings = holdings or DEFAULT_HOLDINGS
    return {
        "radar": _radar(signals),
        "holdings": _holding_reviews(holdings, signals),
        "signals": signals[:10],
        "predictions": _predictions(signals),
        "logic_chains": _logic_chains(signals),
    }


def _radar(signals: list[dict]) -> list[dict]:
    strengthened = [signal for signal in signals if signal["status"] == "增强"]
    observed = [signal for signal in signals if signal["status"] == "观察"]
    unverified = [signal for signal in signals if signal["status"] == "待核验"]
    return [
        {
            "name": "低位埋伏",
            "items": _theme_names([signal for signal in observed if _is_low_position_candidate(signal)], 4),
            "rule": "只看有证据但尚未过热的细分题材，等待回踩和成交量确认。",
        },
        {
            "name": "强势接力",
            "items": _theme_names(strengthened, 4),
            "rule": "只适合小仓跟踪，必须核验龙头涨幅和估值位置。",
        },
        {
            "name": "风险释放",
            "items": _theme_names([signal for signal in observed if _is_high_volatility(signal)], 4),
            "rule": "高波动主题先看是否缩量止跌，不把第一根反弹当反转。",
        },
        {
            "name": "不能碰",
            "items": _theme_names(unverified, 4),
            "rule": "证据不足或逻辑未确认，暂不进入买入清单。",
        },
    ]


def _holding_reviews(holdings: list[dict], signals: list[dict]) -> list[dict]:
    signal_text = " ".join(signal["name"] + " " + signal.get("evidence", "") for signal in signals)
    reviews = []
    for holding in holdings:
        themes = _matched_holding_themes(holding, signals, signal_text)
        action = _holding_action(holding, themes)
        stop_loss = _holding_stop_loss(holding, action)
        reviews.append(
            {
                **holding,
                "action": action,
                "themes": themes[:3],
                "stop_loss": stop_loss,
                "trigger": _holding_trigger(action, themes, stop_loss),
                "reason": _holding_reason(action, themes),
                "checks": [
                    "先核验今日成交量、分时承接和板块强弱。",
                    "若跌破个人止损线或主题被证伪，优先降低仓位。",
                    "若继续持有，不追加到单标的上限以上。",
                ],
            }
        )
    return reviews


def _predictions(signals: list[dict]) -> list[dict]:
    predictions = []
    for signal in signals[:8]:
        base = min(max(signal["score"] / 100, 0.35), 0.68)
        if signal["status"] == "增强":
            base = min(base + 0.08, 0.72)
        if signal["status"] == "待核验":
            base = max(base - 0.08, 0.3)
        predictions.append(
            {
                "name": signal["name"],
                "market_name": signal["market_name"],
                "summary": "异步预测待接入，仅展示概率区间和观察方向。",
                "horizons": {
                    "1d": {"probability": round(base, 2), "bias": _bias(base)},
                    "3d": {"probability": round(max(base - 0.04, 0.28), 2), "bias": _bias(base - 0.04)},
                    "5d": {"probability": round(max(base - 0.07, 0.25), 2), "bias": _bias(base - 0.07)},
                },
                "source": "alphaear-predictor async queue pending",
            }
        )
    return predictions


def _logic_chains(signals: list[dict]) -> list[dict]:
    chains = []
    for signal in signals[:6]:
        source = signal["evidence_sources"][0]["title"] if signal.get("evidence_sources") else signal["name"]
        chains.append(
            {
                "name": signal["name"],
                "chain": [
                    source,
                    f"{signal['name']} 主题热度变化",
                    "映射到相关龙头和高弹性标的",
                    "结合估值、成交量和公告决定留/减/观察",
                ],
                "tool": "alphaear-logic-visualizer",
            }
        )
    return chains


def _theme_names(signals: list[dict], limit: int) -> list[str]:
    return [signal["name"] for signal in signals[:limit]]


def _is_low_position_candidate(signal: dict) -> bool:
    return signal["score"] < 180 or "材料" in signal["name"] or "光刻胶" in signal["name"]


def _is_high_volatility(signal: dict) -> bool:
    text = signal["name"]
    return any(keyword in text for keyword in ["CPO", "存储", "半导体", "AI", "光刻胶", "刻蚀", "电子特气"])


def _matched_holding_themes(holding: dict, signals: list[dict], signal_text: str) -> list[str]:
    name = holding["name"]
    symbol = holding["symbol"]
    if name == "美的集团":
        keywords = ["机器人", "消费", "AI 终端"]
    elif name == "深科技":
        keywords = ["存储", "HBM", "先进封装"]
    elif name == "通富微电":
        keywords = ["先进封装", "半导体", "存储"]
    elif name == "士兰微":
        keywords = ["半导体", "功率", "模拟"]
    else:
        keywords = [name, symbol]
    matched = [signal["name"] for signal in signals if any(keyword in signal["name"] or keyword in signal.get("evidence", "") for keyword in keywords)]
    if not matched and any(keyword in signal_text for keyword in keywords):
        matched = keywords[:1]
    return matched


def _holding_action(holding: dict, themes: list[str]) -> str:
    if not themes:
        return "观察"
    if holding["name"] == "美的集团":
        return "留"
    if any(any(keyword in theme for keyword in ["存储", "CPO", "半导体"]) for theme in themes):
        return "减"
    return "观察"


def _holding_stop_loss(holding: dict, action: str) -> float:
    buffer = 0.95 if action == "留" else 0.92
    return round(holding["cost"] * buffer, 3)


def _holding_trigger(action: str, themes: list[str], stop_loss: float) -> str:
    if action == "留":
        return f"跌破 {stop_loss} 或基本面公告转弱再减仓。"
    if action == "减":
        theme_text = " / ".join(themes[:2]) or "关联题材"
        return f"{theme_text} 放量转弱或跌破 {stop_loss}，优先降仓。"
    if action == "清":
        return f"跌破 {stop_loss} 且主题被证伪时执行。"
    return f"站稳成本线并出现板块放量确认，否则跌破 {stop_loss} 控制风险。"


def _holding_reason(action: str, themes: list[str]) -> str:
    if action == "留":
        return "基本面属性更强，按中线仓位观察，不按短线题材频繁处理。"
    if action == "减":
        return f"关联 {(' / '.join(themes[:2]) or '高波动主题')}，先控制回撤，再等信号重新强化。"
    if action == "清":
        return "主题被证伪或跌破纪律线时执行。"
    return "主题证据不足，先观察成交量和公告。"


def _bias(probability: float) -> str:
    if probability >= 0.6:
        return "偏强"
    if probability <= 0.42:
        return "偏弱"
    return "震荡"
