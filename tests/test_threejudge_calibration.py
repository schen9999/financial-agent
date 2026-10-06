"""eval/build_threejudge_calibration.py and eval/threejudge_report.py:
claim matching across judgings, strata and weights, a blind labelling CSV,
and weighted precision/recall and agreement arithmetic. No API calls."""
import csv
import json

import pytest

from eval import build_threejudge_calibration as btc
from eval import threejudge_report as tr

R1 = "eval/runs/rejudge-2026-10-06"


def test_claims_match_across_judgings():
    j1 = [{"claim": "Revenue grew 6% to $391.0 billion", "label": "SUPPORTED"},
          {"claim": "margin pressure from tariffs", "label": "UNSUPPORTED"}]
    j2 = [{"claim": "revenue grew 6% to $391.0 billion.", "label": "SUPPORTED"}]
    j3 = [{"claim": "Margin pressure from tariffs bears watching", "label": "INFERENCE"},
          {"claim": "a new claim", "label": "SUPPORTED"}]
    u = btc.unify([j1, j2, j3])
    assert [c["verdicts"] for c in u] == [["SUPPORTED", "SUPPORTED", "NOT_LISTED"],
                                          ["UNSUPPORTED", "NOT_LISTED", "INFERENCE"],
                                          ["NOT_LISTED", "NOT_LISTED", "SUPPORTED"]]
    assert btc.majority(["UNSUPPORTED", "NOT_LISTED", "UNSUPPORTED"]) == "UNSUPPORTED"
    assert btc.majority(["UNSUPPORTED", "SUPPORTED", "NOT_LISTED"]) == "SUPPORTED"
    assert btc.majority(["INFERENCE", "INFERENCE", "UNSUPPORTED"]) == "INFERENCE"


def test_population_with_identical_second_and_third_judgings():
    rows = btc.population(["4hsn2"], ["raw", R1, R1])
    assert all(r["verdicts"][1] == r["verdicts"][2] for r in rows)
    assert {r["stratum"] for r in rows} == set("UIWS")
    assert all(r["stratum"] == "U" for r in rows if "UNSUPPORTED" in r["verdicts"])
    # every claim the first judging listed is in the pool once
    assert sum(r["verdicts"][0] != "NOT_LISTED" for r in rows) >= 395


def test_refuses_a_missing_judging(tmp_path):
    with pytest.raises(SystemExit, match="all three judgings must exist"):
        btc.population(["4hsn2"], ["raw", R1, str(tmp_path)])


def test_writes_a_blind_sample_and_a_weighted_key(tmp_path, monkeypatch):
    monkeypatch.setattr(btc, "JV", tmp_path)
    assert btc.main(["--runs", "4hsn2", "--judgings", "raw", R1, R1]) == 0
    with open(tmp_path / "threejudge_sample.csv", newline="", encoding="utf-8") as f:
        sample = list(csv.DictReader(f))
    with open(tmp_path / "threejudge_key.csv", newline="", encoding="utf-8") as f:
        key = list(csv.DictReader(f))
    method = json.loads((tmp_path / "threejudge_method.json").read_text())
    assert list(sample[0]) == ["id", "ticker", "claim", "context", "human_label"]
    assert all(r["human_label"] == "" for r in sample)
    assert not any("LABEL:" in r["context"] or "NOT_LISTED" in r["context"] for r in sample)
    assert [r["id"] for r in sample] == [r["id"] for r in key]
    assert len(key) == sum(method["sample"].values()) <= btc.TOTAL
    for k in "UIWS":
        w = sum(float(r["weight"]) for r in key if r["stratum"] == k)
        assert w == pytest.approx(method["population"][k])
    with pytest.raises(SystemExit, match="--force"):
        btc.main(["--runs", "4hsn2", "--judgings", "raw", R1, R1])


def _row(stratum, human, j1, j2, j3):
    return {"stratum": stratum, "human": human, "j1": j1, "j2": j2, "j3": j3}


def test_weighted_precision_recall_and_majority():
    U, S, N = "UNSUPPORTED", "SUPPORTED", "NOT_LISTED"
    rows = [_row("U", U, U, U, S), _row("U", S, U, N, N),
            _row("S", U, S, S, S), _row("S", S, S, S, S)]
    for r in rows:
        r["w"] = 1 if r["stratum"] == "U" else 10     # S stands for 10x as many claims
    assert tr.pr(rows, "j1") == (0.5, pytest.approx(1 / 11))
    assert tr.pr(rows, "j2") == (1.0, pytest.approx(1 / 11))
    assert tr.pr(rows, "j3") == (None, 0.0)
    assert tr.pr(rows, "majority") == (1.0, pytest.approx(1 / 11))


def test_load_reweights_to_labelled_rows(tmp_path):
    (tmp_path / "s.csv").write_text("id,ticker,claim,context,human_label\n0,A,c,x,UNSUPPORTED\n"
                                    "1,A,c,x,\n2,A,c,x,SUPPORTED\n", encoding="utf-8")
    (tmp_path / "k.csv").write_text("id,stratum,j1,j2,j3\n0,U,a,b,c\n1,U,a,b,c\n2,S,a,b,c\n", encoding="utf-8")
    rows = tr.load(tmp_path / "s.csv", tmp_path / "k.csv", {"population": {"U": 8, "S": 50}})
    assert [(r["id"], r["w"]) for r in rows] == [("0", 8.0), ("2", 50.0)]


def test_kappas():
    assert tr.cohen(list("aabb"), list("aabb")) == 1.0
    assert tr.cohen(list("abab"), list("aabb")) == 0.0
    # Fleiss (1971) worked example shape: perfect agreement is 1
    assert tr.fleiss([["a"] * 3, ["b"] * 3]) == 1.0
    assert tr.fleiss([["a", "a", "b"], ["a", "b", "b"]]) == pytest.approx(-1 / 3)


def test_label_cli_refuses_the_key():
    from eval import label_cli
    src = (btc.ROOT / "eval" / "label_cli.py").read_text(encoding="utf-8")
    assert 'endswith("_key.csv")' in src and label_cli
