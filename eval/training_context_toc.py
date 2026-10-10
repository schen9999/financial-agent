#!/usr/bin/env python3
"""Table-of-contents text in the fine-tune's training inputs (offline).

The fine-tune (Qwen2.5-1.5B, QLoRA) was trained on data/sections_dataset.jsonl,
built by scripts/build_dataset.py from data/raw_research.jsonl. Each input
carries the first SEC_CONTEXT_CAP (500) characters of the filing's MD&A and
Risk Factors text; the Risk Factors targets are sentences drawn from the
whole risk_factors text (build_risk_factors). This counts inputs whose Risk
Factors context reads as a TOC listing, by the committed query-time
predicate agent.tools.sec_common.is_toc_listing_chunk (imported, unchanged).

Primary: the 500-character slice the model saw. Secondary: the same
predicate over the full stored risk_factors text of each raw row.

  python eval/training_context_toc.py
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from agent.tools.sec_common import is_toc_listing_chunk  # noqa: E402
from build_dataset import SEC_CONTEXT_CAP  # noqa: E402


def input_risk_context(user_content: str) -> str:
    m = re.search(r"\nSEC: (\{.*\})\s*$", user_content, re.S)
    return (json.loads(m.group(1)).get("Risk Factors") or "") if m else ""


def main() -> int:
    rows = [json.loads(line) for line in
            (ROOT / "data" / "sections_dataset.jsonl").read_text(encoding="utf-8").splitlines() if line]
    toc, n = Counter(), Counter()
    for r in rows:
        n[r["section"]] += 1
        if is_toc_listing_chunk(input_risk_context(r["messages"][0]["content"])):
            toc[r["section"]] += 1
    raw = [json.loads(line) for line in
           (ROOT / "data" / "raw_research.jsonl").read_text(encoding="utf-8").splitlines() if line]
    rf = [(x["sec_raw"] or {}).get("risk_factors") or "" for x in raw]
    sliced = [x["ticker"] for x, t in zip(raw, rf) if is_toc_listing_chunk(t[:SEC_CONTEXT_CAP])]
    full = sum(is_toc_listing_chunk(t) for t in rf)

    print(f"Predicate: agent.tools.sec_common.is_toc_listing_chunk; slice SEC_CONTEXT_CAP = {SEC_CONTEXT_CAP}")
    print("data/sections_dataset.jsonl, Risk Factors context in the training input (what the model saw):")
    for sec in sorted(n):
        print(f"  {sec:<24} {toc[sec]}/{n[sec]} pairs with a TOC listing as risk context")
    print(f"data/raw_research.jsonl, risk_factors[:{SEC_CONTEXT_CAP}]: {len(sliced)}/{len(raw)} rows read as a TOC listing")
    print(f"  secondary, full stored risk_factors text: {full}/{len(raw)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
