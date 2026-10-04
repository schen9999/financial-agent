#!/usr/bin/env python3
"""Claim density per run: how much checkable content each brief put in front
of the judge, and what the judge chose to audit.

The unsupported rate is unsupported / judged claims, so an arm that states
fewer checkable facts — or whose text the judge segments into fewer claims —
gets a lower rate for free. For each run's findings directory this reports,
per ticker:

  claims, supported      judged claims and SUPPORTED claims (mean, min)
  numeric / qualitative  claims whose quoted text contains a digit / does not.
                         The judge prompt asks for quantitative figures, named
                         milestones and forward-looking numbers; whether it
                         also audits qualitative phrases varies from brief to
                         brief, and that variation moves the claim count
  0-qual tickers         briefs where the judge audited numbers only
  audited words, numbers size of the audited text (Executive Summary +
                         Outlook) and how many numbers it contains

Sensitivity: "numeric" is eval.label.numeric_claim_counts — the quoted claim
contains a digit — so a positional phrase such as "near 52-week highs"
counts as numeric though it quotes no figure. The report therefore also
gives the numeric counts without the claims that are numeric only through
"52-week" (strict). The definition itself is not changed here: it is used by
the harness inside the pinned image.

Found on the 2026-10-03 smokes (hosted hm527 vs CPU SLM 9jddz, same image):
90 vs 53 claims over the same 10 tickers.

  python eval/claim_density.py --run hm527 eval/runs/raw/hm527-findings \\
      --run 9jddz eval/runs/raw/9jddz-findings --tickers AMZN GOOGL V
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval.label import (count_labels_deduped, numeric_claim_counts, parse_claims,  # noqa: E402
                        parse_findings_file)
from eval.stats import format_rate_ci  # noqa: E402

_NUMBER = re.compile(r"\d[\d,.]*")
PHRASE = "52-week"  # digits that are a label, not a figure


def strict_numeric_counts(findings: str) -> dict:
    """numeric_claim_counts without the claims whose only digits are in
    "52-week": (total, unsupported)."""
    total = unsupported = 0
    for c in parse_claims(findings):
        if re.search(r"\d", re.sub(r"(?i)52[- ]week", "", c["claim"])):
            total += 1
            unsupported += c["label"] == "UNSUPPORTED"
    return {"total": total, "unsupported": unsupported}


def brief_density(findings_text: str) -> dict | None:
    """One findings file -> its claim and audited-text counts."""
    p = parse_findings_file(findings_text)
    if not p:
        return None
    claims = parse_claims(p["findings"])
    counts = count_labels_deduped(p["findings"])
    num = numeric_claim_counts(p["findings"])
    strict = strict_numeric_counts(p["findings"])
    body = re.sub(r"(?m)^(#+ .*|---|\*This brief is for informational.*)$", "", p["audited"])
    return {"claims": counts["total"], "supported": counts["supported"],
            "numeric": num["total"], "numeric_unsupported": num["unsupported"],
            "numeric_strict": strict["total"],
            "numeric_strict_unsupported": strict["unsupported"],
            "qualitative": len(claims) - num["total"],
            "words": len(body.split()), "numbers": len(_NUMBER.findall(body))}


def run_density(findings_dir: Path) -> dict:
    """{ticker: brief_density} for every findings file of the run."""
    out = {}
    for f in sorted(findings_dir.rglob("*.md")):
        d = brief_density(f.read_text(encoding="utf-8"))
        if d:
            out[f.stem.split("_")[0]] = d
    return out


def summarize(per: dict) -> dict:
    n = len(per) or 1
    mean = lambda k: sum(d[k] for d in per.values()) / n  # noqa: E731
    return {"tickers": len(per), "claims": sum(d["claims"] for d in per.values()),
            "numeric": sum(d["numeric"] for d in per.values()),
            "numeric_unsupported": sum(d["numeric_unsupported"] for d in per.values()),
            "numeric_min": min((d["numeric"] for d in per.values()), default=0),
            "numeric_strict": sum(d["numeric_strict"] for d in per.values()),
            "numeric_strict_unsupported": sum(d["numeric_strict_unsupported"]
                                              for d in per.values()),
            "numeric_strict_mean": round(sum(d["numeric_strict"] for d in per.values()) / n, 2),
            **{f"{k}_mean": round(mean(k), 2)
               for k in ("claims", "supported", "numeric", "qualitative", "words", "numbers")},
            "claims_min": min((d["claims"] for d in per.values()), default=0),
            "claims_min_tickers": sorted(t for t, d in per.items()
                                         if d["claims"] == min(x["claims"] for x in per.values())),
            "zero_qualitative": sorted(t for t, d in per.items() if d["qualitative"] == 0)}


def print_report(runs: dict, tickers=()) -> None:
    """`runs` is {label: run_density(...)}."""
    print(f"{'run':<14} {'tickers':>7} {'claims':>6} {'claims/t':>8} {'min':>4} "
          f"{'numeric/t':>9} {'min':>4} {'qual/t':>7} {'0-qual':>6} {'words/t':>8} {'numbers/t':>9}")
    for label, per in runs.items():
        s = summarize(per)
        print(f"{label:<14} {s['tickers']:>7} {s['claims']:>6} {s['claims_mean']:>8.1f} "
              f"{s['claims_min']:>4} {s['numeric_mean']:>9.1f} {s['numeric_min']:>4} "
              f"{s['qualitative_mean']:>7.1f} {len(s['zero_qualitative']):>6} "
              f"{s['words_mean']:>8.0f} {s['numbers_mean']:>9.1f}")
    print("numeric claims (quote a figure), unsupported rate:")
    for label, per in runs.items():
        s = summarize(per)
        print(f"  {label:<14} {s['numeric_unsupported']}/{s['numeric']} = "
              f"{format_rate_ci(s['numeric_unsupported'], s['numeric'])}")
    print(f'sensitivity, numeric claims without those numeric only through "{PHRASE}":')
    for label, per in runs.items():
        s = summarize(per)
        print(f"  {label:<14} {s['numeric_strict_mean']:.2f}/ticker "
              f"({s['numeric'] - s['numeric_strict']} of {s['numeric']} dropped)   unsupported "
              f"{s['numeric_strict_unsupported']}/{s['numeric_strict']} = "
              f"{format_rate_ci(s['numeric_strict_unsupported'], s['numeric_strict'])}")
    for label, per in runs.items():
        s = summarize(per)
        print(f"{label}: min claims at {', '.join(s['claims_min_tickers'])}; the judge audited "
              f"numbers only for {', '.join(s['zero_qualitative']) or 'no ticker'}")
    if tickers:
        print(f"\n{'ticker':<7} {'run':<10} {'claims':>6} {'numeric':>7} {'qual':>5} "
              f"{'words':>6} {'numbers':>7}")
        for t in tickers:
            for label, per in runs.items():
                d = per.get(t)
                if d:
                    print(f"{t:<7} {label:<10} {d['claims']:>6} {d['numeric']:>7} "
                          f"{d['qualitative']:>5} {d['words']:>6} {d['numbers']:>7}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run", nargs=2, action="append", required=True,
                    metavar=("LABEL", "FINDINGS_DIR"))
    ap.add_argument("--tickers", nargs="*", default=[],
                    help="also print these tickers' rows for every run")
    args = ap.parse_args(argv)
    print_report({label: run_density(Path(d)) for label, d in args.run}, args.tickers)
    return 0


if __name__ == "__main__":
    sys.exit(main())
