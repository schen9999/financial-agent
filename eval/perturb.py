#!/usr/bin/env python3
"""Synthetic failure injection for judge validation.

Takes a completed run's findings artifacts (retrieved context + audited
text, from eval_findings/) and produces perturbed fixtures with KNOWN
ground truth, three controlled failure types:

  numeric_swap   a number that appears in both the audited text and the
                 context is changed in the audited text -> that claim is
                 now UNSUPPORTED, and the new value is the tag needle.
  drop_support   the context lines containing a number the audited text
                 cites are deleted -> the (unchanged) claim loses its
                 support; the original value is the needle.
  insert_claim   a fabricated, plausible, specific sentence is appended
                 to the audited text; a distinctive phrase is the needle.

Each fixture records: context, audited text, perturbation type, the tag
needle (how a judge flag is matched back to the injection), and a note.
eval/critic_check.py runs the real judge over the fixtures and scores
recall/precision against these tags.

Disclosed caveat: findings artifacts do not persist the pre-written
sections the judge normally also receives, so fixtures are audited
against raw source context only — judge precision measured on fixtures
is a lower bound.

Usage:
  python eval/perturb.py --arms baseline --count 20 --seed 42 \
      --provenance local-run-2026-08-24 --out eval/perturbed/fixtures.jsonl
"""
import argparse
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval.label import parse_findings_file  # noqa: E402

REPO = Path(__file__).resolve().parents[1]

# Number with at least two digits, optionally decimal/comma/percent — the
# kind of specific figure the judge audits.
_NUM_RE = re.compile(r"\d[\d,]*\.\d+|\d[\d,]{1,}")

# (sentence template, needle template) — the needle is a long distinctive
# fragment so a judge flag matches this insertion and nothing else.
_INSERT_TEMPLATES = [
    ('Management has guided to {pct}% revenue growth for the next fiscal year.',
     '{pct}% revenue growth'),
    ('The company expects operating margin to expand to {pct}% by year-end.',
     'margin to expand to {pct}%'),
    ('Analysts cited in the filings project a price target of ${num} per share.',
     'price target of ${num}'),
    ('The board approved a ${num} billion incremental buyback program.',
     '${num} billion incremental buyback'),
    ('Management reiterated a {pct}% market-share objective in its latest call.',
     '{pct}% market-share objective'),
]


def _numbers_in(text: str) -> list[str]:
    return _NUM_RE.findall(text)


def _shared_numbers(audited: str, context: str) -> list[str]:
    """Numbers cited in the audited text that literally appear in the context
    (the plausibly-supported ones), deduplicated, order-stable."""
    ctx = context
    seen, out = set(), []
    for n in _numbers_in(audited):
        # >=3 digits: skips weak targets like the 52 in "52-week", whose
        # perturbation is noisy and whose needle collides with other figures.
        # Year-like integers (19xx/20xx) are dates, not metrics — excluded.
        if (n in ctx and n not in seen
                and len(n.replace(",", "").replace(".", "")) >= 3
                and not re.fullmatch(r"(19|20)\d{2}", n)):
            seen.add(n)
            out.append(n)
    return out


def _swap_value(n: str, rng: random.Random) -> str:
    """A same-shaped but different number (x1.17–1.62, decimals preserved)."""
    raw = float(n.replace(",", ""))
    factor = rng.uniform(1.17, 1.62)
    decimals = len(n.split(".")[1]) if "." in n else 0
    new = f"{raw * factor:.{decimals}f}"
    if "," in n:
        new = f"{float(new):,.{decimals}f}"
    return new


def make_numeric_swap(ticker, context, audited, rng):
    for n in _shared_numbers(audited, context):
        new = _swap_value(n, rng)
        if new != n and new not in context:
            return {
                "type": "numeric_swap", "ticker": ticker,
                "context": context,
                "audited": audited.replace(n, new, 1),
                "needle": new,
                "note": f"swapped first occurrence of {n} -> {new} in audited text",
            }
    return None


def make_drop_support(ticker, context, audited, rng):
    for n in _shared_numbers(audited, context):
        kept = [ln for ln in context.split("\n") if n not in ln]
        if len(kept) < context.count("\n") + 1:  # something was dropped
            return {
                "type": "drop_support", "ticker": ticker,
                "context": "\n".join(kept),
                "audited": audited,
                "needle": n,
                "note": f"dropped context lines containing {n}",
            }
    return None


def make_insert_claim(ticker, context, audited, rng):
    tmpl, needle_tmpl = rng.choice(_INSERT_TEMPLATES)
    pct = rng.choice([9, 12, 14, 17, 21, 23])
    num = rng.choice([185, 240, 310, 415, 3.5, 7.5])
    sentence = tmpl.format(pct=pct, num=num)
    needle = needle_tmpl.format(pct=pct, num=num)
    if sentence in context or sentence in audited:
        return None
    return {
        "type": "insert_claim", "ticker": ticker,
        "context": context,
        "audited": audited.rstrip() + " " + sentence,
        "needle": needle,
        "note": f"appended fabricated sentence: {sentence}",
    }


def build_fixtures(findings_dir: Path, arms: list[str], count: int, seed: int,
                   provenance: str) -> list[dict]:
    rng = random.Random(seed)
    # One (context, audited) pair per (ticker, arm) file.
    pairs = []
    for arm in arms:
        for f in sorted(findings_dir.glob(f"*_{arm}.md")):
            parsed = parse_findings_file(f.read_text(encoding="utf-8"))
            if parsed:
                pairs.append((f.name[: -len(f"_{arm}.md")], parsed["context"],
                              parsed["audited"]))
    if not pairs:
        sys.exit(f"no findings for arms {arms} in {findings_dir}")

    makers = [make_numeric_swap, make_drop_support, make_insert_claim]
    fixtures, i, seen = [], 0, set()
    while len(fixtures) < count and i < count * 10:
        ticker, context, audited = pairs[i % len(pairs)]
        maker = makers[len(fixtures) % len(makers)]
        fx = maker(ticker, context, audited, rng)
        i += 1
        # A (ticker, type, needle) repeat is the same fixture again — a
        # deterministic maker re-visiting a file must not shrink the real N.
        if fx and (ticker, fx["type"], fx["needle"]) not in seen:
            seen.add((ticker, fx["type"], fx["needle"]))
            fx["id"] = len(fixtures)
            fx["provenance"] = provenance
            fixtures.append(fx)
    if len(fixtures) < count:
        sys.exit(f"could only build {len(fixtures)}/{count} fixtures")
    return fixtures


def main():
    ap = argparse.ArgumentParser(description="Build perturbed judge fixtures.")
    ap.add_argument("--findings-dir", default=str(REPO / "eval_findings"))
    ap.add_argument("--arms", nargs="+", default=["baseline"])
    ap.add_argument("--count", type=int, default=20)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--provenance", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    fixtures = build_fixtures(Path(args.findings_dir), args.arms, args.count,
                              args.seed, args.provenance)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for fx in fixtures:
            f.write(json.dumps(fx) + "\n")
    by_type = {}
    for fx in fixtures:
        by_type[fx["type"]] = by_type.get(fx["type"], 0) + 1
    print(f"Wrote {len(fixtures)} fixtures to {out}: {by_type}")


if __name__ == "__main__":
    main()
