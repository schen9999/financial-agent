#!/usr/bin/env python3
"""Build the HELD-OUT judge-validation sample from the 40-ticker A/B runs.

Draws claims from the j4cnp (baseline) and lsnnc (local-model) findings,
stratified by (arm, judge label) with a global cap of 3 claims per ticker,
oversampling the scarce labels toward roughly 15 UNSUPPORTED /
15 INFERENCE / 20 SUPPORTED. Within each label the two arms are drawn
round-robin so neither dominates a stratum.

Held-out means held out: rows are checked against the 50-claim DEV set
(eval/judge_validation/sample.csv — the set judge v2's rules were tuned
on) by normalized claim text AND by sha256 of the retrieved-source-context
slice; any match is excluded. The output is written UNLABELED — labeling
happens blind, without opening the key file, exactly as for the dev set.
The labeling context includes the pre-written sections (extended findings
format), so labelers see what the judge saw.

Usage:
  python eval/build_holdout.py   # writes holdout_sample.csv + holdout_key.csv
"""
import csv
import hashlib
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval.label import collect_claims

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "eval" / "judge_validation"
DEV_SAMPLE = OUT_DIR / "sample.csv"

SOURCES = [
    (REPO / "eval/runs/j4cnp-findings", "baseline",
     "grounding-eval-extended-j4cnp"),
    (REPO / "eval/runs/lsnnc-findings", "local-model",
     "grounding-eval-extended-local-lsnnc"),
]
TARGETS = {"UNSUPPORTED": 15, "INFERENCE": 15, "SUPPORTED": 20}
TICKER_CAP = 3
SEED = 42


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace(",", "").replace('"', "")).strip().lower()


def _source_slice_sha(context: str) -> str:
    """sha256 of the retrieved-source-context portion of a composed labeling
    context — comparable across formats (the dev set's contexts lack the
    pre-written sections, so whole-string hashes never match)."""
    m = re.search(r"=== RETRIEVED SOURCE CONTEXT ===\n(.*?)(?=\n=== |\Z)",
                  context, re.S)
    body = m.group(1) if m else context
    return hashlib.sha256(body.strip().encode("utf-8")).hexdigest()


def main():
    rows = []
    for findings_dir, arm, provenance in SOURCES:
        rows.extend(collect_claims(findings_dir, [arm], provenance))

    # Hold-out guard against the dev set.
    dev = list(csv.DictReader(DEV_SAMPLE.open(encoding="utf-8")))
    dev_claims = {_norm(r["claim"]) for r in dev}
    dev_shas = {_source_slice_sha(r["context"]) for r in dev}
    before = len(rows)
    rows = [r for r in rows if _norm(r["claim"]) not in dev_claims
            and _source_slice_sha(r["context"]) not in dev_shas]
    excluded = before - len(rows)

    rng = random.Random(SEED)
    per_ticker = {}
    picked = []

    def take(row):
        picked.append(row)
        per_ticker[row["ticker"]] = per_ticker.get(row["ticker"], 0) + 1

    # Scarce labels first so the ticker cap never squeezes them out.
    for label in ("UNSUPPORTED", "INFERENCE", "SUPPORTED"):
        pools = {}
        for _, arm, _p in SOURCES:
            pool = [r for r in rows if r["label"] == label and r["arm"] == arm]
            rng.shuffle(pool)
            pools[arm] = pool
        want = TARGETS[label]
        got = 0
        # Round-robin across arms, larger pool first, honoring the cap.
        order = sorted(pools, key=lambda a: -len(pools[a]))
        while got < want and any(pools.values()):
            for arm in order:
                if got >= want:
                    break
                while pools[arm]:
                    r = pools[arm].pop()
                    if per_ticker.get(r["ticker"], 0) < TICKER_CAP:
                        take(r)
                        got += 1
                        break
        if got < want:
            print(f"NOTE: {label} pool exhausted at {got}/{want} "
                  f"(ticker cap {TICKER_CAP})")
    rng.shuffle(picked)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "holdout_sample.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "provenance", "ticker", "claim", "context",
                    "human_label"])
        for i, r in enumerate(picked):
            w.writerow([i, r["provenance"], r["ticker"], r["claim"],
                        r["context"], ""])
    with open(OUT_DIR / "holdout_key.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "arm", "judge_label", "judge_reason"])
        for i, r in enumerate(picked):
            w.writerow([i, r["arm"], r["label"], r["reason"]])

    strata = {}
    for r in picked:
        strata[(r["label"], r["arm"])] = strata.get((r["label"], r["arm"]), 0) + 1
    print(f"holdout: {len(picked)} claims -> {OUT_DIR / 'holdout_sample.csv'}")
    print(f"dev-set overlap excluded: {excluded} "
          f"(checked claim text + source-context sha)")
    for (label, arm), n in sorted(strata.items()):
        print(f"  {label:<12} {arm:<12} {n}")
    print(f"tickers used: {len(per_ticker)}, max per ticker: "
          f"{max(per_ticker.values())}")


if __name__ == "__main__":
    main()
