#!/usr/bin/env python3
"""A10 capacity sweep: replay a recorded eval run's LLM calls, length-matched,
against the llama.cpp GPU endpoint at a fixed client concurrency P.

Why length-matched: the LLM ledger records each call's site and token counts,
not its prompt text, so the exact prompts cannot be replayed. Each replayed
request reproduces one recorded call's prompt length and completion length:

  prompt      token ids sent to /completion: a per-request marker
              ("[replay <level>-<n>]", distinct on every request, so no two
              requests share a prefix) followed by a slice of the run's own
              retrieved source contexts (eval/runs/<run>-contexts/), cut to
              the recorded prompt_tokens exactly
  completion  n_predict = the recorded completion_tokens, ignore_eos, so the
              server generates exactly that many tokens
  cache       cache_prompt false; tokens_cached and timings.prompt_n are
              recorded per request, and the level's prompt-cache counter
              delta is checked (a hit would make the level faster than the
              work it claims)

Counting is server-side: per request the response's own timings; per level
the /metrics counter deltas, which must equal the sums of the requests'
prompt and generated tokens (the traffic proof's arithmetic). One connection
per request (Connection: close), no keep-alive reuse.

Per level (P = 1, 2, 4 ...): P worker threads take the requests in order from
one queue (closed loop). Reported: wall time, requests and errors, output
and prompt tokens per second over the level, end-to-end latency p50/p95, and
the level's time window for the nvidia-smi capture (scripts/nvsmi_summary.py
--window).

Subcommands:
  plan  (laptop)   python scripts/capacity_replay.py plan --run nstp9 \\
                       --log eval/runs/slm-proof-nstp9/grounding-eval-extended-slm-gpu-nstp9.log \\
                       --out eval/runs/capacity-plan-nstp9.json
  run   (node 2)   python3 scripts/capacity_replay.py run --plan capacity-plan-nstp9.json \\
                       --url http://127.0.0.1:30880 --key-file ~/.llama-key --levels 1 2 4 \\
                       --out capacity-sweep
  summary          python scripts/capacity_replay.py summary --dir eval/runs/capacity-sweep-<date>

Stdlib only (node 2 runs it with the system python3).
"""
import argparse
import http.client
import json
import queue
import re
import sys
import threading
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

CALL = re.compile(r"^\[pod/([^/]+)/[^\]]+\] EVAL_LLM_CALL (\{.*\})\s*$")
METRICS = ("prompt_tokens_total", "tokens_predicted_total", "prompt_tokens_cached_total")


# ── plan ─────────────────────────────────────────────────────────────────────
def ledger_calls(log_text: str, endpoint: str) -> list[dict]:
    out = []
    for line in log_text.splitlines():
        m = CALL.match(line.strip())
        if m and "-aggregate-" not in m.group(1):
            c = json.loads(m.group(2))
            if c.get("endpoint") == endpoint and not c.get("error"):
                out.append({"pod": m.group(1), "seq": c["seq"], "site": c["site"],
                            "prompt_tokens": c["prompt_tokens"], "completion_tokens": c["completion_tokens"]})
    # the pod log can carry a line twice (a retried log stream); one per pod and seq
    uniq = {(c["pod"], c["seq"]): c for c in out}
    return [uniq[k] for k in sorted(uniq)]


def make_plan(run: str, log: Path, contexts: Path, endpoint: str) -> dict:
    calls = ledger_calls(log.read_text(encoding="utf-8", errors="replace"), endpoint)
    pool = "\n\n".join(p.read_text(encoding="utf-8") for p in sorted(contexts.glob("*.txt")))
    return {"run": run, "endpoint": endpoint, "calls": calls, "text_pool": pool}


