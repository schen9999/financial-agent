#!/usr/bin/env python3
"""Build the judge-UNSUPPORTED + judge-INFERENCE relabel sample.

Why: the blind relabel of the judge-SUPPORTED rows (relabel_S.csv) withdrew
39 of the calibration batch's 42 first-pass UNSUPPORTED labels, so the
batch's first pass skews toward UNSUPPORTED. The batch's U and I strata come
from that same pass (judge-UNSUPPORTED rows were 21/23 human-UNSUPPORTED vs
9/15 in the holdout, p = 0.039), so they are relabeled the same way.

Output (same blind shape as relabel_S.csv, via build_relabel_s.build):
  relabel_UI.csv      id, ticker, claim, context, human_label (blank);
                      77 rows = the batch's 23 U + 24 I and the holdout's
                      15 U + 15 I judge-labeled rows, shuffled with SEED;
                      fresh ids 0..76, no source and no judge label.
  relabel_UI_key.csv  id -> source set, source id, run, arm, judge label.
                      Gitignored; do not open while labeling.

Usage:
  python eval/build_relabel_ui.py           # refuses if relabel_UI.csv exists
  python eval/build_relabel_ui.py --force
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval.build_relabel_s import OUT_DIR, build  # noqa: E402

LABELS = ("UNSUPPORTED", "INFERENCE")
SAMPLE_FILE = OUT_DIR / "relabel_UI.csv"
KEY_FILE = OUT_DIR / "relabel_UI_key.csv"
SEED = 20260926


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true")
    build(LABELS, SAMPLE_FILE, KEY_FILE, SEED, ap.parse_args(argv).force)


if __name__ == "__main__":
    main()
