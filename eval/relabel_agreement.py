#!/usr/bin/env python3
"""Test-retest analysis of the blind judge-SUPPORTED relabel (2026-09-24).

relabel_S.csv holds 123 judge-SUPPORTED claims, the calibration batch's 103
and the held-out sample's 20, relabeled blind with the source hidden
(eval/build_relabel_s.py). This joins each relabel back to its original
label through relabel_S_key.csv and reports, per source:

  - human-UNSUPPORTED rate, original vs relabel, with Wilson 95% intervals
  - Fisher exact, relabel holdout vs relabel batch
  - the 3x3 original-vs-relabel table, exact agreement, Cohen's kappa
  - how the original UNSUPPORTED labels moved
and, for the batch's first pass: the UNSUPPORTED rate by labeling position,
by arm, and by audited section; and the relabel's rate by section.

Usage:
  python eval/relabel_agreement.py
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval.agreement import LABELS, cohens_kappa  # noqa: E402
from eval.build_relabel_s import KEY_FILE, SAMPLE_FILE, SOURCES, read_csv  # noqa: E402
from eval.label_cli import locate_section  # noqa: E402
from eval.stats import fisher_exact, format_rate_ci  # noqa: E402

FIRST = {"calibration_batch": "first pass 2026-09-24", "holdout": "labels 2026-09-06"}
POSITION_SPLIT = 34  # batch rows 1-34 vs 35-150, in labeling (file) order


def joined(sample=SAMPLE_FILE, key=KEY_FILE, sources=SOURCES) -> dict:
    """source -> list of dicts: original, relabel, arm, position, section."""
    rel = {r["id"]: r for r in read_csv(sample)}
    orig = {name: read_csv(path) for name, path, _ in sources}
    pos = {name: {r["id"]: i + 1 for i, r in enumerate(rows)} for name, rows in orig.items()}
    by_id = {name: {r["id"]: r for r in rows} for name, rows in orig.items()}
    out = {name: [] for name, _, _ in sources}
    for k in read_csv(key):
        o = by_id[k["source"]][k["source_id"]]
        r = rel[k["id"]]
        if (o["claim"], o["context"]) != (r["claim"], r["context"]):
            sys.exit(f"relabel id {k['id']} does not match {k['source']} id {k['source_id']}")
        out[k["source"]].append({
            "original": o["human_label"].strip().upper(),
            "relabel": r["human_label"].strip().upper(),
            "arm": k["arm"], "position": pos[k["source"]][k["source_id"]],
            "section": locate_section(r["claim"], r["context"])})
    return out


def rate(rows, field) -> tuple[int, int]:
    return sum(r[field] == "UNSUPPORTED" for r in rows), len(rows)


def line(label, u, n) -> str:
    return f"  {label:<34} {u}/{n} = {format_rate_ci(u, n)}"


def main():
    data = joined()
    missing = [s for s, rows in data.items() for r in rows if not r["relabel"]]
    if missing:
        sys.exit(f"{len(missing)} relabel rows are blank; finish labeling first")

    print("human-UNSUPPORTED rate on judge-SUPPORTED claims")
    for s, rows in data.items():
        print(line(f"{s}, {FIRST[s]}", *rate(rows, "original")))
        print(line(f"{s}, blind relabel", *rate(rows, "relabel")))
    (a, n), (b, m) = rate(data["holdout"], "relabel"), rate(data["calibration_batch"], "relabel")
    print(f"  Fisher, relabel holdout vs relabel batch: p = {fisher_exact(a, n - a, b, m - b):.4f}")
    allrows = [r for rows in data.values() for r in rows]
    print(line("both sources, blind relabel", *rate(allrows, "relabel")))

    print("\nTest-retest (rows = original, cols = relabel)")
    for s, rows in data.items():
        pairs = [(r["original"], r["relabel"]) for r in rows]
        print(f"  {s} ({FIRST[s]} vs relabel), n = {len(rows)}")
        print(f"    {'':<13}" + "".join(f"{lab:>13}" for lab in LABELS))
        for o in LABELS:
            print(f"    {o:<13}" + "".join(
                f"{sum(1 for x, y in pairs if x == o and y == h):>13}" for h in LABELS))
        same = sum(x == y for x, y in pairs)
        print(f"    exact agreement {same}/{len(pairs)}; "
              f"Cohen's kappa {cohens_kappa(pairs):.3f}")
        was_u = [y for x, y in pairs if x == "UNSUPPORTED"]
        print(f"    original UNSUPPORTED {len(was_u)}: kept {was_u.count('UNSUPPORTED')}, "
              f"to SUPPORTED {was_u.count('SUPPORTED')}, to INFERENCE {was_u.count('INFERENCE')}")

    batch = data["calibration_batch"]
    print("\nBatch first pass, human-UNSUPPORTED on judge-SUPPORTED claims")
    early = [r for r in batch if r["position"] <= POSITION_SPLIT]
    late = [r for r in batch if r["position"] > POSITION_SPLIT]
    (a, n), (b, m) = rate(early, "original"), rate(late, "original")
    print(line(f"rows 1-{POSITION_SPLIT}", a, n))
    print(line(f"rows {POSITION_SPLIT + 1}-150", b, m))
    print(f"  Fisher, by position: p = {fisher_exact(a, n - a, b, m - b):.4f}")
    for arm in sorted({r["arm"] for r in batch}):
        print(line(f"arm {arm}", *rate([r for r in batch if r["arm"] == arm], "original")))
    for sec in ("Executive Summary", "Outlook", "not located"):
        print(line(f"section {sec}", *rate([r for r in batch if r["section"] == sec], "original")))

    print("\nBlind relabel by audited section, both sources")
    for sec in ("Executive Summary", "Outlook", "not located"):
        rows = [r for r in allrows if r["section"] == sec]
        inf = sum(r["relabel"] == "INFERENCE" for r in rows)
        print(line(f"section {sec}", *rate(rows, "relabel")) + f"   (INFERENCE {inf}/{len(rows)})")


if __name__ == "__main__":
    main()
