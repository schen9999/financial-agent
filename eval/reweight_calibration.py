#!/usr/bin/env python3
"""Population-weighted judge recall and true unsupported rate from a
judge-label-stratified human sample.

Why this exists: the held-out judge-v2 validation (holdout_sample.csv) was
stratified by JUDGE label, 20 SUPPORTED / 15 UNSUPPORTED / 15 INFERENCE,
while judge-SUPPORTED is ~90% of claims in the real runs. Recall computed
on the sample as drawn (eval/agreement.py) weights the judge-SUPPORTED
stratum at 20/50 instead of ~90%, so it overstates recall. Precision
conditions on the judge label and needs no reweighting.

Method, per stratum k in {SUPPORTED, UNSUPPORTED, INFERENCE} (judge label):
  p_k      = human-UNSUPPORTED / n_k in the labeled sample
  N_k      = judge-label count in the population run (count_labels_deduped
             over the run's findings files)
  T        = sum_k N_k * p_k   (estimated truly-unsupported claims)
  recall   = N_U * p_U / T
  true rate = T / sum_k N_k
Point estimates use p_k = x_k / n_k. 95% intervals: Monte Carlo over
independent Jeffreys Beta(x_k + 0.5, n_k - x_k + 0.5) posteriors per
stratum, 200k draws, fixed seed, 2.5/97.5 percentiles. Population counts
N_k are treated as fixed (they are the full runs, not samples). The pooled
row sums N_k across runs and reuses the same per-stratum draws.

Usage:
  python eval/reweight_calibration.py \\
      --labeled eval/judge_validation/holdout_sample.csv \\
      --key eval/judge_validation/holdout_key.csv \\
      --run j4cnp eval/runs/j4cnp-claims.jsonl eval/runs/raw/j4cnp-findings \\
      --run lsnnc eval/runs/lsnnc-claims.jsonl eval/runs/raw/lsnnc-findings
  Repeat --labeled/--key (paired in order) to pool several samples per
  judge-label stratum, e.g. the holdout plus calibration_batch.csv.
"""
import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval.agreement import LABELS, load_pairs  # noqa: E402
from eval.label import count_labels_deduped, parse_findings_file  # noqa: E402
from eval.section_attribution import attribute, bucket, section_texts  # noqa: E402

DRAWS = 200_000
SEED = 20260924


def stratum_counts(pairs: list[tuple[str, str]]) -> dict:
    """judge label -> (human-UNSUPPORTED count x_k, stratum size n_k)."""
    return {k: (sum(1 for j, h in pairs if j == k and h == "UNSUPPORTED"),
                sum(1 for j, _ in pairs if j == k))
            for k in LABELS}


def population_counts(claims_path: Path, findings_dir: Path) -> dict:
    """Judge-label counts from count_labels_deduped over the findings files,
    cross-checked against the run's claims.jsonl (they must agree)."""
    tot = {k: 0 for k in LABELS}
    for f in sorted(findings_dir.glob("*.md")):
        parsed = parse_findings_file(f.read_text(encoding="utf-8"))
        if not parsed:
            sys.exit(f"could not parse {f}")
        c = count_labels_deduped(parsed["findings"])
        for k in LABELS:
            tot[k] += c[k.lower()]
    jsonl = {k: 0 for k in LABELS}
    for line in claims_path.read_text(encoding="utf-8").splitlines():
        jsonl[json.loads(line)["judge_label"]] += 1
    if jsonl != tot:
        sys.exit(f"{claims_path}: claims.jsonl counts {jsonl} disagree with "
                 f"deduped findings counts {tot}")
    return tot


def section_population_counts(claims_path: Path, findings_dir: Path) -> dict:
    """bucket -> judge-label counts, attributing each claim row exactly as
    eval/section_attribution.py does (fine-tune-owned / other / unattributed)."""
    secs = section_texts(findings_dir)
    out = {}
    for line in claims_path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        b = bucket(attribute(r["claim"], secs.get((r["ticker"], r["arm"]), {})))
        out.setdefault(b, {k: 0 for k in LABELS})[r["judge_label"]] += 1
    return out


def reweight(strata: dict, pop: dict, p: dict | None = None) -> tuple[float, float]:
    """(recall, true unsupported rate) for population counts `pop` and
    per-stratum human-UNSUPPORTED proportions `p` (default: x_k / n_k)."""
    if p is None:
        p = {k: x / n for k, (x, n) in strata.items()}
    t = sum(pop[k] * p[k] for k in LABELS)
    total = sum(pop.values())
    recall = pop["UNSUPPORTED"] * p["UNSUPPORTED"] / t if t else float("nan")
    return recall, t / total


