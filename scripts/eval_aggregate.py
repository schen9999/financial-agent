#!/usr/bin/env python3
"""eval_aggregate.py — final step of the Argo grounding-eval workflow.

Input: a JSON array of strings, each string being the --json-out payload of one
fanned-out grounding_check.py pod (one ticker each). Merges the per-ticker
results, prints the aggregate table, and enforces the quality gate:

  exit 1  if unsupported% > --max-unsupported-pct   (grounding regression)
  exit 1  if any ticker was skipped                 (incomplete eval is not a pass)
  exit 1  if total claims < --min-claims            (degenerate run can't pass 0/0)

A non-zero exit fails the Argo workflow, which is the point: the nightly eval
is a gate, not a report. Pure-stdlib on purpose — the aggregate pod starts fast.

Artifact archival (off by default): when EVAL_ARTIFACTS_PUT_URL is set — an
OCI Object Storage pre-authenticated request that permits writes — the run's
summary and per-ticker results are PUT under eval-runs/<run-id>/ in the
versioned eval-artifacts bucket. Best-effort BY DESIGN: the gate measures
grounding, archival is auxiliary, so an upload failure prints a WARNING and
never changes the exit code. Failed runs are archived too — they are the most
valuable ones to keep.
"""
import sys
import json
import os
import argparse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Repo root on sys.path so `eval.stats` imports when run as a script
# (pods set PYTHONPATH=/app; this covers bare local runs too). stats is
# stdlib-only, so the aggregate pod still starts fast.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval.stats import format_rate_ci, wilson_interval  # noqa: E402


def maybe_upload_artifacts(summary, results, skipped):
    """PUT the run's artifacts to the archive; returns None when disabled,
    else True/False for upload success. Never raises."""
    base = os.getenv("EVAL_ARTIFACTS_PUT_URL", "").strip()
    if not base:
        return None
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    objects = {
        "aggregate.json": summary,
        "results.json": {"results": results, "skipped": skipped},
    }
    ok = True
    for name, doc in objects.items():
        url = f"{base.rstrip('/')}/eval-runs/{run_id}/{name}"
        req = urllib.request.Request(
            url,
            data=json.dumps(doc, indent=2).encode("utf-8"),
            method="PUT",
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30):
                pass
        except Exception as e:  # noqa: BLE001 — archival must never fail the gate
            print(f"  WARNING: artifact upload failed for {name}: {e}")
            ok = False
    if ok:
        print(f"  artifacts uploaded: eval-runs/{run_id}/ ({len(objects)} objects)")
    return ok


def local_models(results):
    """Distinct local-model provenance dicts across the run's rows (rows from
    arms that routed to a local model carry one; others don't)."""
    seen = []
    for r in results:
        lm = r.get("local_model")
        if lm and lm not in seen:
            seen.append(lm)
    return seen


_FLAGS = ("truncated", "repeat_run", "retry", "parse_failure", "format_failure", "errors")


def _merge(into, a):
    t = into or {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0, "tokens_unrecorded": 0,
                 "latency_s_total": 0.0, "latency_s_max": 0.0, **{f: 0 for f in _FLAGS}}
    t["calls"] += a["calls"]
    t["prompt_tokens"] += a["prompt_tokens"]
    t["completion_tokens"] += a["completion_tokens"]
    t["tokens_unrecorded"] += max(a["prompt_tokens_unrecorded"], a["completion_tokens_unrecorded"])
    t["latency_s_total"] = round(t["latency_s_total"] + a["latency_s_total"], 3)
    t["latency_s_max"] = max(t["latency_s_max"], a["latency_s_max"] or 0.0)
    for f in _FLAGS:
        t[f] += a.get(f, 0)
    return t


