#!/usr/bin/env python3
"""Attribute judged claims to the pre-written section they restate, and
report unsupported rates on fine-tune-owned sections vs the rest.

Why: the judge audits the Executive Summary + Outlook of the SYNTHESIS, but
the local-model arm's fine-tune writes only two of the four pre-written
input sections (Financial Health and the risk-factors section — the model
titles it variously, e.g. "Primary Risk Factors Disclosed"). To ask whether
the local arm's extra unsupported claims trace to fine-tune-authored
content, each claim is attributed to the pre-written section whose text it
restates.

Method, stated for the docs that cite these numbers: a claim is attributed
by (a) normalized-substring containment in a section's text, else (b) the
section with the highest word-overlap score (|claim words ∩ section words| /
|claim words|) when that score is ≥ 0.6; otherwise it is UNATTRIBUTED
(synthesis-original phrasing — roughly a fifth of claims). Attribution is a
heuristic over paraphrased text, not ground truth; rates on the buckets are
indicative, the overall A/B is the measured result.

Usage:
  python eval/section_attribution.py \
      --run eval/runs/j4cnp-claims.jsonl eval/runs/raw/j4cnp-findings \
      --run eval/runs/lsnnc-claims.jsonl eval/runs/raw/lsnnc-findings
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval.label import parse_findings_file
from eval.stats import fisher_exact, format_rate_ci

# The fine-tune serves Financial Health + Risk Factors in the local-model
# arm; Haiku keeps the other two sections in every arm.
OWNED = ("financial-health", "risk-factors")

_SECTION_HEAD_RE = re.compile(r"^### ([^\n]+)\n(.*?)(?=^### |\Z)", re.M | re.S)


def canonical_section(heading: str) -> str:
    h = heading.lower()
    if "financial health" in h:
        return "financial-health"
    if "risk factor" in h:
        return "risk-factors"
    if "recent development" in h:
        return "recent-developments"
    if "filing highlight" in h or "sec filing" in h:
        return "sec-filing-highlights"
    return "other"


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace(",", "").replace('"', "")).strip().lower()


def _words(s: str) -> set:
    return set(re.findall(r"[a-z0-9.%$]+", _norm(s)))


def section_texts(findings_dir: Path) -> dict:
    """(ticker, arm) -> {canonical section: (normalized text, word set)}."""
    out = {}
    for f in sorted(findings_dir.glob("*_*.md")):
        ticker, arm = f.stem.rsplit("_", 1)
        parsed = parse_findings_file(f.read_text(encoding="utf-8"))
        if not parsed or "section_block" not in parsed:
            print(f"WARNING: no pre-written sections in {f.name}, skipping")
            continue
        secs = {}
        for head, body in _SECTION_HEAD_RE.findall(parsed["section_block"]):
            secs[canonical_section(head)] = (_norm(body), _words(body))
        out[(ticker, arm)] = secs
    return out


def attribute(claim: str | None, secs: dict, overlap_min: float = 0.6) -> str | None:
    """Canonical section name, or None when unattributed."""
    if not claim or not secs:
        return None
    nc, wc = _norm(claim), _words(claim)
    for name, (text, _) in secs.items():
        if nc in text:
            return name
    best, score = None, 0.0
    for name, (_, wv) in secs.items():
        ov = len(wc & wv) / max(1, len(wc))
        if ov > score:
            best, score = name, ov
    return best if score >= overlap_min else None


def bucket(section: str | None) -> str:
    if section is None:
        return "unattributed"
    return "fine-tune-owned" if section in OWNED else "other-sections"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", nargs=2, action="append", required=True,
                    metavar=("CLAIMS_JSONL", "FINDINGS_DIR"))
    args = ap.parse_args()

    per = {}  # (arm, bucket) -> [unsupported, total]
    for claims_path, findings_dir in args.run:
        secs = section_texts(Path(findings_dir))
        for line in Path(claims_path).read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            b = bucket(attribute(r["claim"], secs.get((r["ticker"], r["arm"]), {})))
            cell = per.setdefault((r["arm"], b), [0, 0])
            cell[1] += 1
            if r["judge_label"] == "UNSUPPORTED":
                cell[0] += 1

    arms = sorted({a for a, _ in per})
    print(f"{'arm':<14} {'bucket':<16} {'unsupported':<24}")
    for arm in arms:
        for b in ("fine-tune-owned", "other-sections", "unattributed"):
            u, n = per.get((arm, b), (0, 0))
            print(f"{arm:<14} {b:<16} {u}/{n} = {format_rate_ci(u, n)}")
    if len(arms) == 2:
        for b in ("fine-tune-owned", "other-sections", "unattributed"):
            (u1, n1), (u2, n2) = (per.get((a, b), (0, 0)) for a in arms)
            p = fisher_exact(u1, n1 - u1, u2, n2 - u2)
            print(f"Fisher {arms[0]} vs {arms[1]} on {b}: p = {p:.4f}")


if __name__ == "__main__":
    main()
