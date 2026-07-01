DEFAULT_TOTAL_CAPITAL = 500_000
DEFAULT_MARKET_RATIO = {"ch": 3, "hk": 1, "us": 1}

MARKET_NAMES = {
    "ch": "A 股",
    "hk": "港股",
    "us": "美股",
}


def build_default_portfolio_plan(
    total_capital: int = DEFAULT_TOTAL_CAPITAL,
    ratios: dict[str, int] | None = None,
) -> dict:
    ratios = ratios or DEFAULT_MARKET_RATIO
    ratio_sum = sum(ratios.values())
    markets = {}
    for market, ratio in ratios.items():
        target_pct = ratio / ratio_sum
        markets[market] = {
            "name": MARKET_NAMES[market],
            "target_ratio": round(target_pct, 4),
            "target_amount": int(total_capital * target_pct),
            "role": _market_role(market),
        }

    guardrails = {
        "max_single_position_pct": 0.05,
        "max_single_position_amount": int(total_capital * 0.05),
        "max_theme_pct": 0.15,
        "max_theme_amount": int(total_capital * 0.15),
        "max_high_volatility_pct": 0.25,
        "suggested_batches": 4,
        "single_trade_note": "新手单次建仓不宜过大，优先分 3-6 个月逐步执行。",
    }

    return {
        "total_capital": total_capital,
        "ratio_label": "3:1:1",
        "markets": markets,
        "guardrails": guardrails,
        "risk_checks": [
            "单一市场是否偏离目标比例超过 5 个百分点。",
            "单一主题是否超过总本金 15%。",
            "单一股票或 ETF 是否超过总本金 5%。",
            "高波动资产合计是否超过总本金 25%。",
            "是否保留了生活应急资金，不把短期要用的钱投入权益市场。",
        ],
        "questions": [
            "你的投资期限是 1 年以内、1-3 年，还是 3 年以上？",
            "你能接受账户最大回撤 5%、10%、还是 20%？",
            "你更想买 ETF/基金，还是愿意研究个股？",
            "你是否已有港美股账户和换汇安排？",
        ],
    }


def _market_role(market: str) -> str:
    roles = {
        "ch": "人民币核心仓位，重点关注宽基、红利和政策支持方向。",
        "hk": "估值修复和高股息补充仓位，同时承担港币和流动性风险。",
        "us": "美元资产和全球龙头补充仓位，重点控制汇率和估值风险。",
    }
    return roles[market]
