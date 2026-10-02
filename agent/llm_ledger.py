"""Per-call LLM ledger: one record per model call, for the eval's blast-radius
metrics (calls per ticker, tokens and latency per call site, truncations,
repetition loops, parse failures, retries, which endpoint served each call).

Off unless enabled: the eval harness calls enable(); the app never does, so a
long-running API process accumulates nothing. Recording is observation only —
it never changes what a call sends or returns. Thread-safe: sections run
concurrently. The call site for code that cannot name it directly (the RAG
query engine's LLM) comes from a thread-local set by the caller (site()).
"""
import re
import threading
import time
from contextlib import contextmanager

_lock = threading.Lock()
_records: list[dict] = []
_enabled = False
_local = threading.local()


def enable(on: bool = True):
    global _enabled
    _enabled = on


def enabled() -> bool:
    return _enabled


@contextmanager
def site(name: str):
    """Name the call site for calls made in this thread inside the block."""
    prev = getattr(_local, "site", None)
    _local.site = name
    try:
        yield
    finally:
        _local.site = prev


def current_site(default: str = "unknown") -> str:
    return getattr(_local, "site", None) or default


def record(site_name: str, endpoint: str, model: str | None = None, *,
           prompt_tokens: int | None = None, completion_tokens: int | None = None,
           latency_s: float | None = None, finish_reason: str | None = None,
           text: str | None = None, max_tokens: int | None = None,
           retry: bool = False, parse_failure: bool = False,
           format_failure: bool = False, error: str | None = None):
    if not _enabled:
        return
    truncated = finish_reason == "length"
    rec = {
        "site": site_name, "endpoint": endpoint, "model": model,
        "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens,
        "latency_s": round(latency_s, 3) if latency_s is not None else None,
        "finish_reason": finish_reason, "max_tokens": max_tokens,
        "truncated": truncated,
        "repeat_run": bool(text) and repetition_run(text),
        "retry": retry, "parse_failure": parse_failure,
        "format_failure": format_failure, "error": error,
    }
    with _lock:
        _records.append(rec)


def flag_last(site_name: str, **flags):
    """Set flags (parse_failure, format_failure, ...) on the newest record for
    `site_name` — the call whose output just failed a check. Sites are
    distinct per concurrent call (section:<name>, rag:<which>)."""
    if not _enabled:
        return
    with _lock:
        for rec in reversed(_records):
            if rec["site"] == site_name:
                rec.update(flags)
                return


def record_response(site_name: str, endpoint: str, model: str | None,
                    response, t0: float, **extra):
    """Record a LangChain message response (hosted ChatAnthropic or our SLM
    client): usage_metadata + finish/stop reason when the provider sets them."""
    usage = getattr(response, "usage_metadata", None) or {}
    meta = getattr(response, "response_metadata", None) or {}
    finish = meta.get("finish_reason") or meta.get("stop_reason")
    if finish == "max_tokens":  # Anthropic's name for a length stop
        finish = "length"
    content = getattr(response, "content", None)
    record(site_name, endpoint, model,
           prompt_tokens=usage.get("input_tokens"),
           completion_tokens=usage.get("output_tokens"),
           latency_s=time.perf_counter() - t0, finish_reason=finish,
           text=content if isinstance(content, str) else None, **extra)


def drain() -> list[dict]:
    """Return and clear every record so far (the harness drains per ticker)."""
    with _lock:
        out = list(_records)
        _records.clear()
    return out


def summarize(records: list[dict]) -> dict:
    """Per-site and overall totals. Token sums skip records without usage
    (counted in `*_tokens_unrecorded`) instead of guessing."""
    def agg(rows):
        lat = [r["latency_s"] for r in rows if r["latency_s"] is not None]
        out = {"calls": len(rows),
               "latency_s_total": round(sum(lat), 3),
               "latency_s_max": round(max(lat), 3) if lat else None}
        for k in ("prompt_tokens", "completion_tokens"):
            vals = [r[k] for r in rows if r[k] is not None]
            out[k] = sum(vals)
            out[k + "_unrecorded"] = len(rows) - len(vals)
        for flag in ("truncated", "repeat_run", "retry", "parse_failure", "format_failure"):
            out[flag] = sum(1 for r in rows if r[flag])
        out["errors"] = sum(1 for r in rows if r["error"])
        return out

    by_site = {}
    for r in records:
        by_site.setdefault(r["site"], []).append(r)
    return {
        "total": agg(records),
        "by_site": {s: agg(rows) for s, rows in sorted(by_site.items())},
        "endpoints": sorted({r["endpoint"] for r in records}),
    }


# ── Repetition-loop detection ───────────────────────────────────────────────
_WORD_RE = re.compile(r"\S+")


def repetition_run(text: str, min_n: int = 5, max_n: int = 60, min_repeats: int = 3) -> bool:
    """True when some run of `n` words (min_n <= n <= max_n) repeats back to
    back at least `min_repeats` times — the signature of a decoding loop.
    Prose and bullet lists repeat short phrases, not 5+-word spans three times
    in a row. Hitting the token cap is counted separately (finish_reason)."""
    w = _WORD_RE.findall(text)
    for n in range(min_n, min(max_n, len(w) // min_repeats) + 1):
        for i in range(len(w) - n * min_repeats + 1):
            first = w[i:i + n]
            if all(w[i + k * n:i + (k + 1) * n] == first for k in range(1, min_repeats)):
                return True
    return False