# ── run ──────────────────────────────────────────────────────────────────────
class Endpoint:
    def __init__(self, url: str, key: str, timeout: float = 900.0):
        u = urllib.parse.urlparse(url)
        self.host, self.port, self.key, self.timeout = u.hostname, u.port or 80, key, timeout

    def call(self, method: str, path: str, body: dict | None = None) -> tuple[int, bytes]:
        conn = http.client.HTTPConnection(self.host, self.port, timeout=self.timeout)
        try:
            hdr = {"Authorization": f"Bearer {self.key}", "Connection": "close"}
            data = None
            if body is not None:
                data = json.dumps(body).encode()
                hdr["Content-Type"] = "application/json"
            conn.request(method, path, body=data, headers=hdr)
            r = conn.getresponse()
            return r.status, r.read()
        finally:
            conn.close()

    def tokenize(self, text: str) -> list[int]:
        st, b = self.call("POST", "/tokenize", {"content": text, "add_special": False})
        if st != 200:
            raise SystemExit(f"/tokenize returned {st}")
        return json.loads(b)["tokens"]

    def metrics(self) -> dict:
        st, b = self.call("GET", "/metrics")
        if st != 200:
            raise SystemExit(f"/metrics returned {st}")
        out = {}
        for line in b.decode().splitlines():
            m = re.match(r"^llamacpp:(\w+)\s+([0-9.eE+-]+)$", line)
            if m and m.group(1) in METRICS:
                out[m.group(1)] = float(m.group(2))
        return out


def build_prompt(pool: list[int], marker: list[int], n_tokens: int, offset: int) -> list[int]:
    need = n_tokens - len(marker)
    if need <= 0:
        return marker[:n_tokens]
    start = offset % max(1, len(pool) - need)
    body = pool[start:start + need]
    while len(body) < need:          # pool shorter than one prompt: wrap
        body += pool[:need - len(body)]
    return marker + body


