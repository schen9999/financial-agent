"""eval/agreement.py must work on a PARTIALLY labeled file (mid-labeling):
blank human_label rows are excluded with a printed count, invalid labels
fail loudly."""
import csv

import pytest

from eval.agreement import load_pairs


def _write(path, rows, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def _files(tmp_path, labels):
    labeled = tmp_path / "sample.csv"
    key = tmp_path / "sample_key.csv"
    _write(labeled,
           [{"id": str(i), "provenance": "t", "ticker": "AAPL",
             "claim": f"c{i}", "context": "ctx", "human_label": lab}
            for i, lab in enumerate(labels)],
           ["id", "provenance", "ticker", "claim", "context", "human_label"])
    _write(key,
           [{"id": str(i), "arm": "baseline", "judge_label": "SUPPORTED",
             "judge_reason": "r"} for i in range(len(labels))],
           ["id", "arm", "judge_label", "judge_reason"])
    return labeled, key


def test_blank_rows_excluded_with_count(tmp_path, capsys):
    labeled, key = _files(tmp_path, ["SUPPORTED", "", "inference", "", ""])
    pairs = load_pairs(labeled, key)
    assert len(pairs) == 2  # only the filled rows, case-insensitive
    assert "3 rows still unlabeled" in capsys.readouterr().out


def test_invalid_label_fails_loudly(tmp_path):
    labeled, key = _files(tmp_path, ["SUPPORTED", "MAYBE"])
    with pytest.raises(SystemExit):
        load_pairs(labeled, key)
