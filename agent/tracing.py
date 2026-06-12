"""LangSmith tracing setup.

Importing this module reconciles the LANGSMITH_* and LANGCHAIN_* environment
variable aliases so the key can live under either name in .env, matching how
the project reads its other secrets. The actual API key is never hardcoded — it
is read from the environment.

LangChain ChatAnthropic calls (sections, synthesis, the ReAct agent) auto-trace
when LANGCHAIN_TRACING_V2=true, capturing prompts, completions, token counts,
latency and cost. The re-exported `traceable` decorator adds spans around the
non-LangChain code (LlamaIndex RAG, the Celery task) and carries the
request-type / model tags. When tracing is disabled or no key is present,
`traceable` is a near-zero-overhead pass-through, so decorated code runs
unchanged.
"""
import os

from dotenv import load_dotenv
from langsmith import traceable  # re-exported for use across the agent

load_dotenv()

# The langsmith SDK authenticates with LANGCHAIN_API_KEY (legacy) or
# LANGSMITH_API_KEY (current). Accept whichever is set and mirror it to both.
_key = os.getenv("LANGSMITH_API_KEY") or os.getenv("LANGCHAIN_API_KEY")
if _key:
    os.environ.setdefault("LANGCHAIN_API_KEY", _key)
    os.environ.setdefault("LANGSMITH_API_KEY", _key)

# Tracing flag and project name have the same dual-naming.
_tracing = os.getenv("LANGSMITH_TRACING") or os.getenv("LANGCHAIN_TRACING_V2")
if _tracing:
    os.environ.setdefault("LANGCHAIN_TRACING_V2", _tracing)

_project = os.getenv("LANGSMITH_PROJECT") or os.getenv("LANGCHAIN_PROJECT")
if _project:
    os.environ.setdefault("LANGCHAIN_PROJECT", _project)


def tracing_enabled() -> bool:
    """True when LangSmith tracing is on and a key is available."""
    return (
        os.getenv("LANGCHAIN_TRACING_V2", "").strip().lower() == "true"
        and bool(os.getenv("LANGCHAIN_API_KEY"))
    )


__all__ = ["traceable", "tracing_enabled"]
