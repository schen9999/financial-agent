#!/usr/bin/env python3
"""Traffic proof by per-request match (declared 2026-10-07, before any run
it judges): the run's LLM calls must match the llama.cpp server's own
per-request log, call by call. The /metrics counter is reported beside it
and does not decide.

Why: the process-wide `prompt_tokens_total` counter drifts by a few tokens
with nothing else on the endpoint. The 2026-10-07 capacity replay
(eval/runs/capacity-sweep-2026-10-07/) sent 352,522 prompt tokens three
times, the server's per-request timings summed to exactly that each time,
and the counter moved 1, 2 and 2 tokens less. The counter-based proof
(scripts/slm_traffic_proof.py, unchanged) failed 5bdz5 (+1), 4kkgm (-4) and
6z5xz (+8) on that drift; those runs stay not citable under the rule they
ran under and are not re-scored.

Inputs
  --server-log   the endpoint pod's llama-server log from the run's start
                 (`kubectl logs deploy/llamacpp --since-time=<workflow
                 creationTimestamp>`), captured right after the run: every
                 task in it counts, so any other traffic in the window, or
                 after the run before the capture, makes the proof fail
  --log          the workflow's pod log, every eval pod and every attempt
                 (EVAL_LLM_CALL lines; the aggregate pod's reprint excluded,
                 each (pod, seq) once)
  --endpoint     slm-cpu | slm-gpu
  --before/--after  the counter snapshots of `make slm-eval-run` (reported)

Per server task (llama-server's own lines): prompt tokens = release
n_tokens - generated + 1 (cached prefix included, as the API's usage
reports it), completion = generated.

Verdict
  TASK-EXACT  every task in the window is complete (prompt eval, eval and
              release lines), and the multiset of (prompt, completion) over
              the server's tasks equals the harness's over all its calls:
              nothing unmatched on either side
  FAIL        anything else, with the unmatched pairs listed

  python3 scripts/traffic_proof_tasks.py --server-log window.log --log <wf>.log \\
      --endpoint slm-gpu --before <wf>-before.json --after <wf>-after.json
Stdlib only, no newer-than-3.6 syntax.
"""
import argparse
import json
import re
import sys
from collections import Counter

TASK = r"task (\d+) \|"
PEVAL = re.compile(TASK + r"\s+prompt eval time =\s+[\d.]+ ms /\s+(\d+) tokens")
EVAL = re.compile(TASK + r"\s+eval time =\s+[\d.]+ ms /\s+(\d+) tokens")
RELEASE = re.compile(TASK + r" stop processing: n_tokens = (\d+)")
CALL = re.compile(r"^\[pod/([^/]+)/[^\]]+\] EVAL_LLM_CALL (\{.*\})\s*$")
METRICS = ("prompt_tokens_total", "prompt_tokens_cached_total", "tokens_predicted_total")


def server_tasks(text):
    t = {}
    for rx, k in ((PEVAL, "processed"), (EVAL, "generated"), (RELEASE, "release")):
        for m in rx.finditer(text):
            t.setdefault(int(m.group(1)), {})[k] = int(m.group(2))
    return t


def harness_calls(text, endpoint):
    calls = {}
    for line in text.splitlines():
        m = CALL.match(line.strip())
        if m and "-aggregate-" not in m.group(1):
            c = json.loads(m.group(2))
            if c.get("endpoint") == endpoint:
                calls[(m.group(1), c.get("seq"))] = c
    return list(calls.values())


def verdict(tasks, calls):
    incomplete = sorted(k for k, v in tasks.items() if not {"processed", "generated", "release"} <= set(v))
    server = Counter((v["release"] - v["generated"] + 1, v["generated"])
                     for k, v in tasks.items() if k not in incomplete)
    harness = Counter((c.get("prompt_tokens") or 0, c.get("completion_tokens") or 0) for c in calls)
    only_server = sorted((server - harness).elements())
    only_harness = sorted((harness - server).elements())
    ok = not incomplete and not only_server and not only_harness and len(tasks) > 0
    return {
        "verdict": "TASK-EXACT" if ok else "FAIL",
        "server_tasks": len(tasks), "incomplete_tasks": incomplete,
        "harness_calls": len(calls), "errored_calls": sum(1 for c in calls if c.get("error")),
        "unmatched_server": only_server, "unmatched_harness": only_harness,
        "prompt_tokens": sum(p for p, _ in harness.elements()),
        "completion_tokens": sum(g for _, g in harness.elements()),
        "server_cached_prefix_tokens": sum(v["release"] - v["generated"] + 1 - v["processed"]
                                           for k, v in tasks.items() if k not in incomplete),
    }


def counter_report(before, after, res):
    b, a = before["counters"], after["counters"]
    d = dict((k, a.get(k, 0) - b.get(k, 0)) for k in METRICS)
    prompt = d["prompt_tokens_total"] + d["prompt_tokens_cached_total"]
    return {"counter_prompt": prompt, "counter_completion": d["tokens_predicted_total"],
            "counter_minus_harness_prompt": prompt - res["prompt_tokens"],
            "counter_minus_harness_completion": d["tokens_predicted_total"] - res["completion_tokens"]}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--server-log", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--endpoint", required=True, choices=["slm-cpu", "slm-gpu"])
    ap.add_argument("--before")
    ap.add_argument("--after")
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    with open(args.server_log, encoding="utf-8", errors="replace") as f:
        tasks = server_tasks(f.read())
    with open(args.log, encoding="utf-8", errors="replace") as f:
        calls = harness_calls(f.read(), args.endpoint)
    res = verdict(tasks, calls)
    if args.before and args.after:
        with open(args.before) as f1, open(args.after) as f2:
            res["counter"] = counter_report(json.load(f1), json.load(f2), res)
    print("=== traffic proof by per-request match (%s) ===" % args.endpoint)
    print("  harness : %d calls (%d errored), %d prompt + %d completion tokens"
          % (res["harness_calls"], res["errored_calls"], res["prompt_tokens"], res["completion_tokens"]))
    print("  server  : %d tasks in the window, %d incomplete; cached prefix reused %d tokens"
          % (res["server_tasks"], len(res["incomplete_tasks"]), res["server_cached_prefix_tokens"]))
    print("  unmatched: server %d, harness %d" % (len(res["unmatched_server"]), len(res["unmatched_harness"])))
    for name in ("unmatched_server", "unmatched_harness"):
        for p in res[name][:10]:
            print("    %s (prompt, completion) = %s" % (name, p))
    if "counter" in res:
        c = res["counter"]
        print("  /metrics counter (reported, not deciding): prompt %+d, completion %+d vs the harness"
              % (c["counter_minus_harness_prompt"], c["counter_minus_harness_completion"]))
    print("TRAFFIC PROOF (per-request): %s" % res["verdict"])
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(res, f, indent=2, default=list)
    return 0 if res["verdict"] == "TASK-EXACT" else 1


if __name__ == "__main__":
    sys.exit(main())
