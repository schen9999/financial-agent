#!/usr/bin/env python3
"""GGUF file sizes per quantization in Hugging Face repos, at pinned
revisions, against memory budgets. Computed, not booted: it reads the
repo's file listing (no weights are downloaded) and compares each quant's
total bytes (all shards summed; mmproj vision projectors and mtp/dflash
draft files excluded) with each budget. A file under a budget is a
necessary condition for fitting, not a sufficient one: the KV cache,
compute buffers and the runtime come on top.

Written for the 2026-10-15 "why this model" fit table (docs/gpu-inference.md):

  python scripts/hf_gguf_fit.py \\
      ggml-org/Qwen3.6-35B-A3B-GGUF@baec3ebee244827cda0f4557eafa8b28f7545fa6 \\
      --quants Q4_K_M --budget A10=22.49 --budget E5-node=58
"""
import argparse
import json
import re
import sys
import urllib.request

API = "https://huggingface.co/api/models/"
_SHARD = re.compile(r"-\d{5}-of-\d{5}\.gguf$")
_EXTRA = ("mmproj", "mtp-", "dflash")


def _get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def list_files(repo: str, revision: str) -> list[tuple[str, int]]:
    """(path, bytes) of every file in the repo at the revision, recursively."""
    out, todo = [], [""]
    while todo:
        p = todo.pop()
        for e in _get(f"{API}{repo}/tree/{revision}" + (f"/{p}" if p else "")):
            if e["type"] == "directory":
                todo.append(e["path"])
            else:
                out.append((e["path"], e.get("lfs", {}).get("size", e.get("size", 0))))
    return out


def group_quants(files: list[tuple[str, int]]) -> dict[str, tuple[int, int]]:
    """Model GGUFs grouped by quant name: {name: (total bytes, file count)}.
    Shards ("-00001-of-00004.gguf") sum into one entry; projector and draft
    files are dropped."""
    groups: dict[str, list[int]] = {}
    for path, size in files:
        name = path.rsplit("/", 1)[-1]
        if not name.endswith(".gguf") or name.startswith(_EXTRA):
            continue
        key = _SHARD.sub("", name).removesuffix(".gguf")
        g = groups.setdefault(key, [0, 0])
        g[0] += size
        g[1] += 1
    return {k: (v[0], v[1]) for k, v in groups.items()}


def quant_label(name: str) -> str:
    """The quant part of a GGUF name: the text after the last '-' that
    starts a quant tag (Q*, IQ*, TQ*, UD-*, BF16, F16, MXFP4*)."""
    m = re.search(r"-((?:UD-)?(?:[IT]?Q\d\w*|BF16|F16|MXFP4\w*))$", name)
    return m.group(1) if m else name


def fit_rows(groups, budgets: dict[str, float], quants: list[str] | None):
    """Rows sorted by size: (quant, bytes, GiB, files, {budget: margin GiB})."""
    rows = []
    for name, (size, n) in groups.items():
        q = quant_label(name)
        if quants and q not in quants:
            continue
        gib = size / 2**30
        rows.append((q, size, gib, n, {b: cap - gib for b, cap in budgets.items()}))
    return sorted(rows, key=lambda r: r[1])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("repos", nargs="+", help="repo@revision (a full commit sha)")
    ap.add_argument("--budget", action="append", default=[], metavar="NAME=GIB",
                    help="memory budget in GiB, repeatable")
    ap.add_argument("--quants", nargs="*", help="only these quant tags (e.g. Q4_K_M UD-IQ1_M)")
    ap.add_argument("--smallest", action="store_true", help="also print the smallest quant in each repo")
    args = ap.parse_args(argv)
    budgets = {}
    for b in args.budget:
        k, v = b.split("=", 1)
        budgets[k] = float(v)
    for spec in args.repos:
        repo, _, rev = spec.partition("@")
        if not rev:
            print(f"{spec}: give repo@revision", file=sys.stderr)
            return 2
        groups = group_quants(list_files(repo, rev))
        rows = fit_rows(groups, budgets, args.quants)
        if args.smallest:
            allrows = fit_rows(groups, budgets, None)
            if allrows and allrows[0] not in rows:
                rows = [allrows[0]] + rows
        print(f"== {repo} @{rev[:7]}")
        for q, size, gib, n, margins in rows:
            m = "  ".join(f"{b}: {'fits file' if d >= 0 else 'exceeds'} ({d:+.2f} GiB)"
                          for b, d in margins.items())
            print(f"   {q:<12} {size:>16,} B  {gib:7.2f} GiB  {n:>2} file(s)  {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
