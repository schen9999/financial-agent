"""sec_common.lookup_cik — authoritative, cached, retry-on-failure.
Offline: requests is monkeypatched; the MSFT row mirrors the real mapping."""
import pytest

import agent.tools.sec_common as sc

PAYLOAD = {
    "0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."},
    "1": {"cik_str": 789019, "ticker": "MSFT", "title": "MICROSOFT CORP"},
}


class _Resp:
    def raise_for_status(self):
        pass

    def json(self):
        return PAYLOAD


@pytest.fixture(autouse=True)
def _reset_cache():
    sc._cik_map = None
    yield
    sc._cik_map = None


def test_msft_resolves_zero_padded(monkeypatch):
    monkeypatch.setattr(sc.requests, "get", lambda *a, **k: _Resp())
    assert sc.lookup_cik("MSFT") == "0000789019"
    assert sc.lookup_cik("msft ") == "0000789019"  # case/space insensitive


def test_single_fetch_cached(monkeypatch):
    calls = []
    monkeypatch.setattr(sc.requests, "get",
                        lambda *a, **k: calls.append(1) or _Resp())
    sc.lookup_cik("AAPL")
    sc.lookup_cik("MSFT")
    assert len(calls) == 1


def test_unknown_ticker_none(monkeypatch):
    monkeypatch.setattr(sc.requests, "get", lambda *a, **k: _Resp())
    assert sc.lookup_cik("ZZZZZZ") is None


def test_fetch_failure_returns_none_and_retries(monkeypatch):
    def boom(*a, **k):
        raise ConnectionError("edgar throttled")

    monkeypatch.setattr(sc.requests, "get", boom)
    assert sc.lookup_cik("MSFT") is None
    assert sc._cik_map is None  # failure not cached
    monkeypatch.setattr(sc.requests, "get", lambda *a, **k: _Resp())
    assert sc.lookup_cik("MSFT") == "0000789019"  # next call succeeds
