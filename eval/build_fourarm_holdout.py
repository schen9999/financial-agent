#!/usr/bin/env python3
"""Build the held-out judge-validation sample for the 2026-09-23 four-arm
comparison (kcf7s hosted, v924f financial-lora, 4nfsm qwen2.5-1.5b-instruct,
cnkp2 qwen2.5-7b-instruct; 40 tickers, judge v2).

RESERVED: this sample exists only for manual judge validation on the
four-arm claim set. It must not be used for prompt tuning, model selection,
threshold setting, or any other analysis — otherwise it stops being held out.

Method (also written to fourarm_holdout_method.json):
  - population: every judged claim with a CLAIM line in the four runs'
    findings (eval.label.collect_claims). Free-form verdicts without a CLAIM
    line (claim=null in the claims.jsonl) cannot be labeled and are excluded.
  - exclusions: any claim overlapping the dev set (sample.csv) or the v2
    held-out set (holdout_sample.csv), by normalized claim text or by sha256
    of the retrieved-source-context slice.
  - strata: (arm, judge verdict). Equal allocation per arm: UNSUPPORTED 6,
    INFERENCE 6, SUPPORTED 8; a stratum smaller than its target is taken
    whole. Within a stratum, a seeded shuffle, then draws honoring a cap of
    3 claims per (arm, ticker). Allocation is not proportional: stratum
    population and sample sizes are recorded so estimates can be reweighted.
  - blinding: the labeling CSV carries no run, arm, or judge verdict; those
    are only in the key. Label without opening the key.

Usage:
  python eval/build_fourarm_holdout.py           # refuses if the method file exists
  python eval/build_fourarm_holdout.py --force   # redraw; keeps provenance fields

The answer key is written to eval/judge_validation/ but is gitignored: keep it
outside the repository while the sample is unlabeled.
"""
import csv
import hashlib
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval.label import collect_claims  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "eval" / "judge_validation"
EXCLUDE = [OUT_DIR / "sample.csv", OUT_DIR / "holdout_sample.csv"]

# (label, findings dir, harness arm in the file names, workflow)
SOURCES = [
    ("hosted", "kcf7s", "baseline", "grounding-eval-extended-kcf7s"),
    ("financial-lora", "v924f", "local-model", "grounding-eval-extended-local-v924f"),
    ("qwen2.5-1.5b-instruct", "4nfsm", "local-model", "grounding-eval-extended-local-4nfsm"),
    ("qwen2.5-7b-instruct", "cnkp2", "local-model", "grounding-eval-extended-local-cnkp2"),
]
TARGETS = {"UNSUPPORTED": 6, "INFERENCE": 6, "SUPPORTED": 8}
TICKER_CAP = 3
SEED = 20260923


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace(",", "").replace('"', "")).strip().lower()


def _source_slice_sha(context: str) -> str:
    m = re.search(r"=== RETRIEVED SOURCE CONTEXT ===\n(.*?)(?=\n=== |\Z)", context, re.S)
    body = m.group(1) if m else context
    return hashlib.sha256(body.strip().encode("utf-8")).hexdigest()


def draw(rows: list[dict], seed: int = SEED) -> tuple[list[dict], dict]:
    """Stratified draw; returns (picked, strata {(arm, label): [population, drawn]})."""
    rng = random.Random(seed)
    picked, strata, per_ticker = [], {}, {}
    for arm in [s[0] for s in SOURCES]:
        for label in ("UNSUPPORTED", "INFERENCE", "SUPPORTED"):
            pool = sorted((r for r in rows if r["arm"] == arm and r["label"] == label),
                          key=lambda r: (r["ticker"], r["claim"]))
            rng.shuffle(pool)
            got = 0
            for r in pool:
                if got >= TARGETS[label]:
                    break
                if per_ticker.get((arm, r["ticker"]), 0) >= TICKER_CAP:
                    continue
                picked.append(r)
                per_ticker[(arm, r["ticker"])] = per_ticker.get((arm, r["ticker"]), 0) + 1
                got += 1
            strata[(arm, label)] = [len(pool), got]
    rng.shuffle(picked)
    return picked, strata


