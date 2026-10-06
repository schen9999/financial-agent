"""eval/rejudge_runs.py: with the original findings returned in place of a
re-judge, the counting reproduces each run's recorded totals — so a real
re-judge is compared on the same arithmetic. No API calls."""
from eval import rejudge_runs as rj


def test_counting_reproduces_the_recorded_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(rj, "rejudge_one", lambda parsed, attempts=3: parsed["findings"])
    summary = rj.run_all(["4hsn2", "5bdz5"], tmp_path, workers=2)
    assert (summary["4hsn2"]["unsupported"], summary["4hsn2"]["total"]) == (15, 399)
    assert (summary["5bdz5"]["unsupported"], summary["5bdz5"]["total"]) == (19, 265)
    assert summary["5bdz5"]["unsupported_qualitative"] == 17
    assert len(list((tmp_path / "4hsn2").glob("*.findings.txt"))) == 40
    # resumable: a second pass re-judges nothing
    monkeypatch.setattr(rj, "rejudge_one", lambda *a, **k: (_ for _ in ()).throw(AssertionError))
    assert rj.run_all(["4hsn2"], tmp_path, workers=2)["4hsn2"]["unsupported"] == 15
    t = rj.table(summary, [("4hsn2", "5bdz5")])
    assert "| 4hsn2 vs 5bdz5 | 15/399 vs 19/265 |" in t
