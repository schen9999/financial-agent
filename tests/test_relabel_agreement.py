"""eval/relabel_agreement.py joins relabels to originals through the key;
eval/reweight_calibration.py --use filters a sample's judge-label strata."""
import csv

import pytest

from eval import reweight_calibration as rc
from eval.relabel_agreement import joined, rate

CTX = "=== AUDITED TEXT (Exec Summary + Outlook) ===\n### Outlook\nMargins may compress."


def _csv(path, header, rows, comment=None):
    with open(path, "w", newline="", encoding="utf-8") as f:
        if comment:
            f.write(comment + "\n")
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def _fixture(tmp_path, relabel_claim="Margins may compress"):
    hdr = ["id", "ticker", "claim", "context", "human_label"]
    _csv(tmp_path / "batch.csv", hdr, [[0, "A", "Margins may compress", CTX, "UNSUPPORTED"],
                                       [1, "B", "x", "ctx", "SUPPORTED"]])
    _csv(tmp_path / "hold.csv", hdr, [[0, "C", "y", "ctx", "SUPPORTED"]])
    _csv(tmp_path / "rel.csv", hdr, [[0, "C", "y", "ctx", "SUPPORTED"],
                                     [1, "A", relabel_claim, CTX, "SUPPORTED"],
                                     [2, "B", "x", "ctx", "SUPPORTED"]])
    _csv(tmp_path / "rel_key.csv", ["id", "source", "source_id", "run", "arm", "judge_label"],
         [[0, "holdout", 0, "", "baseline", "SUPPORTED"],
          [1, "calibration_batch", 0, "j4cnp", "baseline", "SUPPORTED"],
          [2, "calibration_batch", 1, "lsnnc", "local-model", "SUPPORTED"]],
         comment="# seed 1")
    sources = [("calibration_batch", tmp_path / "batch.csv", None),
               ("holdout", tmp_path / "hold.csv", None)]
    return tmp_path / "rel.csv", tmp_path / "rel_key.csv", sources


def test_joined_maps_relabel_to_original_by_source(tmp_path):
    rel, key, sources = _fixture(tmp_path)
    data = joined(rel, key, sources)
    batch = data["calibration_batch"]
    assert rate(batch, "original") == (1, 2)
    assert rate(batch, "relabel") == (0, 2)
    assert batch[0]["section"] == "Outlook" and batch[0]["position"] == 1
    assert rate(data["holdout"], "relabel") == (0, 1)


def test_joined_refuses_a_mismatched_row(tmp_path):
    rel, key, sources = _fixture(tmp_path, relabel_claim="something else")
    with pytest.raises(SystemExit):
        joined(rel, key, sources)


def test_reweight_use_filters_strata(tmp_path, monkeypatch, capsys):
    hdr = ["id", "ticker", "claim", "context", "human_label"]
    _csv(tmp_path / "s.csv", hdr, [[0, "A", "a", "c", "UNSUPPORTED"], [1, "B", "b", "c", "SUPPORTED"]])
    _csv(tmp_path / "s_key.csv", ["id", "judge_label"], [[0, "SUPPORTED"], [1, "SUPPORTED"]])
    _csv(tmp_path / "h.csv", hdr, [[0, "C", "c", "c", "UNSUPPORTED"], [1, "D", "d", "c", "INFERENCE"],
                                   [2, "E", "e", "c", "SUPPORTED"]])
    _csv(tmp_path / "h_key.csv", ["id", "judge_label"],
         [[0, "UNSUPPORTED"], [1, "INFERENCE"], [2, "SUPPORTED"]])
    # judge-SUPPORTED rows from s.csv (all), U and I only from h.csv
    monkeypatch.setattr(rc, "population_counts",
                        lambda c, f: {"SUPPORTED": 10, "UNSUPPORTED": 1, "INFERENCE": 1})
    monkeypatch.setattr("sys.argv", ["x", "--labeled", str(tmp_path / "s.csv"),
                                     "--key", str(tmp_path / "s_key.csv"), "--use", "ALL",
                                     "--labeled", str(tmp_path / "h.csv"),
                                     "--key", str(tmp_path / "h_key.csv"),
                                     "--use", "UNSUPPORTED,INFERENCE",
                                     "--run", "r", "c", "f", "--draws", "200"])
    rc.main()
    out = capsys.readouterr().out
    assert "SUPPORTED    1/2" in out
    assert "UNSUPPORTED  1/1" in out
    assert "INFERENCE    0/1" in out
