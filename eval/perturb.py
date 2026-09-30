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


# --- Numeric-check injections ------------------------------------------------
# Known-error fixtures for agent/numeric_check.py recall. No LLM: each
# injection edits one labeled stock-field number that the check already
# compares (status "checked") in a brief with zero findings, so any finding
# the edited copy produces is attributable to the injection.

NUMERIC_PERTURBATIONS = ("x10", "x100", "x0.01", "sign_flip", "swap_fields",
                         "unit_down", "placeholder")
# Template fillers a generator leaves behind. The first five are the forms
# seen in committed briefs; the rest are plausible ones the detector was not
# written against, so placeholder recall is not 100% by construction.
PLACEHOLDER_TOKENS = ("[City Name]", "[Company]", "[X]", "[insert date]",
                      "$X", "N/A", "{market_cap}", "TBD", "XX", "[●]")
_UNIT_DOWN = {"trillion": "billion", "billion": "million", "T": "B", "B": "M",
              "bn": "mn", "tn": "bn"}
_FORM_CLASS = {"market_cap": "money", "revenue": "money", "net_income": "money",
               "current_price": "price", "week_52_high": "price",
               "week_52_low": "price", "pe_ratio": "pe", "forward_pe": "pe"}


def _num_span(text: str, span: tuple[int, int]):
    """The number inside a binding's value text: (start, end, num_text)."""
    from agent.numeric_check import _VALUE_RE
    vm = _VALUE_RE.match(text, span[0])
    if not vm or vm.end() > span[1] + 1:
        return None
    s, e = vm.span("num")
    return s, e, vm


def _scaled(num_text: str, factor: float) -> str:
    """num_text scaled by factor, keeping comma style and enough decimals to
    stay at >= 3 significant digits."""
    import math
    raw = float(num_text.replace(",", "")) * factor
    dec = len(num_text.split(".")[1]) if "." in num_text else 0
    if raw:
        dec = max(dec, 2 - int(math.floor(math.log10(abs(raw)))))
    out = f"{raw:,.{dec}f}" if "," in num_text else f"{raw:.{dec}f}"
    return out


def _edit(sections, index, start, end, new):
    out = list(sections)
    heading, text = out[index]
    out[index] = (heading, text[:start] + new + text[end:])
    return out


def inject_numeric(sections: list[tuple[str, str]], bindings: list[dict],
                   kind: str, rng: random.Random) -> dict | None:
    """One injection of `kind` into a copy of `sections`, or None when the
    brief has no eligible binding. Returns {kind, sections, targets
    [(section_index, field)], expect ("mismatch"|"placeholder"), note}."""
    pool = [b for b in bindings if b["status"] == "checked"
            and b.get("stated_value")]
    rng.shuffle(pool)
    for b in pool:
        i, span = b["section_index"], b["span"]
        text = sections[i][1]
        ns = _num_span(text, span)
        if not ns:
            continue
        s, e, vm = ns
        num = text[s:e]
        if kind in ("x10", "x100", "x0.01"):
            factor = {"x10": 10, "x100": 100, "x0.01": 0.01}[kind]
            new = _scaled(num, factor)
            return {"kind": kind, "sections": _edit(sections, i, s, e, new),
                    "targets": [(i, b["field"])], "expect": "mismatch",
                    "note": f"{b['field']}: {num} -> {new}"}
        if kind == "sign_flip":
            if b["sign_fixed"]:
                continue
            vs, ve = span
            val = text[vs:ve]
            m = re.search(r"[-−]", val[: e - vs])
            new_text = (text[:vs + m.start()] + text[vs + m.end():] if m
                        else text[:vs] + "-" + text[vs:])
            out = list(sections)
            out[i] = (sections[i][0], new_text)
            return {"kind": kind, "sections": out,
                    "targets": [(i, b["field"])], "expect": "mismatch",
                    "note": f"{b['field']}: sign flipped on {b['stated']}"}
        if kind == "unit_down":
            unit = vm.group("unit") or vm.group("abbr")
            if unit not in _UNIT_DOWN:
                continue
            us, ue = vm.span("unit") if vm.group("unit") else vm.span("abbr")
            new = _UNIT_DOWN[unit]
            return {"kind": kind, "sections": _edit(sections, i, us, ue, new),
                    "targets": [(i, b["field"])], "expect": "mismatch",
                    "note": f"{b['field']}: {unit} -> {new}"}
        if kind == "placeholder":
            tok = rng.choice(PLACEHOLDER_TOKENS)
            vs, ve = span
            return {"kind": kind, "sections": _edit(sections, i, vs, ve, tok),
                    "targets": [(i, b["field"])], "expect": "placeholder",
                    "note": f"{b['field']}: {b['stated']} -> {tok}",
                    "token": tok}
        if kind == "swap_fields":
            # Same-form partners only (money<->money, price<->price,
            # P/E<->P/E): the realistic confusion. A cross-form swap
            # ("market cap of 45.3%") fails the form test and is unchecked
            # by design.
            for o in pool:
                if (o is b or o["field"] == b["field"]
                        or (b.get("in_range") and o.get("in_range"))
                        or _FORM_CLASS.get(o["field"]) != _FORM_CLASS.get(b["field"])
                        or o["section_index"] != i
                        or abs(o["stated_value"] - b["stated_value"])
                        <= 0.05 * max(abs(o["stated_value"]), abs(b["stated_value"]))):
                    continue
                (a0, a1), (b0, b1) = sorted([span, o["span"]])
                if a1 > b0:
                    continue
                t = text
                t = t[:a0] + t[b0:b1] + t[a1:b0] + t[a0:a1] + t[b1:]
                out = list(sections)
                out[i] = (sections[i][0], t)
                return {"kind": kind, "sections": out,
                        "targets": [(i, b["field"]), (i, o["field"])],
                        "expect": "mismatch",
                        "note": f"swapped {b['field']} {b['stated']} <-> "
                                f"{o['field']} {o['stated']}"}
            continue
    return None


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
