#!/usr/bin/env python3
"""Every attempt of an eval run, not just the last one per ticker.

The workflow retries a failed eval pod once (argo/base/eval-workflow.yaml).
The aggregate step only receives the final attempt's result, so a failed
attempt — its cause, the LLM calls it made, any truncation / parse / format
failure in them — used to be invisible, and the SLM traffic proof could not
reconcile the tokens it had sent (smoke 9jddz, 2026-10-03: one NVDA attempt
ran its whole SLM generation, died on an exhausted Anthropic balance at the
judge, was retried, and the server showed one brief more than the harness).

This module reads failed attempts back from what survives them:

  the workflow object   which eval pods failed, for which ticker, and Argo's
                        own message (exit code, OOMKilled, deadline)
  each pod's log        what the harness printed: EVAL_ATTEMPT_BEGIN / _END
                        (grounding_check.py) and one EVAL_LLM_CALL line per
                        LLM call (agent/llm_ledger.py), written as the call
                        returns — so a killed pod still shows its calls

A failed attempt's record is one of:
  complete     BEGIN and END present: every call it made is listed
  no END       the pod was killed (deadline, OOM): listed calls are a lower
               bound — a call in flight at the kill is not in the log
  none         no BEGIN: the image predates attempt logging, or the log is gone

  kubectl -n financial-agent get workflow <wf> -o json > wf.json
  kubectl -n financial-agent logs -l workflows.argoproj.io/workflow=<wf> --prefix --tail=-1 > pods.log
  python3 eval/attempts.py --workflow wf.json --log pods.log

Stdlib only: it runs on the operator host (make eval-run) and inside
scripts/slm_traffic_proof.py.
"""
import argparse
import json
import os
import re
import sys

BEGIN_PREFIX = "EVAL_ATTEMPT_BEGIN "
END_PREFIX = "EVAL_ATTEMPT_END "
CALL_PREFIX = "EVAL_LLM_CALL "
FLAG_PREFIX = "EVAL_LLM_FLAG "
EVAL_TEMPLATE = "eval-one"
FLAGS = ("truncated", "repeat_run", "retry", "parse_failure", "format_failure")

_POD_LINE = re.compile(r"^\[pod/([^/\]]+)/[^\]]*\] ?(.*)$")
_ATTEMPT_SUFFIX = re.compile(r"\((\d+)\)$")


# ── written by the harness, inside the eval pod ─────────────────────────────

def attempt_number():
    """Argo's {{retries}} for this pod (0 = first attempt), set by the
    workflow template as EVAL_ATTEMPT; 0 outside Argo."""
    try:
        return int(os.environ.get("EVAL_ATTEMPT", "0"))
    except ValueError:
        return 0


def write_line(prefix, **fields):
    rec = dict(fields, attempt=attempt_number(),
               pod=os.environ.get("EVAL_POD") or os.environ.get("HOSTNAME"))
    print(prefix + json.dumps(rec, sort_keys=True), flush=True)


def run_recorded(fn, calls_emitted=lambda: None):
    """Run the harness's main(); whichever way it ends, write the END record
    first. `calls_emitted` returns how many EVAL_LLM_CALL lines were written,
    so a reader can tell a complete log from one with lines missing."""
    try:
        fn()
    except SystemExit as e:
        if e.code in (None, 0):
            write_line(END_PREFIX, outcome="ok", calls=calls_emitted())
        else:
            cause = ((str(e.code).strip().splitlines() or ["exit"])[0]
                     if isinstance(e.code, str) else "exit code %s" % e.code)
            write_line(END_PREFIX, outcome="failed", kind="fatal", cause=cause[:300],
                       calls=calls_emitted())
        raise
    except BaseException as e:
        write_line(END_PREFIX, outcome="failed", kind="crash",
                   cause=("%s: %s" % (type(e).__name__, e))[:300], calls=calls_emitted())
        raise
    write_line(END_PREFIX, outcome="ok", calls=calls_emitted())


# ── read back, from the workflow object and the pod logs ────────────────────

def split_pod_logs(text):
    """{pod name: its log} from a `kubectl logs -l ... --prefix` capture."""
    pods = {}
    for line in text.splitlines():
        m = _POD_LINE.match(line)
        if m:
            pods.setdefault(m.group(1), []).append(m.group(2))
    return {pod: "\n".join(lines) for pod, lines in pods.items()}


def _json_after(line, prefix):
    try:
        return json.loads(line[len(prefix):])
    except ValueError:
        return None


