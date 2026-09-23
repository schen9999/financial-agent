#!/usr/bin/env python3
"""Rewrite the rendered k3s-gpu vLLM overlay to serve a different model.

Reads `kubectl kustomize k8s/vllm/overlays/k3s-gpu` on stdin, writes the same
manifests on stdout with three values swapped:

  hostPath   /home/ubuntu/models/<model-dir>   (weights directory on the VM)
  --served-model-name=<served-name>            (the id /v1/models lists)
  --max-model-len=<max-len>                    (per model: KV cache must fit
                                                the A10's 24 GB beside the weights)

The in-container mount path (/models/financial-lora) stays fixed: it is an
internal name only, so the swap touches nothing else. With the defaults the
output is byte-identical to the input — `make vm-vllm` with no overrides
reproduces the committed deployment exactly.

Each value must occur exactly once in the render; anything else means the
overlay drifted from what this script expects, and it exits non-zero rather
than apply a half-swapped deployment. Stdlib only: it runs on the VM host.

Usage (what `make vm-vllm` runs):
  kubectl kustomize k8s/vllm/overlays/k3s-gpu \\
    | python3 scripts/vllm_model_swap.py --model-dir qwen7b-instruct \\
        --served-name qwen7b --max-len 8192 \\
    | kubectl apply -f -
"""
import argparse
import re
import sys

DEFAULT_MODEL_DIR = "qwen-ft"
DEFAULT_SERVED_NAME = "financial-lora"
DEFAULT_MAX_LEN = 4096

MODELS_ROOT = "/home/ubuntu/models/"
_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _one(text: str, old: str, new: str) -> str:
    """Replace the single whole-line-ending occurrence of `old`, or die."""
    pattern = re.compile(re.escape(old) + r"$", re.M)
    hits = len(pattern.findall(text))
    if hits != 1:
        raise SystemExit(f"vllm_model_swap: expected exactly 1 occurrence of "
                         f"{old!r} in the render, found {hits} — overlay drifted")
    return pattern.sub(lambda _: new, text)


def swap(render: str, model_dir: str, served_name: str, max_len: int) -> str:
    for label, value in (("model dir", model_dir), ("served name", served_name)):
        if not _NAME_RE.match(value) or ".." in value:
            raise SystemExit(f"vllm_model_swap: invalid {label} {value!r} "
                             f"(letters, digits, . _ - only; no slashes)")
    if max_len <= 0:
        raise SystemExit(f"vllm_model_swap: invalid max len {max_len}")
    out = _one(render, f"path: {MODELS_ROOT}{DEFAULT_MODEL_DIR}",
               f"path: {MODELS_ROOT}{model_dir}")
    out = _one(out, f"--served-model-name={DEFAULT_SERVED_NAME}",
               f"--served-model-name={served_name}")
    out = _one(out, f"--max-model-len={DEFAULT_MAX_LEN}",
               f"--max-model-len={max_len}")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--model-dir", default=DEFAULT_MODEL_DIR)
    ap.add_argument("--served-name", default=DEFAULT_SERVED_NAME)
    ap.add_argument("--max-len", type=int, default=DEFAULT_MAX_LEN)
    args = ap.parse_args()
    sys.stdout.write(swap(sys.stdin.read(), args.model_dir,
                          args.served_name, args.max_len))


if __name__ == "__main__":
    main()
