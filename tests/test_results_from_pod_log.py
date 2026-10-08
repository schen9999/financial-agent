"""scripts/results_from_pod_log.py: an aggregate rebuilt from the pods' logs
equals the one the cluster printed, and the rebuild stops rather than guess.
Also scripts/template_offload_probe.py's template size."""
import base64
import importlib.util
import io
import json
import pathlib
import tarfile

import pytest

from eval import attempts
from eval.label import render_findings_md

_REPO = pathlib.Path(__file__).resolve().parents[1]


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, _REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


rebuild = _load("results_from_pod_log", "scripts/results_from_pod_log.py")
probe = _load("template_offload_probe", "scripts/template_offload_probe.py")
eval_aggregate = _load("eval_aggregate_rebuild", "scripts/eval_aggregate.py")

FINDINGS = """CLAIM: "revenue of $10.0 billion"
LABEL: SUPPORTED
REASON: matches.

CLAIM: "a durable distribution advantage"
LABEL: UNSUPPORTED
REASON: absent.
"""
CONTEXT = 'STOCK DATA:\n{\n  "ticker": "AAA",\n  "current_price": 10.0\n}\n\nNEWS ARTICLES:\n[]'


def _site(prompt, compl):
    return {"calls": 1, "prompt_tokens": prompt, "completion_tokens": compl,
            "prompt_tokens_unrecorded": 0, "completion_tokens_unrecorded": 0,
            "latency_s_total": 2.5, "latency_s_max": 2.5, "truncated": 0, "repeat_run": 0,
            "retry": 0, "parse_failure": 0, "format_failure": 0, "errors": 0}


def _call(seq, site, endpoint, prompt, compl):
    return attempts.CALL_PREFIX + json.dumps({
        "seq": seq, "site": site, "endpoint": endpoint, "prompt_tokens": prompt,
        "completion_tokens": compl, "truncated": False, "repeat_run": False, "retry": False,
        "parse_failure": False, "format_failure": False, "error": None})


def _pod_log(pod="wf-eval-one-1", ticker="AAA", line_counts=(1, 1, 0, 2), synthesis_prompt=900,
             outcome="ok", ragf=True):
    by_site = {"section:x": _site(500, 100), "synthesis": _site(900, 300)}
    md = render_findings_md(ticker, "baseline", "v2", CONTEXT, "### Financial Health\nx",
                            "### Executive Summary\ny", FINDINGS,
                            {"llm_calls": 2, "llm_endpoints": "anthropic",
                             "llm_by_site": json.dumps(by_site, sort_keys=True)})
    files = {f"eval_findings/{ticker}_baseline.md": md}
    if ragf:
        files[f"eval_findings/{ticker}_baseline.ragf.json"] = json.dumps({"answers": {
            "risks": {"supported": 9, "unsupported": 1, "total": 10, "chunks": ["c"]}}})
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for name, text in files.items():
            data = text.encode("utf-8")
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))
    s, u, i, t = line_counts
    lines = [
        attempts.BEGIN_PREFIX + json.dumps({"attempt": 0, "tickers": [ticker]}),
        _call(1, "section:x", "anthropic", 500, 100),
        _call(2, "synthesis", "anthropic", synthesis_prompt, 300),
        _call(3, "judge", "anthropic", 4000, 700),
        f"  [{ticker} | baseline] {s} SUP  {u} UNSUP  {i} INF  ({t} claims)  retrieval=5.78s  "
        f"pipeline=27.77s  haiku_cost=$0.00647  llm_calls=2 (anthropic) truncated=0",
        f"===EVAL_FINDINGS_TGZ_BEGIN pod={pod}===",
        base64.b64encode(buf.getvalue()).decode(),
        "===EVAL_FINDINGS_TGZ_END===",
        attempts.END_PREFIX + json.dumps({"attempt": 0, "outcome": outcome, "calls": 3}),
    ]
    return "\n".join(f"[pod/{pod}/main] {ln}" for ln in lines) + "\n"


def test_rebuilt_row_carries_what_the_aggregate_reads():
    (payload,) = rebuild.rebuild(_pod_log())
    (row,) = payload["results"]
    assert (row["ticker"], row["arm"], row["judge_version"], row["attempt"]) == (
        "AAA", "baseline", "v2", 0)
    assert (row["supported"], row["unsupported"], row["inference"], row["total"]) == (1, 1, 0, 2)
    assert row["numeric_claims"] == {"total": 1, "supported": 1, "unsupported": 0, "inference": 0}
    assert (row["retrieval_s"], row["pipeline_s"], row["stock_block_empty"]) == (5.78, 27.77, False)
    assert row["llm"]["by_endpoint"]["anthropic"]["prompt_tokens"] == 1400  # judge call excluded
    assert row["llm"]["total"]["calls"] == 2 and row["llm"]["endpoints"] == ["anthropic"]
    assert row["rag_faithfulness"] == {"risks": {"supported": 9, "unsupported": 1, "total": 10}}
    assert "est_cost" not in row


