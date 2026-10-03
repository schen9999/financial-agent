#!/usr/bin/env python3
"""Per-call RAG answer tokens of an eval run, from its workflow object.

Each eval pod's result (an Argo output parameter) carries that ticker's LLM
ledger summed per call site. A brief makes one RAG answer call per site, so
the per-ticker sums are per-call values — unless the site's rows were
recorded twice. That happened on hosted smoke x2cx8 (2026-10-03, image
2dd1aa3): two threads each registered agent/tools/rag.py's usage handler, so
every hosted RAG call has two identical ledger rows. A site with 2 rows whose
total latency is twice its max and whose token sums are even is reported as
DUPLICATED and halved; anything else with more than one row is left as is
and flagged, never guessed at.

  kubectl -n financial-agent get workflow <wf> -o json > eval/runs/<wf>-workflow.json
  python scripts/rag_ledger_from_workflow.py eval/runs/x2cx8-workflow.json

Stdlib only.
"""
import argparse
import json
import math
import sys

RAG_SITES = ("rag:highlights", "rag:risks")


def percentile(values, q):
    """Linear-interpolated percentile (numpy's default)."""
    xs = sorted(values)
    k = (len(xs) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def ticker_rows(workflow: dict) -> dict:
    """{ticker: result row} from the eval pods' output parameters."""
    rows = {}
    for node in (workflow.get("status", {}).get("nodes") or {}).values():
        for prm in (node.get("outputs") or {}).get("parameters") or []:
            try:
                val = json.loads(prm.get("value") or "")
            except ValueError:
                continue
            items = val if isinstance(val, list) else val.get("results", [val]) if isinstance(val, dict) else []
            for r in items:
                if isinstance(r, dict) and r.get("ticker") and r.get("llm"):
                    rows[r["ticker"]] = r
    return rows


def per_call(site_summary: dict) -> dict:
    """One site's ledger summary for one ticker -> the single call behind it."""
    s = site_summary
    n = s["calls"]
    duplicated = (n == 2 and s["prompt_tokens"] % 2 == 0 and s["completion_tokens"] % 2 == 0
                  and abs(s["latency_s_total"] - 2 * (s["latency_s_max"] or 0)) <= 0.011)
    div = 2 if duplicated else 1
    return {"records": n, "duplicated": duplicated, "unexplained": n > 1 and not duplicated,
            "prompt_tokens": s["prompt_tokens"] // div,
            "completion_tokens": s["completion_tokens"] // div,
            "latency_s": s["latency_s_max"], "truncated": s["truncated"] // div}


def analyse(workflow: dict) -> dict:
    rows = ticker_rows(workflow)
    out = {"tickers": {}, "sites": {}}
    for ticker in sorted(rows):
        by_site = rows[ticker]["llm"]["by_site"]
        out["tickers"][ticker] = {
            "retrieval_s": (rows[ticker].get("timing_s") or {}).get("retrieval"),
            **{site: per_call(by_site[site]) for site in RAG_SITES if site in by_site}}
    for name, sites in (*((s, (s,)) for s in RAG_SITES), ("both", RAG_SITES)):
        calls = [t[s] for t in out["tickers"].values() for s in sites if s in t]
        comp = [c["completion_tokens"] for c in calls]
        if comp:
            out["sites"][name] = {
                "calls": len(calls), "records": sum(c["records"] for c in calls),
                "prompt_tokens": sum(c["prompt_tokens"] for c in calls),
                "completion_tokens": sum(comp), "min": min(comp),
                "median": percentile(comp, 0.5), "p95": percentile(comp, 0.95), "max": max(comp),
                "truncated": sum(c["truncated"] for c in calls)}
    out["duplicated_sites"] = sum(c["duplicated"] for t in out["tickers"].values()
                                  for c in t.values() if isinstance(c, dict))
    out["unexplained_sites"] = sum(c["unexplained"] for t in out["tickers"].values()
                                   for c in t.values() if isinstance(c, dict))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("workflow", help="kubectl get workflow -o json output")
    args = ap.parse_args(argv)
    with open(args.workflow, encoding="utf-8") as f:
        wf = json.load(f)
    res = analyse(wf)
    print(f"{wf['metadata']['name']} ({wf['status'].get('phase')}): {len(res['tickers'])} tickers")
    for ticker, t in res["tickers"].items():
        for site in RAG_SITES:
            c = t.get(site)
            if c:
                tag = "DUPLICATED" if c["duplicated"] else "UNEXPLAINED" if c["unexplained"] else "single"
                print(f"  {ticker:<6} {site:<15} records={c['records']} {tag:<11} "
                      f"prompt={c['prompt_tokens']:>5} completion={c['completion_tokens']:>4} "
                      f"latency={c['latency_s']:>6.2f}s retrieval_wall={t['retrieval_s']}s")
    print("\nper real call (p95 interpolated):")
    print(f"  {'site':<15} {'calls':>5} {'records':>7} {'prompt':>7} {'compl':>6} "
          f"{'min':>4} {'median':>6} {'p95':>5} {'max':>4} {'trunc':>5}")
    for name, s in res["sites"].items():
        print(f"  {name:<15} {s['calls']:>5} {s['records']:>7} {s['prompt_tokens']:>7} "
              f"{s['completion_tokens']:>6} {s['min']:>4} {s['median']:>6.0f} {s['p95']:>5.0f} "
              f"{s['max']:>4} {s['truncated']:>5}")
    print(f"\nduplicated (ticker, site) rows: {res['duplicated_sites']}; "
          f"unexplained multi-record rows: {res['unexplained_sites']}")
    return 1 if res["unexplained_sites"] else 0


if __name__ == "__main__":
    sys.exit(main())
