"""scripts/wait_for_model.py — vm-vllm's /v1/models check retries through
the window where the rollout is ready but the NodePort still refuses."""
import importlib.util
import pathlib

import pytest

_MOD_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "wait_for_model.py"
_spec = importlib.util.spec_from_file_location("wait_for_model", _MOD_PATH)
wfm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(wfm)


class _Clock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t

    def sleep(self, s):
        self.t += s


def _check_failing(n_failures, message="FATAL: ... unreachable ... Connection refused"):
    calls = []

    def check(url, name, timeout=None):
        calls.append(url)
        if len(calls) <= n_failures:
            raise SystemExit(message)
        return [name]
    return check, calls


def test_succeeds_after_refusals(capsys):
    clock = _Clock()
    check, calls = _check_failing(3)
    ids = wfm.wait_for_model("http://localhost:30880", "qwen7b", timeout=120, interval=5,
                             check=check, sleep=clock.sleep, clock=clock)
    assert ids == ["qwen7b"]
    assert len(calls) == 4
    assert clock.t == 15
    assert capsys.readouterr().out.count("not ready") == 3


def test_first_try_does_not_sleep():
    clock = _Clock()
    check, calls = _check_failing(0)
    wfm.wait_for_model("u", "m", check=check, sleep=clock.sleep, clock=clock)
    assert len(calls) == 1 and clock.t == 0


def test_gives_up_at_timeout_with_last_error():
    clock = _Clock()
    check, calls = _check_failing(10**6, "FATAL: expects 'qwen7b' but serves ['financial-lora']")
    with pytest.raises(SystemExit) as exc:
        wfm.wait_for_model("u", "qwen7b", timeout=120, interval=5,
                           check=check, sleep=clock.sleep, clock=clock)
    assert "serves ['financial-lora']" in str(exc.value)
    assert "gave up after 25 attempt(s) over 120s" in str(exc.value)
    assert clock.t <= 120
