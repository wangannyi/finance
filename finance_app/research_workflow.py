from collections import defaultdict
from typing import Iterable


STAGES = [
    {
        "name": "发现",
        "skills": ["alphaear-news", "alphaear-search", "alphaear-deepear-lite"],
        "output": "多源新闻、热榜和高频金融信号，生成候选主题。",
    },
    {
        "name": "核验",
        "skills": ["alphaear-search", "alphaear-stock"],
        "output": "补充来源链接、行情、估值和公司代码，过滤低置信标的。",
    },
    {
        "name": "跟踪",
        "skills": ["alphaear-sentiment", "alphaear-signal-tracker", "alphaear-predictor"],
        "output": "判断主题增强、观察或待核验，只输出情景和概率，不给确定买卖指令。",
    },
    {
        "name": "成稿",
        "skills": ["alphaear-reporter", "alphaear-logic-visualizer"],
        "output": "生成日报、证据链、风险清单和产业链逻辑图。",
    },
]

HORIZON_INTENSITY = {"day": 3, "week": 2, "month": 1}


def build_research_workflow(reports: list[dict], limit: int = 20) -> dict:
    signals = _tracked_signals(reports, limit)
    latest_update = max((report.get("generated_at", "") for report in reports), default="")
    return {
        "refresh_cadence": "08:00 daily",
        "latest_update": latest_update,
        "stages": STAGES,
        "tracked_signals": signals,
        "quality_rules": [
            "短线只看细分催化，不用大行业词替代。",
            "公司必须来自主题专属清单或可核验来源，不为凑数量补标的。",
            "无法交叉验证的行情和估值标为待核验。",
        ],
    }


def _tracked_signals(reports: list[dict], limit: int) -> list[dict]:
    grouped: dict[tuple[str, str], dict] = {}
    horizon_hits: dict[tuple[str, str], set[str]] = defaultdict(set)

    for report in reports:
        market = report.get("market", "")
        market_name = report.get("market_name", market)
        for horizon, directions in (report.get("horizons") or {}).items():
            for direction in directions or []:
                key = (market, direction.get("name", ""))
                if not key[1]:
                    continue
                horizon_hits[key].add(horizon)
                candidate = _direction_to_signal(market, market_name, horizon, direction)
                existing = grouped.get(key)
                if not existing or candidate["score"] > existing["score"]:
                    grouped[key] = candidate

        for theme in report.get("discovered_themes") or []:
            key = (market, theme.get("name", ""))
            if not key[1]:
                continue
            candidate = _discovered_to_signal(market, market_name, theme)
            existing = grouped.get(key)
            if not existing or candidate["score"] > existing["score"]:
                grouped[key] = candidate

    signals = []
    for key, signal in grouped.items():
        horizons = sorted(horizon_hits.get(key, set()), key=lambda item: -HORIZON_INTENSITY.get(item, 0))
        signal["horizons"] = horizons
        signal["status"] = _signal_status(signal, horizons)
        signal["next_action"] = _next_action(signal["status"])
        signals.append(signal)

    signals.sort(key=lambda item: (item["score"], len(item.get("evidence_sources", []))), reverse=True)
    return signals[:limit]


def _direction_to_signal(market: str, market_name: str, horizon: str, direction: dict) -> dict:
    return {
        "market": market,
        "market_name": market_name,
        "name": direction.get("name", ""),
        "score": int(direction.get("score") or 0),
        "primary_horizon": horizon,
        "risk": direction.get("risk", ""),
        "evidence": direction.get("evidence", ""),
        "evidence_sources": _normalize_sources(direction.get("evidence_sources", [])),
    }


def _discovered_to_signal(market: str, market_name: str, theme: dict) -> dict:
    return {
        "market": market,
        "market_name": market_name,
        "name": theme.get("name", ""),
        "score": int(theme.get("score") or 0),
        "primary_horizon": "discovered",
        "risk": theme.get("risk", ""),
        "evidence": "主动发现主题，需结合价格和公告继续核验。",
        "evidence_sources": _normalize_sources(theme.get("evidence_sources", [])),
    }


def _normalize_sources(sources: Iterable[dict]) -> list[dict]:
    return [
        {
            "url": source.get("url", ""),
            "title": source.get("title", source.get("url", "")),
            "matched_keywords": list(source.get("matched_keywords", []))[:6],
        }
        for source in sources or []
    ][:3]


def _signal_status(signal: dict, horizons: list[str]) -> str:
    if "day" in horizons and len(horizons) >= 2 and signal["evidence_sources"]:
        return "增强"
    if signal["score"] >= 80 or signal["evidence_sources"]:
        return "观察"
    return "待核验"


def _next_action(status: str) -> str:
    if status == "增强":
        return "优先核验龙头涨幅、估值位置和最新公告，避免高位追涨。"
    if status == "观察":
        return "加入观察池，等待成交量、新闻和公司详情确认。"
    return "先补证据源和公司基本面，暂不进入候选买入清单。"
