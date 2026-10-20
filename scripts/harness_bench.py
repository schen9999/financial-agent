#!/usr/bin/env python3
"""Closed-loop driver for the harness benchmark (docs/harness-benchmark-plan.md).

Runs as a Job in the financial-agent namespace (scripts/harness_bench_cell.sh
creates it), on the app image, with app-config in its environment. One
invocation is one repeat of one cell:

  1. sets the stub's latency profile and resets its counters
  2. submits briefs through the API exactly as a user does
     (POST /research/async), cycling the 40 extended tickers, and keeps
     capacity x (1 + QUEUE_FACTOR) briefs outstanding (closed loop: QUEUE_FACTOR
     x capacity waiting in the Celery queue at all times)
  3. reads each task's state straight from the Celery result backend in
     Redis (one MGET per poll, so polling never loads the API pod under test)
  4. counts the first WARMUP completions as warm-up (at least one per
     worker process, so every prefork child has paid its first-task import),
     then measures the next BRIEFS completions while the loop stays full
  5. stops submitting, waits for every outstanding brief (so the next cell
     starts empty and the stub's counters cover every brief), and reads the
     stub's counters

Output on stdout: one "BENCH_BRIEF {json}" line per brief and one
"BENCH_SUMMARY {json}" line at the end; scripts/harness_bench_report.py reads
them from the captured Job log.

The brief cache is off for the run (BYPASS_CACHE=true on the worker, set by
make bench-stub-on), so every submission runs the whole pipeline.
"""
import argparse
import json
import os
import sys
import time

import redis
import requests

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "JPM", "V", "WMT",
           "XOM", "UNH", "UPST", "AFRM", "RIVN", "LCID", "SNAP", "PTON", "ROKU", "COIN",
           "CALM", "SFIX", "RDFN", "BYND", "CHGG", "BLNK", "OMER", "EVGO", "OCGN", "EDIT",
           "SANA", "CRBU", "VERV", "BEAM", "NTLA", "TSM", "NVO", "BABA", "TM", "SAP"]
DONE = ("SUCCESS", "FAILURE", "REVOKED")


def expected_calls(corpus: dict, ticker: str) -> int:
    """LLM calls the pipeline makes for one brief of `ticker`: one per site
    the recorded run answered (7, or 5 for a filer with no RAG call)."""
    return len((corpus.get("tickers") or {}).get(ticker) or {}) or 7


def emit(kind: str, obj: dict):
    print(f"{kind} {json.dumps(obj, sort_keys=True)}", flush=True)


