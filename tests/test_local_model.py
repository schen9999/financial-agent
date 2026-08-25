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
