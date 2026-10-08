#!/usr/bin/env python3
"""Retroactive checks over committed findings dirs, with the same functions
the harness now applies live:

  loops    sections / audited text with a repetition run
           (agent.llm_ledger.repetition_run)
  format   audited text missing a non-empty Executive Summary or Outlook
           (agent.grounding.missing_brief_sections)
  sizes    largest section / synthesis / RAG-answer output, chars and
           chars/4 tokens — what agent/tools/slm.py's max_tokens are sized from

  python eval/findings_scan.py eval/runs/raw/*-findings
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.grounding import missing_brief_sections  # noqa: E402
from agent.llm_ledger import repetition_run  # noqa: E402
from eval.label import parse_findings_file  # noqa: E402

_RAG_LABELS = ("RAG — SEC HIGHLIGHTS:\n", "RAG — RISK FACTORS:\n")


def scan(findings_dir: Path) -> dict:
    out = {"files": 0, "loop_sections": [], "loop_audited": [], "format_fail": [],
           "max_section": 0, "max_synthesis": 0, "max_rag": 0}
    for f in sorted(findings_dir.rglob("*.md")):
        p = parse_findings_file(f.read_text(encoding="utf-8"))
        if not p:
            continue
        out["files"] += 1
        sections = p.get("section_block", "")
        if sections and repetition_run(sections):
            out["loop_sections"].append(f.stem)
        if repetition_run(p["audited"]):
            out["loop_audited"].append(f.stem)
        if missing_brief_sections(p["audited"]):
            out["format_fail"].append(f.stem)
        parts = [s for s in re.split(r"(?m)^(?=### )", sections) if s.strip()]
        if parts:
            out["max_section"] = max(out["max_section"], *(len(s) for s in parts))
        # the synthesis reproduces the sections and adds Exec Summary + Outlook
        out["max_synthesis"] = max(out["max_synthesis"], len(sections) + len(p["audited"]))
        for lab in _RAG_LABELS:
            seg = p["context"].split(lab, 1)
            if len(seg) > 1:
                ans = seg[1].split("\n\nRAG —")[0]
                if not ans.startswith("(not available)"):
                    out["max_rag"] = max(out["max_rag"], len(ans))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dirs", nargs="+")
    args = ap.parse_args(argv)
    tot = {"files": 0, "loops": 0, "format": 0}
    print(f"  {'Findings dir':<36} {'Files':>5} {'Loop(sec)':>9} {'Loop(aud)':>9} {'Format':>6}"
          f" {'MaxSec':>11} {'MaxSynth':>11} {'MaxRAG':>11}")
    for d in args.dirs:
        r = scan(Path(d))
        tot["files"] += r["files"]
        tot["loops"] += len(r["loop_sections"]) + len(r["loop_audited"])
        tot["format"] += len(r["format_fail"])

        def tok(n):
            return f"{n}c/{n // 4}t"
        print(f"  {Path(d).name:<36} {r['files']:>5} {len(r['loop_sections']):>9} "
              f"{len(r['loop_audited']):>9} {len(r['format_fail']):>6} {tok(r['max_section']):>11}"
              f" {tok(r['max_synthesis']):>11} {tok(r['max_rag']):>11}")
    print(f"  total: {tot['files']} files, {tot['loops']} loop hits, {tot['format']} format failures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
