#!/usr/bin/env python3
"""Reconstruct per-claim rows for an Argo eval run from its captured
artifacts: the pod log (per-ticker count lines) and the workflow yaml
(per-pod result output parameters, which carry INFERENCE claim texts).

Honesty of the output, stated up front: the run's full per-claim findings
(claim texts for SUPPORTED/UNSUPPORTED, rationales, sections, contexts)
were written to /app/eval_findings INSIDE the eval pods and are not in
these artifacts — the known archival gap. Rows therefore carry:
  claim            text for INFERENCE claims (from inference_claims in the
                   pod result params); null otherwise
  judge_label      always present (reconstructed from the counts)
  judge_rationale  always null (not persisted anywhere)
  section          always null (not persisted anywhere)
  context_hash     always null (contexts not persisted anywhere)
  source           which artifact the row came from
The parser cross-checks log counts against workflow-parameter counts per
(ticker, arm) and reports mismatches.

Usage:
  python eval/parse_run_log.py --log eval/runs/9j2dj-full.log \
      --workflow-yaml eval/runs/9j2dj-workflow.yaml \
      --run grounding-eval-extended-9j2dj \
      --out eval/runs/9j2dj-claims.jsonl
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import yaml

_LOG_LINE = re.compile(
    r"\[(?P<ticker>[A-Z.-]{1,6}) \| (?P<arm>[\w-]+)\]\s+(?P<sup>\d+) SUP\s+"
    r"(?P<uns>\d+) UNSUP\s+(?P<inf>\d+) INF\s+\((?P<tot>\d+) claims\)")


def parse_log_counts(log_text: str) -> dict:
    counts = {}
    for m in _LOG_LINE.finditer(log_text):
        counts[(m["ticker"], m["arm"])] = {
            "supported": int(m["sup"]), "unsupported": int(m["uns"]),
            "inference": int(m["inf"]), "total": int(m["tot"]),
        }
    return counts


def parse_workflow_results(wf: dict) -> dict:
    """(ticker, arm) -> result row dicts from eval-one nodes' output params."""
    rows = {}
    for node in (wf.get("status", {}).get("nodes", {}) or {}).values():
        if node.get("templateName") != "eval-one":
            continue
        for p in (node.get("outputs", {}) or {}).get("parameters", []) or []:
            if p.get("name") != "result" or not p.get("value"):
                continue
            payload = json.loads(p["value"])
            for row in payload.get("results", []):
                rows[(row["ticker"], row["arm"])] = row
    return rows


def emit_rows(run: str, results: dict) -> list[dict]:
    out = []
    for (ticker, arm), row in sorted(results.items()):
        base = {
            "run": run, "ticker": ticker, "arm": arm,
            "judge_version": row.get("judge_version"),
            "section": None, "judge_rationale": None, "context_hash": None,
        }
        inf_texts = list(row.get("inference_claims") or [])
        if len(inf_texts) != row["inference"]:
            print(f"WARNING: {ticker}/{arm}: {len(inf_texts)} inference texts "
                  f"vs count {row['inference']}")
        for label, n in (("SUPPORTED", row["supported"]),
                         ("UNSUPPORTED", row["unsupported"])):
            for _ in range(n):
                out.append({**base, "claim": None, "judge_label": label,
                            "source": "reconstructed-from-counts"})
        for i in range(row["inference"]):
            out.append({**base,
                        "claim": inf_texts[i] if i < len(inf_texts) else None,
                        "judge_label": "INFERENCE",
                        "source": "workflow-output-params:inference_claims"})
    return out


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace(",", "").replace('"', "")).strip().lower()


