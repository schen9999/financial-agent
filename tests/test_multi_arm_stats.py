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


def test_pooled_tests_outsiders_against_concatenated_members(tmp_path):
    runs = {
        "x": _run(tmp_path, "x", "local-model", [("a", "UNSUPPORTED"), ("b", "SUPPORTED")]),
        "h1": _run(tmp_path, "h1", "baseline", [("c", "SUPPORTED"), ("d", "UNSUPPORTED")]),
        "h2": _run(tmp_path, "h2", "baseline", [("e", "SUPPORTED"), ("f", "SUPPORTED"),
                                                ("g", "SUPPORTED")]),
    }
    (a, b, ua, na, ub, nb, p), = mas.pooled(runs, "hosted", ["h1", "h2"])
    assert (a, b, ua, na, ub, nb) == ("x", "hosted", 1, 2, 1, 5)
    assert p == fisher_exact(1, 1, 1, 4)


def test_fmt_p():
    assert mas.fmt_p(0.0764) == "0.0764"
    assert mas.fmt_p(7.8e-05) == "7.8e-05"


def test_committed_w4a16_arm_reproduces():
    """The 2026-09-29 W4A16 arm (r5nzh) against the BF16 fine-tune (v924f):
    the committed rows reproduce the aggregate and the recorded Fisher p."""
    import pathlib
    runs_dir = pathlib.Path(__file__).resolve().parents[1] / "eval" / "runs"
    runs = {name: mas.load_run(runs_dir / f"{name}-claims.jsonl",
                               runs_dir / "raw" / f"{name}-findings")
            for name in ("v924f", "r5nzh")}
    assert mas.tally(runs["r5nzh"]) == (23, 344)
    assert mas.tally(runs["v924f"]) == (25, 385)
    (_, _, *_, p), = mas.pairwise(runs)
    assert mas.fmt_p(p) == "1.0000"
    owned = lambda r: r["attributed"] in mas.OWNED  # noqa: E731
    assert mas.tally(runs["r5nzh"], owned) == (15, 96)


def test_report_runs_claim_density_and_leads_with_numeric_claims(monkeypatch):
    """The 2026-10-03 same-image smokes (hosted hm527, CPU SLM 9jddz): the
    report shows numeric claims per ticker and their own unsupported rate,
    and prints the claim-density table without being asked."""
    import pathlib
    runs_dir = pathlib.Path(__file__).resolve().parents[1] / "eval" / "runs"
    argv = ["multi_arm_stats.py"]
    for label, run in (("hosted", "hm527"), ("slm-cpu", "9jddz")):
        argv += ["--run", label, str(runs_dir / f"{run}-claims.jsonl"),
                 str(runs_dir / "raw" / f"{run}-findings")]
    monkeypatch.setattr(mas.sys, "argv", argv)
    # Collect the report's lines directly instead of through capsys: this
    # test runs right after test_mcp_server, whose abandoned tool thread can
    # leave its redirect_stdout block late and put sys.stdout back to an
    # older stream — capsys then reads nothing (seen on a fresh checkout).
    lines = []
    for mod in (mas, mas.claim_density):
        monkeypatch.setattr(mod, "print", lambda *a, **k: lines.append(" ".join(map(str, a))),
                            raising=False)
    mas.main()
    out = "\n".join(lines)
    assert "hosted         6.1/ticker (min 3, 10 tickers)   unsupported 0/61" in out
    assert "slm-cpu        3.1/ticker (min 2, 10 tickers)   unsupported 0/31" in out
    assert "Pairwise, exact two-sided Fisher (numeric claims):" in out
    assert "Claim density (eval/claim_density.py):" in out
    assert out.index("Co-primary, numeric claims") < out.index("Pairwise, exact two-sided Fisher (all")


