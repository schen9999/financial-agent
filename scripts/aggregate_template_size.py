#!/usr/bin/env python3
"""How big was the aggregate step's template in a finished eval run, against
Argo's inline limit?

Argo v3.7.18 hands a step its resolved template in the ARGO_TEMPLATE env
var, after clearing inputs.parameters and keeping inputs.artifacts
(workflow/controller/workflowpod.go). The eval's aggregate step therefore
carries every ticker's result once, in its raw input artifact. Above
common.MaxEnvVarLen = 131,072 bytes the controller offloads the template to
a ConfigMap, which needs `create` on configmaps in the workflow's namespace
(argo/base/rbac.yaml).

From a workflow object this prints the size of that template as Go's
json.Marshal writes it (quotes, backslashes and control characters escaped;
<, > and & as six bytes; the rest as UTF-8), the bytes per ticker, the
ticker count at which the limit is crossed, and the size at 40 tickers.

  python3 scripts/aggregate_template_size.py eval/runs/hm527-workflow.json \\
      eval/runs/slm-proof-8vpq6/grounding-eval-extended-slm-cpu-8vpq6-workflow.json

Host-side only, stdlib only.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from workflow_nodes import nodes  # noqa: E402

LIMIT = 131072  # common.MaxEnvVarLen, Argo v3.7.18
_BACKSLASH = chr(92)


def go_json_len(s):
    """len(json.Marshal(s)) in Go."""
    n = 2
    for ch in s:
        o = ord(ch)
        if ch == '"' or ch == _BACKSLASH or ch in "\n\r\t":
            n += 2
        elif o < 0x20 or ch in "<>&" or o in (0x2028, 0x2029):
            n += 6
        else:
            n += len(ch.encode("utf-8"))
    return n


def measure(workflow):
    """Size of the aggregate step's resolved template, or None if the
    workflow has no aggregate node with a raw input artifact."""
    agg = next((n for n in nodes(workflow).values()
                if n.get("templateName") == "aggregate"), None)
    arts = ((agg or {}).get("inputs") or {}).get("artifacts") or []
    raw = next((a["raw"]["data"] for a in arts if (a.get("raw") or {}).get("data")), None)
    if raw is None:
        return None
    stored = (workflow.get("status") or {}).get("storedWorkflowTemplateSpec") or {}
    tmpl = next((t for t in stored.get("templates", []) if t.get("name") == "aggregate"), {})
    shell = json.loads(json.dumps(tmpl))
    shell["inputs"] = {"artifacts": [dict(arts[0], raw={"data": ""})]}
    overhead = len(json.dumps(shell, separators=(",", ":")))
    data = go_json_len(raw)
    tickers = len(json.loads(raw))
    per = data / tickers
    return {"tickers": tickers, "results_bytes": data, "template_bytes": data + overhead,
            "bytes_per_ticker": per, "times_limit": (data + overhead) / LIMIT,
            "crosses_at": int((LIMIT - overhead) // per) + 1,
            "at_40": per * 40 + overhead, "phase": (agg or {}).get("phase")}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("workflows", nargs="+", help="kubectl get workflow -o json output(s)")
    args = ap.parse_args(argv)
    print("limit: %d bytes (Argo v3.7.18 common.MaxEnvVarLen)" % LIMIT)
    for path in args.workflows:
        with open(path, encoding="utf-8") as f:
            wf = json.load(f)
        m = measure(wf)
        name = (wf.get("metadata") or {}).get("name")
        if m is None:
            print("%s: no aggregate node with a raw input artifact" % name)
            continue
        print("%s: %d tickers, aggregate %s" % (name, m["tickers"], m["phase"]))
        print("  template %d bytes = %.2fx the limit -> %s" % (
            m["template_bytes"], m["times_limit"],
            "OFFLOADED to a ConfigMap" if m["template_bytes"] > LIMIT else "inline"))
        print("  %.0f bytes per ticker; the limit is crossed from %d tickers; at 40 tickers "
              "about %.0f bytes (%.2fx)" % (m["bytes_per_ticker"], m["crosses_at"], m["at_40"],
                                            m["at_40"] / LIMIT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
