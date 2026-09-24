import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from agent.tools import local_model
from agent.tools.local_model import use_local_model, is_local_section, LocalChat


@pytest.fixture(autouse=True)
def _clean_env():
    saved = {k: os.environ.get(k) for k in ("USE_LOCAL_MODEL", "LOCAL_MODEL_NAME", "LOCAL_MODEL_URL", "LOCAL_MODEL_BACKEND")}
    for k in saved:
        os.environ.pop(k, None)
    yield
    for k, v in saved.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


# ── flags / routing ──────────────────────────────────────────────────────────

def test_use_local_model_default_off():
    assert use_local_model() is False


def test_use_local_model_flag():
    os.environ["USE_LOCAL_MODEL"] = "true"
    assert use_local_model() is True


def test_local_sections_are_the_two_trained():
    assert is_local_section("### Financial Health")
    assert is_local_section("### Risk Factors")
    # SEC Highlights (table-bound figures) and Recent Developments (sparse news)
    # stay with Haiku.
    assert not is_local_section("### SEC Filing Highlights")
    assert not is_local_section("### Recent Developments")


# ── message conversion / invoke ───────────────────────────────────────────────

class _Msg:
    def __init__(self, content):
        self.content = content


class HumanMessage(_Msg):
    pass


class SystemMessage(_Msg):
    pass


def test_role_mapping():
    assert LocalChat._role(HumanMessage("x")) == "user"
    assert LocalChat._role(SystemMessage("x")) == "system"


def test_invoke_posts_to_ollama_and_returns_content(monkeypatch):
    captured = {}

    class _Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"message": {"content": "### Financial Health\nstub"}}

    def fake_post(url, json=None, timeout=None):
        captured["url"] = url
        captured["json"] = json
        return _Resp()

    monkeypatch.setattr(local_model.requests, "post", fake_post)

    chat = LocalChat(model="financial-lora", url="http://localhost:11434")
    out = chat.invoke([HumanMessage("write the section")])

    assert out.content == "### Financial Health\nstub"
    assert captured["url"].endswith("/api/chat")
    assert captured["json"]["model"] == "financial-lora"
    assert captured["json"]["messages"][0]["role"] == "user"
    assert captured["json"]["stream"] is False


def test_model_and_url_from_env():
    os.environ["LOCAL_MODEL_NAME"] = "my-model"
    os.environ["LOCAL_MODEL_URL"] = "http://host:9999/"
    chat = LocalChat()
    assert chat.model == "my-model"
    assert chat.url == "http://host:9999"  # trailing slash stripped


# ── OpenAI-compatible backend (vLLM) ─────────────────────────────────────────

def test_backend_defaults_to_ollama():
    assert local_model.local_model_backend() == "ollama"


def test_invoke_openai_backend_posts_chat_completions(monkeypatch):
    os.environ["LOCAL_MODEL_BACKEND"] = "openai"
    captured = {}

    class _Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"choices": [{"message": {"content": "### Risk Factors\nstub"}}]}

    def fake_post(url, json=None, timeout=None):
        captured["url"] = url
        captured["json"] = json
        return _Resp()

    monkeypatch.setattr(local_model.requests, "post", fake_post)

    chat = LocalChat(model="financial-lora", url="http://vllm:8000")
    out = chat.invoke([HumanMessage("write the section")])

    assert out.content == "### Risk Factors\nstub"
    assert captured["url"].endswith("/v1/chat/completions")
    assert captured["json"]["model"] == "financial-lora"
    assert captured["json"]["messages"][0]["role"] == "user"
    # OpenAI schema: temperature is top-level, no Ollama "options"/"stream" keys
    assert "options" not in captured["json"]
    assert captured["json"]["temperature"] == pytest.approx(0.1)


def _capture_openai_bodies(monkeypatch, models):
    os.environ["LOCAL_MODEL_BACKEND"] = "openai"
    bodies = []

    class _Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"choices": [{"message": {"content": "ok"}}]}

    def fake_post(url, json=None, timeout=None):
        bodies.append(json)
        return _Resp()

    monkeypatch.setattr(local_model.requests, "post", fake_post)
    for m in models:
        LocalChat(model=m, url="http://vllm:8000", temperature=0.1).invoke(
            [HumanMessage("write the section")])
    return bodies


def test_openai_request_identical_across_served_models(monkeypatch):
    """A model comparison must vary only the model: vLLM fills any omitted
    sampling param from each model's own generation_config.json, so every
    param is sent explicitly and the bodies differ only in `model`."""
    models = ["financial-lora", "qwen7b", "llama8b"]
    bodies = _capture_openai_bodies(monkeypatch, models)
    assert [b["model"] for b in bodies] == models
    stripped = [{k: v for k, v in b.items() if k != "model"} for b in bodies]
    assert stripped[0] == stripped[1] == stripped[2]
    assert stripped[0] == {
        "temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20,
        "repetition_penalty": 1.1, "min_p": 0.0,
        "messages": [{"role": "user", "content": "write the section"}],
    }


def test_sampling_params_are_what_is_sent(monkeypatch):
    body = _capture_openai_bodies(monkeypatch, ["financial-lora"])[0]
    chat = LocalChat(model="financial-lora", url="http://vllm:8000", temperature=0.1)
    sent = {k: v for k, v in body.items() if k not in ("model", "messages")}
    assert chat.sampling_params() == sent


def test_ollama_path_sends_temperature_only(monkeypatch):
    captured = {}

    class _Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"message": {"content": "ok"}}

    def fake_post(url, json=None, timeout=None):
        captured["json"] = json
        return _Resp()

    monkeypatch.setattr(local_model.requests, "post", fake_post)
    chat = LocalChat(model="financial-lora", url="http://localhost:11434")
    chat.invoke([HumanMessage("x")])
    assert captured["json"]["options"] == {"temperature": pytest.approx(0.1)}
    assert chat.sampling_params() == {"temperature": pytest.approx(0.1)}
