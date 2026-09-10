#!/usr/bin/env python3
"""Extract eval findings from kubectl logs carrying the base64 tar dumps.

The eval WorkflowTemplate prints, in every eval pod and the aggregate:

    ===EVAL_FINDINGS_TGZ_BEGIN pod=<name>===
    <base64 of tar.gz of /app/eval_findings>
    ===EVAL_FINDINGS_TGZ_END===

This script scans a captured logs file (plain `kubectl logs <pod>` or a
label-selector capture with `[pod/...]` line prefixes), decodes every
marker block, and unpacks the tar members into the output directory.
Multiple blocks merge; identical filenames overwrite (same content —
each ticker writes its own file). Extraction is traversal-safe: only
plain files under eval_findings/ are written.

Usage:
  kubectl -n financial-agent logs -l workflows.argoproj.io/workflow=<wf> \
      --prefix --tail=-1 > run.log
  python scripts/extract_findings.py --log run.log --out eval/runs/<wf>/
"""
import argparse
import base64
import io
import re
import sys
import tarfile
from pathlib import Path

BEGIN = re.compile(r"===EVAL_FINDINGS_TGZ_BEGIN.*===")
END = re.compile(r"===EVAL_FINDINGS_TGZ_END===")
_PREFIX = re.compile(r"^\[pod/[^\]]+\]\s?")


def _strip_prefix(line: str) -> str:
    return _PREFIX.sub("", line)


def extract_blocks(log_text: str) -> list[bytes]:
    """Base64-decoded payloads of every marker block in the log."""
    blocks, buf, inside = [], [], False
    for raw in log_text.splitlines():
        line = _strip_prefix(raw).strip()
        if BEGIN.search(line):
            inside, buf = True, []
            continue
        if END.search(line):
            if inside and buf:
                blocks.append(base64.b64decode("".join(buf)))
            inside = False
            continue
        if inside and line:
            buf.append(line)
    return blocks


def unpack(blob: bytes, out_dir: Path) -> int:
    """Untar one payload into out_dir; returns files written."""
    written = 0
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tf:
        for m in tf.getmembers():
            if not m.isfile():
                continue
            name = Path(m.name).name  # flatten; traversal-safe
            data = tf.extractfile(m).read()
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / name).write_bytes(data)
            written += 1
    return written


def main():
    ap = argparse.ArgumentParser(description="Extract findings dumps from kubectl logs.")
    ap.add_argument("--log", required=True)
    ap.add_argument("--out", required=True, help="e.g. eval/runs/<workflow>/")
    args = ap.parse_args()

    blocks = extract_blocks(Path(args.log).read_text(encoding="utf-8", errors="replace"))
    if not blocks:
        sys.exit("no EVAL_FINDINGS_TGZ marker blocks found in the log")
    out = Path(args.out)
    total = sum(unpack(b, out) for b in blocks)
    print(f"{len(blocks)} dump block(s), {total} file write(s) -> {out}")


if __name__ == "__main__":
    main()
