#!/usr/bin/env python3
"""OpenAI-compatible model stub for the harness benchmark.

docs/harness-benchmark-plan.md: the model is removed as the bottleneck so
the benchmark measures the harness. The app reaches this server through its
existing self-served route (SLM_FULL=true, SLM_ENDPOINT=cpu, SLM_CPU_URL at
this Service); nothing in the app image changes.

Every /v1/chat/completions request is answered with the text the real model
wrote for that ticker and call site in a committed run (the corpus, built by
scripts/build_stub_corpus.py), after the delay the latency profile assigns
to that call's RECORDED prompt and completion token counts:

  L0  no delay                                       pure harness overhead
  L1  prompt/2299.5 + completion/110.4 seconds       the model on the A10
  L2  prompt/109.8  + completion/13.3  seconds       the model on 8 E5 vCPU

Recorded counts, not the live prompt's: the delay must not depend on how a
tokenizer the stub does not have would count live data, and the same brief
then costs the same model time in every cell. No capacity limit: each
request waits only its own delay in its own thread, so the harness, never
the stub, is what saturates.

Site detection (the app sends no site name): max_tokens picks the family
(768 section, 4096 synthesis, RAG_MAX_TOKENS rag), the prompt text picks the
member, "({TICKER})" in the prompt or the RAG chunks' "ticker: X" metadata
line picks the ticker. The
synthesis answer is rebuilt as the real model is told to write it: the
recorded Executive Summary and Outlook around the pre-written sections
copied verbatim from the prompt. An unknown ticker or site is answered with
generic text and counted (stats "unmatched"), never an error.

Endpoints: /v1/models, /props, /health, /stats (counters, in flight,
per-site counts, stock-block-empty count), POST /stats/reset, and
/v1/chat/completions. Bearer key from SLM_CPU_API_KEY when set. One JSON
line per request on stdout.

Stdlib only (runs on the app image or any python:3). Env: PROFILE (L0|L1|L2,
read per request from /stats/profile too), STUB_CORPUS, STUB_MODEL_NAME,
SLM_CPU_API_KEY, PORT.
"""
import json
import os
import re
import sys
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PROFILES = {
    "L0": (None, None),
    "L1": (2299.5, 110.4),
    "L2": (109.8, 13.3),
}
SECTION_SITES = {"Financial Health": "section:financial_health",
                 "Recent Developments": "section:recent_developments",
                 "SEC Filing Highlights": "section:sec_filing_highlights",
                 "Risk Factors": "section:risk_factors"}
DISCLAIMER = ("---\n*This brief is for informational purposes only and does not "
              "constitute financial advice.*")

_SECTION_RE = re.compile(r"Write ONLY the '#* *([^']+)' section for .*?\(([A-Z.\-]{1,8})\)")
_SYNTH_RE = re.compile(r"Complete this investment brief for (.*?) \(([A-Z.\-]{1,8})\)")
# query_sec_filing strips "TICKER:" from the question; the ticker reaches
# the answer prompt in each chunk's metadata header ("ticker: AAPL").
_RAG_QUERY_RE = re.compile(r"(Summarize the key takeaways|What are the primary risk factors)")
_RAG_TICKER_RE = re.compile(r"^ticker: ([A-Z][A-Z.\-]{0,7})\s*$", re.M)
_PREWRITTEN_RE = re.compile(r"Pre-written sections:\n(.*?)\n\nGROUNDING RULES", re.S)
_STOCK_RE = re.compile(r"^STOCK DATA:\n(.*?)\n\nNEWS ARTICLES:", re.S | re.M)


def delay_s(profile: str, prompt_tokens: int, completion_tokens: int) -> float:
    pp, tg = PROFILES[profile]
    if pp is None:
        return 0.0
    return prompt_tokens / pp + completion_tokens / tg


def prompt_text(body: dict) -> str:
    parts = []
    for m in body.get("messages") or []:
        c = m.get("content")
        if isinstance(c, list):
            c = "".join(p.get("text", "") for p in c if isinstance(p, dict))
        parts.append(c or "")
    return "\n".join(parts)


