import json
import subprocess
import sys
from pathlib import Path
from typing import Callable


CODEX_SKILLS_DIR = Path.home() / ".codex" / "skills"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALPHAEAR_DB = PROJECT_ROOT / "data" / "alphaear_runtime.db"

Executor = Callable[[str, dict], dict]


def run_slot_skill_adapters(plan: dict, context: dict, executor: Executor | None = None) -> list[dict]:
    executor = executor or execute_skill_adapter
    results = []
    for skill in plan["skills"]:
        if skill == "alphaear-predictor" and plan.get("async_only"):
            results.append(
                {
                    "skill": skill,
                    "status": "queued_async",
                    "summary": "已进入异步预测队列，只对重点股票生成 1日/3日/5日概率。",
                    "symbols": _focus_symbols(context),
                }
            )
            continue
        try:
            result = executor(skill, context)
        except Exception as exc:  # pragma: no cover - defensive boundary
            result = {"status": "error", "summary": str(exc), "items": []}
        results.append({"skill": skill, **result})
    return results


def execute_skill_adapter(skill: str, context: dict, timeout_seconds: float = 18) -> dict:
    code = _skill_code(skill, context)
    if code is None:
        return {
            "status": "agentic",
            "summary": "该 skill 以 Agent 工作流方式执行，已由项目内信号/报告模块承载。",
            "items": [],
        }

    skill_dir = CODEX_SKILLS_DIR / skill
    if not (skill_dir / "SKILL.md").exists():
        return {"status": "missing", "summary": f"{skill} 未安装", "items": []}

    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            cwd=str(skill_dir),
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            env={**_clean_env(), "ALPHAEAR_RUNTIME_DB": str(ALPHAEAR_DB)},
        )
    except subprocess.TimeoutExpired:
        return {
            "status": "degraded",
            "summary": f"{skill} timed out after {timeout_seconds:g}s",
            "items": [],
        }
    if proc.returncode != 0:
        return {
            "status": "error",
            "summary": (proc.stderr or proc.stdout or "").strip()[-800:] or f"{skill} exited {proc.returncode}",
            "items": [],
        }
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"status": "ok", "summary": proc.stdout.strip()[:1200], "items": []}


def _skill_code(skill: str, context: dict) -> str | None:
    db_path = str(ALPHAEAR_DB)
    symbols = _focus_symbols(context)
    query = _focus_query(context)
    titles = _focus_titles(context)
    slot = context.get("slot", "")
    news_sources = ["cls", "wallstreetcn", "xueqiu"] if slot == "morning" else ["cls"]
    include_polymarket = slot == "morning"

    if skill == "alphaear-news":
        return f"""
import json, requests, time
items=[]
for src in {news_sources!r}:
    try:
        resp=requests.get('https://newsnow.busiyi.world/api/s', params={{'id':src}}, headers={{'User-Agent':'Mozilla/5.0 local-private-finance-research/1.0'}}, timeout=6)
        if resp.status_code == 200:
            for i,item in enumerate((resp.json().get('items') or [])[:3], 1):
                items.append({{'id': item.get('id') or f'{{src}}_{{int(time.time())}}_{{i}}', 'source': src, 'rank': i, 'title': item.get('title',''), 'url': item.get('url',''), 'publish_time': item.get('publish_time'), 'meta_data': item.get('extra', {{}})}})
    except Exception as exc:
        items.append({{'source': src, 'rank': 0, 'title': f'新闻源暂不可用: {{exc}}', 'url': '', 'error': str(exc)}})
poly=[]
if {include_polymarket!r}:
    try:
        resp=requests.get('https://gamma-api.polymarket.com/markets', params={{'active':'true','closed':'false','limit':3}}, timeout=6)
        if resp.status_code == 200:
            poly=resp.json()[:3]
    except Exception as exc:
        poly=[{{'error': str(exc)}}]
status='ok' if any(not item.get('error') for item in items) else 'degraded'
print(json.dumps({{'status':status,'summary':f'news {{len(items)}} items, polymarket {{len(poly)}} markets','items':items[:6], 'polymarket': poly}}, ensure_ascii=False))
"""
    if skill == "alphaear-search":
        return f"""
import json
from ddgs import DDGS
query={query!r}
items=[]
try:
    with DDGS(timeout=6) as ddgs:
        for item in ddgs.text(query, max_results=3):
            items.append({{'title': item.get('title',''), 'url': item.get('href',''), 'body': item.get('body','')}})
except Exception as exc:
    items=[{{'title':'搜索源暂不可用', 'url':'', 'body':str(exc), 'error':str(exc)}}]
status='ok' if items and not items[0].get('error') else 'degraded'
print(json.dumps({{'status':status,'summary':str(items)[:1200],'items':items}}, ensure_ascii=False))
"""
    if skill == "alphaear-stock":
        return f"""
import json, os
from scripts.database_manager import DatabaseManager
from scripts.stock_tools import StockTools
db=DatabaseManager(os.environ.get('ALPHAEAR_RUNTIME_DB', {db_path!r}))
tools=StockTools(db, auto_update=False)
symbols={symbols!r}
items=[]
for symbol in symbols[:6]:
    rows=tools.search_ticker(symbol, limit=3)
    items.append({{'symbol':symbol,'matches':rows}})
print(json.dumps({{'status':'ok','summary':f'stock lookup {{len(items)}} symbols','items':items}}, ensure_ascii=False))
"""
    if skill == "alphaear-sentiment":
        return f"""
import json, os
from scripts.database_manager import DatabaseManager
from scripts.sentiment_tools import SentimentTools
db=DatabaseManager(os.environ.get('ALPHAEAR_RUNTIME_DB', {db_path!r}))
tools=SentimentTools(db, mode='llm')
texts={titles!r}
items=[{{'text': t, **tools.analyze_sentiment(t)}} for t in texts[:6]]
print(json.dumps({{'status':'ok','summary':f'sentiment {{len(items)}} texts','items':items}}, ensure_ascii=False))
"""
    if skill == "alphaear-deepear-lite":
        return """
import json
from scripts.deepear_lite import DeepEarLiteTools
summary=DeepEarLiteTools().fetch_latest_signals()
print(json.dumps({'status':'ok' if not summary.startswith('Error ') else 'error','summary':summary[:2000],'items':[]}, ensure_ascii=False))
"""
    if skill == "alphaear-logic-visualizer":
        return None
    if skill == "alphaear-reporter":
        return None
    if skill == "alphaear-signal-tracker":
        return None
    if skill == "alphaear-predictor":
        return None
    return None


def _focus_symbols(context: dict) -> list[str]:
    symbols = context.get("symbols") or []
    return [str(symbol) for symbol in symbols if symbol][:8]


def _focus_query(context: dict) -> str:
    signals = context.get("signals") or []
    if signals:
        return " ".join(signal.get("name", "") for signal in signals[:3]).strip()
    return "A股 美股 港股 今日 热点"


def _focus_titles(context: dict) -> list[str]:
    titles = []
    for signal in context.get("signals") or []:
        titles.append(f"{signal.get('name', '')} {signal.get('evidence', '')}".strip())
    return titles[:8] or ["今日市场热点需要继续核验"]


def _clean_env() -> dict:
    import os

    return dict(os.environ)