def llm_totals(summaries):
    """Merge per-ticker ledger summaries (agent/llm_ledger.summarize) into
    per-site, per-endpoint and overall totals. Rows from images before the
    ledger carry none and are simply absent here (counted by the caller)."""
    by_site, by_endpoint = {}, {}
    for s in summaries:
        for site, a in s.get("by_site", {}).items():
            by_site[site] = _merge(by_site.get(site), a)
        for ep, a in s.get("by_endpoint", {}).items():
            by_endpoint[ep] = _merge(by_endpoint.get(ep), a)
    total = {k: sum(t[k] for t in by_site.values())
             for k in ("calls", "prompt_tokens", "completion_tokens", "tokens_unrecorded", *_FLAGS)}
    return {"by_site": by_site, "by_endpoint": by_endpoint, "total": total,
            "endpoints": sorted(by_endpoint)}


def slm_provenance(results):
    seen = []
    for r in results:
        p = r.get("slm")
        if p and p not in seen:
            seen.append(p)
    return seen


def rag_faithfulness_totals(results):
    """Summed over both RAG answers of every row that ran the metric."""
    sup = uns = tot = answers = 0
    for r in results:
        for v in (r.get("rag_faithfulness") or {}).values():
            if v:
                answers += 1
                sup += v["supported"]
                uns += v["unsupported"]
                tot += v["total"]
    return {"answers": answers, "supported": sup, "unsupported": uns, "claims": tot}


def stock_block_counts(results):
    """(tickers whose brief saw an empty STOCK DATA block, rows that don't
    record it). Detection only — never a gate failure (eval/stock_block.py).
    Rows from images before the check carry no field: unrecorded, not clean."""
    empty = sorted(r["ticker"] for r in results if r.get("stock_block_empty") is True)
    unrecorded = sum(1 for r in results if r.get("stock_block_empty") is None)
    return empty, unrecorded


