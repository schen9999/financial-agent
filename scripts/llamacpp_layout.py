#!/usr/bin/env python3
"""Set the GPU endpoint's MoE layout in the rendered k3s-gpu llama.cpp overlay.

Reads `kubectl kustomize k8s/llamacpp/overlays/k3s-gpu` on stdin and writes
it back with --n-cpu-moe set to N. N > 0 keeps the first N layers' MoE
expert weights in host RAM (hybrid GPU+CPU), and then the served alias
becomes <alias>-hybrid-ncmoe<N> in the same edit, so the eval (which checks
the alias on /v1/models) can never report a hybrid run as a GPU run. N = 0
(all layers on the GPU) leaves the render byte-identical.

Each value must occur exactly once; anything else means the overlay drifted
and the script exits non-zero rather than apply a half-edited deployment.
Stdlib only: it runs on the VM host.

  kubectl kustomize k8s/llamacpp/overlays/k3s-gpu | python3 scripts/llamacpp_layout.py --ncmoe 4
"""
import argparse
import re
import sys

ALIAS = "qwen3.6-35b-a3b-q4km"


def _one(text, pattern, repl, what):
    rx = re.compile(pattern, re.M)
    hits = len(rx.findall(text))
    if hits != 1:
        raise SystemExit("llamacpp_layout: expected exactly 1 %s in the render, found %d "
                         "- overlay drifted" % (what, hits))
    return rx.sub(repl, text)


def served_alias(ncmoe):
    return ALIAS if ncmoe == 0 else "%s-hybrid-ncmoe%d" % (ALIAS, ncmoe)


def apply(render, ncmoe):
    if ncmoe < 0:
        raise SystemExit("llamacpp_layout: --ncmoe must be >= 0")
    out = _one(render, r'^(\s*- --n-cpu-moe\n\s*- )"0"$', lambda m: '%s"%d"' % (m.group(1), ncmoe),
               "--n-cpu-moe \"0\"")
    out = _one(out, r"^(\s*- --alias\n\s*- )" + re.escape(ALIAS) + r"$",
               lambda m: m.group(1) + served_alias(ncmoe), "--alias " + ALIAS)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--ncmoe", type=int, default=0)
    args = ap.parse_args(argv)
    sys.stdout.write(apply(sys.stdin.read(), args.ncmoe))
    return 0


if __name__ == "__main__":
    sys.exit(main())
