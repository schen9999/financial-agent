#!/usr/bin/env python3
"""Run the real grounding critic over perturbed fixtures and score it.

For each fixture (eval/perturb.py) the judge (agent/grounding.py — the same
temperature-0 Sonnet judge the eval DAG and the inline critic share) audits
the perturbed text against the perturbed context. A fixture counts as
DETECTED when any judge-UNSUPPORTED claim contains the fixture's tag needle
(comma-insensitive). Reported, each with a Wilson 95% interval:

  recall     detected fixtures / all fixtures       (the assertion rides here)
  precision  detected fixtures / all UNSUPPORTED flags that matched a needle
             plus flags that matched none (false positives *relative to the
             injection tags* — a lower bound, since fixtures omit the
             pre-written sections the judge normally also sees)

Spends real Anthropic credits (~20 Sonnet judge calls). The credit guard
(eval/runtime_guards.py) fails loudly on an empty balance.

Usage:
  python eval/critic_check.py --fixtures eval/perturbed/fixtures.jsonl \
      [--json-out result.json]
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dotenv import load_dotenv  # noqa: E402
load_dotenv()

from agent.grounding import extract_claims, grade_brief  # noqa: E402
from eval.runtime_guards import check_fatal_api_error  # noqa: E402
from eval.stats import format_rate_ci, wilson_interval  # noqa: E402

SECTION_BLOCK_NOTE = (
    "(The pre-written sections are not available for this audit; judge the "
    "text strictly against the raw source data above.)"
)


def _norm(s: str) -> str:
    return s.replace(",", "").lower()


def needle_in(needle: str, text: str) -> bool:
    """Digit-boundary-aware needle match: '67' must not match inside '167'."""
    import re
    return re.search(rf"(?<![\d.]){re.escape(_norm(needle))}(?![\d])", _norm(text)) is not None


def run_fixtures(fixtures: list[dict]) -> dict:
    detected, false_pos, rows = 0, 0, []
    for fx in fixtures:
        try:
            grade = grade_brief(fx["context"], SECTION_BLOCK_NOTE, fx["audited"])
        except Exception as e:  # noqa: BLE001
            check_fatal_api_error(e)
            raise
        unsupported = extract_claims(grade.findings, "UNSUPPORTED")
        hit = any(needle_in(fx["needle"], c) for c in unsupported)
        extra = sum(1 for c in unsupported if not needle_in(fx["needle"], c))
        detected += hit
        false_pos += extra
        rows.append({"id": fx["id"], "type": fx["type"], "detected": hit,
                     "extra_flags": extra, "unsupported_flags": len(unsupported),
                     # keep the texts — an off-needle flag is unauditable
                     # without them (learned 2026-09-04)
                     "unsupported_claims": [
                         {"text": c, "matches_needle": needle_in(fx["needle"], c)}
                         for c in unsupported
                     ]})
        print(f"  fixture {fx['id']:>2} [{fx['type']:<12}] "
              f"{'DETECTED' if hit else 'MISSED  '} "
              f"(+{extra} flags off-needle)", flush=True)
        time.sleep(0.5)

    n = len(fixtures)
    flags_total = detected + false_pos
    return {
        "n": n,
        "detected": detected,
        "recall": detected / n if n else 0.0,
        "recall_ci_95": [round(x, 4) for x in wilson_interval(detected, n)],
        "matched_flags": detected,
        "off_needle_flags": false_pos,
        "precision": (detected / flags_total) if flags_total else None,
        "precision_ci_95": ([round(x, 4) for x in wilson_interval(detected, flags_total)]
                            if flags_total else None),
        "rows": rows,
    }


def main():
    ap = argparse.ArgumentParser(description="Score the critic on perturbed fixtures.")
    ap.add_argument("--fixtures", required=True)
    ap.add_argument("--json-out", default=None)
    args = ap.parse_args()

    fixtures = [json.loads(ln) for ln in
                Path(args.fixtures).read_text(encoding="utf-8").splitlines() if ln.strip()]
    print(f"Running the judge over {len(fixtures)} perturbed fixtures...")
    result = run_fixtures(fixtures)

    print("=" * 70)
    print(f"  CRITIC ON INJECTED FAILURES — {result['n']} fixtures")
    print(f"  recall    : {format_rate_ci(result['detected'], result['n'])} "
          f"({result['detected']}/{result['n']})")
    if result["precision"] is not None:
        print(f"  precision : {format_rate_ci(result['matched_flags'], result['matched_flags'] + result['off_needle_flags'])} "
              f"(vs injection tags; lower bound — fixtures omit pre-written sections)")
    print("=" * 70)
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"wrote {args.json_out}")


if __name__ == "__main__":
    main()
