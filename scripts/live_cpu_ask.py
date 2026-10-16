#!/usr/bin/env python3
"""Live CPU /ask: one question answered by the ReAct agent (agent/react_agent.py)
with every model call on the CPU llama.cpp endpoint in the OKE cluster.

A demonstration, not a citable run: no judge, no traffic proof. It prints the
question, each tool call as the agent makes it, each tool's result (cut short),
the answer, the wall time, and per model call the endpoint and the alias the
server reported. It refuses to start unless the process is routed to the CPU
endpoint only, and it blocks the Anthropic SDK for its whole run: a hosted
model call would raise and fail the script, and none is expected (the /ask
agent, and the RAG answer inside query_sec_filing, both go to the SLM under
SLM_FULL; agent/tools/slm.py).

The image is pinned (f3043751) and predates this file, so it runs inside the
api pod as an argument to `python -c` (no stdin: the operator's kubectl
credential plugin consumes stdin):

  make live-cpu-ask                 # the default question
  make live-cpu-ask ALT=1           # alternate 1 (or 2)

Exit 0 only if the agent answered, used at least two tools, every model call
went to slm-cpu, and no hosted call was attempted.
"""
import argparse
import os
import re
import sys
import time

# (ticker, question, tools a correct agent needs). The default avoids Yahoo:
# the GPU smoke fetches Yahoo for ten tickers at the same time from the same
# egress IP, which has answered 429 before. It asks about a filing that
# cannot change before the demo: get_sec_filings always returns the LATEST
# 10-K, query_sec_filing answers from the 10-K indexed in Pinecone (all
# namespaces rebuilt 2026-09-04, scripts/reindex_filings.py), and the two
# agree only while no newer 10-K exists. Walmart's fiscal year ends 31 Jan;
# its 10-K of 2026-03-13 predates the reindex and the next is due about
# March 2027. (Visa, the first default, files in November: inside the demo
# window.) Apple files in late October, so its alternate names the fiscal
# 2025 10-K, the indexed one, and does not ask for a filing date.
# The default asks about one risk the top-3 retrieval returns cleanly. The
# open-ended "main risk factors" (trial 2026-10-16) drifted: with three
# chunks the answer recast Walmart's "Shared Value" framework as risks and
# mislabelled a category; only its omnichannel/eCommerce point was a risk
# factor.
QUESTIONS = [
    ("WMT", "When was Walmart's most recent 10-K filed, and what does it say about "
            "the risks of its omnichannel and eCommerce investments?",
     ("get_sec_filings", "query_sec_filing")),
    ("AAPL", "What is Apple's current P/E ratio, and what risk factors does its "
             "fiscal 2025 10-K list?", ("get_stock_data", "query_sec_filing")),
    ("MSFT", "What has been in the news about Microsoft recently, and when was "
             "its latest 10-Q filed?", ("get_company_news", "get_sec_filings")),
]

# The 10-K each default ticker's Pinecone namespace was built from (EDGAR
# filing date). If get_sec_filings reports another 10-K, the two tools would
# describe different filings on screen: the run is NOT OK.
INDEXED_10K = {"WMT": "2026-03-13"}
_TEN_K_DATE = re.compile(r"""form_type['"]:\s*['"]10-K['"],\s*['"]filing_date['"]:\s*['"](\d{4}-\d{2}-\d{2})""")

RESULT_CHARS = 240


def check_route() -> None:
    """Refuse unless this process sends model calls to the CPU endpoint only."""
    problems = []
    if os.getenv("SLM_FULL", "").strip().lower() != "true":
        problems.append("SLM_FULL is not true (the agent would use hosted Sonnet)")
    if os.getenv("SLM_ENDPOINT", "").strip().lower() != "cpu":
        problems.append(f"SLM_ENDPOINT is {os.getenv('SLM_ENDPOINT')!r}, not 'cpu'")
    for var in ("SLM_GPU_URL", "SLM_GPU_API_KEY"):
        if os.getenv(var, "").strip():
            problems.append(f"{var} is set; blank it so nothing here can reach node 2")
    if problems:
        raise SystemExit("refusing: " + "; ".join(problems))


class HostedCallBlocked(RuntimeError):
    pass


