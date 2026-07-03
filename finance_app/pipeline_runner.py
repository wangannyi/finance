import json
import sys
from datetime import datetime, timezone

from .crawler import refresh_reports
from .intraday_brief import build_intraday_brief
from .research_workflow import build_research_workflow
from .skill_adapter import run_slot_skill_adapters
from .skill_pipeline import get_slot_plan
from .storage import ReportStore


def run_pipeline_slot(
    slot: str,
    db_path: str = "data/reports.sqlite3",
    store: ReportStore | None = None,
    execute_skills: bool = False,
    skill_executor=None,
    report_runner=refresh_reports,
) -> dict:
    store = store or ReportStore(db_path)
    plan = get_slot_plan(slot)
    reports = store.get_latest_reports()

    if slot == "morning":
        reports = report_runner(db_path)
        preload = {
            "status": "skipped_async",
            "message": "公司详情预热不阻塞晨报；网站服务启动和 /api/preload-companies 会在后台处理。",
        }
    else:
        preload = None

    workflow = build_research_workflow(reports)
    intraday = build_intraday_brief(reports)
    context = {
        "slot": slot,
        "reports": reports,
        "signals": workflow["tracked_signals"],
        "symbols": _focus_symbols(intraday),
    }
    skill_results = run_slot_skill_adapters(plan, context, executor=skill_executor) if execute_skills else []

    payload = {
        "slot": slot,
        "time": plan["time"],
        "title": plan["title"],
        "status": "complete",
        "async_only": plan["async_only"],
        "skills": plan["skills"],
        "layers": plan["layers"],
        "output": plan["output"],
        "generated_at": _now_iso(),
        "preload": preload,
        "workflow": workflow,
        "intraday": intraday,
        "skill_results": skill_results,
        "note": _slot_note(plan),
    }
    store.save_pipeline_run(slot, payload)
    return payload


def _slot_note(plan: dict) -> str:
    if plan["async_only"]:
        return "该时点包含异步 skill，页面先展示队列状态和概率区间，不阻塞刷新。"
    return "该时点只运行必要 skill 层，避免全量触发 9 个 skill。"


def _focus_symbols(intraday: dict) -> list[str]:
    symbols = [item.get("symbol", "") for item in intraday.get("holdings", [])]
    for signal in intraday.get("signals", [])[:4]:
        for source in signal.get("evidence_sources", []):
            for keyword in source.get("matched_keywords", []):
                if keyword.isupper() and 2 <= len(keyword) <= 6:
                    symbols.append(keyword)
    seen = []
    for symbol in symbols:
        if symbol and symbol not in seen:
            seen.append(symbol)
    return seen[:8]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def main() -> int:
    slot = sys.argv[1] if len(sys.argv) > 1 else "morning"
    db_path = sys.argv[2] if len(sys.argv) > 2 else "data/reports.sqlite3"
    result = run_pipeline_slot(slot, db_path=db_path, execute_skills=True)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