def posterior_draws(strata: dict, draws: int = DRAWS, seed: int = SEED) -> list[dict]:
    rng = random.Random(seed)
    return [{k: rng.betavariate(x + 0.5, n - x + 0.5)
             for k, (x, n) in strata.items()} for _ in range(draws)]


def interval(values: list[float]) -> tuple[float, float]:
    v = sorted(values)
    return v[int(0.025 * (len(v) - 1))], v[int(0.975 * (len(v) - 1))]


def summarize(strata: dict, pop: dict, draws: list[dict]) -> dict:
    recall, rate = reweight(strata, pop)
    sims = [reweight(strata, pop, d) for d in draws]
    return {"recall": recall, "recall_ci": interval([s[0] for s in sims]),
            "rate": rate, "rate_ci": interval([s[1] for s in sims]),
            "flagged_rate": pop["UNSUPPORTED"] / sum(pop.values())}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--labeled", required=True, action="append",
                    help="repeatable, paired in order with --key; samples are "
                         "pooled per judge-label stratum")
    ap.add_argument("--key", required=True, action="append")
    ap.add_argument("--use", action="append",
                    help="optional, paired in order with --labeled: the judge "
                         "labels to take from that sample, comma-separated "
                         "(e.g. UNSUPPORTED,INFERENCE), or ALL (default)")
    ap.add_argument("--run", nargs=3, action="append", required=True,
                    metavar=("LABEL", "CLAIMS_JSONL", "FINDINGS_DIR"))
    ap.add_argument("--by-section", action="store_true",
                    help="Also report each run's fine-tune-owned / "
                         "other-sections / unattributed buckets.")
    ap.add_argument("--draws", type=int, default=DRAWS)
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    if len(args.labeled) != len(args.key):
        sys.exit("--labeled and --key must be given the same number of times")
    uses = args.use or ["ALL"] * len(args.labeled)
    if len(uses) != len(args.labeled):
        sys.exit("--use, when given, must be given once per --labeled")
    pairs = []
    for lab, key, use in zip(args.labeled, args.key, uses):
        keep = set(LABELS) if use.upper() == "ALL" else \
            {u.strip().upper() for u in use.split(",")}
        if not keep <= set(LABELS):
            sys.exit(f"--use {use}: labels must be from {LABELS} or ALL")
        pairs += [p for p in load_pairs(Path(lab), Path(key)) if p[0] in keep]
    strata = stratum_counts(pairs)
    pops = {label: population_counts(Path(c), Path(f)) for label, c, f in args.run}
    if len(pops) > 1:
        pops["pooled"] = {k: sum(p[k] for p in pops.values()) for k in LABELS}
    draws = posterior_draws(strata, args.draws, args.seed)

    print("Method: per-judge-label stratum p_k = human-UNSUPPORTED / n_k;")
    print("  recall = N_U p_U / sum_k N_k p_k; true rate = sum_k N_k p_k / N.")
    print(f"  95% intervals: Monte Carlo over independent Jeffreys "
          f"Beta(x+0.5, n-x+0.5) per stratum, {args.draws} draws, "
          f"seed {args.seed}.")
    print("\nLabeled sample strata (judge label: human-UNSUPPORTED / n):")
    for k, (x, n) in strata.items():
        print(f"  {k:<12} {x}/{n}")
    for label, pop in pops.items():
        report(label, pop, strata, draws)
    if args.by_section:
        print("\nPer section bucket (attribution as eval/section_attribution.py;"
              " p_k from the whole sample, not per section):")
        for label, c, f in args.run:
            for b, pop in sorted(section_population_counts(Path(c), Path(f)).items()):
                report(f"{label} / {b}", pop, strata, draws)


def report(label: str, pop: dict, strata: dict, draws: list[dict]):
    s = summarize(strata, pop, draws)
    counts = " / ".join(f"{pop[k]} {k[0]}" for k in LABELS)
    print(f"\n{label} ({counts}):")
    print(f"  judge-flagged unsupported rate : {s['flagged_rate']:.2%}")
    if pop["UNSUPPORTED"]:
        print(f"  population-weighted recall     : {s['recall']:.1%} "
              f"(95% CI {s['recall_ci'][0]:.1%}-{s['recall_ci'][1]:.1%})")
    else:
        print("  population-weighted recall     : 0 (judge flagged none)")
    print(f"  estimated true unsupported rate: {s['rate']:.1%} "
          f"(95% CI {s['rate_ci'][0]:.1%}-{s['rate_ci'][1]:.1%})")


if __name__ == "__main__":
    main()
