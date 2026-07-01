from typing import Iterable

from .config import HORIZON_WEIGHTS
from .models import EvidenceSource, HotDirection, Leader, MarketReport, utc_now_iso
from .theme_discovery import PROACTIVE_THEMES, discover_themes


COMPANY_POOLS = {
    "ch": {
        "leaders": [
            ("中际旭创", "300308.SZ", "AI 光模块龙头。"),
            ("新易盛", "300502.SZ", "高速光模块代表。"),
            ("北方华创", "002371.SZ", "半导体设备平台型龙头。"),
            ("中微公司", "688012.SH", "刻蚀设备代表。"),
            ("恒瑞医药", "600276.SH", "创新药平台型龙头。"),
            ("长江电力", "600900.SH", "水电红利核心资产。"),
            ("汇川技术", "300124.SZ", "工控和伺服龙头。"),
            ("沪电股份", "002463.SZ", "AI 服务器 PCB 代表。"),
            ("兆易创新", "603986.SH", "存储芯片设计代表。"),
            ("澜起科技", "688008.SH", "内存接口芯片龙头。"),
        ],
        "challengers": [
            ("胜宏科技", "300476.SZ", "高端 PCB 和算力链弹性标的。"),
            ("天孚通信", "300394.SZ", "光器件平台型公司。"),
            ("圣邦股份", "300661.SZ", "模拟芯片代表。"),
            ("江波龙", "301308.SZ", "存储模组代表。"),
            ("绿的谐波", "688017.SH", "机器人减速器弹性标的。"),
            ("三环集团", "300408.SZ", "MLCC 和电子陶瓷代表。"),
            ("扬杰科技", "300373.SZ", "功率器件代表。"),
            ("华海清科", "688120.SH", "CMP 设备代表。"),
            ("生益科技", "600183.SH", "覆铜板材料代表。"),
            ("埃斯顿", "002747.SZ", "工业机器人整机代表。"),
        ],
    },
    "hk": {
        "leaders": [
            ("腾讯控股", "0700.HK", "互联网平台和 AI 应用龙头。"),
            ("阿里巴巴-W", "9988.HK", "电商、云和 AI 平台龙头。"),
            ("中国移动", "0941.HK", "港股高股息核心标的。"),
            ("中国海洋石油", "0883.HK", "能源高股息代表。"),
            ("香港交易所", "0388.HK", "港股融资和交易活跃度核心标的。"),
            ("中芯国际", "0981.HK", "晶圆制造核心公司。"),
            ("百济神州", "6160.HK", "全球化创新药龙头。"),
            ("美团-W", "3690.HK", "本地生活平台龙头。"),
            ("汇丰控股", "0005.HK", "金融高股息代表。"),
            ("华虹半导体", "1347.HK", "特色工艺晶圆代工代表。"),
        ],
        "challengers": [
            ("商汤-W", "0020.HK", "AI 软件和模型应用弹性标的。"),
            ("康方生物", "9926.HK", "双抗和 BD 催化代表。"),
            ("信达生物", "1801.HK", "创新药商业化代表。"),
            ("ASMPT", "0522.HK", "封装设备代表。"),
            ("华泰证券", "6886.HK", "中资券商弹性标的。"),
            ("中信证券", "6030.HK", "投行业务龙头映射。"),
            ("携程集团-S", "9961.HK", "出行消费修复代表。"),
            ("安踏体育", "2020.HK", "运动消费龙头。"),
            ("中国神华", "1088.HK", "煤炭高股息代表。"),
            ("小米集团-W", "1810.HK", "AI 终端和硬件生态代表。"),
        ],
    },
    "us": {
        "leaders": [
            ("NVIDIA", "NVDA", "AI 加速计算龙头。"),
            ("Microsoft", "MSFT", "云计算和 AI 应用平台龙头。"),
            ("Broadcom", "AVGO", "AI 网络和定制芯片代表。"),
            ("Micron Technology", "MU", "HBM 和存储周期核心。"),
            ("Coherent", "COHR", "AI 数据中心光器件代表。"),
            ("Constellation Energy", "CEG", "核电和 AI 电力代表。"),
            ("JPMorgan Chase", "JPM", "大型银行龙头。"),
            ("Apple", "AAPL", "消费电子和生态平台龙头。"),
            ("Alphabet", "GOOGL", "搜索、广告和 AI 平台。"),
            ("GE Vernova", "GEV", "电网和电力设备代表。"),
        ],
        "challengers": [
            ("Lumentum", "LITE", "光器件和激光器弹性标的。"),
            ("Marvell Technology", "MRVL", "AI 互联芯片代表。"),
            ("SanDisk", "SNDK", "NAND/SSD 弹性标的。"),
            ("Western Digital", "WDC", "数据中心存储代表。"),
            ("Vistra", "VST", "电力容量市场代表。"),
            ("Rocket Lab", "RKLB", "商业航天弹性标的。"),
            ("Palantir", "PLTR", "国防和商业 AI 软件代表。"),
            ("Coinbase", "COIN", "加密基础设施代表。"),
            ("Robinhood", "HOOD", "零售交易和加密业务代表。"),
            ("Circle", "CRCL", "稳定币相关代表。"),
        ],
    },
}

