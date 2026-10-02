#!/usr/bin/env python3
"""Tool-use check for the ReAct /ask agent (agent/react_agent.py) — the most
agentic part of the system, and the one the grounding eval never exercises.

Ten fixed questions, each with the one tool a correct agent must call.
Scored mechanically from the message trace — no LLM judge:
  parse rate        valid tool calls / all tool calls the model emitted
                    (an unparseable call lands in AIMessage.invalid_tool_calls)
  correct tool      the expected tool was called (and, separately, first)
  loop completion   the agent ended on a non-empty answer with no pending tool
                    call, without an error or hitting the recursion limit
Answers are not graded for correctness; this measures the tool loop only.

Route (one per run, so each JSON names what served it):
  --route hosted   Sonnet 4.6 (the production /ask model)
  --route cpu|gpu  SLM_FULL on the named endpoint (env as for the eval pods)
Tools hit the real data sources (yfinance, NewsAPI, EDGAR, Pinecone).

  python eval/tool_use_check.py --route cpu --json-out /tmp/tool_use_cpu.json
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

QUESTIONS = [
    ("AAPL", "What is the current P/E ratio?", "get_stock_data"),
    ("MSFT", "What is the market capitalization right now?", "get_stock_data"),
    ("NVDA", "What is the 52-week high?", "get_stock_data"),
    ("JPM", "What is the dividend yield?", "get_stock_data"),
    ("TSLA", "What has been in the news about the company recently?", "get_company_news"),
    ("AMZN", "Summarize the latest news headlines about the company.", "get_company_news"),
    ("GOOGL", "When was the most recent 10-K filed, and what does its summary say?", "get_sec_filings"),
    ("META", "What is the filing date of the company's latest 10-Q?", "get_sec_filings"),
    ("WMT", "According to its SEC filings, what are the main risk factors?", "query_sec_filing"),
    ("V", "What do the company's SEC filings say about competition?", "query_sec_filing"),
]


def score_trace(messages, expected: str) -> dict:
    """Score one question's message trace (pure; unit-tested)."""
    from langchain_core.messages import AIMessage
    valid, invalid, names = 0, 0, []
    for m in messages:
        if isinstance(m, AIMessage):
            calls = getattr(m, "tool_calls", None) or []
            valid += len(calls)
            invalid += len(getattr(m, "invalid_tool_calls", None) or [])
            names += [c["name"] for c in calls]
    last = messages[-1] if messages else None
    completed = (isinstance(last, AIMessage) and not (last.tool_calls or [])
                 and isinstance(last.content, str) and bool(last.content.strip()))
    return {"tool_calls": valid, "invalid_tool_calls": invalid, "tools_called": names,
            "expected_tool": expected, "expected_called": expected in names,
            "expected_first": bool(names) and names[0] == expected, "completed": completed}


def _set_route(route: str):
    if route == "hosted":
        os.environ["SLM_FULL"] = "false"
    else:
        os.environ["SLM_FULL"] = "true"
        os.environ["SLM_ENDPOINT"] = route


def run(route: str) -> dict:
    _set_route(route)
    from agent import llm_ledger
    from agent.react_agent import react_trace
    provenance = None
    if route != "hosted":
        from agent.tools.slm import server_facts
        provenance = server_facts()
    llm_ledger.enable()
    rows = []
    for ticker, question, expected in QUESTIONS:
        llm_ledger.drain()
        t0 = time.perf_counter()
        try:
            row = score_trace(react_trace(ticker, question), expected)
            row["error"] = None
        except Exception as e:  # recursion limit, endpoint error: the loop did not complete
            row = {"tool_calls": 0, "invalid_tool_calls": 0, "tools_called": [],
                   "expected_tool": expected, "expected_called": False, "expected_first": False,
                   "completed": False, "error": f"{type(e).__name__}: {str(e)[:200]}"}
        recs = llm_ledger.drain()
        row.update(ticker=ticker, question=question, wall_s=round(time.perf_counter() - t0, 2),
                   llm_calls=len(recs), endpoints=sorted({r["endpoint"] for r in recs}),
                   prompt_tokens=sum(r["prompt_tokens"] or 0 for r in recs),
                   completion_tokens=sum(r["completion_tokens"] or 0 for r in recs))
        rows.append(row)
        print(f"  {ticker:<6} expected {expected:<17} called {row['tools_called'] or '-'} "
              f"completed={row['completed']} {row['wall_s']}s"
              f"{'  ERROR ' + row['error'] if row['error'] else ''}", flush=True)
    n = len(rows)
    calls = sum(r["tool_calls"] for r in rows)
    bad = sum(r["invalid_tool_calls"] for r in rows)
    summary = {
        "route": route, "questions": n,
        "parse_rate": round(calls / (calls + bad), 3) if calls + bad else None,
        "tool_calls": calls, "invalid_tool_calls": bad,
        "expected_called": sum(r["expected_called"] for r in rows),
        "expected_first": sum(r["expected_first"] for r in rows),
        "completed": sum(r["completed"] for r in rows),
        "errors": sum(1 for r in rows if r["error"]),
        "endpoints": sorted({e for r in rows for e in r["endpoints"]}),
    }
    print(f"\n  route {route}: parse rate {summary['parse_rate']} ({calls} valid, {bad} invalid); "
          f"correct tool {summary['expected_called']}/{n} (first {summary['expected_first']}/{n}); "
          f"completed {summary['completed']}/{n}; errors {summary['errors']}; "
          f"endpoints {summary['endpoints']}", flush=True)
    return {"summary": summary, "provenance": provenance, "rows": rows}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--route", choices=("hosted", "cpu", "gpu"), required=True)
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    out = run(args.route)
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(out, indent=2), encoding="utf-8")
        print(f"  written: {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