METHOD_FILE = OUT_DIR / "fourarm_holdout_method.json"
# Fields added by hand after the draw (where the key lives, when it was
# public). A rerun must never silently drop them.
PROVENANCE_KEYS = ("key_location", "key_exposure")


def check_can_write(path: Path, force: bool) -> None:
    """Refuse to redraw over an existing method file unless forced: the
    sample is reserved, and the file carries provenance a rerun would lose."""
    if path.exists() and not force:
        raise SystemExit(
            f"{path.name} already exists; refusing to overwrite the reserved sample "
            "and its provenance record. Rerun with --force to redraw (provenance "
            f"fields {', '.join(PROVENANCE_KEYS)} are carried over).")


def write_method(path: Path, method: dict, force: bool = False) -> dict:
    """Write the method record; with force, keep existing provenance fields."""
    check_can_write(path, force)
    if path.exists():
        old = json.loads(path.read_text(encoding="utf-8"))
        for k in PROVENANCE_KEYS:
            if k in old:
                method[k] = old[k]
    path.write_text(json.dumps(method, indent=2) + "\n", encoding="utf-8", newline="\n")
    return method


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true",
                    help="redraw even though fourarm_holdout_method.json exists")
    force = ap.parse_args(argv).force
    # Before writing anything: a refused run must leave all three files intact.
    check_can_write(METHOD_FILE, force)

    rows = []
    for label, run, harness_arm, wf in SOURCES:
        for r in collect_claims(REPO / f"eval/runs/raw/{run}-findings", [harness_arm], wf):
            rows.append({**r, "arm": label, "run": run})

    ex_claims, ex_shas = set(), set()
    for path in EXCLUDE:
        for r in csv.DictReader(path.open(encoding="utf-8")):
            ex_claims.add(_norm(r["claim"]))
            ex_shas.add(_source_slice_sha(r["context"]))
    before = len(rows)
    rows = [r for r in rows if _norm(r["claim"]) not in ex_claims
            and _source_slice_sha(r["context"]) not in ex_shas]
    excluded = before - len(rows)

    picked, strata = draw(rows)

    with open(OUT_DIR / "fourarm_holdout_sample.csv", "w", newline="\n", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "ticker", "claim", "context", "human_label"])
        for i, r in enumerate(picked):
            w.writerow([i, r["ticker"], r["claim"], r["context"], ""])
    with open(OUT_DIR / "fourarm_holdout_key.csv", "w", newline="\n", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "run", "arm", "judge_label", "judge_reason"])
        for i, r in enumerate(picked):
            w.writerow([i, r["run"], r["arm"], r["label"], r["reason"]])
    method = {
        "purpose": "manual judge validation on the 2026-09-23 four-arm claim set ONLY; "
                   "not for tuning, selection, or any other analysis",
        "runs": {s[0]: s[3] for s in SOURCES},
        "judge_prompt_version": "v2",
        "seed": SEED,
        "rng": "python random.Random(seed); per stratum: sort by (ticker, claim), "
               "shuffle, draw in order skipping (arm, ticker) pairs at the cap",
        "strata": "arm x judge verdict",
        "targets_per_arm": TARGETS,
        "ticker_cap_per_arm": TICKER_CAP,
        "population_claims": before,
        "excluded_overlap_with": [p.name for p in EXCLUDE],
        "excluded_count": excluded,
        "excluded_free_form_null_claims": "not in population (no CLAIM line to label)",
        "strata_population_and_drawn": {f"{a}|{l}": v for (a, l), v in strata.items()},
        "sample_size": len(picked),
    }
    write_method(METHOD_FILE, method, force)

    print(f"population {before}, overlap excluded {excluded}, sample {len(picked)}")
    for (a, l), (pop, got) in strata.items():
        print(f"  {a:<22} {l:<12} {got}/{pop}")


if __name__ == "__main__":
    main()
