#!/usr/bin/env python3
"""Unsupported-claim rates across N eval runs: Wilson 95% CI per run, exact
two-sided Fisher for every pair, and a per-section breakdown.

Written for the 2026-09-23 four-arm comparison (hosted baseline vs three
local models), where three runs share the harness arm name `local-model`,
so runs are keyed by a caller-supplied label instead of the arm.
eval/section_attribution.py (keyed by arm, two runs) is left unchanged so its
recorded j4cnp/lsnnc output keeps reproducing; this script reuses its
attribution heuristic exactly — claims are attributed to the pre-written
section they restate (normalized containment, else word-overlap >= 0.6,
else unattributed). Section buckets are diagnostic; the per-run totals are
the measured result. Free-form verdicts without a CLAIM line (claim=null)
count in the totals and land in "unattributed".

Usage:
  python eval/multi_arm_stats.py \\
      --run hosted  eval/runs/kcf7s-claims.jsonl eval/runs/raw/kcf7s-findings \\
      --run lora    eval/runs/v924f-claims.jsonl eval/runs/raw/v924f-findings ... \\
      [--pool hosted-pooled hosted rerun]

--pool NAME LABEL LABEL... concatenates the claims of runs from the same arm
(e.g. two hosted runs on one image) and tests each run outside the pool
against it.

Runs over the same tickers also get a paired per-ticker comparison of
numeric claims (exact sign test, mean difference with a bootstrap interval).
--rows LABEL FILE adds what the claims do not carry, from each run's
per-ticker result rows (a workflow object, or the aggregate's input JSON):
RAG faithfulness side by side — judge rf-v1, unvalidated, never part of the
grounding rate — and latency per call site and per ticker.
"""
import argparse
import json
import random
import sys
from itertools import combinations
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from eval import claim_density  # noqa: E402
from eval.section_attribution import attribute, section_texts  # noqa: E402
from eval.stats import fisher_exact, format_rate_ci  # noqa: E402

SECTIONS = ("financial-health", "risk-factors", "recent-developments",
            "sec-filing-highlights", "other", "unattributed")
OWNED = ("financial-health", "risk-factors")


def load_run(claims_path: Path, findings_dir: Path) -> list[dict]:
    """Claim rows, each with its attributed section added."""
    secs = section_texts(findings_dir)
    rows = []
    for line in claims_path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        r["attributed"] = attribute(r["claim"], secs.get((r["ticker"], r["arm"]), {})) \
            or "unattributed"
        rows.append(r)
    return rows


def tally(rows, pred=lambda r: True) -> tuple[int, int]:
    sel = [r for r in rows if pred(r)]
    return sum(r["judge_label"] == "UNSUPPORTED" for r in sel), len(sel)


def pairwise(runs: dict, pred=lambda r: True) -> list[tuple]:
    out = []
    for a, b in combinations(runs, 2):
        (ua, na), (ub, nb) = tally(runs[a], pred), tally(runs[b], pred)
        out.append((a, b, ua, na, ub, nb, fisher_exact(ua, na - ua, ub, nb - ub)))
    return out


def pooled(runs: dict, name: str, members: list[str], pred=lambda r: True) -> list[tuple]:
    """Fisher of the pooled member runs against each run outside the pool."""
    pool = [r for m in members for r in runs[m]]
    up, np_ = tally(pool, pred)
    out = []
    for label, rows in runs.items():
        if label in members:
            continue
        u, n = tally(rows, pred)
        out.append((label, name, u, n, up, np_, fisher_exact(u, n - u, up, np_ - up)))
    return out


