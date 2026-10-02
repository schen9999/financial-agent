#!/usr/bin/env python3
"""Token counts for the locally written sections, to estimate truncation at
the 512-token cap (LocalChat's max_tokens) in live runs, which do not record
finish_reason.

Method: re-tokenize each section's text with the served models' tokenizer
(Qwen2.5; quantization does not change it) and call a section truncated when
the count reaches THRESHOLD. The method is validated on the replay pilot,
where vLLM recorded finish_reason and completion_tokens for every section:
the JSON reports how often re-tokenized counts equal the recorded ones and
how well THRESHOLD reproduces finish_reason == "length".

Live sections are cut out of each findings file's pre-written block, which
the pipeline built as "\\n\\n".join(section outputs) in _SECTIONS order:
Financial Health runs up to the Recent Developments heading (Haiku writes
that section and opens it with its heading); Risk Factors runs from the
last risk-factor heading after SEC Filing Highlights to the end. The block
was whitespace-stripped when saved, so a live count can be off by a token
or two; a section whose heading cannot be found is reported as unknown.

Writes eval/numeric_check/section-token-counts.json.

Usage:
  python scripts/section_token_counts.py \\
      --tokenizer financial-lora-merged/tokenizer.json
"""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from eval.label import parse_findings_file  # noqa: E402
from eval.section_attribution import canonical_section  # noqa: E402

CAP = 512
THRESHOLD = 505
LIVE_RUNS = ("v924f", "r5nzh", "lsnnc", "4nfsm", "cnkp2")
_HEAD = re.compile(r"^#{2,3}[ \t]+(.+?)[ \t]*$", re.M)


def _replay_module():
    spec = importlib.util.spec_from_file_location(
        "replay_sections", REPO / "scripts" / "replay_sections.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def live_sections(section_block: str) -> dict:
    """{'financial-health': text|None, 'risk-factors': text|None} cut from a
    findings file's pre-written block."""
    heads = [(m.start(), canonical_section(m.group(1))) for m in _HEAD.finditer(section_block)]
    rd = next((s for s, c in heads if c == "recent-developments"), None)
    sec = next((s for s, c in heads if c == "sec-filing-highlights"), None)
    fh = section_block[:rd].rstrip("\n") if rd is not None and rd > 0 else None
    rf_start = next((s for s, c in reversed(heads)
                     if c == "risk-factors" and (sec is None or s > sec)), None)
    rf = section_block[rf_start:] if rf_start is not None else None
    return {"financial-health": fh, "risk-factors": rf}


def main():
    ap = argparse.ArgumentParser(description="Section token counts / truncation.")
    ap.add_argument("--tokenizer", default=str(REPO / "financial-lora-merged" / "tokenizer.json"))
    ap.add_argument("--pilot", default=str(REPO / "eval" / "runs" / "replay-pilot-2026-09-30"))
    ap.add_argument("--out", default=str(REPO / "eval" / "numeric_check" / "section-token-counts.json"))
    args = ap.parse_args()

    from tokenizers import Tokenizer
    tok = Tokenizer.from_file(args.tokenizer)
    count = lambda t: len(tok.encode(t, add_special_tokens=False).ids)  # noqa: E731
    rs = _replay_module()

    # Validation on the pilot (recorded finish_reason / completion_tokens).
    exact = n = agree = 0
    diffs = []
    for p in sorted(Path(args.pilot).glob("*/*-s*.md"), key=lambda p: str(p)):
        r = rs.read_replay_file(p)
        for name, text in r["sections"]:
            key = name.lower().replace(" ", "_")
            recorded = r["meta"][f"{key}_completion_tokens"]
            finish = r["meta"][f"{key}_finish_reason"]
            expected = recorded - (1 if finish == "stop" else 0)  # EOS is counted
            c = count(text)
            n += 1
            exact += c == expected
            diffs.append(c - expected)
            agree += (c >= THRESHOLD) == (finish == "length")
    validation = {"sections": n, "exact_count_matches": exact,
                  "max_abs_diff": max(abs(d) for d in diffs),
                  "threshold": THRESHOLD, "threshold_agrees_with_finish_reason": agree}

    live = {}
    for run in LIVE_RUNS:
        live[run] = {}
        for f in sorted((REPO / "eval" / "runs" / "raw" / f"{run}-findings").glob("*.md"),
                        key=lambda p: p.name):
            parsed = parse_findings_file(f.read_text(encoding="utf-8"))
            ticker = parsed.get("metadata", {}).get("ticker", f.stem.split("_")[0])
            secs = live_sections(parsed.get("section_block", ""))
            live[run][ticker] = {k: (count(v) if v is not None else None)
                                 for k, v in secs.items()}
    result = {
        "cap": CAP, "threshold": THRESHOLD,
        "tokenizer": Path(args.tokenizer).name,
        "tokenizer_sha256": hashlib.sha256(Path(args.tokenizer).read_bytes()).hexdigest(),
        "validation_on_pilot": validation,
        "live": live,
    }
    Path(args.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(validation))
    for run, t in live.items():
        vals = [v for d in t.values() for v in d.values()]
        print(run, "sections", len(vals), "unknown", sum(v is None for v in vals),
              "truncated(est)", sum(v is not None and v >= THRESHOLD for v in vals))


if __name__ == "__main__":
    main()