def percentile(xs: list[float], q: float) -> float:
    s = sorted(xs)
    if not s:
        return float("nan")
    k = (len(s) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def run_level(ep: Endpoint, plan: dict, pool: list[int], p: int, out: Path) -> dict:
    calls = plan["calls"]
    q: "queue.Queue[tuple[int, dict]]" = queue.Queue()
    for i, c in enumerate(calls):
        q.put((i, c))
    rows, lock = [], threading.Lock()

    def worker():
        while True:
            try:
                i, c = q.get_nowait()
            except queue.Empty:
                return
            marker = ep.tokenize(f"[replay P{p}-{i}] ")
            prompt = build_prompt(pool, marker, c["prompt_tokens"], offset=i * 7919 + p * 104729)
            body = {"prompt": prompt, "n_predict": c["completion_tokens"], "ignore_eos": True,
                    "cache_prompt": False, "temperature": 0.0, "stream": False}
            t0 = time.time()
            try:
                st, b = ep.call("POST", "/completion", body)
                err = None if st == 200 else f"HTTP {st}"
                r = json.loads(b) if st == 200 else {}
            except Exception as e:  # noqa: BLE001 - recorded, not raised
                st, err, r = 0, f"{type(e).__name__}: {e}", {}
            t1 = time.time()
            tm = r.get("timings", {})
            row = {"i": i, "site": c["site"], "target_prompt": c["prompt_tokens"],
                   "target_completion": c["completion_tokens"], "sent_prompt": len(prompt),
                   "start": t0, "end": t1, "latency_s": t1 - t0, "status": st, "error": err,
                   "prompt_n": tm.get("prompt_n"), "predicted_n": tm.get("predicted_n"),
                   "prompt_ms": tm.get("prompt_ms"), "predicted_ms": tm.get("predicted_ms"),
                   "tokens_cached": r.get("tokens_cached")}
            with lock:
                rows.append(row)

    before = ep.metrics()
    t_start = datetime.now(timezone.utc)
    w0 = time.time()
    threads = [threading.Thread(target=worker) for _ in range(p)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    wall = time.time() - w0
    t_end = datetime.now(timezone.utc)
    after = ep.metrics()
    rows.sort(key=lambda r: r["i"])
    with open(out / f"P{p}-requests.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    ok = [r for r in rows if not r["error"]]
    delta = {k: after.get(k, 0) - before.get(k, 0) for k in METRICS}
    sum_prompt = sum((r["prompt_n"] or 0) + (r["tokens_cached"] or 0) for r in ok)
    sum_gen = sum(r["predicted_n"] or 0 for r in ok)
    lat = [r["latency_s"] for r in ok]
    return {
        "P": p, "requests": len(rows), "errors": len(rows) - len(ok),
        "window_utc": [t_start.strftime("%H:%M:%S"), t_end.strftime("%H:%M:%S")],
        "date_utc": t_start.strftime("%Y-%m-%d"), "wall_s": wall,
        "requests_per_min": len(ok) / wall * 60,
        "output_tok_per_s": sum_gen / wall, "prompt_tok_per_s": sum_prompt / wall,
        "latency_p50_s": percentile(lat, 0.5), "latency_p95_s": percentile(lat, 0.95),
        "length_mismatches": sum(1 for r in ok if r["sent_prompt"] != r["target_prompt"]
                                 or r["predicted_n"] != r["target_completion"]),
        "requests_with_cache_hits": sum(1 for r in ok if (r["tokens_cached"] or 0) > 0),
        "server_counter_delta": delta,
        "server_matches_requests": (delta["prompt_tokens_total"] + delta["prompt_tokens_cached_total"] == sum_prompt
                                    and delta["tokens_predicted_total"] == sum_gen),
        "sum_prompt": sum_prompt, "sum_generated": sum_gen,
    }


def cmd_run(args) -> int:
    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    key = Path(args.key_file).expanduser().read_text().strip()
    ep = Endpoint(args.url, key)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    pool = ep.tokenize(plan["text_pool"])
    print(f"plan: {len(plan['calls'])} calls from {plan['run']}; text pool {len(pool)} tokens", flush=True)
    summary = {"run": plan["run"], "url_host": urllib.parse.urlparse(args.url).hostname,
               "calls": len(plan["calls"]), "levels": []}
    for p in args.levels:
        print(f"level P={p} start {datetime.now(timezone.utc):%H:%M:%S}Z", flush=True)
        lv = run_level(ep, plan, pool, p, out)
        summary["levels"].append(lv)
        print(json.dumps(lv), flush=True)
        (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        if args.pause:
            time.sleep(args.pause)
    return 0


# ── summary ──────────────────────────────────────────────────────────────────
def table(summary: dict) -> str:
    L = ["| P | Requests (errors) | Wall | Requests/min | Output tok/s | Prompt tok/s | Latency p50 / p95 | Cache hits | Server = requests |",
         "|---|---|---|---|---|---|---|---|---|"]
    for lv in summary["levels"]:
        L.append(f"| {lv['P']} | {lv['requests']} ({lv['errors']}) | {lv['wall_s'] / 60:.1f} min | "
                 f"{lv['requests_per_min']:.1f} | {lv['output_tok_per_s']:.1f} | {lv['prompt_tok_per_s']:.1f} | "
                 f"{lv['latency_p50_s']:.1f} s / {lv['latency_p95_s']:.1f} s | {lv['requests_with_cache_hits']} | "
                 f"{'yes' if lv['server_matches_requests'] else 'NO'} |")
    return "\n".join(L)


def cmd_summary(args) -> int:
    s = json.loads((Path(args.dir) / "summary.json").read_text(encoding="utf-8"))
    sys.stdout.reconfigure(encoding="utf-8")
    print(table(s))
    for lv in s["levels"]:
        print(f"P={lv['P']}: window {lv['date_utc']} {lv['window_utc'][0]}-{lv['window_utc'][1]} UTC; "
              f"length mismatches {lv['length_mismatches']}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("plan")
    a.add_argument("--run", required=True)
    a.add_argument("--log", type=Path, required=True)
    a.add_argument("--contexts", type=Path)
    a.add_argument("--endpoint", default="slm-gpu")
    a.add_argument("--out", type=Path, required=True)
    b = sub.add_parser("run")
    b.add_argument("--plan", required=True)
    b.add_argument("--url", required=True)
    b.add_argument("--key-file", required=True)
    b.add_argument("--levels", type=int, nargs="+", default=[1, 2, 4])
    b.add_argument("--out", required=True)
    b.add_argument("--pause", type=float, default=30.0, help="idle seconds between levels")
    c = sub.add_parser("summary")
    c.add_argument("--dir", required=True)
    args = ap.parse_args(argv)
    if args.cmd == "plan":
        ctx = args.contexts or args.log.parents[1] / f"{args.run}-contexts"
        plan = make_plan(args.run, args.log, ctx, args.endpoint)
        args.out.write_text(json.dumps(plan) + "\n", encoding="utf-8")
        print(f"{len(plan['calls'])} calls, text pool {len(plan['text_pool'])} chars -> {args.out}")
        return 0
    return cmd_run(args) if args.cmd == "run" else cmd_summary(args)


if __name__ == "__main__":
    sys.exit(main())