def test_sign_test_and_paired_difference():
    assert mas.sign_test(0, 0) == 1.0
    assert mas.sign_test(5, 0) == 2 * (1 / 32)
    assert mas.sign_test(3, 3) == 1.0
    a = {t: {"numeric": n} for t, n in (("A", 7), ("B", 6), ("C", 5), ("D", 4), ("X", 9))}
    b = {t: {"numeric": n} for t, n in (("A", 4), ("B", 4), ("C", 5), ("D", 5), ("Y", 1))}
    pr = mas.paired(a, b)
    assert (pr["tickers"], pr["a_more"], pr["equal"], pr["b_more"]) == (4, 2, 1, 1)
    assert (pr["mean_a"], pr["mean_b"], pr["mean_diff"], pr["median_diff"]) == (5.5, 4.5, 1.0, 1.0)
    assert pr["ci"][0] <= pr["mean_diff"] <= pr["ci"][1]
    assert pr == mas.paired(a, b)  # seeded: the interval is reproducible
    assert mas.paired(a, {"Z": {"numeric": 1}}) is None


def test_rows_sections_from_the_committed_extended_runs():
    """Hosted 9jzmj vs CPU SLM 8vpq6 (same image, 2026-10-04): rows read
    from the workflow objects, compressed node status included."""
    import pathlib
    runs_dir = pathlib.Path(__file__).resolve().parents[1] / "eval" / "runs"
    hosted = mas.load_rows(runs_dir / "9jzmj-workflow.json")
    slm = mas.load_rows(runs_dir / "slm-proof-8vpq6" /
                        "grounding-eval-extended-slm-cpu-8vpq6-workflow.json")
    assert (len(hosted), len(slm)) == (40, 40)
    assert mas.ragf_totals(hosted) == (14, 1017, 70)
    assert mas.ragf_totals(slm) == (6, 1415, 70)
    calls, mean, mx = mas.site_latency(slm)["synthesis"]
    assert calls == 40 and round(mean, 2) == 114.45 and round(mx, 2) == 155.76
    assert mas.site_latency(hosted)["rag:risks"][0] == 35
    # the aggregate's input JSON is accepted as well as a workflow object
    assert len(mas.load_rows(runs_dir / "9jzmj-results-rebuilt.json")) == 40


def test_speed_ratios_read_slower_over_faster_in_either_argument_order():
    assert mas.slower_faster("gpu", 2.0, "cpu", 20.0) == ("cpu", "gpu", 10.0, 20.0, 2.0)
    assert mas.slower_faster("cpu", 20.0, "gpu", 2.0) == ("cpu", "gpu", 10.0, 20.0, 2.0)
    rows_a = [{"ticker": "A", "pipeline_s": 30.0}, {"ticker": "B", "pipeline_s": 10.0},
              {"ticker": "X", "pipeline_s": 999.0}]
    rows_b = [{"ticker": "A", "pipeline_s": 3.0}, {"ticker": "B", "pipeline_s": 1.0}]
    assert mas.common_ratio("cpu", rows_a, "gpu", rows_b, "pipeline_s") == \
        ("cpu", "gpu", 2, 10.0, 20.0, 2.0)
    assert mas.common_ratio("cpu", rows_a, "gpu", [{"ticker": "Z", "pipeline_s": 1.0}],
                            "pipeline_s") is None


def test_gpu_extended_rows_from_the_committed_workflow_object():
    """GPU SLM p9jr2 (same image, 2026-10-05): the workflow object carries the
    aggregate's per-site ledger and RAG faithfulness."""
    import pathlib
    runs_dir = pathlib.Path(__file__).resolve().parents[1] / "eval" / "runs"
    gpu = mas.load_rows(runs_dir / "slm-proof-p9jr2" /
                        "grounding-eval-extended-slm-gpu-p9jr2-workflow.json")
    assert len(gpu) == 40
    assert mas.ragf_totals(gpu) == (6, 1465, 70)
    calls, mean, mx = mas.site_latency(gpu)["synthesis"]
    assert calls == 40 and round(mean, 2) == 11.41 and round(mx, 2) == 19.50
