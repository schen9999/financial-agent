"""eval/error_types.py: adjudicated types of UNSUPPORTED numeric claims —
complete against the claims files, and tallied into model errors."""
import json

from eval import error_types as et
from eval.stats import fisher_exact


def _spec(tmp_path, rows, classified):
    (tmp_path / "a.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return {"types": {"wrong value": "", "wrong label": "", "judge error": ""},
            "runs": {"a": "a.jsonl"}, "classified": classified}


def test_check_flags_unclassified_extra_and_unknown(tmp_path):
    rows = [{"ticker": "X", "claim": "revenue of $5M", "judge_label": "UNSUPPORTED"},
            {"ticker": "X", "claim": "strong brand", "judge_label": "UNSUPPORTED"},
            {"ticker": "Y", "claim": "margin 3%", "judge_label": "SUPPORTED"}]
    spec = _spec(tmp_path, rows, [])
    runs = et.load(spec, tmp_path)
    assert runs["a"] == {"numeric": 2, "unsupported": [("X", "revenue of $5M")]}
    assert et.check(spec, runs) == ["a: unclassified X 'revenue of $5M'"]
    spec["classified"] = [{"run": "a", "ticker": "X", "claim": "revenue of $5M", "type": "typo"},
                          {"run": "a", "ticker": "Y", "claim": "margin 3%", "type": "judge error"}]
    problems = et.check(spec, runs)
    assert problems[0].startswith("unknown type 'typo'")
    assert any("classified but not an UNSUPPORTED numeric claim: Y" in p for p in problems)


def test_committed_adjudication_is_complete_and_reproduces_the_counts():
    spec = json.loads((et._REPO / "eval/runs/numeric-error-types-2026-10-05.json")
                      .read_text(encoding="utf-8"))
    runs = et.load(spec)
    assert et.check(spec, runs) == []
    t = et.tally(spec)
    assert {r: runs[r]["numeric"] for r in runs} == \
        {"hosted-9jzmj": 277, "slm-cpu-8vpq6": 161, "slm-gpu-p9jr2": 155}
    assert t["slm-gpu-p9jr2"]["wrong label"] == ["SFIX", "CRBU"]
    assert t["slm-cpu-8vpq6"]["wrong value"] == ["CHGG"]
    me = {r: sum(len(t[r][k]) for k in et.MODEL_ERRORS) for r in runs}
    assert me == {"hosted-9jzmj": 0, "slm-cpu-8vpq6": 1, "slm-gpu-p9jr2": 2}
    assert round(fisher_exact(0, 277, 2, 153), 4) == 0.1282