def parse_pod_log(text):
    """What one eval pod's harness reported about its own attempt."""
    begin = end = fatal = None
    calls = {}
    order = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith(CALL_PREFIX):
            rec = _json_after(line, CALL_PREFIX)
            if rec is not None:
                key = rec.get("seq", len(order))
                calls[key] = rec
                order.append(key)
        elif line.startswith(FLAG_PREFIX):
            upd = _json_after(line, FLAG_PREFIX)
            if upd and upd.get("seq") in calls:
                calls[upd["seq"]].update({k: v for k, v in upd.items() if k != "seq"})
        elif line.startswith(BEGIN_PREFIX):
            begin = _json_after(line, BEGIN_PREFIX)
        elif line.startswith(END_PREFIX):
            end = _json_after(line, END_PREFIX)
        elif fatal is None and line.startswith("FATAL:"):
            fatal = line
    return {"begin": begin, "end": end, "fatal": fatal, "calls": [calls[k] for k in order]}


def summarize_calls(calls):
    """Per-site and per-endpoint sums in the shape of the aggregate's table."""
    def agg(rows):
        out = {"calls": len(rows),
               "prompt_tokens": sum(r.get("prompt_tokens") or 0 for r in rows),
               "completion_tokens": sum(r.get("completion_tokens") or 0 for r in rows),
               "tokens_unrecorded": sum(1 for r in rows if r.get("prompt_tokens") is None
                                        or r.get("completion_tokens") is None),
               "errors": sum(1 for r in rows if r.get("error"))}
        for f in FLAGS:
            out[f] = sum(1 for r in rows if r.get(f))
        return out
    by_site, by_endpoint = {}, {}
    for r in calls:
        by_site.setdefault(r.get("site", "?"), []).append(r)
        by_endpoint.setdefault(r.get("endpoint", "?"), []).append(r)
    return {"by_site": {s: agg(v) for s, v in sorted(by_site.items())},
            "by_endpoint": {e: agg(v) for e, v in sorted(by_endpoint.items())}}


def _ticker(node):
    for p in (node.get("inputs") or {}).get("parameters") or []:
        if p.get("name") == "ticker":
            return p.get("value")
    return None


def eval_pod_nodes(workflow):
    """The workflow's eval-one Pod nodes: ticker, attempt number, phase."""
    out = []
    for node in ((workflow.get("status") or {}).get("nodes") or {}).values():
        if node.get("type") != "Pod" or node.get("templateName") != EVAL_TEMPLATE:
            continue
        m = _ATTEMPT_SUFFIX.search(node.get("displayName") or "")
        out.append({"ticker": _ticker(node), "attempt": int(m.group(1)) if m else 0,
                    "node": node.get("displayName"), "id_suffix": node["id"].rsplit("-", 1)[-1],
                    "phase": node.get("phase"), "message": node.get("message"),
                    "started": node.get("startedAt"), "finished": node.get("finishedAt")})
    return sorted(out, key=lambda n: (n["ticker"] or "", n["attempt"]))


def _pod_for(node, pod_logs):
    for pod in pod_logs:
        if pod.endswith("-" + node["id_suffix"]):
            return pod
    return None


def build_report(workflow, pod_logs):
    """Retries and failed attempts of one run. `pod_logs` is {pod: log}."""
    nodes = eval_pod_nodes(workflow)
    tickers = sorted({n["ticker"] for n in nodes if n["ticker"]})
    failed = []
    for n in nodes:
        if n["phase"] == "Succeeded":
            continue
        pod = _pod_for(n, pod_logs)
        parsed = parse_pod_log(pod_logs[pod]) if pod else {"begin": None, "end": None,
                                                           "fatal": None, "calls": []}
        end_calls = (parsed["end"] or {}).get("calls")
        if parsed["begin"] and parsed["end"] and end_calls in (None, len(parsed["calls"])):
            record = "complete"
        elif parsed["begin"]:
            record = "no END"
        else:
            record = "none"
        end = parsed["end"] or {}
        cause = (end.get("cause") or parsed["fatal"]
                 or ("no cause in the pod log" if pod else "pod log not captured"))
        failed.append({**n, "pod": pod, "record": record, "cause": cause,
                       "kind": end.get("kind"), "calls": parsed["calls"],
                       **summarize_calls(parsed["calls"])})
    retried = sorted({n["ticker"] for n in nodes if n["attempt"] > 0 and n["ticker"]})
    by_endpoint = {}
    for a in failed:
        for ep, s in a["by_endpoint"].items():
            t = by_endpoint.setdefault(ep, {k: 0 for k in s})
            for k, v in s.items():
                t[k] += v
    return {"workflow": (workflow.get("metadata") or {}).get("name"),
            "phase": (workflow.get("status") or {}).get("phase"),
            "tickers": len(tickers), "eval_pods": len(nodes),
            "retries": sum(1 for n in nodes if n["attempt"] > 0), "retried_tickers": retried,
            "failed_attempts": failed, "failed_by_endpoint": by_endpoint,
            "unrecorded": [a for a in failed if a["record"] != "complete"]}


