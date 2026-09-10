#!/usr/bin/env python3
"""Judge-vs-human agreement on a labeled claims sample.

Reads the labeling CSV produced by eval/label.py after a human has filled
the human_label column, joins the hidden judge verdicts from the key file,
and reports:

  - Cohen's kappa over the three labels (SUPPORTED/UNSUPPORTED/INFERENCE)
  - Precision and recall of the judge on the UNSUPPORTED class, treating
    the human labels as ground truth (the class the gate rides on),
    each with a Wilson 95% interval (eval/stats.py)
  - The full 3x3 confusion matrix

Usage:
  python eval/agreement.py --labeled eval/judge_validation/sample.csv \
      --key eval/judge_validation/sample_key.csv
"""
import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval.stats import format_rate_ci  # noqa: E402

LABELS = ("SUPPORTED", "UNSUPPORTED", "INFERENCE")


def cohens_kappa(pairs: list[tuple[str, str]]) -> float:
    """Cohen's kappa for two raters over categorical labels."""
    n = len(pairs)
    if n == 0:
        raise ValueError("no labeled pairs")
    po = sum(1 for a, b in pairs if a == b) / n
    pe = 0.0
    for lab in LABELS:
        pa = sum(1 for a, _ in pairs if a == lab) / n
        pb = sum(1 for _, b in pairs if b == lab) / n
        pe += pa * pb
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1 - pe)


def precision_recall_unsupported(pairs: list[tuple[str, str]]):
    """(judge, human) pairs -> precision/recall of judge on UNSUPPORTED with
    human as truth. Returns dict with counts so intervals can be attached."""
    tp = sum(1 for j, h in pairs if j == "UNSUPPORTED" and h == "UNSUPPORTED")
    fp = sum(1 for j, h in pairs if j == "UNSUPPORTED" and h != "UNSUPPORTED")
    fn = sum(1 for j, h in pairs if j != "UNSUPPORTED" and h == "UNSUPPORTED")
    return {"tp": tp, "fp": fp, "fn": fn,
            "precision_n": tp + fp, "recall_n": tp + fn}


def load_pairs(labeled: Path, key: Path) -> list[tuple[str, str]]:
    with open(key, newline="", encoding="utf-8") as f:
        judge = {row["id"]: row["judge_label"].strip().upper()
                 for row in csv.DictReader(f)}
    pairs, unlabeled, bad = [], 0, []
    with open(labeled, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            h = row["human_label"].strip().upper()
            if not h:
                unlabeled += 1
                continue
            if h not in LABELS:
                bad.append((row["id"], row["human_label"]))
                continue
            pairs.append((judge[row["id"]], h))
    if bad:
        sys.exit(f"Invalid human labels (use SUPPORTED/UNSUPPORTED/INFERENCE): {bad}")
    if unlabeled:
        print(f"NOTE: {unlabeled} rows still unlabeled — excluded.")
    return pairs


def main():
    ap = argparse.ArgumentParser(description="Judge-vs-human agreement report.")
    ap.add_argument("--labeled", required=True)
    ap.add_argument("--key", required=True)
    args = ap.parse_args()

    pairs = load_pairs(Path(args.labeled), Path(args.key))
    if not pairs:
        sys.exit("No labeled rows found — fill human_label first.")

    n = len(pairs)
    kappa = cohens_kappa(pairs)
    pr = precision_recall_unsupported(pairs)

    print("=" * 70)
    print(f"  JUDGE VALIDATION — {n} human-labeled claims")
    print("=" * 70)
    print("  Confusion (rows = judge, cols = human):")
    print(f"  {'':<14}" + "".join(f"{lab:>13}" for lab in LABELS))
    for j in LABELS:
        row = [sum(1 for a, b in pairs if a == j and b == h) for h in LABELS]
        print(f"  {j:<14}" + "".join(f"{v:>13}" for v in row))
    print(f"\n  Cohen's kappa (3-class)      : {kappa:.3f}")
    if pr["precision_n"]:
        print(f"  Judge precision, UNSUPPORTED : "
              f"{format_rate_ci(pr['tp'], pr['precision_n'])}  "
              f"({pr['tp']}/{pr['precision_n']})")
    else:
        print("  Judge precision, UNSUPPORTED : n/a (judge flagged none)")
    if pr["recall_n"]:
        print(f"  Judge recall,    UNSUPPORTED : "
              f"{format_rate_ci(pr['tp'], pr['recall_n'])}  "
              f"({pr['tp']}/{pr['recall_n']})")
    else:
        print("  Judge recall,    UNSUPPORTED : n/a (human flagged none)")
    print("=" * 70)


if __name__ == "__main__":
    main()