def classify(body: dict, text: str, rag_max_tokens: int = 2048) -> tuple[str, str | None]:
    """(site, ticker) for one request; site "unknown" when nothing matches."""
    mt = body.get("max_tokens")
    m = _SECTION_RE.search(text)
    if m and m.group(1).strip() in SECTION_SITES:
        return SECTION_SITES[m.group(1).strip()], m.group(2)
    m = _SYNTH_RE.search(text)
    if m:
        return "synthesis", m.group(2)
    m = _RAG_QUERY_RE.search(text)
    if m:
        site = "rag:highlights" if m.group(1).startswith("Summarize") else "rag:risks"
        t = _RAG_TICKER_RE.search(text)
        return site, (t.group(1) if t else None)
    if mt == rag_max_tokens:
        return "rag:unknown", None
    return "unknown", None


def stock_block_empty(text: str) -> bool | None:
    """eval/stock_block.py's rule on the Financial Health prompt's data."""
    m = _STOCK_RE.search(text.replace("\r\n", "\n"))
    if not m:
        return None
    try:
        return not json.loads(m.group(1))
    except ValueError:
        return None


def synthesis_text(rec: dict, text: str) -> str:
    m = _SYNTH_RE.search(text)
    company, ticker = (m.group(1), m.group(2)) if m else ("Company", "TICKER")
    pw = _PREWRITTEN_RE.search(text)
    sections = pw.group(1).strip() if pw else ""
    return (f"## {company} ({ticker}) — Investment Brief\n\n"
            f"### Executive Summary\n{rec['executive_summary']}\n\n{sections}\n\n"
            f"### Outlook\n{rec['outlook']}\n\n{DISCLAIMER}")