@pytest.mark.parametrize("kwargs,match", [
    ({"line_counts": (2, 0, 0, 2)}, "result line says"),
    ({"synthesis_prompt": 901}, "disagree with llm_by_site"),
    ({"outcome": "failed"}, "not a finished attempt"),
])
def test_rebuild_stops_instead_of_guessing(kwargs, match):
    with pytest.raises(SystemExit, match=match):
        rebuild.rebuild(_pod_log(**kwargs))


def test_rebuild_refuses_duplicates_and_skipped_tickers():
    with pytest.raises(SystemExit, match="two pods"):
        rebuild.rebuild(_pod_log() + _pod_log(pod="wf-eval-one-2"))
    with pytest.raises(SystemExit, match="SKIPPED after retries"):
        rebuild.rebuild(_pod_log() + "[pod/x/main]   [BBB] SKIPPED after retries (format): x\n")


def test_compare_reports_only_real_differences():
    cluster = ["====", "  TOTAL 86 8 7 101", "  est. run cost     : $1.0568", "====", ""]
    offline = ["====", "  TOTAL 86 8 7 101", "===="]
    assert rebuild.compare(offline, cluster) == [("in-cluster only", "  est. run cost     : $1.0568")]
    assert rebuild.compare(["  TOTAL 86 7 7 100"], ["  TOTAL 86 8 7 101"]) == [
        ("offline only", "  TOTAL 86 7 7 100"), ("in-cluster only", "  TOTAL 86 8 7 101")]


def _aggregate_lines(monkeypatch, capsys, results_file):
    monkeypatch.delenv("EVAL_ARTIFACTS_PUT_URL", raising=False)
    monkeypatch.setattr(eval_aggregate.sys, "argv",
                        ["eval_aggregate.py", "--input", str(results_file),
                         "--max-unsupported-pct", "5", "--min-claims", "30"])
    lines = []
    monkeypatch.setattr(eval_aggregate, "print",
                        lambda *a, **k: lines.append(" ".join(map(str, a))), raising=False)
    code = 0
    try:
        eval_aggregate.main()
    except SystemExit as e:
        code = e.code
    return [ln.rstrip() for ln in lines if ln.strip()], code


def test_committed_7c66k_rebuild_reproduces_the_in_cluster_aggregate(monkeypatch, capsys):
    """The validation behind 9jzmj: 7c66k ran on the same image and has a
    real aggregate. Every line the cluster printed, bar the estimated cost,
    comes out of the aggregate run on the rows rebuilt from its pod logs."""
    smoke = (_REPO / "eval/runs/hosted-smoke-3.log").read_text(encoding="utf-8").splitlines()
    start = next(i for i, ln in enumerate(smoke) if "NIGHTLY GROUNDING EVAL" in ln) - 1
    end = next(i for i, ln in enumerate(smoke) if ln.startswith("===EVAL_FINDINGS_TGZ_BEGIN"))
    cluster = [ln.rstrip() for ln in smoke[start:end] if ln.strip()]
    offline, code = _aggregate_lines(monkeypatch, capsys,
                                     _REPO / "eval/runs/7c66k-results-rebuilt.json")
    missing = [ln for ln in cluster if ln not in offline]
    assert len(missing) == 1 and "est. run cost" in missing[0]
    assert [ln for ln in offline if ln not in cluster] == []
    assert code == 1 and "  GATE FAILED: unsupported rate 7.92% exceeds 5.0%" in offline


def test_committed_9jzmj_rebuild_is_the_recorded_aggregate(monkeypatch, capsys):
    offline, code = _aggregate_lines(monkeypatch, capsys,
                                     _REPO / "eval/runs/9jzmj-results-rebuilt.json")
    recorded = (_REPO / "eval/runs/9jzmj-aggregate.txt").read_text(encoding="utf-8").splitlines()
    assert offline == [ln.rstrip() for ln in recorded[:-1] if ln.strip()]
    assert code == 0 and "  TOTAL     381    7   23  411     5.41    25.86" in offline
    assert "  numeric unsupported: 2/277 = 0.72% (95% CI 0.2–2.6%)" in offline


def test_probe_template_crosses_the_inline_limit_only_when_asked():
    big = probe.workflow(150000, "img", "Never", "financial-agent")
    small = probe.workflow(100000, "img", "Never", "financial-agent")
    size = lambda wf: len(json.dumps(wf["spec"]["templates"][0], separators=(",", ":")))  # noqa: E731
    assert size(big) > probe.LIMIT > size(small)
    assert probe.LIMIT == 131072