def block_hosted() -> dict:
    """Make every Anthropic SDK request raise, and count the attempts. Both the
    LangChain (ChatAnthropic) and llama_index Anthropic clients go through
    these two methods."""
    from anthropic._base_client import AsyncAPIClient, SyncAPIClient
    attempts = {"n": 0}

    def _sync(self, *a, **k):
        attempts["n"] += 1
        raise HostedCallBlocked("hosted Anthropic call attempted during the live CPU ask")

    async def _async(self, *a, **k):
        attempts["n"] += 1
        raise HostedCallBlocked("hosted Anthropic call attempted during the live CPU ask")

    SyncAPIClient.request = _sync
    AsyncAPIClient.request = _async
    return attempts


def _short(text, n=RESULT_CHARS) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[:n] + " …"


def run(ticker: str, question: str, out=print) -> dict:
    from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

    from agent import llm_ledger, react_agent
    from agent.tools.slm import server_facts

    facts = server_facts()
    out(f"endpoint  {facts['slm_endpoint']}  served alias {facts['slm_served_name']}  "
        f"build {facts['slm_build']}")
    out(f"question  [{ticker}] {question}")
    llm_ledger.enable()
    llm_ledger.drain()
    graph = react_agent._build_graph(react_agent._route())
    t0 = time.perf_counter()
    tools, answer, results = [], None, {}
    stream = graph.stream(
        {"messages": [HumanMessage(content=f"Ticker: {ticker.upper()}. {question}")]},
        config={"recursion_limit": react_agent.RECURSION_LIMIT}, stream_mode="updates")
    for update in stream:
        for node, payload in update.items():
            for m in (payload or {}).get("messages", []):
                t = time.perf_counter() - t0
                if isinstance(m, AIMessage) and m.tool_calls:
                    for c in m.tool_calls:
                        tools.append(c["name"])
                        out(f"  {t:6.1f}s  tool call   {c['name']}({_short(c['args'], 120)})")
                elif isinstance(m, ToolMessage):
                    results[m.name] = str(m.content)
                    out(f"  {t:6.1f}s  tool result {m.name}: {_short(m.content)}")
                elif isinstance(m, AIMessage) and isinstance(m.content, str) and m.content.strip():
                    answer = m.content.strip()
    wall = time.perf_counter() - t0
    recs = llm_ledger.drain()
    filing_ok = True
    if ticker in INDEXED_10K and "get_sec_filings" in results:
        m = _TEN_K_DATE.search(results["get_sec_filings"])
        got, want = (m.group(1) if m else None), INDEXED_10K[ticker]
        filing_ok = got == want
        out(f"10-K check  get_sec_filings: {got or 'no 10-K date in the result'}; "
            f"indexed filing: {want} -> {'same filing' if filing_ok else 'MISMATCH'}")
    out("answer")
    out(answer or "(no answer)")
    out("model calls")
    for r in recs:
        out(f"  {r['site']:<5} {r['endpoint']:<8} alias {r['model']}  "
            f"{r['prompt_tokens']} prompt + {r['completion_tokens']} completion tokens  "
            f"{r['latency_s']} s{'  ERROR ' + r['error'] if r.get('error') else ''}")
    return {"wall_s": round(wall, 1), "tools": tools, "answer": answer, "calls": recs,
            "endpoints": sorted({r["endpoint"] for r in recs}),
            "aliases": sorted({r["model"] for r in recs if r.get("model")}),
            "served_alias": facts["slm_served_name"], "filing_ok": filing_ok}


def verdict(res: dict, hosted_attempts: int) -> tuple[bool, str]:
    ok = (bool(res["answer"]) and len(set(res["tools"])) >= 2
          and res["endpoints"] == ["slm-cpu"] and hosted_attempts == 0
          and not any(r.get("error") for r in res["calls"])
          and res.get("filing_ok", True))
    line = (f"LIVE CPU ASK: {'OK' if ok else 'NOT OK'} — wall {res['wall_s']} s, "
            f"tools {res['tools']}, {len(res['calls'])} model calls on {res['endpoints']}, "
            f"alias {res['aliases']}, hosted calls attempted {hosted_attempts}"
            f"{'' if res.get('filing_ok', True) else ', 10-K MISMATCH'}. "
            f"A demonstration, not a citable run.")
    return ok, line


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="live_cpu_ask", description=__doc__.split("\n\n")[0])
    ap.add_argument("--alt", type=int, default=0, choices=range(len(QUESTIONS)),
                    help="0 = the default question, 1 or 2 = an alternate")
    args = ap.parse_args(argv)
    check_route()
    attempts = block_hosted()
    ticker, question, _ = QUESTIONS[args.alt]
    try:
        res = run(ticker, question)
    except HostedCallBlocked as e:
        print(f"LIVE CPU ASK: NOT OK — {e}")
        return 1
    ok, line = verdict(res, attempts["n"])
    print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
