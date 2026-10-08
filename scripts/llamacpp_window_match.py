#!/usr/bin/env python3
"""Match a llama-server log window against the harness's LLM ledger, call
by call — the offline check behind a traffic-proof FAIL (host-only; reads
committed captures, touches nothing live).

Server side, per task, from llama-server's own log lines:
  prompt eval time = ... / P tokens     P = prompt tokens processed (cache hits excluded)
  eval time = ... / G tokens            G = generated tokens
  release ... n_tokens = R              R = tokens in the slot at release
Prompt tokens as the response reports them are R - G + 1 (the last
generated token is never fed back), so cached = (R - G + 1) - P.

Harness side: every EVAL_LLM_CALL line of the run's eval pods for the
endpoint (prompt_tokens, completion_tokens), aggregate pod excluded.

Pairing: the two multisets of (prompt, completion) are compared exactly;
then sums, per-task consistency, and the /metrics counter deltas from the
proof's before/after snapshots.

  python scripts/llamacpp_window_match.py --dir eval/runs/slm-proof-4kkgm \\
      --log eval/runs/raw/4kkgm.log --endpoint slm-cpu
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

TASK = r"task (\d+) \|"
PEVAL = re.compile(TASK + r"\s+prompt eval time =\s+[\d.]+ ms /\s+(\d+) tokens")
EVAL = re.compile(TASK + r"\s+eval time =\s+[\d.]+ ms /\s+(\d+) tokens")
RELEASE = re.compile(TASK + r" stop processing: n_tokens = (\d+)")
CALL = re.compile(r"^\[pod/([^/]+)/[^\]]+\] EVAL_LLM_CALL (\{.*\})\s*$")


def server_tasks(text: str) -> dict:
    t = {}
    for rx, k in ((PEVAL, "processed"), (EVAL, "generated"), (RELEASE, "release")):
        for m in rx.finditer(text):
            t.setdefault(int(m.group(1)), {})[k] = int(m.group(2))
    for v in t.values():
        if {"generated", "release"} <= v.keys():
            v["prompt"] = v["release"] - v["generated"] + 1
            v["cached"] = v["prompt"] - v.get("processed", v["prompt"])
    return t


def ledger_calls(text: str, endpoint: str) -> list[dict]:
    out = []
    for line in text.splitlines():
        m = CALL.match(line.strip())
        if m and "-aggregate-" not in m.group(1):
            c = json.loads(m.group(2))
            if c.get("endpoint") == endpoint:
                out.append(dict(c, pod=m.group(1)))
    return out


def match(tasks: dict, calls: list[dict], before: dict, after: dict) -> dict:
    s = Counter((v["prompt"], v["generated"]) for v in tasks.values() if "prompt" in v)
    h = Counter((c["prompt_tokens"], c["completion_tokens"]) for c in calls)
    d = {k: after["counters"][k] - before["counters"][k] for k in before["counters"]}
    return {
        "server_tasks": len(tasks),
        "complete_tasks": sum(1 for v in tasks.values() if "prompt" in v),
        "harness_calls": len(calls),
        "unmatched_server": sorted((s - h).elements()),
        "unmatched_harness": sorted((h - s).elements()),
        "server_prompt_sum": sum(v["prompt"] for v in tasks.values() if "prompt" in v),
        "server_processed_sum": sum(v.get("processed", 0) for v in tasks.values()),
        "server_cached_sum": sum(v.get("cached", 0) for v in tasks.values()),
        "server_generated_sum": sum(v.get("generated", 0) for v in tasks.values()),
        "harness_prompt_sum": sum(c["prompt_tokens"] for c in calls),
        "harness_completion_sum": sum(c["completion_tokens"] for c in calls),
        "tasks_with_cache_hits": {k: v["cached"] for k, v in tasks.items() if v.get("cached")},
        "counter_delta": d,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", type=Path, required=True, help="slm-proof-<run> folder")
    ap.add_argument("--log", type=Path, required=True, help="the run's full pod log")
    ap.add_argument("--endpoint", default="slm-cpu")
    args = ap.parse_args(argv)
    before = json.loads(next(args.dir.glob("*-before.json")).read_text(encoding="utf-8"))
    after = json.loads(next(args.dir.glob("*-after.json")).read_text(encoding="utf-8"))
    tasks = server_tasks((args.dir / "llamacpp-server-window.log").read_text(encoding="utf-8"))
    calls = ledger_calls(args.log.read_text(encoding="utf-8", errors="replace"), args.endpoint)
    print(json.dumps(match(tasks, calls, before, after), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