def rows_from_findings_dir(run: str, findings_dir: Path, results: dict,
                           contexts_dir: Path | None = None) -> list[dict]:
    """Full per-claim rows from recovered findings files ({TICKER}_{arm}.md,
    or <TICKER>/{TICKER}_{arm}.md). Preferred over the label-only
    reconstruction: rows carry claim text, judge rationale, section
    (located within the audited Exec Summary / Outlook blocks), and the
    sha256 of the exact retrieved-context string the judge saw (context
    bodies written to contexts_dir/<sha>.txt). judge_version comes from the
    file's own `## Metadata` block when present (extended format), else from
    the matching workflow result row."""
    import hashlib

    from eval.label import parse_claims, parse_findings_file

    out = []
    for f in sorted(findings_dir.rglob("*_*.md")):
        ticker, arm = f.stem.rsplit("_", 1)
        parsed = parse_findings_file(f.read_text(encoding="utf-8"))
        if not parsed:
            print(f"WARNING: could not parse {f}")
            continue
        ctx = parsed["context"]
        sha = hashlib.sha256(ctx.encode("utf-8")).hexdigest()
        if contexts_dir is not None:
            contexts_dir.mkdir(parents=True, exist_ok=True)
            (contexts_dir / f"{sha}.txt").write_text(ctx, encoding="utf-8")
        # Section blocks of the audited text, for locating each claim.
        blocks = {}
        for m in re.finditer(r"### (Executive Summary|Outlook)\n(.*?)(?=\n### |\Z)",
                             parsed["audited"], re.S):
            blocks[m.group(1)] = _norm(m.group(2))
        wf_row = results.get((ticker, arm), {})
        judge_version = (parsed.get("metadata", {}).get("judge_prompt_version")
                         or wf_row.get("judge_version"))
        for c in parse_claims(parsed["findings"]):
            nc = _norm(c["claim"])
            section = next((name for name, body in blocks.items() if nc and nc in body),
                           None)
            out.append({
                "run": run, "ticker": ticker, "arm": arm,
                "judge_version": judge_version,
                "section": section,
                "claim": c["claim"], "judge_label": c["label"],
                "judge_rationale": c["reason"] or None,
                "context_sha256": sha,
                "source": "recovered-findings",
            })
        # The judge occasionally deviates from the CLAIM/LABEL/REASON format:
        # a block can carry EXTRA LABEL+REASON pairs. Observed 2026-09-05
        # (9j2dj): a pair with a DIFFERENT label than the block's primary is
        # a distinct free-form verdict (BEAM's real UNSUPPORTED); a pair with
        # the SAME label re-explains the same claim (JPM) and is suppressed
        # as a duplicate — which also explains the run's own count being one
        # high (count_labels counts every LABEL: line).
        for block in re.split(r"\*{0,2}CLAIM:\*{0,2}", parsed["findings"])[1:]:
            pairs = re.findall(
                r"\*{0,2}LABEL:\*{0,2}\s*([A-Za-z]+)\s*\n\*{0,2}REASON:\*{0,2}\s*(.+)",
                block)
            if len(pairs) <= 1:
                continue
            primary = pairs[0][0].upper()
            for label, reason in pairs[1:]:
                if label.upper() == primary:
                    print(f"NOTE {ticker}/{arm}: duplicate {label} label within "
                          f"one claim block — suppressed (run count inflated by 1)")
                    continue
                if label.upper() not in ("SUPPORTED", "UNSUPPORTED", "INFERENCE"):
                    continue
                print(f"NOTE {ticker}/{arm}: free-form {label} verdict without "
                      f"CLAIM line — emitted with claim=null")
                out.append({
                    "run": run, "ticker": ticker, "arm": arm,
                    "judge_version": judge_version,
                    "section": None, "claim": None,
                    "judge_label": label.upper(),
                    "judge_rationale": reason.strip() or None,
                    "context_sha256": sha,
                    "source": "recovered-freeform-label",
                })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True)
    ap.add_argument("--workflow-yaml", required=True)
    ap.add_argument("--run", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--findings-dir", default=None,
                    help="Directory of recovered findings files — preferred "
                         "source: full claim text/rationale/section/context "
                         "instead of the label-only reconstruction.")
    ap.add_argument("--contexts-dir", default=None,
                    help="Where to write context bodies keyed by sha256 "
                         "(with --findings-dir).")
    args = ap.parse_args()

    log_counts = parse_log_counts(Path(args.log).read_text(encoding="utf-8"))
    wf = yaml.safe_load(Path(args.workflow_yaml).read_text(encoding="utf-8"))
    results = parse_workflow_results(wf)

    mismatched = []
    for key, lc in sorted(log_counts.items()):
        wr = results.get(key)
        if not wr:
            mismatched.append((key, "in log, missing from workflow params"))
        elif any(lc[k] != wr[k] for k in ("supported", "unsupported", "inference", "total")):
            mismatched.append((key, f"log {lc} != params "
                                    f"{ {k: wr[k] for k in lc} }"))
    for key in results:
        if key not in log_counts:
            mismatched.append((key, "in workflow params, missing from log"))

    if args.findings_dir:
        rows = rows_from_findings_dir(
            args.run, Path(args.findings_dir), results,
            Path(args.contexts_dir) if args.contexts_dir else None)
        # Cross-check recovered rows against workflow-param counts.
        per = {}
        for r in rows:
            key = (r["ticker"], r["arm"], r["judge_label"].lower())
            per[key] = per.get(key, 0) + 1
        for (ticker, arm), wr in sorted(results.items()):
            for lab in ("supported", "unsupported", "inference"):
                got = per.get((ticker, arm, lab), 0)
                if got != wr[lab]:
                    print(f"MISMATCH {ticker}/{arm} {lab}: findings {got} "
                          f"!= params {wr[lab]}")
    else:
        rows = emit_rows(args.run, results)
    with open(args.out, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    with_text = sum(1 for r in rows if r["claim"])
    by_label = {}
    for r in rows:
        by_label[r["judge_label"]] = by_label.get(r["judge_label"], 0) + 1
    tots = [results[k]["total"] for k in results]
    print(f"rows: {len(rows)} ({by_label}) | claim text present: {with_text} "
          f"(INFERENCE only — findings were pod-local, see module docstring)")
    print(f"tickers: {len(results)} | per-ticker claims min={min(tots)} max={max(tots)}")
    print(f"log-vs-params mismatches: {mismatched if mismatched else 'none'}")


if __name__ == "__main__":
    main()
