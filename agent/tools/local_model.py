"""Local fine-tuned model client — a drop-in for Haiku on the section generators.

The QLoRA-fine-tuned Qwen2.5-1.5B (see fine_tune_financial.ipynb) is served by
Ollama; `LocalChat` wraps Ollama's chat endpoint behind the same minimal
interface the agent uses for Haiku: `.invoke(messages).content`.

Routing is gated by USE_LOCAL_MODEL (default off). Only the two sections the
model was trained on are routed to it. Recent Developments and SEC Filing
Highlights always stay with Haiku — deterministic targets couldn't be built for
them (sparse news; table-bound MD&A figures). When the flag is off, nothing
changes and Haiku serves every section exactly as before.
"""
import os

import requests

# Single source of truth for which sections the local model serves. Mirrors
# LOCAL_SECTIONS in scripts/build_dataset.py (the set the model is trained on).
LOCAL_SECTIONS = frozenset({
    "### Financial Health",
    "### Risk Factors",
})


def use_local_model() -> bool:
    """Whether to route trained sections to the local fine-tuned model."""
    return os.getenv("USE_LOCAL_MODEL", "false").strip().lower() == "true"


def is_local_section(heading: str) -> bool:
    """True for sections the local model is trained to serve."""
    return heading in LOCAL_SECTIONS


class _Response:
    """Mimics a LangChain message response so callers can read `.content`."""
    def __init__(self, content: str):
        self.content = content


class LocalChat:
    """Minimal Ollama chat client with a ChatAnthropic-compatible `.invoke`."""

    def __init__(self, model: str | None = None, url: str | None = None, temperature: float = 0.1):
        self.model = model or os.getenv("LOCAL_MODEL_NAME", "financial-lora")
        self.url = (url or os.getenv("LOCAL_MODEL_URL", "http://localhost:11434")).rstrip("/")
        self.temperature = temperature

    @staticmethod
    def _role(message) -> str:
        name = type(message).__name__.lower()
        if "system" in name:
            return "system"
        if "ai" in name or "assistant" in name:
            return "assistant"
        return "user"

    def invoke(self, messages):
        """messages: list of LangChain message objects (or anything with .content).
        Returns an object exposing `.content`, matching `_haiku.invoke(...)`."""
        payload = {
            "model": self.model,
            "stream": False,
            "options": {"temperature": self.temperature},
            "messages": [
                {"role": self._role(m), "content": getattr(m, "content", str(m))}
                for m in messages
            ],
        }
        resp = requests.post(f"{self.url}/api/chat", json=payload, timeout=180)
        resp.raise_for_status()
        return _Response(resp.json()["message"]["content"])
