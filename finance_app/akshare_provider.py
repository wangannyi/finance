from typing import Any, Optional


class AkshareProvider:
    def __init__(self, ak_module: Optional[Any] = "auto"):
        if ak_module == "auto":
            try:
                import akshare as ak  # type: ignore
            except Exception:
                ak = None
            self.ak = ak
        else:
            self.ak = ak_module

    def status(self) -> dict:
        if self.ak is None:
            return {
                "available": False,
                "message": "AKShare 未安装。运行 pip install -r requirements.txt 后可启用 A 股/港股增强数据。",
            }
        return {
            "available": True,
            "message": "AKShare 已可用，可用于 A 股/港股行情和后续基本面扩展。",
        }

    def a_share_snapshot(self, limit: int = 20) -> list[dict]:
        if self.ak is None:
            return []
        frame = self.ak.stock_zh_a_spot_em()
        rows = frame.head(limit).to_dict("records")
        return [self._normalize_a_share(row) for row in rows]

    def hk_snapshot(self, limit: int = 20) -> list[dict]:
        if self.ak is None:
            return []
        frame = self.ak.stock_hk_spot_em()
        rows = frame.head(limit).to_dict("records")
        return [self._normalize_hk(row) for row in rows]

    def market_snapshot(self) -> dict:
        status = self.status()
        errors = []
        a_share = []
        hk = []
        if status["available"]:
            try:
                a_share = self.a_share_snapshot()
            except Exception as exc:
                errors.append(f"A 股增强数据获取失败：{exc}")
            try:
                hk = self.hk_snapshot()
            except Exception as exc:
                errors.append(f"港股增强数据获取失败：{exc}")
        return {
            "status": status,
            "a_share": a_share,
            "hk": hk,
            "errors": errors,
        }

    def _normalize_a_share(self, row: dict) -> dict:
        code = str(row.get("代码", "")).zfill(6)
        suffix = "SH" if code.startswith(("5", "6", "9")) else "SZ"
        return {
            "symbol": f"{code}.{suffix}",
            "name": row.get("名称"),
            "price": _to_float(row.get("最新价")),
            "change_pct": _to_float(row.get("涨跌幅")),
            "pe": _first_float(row, ["市盈率-动态", "市盈率", "市盈率TTM"]),
            "turnover": _to_float(row.get("成交额")),
            "source": "AKShare stock_zh_a_spot_em",
        }

    def _normalize_hk(self, row: dict) -> dict:
        code = str(row.get("代码", "")).zfill(5)
        return {
            "symbol": f"{code[-4:]}.HK",
            "name": row.get("名称"),
            "price": _to_float(row.get("最新价")),
            "change_pct": _to_float(row.get("涨跌幅")),
            "pe": _first_float(row, ["市盈率", "市盈率TTM", "PE"]),
            "turnover": _to_float(row.get("成交额")),
            "source": "AKShare stock_hk_spot_em",
        }


def _to_float(value) -> float | None:
    if value in (None, "", "-"):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _first_float(row: dict, keys: list[str]) -> float | None:
    for key in keys:
        value = _to_float(row.get(key))
        if value is not None:
            return value
    return None
