#!/usr/bin/env python3
"""Draw the 150-claim judge-v2 calibration batch from the 40-ticker A/B runs.

Why: the held-out validation put 20 labels in the judge-SUPPORTED stratum,
and one human-UNSUPPORTED claim among those 20 decides most of the
population-weighted recall (eval/reweight_calibration.py: 25.4% on j4cnp,
CI 7.4-58.4%). This batch spends most of its labels where recall is decided.

Method (also written to calibration_batch_method.json):
  - population: every judged claim with a CLAIM line in j4cnp (baseline)
    and lsnnc (local-model), via eval.label.collect_claims. Free-form
    verdicts without a CLAIM line cannot be labeled and are not in the pool.
  - exclusions: any claim in the dev set (sample.csv) or the v2 held-out set
    (holdout_sample.csv) by normalized claim text, plus the dev set by
    source-context sha256 (as eval/build_holdout.py). Context sha is not
    used against the holdout: the holdout drew from these same runs, so
    every ticker's context matches and the check would empty the pool.
  - strata: judge label, then arm. Targets: SUPPORTED 100, INFERENCE 25,
    UNSUPPORTED 25, total 150. Within a label, arms are allocated in
    proportion to the runs' judge-label counts (largest remainder); an arm
    short of its share gives the rest to the other arm; a label short of
    its target is taken whole and the shortfall goes to SUPPORTED, the
    stratum that drives recall, so the batch stays at 150.
  - draw: per (label, arm), sort by (ticker, claim), seeded shuffle, take
    the first n: a simple random draw within the stratum.
  - ticker cap: at most 4 SUPPORTED claims per ticker, applied only if it
    is not binding on the random draw. If any ticker exceeds 4, the cap is
    NOT applied (it would stop the draw being simple random) and its would-be
    effect is reported instead.
  - blinding: the labeling CSV carries no run, arm, provenance, or judge
    label (provenance would reveal the arm, and 22 of 23 eligible
    UNSUPPORTED claims are local-model). Rows are shuffled. Label without
    opening the key.

Usage:
  python eval/build_calibration_batch.py           # refuses if the method file exists
  python eval/build_calibration_batch.py --force   # redraw

The answer key is written to eval/judge_validation/ but is gitignored, like
the four-arm key: keep it out of the public repository while unlabeled.
"""
import argparse
import csv
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval.build_fourarm_holdout import check_can_write, write_method  # noqa: E402
from eval.build_holdout import _norm, _source_slice_sha  # noqa: E402
from eval.label import collect_claims  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "eval" / "judge_validation"
DEV = OUT_DIR / "sample.csv"
HOLDOUT = OUT_DIR / "holdout_sample.csv"
METHOD_FILE = OUT_DIR / "calibration_batch_method.json"
SAMPLE_FILE = OUT_DIR / "calibration_batch.csv"
KEY_FILE = OUT_DIR / "calibration_batch_key.csv"

# (run, harness arm, workflow)
SOURCES = [
    ("j4cnp", "baseline", "grounding-eval-extended-j4cnp"),
    ("lsnnc", "local-model", "grounding-eval-extended-local-lsnnc"),
]
LABELS = ("SUPPORTED", "UNSUPPORTED", "INFERENCE")
TARGETS = {"SUPPORTED": 100, "INFERENCE": 25, "UNSUPPORTED": 25}
TOTAL = 150
FILL_FROM = "SUPPORTED"
TICKER_CAP = 4
SEED = 20260924


def allocate(total: int, pop: dict, avail: dict) -> dict:
    """Split `total` across arms in proportion to `pop` (largest remainder),
    capped by `avail`; any arm's shortfall moves to arms with room."""
    base = sum(pop.values())
    quota = {a: total * pop[a] / base for a in pop}
    out = {a: int(q) for a, q in quota.items()}
    for a in sorted(pop, key=lambda a: -(quota[a] - out[a]))[: total - sum(out.values())]:
        out[a] += 1
    out = {a: min(n, avail[a]) for a, n in out.items()}
    short = total - sum(out.values())
    for a in sorted(pop, key=lambda a: -pop[a]):
        extra = min(short, avail[a] - out[a])
        out[a] += extra
        short -= extra
    return out


def plan(pop: dict, avail: dict) -> dict:
    """(label, arm) -> draw size. pop/avail: {label: {arm: count}}."""
    sizes = {}
    for label in ("UNSUPPORTED", "INFERENCE"):
        want = min(TARGETS[label], sum(avail[label].values()))
        sizes.update({(label, a): n for a, n in
                      allocate(want, pop[label], avail[label]).items()})
    fill = TOTAL - sum(sizes.values())
    sizes.update({(FILL_FROM, a): n for a, n in
                  allocate(fill, pop[FILL_FROM], avail[FILL_FROM]).items()})
    return sizes


def draw(pool: list[dict], sizes: dict, seed: int = SEED) -> list[dict]:
    rng = random.Random(seed)
    picked = []
    for (label, arm), n in sorted(sizes.items()):
        stratum = sorted((r for r in pool if r["label"] == label and r["arm"] == arm),
                         key=lambda r: (r["ticker"], r["claim"]))
        rng.shuffle(stratum)
        picked.extend(stratum[:n])
    rng.shuffle(picked)
    return picked


