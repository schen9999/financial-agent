"""Retried eval attempts stay visible: the harness's attempt records
(eval/attempts.py, agent/llm_ledger.emit_calls), the report read back from
the workflow object and pod logs, the traffic proof over every attempt, and
the aggregate's retry and claim-density lines."""
import importlib.util
import json
import pathlib

import pytest

from agent import llm_ledger
from eval import attempts

_REPO = pathlib.Path(__file__).resolve().parents[1]


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, _REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


eval_aggregate = _load("eval_aggregate_attempts", "scripts/eval_aggregate.py")
proof = _load("slm_traffic_proof_attempts", "scripts/slm_traffic_proof.py")

WF = "grounding-eval-slm-cpu-test1"


# ── what the harness writes ──────────────────────────────────────────────────

@pytest.fixture
def emitting():
    lines = []
    llm_ledger.drain()
    llm_ledger.enable()
    llm_ledger.emit_calls(lines.append)
    yield lines
    llm_ledger.emit_calls(None)
    llm_ledger.enable(False)
    llm_ledger.drain()


def test_ledger_emits_each_call_and_later_flags(emitting):
    llm_ledger.record("rag:risks", "slm-cpu", "m", prompt_tokens=2635, completion_tokens=702,
                      latency_s=1.0, finish_reason="stop")
    llm_ledger.record("synthesis", "slm-cpu", "m", prompt_tokens=1480, completion_tokens=4096,
                      latency_s=2.0, finish_reason="length")
    llm_ledger.flag_last("synthesis", format_failure=True)
    assert [ln.split(" ", 1)[0] for ln in emitting] == ["EVAL_LLM_CALL", "EVAL_LLM_CALL",
                                                         "EVAL_LLM_FLAG"]
    calls = attempts.parse_pod_log("\n".join(emitting))["calls"]
    assert [(c["site"], c["prompt_tokens"], c["completion_tokens"]) for c in calls] == [
        ("rag:risks", 2635, 702), ("synthesis", 1480, 4096)]
    assert calls[1]["truncated"] and calls[1]["format_failure"] and not calls[0]["format_failure"]


def test_emission_is_off_unless_the_harness_turns_it_on(capsys):
    llm_ledger.drain()
    llm_ledger.enable()
    llm_ledger.record("synthesis", "anthropic", "m", prompt_tokens=1, completion_tokens=1)
    llm_ledger.enable(False)
    assert "seq" not in llm_ledger.drain()[0]
    assert "EVAL_LLM_CALL" not in capsys.readouterr().out


def _end(capsys):
    (line,) = [ln for ln in capsys.readouterr().out.splitlines()
               if ln.startswith(attempts.END_PREFIX)]
    return json.loads(line[len(attempts.END_PREFIX):])


def test_end_record_on_every_exit_path(monkeypatch, capsys):
    monkeypatch.setenv("EVAL_ATTEMPT", "1")
    monkeypatch.setenv("EVAL_POD", "pod-x")
    attempts.run_recorded(lambda: None, lambda: 7)
    assert _end(capsys) == {"attempt": 1, "pod": "pod-x", "outcome": "ok", "calls": 7}

    def credit_guard():
        raise SystemExit("FATAL: Anthropic credit balance too low — stopping this eval run now.\n"
                         "  underlying error: 400")

    with pytest.raises(SystemExit):
        attempts.run_recorded(credit_guard, lambda: 7)
    end = _end(capsys)
    assert (end["outcome"], end["kind"]) == ("failed", "fatal")
    assert end["cause"] == "FATAL: Anthropic credit balance too low — stopping this eval run now."

    def crash():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        attempts.run_recorded(crash)
    assert _end(capsys)["cause"] == "RuntimeError: boom"


def test_attempt_number_survives_an_unresolved_template(monkeypatch):
    monkeypatch.setenv("EVAL_ATTEMPT", "{{retries}}")
    assert attempts.attempt_number() == 0


# ── read back ────────────────────────────────────────────────────────────────

def _node(ticker, idx, attempt, phase, suffix, message=None):
    return {"id": f"{WF}-{suffix}", "type": "Pod", "templateName": "eval-one", "phase": phase,
            "displayName": f"eval-ticker({idx}:{ticker})({attempt})", "message": message,
            "inputs": {"parameters": [{"name": "ticker", "value": ticker}]}}


