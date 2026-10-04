#!/usr/bin/env python3
"""Print a one-step Workflow whose resolved template is larger than Argo's
inline limit, to prove the controller's template offload on a cluster.

Argo v3.7.18 passes each step's resolved template to the pod in the
ARGO_TEMPLATE env var; above common.MaxEnvVarLen = 131,072 bytes the
controller writes it to a ConfigMap (named after the pod, owned by the
Workflow) instead, which needs `create` on configmaps in the workflow's
namespace — argo/base/rbac.yaml grants it, the stock install does not. The
eval's aggregate step crosses the limit through its raw input artifact
(every ticker's result); this probe does the same with --bytes of filler,
and the pod prints how many bytes it received.

  python3 scripts/template_offload_probe.py --bytes 150000 | kubectl create -f -
  python3 scripts/template_offload_probe.py --bytes 100000 | kubectl create -f -   # stays inline

Without the Role the node ends in Error with "configmaps is forbidden";
with it the workflow succeeds, `kubectl -n financial-agent get configmap -l
workflows.argoproj.io/workflow=<wf>` shows the ConfigMap, and deleting the
workflow garbage-collects it. Stdlib only.
"""
import argparse
import json
import sys

LIMIT = 131072


def workflow(n_bytes, image, pull_policy, namespace):
    data = json.dumps({"filler": "x" * n_bytes})
    return {
        "apiVersion": "argoproj.io/v1alpha1", "kind": "Workflow",
        "metadata": {"generateName": "template-offload-probe-", "namespace": namespace},
        "spec": {
            "entrypoint": "probe", "serviceAccountName": "argo-workflow",
            "activeDeadlineSeconds": 300,
            "ttlStrategy": {"secondsAfterCompletion": 3600},
            "templates": [{
                "name": "probe",
                "inputs": {"artifacts": [{"name": "payload", "path": "/tmp/payload.json",
                                          "raw": {"data": data}}]},
                "container": {
                    "image": image, "imagePullPolicy": pull_policy,
                    "command": ["sh", "-c"],
                    "args": ["echo PROBE payload_bytes=$(wc -c < /tmp/payload.json)"],
                },
            }],
        },
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--bytes", type=int, default=150000,
                    help="filler size; the template is this plus about 400 bytes (limit %d)" % LIMIT)
    ap.add_argument("--image", default="financial-agent-app:local")
    ap.add_argument("--image-pull-policy", default="IfNotPresent")
    ap.add_argument("--namespace", default="financial-agent")
    args = ap.parse_args(argv)
    # JSON is YAML: kubectl create -f - takes it as is
    json.dump(workflow(args.bytes, args.image, args.image_pull_policy, args.namespace), sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