EXTRA_DIRECTIONS = {
    "ch": [
        {
            "name": "业绩预告/中报超预期",
            "keywords": ["中报", "业绩预告", "预增", "超预期", "利润"],
            "risk": "业绩披露期容易出现兑现和预期差波动。",
        },
        {
            "name": "资金流/成交放大",
            "keywords": ["资金流入", "主力资金", "成交额", "放量", "换手"],
            "risk": "资金驱动持续性弱，需防范快速轮动。",
        },
    ],
    "hk": [
        {
            "name": "南向资金加仓",
            "keywords": ["南向资金", "港股通", "加仓", "成交", "净买入"],
            "risk": "南向资金风格切换会影响短期表现。",
        },
        {
            "name": "回购与估值修复",
            "keywords": ["回购", "buyback", "估值修复", "低估值", "净买入"],
            "risk": "回购不等于基本面反转，需验证盈利趋势。",
        },
    ],
    "us": [
        {
            "name": "财报超预期交易",
            "keywords": ["earnings", "guidance", "beat", "revenue", "margin"],
            "risk": "财报后波动大，指引变化会快速改变估值。",
        },
        {
            "name": "ETF资金流入",
            "keywords": ["ETF", "inflows", "fund flows", "sector ETF", "volume"],
            "risk": "ETF 流入可能放大趋势，也可能快速反转。",
        },
    ],
}


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


def _directions_for_horizon(market_config: dict, horizon: str) -> list[dict]:
    directions = list(market_config.get("horizon_directions", {}).get(horizon) or market_config["directions"])
    market = market_config["code"]
    seen = {item["name"] for item in directions}
    for theme in PROACTIVE_THEMES.get(market, []):
        if theme["name"] in seen:
            continue
        directions.append(
            {
                "name": theme["name"],
                "keywords": theme["keywords"],
                "risk": theme["risk"],
                "leaders": [],
                "challengers": [],
            }
        )
        seen.add(theme["name"])
        if len(directions) >= 10:
            break
    for extra in EXTRA_DIRECTIONS.get(market, []):
        if len(directions) >= 10:
            break
        if extra["name"] in seen:
            continue
        directions.append({**extra, "leaders": [], "challengers": []})
        seen.add(extra["name"])
    return directions


def _company_group(market: str, direction: dict, group: str, exclude: set[str] | None = None) -> list[Leader]:
    configured = direction.get(group, [])
    pool = COMPANY_POOLS.get(market, {}).get(group, [])
    companies = []
    seen = set(exclude or set())
    for item in [*configured, *pool]:
        name, ticker, detail = item
        if ticker in seen:
            continue
        companies.append(Leader(name=name, ticker=ticker, detail=detail))
        seen.add(ticker)
        if len(companies) >= 5:
            break
    return companies


def build_market_report(market_config: dict, documents: Iterable[str], market_code: str | None = None) -> MarketReport:
    documents = list(documents)
    market = market_code or market_config["code"]
    horizons = {}
    for horizon in ("day", "week", "month"):
        scored = []
        for index, direction in enumerate(_directions_for_horizon(market_config, horizon)):
            score = _score_direction(direction, documents, horizon, index)
            leaders = _company_group(market, direction, "leaders")
            scored.append(
                HotDirection(
                    name=direction["name"],
                    score=score,
                    evidence=_evidence(direction, score, market_config["name"]),
                    risk=direction["risk"],
                    leaders=leaders,
                    challengers=_company_group(market, direction, "challengers", {leader.ticker for leader in leaders}),
                    evidence_sources=_evidence_sources(direction, documents),
                )
            )
        horizons[horizon] = sorted(scored, key=lambda item: item.score, reverse=True)[:10]

    return MarketReport(
        market=market,
        market_name=market_config["name"],
        generated_at=utc_now_iso(),
        summary=market_config["summary"],
        sources=market_config["sources"],
        horizons=horizons,
        discovered_themes=discover_themes(market_code or market_config["code"], documents),
    )
