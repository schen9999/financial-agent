"""scripts/numeric_backtest.py --runs: the named runs only, into their own
adjudication CSV, never the main one; the lsnnc CRBU assertion still runs."""
import argparse
import csv

from scripts import numeric_backtest as nb


def _briefs():
    files = sorted(nb.RAW.glob("*-findings/**/*.md"))
    return [b for b in (nb.load_brief(p, nb.RAW) for p in files) if b], len(files)


def test_runs_mode_writes_its_own_csv_and_never_the_main_one(tmp_path):
    before = nb.ADJ_PATH.read_bytes()
    briefs, n = _briefs()
    out = tmp_path / "bt.json"
    args = argparse.Namespace(runs=["p9jr2"], adjudication=str(nb.ADJ_PATH), date="2026-10-05",
                              out=str(out), seed=42)
    redirected = nb.ADJ_PATH.with_name("adjudication-2026-10-05-p9jr2.csv")
    try:
        nb.main_runs(args, briefs, [], n)
        rows = list(csv.DictReader(redirected.open(encoding="utf-8")))
    finally:
        redirected.unlink(missing_ok=True)
    assert nb.ADJ_PATH.read_bytes() == before
    assert len(rows) == 3 and {r["run"] for r in rows} == {"p9jr2"}
    assert {r["model"] for r in rows} == {"qwen3.6-35b-a3b-q4km"}
    assert all(r["verdict"] == "" for r in rows)
    assert out.exists() and out.with_suffix(".md").exists()