def format_report(rep):
    lines = ["attempts of %s (%s): %d eval pod(s) for %d ticker(s)"
             % (rep["workflow"], rep["phase"], rep["eval_pods"], rep["tickers"])]
    lines.append("  Argo retries      : %d%s" % (rep["retries"],
                 " (%s)" % ", ".join(rep["retried_tickers"]) if rep["retried_tickers"] else ""))
    failed = rep["failed_attempts"]
    lines.append("  failed attempts   : %d%s" % (
        len(failed), "" if failed or rep["retries"]
        else " - every eval pod succeeded on its first attempt"))
    for a in failed:
        lines.append("  FAILED ATTEMPT %s  pod %s" % (a["node"], a["pod"] or "(log not captured)"))
        lines.append("    argo            : %s - %s" % (a["phase"], a["message"] or "no message"))
        lines.append("    cause (pod log) : %s" % a["cause"])
        if a["record"] == "complete":
            lines.append("    call record     : complete - every LLM call of this attempt is listed")
        elif a["record"] == "no END":
            lines.append("    call record     : INCOMPLETE (no END record or calls missing - pod "
                         "killed?) - listed calls are a lower bound; a call in flight at the "
                         "kill is not in the log")
        else:
            lines.append("    call record     : NONE - the pod log has no attempt record (image "
                         "predates attempt logging, or the log is gone); its LLM calls and "
                         "tokens are UNRECORDED")
        if a["by_site"]:
            lines.append("    LLM calls FROM THIS FAILED ATTEMPT (not in the aggregate's table):")
            lines.append("    %-28s %5s %8s %7s %5s %4s %5s %3s %5s %3s" % (
                "Site", "Calls", "Prompt", "Compl", "Trunc", "Loop", "Parse", "Fmt", "Retry", "Err"))
            for site, s in a["by_site"].items():
                lines.append("    %-28s %5d %8d %7d %5d %4d %5d %3d %5d %3d" % (
                    site, s["calls"], s["prompt_tokens"], s["completion_tokens"], s["truncated"],
                    s["repeat_run"], s["parse_failure"], s["format_failure"], s["retry"],
                    s["errors"]))
    for ep, s in sorted(rep["failed_by_endpoint"].items()):
        lines.append("  FAILED_ATTEMPT_TRAFFIC " + json.dumps(dict(s, endpoint=ep,
                     attempts=len(failed), attempts_without_complete_record=len(rep["unrecorded"])),
                     sort_keys=True))
    if failed:
        tot = {f: sum(s[f] for a in failed for s in a["by_site"].values())
               for f in FLAGS + ("errors",)}
        lines.append("  failure counts FROM FAILED ATTEMPTS: Trunc %d, Loop %d, Parse %d, Fmt %d, "
                     "Retry %d, Err %d%s" % (
                         tot["truncated"], tot["repeat_run"], tot["parse_failure"],
                         tot["format_failure"], tot["retry"], tot["errors"],
                         "  (INCOMPLETE: %d attempt(s) without a complete call record)"
                         % len(rep["unrecorded"]) if rep["unrecorded"] else ""))
    return lines


def load(workflow_path, log_path):
    with open(workflow_path, encoding="utf-8") as f:
        workflow = json.load(f)
    with open(log_path, encoding="utf-8", errors="replace") as f:
        return build_report(workflow, split_pod_logs(f.read()))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--workflow", required=True, help="kubectl get workflow -o json output")
    ap.add_argument("--log", required=True,
                    help="every pod's log: kubectl logs -l workflows.argoproj.io/workflow=<wf> "
                         "--prefix --tail=-1")
    ap.add_argument("--json-out", default=None, metavar="PATH",
                    help="also write the report as JSON (the run's attempts record, "
                         "captured with its other artifacts)")
    args = ap.parse_args(argv)
    report = load(args.workflow, args.log)
    for line in format_report(report):
        print(line)
    if args.json_out:
        with open(os.path.expanduser(args.json_out), "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, indent=1, sort_keys=True)
            f.write("\n")
        print("  attempts record written: %s" % args.json_out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
