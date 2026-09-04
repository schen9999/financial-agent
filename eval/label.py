#!/usr/bin/env python3
"""Build a human-labeling CSV from a grounding run's findings files.

Reads eval_findings/{TICKER}_{arm}.md files (written by grounding_check.py's
_save_findings), extracts every judged claim, stratifies a sample across the
judge's SUPPORTED / UNSUPPORTED / INFERENCE labels, and writes:

  <out>.csv       one row per sampled claim: id, provenance, ticker, claim,
                  context (what the labeler reads), empty human_label column.
                  The judge's verdict is NOT in this file.
  <out>_key.csv   id -> judge label + reason, for eval/agreement.py to join
                  after labeling. Do not open it while labeling.

Stratification keeps every claim from scarce strata (UNSUPPORTED first, then
INFERENCE) and fills the remainder with SUPPORTED claims, deterministically
(--seed).

Protocol caveat, disclosed: the findings files persist the retrieved source
context and the audited Exec Summary + Outlook, but NOT the four pre-written
sections the judge additionally saw. Human labels are therefore made against
slightly less context than the judge had; treat disagreements on
section-derived facts with that in mind.

Usage:
  python eval/label.py --arm baseline --sample 50 --seed 42 \
      --out eval/judge_validation/sample
"""
import argparse
import csv
import random
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_FINDINGS = REPO / "eval_findings"

_SECTION_RE = re.compile(
    r"## Retrieved source context\s*\n(.*?)\n## Audited[^\n]*\n(.*?)\n## Judge findings\s*\n(.*)",
    re.S,
)


def parse_findings_file(text: str) -> dict | None:
    """Split one findings .md into its three sections."""
    m = _SECTION_RE.search(text)
    if not m:
        return None
    return {"context": m.group(1).strip(), "audited": m.group(2).strip(),
            "findings": m.group(3).strip()}


def parse_claims(findings: str) -> list[dict]:
    """Extract (claim, label, reason) triples from judge findings text.
    Tolerates plain and bold (**...**) judge formatting, like
    agent/grounding.py's counters."""
    out = []
    for block in re.split(r"\*{0,2}CLAIM:\*{0,2}", findings)[1:]:
        claim = block.split("\n", 1)[0].strip().strip('"').strip()
        label_m = re.search(r"\*{0,2}LABEL:\*{0,2}\s*([A-Za-z]+)", block)
        reason_m = re.search(r"\*{0,2}REASON:\*{0,2}\s*(.+)", block)
        if claim and label_m and label_m.group(1).upper() in (
                "SUPPORTED", "UNSUPPORTED", "INFERENCE"):
            out.append({
                "claim": claim,
                "label": label_m.group(1).upper(),
                "reason": reason_m.group(1).strip() if reason_m else "",
            })
    return out


def collect_claims(findings_dir: Path, arms: list[str], provenance: str) -> list[dict]:
    """Claims from every requested arm. The arm goes to the KEY file only —
    the labeling CSV stays blind to which model produced each claim."""
    rows = []
    for arm in arms:
        for f in sorted(findings_dir.glob(f"*_{arm}.md")):
            ticker = f.name[: -len(f"_{arm}.md")]
            parsed = parse_findings_file(f.read_text(encoding="utf-8"))
            if not parsed:
                print(f"WARNING: could not parse {f.name}, skipping")
                continue
            context = (
                f"=== RETRIEVED SOURCE CONTEXT ===\n{parsed['context']}\n\n"
                f"=== AUDITED TEXT (Exec Summary + Outlook) ===\n{parsed['audited']}"
            )
            for c in parse_claims(parsed["findings"]):
                rows.append({"ticker": ticker, "arm": arm, "provenance": provenance,
                             "context": context, **c})
    return rows


def stratified_sample(rows: list[dict], n: int, seed: int) -> list[dict]:
    """All of the scarcest strata first (UNSUPPORTED, then INFERENCE), fill
    with SUPPORTED. Deterministic under --seed."""
    rng = random.Random(seed)
    by = {lab: [r for r in rows if r["label"] == lab]
          for lab in ("UNSUPPORTED", "INFERENCE", "SUPPORTED")}
    picked = []
    for lab in ("UNSUPPORTED", "INFERENCE", "SUPPORTED"):
        pool = by[lab][:]
        rng.shuffle(pool)
        take = min(len(pool), n - len(picked))
        picked.extend(pool[:take])
    rng.shuffle(picked)
    return picked


def main():
    ap = argparse.ArgumentParser(description="Build a judge-validation labeling CSV.")
    ap.add_argument("--findings-dir", default=str(DEFAULT_FINDINGS))
    ap.add_argument("--arms", nargs="+", default=["baseline"],
                    help="Which arms' findings to pool. Pool more than one when "
                         "a single arm lacks a stratum (a near-zero baseline "
                         "has no UNSUPPORTED claims to validate against). The "
                         "arm is recorded in the key file only — labeling is "
                         "blind to it.")
    ap.add_argument("--sample", type=int, default=50)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--provenance", required=True,
                    help="Run identity stamped on every row, e.g. "
                         "'local-run-2026-08-24-baseline'. Be exact — this is "
                         "what ties labels back to a real run.")
    ap.add_argument("--out", required=True, help="Output path stem (no extension)")
    args = ap.parse_args()

    rows = collect_claims(Path(args.findings_dir), args.arms, args.provenance)
    if not rows:
        sys.exit(f"No claims found for arms {args.arms} in {args.findings_dir}")
    sample = stratified_sample(rows, args.sample, args.seed)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(f"{out}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "provenance", "ticker", "claim", "context", "human_label"])
        for i, r in enumerate(sample):
            w.writerow([i, r["provenance"], r["ticker"], r["claim"], r["context"], ""])
    with open(f"{out}_key.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "arm", "judge_label", "judge_reason"])
        for i, r in enumerate(sample):
            w.writerow([i, r["arm"], r["label"], r["reason"]])

    strata = {lab: sum(1 for r in sample if r["label"] == lab)
              for lab in ("SUPPORTED", "UNSUPPORTED", "INFERENCE")}
    print(f"Wrote {len(sample)} claims to {out}.csv (+ key). "
          f"Strata: {strata}. Pool was {len(rows)} claims. "
          f"Label the human_label column SUPPORTED/UNSUPPORTED/INFERENCE "
          f"without opening the key file, then run eval/agreement.py.")


if __name__ == "__main__":
    main()