def _workflow(*nodes):
    agg = {"id": f"{WF}-9", "type": "Pod", "templateName": "aggregate", "phase": "Succeeded",
           "displayName": "aggregate"}
    return {"metadata": {"name": WF},
            "status": {"phase": "Succeeded", "nodes": {n["id"]: n for n in (*nodes, agg)}}}


def _call(seq, site, prompt, compl, **flags):
    return attempts.CALL_PREFIX + json.dumps({
        "seq": seq, "site": site, "endpoint": "slm-cpu", "prompt_tokens": prompt,
        "completion_tokens": compl, "truncated": False, "repeat_run": False, "retry": False,
        "parse_failure": False, "format_failure": False, "error": None, **flags})


def _pod_log(pod, lines):
    return "\n".join(f"[pod/{pod}/main] {ln}" for ln in lines) + "\n"


FAILED_POD, RETRY_POD = f"{WF}-eval-one-111", f"{WF}-eval-one-222"
BEGIN = attempts.BEGIN_PREFIX + '{"attempt": 0, "tickers": ["NVDA"]}'
FATAL = "FATAL: Anthropic credit balance too low — stopping this eval run now."
END_FAILED = attempts.END_PREFIX + json.dumps(
    {"attempt": 0, "outcome": "failed", "kind": "fatal", "cause": FATAL, "calls": 2})
RETRIED = _workflow(_node("NVDA", 1, 0, "Failed", "111", "main: Error (exit code 1)"),
                    _node("NVDA", 1, 1, "Succeeded", "222"),
                    _node("AAPL", 0, 0, "Succeeded", "333"))


def _report(failed_lines):
    log = _pod_log(FAILED_POD, failed_lines) + _pod_log(RETRY_POD, [BEGIN, "ok"])
    return attempts.build_report(RETRIED, attempts.split_pod_logs(log))


def test_report_lists_the_failed_attempt_with_cause_tokens_and_flags():
    rep = _report([BEGIN, _call(1, "rag:risks", 2635, 702),
                   _call(2, "synthesis", 1480, 842, format_failure=True), FATAL, END_FAILED])
    assert (rep["retries"], rep["retried_tickers"], rep["tickers"]) == (1, ["NVDA"], 2)
    (a,) = rep["failed_attempts"]
    assert (a["ticker"], a["attempt"], a["pod"], a["record"]) == ("NVDA", 0, FAILED_POD, "complete")
    assert a["cause"] == FATAL and a["message"] == "main: Error (exit code 1)"
    assert rep["failed_by_endpoint"]["slm-cpu"]["prompt_tokens"] == 4115
    assert rep["failed_by_endpoint"]["slm-cpu"]["format_failure"] == 1
    text = "\n".join(attempts.format_report(rep))
    assert "Argo retries      : 1 (NVDA)" in text
    assert "LLM calls FROM THIS FAILED ATTEMPT" in text
    assert "failure counts FROM FAILED ATTEMPTS: Trunc 0, Loop 0, Parse 0, Fmt 1, Retry 0, Err 0" in text


def test_killed_pod_keeps_its_calls_but_is_marked_incomplete():
    rep = _report([BEGIN, _call(1, "rag:risks", 2635, 702)])
    (a,) = rep["failed_attempts"]
    assert a["record"] == "no END" and rep["unrecorded"] == [a]
    assert rep["failed_by_endpoint"]["slm-cpu"]["completion_tokens"] == 702
    assert "INCOMPLETE" in "\n".join(attempts.format_report(rep))


def test_end_record_with_calls_missing_from_the_log_is_not_complete():
    rep = _report([BEGIN, _call(1, "rag:risks", 2635, 702), END_FAILED])  # END says 2 calls
    assert rep["failed_attempts"][0]["record"] == "no END"


def test_old_image_pod_has_no_record_and_the_cause_comes_from_its_fatal_line():
    rep = _report(["  [NVDA | slm-full-cpu] judging...", FATAL, "Error: exit status 1"])
    (a,) = rep["failed_attempts"]
    assert (a["record"], a["cause"], a["calls"]) == ("none", FATAL, [])
    assert "UNRECORDED" in "\n".join(attempts.format_report(rep))