def sign_test(pos: int, neg: int) -> float:
    """Exact two-sided sign test on the non-tied pairs."""
    n, k = pos + neg, min(pos, neg)
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def paired(dens_a: dict, dens_b: dict, field: str = "numeric", seed: int = 0,
           resamples: int = 10000) -> dict | None:
    """Per-ticker a - b over the tickers both runs have. The interval on the
    mean difference is a percentile bootstrap over tickers (seeded)."""
    common = sorted(set(dens_a) & set(dens_b))
    if not common:
        return None
    d = [dens_a[t][field] - dens_b[t][field] for t in common]
    rng = random.Random(seed)
    means = sorted(sum(rng.choices(d, k=len(d))) / len(d) for _ in range(resamples))
    pos, neg = sum(x > 0 for x in d), sum(x < 0 for x in d)
    srt = sorted(d)
    return {"tickers": len(common),
            "mean_a": sum(dens_a[t][field] for t in common) / len(common),
            "mean_b": sum(dens_b[t][field] for t in common) / len(common),
            "mean_diff": sum(d) / len(d),
            "median_diff": (srt[(len(d) - 1) // 2] + srt[len(d) // 2]) / 2,
            "ci": (means[int(0.025 * resamples)], means[int(0.975 * resamples) - 1]),
            "a_more": pos, "equal": len(d) - pos - neg, "b_more": neg,
            "sign_p": sign_test(pos, neg)}


def load_rows(path: Path) -> list[dict]:
    """A run's per-ticker result rows: from a workflow object (the eval pods'
    stored output parameters) or from the aggregate's input JSON."""
    from workflow_nodes import eval_results
    doc = json.loads(path.read_text(encoding="utf-8"))
    payloads = eval_results(doc) if isinstance(doc, dict) else doc
    return [r for p in payloads for r in p.get("results", [])]


def ragf_totals(rows: list[dict]) -> tuple[int, int, int]:
    """(unsupported, claims, answers) over every RAG answer that was judged."""
    uns = tot = answers = 0
    for r in rows:
        for v in (r.get("rag_faithfulness") or {}).values():
            if v:
                answers += 1
                uns += v["unsupported"]
                tot += v["total"]
    return uns, tot, answers


def site_latency(rows: list[dict]) -> dict:
    """{site: (calls, mean seconds per call, max seconds)} from the ledgers."""
    out = {}
    for r in rows:
        for site, s in ((r.get("llm") or {}).get("by_site") or {}).items():
            c, total, mx = out.get(site, (0, 0.0, 0.0))
            out[site] = (c + s["calls"], total + s["latency_s_total"],
                         max(mx, s["latency_s_max"] or 0.0))
    return {site: (c, total / c if c else 0.0, mx) for site, (c, total, mx) in sorted(out.items())}


def _spread(vals: list[float]) -> str:
    return f"mean {sum(vals) / len(vals):>7.2f}  min {min(vals):>7.2f}  max {max(vals):>7.2f}"


def print_rows_sections(rows: dict) -> None:
    print("\nRAG faithfulness (RAG-answer claims unsupported by their own chunks; judge rf-v1, "
          "UNVALIDATED, separate from the grounding rate):")
    for label, rs in rows.items():
        u, n, answers = ragf_totals(rs)
        print(f"  {label:<14} {u}/{n} = {format_rate_ci(u, n)} over {answers} answers")
    for a, b in combinations(rows, 2):
        (ua, na, _), (ub, nb, _) = ragf_totals(rows[a]), ragf_totals(rows[b])
        if na and nb:
            print(f"  {a:<14} vs {b:<14} {ua}/{na} vs {ub}/{nb}   "
                  f"p = {fmt_p(fisher_exact(ua, na - ua, ub, nb - ub))}  (exact two-sided Fisher)")

    lat = {label: site_latency(rs) for label, rs in rows.items()}
    print("\nLatency per call site (calls; mean s per call; max s):")
    for site in sorted({s for v in lat.values() for s in v}):
        print(f"  {site}")
        for label, v in lat.items():
            if site in v:
                c, mean, mx = v[site]
                print(f"    {label:<14} {c:>4} calls   mean {mean:>7.2f}   max {mx:>7.2f}")
    print("\nPer ticker, seconds (the harness's own timers):")
    for label, rs in rows.items():
        print(f"  {label:<14} pipeline  {_spread([r['pipeline_s'] for r in rs])}   "
              f"({len(rs)} tickers)")
        print(f"  {'':<14} retrieval {_spread([r['retrieval_s'] for r in rs])}")
    for a, b in combinations(rows, 2):
        pa = {r["ticker"]: r["pipeline_s"] for r in rows[a]}
        pb = {r["ticker"]: r["pipeline_s"] for r in rows[b]}
        common = sorted(set(pa) & set(pb))
        if common:
            ma, mb = (sum(p[t] for t in common) / len(common) for p in (pa, pb))
            print(f"  {b} / {a} mean pipeline time over {len(common)} common tickers: "
                  f"{mb / ma:.1f}x ({mb:.1f} s vs {ma:.1f} s)")


def fmt_p(p: float) -> str:
    return f"{p:.4f}" if p >= 1e-4 else f"{p:.1e}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", nargs=3, action="append", required=True,
                    metavar=("LABEL", "CLAIMS_JSONL", "FINDINGS_DIR"))
    ap.add_argument("--pool", nargs="+", action="append", default=[],
                    metavar="NAME LABEL",
                    help="pool the labeled runs under NAME and test every other "
                         "run against the pool (e.g. --pool hosted-pooled kcf7s dvvxk)")
    ap.add_argument("--rows", nargs=2, action="append", default=[],
                    metavar=("LABEL", "WORKFLOW_OR_RESULTS_JSON"),
                    help="per-ticker result rows of a run given by --run: adds RAG "
                         "faithfulness and latency sections")
    args = ap.parse_args()
    runs = {label: load_run(Path(c), Path(f)) for label, c, f in args.run}
    for name, *members in args.pool:
        if len(members) < 2 or any(m not in runs for m in members):
            ap.error(f"--pool {name}: needs two or more labels given by --run")

    print("Per run (all judged claims):")
    for label, rows in runs.items():
        u, n = tally(rows)
        print(f"  {label:<14} {u}/{n} = {format_rate_ci(u, n)}")

    # Co-primary: numeric claims (claims that quote a figure). The rate over
    # all claims rewards an arm that states fewer checkable facts, and how
    # many qualitative phrases the judge lists varies from run to run; the
    # numeric subset is the stable denominator (eval/claim_density.py).
    dens = {label: claim_density.run_density(Path(f)) for label, _c, f in args.run}
    num = {label: claim_density.summarize(per) for label, per in dens.items()}
    print("\nCo-primary, numeric claims (claims that quote a figure):")
    for label, s in num.items():
        print(f"  {label:<14} {s['numeric_mean']:.1f}/ticker (min {s['numeric_min']}, "
              f"{s['tickers']} tickers)   unsupported {s['numeric_unsupported']}/{s['numeric']} = "
              f"{format_rate_ci(s['numeric_unsupported'], s['numeric'])}")
    print("Pairwise, exact two-sided Fisher (numeric claims):")
    for a, b in combinations(num, 2):
        ua, na, ub, nb = (num[a]["numeric_unsupported"], num[a]["numeric"],
                          num[b]["numeric_unsupported"], num[b]["numeric"])
        print(f"  {a:<14} vs {b:<14} {ua}/{na} vs {ub}/{nb}   "
              f"p = {fmt_p(fisher_exact(ua, na - ua, ub, nb - ub))}")
    def print_paired(field, what):
        for a, b in combinations(dens, 2):
            pr = paired(dens[a], dens[b], field)
            if pr and pr["tickers"] > 1:
                print(f"Paired per ticker, {what}, {pr['tickers']} common tickers ({a} - {b}):")
                print(f"  mean {pr['mean_a']:.2f} vs {pr['mean_b']:.2f}; mean difference "
                      f"{pr['mean_diff']:+.2f} (95% bootstrap CI {pr['ci'][0]:+.2f} to "
                      f"{pr['ci'][1]:+.2f}), median {pr['median_diff']:+.1f}")
                print(f"  {a} has more on {pr['a_more']} tickers, equal on {pr['equal']}, "
                      f"{b} more on {pr['b_more']}; exact two-sided sign test p = "
                      f"{fmt_p(pr['sign_p'])}")

    print_paired("numeric", "numeric claims")
    print(f'Sensitivity, numeric claims without those numeric only through '
          f'"{claim_density.PHRASE}" (a label, not a figure):')
    for label, s in num.items():
        print(f"  {label:<14} {s['numeric_strict_mean']:.2f}/ticker   unsupported "
              f"{s['numeric_strict_unsupported']}/{s['numeric_strict']} = "
              f"{format_rate_ci(s['numeric_strict_unsupported'], s['numeric_strict'])}")
    for a, b in combinations(num, 2):
        ua, na, ub, nb = (num[a]["numeric_strict_unsupported"], num[a]["numeric_strict"],
                          num[b]["numeric_strict_unsupported"], num[b]["numeric_strict"])
        print(f"  {a:<14} vs {b:<14} {ua}/{na} vs {ub}/{nb}   "
              f"p = {fmt_p(fisher_exact(ua, na - ua, ub, nb - ub))}  (exact two-sided Fisher)")
    print_paired("numeric_strict", "numeric claims without the 52-week ones")
    print("\nClaim density (eval/claim_density.py):")
    claim_density.print_report(dens)

    print("\nPairwise, exact two-sided Fisher (all claims):")
    for a, b, ua, na, ub, nb, p in pairwise(runs):
        print(f"  {a:<14} vs {b:<14} {ua}/{na} vs {ub}/{nb}   p = {fmt_p(p)}")

    for name, *members in args.pool:
        print(f"\nPooled {name} ({' + '.join(members)}), exact two-sided Fisher "
              f"(all claims):")
        for a, b, ua, na, ub, nb, p in pooled(runs, name, members):
            print(f"  {a:<14} vs {b:<14} {ua}/{na} vs {ub}/{nb}   p = {fmt_p(p)}")

    print("\nPer section (attributed; unsupported/claims = rate, 95% CI):")
    for sec in SECTIONS:
        print(f"  {sec}")
        for label, rows in runs.items():
            u, n = tally(rows, lambda r, s=sec: r["attributed"] == s)
            print(f"    {label:<14} {u}/{n} = {format_rate_ci(u, n)}")

    owned = lambda r: r["attributed"] in OWNED  # noqa: E731
    rest = lambda r: r["attributed"] not in OWNED  # noqa: E731
    for title, pred in (("Financial Health + Risk Factors (fine-tune-owned in the "
                         "local arms)", owned), ("All other claims", rest)):
        print(f"\n{title}, per run:")
        for label, rows in runs.items():
            u, n = tally(rows, pred)
            print(f"  {label:<14} {u}/{n} = {format_rate_ci(u, n)}")
        print(f"{title}, pairwise Fisher:")
        for a, b, ua, na, ub, nb, p in pairwise(runs, pred):
            print(f"  {a:<14} vs {b:<14} {ua}/{na} vs {ub}/{nb}   p = {fmt_p(p)}")

    if args.rows:
        unknown = [label for label, _ in args.rows if label not in runs]
        if unknown:
            ap.error(f"--rows: no --run with label {', '.join(unknown)}")
        print_rows_sections({label: load_rows(Path(path)) for label, path in args.rows})


if __name__ == "__main__":
    main()
