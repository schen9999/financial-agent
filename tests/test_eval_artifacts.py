"""Eval artifact archival (scripts/eval_aggregate.py, task: Object Storage
wiring). The upload is env-gated (EVAL_ARTIFACTS_PUT_URL, off by default) and
best-effort — these tests pin all three properties with a mocked HTTP client:
no env means no network call, the enabled path PUTs the right objects, and an
upload failure warns without ever changing the gate's exit code.
"""
import importlib.util
import io
import json
import pathlib
import urllib.error

import pytest

_MOD_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "eval_aggregate.py"
_spec = importlib.util.spec_from_file_location("eval_aggregate", _MOD_PATH)
eval_aggregate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(eval_aggregate)

SUMMARY = {"totals": {"claims": 10}, "gate": {"passed": True, "failures": []}}
RESULTS = [{"ticker": "AAPL", "supported": 5, "unsupported": 0, "inference": 1,
            "total": 6, "retrieval_s": 1.0, "pipeline_s": 2.0}]


class _FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_disabled_without_env_makes_no_call(monkeypatch):
    monkeypatch.delenv("EVAL_ARTIFACTS_PUT_URL", raising=False)
    monkeypatch.setattr(
        eval_aggregate.urllib.request, "urlopen",
        lambda *a, **k: pytest.fail("urlopen must not be called when archival is off"),
    )
    assert eval_aggregate.maybe_upload_artifacts(SUMMARY, RESULTS, []) is None


def test_enabled_puts_summary_and_results(monkeypatch):
    monkeypatch.setenv("EVAL_ARTIFACTS_PUT_URL", "https://example.test/p/tok/n/ns/b/bucket/o/")
    calls = []

    def fake_urlopen(req, timeout=None):
        calls.append(req)
        return _FakeResponse()

    monkeypatch.setattr(eval_aggregate.urllib.request, "urlopen", fake_urlopen)
    assert eval_aggregate.maybe_upload_artifacts(SUMMARY, RESULTS, ["MSFT"]) is True

    assert len(calls) == 2
    urls = [c.full_url for c in calls]
    assert all(u.startswith("https://example.test/p/tok/n/ns/b/bucket/o/eval-runs/") for u in urls)
    assert urls[0].endswith("/aggregate.json")
    assert urls[1].endswith("/results.json")
    for c in calls:
        assert c.get_method() == "PUT"
        assert c.get_header("Content-type") == "application/json"
    assert json.loads(calls[0].data) == SUMMARY
    assert json.loads(calls[1].data) == {"results": RESULTS, "skipped": ["MSFT"]}


def test_upload_failure_warns_and_returns_false(monkeypatch, capsys):
    monkeypatch.setenv("EVAL_ARTIFACTS_PUT_URL", "https://example.test/o/")

    def failing_urlopen(req, timeout=None):
        raise urllib.error.URLError("boom")

    monkeypatch.setattr(eval_aggregate.urllib.request, "urlopen", failing_urlopen)
    assert eval_aggregate.maybe_upload_artifacts(SUMMARY, RESULTS, []) is False
    out = capsys.readouterr().out
    assert "WARNING: artifact upload failed" in out
    assert "artifacts uploaded" not in out


def test_upload_failure_never_fails_the_gate(monkeypatch, tmp_path, capsys):
    """End-to-end through main(): passing gate + broken archive -> exit 0."""
    payload = json.dumps({"results": RESULTS, "skipped": []})
    input_file = tmp_path / "all_results.json"
    input_file.write_text(json.dumps([payload]), encoding="utf-8")

    monkeypatch.setenv("EVAL_ARTIFACTS_PUT_URL", "https://example.test/o/")
    monkeypatch.setattr(
        eval_aggregate.urllib.request, "urlopen",
        lambda *a, **k: (_ for _ in ()).throw(urllib.error.URLError("down")),
    )
    monkeypatch.setattr(
        eval_aggregate.sys, "argv",
        ["eval_aggregate.py", "--input", str(input_file), "--min-claims", "1"],
    )
    eval_aggregate.main()  # raises SystemExit(1) only on gate failure
    out = capsys.readouterr().out
    assert "GATE PASSED" in out
    assert "WARNING: artifact upload failed" in out
