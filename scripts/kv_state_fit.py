#!/usr/bin/env python3
"""Does a GGUF fit as served, not just on file size? Computed, not booted.

For each model: the GGUF file bytes (scripts/hf_gguf_fit.py, pinned
revision) plus the per-request memory llama.cpp allocates at the harness's
context, from the model's config.json at a pinned revision:
  - KV cache for every full-attention layer, f16 (llama.cpp's default
    type_k/type_v): 2 x layers x kv_heads x head_dim x 2 bytes per token;
  - recurrent state for every linear-attention (Gated DeltaNet) layer, f32,
    per sequence: v_heads x k_dim x v_dim (the state matrix) plus
    (conv_kernel - 1) x (2 x k_heads x k_dim + v_heads x v_dim) (the conv
    state);
  - a runtime allowance (--overhead-gib, default 1.0) for compute buffers
    and the CUDA context: an ASSUMPTION, not a measurement per model.
MTP draft layers are not counted (llama.cpp loads them only for speculative
decoding). The verdict per budget: "fits as served" (file + KV + state +
allowance under the budget), "weights only" (the file fits, the rest does
not: does not fit as served), or "no" (the file alone exceeds it).

  python scripts/kv_state_fit.py --seqs 8 --tokens 5120 --budget A10=22.49 \\
    "Qwen/Qwen3.6-35B-A3B@995ad96eacd98c81ed38be0c5b274b04031597b0|ggml-org/Qwen3.6-35B-A3B-GGUF@baec3ebee244827cda0f4557eafa8b28f7545fa6|Q4_K_M"
"""
import argparse
import json
import sys
import urllib.request

from scripts.hf_gguf_fit import fit_rows, group_quants, list_files

GIB = 2**30


def load_config(repo: str, revision: str) -> dict:
    url = f"https://huggingface.co/{repo}/raw/{revision}/config.json"
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def layer_counts(cfg: dict) -> tuple[int, int]:
    """(full-attention layers, linear-attention layers), MTP excluded."""
    t = cfg.get("text_config", cfg)
    if "layer_types" in t:
        types = t["layer_types"][: t["num_hidden_layers"]]
        return types.count("full_attention"), types.count("linear_attention")
    if "attn_type_list" in t:  # MiniMax: 1 = softmax attention, 0 = lightning (linear)
        kinds = t["attn_type_list"][: t["num_hidden_layers"]]
        if 0 in kinds:
            raise ValueError("lightning-attention layers: state size not modelled here")
        return len(kinds), 0
    return t["num_hidden_layers"], 0


def kv_bytes_per_token(cfg: dict, kv_bytes: int = 2) -> int:
    t = cfg.get("text_config", cfg)
    full, _ = layer_counts(cfg)
    head_dim = t.get("head_dim") or t["hidden_size"] // t["num_attention_heads"]
    return 2 * full * t["num_key_value_heads"] * head_dim * kv_bytes


def recurrent_bytes_per_seq(cfg: dict, state_bytes: int = 4) -> int:
    t = cfg.get("text_config", cfg)
    _, linear = layer_counts(cfg)
    if not linear:
        return 0
    vh, kh = t["linear_num_value_heads"], t["linear_num_key_heads"]
    kd, vd = t["linear_key_head_dim"], t["linear_value_head_dim"]
    conv = (t["linear_conv_kernel_dim"] - 1) * (2 * kh * kd + vh * vd)
    return linear * (vh * kd * vd + conv) * state_bytes


def served_bytes(cfg: dict, file_bytes: int, seqs: int, tokens: int,
                 overhead_gib: float) -> dict:
    kv = kv_bytes_per_token(cfg) * seqs * tokens
    rec = recurrent_bytes_per_seq(cfg) * seqs
    total = file_bytes + kv + rec + overhead_gib * GIB
    return {"file": file_bytes, "kv": kv, "recurrent": rec,
            "overhead": overhead_gib * GIB, "total": total}


def verdict(file_bytes: int, total: float, budget_gib: float) -> str:
    if file_bytes > budget_gib * GIB:
        return "no"
    return "fits as served" if total <= budget_gib * GIB else "weights only"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("specs", nargs="+", metavar="CONFIG@REV|GGUF@REV|QUANT")
    ap.add_argument("--seqs", type=int, default=8)
    ap.add_argument("--tokens", type=int, default=5120, help="tokens per sequence")
    ap.add_argument("--overhead-gib", type=float, default=1.0)
    ap.add_argument("--budget", action="append", default=[], metavar="NAME=GIB")
    args = ap.parse_args(argv)
    budgets = {k: float(v) for k, v in (b.split("=", 1) for b in args.budget)}
    print(f"context: {args.seqs} sequences x {args.tokens} tokens; KV f16, recurrent state f32; "
          f"runtime allowance {args.overhead_gib} GiB (assumed)")
    for spec in args.specs:
        cfg_spec, gguf_spec, quant = spec.split("|")
        crepo, crev = cfg_spec.split("@")
        grepo, grev = gguf_spec.split("@")
        cfg = load_config(crepo, crev)
        rows = fit_rows(group_quants(list_files(grepo, grev)), {}, [quant])
        if not rows:
            print(f"== {crepo}: no {quant} in {grepo}")
            continue
        file_bytes = rows[0][1]
        full, linear = layer_counts(cfg)
        s = served_bytes(cfg, file_bytes, args.seqs, args.tokens, args.overhead_gib)
        print(f"== {crepo} @{crev[:7]} + {grepo} @{grev[:7]} {quant}")
        print(f"   layers: {full} full attention, {linear} linear; "
              f"KV {kv_bytes_per_token(cfg):,} B/token; recurrent {recurrent_bytes_per_seq(cfg):,} B/sequence")
        print(f"   file {s['file']/GIB:.2f} + KV {s['kv']/GIB:.2f} + recurrent {s['recurrent']/GIB:.2f} "
              f"+ allowance {s['overhead']/GIB:.2f} = {s['total']/GIB:.2f} GiB")
        for b, cap in budgets.items():
            print(f"   {b} ({cap} GiB): {verdict(file_bytes, s['total'], cap)} "
                  f"({cap - s['total']/GIB:+.2f} GiB as served)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
