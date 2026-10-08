#!/usr/bin/env python3
"""A workflow object's node status, wherever Argo put it.

`kubectl get workflow <wf> -o json` carries the per-node status in one of
three places:

  status.nodes            the plain map (small workflows)
  status.compressedNodes  the same map, gzip-compressed and base64-encoded,
                          once the object nears the 1 MB etcd limit — the
                          40-ticker runs (9jzmj, 2026-10-04: status of 116 KB,
                          no `nodes` key)
  nowhere                 status.offloadNodeStatusVersion is set: the nodes
                          live in Argo's persistence database and are not in
                          the object at all

Readers that only look at status.nodes see a compressed workflow as having
no pods. nodes() returns the map from either of the first two and stops,
saying so, on the third — it never reports an empty workflow for one whose
nodes are merely elsewhere. `expand` rewrites an object with status.nodes
filled in, for readers that are not changed to call this (eval/attempts.py
runs inside the eval pods and is left as built into the pinned image; the
Makefile expands the object before handing it over).

  kubectl -n financial-agent get workflow <wf> -o json | python3 scripts/workflow_nodes.py expand > wf.json

`results` prints the eval pods' stored output parameters — the exact rows
the aggregate step receives — as the aggregate's --input, so the aggregate
can be run offline on a workflow whose own aggregate step never started
(9jzmj), estimated cost included:

  python3 scripts/workflow_nodes.py results eval/runs/9jzmj-workflow.json > rows.json
  python3 scripts/eval_aggregate.py --input rows.json

Host-side only, stdlib only.
"""
import base64
import gzip
import json
import sys


class NodesOffloaded(SystemExit):
    """The node status is in Argo's database, not in the object."""


def nodes(workflow):
    """{node id: node} of a workflow object, decompressing if needed."""
    status = workflow.get("status") or {}
    if status.get("nodes"):
        return status["nodes"]
    packed = status.get("compressedNodes")
    if packed:
        return json.loads(gzip.decompress(base64.b64decode(packed)).decode("utf-8"))
    version = status.get("offloadNodeStatusVersion")
    if version:
        raise NodesOffloaded(
            "workflow %s: node status is OFFLOADED to Argo's persistence database (version %s) "
            "and is not in this object. This is not an empty workflow. Fetch it through the "
            "Argo server instead (argo get <wf> -o json), which rehydrates the nodes."
            % ((workflow.get("metadata") or {}).get("name"), version))
    return {}


def expand(workflow):
    """The same object with status.nodes populated and compressedNodes dropped."""
    out = dict(workflow)
    status = dict(out.get("status") or {})
    status["nodes"] = nodes(workflow)
    status.pop("compressedNodes", None)
    out["status"] = status
    return out


def eval_results(workflow, template="eval-one", parameter="result"):
    """The succeeded eval pods' stored result payloads, in ticker order —
    what `{{tasks.eval-ticker.outputs.parameters.result}}` hands the
    aggregate. Failed attempts' pods carry no usable result and are skipped."""
    out = []
    for node in nodes(workflow).values():
        if node.get("type") != "Pod" or node.get("templateName") != template \
                or node.get("phase") != "Succeeded":
            continue
        for p in (node.get("outputs") or {}).get("parameters") or []:
            if p.get("name") == parameter and p.get("value"):
                out.append(json.loads(p["value"]))
    return sorted(out, key=lambda v: [r.get("ticker") for r in v.get("results", [])]
                  + list(v.get("skipped", [])))


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0] not in ("expand", "results") or len(argv) > 2:
        print(__doc__.split("\n\n")[0] + "\n\nusage: workflow_nodes.py expand|results "
              "[workflow.json] (default: stdin)", file=sys.stderr)
        return 2
    if len(argv) == 2:
        with open(argv[1], encoding="utf-8") as f:
            workflow = json.load(f)
    else:
        workflow = json.load(sys.stdin)
    if argv[0] == "results":
        rows = eval_results(workflow)
        json.dump(rows, sys.stdout)
        sys.stdout.write("\n")
        print("workflow_nodes: %d eval result payload(s)" % len(rows), file=sys.stderr)
        return 0
    was_compressed = bool((workflow.get("status") or {}).get("compressedNodes")
                          and not (workflow.get("status") or {}).get("nodes"))
    out = expand(workflow)
    json.dump(out, sys.stdout)
    sys.stdout.write("\n")
    print("workflow_nodes: %d node(s)%s" % (len(out["status"]["nodes"]),
          " (read from status.compressedNodes)" if was_compressed else ""), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