def test_no_retries_report():
    rep = attempts.build_report(_workflow(_node("AAPL", 0, 0, "Succeeded", "333")), {})
    assert (rep["retries"], rep["failed_attempts"]) == (0, [])
    assert "every eval pod succeeded on its first attempt" in "\n".join(attempts.format_report(rep))


def test_captured_9jddz_run_reports_its_nvda_retry():
    wf = _REPO / "eval/runs/9jddz-workflow.json"
    log = _REPO / "eval/runs/slm-proof-9jddz/grounding-eval-slm-cpu-9jddz.log"
    if not (wf.exists() and log.exists()):
        pytest.skip("9jddz capture not present")
    rep = attempts.load(str(wf), str(log))
    (a,) = rep["failed_attempts"]
    assert (rep["retries"], a["ticker"], a["attempt"], a["record"]) == (1, "NVDA", 0, "none")
    assert a["cause"].startswith("FATAL: Anthropic credit balance too low")


# ── traffic proof over every attempt ─────────────────────────────────────────

METRICS = ("llamacpp:prompt_tokens_total {p}\nllamacpp:prompt_tokens_cached_total 0\n"
           "llamacpp:tokens_predicted_total {t}\nllamacpp:n_decode_total 5\n")


def _snap(p, t):
    return {"endpoint": "slm-cpu", "url": "u", "build": "b", "model_path": "/m.gguf",
            "counters": proof.parse_metrics(METRICS.format(p=p, t=t))}


TRAFFIC = {"endpoint": "slm-cpu", "calls": 14, "prompt_tokens": 20000, "completion_tokens": 5000,
           "errored_calls": 0, "calls_without_usage": 0}
RECORDED = [BEGIN, _call(1, "rag:risks", 2635, 702), _call(2, "synthesis", 1480, 842), END_FAILED]


def test_proof_is_exact_only_when_failed_attempts_are_counted():
    server = _snap(20000 + 4115, 5000 + 1544)
    v, lines = proof.verify(_snap(0, 0), server, TRAFFIC, _report(RECORDED))
    assert v == "EXACT"
    assert any("failed attempts: 1 attempt(s) (NVDA: FATAL" in ln for ln in lines)
    # the same run judged on final attempts alone would not balance
    assert proof.verify(_snap(0, 0), server, TRAFFIC, _report([]))[0] == "FAIL"


def test_proof_fails_and_says_why_when_a_failed_attempt_left_no_record():
    v, lines = proof.verify(_snap(0, 0), _snap(30123, 7943), TRAFFIC, _report([FATAL]))
    assert v == "FAIL"
    assert any("NVDA attempt 0: call record MISSING" in ln for ln in lines)
    assert any("10123 prompt + 2943 completion tokens MORE" in ln
               and "no complete call record (NVDA attempt 0)" in ln for ln in lines)


def test_proof_never_gives_lower_bound_past_an_unrecorded_attempt():
    errored = dict(TRAFFIC, errored_calls=1, calls_without_usage=1)
    assert proof.verify(_snap(0, 0), _snap(30123, 7943), errored, _report([FATAL]))[0] == "FAIL"
    assert proof.verify(_snap(0, 0), _snap(30123, 7943), errored, _report(RECORDED))[0] == "LOWER-BOUND"


def test_proof_killed_attempt_with_an_unlogged_call_in_flight_fails():
    killed = [BEGIN, _call(1, "rag:risks", 2635, 702)]
    v, lines = proof.verify(_snap(0, 0), _snap(22635 + 1480, 5702 + 300), TRAFFIC, _report(killed))
    assert v == "FAIL" and any("call record INCOMPLETE" in ln for ln in lines)
    # nothing was in flight: the logged calls balance, and that is exact
    assert proof.verify(_snap(0, 0), _snap(22635, 5702), TRAFFIC, _report(killed))[0] == "EXACT"


def test_proof_without_a_workflow_says_retries_were_not_looked_for():
    v, lines = proof.verify(_snap(0, 0), _snap(20000, 5000), TRAFFIC)
    assert v == "EXACT" and any("NOT LOOKED FOR" in ln for ln in lines)


# ── aggregate: retries and claim density ─────────────────────────────────────

