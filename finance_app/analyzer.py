from typing import Iterable

from .config import HORIZON_WEIGHTS
from .models import EvidenceSource, HotDirection, Leader, MarketReport, utc_now_iso


def _document_text(document) -> str:
    if isinstance(document, dict):
        return f"{document.get('title', '')}\n{document.get('text', '')}"
    return str(document)


def _all_text(documents: Iterable) -> str:
    return "\n".join(_document_text(document) for document in documents).lower()


def _score_direction(direction: dict, documents: Iterable[str], horizon: str, index: int) -> int:
    text = _all_text(documents)
    keyword_hits = sum(text.count(keyword.lower()) for keyword in direction["keywords"])
    weights = HORIZON_WEIGHTS[horizon]
    base = max(0, 100 - index * 9)
    return base + keyword_hits * 12 + weights["freshness"] * 3 + weights["position"]


def _evidence(direction: dict, score: int, market_name: str) -> str:
    keywords = "、".join(direction["keywords"][:4])
    if score >= 125:
        return f"{market_name}公开信息中多次出现 {keywords} 等关键词，热度和产业关注度较高。"
    if score >= 110:
        return f"{market_name}公开信息中出现 {keywords} 等相关线索，可作为近期观察方向。"
    return f"该方向具备中期跟踪价值，但本轮抓取到的直接热度有限，需要继续验证。"


def _evidence_sources(direction: dict, documents: Iterable, limit: int = 3) -> list[EvidenceSource]:
    sources = []
    for document in documents:
        if not isinstance(document, dict):
            continue
        text = _document_text(document).lower()
        matched = [
            keyword
            for keyword in direction["keywords"]
            if keyword.lower() in text
        ]
        if matched:
            sources.append(
                EvidenceSource(
                    url=document.get("url", ""),
                    title=document.get("title", document.get("url", "")),
                    matched_keywords=matched[:6],
                    error=document.get("error"),
                )
            )
        if len(sources) >= limit:
            break
    return sources


def build_market_report(market_config: dict, documents: Iterable[str], market_code: str | None = None) -> MarketReport:
    horizons = {}
    for horizon in ("day", "week", "month"):
        scored = []
        for index, direction in enumerate(market_config["directions"]):
            score = _score_direction(direction, documents, horizon, index)
            leaders = [
                Leader(name=name, ticker=ticker, detail=detail)
                for name, ticker, detail in direction["leaders"]
            ]
            scored.append(
                HotDirection(
                    name=direction["name"],
                    score=score,
                    evidence=_evidence(direction, score, market_config["name"]),
                    risk=direction["risk"],
                    leaders=leaders,
                    evidence_sources=_evidence_sources(direction, documents),
                )
            )
        horizons[horizon] = sorted(scored, key=lambda item: item.score, reverse=True)[:5]

    return MarketReport(
        market=market_code or market_config["code"],
        market_name=market_config["name"],
        generated_at=utc_now_iso(),
        summary=market_config["summary"],
        sources=market_config["sources"],
        horizons=horizons,
    )
