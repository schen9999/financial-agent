#!/usr/bin/env python3
"""GPTQ W4A16 quantization of the merged fine-tune for vLLM on the A10.

llm-compressor `oneshot` with a GPTQModifier, scheme W4A16 (int4 weights,
symmetric, group size 128; activations stay 16-bit), every Linear except
lm_head. The output is a compressed-tensors checkpoint that vLLM v0.10.2
loads from the weights directory's config.json alone (no --quantization
flag); on Ampere it runs the Marlin kernels.

Calibration: rows of data/sections_dataset.jsonl (the fine-tune's own
training pairs), each rendered with the model's chat template over both the
user and assistant turns, drawn in a fixed-seed order. The dataset has 104
rows; asking for more samples than there are rows is refused rather than
padded with repeats, which add no information to GPTQ's Hessian.

Next to the weights it writes quant_meta.json: sample count, seed, token
count, dataset hash, the scheme as saved, and the llm-compressor,
compressed-tensors, torch and transformers versions. Tokenizer files are
copied from the input (not re-saved by this transformers), and a list-form
extra_special_tokens is removed from tokenizer_config.json: that layout
crashes vllm v0.10.2 (deploy-runbook, bootstrap step 9).

Runs on the node's A10 in a throwaway venv; llm-compressor is not an app
dependency and stays out of requirements.txt and the image. The 1.5B model
needs a few GB of GPU memory, so free the GPU first (vLLM holds 90% of it):

  python3 -m venv /home/ubuntu/venvs/llmc
  /home/ubuntu/venvs/llmc/bin/pip install llmcompressor==0.7.1
  kubectl -n financial-agent scale deployment/vllm --replicas=0
  /home/ubuntu/venvs/llmc/bin/python scripts/quantize_w4a16.py --num-samples 104
  make vm-vllm          # back to the BF16 fine-tune, or serve the W4A16 dir:
  make vm-vllm MODEL_DIR=qwen-ft-w4a16 SERVED_NAME=financial-lora-w4a16 MAX_LEN=4096
"""
import argparse
import hashlib
import json
import random
import shutil
import sys
import time
from importlib.metadata import version
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_IN = "/home/ubuntu/models/qwen-ft"
DEFAULT_OUT = "/home/ubuntu/models/qwen-ft-w4a16"
DEFAULT_DATA = REPO / "data" / "sections_dataset.jsonl"
GROUP_SIZE = 128
IGNORE = ["lm_head"]
TOKENIZER_FILES = ("tokenizer.json", "tokenizer_config.json", "chat_template.jinja",
                   "vocab.json", "merges.txt", "special_tokens_map.json", "added_tokens.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def pick_rows(rows: list, n: int, seed: int) -> list:
    """n rows in a fixed-seed order; refuses n > len(rows) (no repeats)."""
    if not 0 < n <= len(rows):
        raise SystemExit(f"quantize_w4a16: --num-samples {n} but the dataset has "
                         f"{len(rows)} rows (repeats add nothing to GPTQ); "
                         f"use 1..{len(rows)}")
    return random.Random(seed).sample(rows, n)


def strip_extra_special_tokens(tokenizer_config: Path) -> bool:
    """Delete a list-form extra_special_tokens (vllm v0.10.2 needs a dict or none)."""
    cfg = json.loads(tokenizer_config.read_text(encoding="utf-8"))
    if not isinstance(cfg.get("extra_special_tokens"), list):
        return False
    del cfg["extra_special_tokens"]
    tokenizer_config.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n",
                                encoding="utf-8")
    return True


