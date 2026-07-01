from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Dict, List


@dataclass
class Leader:
    name: str
    ticker: str
    detail: str


@dataclass
class HotDirection:
    name: str
    score: int
    evidence: str
    risk: str
    leaders: List[Leader]


@dataclass
class MarketReport:
    market: str
    market_name: str
    generated_at: str
    summary: str
    sources: List[str]
    horizons: Dict[str, List[HotDirection]]

    def to_dict(self) -> dict:
        return asdict(self)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
