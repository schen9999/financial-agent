"""eval/multi_arm_stats.py — runs are keyed by label (three runs share the
harness arm `local-model`), every pair gets a Fisher test, and null-claim
free-form verdicts count in totals as unattributed."""
import json

from eval import multi_arm_stats as mas
from eval.stats import fisher_exact

FINDINGS = """# {t} — {arm}

## Metadata

ticker: {t}
arm: {arm}

## Retrieved source context

ctx

## Pre-written sections (judge input)

### Financial Health
Revenue was $10.0 billion with a 20% margin.

### Risk Factors
- Competition from larger rivals.

## Audited (Exec Summary + Outlook)

### Executive Summary
x

## Judge findings

f
"""


def _run(tmp_path, name, arm, rows):
    fdir = tmp_path / f"{name}-findings"
    fdir.mkdir()
    (fdir / f"AAA_{arm}.md").write_text(FINDINGS.format(t="AAA", arm=arm), encoding="utf-8")
    claims = tmp_path / f"{name}.jsonl"
    claims.write_text("".join(json.dumps({"ticker": "AAA", "arm": arm, "claim": c,
                                          "judge_label": lab}) + "\n" for c, lab in rows),
                      encoding="utf-8")
    return mas.load_run(claims, fdir)


def test_attribution_and_pairwise(tmp_path):
    runs = {
        "a": _run(tmp_path, "a", "local-model", [
            ("Revenue was $10.0 billion", "UNSUPPORTED"),
            ("Competition from larger rivals", "SUPPORTED"),
            (None, "UNSUPPORTED")]),
        "b": _run(tmp_path, "b", "local-model", [
            ("Revenue was $10.0 billion", "SUPPORTED"),
            ("something the synthesis made up entirely", "SUPPORTED")]),
    }
    assert [r["attributed"] for r in runs["a"]] == ["financial-health", "risk-factors",
                                                   "unattributed"]
    assert mas.tally(runs["a"]) == (2, 3)
    assert mas.tally(runs["b"], lambda r: r["attributed"] == "unattributed") == (0, 1)
    (a, b, ua, na, ub, nb, p), = mas.pairwise(runs)
    assert (a, b, ua, na, ub, nb) == ("a", "b", 2, 3, 0, 2)
    assert p == fisher_exact(2, 1, 0, 2)


def test_fmt_p():
    assert mas.fmt_p(0.0764) == "0.0764"
    assert mas.fmt_p(7.8e-05) == "7.8e-05"