def saved_scheme(out: Path) -> dict:
    """The quantization config vLLM will read, checked against what was asked."""
    q = json.loads((out / "config.json").read_text(encoding="utf-8")).get("quantization_config")
    if not q or q.get("quant_method") != "compressed-tensors":
        raise SystemExit("quantize_w4a16: saved config.json has no compressed-tensors "
                         "quantization_config")
    weights = [g["weights"] for g in q["config_groups"].values()]
    if any((w["num_bits"], w["group_size"]) != (4, GROUP_SIZE) for w in weights):
        raise SystemExit(f"quantize_w4a16: saved weights scheme {weights} is not 4-bit, "
                         f"group size {GROUP_SIZE}")
    return {"format": q.get("format"), "config_groups": q["config_groups"],
            "ignore": q.get("ignore")}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--input", default=DEFAULT_IN)
    ap.add_argument("--output", default=DEFAULT_OUT)
    ap.add_argument("--dataset", default=str(DEFAULT_DATA))
    ap.add_argument("--num-samples", type=int, default=256)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--max-seq-length", type=int, default=2048)
    args = ap.parse_args(argv)

    src, out, data = Path(args.input), Path(args.output), Path(args.dataset)
    if out.exists():
        raise SystemExit(f"quantize_w4a16: {out} exists; remove it first")
    rows = [json.loads(line) for line in data.read_text(encoding="utf-8").splitlines() if line]
    picked = pick_rows(rows, args.num_samples, args.seed)

    import torch
    from datasets import Dataset
    from llmcompressor import oneshot
    from llmcompressor.modifiers.quantization import GPTQModifier
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if not torch.cuda.is_available():
        raise SystemExit("quantize_w4a16: no CUDA device (is vLLM still holding the GPU?)")
    torch.manual_seed(args.seed)
    tokenizer = AutoTokenizer.from_pretrained(src)
    model = AutoModelForCausalLM.from_pretrained(src, torch_dtype="auto")

    texts = [tokenizer.apply_chat_template(r["messages"], tokenize=False) for r in picked]
    enc = tokenizer(texts, add_special_tokens=False, truncation=True,
                    max_length=args.max_seq_length)
    ds = Dataset.from_dict({"input_ids": enc["input_ids"],
                            "attention_mask": enc["attention_mask"]})
    n_tokens = sum(len(ids) for ids in enc["input_ids"])
    truncated = sum(len(ids) >= args.max_seq_length for ids in enc["input_ids"])

    t0 = time.time()
    oneshot(model=model, dataset=ds,
            recipe=GPTQModifier(targets="Linear", scheme="W4A16", ignore=IGNORE),
            max_seq_length=args.max_seq_length, num_calibration_samples=len(picked),
            shuffle_calibration_samples=False)
    seconds = time.time() - t0
    model.save_pretrained(out, save_compressed=True)

    for name in TOKENIZER_FILES:
        if (src / name).exists():
            shutil.copy2(src / name, out / name)
    stripped = strip_extra_special_tokens(out / "tokenizer_config.json")

    meta = {
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "input_dir": str(src), "output_dir": str(out),
        "algorithm": "GPTQ", "scheme": "W4A16", "group_size": GROUP_SIZE, "ignore": IGNORE,
        "saved_quantization_config": saved_scheme(out),
        "calibration": {
            "dataset": str(data.relative_to(REPO) if data.is_relative_to(REPO) else data),
            "dataset_sha256": sha256(data), "dataset_rows": len(rows),
            "num_samples": len(picked), "seed": args.seed,
            "max_seq_length": args.max_seq_length, "tokens": n_tokens,
            "samples_truncated": truncated,
            "text": "chat template over the user + assistant turns",
        },
        "oneshot_seconds": round(seconds, 1),
        "gpu": torch.cuda.get_device_name(0),
        "source_dtype": str(model.config.torch_dtype),
        "source_weights_sha256": {p.name: sha256(p) for p in sorted(src.glob("*.safetensors"))},
        "weights_bytes": sum(p.stat().st_size for p in out.glob("*.safetensors")),
        "tokenizer_extra_special_tokens_stripped": stripped,
        "versions": {pkg: version(pkg) for pkg in
                     ("llmcompressor", "compressed-tensors", "torch", "transformers")},
    }
    (out / "quant_meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