def _row(ticker, total, supported, numeric=None, **extra):
    row = {"ticker": ticker, "supported": supported, "unsupported": total - supported,
           "inference": 0, "total": total, "retrieval_s": 1.0, "pipeline_s": 2.0, **extra}
    if numeric is not None:  # (numeric claims, unsupported among them)
        row["numeric_claims"] = {"total": numeric[0], "unsupported": numeric[1],
                                 "supported": numeric[0] - numeric[1], "inference": 0}
    return row


def _aggregate(monkeypatch, tmp_path, rows):
    f = tmp_path / "all.json"
    f.write_text(json.dumps([json.dumps({"results": rows, "skipped": [], "failures": []})]),
                 encoding="utf-8")
    captured = {}
    monkeypatch.delenv("EVAL_ARTIFACTS_PUT_URL", raising=False)
    monkeypatch.setattr(eval_aggregate, "maybe_upload_artifacts",
                        lambda summary, results, skipped: captured.update(summary))
    monkeypatch.setattr(eval_aggregate.sys, "argv",
                        ["eval_aggregate.py", "--input", str(f), "--min-claims", "1",
                         "--max-unsupported-pct", "50"])
    try:
        eval_aggregate.main()
    except SystemExit:
        pass
    return captured


def test_aggregate_reports_claim_density_and_retried_tickers(monkeypatch, tmp_path, capsys):
    rows = [_row("AMZN", 2, 2, (2, 0), attempt=0), _row("V", 2, 2, (2, 0), attempt=0),
            _row("TSLA", 12, 10, (4, 1), attempt=0), _row("NVDA", 4, 4, (4, 0), attempt=1)]
    summary = _aggregate(monkeypatch, tmp_path, rows)
    out = capsys.readouterr().out
    assert "claims per ticker : mean 5.0, min 2 (AMZN, V)" in out
    assert "numeric claims    : 12 = mean 3.0/ticker, min 2 (AMZN, V)" in out
    assert "numeric unsupported: 1/12 = 8.33%" in out
    assert "Argo retries      : 1 (NVDA)" in out
    assert "FINAL attempts only" in out
    t = summary["totals"]
    assert t["claims_per_ticker"] == {"mean": 5.0, "min": 2, "min_tickers": ["AMZN", "V"]}
    assert t["numeric_claims"] == {"mean": 3.0, "min": 2, "min_tickers": ["AMZN", "V"],
                                   "total": 12, "unsupported": 1, "unrecorded": 0}
    assert t["retried_tickers"] == ["NVDA"]


def test_aggregate_never_reports_missing_numeric_counts_as_zero(monkeypatch, tmp_path, capsys):
    _aggregate(monkeypatch, tmp_path, [_row("AAPL", 10, 9, attempt=0)])
    assert "numeric claims    : unrecorded" in capsys.readouterr().out
    _aggregate(monkeypatch, tmp_path, [_row("AAPL", 10, 9, attempt=0),
                                       _row("V", 2, 2, (2, 0), attempt=0)])
    out = capsys.readouterr().out
    assert "numeric claims    : 2 = mean 2.0/ticker, min 2 (V)" in out
    assert "(1 row(s) unrecorded)" in out


def test_attempts_report_is_written_as_json(tmp_path, capsys):
    wf, log, out = tmp_path / "wf.json", tmp_path / "pods.log", tmp_path / "attempts.json"
    wf.write_text(json.dumps(RETRIED), encoding="utf-8")
    log.write_text(_pod_log(FAILED_POD, RECORDED), encoding="utf-8")
    assert attempts.main(["--workflow", str(wf), "--log", str(log), "--json-out", str(out)]) == 0
    rep = json.loads(out.read_text(encoding="utf-8"))
    assert rep["retried_tickers"] == ["NVDA"]
    assert rep["failed_attempts"][0]["by_site"]["synthesis"]["completion_tokens"] == 842
    assert "attempts record written" in capsys.readouterr().out


def test_aggregate_says_when_rows_do_not_record_attempts(monkeypatch, tmp_path, capsys):
    _aggregate(monkeypatch, tmp_path, [_row("AAPL", 10, 9)])
    out = capsys.readouterr().out
    assert "Argo retries      : 0   (1 row(s) from an image that does not record attempts)" in out
    assert "FINAL attempts only" not in out
