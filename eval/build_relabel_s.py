#!/usr/bin/env python3
"""Build the judge-SUPPORTED relabel sample (relabel review of 2026-09-24).

Why: on judge-SUPPORTED claims the calibration batch found 42/103
human-UNSUPPORTED against 1/20 in the held-out sample (Fisher p = 0.0016).
Relabeling both sets' judge-SUPPORTED rows together, blind to which set a
row came from, separates a labeling-standard shift from sampling.

Output (same blind shape as calibration_batch.csv):
  relabel_S.csv      id, ticker, claim, context, human_label (blank);
                     123 rows = the batch's 103 + the holdout's 20
                     judge-SUPPORTED rows, shuffled with SEED; ids are fresh
                     0..122, and nothing in a row names its source.
  relabel_S_key.csv  id -> source set, source id, run, arm, judge label.
                     Gitignored; do not open while labeling.

Every row in this sample is judge-SUPPORTED by construction; that is the
only judge information the labeler can infer.

Usage:
  python eval/build_relabel_s.py           # refuses if relabel_S.csv exists
  python eval/build_relabel_s.py --force
"""
import argparse
import csv
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "eval" / "judge_validation"
SAMPLE_FILE = OUT_DIR / "relabel_S.csv"
KEY_FILE = OUT_DIR / "relabel_S_key.csv"
# (source name, sample csv, key csv)
SOURCES = [
    ("calibration_batch", OUT_DIR / "calibration_batch.csv",
     OUT_DIR / "calibration_batch_key.csv"),
    ("holdout", OUT_DIR / "holdout_sample.csv", OUT_DIR / "holdout_key.csv"),
]
SEED = 20260925


def read_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(line for line in f if not line.startswith("#"))
                    if path.name.endswith("_key.csv") else csv.DictReader(f))


def collect(sources=SOURCES) -> list[dict]:
    rows = []
    for name, sample, key in sources:
        judge = {r["id"]: r for r in read_csv(key)}
        for r in read_csv(sample):
            k = judge[r["id"]]
            if k["judge_label"].strip().upper() == "SUPPORTED":
                rows.append({"source": name, "source_id": r["id"],
                             "run": k.get("run", ""), "arm": k["arm"],
                             "judge_label": "SUPPORTED", "ticker": r["ticker"],
                             "claim": r["claim"], "context": r["context"]})
    return rows


def shuffle(rows: list[dict], seed: int = SEED) -> list[dict]:
    rows = sorted(rows, key=lambda r: (r["source"], int(r["source_id"])))
    random.Random(seed).shuffle(rows)
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true")
    if SAMPLE_FILE.exists() and not ap.parse_args(argv).force:
        sys.exit(f"{SAMPLE_FILE.name} exists; refusing to overwrite (use --force)")
    rows = shuffle(collect())
    with open(SAMPLE_FILE, "w", newline="\n", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "ticker", "claim", "context", "human_label"])
        for i, r in enumerate(rows):
            w.writerow([i, r["ticker"], r["claim"], r["context"], ""])
    with open(KEY_FILE, "w", newline="\n", encoding="utf-8") as f:
        f.write(f"# relabel_S seed {SEED}; sources: "
                + ", ".join(f"{n} {sum(r['source'] == n for r in rows)}" for n, _, _ in SOURCES)
                + "\n")
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "source", "source_id", "run", "arm", "judge_label"])
        for i, r in enumerate(rows):
            w.writerow([i, r["source"], r["source_id"], r["run"], r["arm"], r["judge_label"]])
    counts = {n: sum(r["source"] == n for r in rows) for n, _, _ in SOURCES}
    print(f"{SAMPLE_FILE.name}: {len(rows)} rows {counts}, seed {SEED}; key -> {KEY_FILE.name}")


if __name__ == "__main__":
    main()