class Stub:
    def __init__(self, corpus: dict, model: str, key: str, profile: str):
        self.corpus = corpus.get("tickers", {})
        self.model, self.key = model, key
        self.profile = profile
        self.lock = threading.Lock()
        self.reset()
        # Generic fallback sizes: the corpus medians per site.
        self.fallback = {}
        for site in {s for t in self.corpus.values() for s in t}:
            recs = sorted((t[site] for t in self.corpus.values() if site in t),
                          key=lambda r: r["completion_tokens"] or 0)
            self.fallback[site] = recs[len(recs) // 2]

    def reset(self):
        with getattr(self, "lock", threading.Lock()):
            self.requests = 0
            self.in_flight = 0
            self.max_in_flight = 0
            self.by_site: dict = {}
            self.unmatched = 0
            self.stock_empty = 0
            self.stock_unknown = 0
            self.errors = 0
            self.prompt_tokens = 0
            self.completion_tokens = 0
            self.delay_total = 0.0
            self.since = time.time()

    def stats(self) -> dict:
        with self.lock:
            return {"profile": self.profile, "requests": self.requests,
                    "in_flight": self.in_flight, "max_in_flight": self.max_in_flight,
                    "by_site": dict(self.by_site), "unmatched": self.unmatched,
                    "stock_block_empty": self.stock_empty,
                    "stock_block_unknown": self.stock_unknown, "errors": self.errors,
                    "prompt_tokens": self.prompt_tokens,
                    "completion_tokens": self.completion_tokens,
                    "delay_s_total": round(self.delay_total, 3), "since": self.since,
                    "now": time.time()}

    def answer(self, body: dict) -> tuple[dict, dict]:
        text = prompt_text(body)
        site, ticker = classify(body, text)
        rec = (self.corpus.get(ticker) or {}).get(site)
        matched = rec is not None
        if rec is None:
            base = site if site in self.fallback else (
                "synthesis" if body.get("max_tokens", 0) >= 4096 else "section:financial_health")
            rec = self.fallback.get(base) or {"text": "No data.", "prompt_tokens": 0,
                                              "completion_tokens": 0}
            if site == "unknown":
                site = base
        if site == "synthesis":
            content = synthesis_text(rec["text"], text)
        elif isinstance(rec["text"], dict):
            content = json.dumps(rec["text"])
        else:
            content = rec["text"]
        pt, ct = int(rec["prompt_tokens"] or 0), int(rec["completion_tokens"] or 0)
        empty = stock_block_empty(text) if site == "section:financial_health" else False
        profile = self.profile
        d = delay_s(profile, pt, ct)
        with self.lock:
            self.requests += 1
            self.in_flight += 1
            self.max_in_flight = max(self.max_in_flight, self.in_flight)
            self.by_site[site] = self.by_site.get(site, 0) + 1
            self.unmatched += 0 if matched else 1
            self.stock_empty += 1 if empty is True else 0
            self.stock_unknown += 1 if empty is None else 0
            self.prompt_tokens += pt
            self.completion_tokens += ct
            self.delay_total += d
            in_flight = self.in_flight
        t0 = time.time()
        try:
            if d:
                time.sleep(d)
        finally:
            with self.lock:
                self.in_flight -= 1
        resp = {"id": f"chatcmpl-{uuid.uuid4().hex[:12]}", "object": "chat.completion",
                "created": int(t0), "model": self.model,
                "choices": [{"index": 0, "finish_reason": "stop",
                             "message": {"role": "assistant", "content": content}}],
                "usage": {"prompt_tokens": pt, "completion_tokens": ct,
                          "total_tokens": pt + ct}}
        log = {"t": round(t0, 3), "site": site, "ticker": ticker, "matched": matched,
               "profile": profile, "prompt_tokens": pt, "completion_tokens": ct,
               "delay_s": round(d, 3), "in_flight": in_flight,
               "stock_block_empty": empty}
        return resp, log


def make_handler(stub: Stub):
    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a):  # request lines go out as JSON instead
            pass

        def _send(self, code: int, obj: dict):
            data = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _authorized(self) -> bool:
            if not stub.key:
                return True
            if self.headers.get("Authorization", "") == f"Bearer {stub.key}":
                return True
            self._send(401, {"error": "invalid api key"})
            return False

        def _body(self) -> dict:
            n = int(self.headers.get("Content-Length") or 0)
            return json.loads(self.rfile.read(n) or b"{}")

        def do_GET(self):
            if self.path == "/health":
                return self._send(200, {"status": "ok"})
            if self.path == "/stats":
                return self._send(200, stub.stats())
            if not self._authorized():
                return
            if self.path == "/v1/models":
                return self._send(200, {"object": "list", "data": [
                    {"id": stub.model, "object": "model", "owned_by": "model-stub",
                     "meta": {"stub": True}}]})
            if self.path == "/props":
                return self._send(200, {"build_info": "model-stub",
                                        "model_path": "model-stub", "total_slots": 0,
                                        "default_generation_settings": {"n_ctx": 32768},
                                        "stub_profile": stub.profile})
            self._send(404, {"error": "not found"})

        def do_POST(self):
            if self.path == "/stats/reset":
                stub.reset()
                return self._send(200, stub.stats())
            if self.path == "/stats/profile":
                p = self._body().get("profile")
                if p not in PROFILES:
                    return self._send(400, {"error": f"profile must be one of {list(PROFILES)}"})
                stub.profile = p
                return self._send(200, {"profile": p})
            if not self._authorized():
                return
            if self.path != "/v1/chat/completions":
                return self._send(404, {"error": "not found"})
            try:
                resp, log = stub.answer(self._body())
            except Exception as e:  # counted, logged, answered 500
                with stub.lock:
                    stub.errors += 1
                print(json.dumps({"t": round(time.time(), 3), "error": repr(e)}), flush=True)
                return self._send(500, {"error": repr(e)})
            print(json.dumps(log), flush=True)
            self._send(200, resp)

    return H


def main() -> int:
    profile = os.getenv("PROFILE", "L0")
    if profile not in PROFILES:
        raise SystemExit(f"PROFILE must be one of {list(PROFILES)}, got {profile!r}")
    with open(os.getenv("STUB_CORPUS", "/stub/corpus.json"), encoding="utf-8") as f:
        corpus = json.load(f)
    stub = Stub(corpus, os.getenv("STUB_MODEL_NAME", "model-stub"),
                os.getenv("SLM_CPU_API_KEY", ""), profile)
    port = int(os.getenv("PORT", "8080"))
    srv = ThreadingHTTPServer(("0.0.0.0", port), make_handler(stub))
    srv.daemon_threads = True
    srv.request_queue_size = 256
    print(json.dumps({"listening": port, "profile": profile,
                      "tickers": len(stub.corpus), "source": corpus.get("source")}), flush=True)
    srv.serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
