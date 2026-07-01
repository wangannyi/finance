PROACTIVE_THEMES = {
    "us": [
        {
            "name": "AI 电力/核能",
            "keywords": ["AI power", "nuclear", "grid", "utilities", "energy infrastructure", "data center power"],
            "risk": "电力和核能链条受政策、利率、项目周期和估值波动影响较大。",
        },
        {
            "name": "量子计算",
            "keywords": ["quantum", "IonQ", "Rigetti", "D-Wave", "Quantum Computing", "QUBT"],
            "risk": "商业化早期，估值高度依赖预期，波动和回撤可能很大。",
        },
        {
            "name": "Physical AI/工业自动化",
            "keywords": ["Physical AI", "industrial automation", "factory AI", "robotics", "Vertiv", "Eaton", "Honeywell"],
            "risk": "订单兑现节奏和制造业资本开支会影响短期表现。",
        },
        {
            "name": "国防/航天",
            "keywords": ["defense", "defense tech", "aerospace", "space", "SpaceX", "satellite", "military"],
            "risk": "政策预算、估值和项目交付节奏会带来较大不确定性。",
        },
        {
            "name": "稳定币/代币化",
            "keywords": ["stablecoin", "stablecoins", "tokenization", "crypto treasury", "digital assets", "blockchain"],
            "risk": "监管变化、流动性和加密资产价格波动会显著影响相关标的。",
        },
        {
            "name": "贵金属/矿业",
            "keywords": ["gold", "silver", "miners", "gold miners", "silver miners", "precious metals"],
            "risk": "贵金属价格、实际利率和美元走势会影响主题表现。",
        },
        {
            "name": "关键矿产/稀土",
            "keywords": ["rare earth", "critical minerals", "strategic metals", "lithium", "copper", "uranium"],
            "risk": "商品价格和政策扰动较大，周期属性强。",
        },
        {
            "name": "AI 存储/HBM",
            "keywords": ["HBM", "DRAM", "NAND", "memory", "SSD", "Micron", "SanDisk", "Western Digital"],
            "risk": "存储周期反转时，盈利和估值可能同步下修。",
        },
        {
            "name": "CPO/光通信",
            "keywords": ["CPO", "co-packaged optics", "optical transceiver", "silicon photonics", "Coherent", "Lumentum"],
            "risk": "产业化进度和订单兑现仍需持续验证。",
        },
    ],
    "ch": [
        {
            "name": "固态电池",
            "keywords": ["固态电池", "硫化物电解质", "半固态", "电池材料"],
            "risk": "产业化进度、良率和成本仍有不确定性。",
        },
        {
            "name": "商业航天/低空经济",
            "keywords": ["商业航天", "低空经济", "eVTOL", "卫星互联网", "无人机"],
            "risk": "政策推进和商业化订单节奏容易低于市场预期。",
        },
        {
            "name": "人形机器人",
            "keywords": ["人形机器人", "减速器", "灵巧手", "伺服", "机器人"],
            "risk": "主题弹性高，但量产节奏和盈利兑现仍早。",
        },
        {
            "name": "存储芯片",
            "keywords": ["存储芯片", "HBM", "DRAM", "NAND", "存储"],
            "risk": "价格周期和供需变化对盈利影响大。",
        },
        {
            "name": "CPO/光模块",
            "keywords": ["CPO", "光模块", "硅光", "光通信", "800G", "1.6T"],
            "risk": "高景气方向容易估值透支。",
        },
        {
            "name": "PCB/AI服务器链",
            "keywords": ["PCB", "AI服务器", "服务器PCB", "高速板", "HDI", "玻璃基板"],
            "risk": "订单集中度、扩产节奏和客户资本开支波动会影响兑现。",
        },
        {
            "name": "模拟/功率半导体涨价",
            "keywords": ["模拟芯片", "功率半导体", "涨价", "MLCC", "被动元件", "DrMOS"],
            "risk": "涨价持续性取决于供需紧张程度，库存回补结束后可能降温。",
        },
    ],
    "hk": [
        {
            "name": "AI 融资/新股",
            "keywords": ["AI boom", "artificial intelligence", "fundraising", "share sales", "IPO", "equity capital markets", "新股", "融资"],
            "risk": "新股和融资热度容易受市场情绪影响，上市后波动可能较大。",
        },
        {
            "name": "存储/半导体映射",
            "keywords": ["存储", "半导体", "澜起科技", "兆易创新", "芯片"],
            "risk": "港股相关标的流动性和估值弹性差异较大。",
        },
        {
            "name": "高股息央国企",
            "keywords": ["高股息", "分红", "回购", "南向资金", "央企"],
            "risk": "股息率并不等于低风险，需核验盈利和分红稳定性。",
        },
        {
            "name": "创新药出海",
            "keywords": ["创新药", "BD", "license-out", "出海", "临床"],
            "risk": "临床和授权进展不确定，波动大。",
        },
        {
            "name": "AI 终端/硬件",
            "keywords": ["AI PC", "AI 手机", "联想", "小米", "硬件"],
            "risk": "消费电子需求和产品周期变化较快。",
        },
    ],
}


def discover_themes(market: str, documents: list, limit: int = 8) -> list[dict]:
    discovered = []
    for theme in PROACTIVE_THEMES.get(market, []):
        evidence = _theme_evidence(theme, documents)
        if not evidence:
            continue
        score = sum(len(item["matched_keywords"]) for item in evidence) * 20 + len(evidence) * 8
        discovered.append(
            {
                "name": theme["name"],
                "score": score,
                "risk": theme["risk"],
                "matched_keywords": sorted({kw for item in evidence for kw in item["matched_keywords"]}),
                "evidence_sources": evidence[:3],
            }
        )
    discovered.sort(key=lambda item: item["score"], reverse=True)
    return discovered[:limit]


def _theme_evidence(theme: dict, documents: list) -> list[dict]:
    evidence = []
    for document in documents:
        if not isinstance(document, dict):
            text = str(document)
            title = "legacy text source"
            url = ""
            error = None
        else:
            text = f"{document.get('title', '')}\n{document.get('text', '')}"
            title = document.get("title", document.get("url", ""))
            url = document.get("url", "")
            error = document.get("error")
        lowered = text.lower()
        matched = [kw for kw in theme["keywords"] if kw.lower() in lowered]
        if matched:
            evidence.append(
                {
                    "url": url,
                    "title": title,
                    "matched_keywords": matched[:6],
                    "error": error,
                }
            )
    return evidence