def cap_effect(picked: list[dict], cap: int = TICKER_CAP) -> dict:
    """How a per-ticker cap on the SUPPORTED draw would bind."""
    per = {}
    for r in picked:
        if r["label"] == "SUPPORTED":
            per[r["ticker"]] = per.get(r["ticker"], 0) + 1
    over = {t: n for t, n in sorted(per.items()) if n > cap}
    return {"cap": cap, "tickers_in_draw": len(per), "max_per_ticker": max(per.values()),
            "tickers_over_cap": over,
            "draws_displaced": sum(n - cap for n in over.values()),
            "applied": not over}


def run_label_counts(claims_path: Path) -> dict:
    counts = {k: 0 for k in LABELS}
    for line in claims_path.read_text(encoding="utf-8").splitlines():
        counts[json.loads(line)["judge_label"]] += 1
    return counts


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true",
                    help="redraw even though calibration_batch_method.json exists")
    force = ap.parse_args(argv).force
    check_can_write(METHOD_FILE, force)

    rows = []
    for run, arm, wf in SOURCES:
        rows.extend({**r, "run": run} for r in
                    collect_claims(REPO / f"eval/runs/raw/{run}-findings", [arm], wf))
    dev = list(csv.DictReader(DEV.open(encoding="utf-8")))
    ho = list(csv.DictReader(HOLDOUT.open(encoding="utf-8")))
    ex_claims = {_norm(r["claim"]) for r in dev + ho}
    dev_shas = {_source_slice_sha(r["context"]) for r in dev}
    pool = [r for r in rows if _norm(r["claim"]) not in ex_claims
            and _source_slice_sha(r["context"]) not in dev_shas]

    # Run populations (the reweighting N_k) from the claims files, which
    # match eval/label.py count_labels_deduped over the findings.
    run_pop = {run: run_label_counts(REPO / f"eval/runs/{run}-claims.jsonl")
               for run, _, _ in SOURCES}
    arm_of = {run: arm for run, arm, _ in SOURCES}
    pop = {k: {arm_of[run]: run_pop[run][k] for run in run_pop} for k in LABELS}
    avail = {k: {arm: sum(1 for r in pool if r["label"] == k and r["arm"] == arm)
                 for _, arm, _ in SOURCES} for k in LABELS}
    sizes = plan(pop, avail)
    picked = draw(pool, sizes)
    cap = cap_effect(picked)  # non-binding cap == the random draw unchanged

    strata = {f"{k}|{arm}": {"run_population": pop[k][arm],
                             "eligible_pool": avail[k][arm],
                             "drawn": sizes[(k, arm)]}
              for k in LABELS for _, arm, _ in SOURCES}
    header = [
        "calibration batch 2026-09-24; judge v2; runs j4cnp (baseline), lsnnc (local-model)",
        f"seed {SEED}; draw per (judge label, arm): sort by (ticker, claim), shuffle, first n",
        "stratum: run_population / eligible_pool / drawn",
        *(f"  {s}: {v['run_population']} / {v['eligible_pool']} / {v['drawn']}"
          for s, v in strata.items()),
        f"ticker cap {TICKER_CAP} on SUPPORTED: {'applied (non-binding)' if cap['applied'] else 'NOT applied (binding)'}",
    ]

    with open(SAMPLE_FILE, "w", newline="\n", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "ticker", "claim", "context", "human_label"])
        for i, r in enumerate(picked):
            w.writerow([i, r["ticker"], r["claim"], r["context"], ""])
    with open(KEY_FILE, "w", newline="\n", encoding="utf-8") as f:
        f.writelines(f"# {line}\n" for line in header)
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "run", "arm", "judge_label", "judge_reason"])
        for i, r in enumerate(picked):
            w.writerow([i, r["run"], r["arm"], r["label"], r["reason"]])

    method = {
        "purpose": "judge v2 calibration: population-weighted recall and true "
                   "unsupported rate on j4cnp/lsnnc (eval/reweight_calibration.py)",
        "runs": {run: wf for run, _, wf in SOURCES},
        "judge_prompt_version": "v2",
        "seed": SEED,
        "rng": "python random.Random(seed); per (judge label, arm) in sorted order: "
               "sort by (ticker, claim), shuffle, take first n; then shuffle rows",
        "targets": TARGETS,
        "total": TOTAL,
        "shortfall_filled_from": FILL_FROM,
        "arm_allocation": "proportional to run judge-label counts, largest remainder, "
                          "capped by eligible pool",
        "run_population_counts": run_pop,
        "parsed_claims": len(rows),
        "excluded_overlap": len(rows) - len(pool),
        "excluded_overlap_with": [DEV.name + " (claim text, context sha)",
                                  HOLDOUT.name + " (claim text)"],
        "excluded_free_form_null_claims": "not in pool (no CLAIM line to label)",
        "strata": strata,
        "ticker_cap": cap,
        "sample_size": len(picked),
        "key_location": f"{KEY_FILE.name}, gitignored; never committed while unlabeled",
    }
    write_method(METHOD_FILE, method, force)

    print("\n".join(header))
    print(f"parsed {len(rows)}, overlap excluded {len(rows) - len(pool)}, "
          f"sample {len(picked)}")
    print(f"ticker cap: {json.dumps(cap)}")


if __name__ == "__main__":
    main()
