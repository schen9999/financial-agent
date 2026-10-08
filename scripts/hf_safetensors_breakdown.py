#!/usr/bin/env python3
"""Weight bytes of a Hugging Face safetensors repo by tensor category, from
the shard headers only (HTTP range requests: an 8-byte length + the JSON
header per shard; no weights are downloaded), and whether the language
model fits a GPU memory budget.

Written for the 2026-10-02 vLLM-on-A10 feasibility check for
Qwen3.6-35B-A3B 4-bit builds (docs/eval-methodology.md): with
--language-model-only vLLM skips the vision tower, and the MTP draft layers
load only with speculative decoding, so "LM" below excludes both.

  python scripts/hf_safetensors_breakdown.py palmfuture/Qwen3.6-35B-A3B-GPTQ-Int4 \\
      --revision 00a66983516f8f8057741221277eed4141c9e431 --gpu-mib 23028 --util 0.90
"""
import argparse
import json
import re
import struct
import sys
import urllib.request
from collections import defaultdict


def _range(url, start, end):
    req = urllib.request.Request(url, headers={"Range": f"bytes={start}-{end}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def category(name: str) -> str:
    if "visual" in name:
        return "vision tower"
    if "mtp" in name:
        return "mtp draft layers"
    if "embed_tokens" in name:
        return "embed_tokens"
    if "lm_head" in name:
        return "lm_head"
    if "shared_expert" in name:
        return "shared experts"
    if re.search(r"\.experts\.", name):
        return "routed experts"
    if "linear_attn" in name:
        return "linear attention (Gated DeltaNet)"
    if "self_attn" in name:
        return "full attention"
    if "mlp.gate" in name:
        return "router gates"
    return "other (norms etc.)"


def breakdown(repo: str, revision: str) -> dict:
    api = f"https://huggingface.co/api/models/{repo}/revision/{revision}"
    with urllib.request.urlopen(api, timeout=60) as r:
        meta = json.load(r)
    shards = sorted(s["rfilename"] for s in meta["siblings"] if s["rfilename"].endswith(".safetensors"))
    cats = defaultdict(int)
    for f in shards:
        url = f"https://huggingface.co/{repo}/resolve/{meta['sha']}/{f}"
        n = struct.unpack("<Q", _range(url, 0, 7))[0]
        for name, t in json.loads(_range(url, 8, 8 + n - 1)).items():
            if name != "__metadata__":
                a, b = t["data_offsets"]
                cats[category(name)] += b - a
    return {"repo": repo, "sha": meta["sha"], "shards": len(shards), "bytes": dict(cats)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("repo")
    ap.add_argument("--revision", default="main", help="pin a commit sha for a reproducible number")
    ap.add_argument("--gpu-mib", type=float, default=None, help="GPU memory (nvidia-smi memory.total)")
    ap.add_argument("--util", type=float, default=0.90, help="vLLM --gpu-memory-utilization")
    args = ap.parse_args(argv)
    r = breakdown(args.repo, args.revision)
    gib = 2 ** 30
    total = sum(r["bytes"].values())
    print(f"{r['repo']} @ {r['sha']}: {r['shards']} shards, {total / gib:.2f} GiB of tensors")
    for k, v in sorted(r["bytes"].items(), key=lambda kv: -kv[1]):
        print(f"  {k:<36} {v / gib:7.2f} GiB")
    lm = (total - r["bytes"].get("vision tower", 0) - r["bytes"].get("mtp draft layers", 0)) / gib
    print(f"  language model (no vision, no MTP)   {lm:7.2f} GiB")
    if args.gpu_mib:
        budget = args.gpu_mib / 1024 * args.util
        verdict = (f"weights fit, leaving {budget - lm:.2f} GiB for the CUDA context, "
                   f"activations, KV cache and DeltaNet state" if lm < budget else
                   f"weights ALONE exceed it by {lm - budget:.2f} GiB")
        print(f"  budget {args.gpu_mib:.0f} MiB x {args.util} = {budget:.2f} GiB -> {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
