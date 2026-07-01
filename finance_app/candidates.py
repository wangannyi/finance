HORIZON_LABELS = {
    "day": "接下来一天",
    "week": "接下来一周",
    "month": "接下来一个月",
}


def build_candidate_pool(reports: list[dict], portfolio_plan: dict) -> dict:
    candidates_by_symbol: dict[str, dict] = {}
    guardrails = portfolio_plan["guardrails"]

    for report in reports:
        market = report["market"]
        market_plan = portfolio_plan["markets"].get(market, {})
        for horizon, directions in report.get("horizons", {}).items():
            for direction in directions:
                for leader in direction.get("leaders", []):
                    symbol = leader["ticker"]
                    candidate = candidates_by_symbol.setdefault(
                        symbol,
                        {
                            "symbol": symbol,
                            "name": leader["name"],
                            "market": market,
                            "market_name": report["market_name"],
                            "market_target_amount": market_plan.get("target_amount", 0),
                            "themes": [],
                            "horizons": [],
                            "max_score": 0,
                            "leader_detail": leader["detail"],
                            "max_observation_amount": guardrails["max_single_position_amount"],
                            "action": "观察",
                            "risk_tags": [],
                            "pre_trade_checks": [],
                        },
                    )
                    _append_unique(candidate["themes"], direction["name"])
                    _append_unique(candidate["horizons"], HORIZON_LABELS.get(horizon, horizon))
                    candidate["max_score"] = max(candidate["max_score"], direction["score"])

    candidates = []
    for candidate in candidates_by_symbol.values():
        candidate["risk_tags"] = _risk_tags(candidate)
        candidate["action"] = _action(candidate)
        candidate["pre_trade_checks"] = _pre_trade_checks(candidate)
        candidates.append(candidate)

    candidates.sort(key=lambda item: (item["max_score"], len(item["themes"])), reverse=True)
    return {
        "limits": {
            "max_single_position_amount": guardrails["max_single_position_amount"],
            "max_theme_amount": guardrails["max_theme_amount"],
            "suggested_batches": guardrails["suggested_batches"],
        },
        "candidates": candidates,
    }


def _append_unique(items: list, value: str) -> None:
    if value not in items:
        items.append(value)


def _risk_tags(candidate: dict) -> list[str]:
    tags = []
    themes = " ".join(candidate["themes"])
    if candidate["max_score"] >= 125:
        tags.append("热度高")
    if any(keyword in themes for keyword in ["AI", "半导体", "机器人", "创新药", "CPO", "光通信", "存储", "HBM"]):
        tags.append("高波动")
    if candidate["market"] in {"hk", "us"}:
        tags.append("汇率风险")
    if len(candidate["themes"]) >= 3:
        tags.append("多主题重叠")
    return tags or ["常规跟踪"]


def _action(candidate: dict) -> str:
    if "高波动" in candidate["risk_tags"] and candidate["max_score"] >= 125:
        return "等待回调"
    if candidate["max_score"] < 100:
        return "暂不参与"
    return "观察"


def _pre_trade_checks(candidate: dict) -> list[str]:
    return [
        f"单标的观察仓不超过 {candidate['max_observation_amount']} 元。",
        "先核验最近一期财报、公告和估值是否匹配。",
        "确认所属主题没有超过总本金 15%。",
        "若价格已连续大涨，优先等待回调或分批观察。",
    ]
