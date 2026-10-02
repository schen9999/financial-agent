#!/usr/bin/env python3
"""Prove an SLM eval run's traffic reached the endpoint it names.

llama-server has no request counter (and logs no per-request lines), but its
token counters are exact: over any window, the server's
  delta(llamacpp:tokens_predicted_total)                         completion tokens
  delta(llamacpp:prompt_tokens_total + prompt_tokens_cached_total) prompt tokens
equal the sums of the `usage` it returned (verified against a live
llama-server b11347, 2026-10-02). The harness records that usage per call, and
the aggregate prints the per-endpoint sums on its SLM_TRAFFIC line. So:

  snapshot  before the run   (counters + build + model file)
  snapshot  after the run
  verify    deltas vs the aggregate's SLM_TRAFFIC line

Verdicts:
  EXACT        server deltas == harness sums, no errored calls
  LOWER-BOUND  server >= harness and every excess token is attributable to
               calls the harness saw fail (a timed-out request the server
               still finished); the run did reach the endpoint
  FAIL         server < harness (the harness counted traffic this endpoint
               never saw — wrong endpoint), excess without errored calls
               (other traffic in the window: not an isolated run), counters
               went backwards (server restarted), or the model file changed

Run snapshots where the eval pods run, with their env (SLM_<EP>_URL and
SLM_<EP>_API_KEY from app-config + the slm-endpoints Secret), e.g.
  kubectl -n financial-agent exec deploy/api -- python scripts/slm_traffic_proof.py snapshot --endpoint cpu
Stdlib only, no newer-than-3.6 syntax.
"""
import argparse
import json
import os
import re
import sys
import urllib.request

COUNTERS = ("prompt_tokens_total", "prompt_tokens_cached_total", "tokens_predicted_total",
            "n_decode_total")
_METRIC_RE = re.compile(r"^llamacpp:([a-z_]+)\s+([0-9.eE+-]+)\s*$")
_TRAFFIC_RE = re.compile(r"SLM_TRAFFIC (\{.*\})")


def parse_metrics(text):
    out = {}
    for line in text.splitlines():
        m = _METRIC_RE.match(line.strip())
        if m and m.group(1) in COUNTERS:
            out[m.group(1)] = float(m.group(2))
    missing = [c for c in COUNTERS if c not in out]
    if missing:
        raise SystemExit("slm_traffic_proof: /metrics lacks %s - is llama-server "
                         "running with --metrics?" % ", ".join(missing))
    return out


def _get(url, key):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def snapshot(endpoint):
    up = endpoint.upper()
    url = os.environ.get("SLM_%s_URL" % up, "").rstrip("/")
    key = os.environ.get("SLM_%s_API_KEY" % up, "")
    if not url or not key:
        raise SystemExit("slm_traffic_proof: SLM_%s_URL / SLM_%s_API_KEY not set" % (up, up))
    props = json.loads(_get(url + "/props", key))
    return {"endpoint": "slm-" + endpoint, "url": url,
            "build": props.get("build_info"), "model_path": props.get("model_path"),
            "counters": parse_metrics(_get(url + "/metrics", key))}


def parse_traffic(log_text, endpoint):
    for m in _TRAFFIC_RE.finditer(log_text):
        d = json.loads(m.group(1))
        if d.get("endpoint") == endpoint:
            return d
    raise SystemExit("slm_traffic_proof: no SLM_TRAFFIC line for %s in the aggregate log "
                     "- did this run route to it at all?" % endpoint)


def verify(before, after, traffic):
    """Return (verdict, lines)."""
    lines, problems = [], []
    if before["endpoint"] != after["endpoint"] or traffic["endpoint"] != after["endpoint"]:
        problems.append("endpoint mismatch: before %s, after %s, run %s"
                        % (before["endpoint"], after["endpoint"], traffic["endpoint"]))
    if (before["build"], before["model_path"]) != (after["build"], after["model_path"]):
        problems.append("server changed mid-run: %s %s -> %s %s"
                        % (before["build"], before["model_path"], after["build"], after["model_path"]))
    b, a = before["counters"], after["counters"]
    if any(a[c] < b[c] for c in COUNTERS):
        problems.append("counters went backwards: the server restarted mid-run")
    d_compl = a["tokens_predicted_total"] - b["tokens_predicted_total"]
    d_prompt = (a["prompt_tokens_total"] + a["prompt_tokens_cached_total"]
                - b["prompt_tokens_total"] - b["prompt_tokens_cached_total"])
    h_compl, h_prompt = traffic["completion_tokens"], traffic["prompt_tokens"]
    unaccounted = traffic.get("errored_calls", 0) + traffic.get("calls_without_usage", 0)
    lines.append("harness: %d calls, %d prompt + %d completion tokens (%d errored)"
                 % (traffic["calls"], h_prompt, h_compl, traffic.get("errored_calls", 0)))
    lines.append("server : %d prompt + %d completion tokens over the window (%s, %s)"
                 % (d_prompt, d_compl, after["build"], after["model_path"]))
    if not problems:
        if (d_compl, d_prompt) == (h_compl, h_prompt) and unaccounted == 0:
            return "EXACT", lines
        if d_compl < h_compl or d_prompt < h_prompt:
            problems.append("server saw FEWER tokens than the harness recorded - this "
                            "traffic did not go (only) to this endpoint")
        elif unaccounted:
            lines.append("excess %d prompt + %d completion tokens: from %d call(s) the "
                         "harness saw fail" % (d_prompt - h_prompt, d_compl - h_compl, unaccounted))
            return "LOWER-BOUND", lines
        else:
            problems.append("server saw MORE tokens than the run sent, with no failed "
                            "calls - other traffic hit the endpoint during the run")
    return "FAIL", lines + ["FAIL: " + p for p in problems]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("snapshot")
    s.add_argument("--endpoint", choices=("cpu", "gpu"), required=True)
    v = sub.add_parser("verify")
    v.add_argument("--before", required=True)
    v.add_argument("--after", required=True)
    v.add_argument("--log", required=True, help="aggregate step log (contains SLM_TRAFFIC)")
    args = ap.parse_args(argv)
    if args.cmd == "snapshot":
        print(json.dumps(snapshot(args.endpoint), sort_keys=True))
        return 0
    if args.cmd == "verify":
        with open(args.before) as f:
            before = json.load(f)
        with open(args.after) as f:
            after = json.load(f)
        with open(args.log) as f:
            traffic = parse_traffic(f.read(), after["endpoint"])
        verdict, lines = verify(before, after, traffic)
        for ln in lines:
            print("  " + ln)
        print("TRAFFIC PROOF: %s" % verdict)
        return 0 if verdict in ("EXACT", "LOWER-BOUND") else 1
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
