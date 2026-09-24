"""eval/runtime_guards.py — credit-balance errors and a wrong or missing
local model must fail loudly."""
import io
import json

import pytest

from eval import runtime_guards
from eval.runtime_guards import check_fatal_api_error, check_local_model_served


class _FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def _serve(monkeypatch, ids, seen=None):
    def fake_urlopen(url, timeout=None):
        if seen is not None:
            seen.append(url)
        body = {"object": "list", "data": [{"id": i, "object": "model"} for i in ids]}
        return _FakeResponse(json.dumps(body).encode())
    monkeypatch.setattr(runtime_guards.urllib.request, "urlopen", fake_urlopen)


def test_local_model_listed_passes(monkeypatch):
    seen = []
    _serve(monkeypatch, ["qwen7b"], seen)
    assert check_local_model_served("http://vllm:8000/", "qwen7b") == ["qwen7b"]
    assert seen == ["http://vllm:8000/v1/models"]


def test_local_model_not_listed_exits(monkeypatch):
    _serve(monkeypatch, ["financial-lora"])
    with pytest.raises(SystemExit) as exc:
        check_local_model_served("http://vllm:8000", "qwen7b")
    assert "'qwen7b'" in str(exc.value)
    assert "financial-lora" in str(exc.value)


def test_local_model_unreachable_exits(monkeypatch):
    def refuse(url, timeout=None):
        raise ConnectionRefusedError("connection refused")
    monkeypatch.setattr(runtime_guards.urllib.request, "urlopen", refuse)
    with pytest.raises(SystemExit) as exc:
        check_local_model_served("http://vllm:8000", "qwen7b")
    assert "unreachable" in str(exc.value)


def test_credit_balance_error_raises_system_exit():
    err = Exception(
        "Error code: 400 - {'error': {'message': 'Your credit balance is too "
        "low to access the Anthropic API.'}}"
    )
    with pytest.raises(SystemExit) as exc:
        check_fatal_api_error(err)
    assert "credit balance too low" in str(exc.value)
    assert "skipped tickers" in str(exc.value)


def test_ordinary_errors_pass_through():
    assert check_fatal_api_error(ConnectionError("connection reset")) is None
    assert check_fatal_api_error(TimeoutError("timed out")) is None
