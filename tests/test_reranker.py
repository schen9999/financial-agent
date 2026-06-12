import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from agent.tools import reranker


# Reranking config is read from the environment on every call. These vars are
# global process state, so save/restore them around each test and reset the
# cached cross-encoder instance so tests don't leak into one another.
_VARS = ["RERANKING_ENABLED", "RERANK_CANDIDATES", "RERANK_TOP_N", "RERANK_MODEL", "BASELINE_TOP_K"]


@pytest.fixture(autouse=True)
def _clean_env():
    saved = {k: os.environ.get(k) for k in _VARS}
    for k in _VARS:
        os.environ.pop(k, None)
    reranker._reranker = None
    yield
    for k, v in saved.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    reranker._reranker = None


class _FakeRerank:
    """Stand-in for SentenceTransformerRerank so unit tests never download or
    load the real cross-encoder model."""
    instances = 0

    def __init__(self, model, top_n):
        _FakeRerank.instances += 1
        self.model = model
        self.top_n = top_n


# ── config flags ────────────────────────────────────────────────────────────

def test_reranking_disabled_by_default():
    assert reranker.reranking_enabled() is False


def test_reranking_enabled_when_flag_true():
    os.environ["RERANKING_ENABLED"] = "true"
    assert reranker.reranking_enabled() is True


def test_reranking_flag_is_case_insensitive():
    os.environ["RERANKING_ENABLED"] = "TRUE"
    assert reranker.reranking_enabled() is True


def test_candidate_and_top_n_defaults():
    assert reranker.rerank_candidates() == 20
    assert reranker.rerank_top_n() == 3


def test_candidate_and_top_n_overrides():
    os.environ["RERANK_CANDIDATES"] = "30"
    os.environ["RERANK_TOP_N"] = "5"
    assert reranker.rerank_candidates() == 30
    assert reranker.rerank_top_n() == 5


def test_invalid_env_falls_back_to_defaults():
    os.environ["RERANK_CANDIDATES"] = "not-a-number"
    os.environ["RERANK_TOP_N"] = ""
    assert reranker.rerank_candidates() == 20
    assert reranker.rerank_top_n() == 3


# ── query-engine kwargs (the OFF/ON config paths) ───────────────────────────

def test_off_path_is_single_stage_top3():
    # Reranking off: original behaviour, no postprocessor, top-3 cosine.
    kwargs = reranker.query_engine_kwargs()
    assert kwargs == {"similarity_top_k": 3}
    assert "node_postprocessors" not in kwargs


def test_baseline_top_k_default_and_override():
    assert reranker.baseline_top_k() == 3
    os.environ["BASELINE_TOP_K"] = "5"
    assert reranker.baseline_top_k() == 5


def test_off_path_honors_baseline_top_k():
    # The no-rerank arm can retrieve a wider top-k without a postprocessor.
    os.environ["BASELINE_TOP_K"] = "5"
    kwargs = reranker.query_engine_kwargs()
    assert kwargs == {"similarity_top_k": 5}
    assert "node_postprocessors" not in kwargs


def test_on_path_is_two_stage(monkeypatch):
    monkeypatch.setattr(reranker, "SentenceTransformerRerank", _FakeRerank)
    os.environ["RERANKING_ENABLED"] = "true"
    os.environ["RERANK_CANDIDATES"] = "20"
    os.environ["RERANK_TOP_N"] = "5"

    kwargs = reranker.query_engine_kwargs()

    assert kwargs["similarity_top_k"] == 20  # over-retrieve
    assert len(kwargs["node_postprocessors"]) == 1
    post = kwargs["node_postprocessors"][0]
    assert isinstance(post, _FakeRerank)
    assert post.top_n == 5  # cross-encoder trims to final top-n


# ── reranker caching / lazy load ────────────────────────────────────────────

def test_get_reranker_is_cached(monkeypatch):
    monkeypatch.setattr(reranker, "SentenceTransformerRerank", _FakeRerank)
    _FakeRerank.instances = 0

    first = reranker.get_reranker()
    second = reranker.get_reranker()

    assert first is second  # cached, model loaded once
    assert _FakeRerank.instances == 1


def test_get_reranker_refreshes_top_n(monkeypatch):
    monkeypatch.setattr(reranker, "SentenceTransformerRerank", _FakeRerank)
    os.environ["RERANK_TOP_N"] = "3"
    r = reranker.get_reranker()
    assert r.top_n == 3

    # An A/B arm bumps top_n in-process; the cached instance reflects it.
    os.environ["RERANK_TOP_N"] = "5"
    r2 = reranker.get_reranker()
    assert r2 is r
    assert r2.top_n == 5


def test_off_path_never_loads_model(monkeypatch):
    # The expensive model must not be constructed when reranking is off.
    monkeypatch.setattr(reranker, "SentenceTransformerRerank", _FakeRerank)
    _FakeRerank.instances = 0
    reranker.query_engine_kwargs()  # off by default
    assert _FakeRerank.instances == 0


def test_custom_model_name(monkeypatch):
    monkeypatch.setattr(reranker, "SentenceTransformerRerank", _FakeRerank)
    os.environ["RERANK_MODEL"] = "BAAI/bge-reranker-large"
    r = reranker.get_reranker()
    assert r.model == "BAAI/bge-reranker-large"
