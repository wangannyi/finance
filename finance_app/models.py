from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Dict, List


@dataclass
class Leader:
    name: str
    ticker: str
    detail: str


@dataclass
class EvidenceSource:
    url: str
    title: str
    matched_keywords: List[str]
    error: str | None = None


@dataclass
class HotDirection:
    name: str
    score: int
    evidence: str
    risk: str
    leaders: List[Leader]
    challengers: List[Leader] = field(default_factory=list)
    evidence_sources: List[EvidenceSource] = field(default_factory=list)


@dataclass
class MarketReport:
    market: str
    market_name: str
    generated_at: str
    summary: str
    sources: List[str]
    horizons: Dict[str, List[HotDirection]]
    discovered_themes: List[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
