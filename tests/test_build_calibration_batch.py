"""eval/build_calibration_batch.py allocation, draw, cap report, blinding;
and eval/agreement.py reading a key file with a '#' header block."""
import csv

import pytest

from eval import build_calibration_batch as b
from eval.agreement import load_pairs


def test_allocate_proportional_largest_remainder():
    # 100 * 354/678 = 52.2, 100 * 324/678 = 47.8 -> 52 / 48
    assert b.allocate(100, {"baseline": 354, "local-model": 324},
                      {"baseline": 341, "local-model": 311}) == \
        {"baseline": 52, "local-model": 48}


def test_allocate_moves_shortfall_to_arm_with_room():
    # 25 * 12/42 = 7.1 baseline wanted, only 1 eligible -> rest to local
    assert b.allocate(22, {"baseline": 12, "local-model": 30},
                      {"baseline": 1, "local-model": 30}) == \
        {"baseline": 1, "local-model": 21}


def test_plan_short_labels_taken_whole_and_supported_fills_to_total():
    pop = {"SUPPORTED": {"baseline": 354, "local-model": 324},
           "UNSUPPORTED": {"baseline": 12, "local-model": 30},
           "INFERENCE": {"baseline": 26, "local-model": 14}}
    avail = {"SUPPORTED": {"baseline": 341, "local-model": 311},
             "UNSUPPORTED": {"baseline": 1, "local-model": 22},
             "INFERENCE": {"baseline": 18, "local-model": 6}}
    sizes = b.plan(pop, avail)
    assert sum(sizes.values()) == b.TOTAL
    assert sizes[("UNSUPPORTED", "baseline")] + sizes[("UNSUPPORTED", "local-model")] == 23
    assert sizes[("INFERENCE", "baseline")] + sizes[("INFERENCE", "local-model")] == 24
    assert sizes[("SUPPORTED", "baseline")] + sizes[("SUPPORTED", "local-model")] == 103


def _rows(n, label, arm, tickers):
    return [{"ticker": tickers[i % len(tickers)], "claim": f"{label}{arm}{i}",
             "label": label, "arm": arm} for i in range(n)]


def test_draw_is_deterministic_and_hits_sizes():
    pool = _rows(30, "SUPPORTED", "baseline", "ABC") + _rows(5, "UNSUPPORTED", "local-model", "D")
    sizes = {("SUPPORTED", "baseline"): 10, ("UNSUPPORTED", "local-model"): 5}
    a, c = b.draw(pool, sizes, seed=3), b.draw(pool, sizes, seed=3)
    assert a == c
    assert sum(r["label"] == "SUPPORTED" for r in a) == 10
    assert sum(r["label"] == "UNSUPPORTED" for r in a) == 5


def test_cap_effect_reports_binding_cap_without_applying():
    picked = _rows(6, "SUPPORTED", "baseline", "A") + _rows(2, "SUPPORTED", "baseline", "B")
    eff = b.cap_effect(picked, cap=4)
    assert eff["applied"] is False
    assert eff["tickers_over_cap"] == {"A": 6}
    assert eff["draws_displaced"] == 2
    assert b.cap_effect(_rows(4, "SUPPORTED", "baseline", "AB"), cap=4)["applied"] is True


def test_committed_batch_does_not_reveal_judge_label():
    path = b.SAMPLE_FILE
    if not path.exists():
        pytest.skip("calibration batch not drawn")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["id", "ticker", "claim", "context", "human_label"]
        rows = list(reader)
    assert len(rows) == b.TOTAL
    assert all(not r["human_label"] for r in rows)


def test_main_refuses_before_reading_when_method_exists(monkeypatch, tmp_path):
    path = tmp_path / "calibration_batch_method.json"
    path.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(b, "METHOD_FILE", path)
    monkeypatch.setattr(b, "collect_claims",
                        lambda *a, **k: pytest.fail("must refuse before drawing"))
    with pytest.raises(SystemExit):
        b.main([])


def test_load_pairs_skips_key_header_comments(tmp_path):
    key = tmp_path / "key.csv"
    key.write_text("# strata: SUPPORTED|baseline 354 / 341 / 54\n# seed 1\n"
                   "id,run,arm,judge_label,judge_reason\n"
                   "0,j4cnp,baseline,SUPPORTED,ok\n1,lsnnc,local-model,UNSUPPORTED,no\n",
                   encoding="utf-8")
    labeled = tmp_path / "s.csv"
    labeled.write_text("id,ticker,claim,context,human_label\n"
                       "0,A,c0,\"# not a comment\",SUPPORTED\n1,B,c1,x,INFERENCE\n",
                       encoding="utf-8")
    assert load_pairs(labeled, key) == [("SUPPORTED", "SUPPORTED"),
                                        ("UNSUPPORTED", "INFERENCE")]