class Driver:
    def __init__(self, a):
        self.a = a
        self.r = redis.Redis.from_url(os.environ["REDIS_URL"])
        self.http = requests.Session()
        self.jobs: dict = {}   # job_id -> record
        self.order = 0
        self.next_ticker = 0
        self.queue_samples = []

    def stub(self, method: str, path: str, **kw) -> dict:
        r = requests.request(method, f"{self.a.stub}{path}", timeout=30, **kw)
        r.raise_for_status()
        return r.json()

    def submit(self):
        t = TICKERS[self.next_ticker % len(TICKERS)]
        self.next_ticker += 1
        t0 = time.time()
        r = self.http.post(f"{self.a.api}/research/async", json={"ticker": t}, timeout=60)
        r.raise_for_status()
        jid = r.json()["job_id"]
        self.order += 1
        self.jobs[jid] = {"job_id": jid, "ticker": t, "n": self.order, "submit": t0,
                          "start": None, "finish": None, "state": "PENDING"}

    def poll(self):
        open_ids = [j for j, rec in self.jobs.items() if rec["finish"] is None]
        if not open_ids:
            return []
        now = time.time()
        vals = self.r.mget([f"celery-task-meta-{j}" for j in open_ids])
        finished = []
        for jid, raw in zip(open_ids, vals):
            if raw is None:
                continue
            meta = json.loads(raw)
            rec = self.jobs[jid]
            state = meta.get("status")
            if state != "PENDING" and rec["start"] is None:
                rec["start"] = now
            if state in DONE:
                rec["finish"] = now
                rec["state"] = state
                result = meta.get("result") if state == "SUCCESS" else None
                brief = (result or {}).get("brief") if isinstance(result, dict) else None
                rec["brief_ok"] = bool(brief and "### Executive Summary" in brief
                                       and "### Outlook" in brief)
                rec["brief_chars"] = len(brief or "")
                if state != "SUCCESS":
                    rec["error"] = str(meta.get("result"))[:300]
                finished.append(rec)
            else:
                rec["state"] = state
        return finished

    def outstanding(self) -> int:
        return sum(1 for rec in self.jobs.values() if rec["finish"] is None)

    def run(self) -> dict:
        a = self.a
        capacity = a.replicas * a.concurrency
        target = capacity * (1 + a.queue_factor)
        warmup = max(a.warmup, capacity)
        corpus = json.load(open(a.corpus)) if a.corpus else {}

        self.stub("POST", "/stats/profile", json={"profile": a.profile})
        self.stub("POST", "/stats/reset")
        stub_before = self.stub("GET", "/stats")
        t_begin = time.time()
        completed: list = []
        measure_start = None
        last_queue = 0.0
        while True:
            submitting = len(completed) < warmup + a.briefs
            while submitting and self.outstanding() < target:
                self.submit()
            for rec in self.poll():
                completed.append(rec)
                k = len(completed)
                rec["phase"] = ("warmup" if k <= warmup else
                                "measured" if k <= warmup + a.briefs else "tail")
                if k == warmup:
                    measure_start = rec["finish"]
                emit("BENCH_BRIEF", {**rec, "cell": a.cell, "repeat": a.repeat})
            now = time.time()
            if now - last_queue >= a.queue_every:
                self.queue_samples.append({"t": now, "llen": self.r.llen("celery")})
                last_queue = now
            if not submitting and self.outstanding() == 0:
                break
            if now - t_begin > a.max_seconds:
                emit("BENCH_ABORT", {"cell": a.cell, "reason": "max_seconds",
                                     "outstanding": self.outstanding()})
                break
            time.sleep(a.poll)
        t_end = time.time()
        stub_after = self.stub("GET", "/stats")

        measured = [r for r in completed if r.get("phase") == "measured"]
        expected = sum(expected_calls(corpus, r["ticker"]) for r in completed
                       if r["state"] == "SUCCESS")
        summary = {
            "cell": a.cell, "repeat": a.repeat, "profile": a.profile,
            "replicas": a.replicas, "concurrency": a.concurrency, "capacity": capacity,
            "outstanding_target": target, "warmup": warmup, "briefs": a.briefs,
            "t_begin": t_begin, "t_end": t_end, "measure_start": measure_start,
            "measure_end": measured[-1]["finish"] if measured else None,
            "completed": len(completed), "measured": len(measured),
            "errors": sum(1 for r in completed if r["state"] != "SUCCESS"),
            "bad_briefs": sum(1 for r in completed
                              if r["state"] == "SUCCESS" and not r.get("brief_ok")),
            "stub_before": stub_before, "stub_after": stub_after,
            "stub_requests_expected": expected, "queue_samples": self.queue_samples,
        }
        emit("BENCH_SUMMARY", summary)
        return summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--cell", required=True)
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--profile", choices=("L0", "L1", "L2"), required=True)
    ap.add_argument("--replicas", type=int, required=True)
    ap.add_argument("--concurrency", type=int, required=True)
    ap.add_argument("--briefs", type=int, default=40)
    ap.add_argument("--warmup", type=int, default=5)
    ap.add_argument("--queue-factor", type=int, default=3)
    ap.add_argument("--api", default="http://api.financial-agent.svc:8000")
    ap.add_argument("--stub", default="http://model-stub.financial-agent.svc:8080")
    ap.add_argument("--corpus", default="/bench/corpus.json")
    ap.add_argument("--poll", type=float, default=0.25)
    ap.add_argument("--queue-every", type=float, default=15.0)
    ap.add_argument("--max-seconds", type=float, default=4 * 3600)
    a = ap.parse_args(argv)
    s = Driver(a).run()
    return 0 if s["measured"] == a.briefs else 1


if __name__ == "__main__":
    sys.exit(main())