def main():
    parser = argparse.ArgumentParser(description="Aggregate fanned-out grounding results.")
    parser.add_argument("--input", required=True,
                        help="Path to a JSON array of per-pod grounding_check --json-out strings.")
    parser.add_argument("--max-unsupported-pct", type=float, default=5.0)
    parser.add_argument("--min-claims", type=int, default=30,
                        help="Fail if fewer total claims were audited (guards against a "
                             "degenerate run passing on an empty denominator).")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        elements = json.load(f)

    results, skipped, failures = [], [], []
    for el in elements:
        payload = json.loads(el) if isinstance(el, str) else el
        results.extend(payload.get("results", []))
        skipped.extend(payload.get("skipped", []))
        failures.extend(payload.get("failures", []))

    sup = sum(r["supported"] for r in results)
    uns = sum(r["unsupported"] for r in results)
    inf = sum(r["inference"] for r in results)
    tot = sum(r["total"] for r in results)
    n = len(results)
    unsupported_pct = (uns / tot * 100) if tot else 100.0
    mean_retr = sum(r["retrieval_s"] for r in results) / n if n else 0.0
    mean_pipe = sum(r["pipeline_s"] for r in results) / n if n else 0.0

    judge_versions = sorted({r["judge_version"] for r in results if r.get("judge_version")})
    print("=" * 78)
    print("  NIGHTLY GROUNDING EVAL — AGGREGATE")
    print("=" * 78)
    print(f"  judge prompt      : {', '.join(judge_versions) if judge_versions else 'unrecorded (pre-v2 rows)'}")
    models = local_models(results)
    for lm in models:
        print(f"  local model       : {lm.get('local_model_served_name')} "
              f"(dir {lm.get('local_model_dir')}, {lm.get('local_model_backend')} "
              f"@ {lm.get('local_model_url')})")
        print(f"  local sampling    : {lm.get('local_model_sampling', 'unrecorded')}")
    if len(models) > 1:
        print("  WARNING: rows served by more than one local model — this run "
              "mixes models and is not a single-model measurement")
    slm_provs = slm_provenance(results)
    for p in slm_provs:
        print(f"  slm endpoint      : {p.get('slm_endpoint')} {p.get('slm_url')} — "
              f"{p.get('slm_served_name')} ({p.get('slm_artifact')})")
        print(f"  slm server        : build {p.get('slm_build')}, {p.get('slm_model_path')} "
              f"{p.get('slm_model_ftype')}, n_ctx {p.get('slm_n_ctx')}, "
              f"{p.get('slm_total_slots')} slots, thinking {p.get('slm_thinking')}")
        print(f"  slm sampling      : {p.get('slm_sampling')}")
        if "-hybrid-" in (p.get("slm_served_name") or ""):
            print("  slm layout        : HYBRID — MoE expert weights partly in host RAM "
                  "(--n-cpu-moe); label this run 'hybrid' in every table, never 'GPU'")
        elif p.get("slm_endpoint") == "slm-gpu":
            print("  slm layout        : all layers on GPU per the served alias — confirm "
                  "'offloaded N/N layers to GPU' in the server log for the record")
    if len(slm_provs) > 1:
        print("  WARNING: rows served by more than one SLM endpoint/config — this run "
              "is not a single-endpoint measurement")
    print(f"  {'Ticker':<8} {'Sup':>4} {'Uns':>4} {'Inf':>4} {'Tot':>4} {'Retr(s)':>8} {'Pipe(s)':>8}")
    print(f"  {'-'*44}")
    for r in sorted(results, key=lambda r: r["ticker"]):
        print(f"  {r['ticker']:<8} {r['supported']:>4} {r['unsupported']:>4} "
              f"{r['inference']:>4} {r['total']:>4} {r['retrieval_s']:>8.2f} {r['pipeline_s']:>8.2f}")
    print(f"  {'-'*44}")
    print(f"  {'TOTAL':<8} {sup:>4} {uns:>4} {inf:>4} {tot:>4} {mean_retr:>8.2f} {mean_pipe:>8.2f}")
    print()
    print(f"  tickers completed : {n}")
    print(f"  tickers skipped   : {len(skipped)}{' (' + ', '.join(skipped) + ')' if skipped else ''}")
    stock_empty, stock_unrecorded = stock_block_counts(results)
    print(f"  stock block empty : {len(stock_empty)}/{n}"
          f"{' (' + ', '.join(stock_empty) + ')' if stock_empty else ''}"
          f"{f'   ({stock_unrecorded} row(s) unrecorded)' if stock_unrecorded else ''}")
    if stock_empty:
        print("  WARNING: briefs above were written WITHOUT stock data (failed stock "
              "fetch, e.g. a yfinance 429) — the gate does not catch this")
    print(f"  unsupported rate  : {unsupported_pct:.2f}%   (gate: <= {args.max_unsupported_pct}%)")
    print(f"  95% CI (Wilson)   : {format_rate_ci(uns, tot)}")
    print(f"  total claims      : {tot}   (gate: >= {args.min_claims})")
    if failures:
        kinds = {}
        for f_ in failures:
            kinds.setdefault(f_["kind"], []).append(f_["ticker"])
        print("  failures by kind  : " + "; ".join(
            f"{k} {len(v)} ({', '.join(sorted(v))})" for k, v in sorted(kinds.items())))

    # LLM calls (agent calls only; judge calls are eval) — failed tickers'
    # calls count too: they reached the endpoint.
    llm_rows = [r["llm"] for r in results if r.get("llm")]
    llm = llm_totals(llm_rows + [f_["llm"] for f_ in failures if f_.get("llm")])
    if llm["by_site"]:
        n_ok = len(llm_rows)
        print()
        print(f"  LLM calls (agent) : {llm['total']['calls']} over {n_ok} completed ticker(s)"
              f"{f' + {len(failures)} failed' if failures else ''}"
              f" = {llm['total']['calls'] / max(n_ok + len(failures), 1):.1f}/ticker;"
              f" endpoints {', '.join(llm['endpoints'])}")
        print(f"  {'Site':<28} {'Calls':>5} {'Prompt':>8} {'Compl':>7} {'Lat(s)':>8} {'Max(s)':>7}"
              f" {'Trunc':>5} {'Loop':>4} {'Parse':>5} {'Fmt':>3} {'Retry':>5} {'Err':>3}")
        for site, t in sorted(llm["by_site"].items()):
            mean = t["latency_s_total"] / t["calls"] if t["calls"] else 0.0
            print(f"  {site:<28} {t['calls']:>5} {t['prompt_tokens']:>8} {t['completion_tokens']:>7}"
                  f" {mean:>8.2f} {t['latency_s_max']:>7.2f} {t['truncated']:>5} {t['repeat_run']:>4}"
                  f" {t['parse_failure']:>5} {t['format_failure']:>3} {t['retry']:>5} {t['errors']:>3}")
        if llm["total"]["tokens_unrecorded"]:
            print(f"  ({llm['total']['tokens_unrecorded']} call(s) without provider usage — "
                  f"token sums exclude them)")
        unrec = len(results) - n_ok
        if unrec:
            print(f"  ({unrec} row(s) from an image without the LLM ledger — not counted)")
    for ep, t in sorted(llm["by_endpoint"].items()):
        if ep.startswith("slm-"):
            # Machine-readable, one line per SLM endpoint, for
            # scripts/slm_traffic_proof.py: these must reconcile with the
            # endpoint's own /metrics counters over the run.
            print("  SLM_TRAFFIC " + json.dumps({
                "endpoint": ep, "calls": t["calls"], "prompt_tokens": t["prompt_tokens"],
                "completion_tokens": t["completion_tokens"],
                "calls_without_usage": t["tokens_unrecorded"], "errored_calls": t["errors"]},
                sort_keys=True))

    ragf = rag_faithfulness_totals(results)
    if ragf["answers"]:
        print(f"  RAG faithfulness  : {ragf['unsupported']}/{ragf['claims']} RAG-answer claims "
              f"unsupported by their own chunks, {format_rate_ci(ragf['unsupported'], ragf['claims'])} "
              f"over {ragf['answers']} answers — judge rf-v1, UNVALIDATED, separate from the "
              f"grounding rate above")

    est_costs = [r["est_cost"] for r in results if "est_cost" in r]
    if est_costs:
        print(f"  est. run cost     : ${sum(est_costs):.4f}   "
              f"(chars/4 tokens priced from scripts/model_prices.json; "
              f"excludes retries — cost of record stays scripts/cost_report.py)")

    failures = []
    if unsupported_pct > args.max_unsupported_pct:
        failures.append(f"unsupported rate {unsupported_pct:.2f}% exceeds {args.max_unsupported_pct}%")
    if skipped:
        failures.append(f"{len(skipped)} ticker(s) skipped: {', '.join(skipped)}")
    if tot < args.min_claims:
        failures.append(f"only {tot} claims audited (< {args.min_claims})")

    summary = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "judge_version": judge_versions or None,
        "local_model": models or None,
        "slm": slm_provs or None,
        "llm": llm,
        "failures": failures,
        "rag_faithfulness": ragf if ragf["answers"] else None,
        "totals": {
            "supported": sup, "unsupported": uns, "inference": inf, "claims": tot,
            "unsupported_pct": round(unsupported_pct, 2),
            "unsupported_ci_95": [round(x * 100, 2) for x in wilson_interval(uns, tot)],
            "mean_retrieval_s": round(mean_retr, 2), "mean_pipeline_s": round(mean_pipe, 2),
            "tickers_completed": n, "tickers_skipped": len(skipped),
            "stock_block_empty": len(stock_empty),
            "stock_block_empty_tickers": stock_empty,
            "stock_block_unrecorded": stock_unrecorded,
        },
        "gate": {
            "max_unsupported_pct": args.max_unsupported_pct,
            "min_claims": args.min_claims,
            "passed": not failures,
            "failures": failures,
        },
    }
    maybe_upload_artifacts(summary, results, skipped)

    print()
    if failures:
        for f_ in failures:
            print(f"  GATE FAILED: {f_}")
        print("=" * 78)
        sys.exit(1)
    print("  GATE PASSED")
    print("=" * 78)


if __name__ == "__main__":
    main()
