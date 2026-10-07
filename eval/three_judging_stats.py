#!/usr/bin/env python3
"""Grounding statistics under the three-judgings protocol (adopted
2026-10-06; eval-methodology, "the judge's run-to-run noise on identical
inputs").

Each run is judged three times: the original judging (the findings in
eval/runs/raw/<run>-findings/) and two re-judges (eval/rejudge_runs.py
output folders). Counting is rejudge_runs.summarize's, so every figure
reproduces the per-judging totals already recorded.

Per run: the unsupported rate of each judging (all claims; numeric claims),
their mean and range.

Between two runs: a paired, ticker-level bootstrap (eval/multi_arm_stats.py
`paired`, 10,000 resamples, seeded) on each ticker's unsupported rate
averaged over the three judgings — it carries both the judge's noise and
the clustering of claims within briefs — with the exact sign test. A
judging in which a ticker has no claims (or no numeric claims) is left out
of that ticker's average; a ticker with none in any judging is left out.
Fisher on each single judging is printed for continuity only, labelled per
judging; the three judgings are never pooled into one test.

  python eval/three_judging_stats.py --runs 9jzmj 8vpq6 p9jr2 4hsn2 nstp9 \\
      --judgings raw eval/runs/rejudge-2026-10-06 eval/runs/rejudge-2026-10-06-r2 \\
      --pairs 4hsn2:nstp9 4hsn2:8vpq6 nstp9:8vpq6 8vpq6:p9jr2 9jzmj:4hsn2 p9jr2:nstp9
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from eval import multi_arm_stats as mas  # noqa: E402
from eval import rejudge_runs as rj  # noqa: E402
from eval.stats import fisher_exact, format_rate_ci  # noqa: E402


def judging_counts(run: str, source: str) -> dict:
    """{ticker: summarize(...)} for one judging of one run."""
    out = {}
    for stem, parsed in rj.briefs(run):
        if source == "raw":
            findings = parsed["findings"]
        else:
            p = Path(source)
            p = p if p.is_absolute() else ROOT / p
            findings = (p / run / f"{stem}.findings.txt").read_text(encoding="utf-8")
        out[stem.rsplit("_", 1)[0]] = rj.summarize(findings, parsed["audited"])
    return out


def ticker_rates(judgings: list[dict]) -> dict:
    """{ticker: {"rate", "numeric_rate"}} averaged over the judgings that
    give the ticker a denominator."""
    out = {}
    for t in judgings[0]:
        row = {}
        for field, u, n in (("rate", "unsupported", "total"),
                            ("numeric_rate", "unsupported_numeric", "numeric")):
            vals = [j[t][u] / j[t][n] for j in judgings if j[t][n]]
            if vals:
                row[field] = sum(vals) / len(vals)
        out[t] = row
    return out


def totals(j: dict) -> dict:
    keys = ("unsupported", "total", "unsupported_numeric", "numeric")
    return {k: sum(v[k] for v in j.values()) for k in keys}


def run_lines(run: str, js: list[dict]) -> list[str]:
    tt = [totals(j) for j in js]
    L = [f"  {run}"]
    for name, u, n in (("all claims", "unsupported", "total"), ("numeric", "unsupported_numeric", "numeric")):
        rates = [t[u] / t[n] for t in tt]
        each = "; ".join(f"j{i + 1} {t[u]}/{t[n]} = {t[u] / t[n]:.2%}" for i, t in enumerate(tt))
        L.append(f"    {name:10}: mean {sum(rates) / 3:.2%} (range {min(rates):.2%}–{max(rates):.2%}); {each}")
    return L


def paired_only(a: dict, b: dict, field: str) -> dict:
    common = {t for t in a if field in a[t]} & {t for t in b if field in b[t]}
    return mas.paired({t: a[t] for t in common}, {t: b[t] for t in common}, field)


def pair_lines(a: str, b: str, ja: list[dict], jb: list[dict]) -> list[str]:
    ra, rb = ticker_rates(ja), ticker_rates(jb)
    L = [f"  {a} - {b}"]
    for field in ("rate", "numeric_rate"):
        pr = paired_only(ra, rb, field)
        L.append(f"    {field:12}: ticker-averaged {pr['mean_a']:.2%} vs {pr['mean_b']:.2%}, diff "
                 f"{pr['mean_diff'] * 100:+.2f} pts (95% bootstrap CI {pr['ci'][0] * 100:+.2f} to "
                 f"{pr['ci'][1] * 100:+.2f}) over {pr['tickers']} tickers; {a} higher on {pr['a_more']}, "
                 f"equal {pr['equal']}, {b} higher {pr['b_more']}; sign p = {mas.fmt_p(pr['sign_p'])}")
    fis = []
    for i, (x, y) in enumerate(zip(ja, jb)):
        tx, ty = totals(x), totals(y)
        p = fisher_exact(tx["unsupported"], tx["total"] - tx["unsupported"],
                         ty["unsupported"], ty["total"] - ty["unsupported"])
        fis.append(f"j{i + 1} p = {mas.fmt_p(p)}")
    L.append(f"    per-judging Fisher, all claims (continuity only): {'; '.join(fis)}")
    return L


def report(runs: list[str], sources: list[str], pairs: list[tuple[str, str]]) -> list[str]:
    js = {r: [judging_counts(r, s) for s in sources] for r in runs}
    L = [f"Three judgings per run: {', '.join(sources)}", "Per run (judge v2; j1 = original judging)"]
    for r in runs:
        L += run_lines(r, js[r])
        tt = totals(js[r][0])
        L.append(f"    j1 Wilson: {format_rate_ci(tt['unsupported'], tt['total'])}")
    L.append("Between runs: paired ticker-level bootstrap on per-ticker rates averaged over the three judgings")
    for a, b in pairs:
        L += pair_lines(a, b, js[a], js[b])
    return L


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--judgings", nargs=3, required=True)
    ap.add_argument("--pairs", nargs="+", default=[], metavar="A:B")
    args = ap.parse_args(argv)
    lines = report(args.runs, args.judgings, [tuple(p.split(":")) for p in args.pairs])
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
