#!/usr/bin/env python3
"""Re-run the CURRENT judge over the 50-claim validation sample and compare
v1 vs v2 against the same human labels.

Method: rows sharing an identical context cell come from one audited
document — the judge runs once per unique document (doc-level, exactly how
it runs in production), then each sampled claim is matched to the new
findings by normalized containment. Unmatched claims (the judge segmented
differently) are reported and excluded from the v2 confusion.

Disclosed asymmetry: findings artifacts never stored the pre-written
sections, so this re-judge (like the human labeler) sees only the retrieved
context + audited text, while the v1 key came from runs that also saw the
sections.

Writes eval/judge_validation/sample_key_v2.csv (all ids; unmatched rows
labeled UNMATCHED) and prints the side-by-side report.

Usage:  python eval/rejudge.py   (~one judge call per unique document)
"""
import csv
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from dotenv import load_dotenv  # noqa: E402
load_dotenv(REPO / ".env")

from langchain_core.messages import HumanMessage, SystemMessage  # noqa: E402

from agent.grounding import (JUDGE_PROMPT_VERSION, JUDGE_SYSTEM,  # noqa: E402
                             JUDGE_SYSTEM_V1, get_judge_llm,
                             judge_user_prompt)
from eval.agreement import (LABELS, cohens_kappa,  # noqa: E402
                            precision_recall_unsupported)
from eval.runtime_guards import check_fatal_api_error  # noqa: E402
from eval.stats import format_rate_ci  # noqa: E402

VAL = REPO / "eval" / "judge_validation"
SECTION_BLOCK_NOTE = (
    "(The pre-written sections are not available for this audit; judge the "
    "text strictly against the raw source data above.)"
)
_SPLIT = re.compile(
    r"=== RETRIEVED SOURCE CONTEXT ===\n(.*)\n\n"
    r"=== AUDITED TEXT \(Exec Summary \+ Outlook\) ===\n(.*)", re.S)


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace(",", "").replace('"', "")).strip().lower()


def parse_claims(findings: str) -> list[tuple[str, str]]:
    out = []
    for block in re.split(r"\*{0,2}CLAIM:\*{0,2}", findings)[1:]:
        claim = block.split("\n", 1)[0].strip().strip('"').strip()
        m = re.search(r"\*{0,2}LABEL:\*{0,2}\s*([A-Za-z]+)", block)
        if claim and m and m.group(1).upper() in LABELS:
            out.append((claim, m.group(1).upper()))
    return out


def match_label(claim: str, judged: list[tuple[str, str]]) -> str | None:
    nc = _norm(claim)
    for fc, lab in judged:
        nf = _norm(fc)
        if nc in nf or nf in nc:
            return lab
    return None


def report(title: str, pairs: list[tuple[str, str]]):
    print(f"\n  -- {title} ({len(pairs)} claims) --")
    print(f"  {'':<14}" + "".join(f"{lab:>13}" for lab in LABELS))
    for j in LABELS:
        row = [sum(1 for a, b in pairs if a == j and b == h) for h in LABELS]
        print(f"  {j:<14}" + "".join(f"{v:>13}" for v in row))
    pr = precision_recall_unsupported(pairs)
    print(f"  kappa: {cohens_kappa(pairs):.3f}")
    if pr["precision_n"]:
        print(f"  precision UNSUPPORTED: {format_rate_ci(pr['tp'], pr['precision_n'])} "
              f"({pr['tp']}/{pr['precision_n']})")
    else:
        print("  precision UNSUPPORTED: n/a (judge flagged none)")
    if pr["recall_n"]:
        print(f"  recall    UNSUPPORTED: {format_rate_ci(pr['tp'], pr['recall_n'])} "
              f"({pr['tp']}/{pr['recall_n']})")
    else:
        print("  recall    UNSUPPORTED: n/a (human flagged none)")


def main():
    import argparse

    ap = argparse.ArgumentParser(description="Re-judge the 50-claim sample.")
    ap.add_argument("--prompt-version", choices=["v1", "v2"],
                    default=JUDGE_PROMPT_VERSION,
                    help="Which preserved prompt to send. Selecting v1 gives a "
                         "clean comparison: same doc-level view, same inputs, "
                         "prompt as the only variable.")
    args = ap.parse_args()
    system = JUDGE_SYSTEM_V1 if args.prompt_version == "v1" else JUDGE_SYSTEM
    tag = "v1_rejudged" if args.prompt_version == "v1" else args.prompt_version
    key_path = VAL / f"sample_key_{tag}.csv"

    rows = list(csv.DictReader(open(VAL / "sample.csv", newline="", encoding="utf-8")))
    v1key = {r["id"]: r for r in
             csv.DictReader(open(VAL / "sample_key.csv", newline="", encoding="utf-8"))}

    docs = {}
    for r in rows:
        docs.setdefault(r["context"], []).append(r)
    print(f"{len(rows)} claims over {len(docs)} unique documents; "
          f"judge prompt {args.prompt_version} (doc-level, sections unavailable)")

    new_labels = {}
    for i, (ctx_cell, doc_rows) in enumerate(docs.items()):
        m = _SPLIT.search(ctx_cell)
        if not m:
            sys.exit(f"could not split context cell for ids {[r['id'] for r in doc_rows]}")
        source_context, audited = m.group(1), m.group(2)
        try:
            findings = get_judge_llm().invoke([
                SystemMessage(content=system),
                HumanMessage(content=judge_user_prompt(
                    source_context, SECTION_BLOCK_NOTE, audited)),
            ]).content
        except Exception as e:  # noqa: BLE001
            check_fatal_api_error(e)
            raise
        judged = parse_claims(findings)
        for r in doc_rows:
            new_labels[r["id"]] = match_label(r["claim"], judged) or "UNMATCHED"
        print(f"  doc {i + 1}/{len(docs)}: {len(judged)} claims judged, "
              f"{sum(1 for r in doc_rows if new_labels[r['id']] != 'UNMATCHED')}"
              f"/{len(doc_rows)} sample claims matched", flush=True)
        time.sleep(0.5)

    with open(key_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "arm", "judge_label", "judge_prompt_version"])
        for r in rows:
            w.writerow([r["id"], v1key[r["id"]]["arm"], new_labels[r["id"]],
                        args.prompt_version])

    human = {r["id"]: r["human_label"].strip().upper() for r in rows
             if r["human_label"].strip()}
    v1_pairs = [(v1key[i]["judge_label"].strip().upper(), h) for i, h in human.items()]
    matched = [i for i in human if new_labels[i] != "UNMATCHED"]
    new_pairs = [(new_labels[i], human[i]) for i in matched]
    unmatched = len(human) - len(matched)

    print("\n" + "=" * 70)
    print(f"  JUDGE v1 (original key) vs {args.prompt_version} rejudge — same human labels")
    print("=" * 70)
    report("v1 (original key, judge saw sections)", v1_pairs)
    report(f"{args.prompt_version} (re-judge, sections unavailable)", new_pairs)
    if unmatched:
        print(f"\n  NOTE: {unmatched} claims unmatched under this rejudge's "
              f"segmentation — excluded from its matrix above.")
    print(f"  key written: {key_path.name}")
    print("=" * 70)


if __name__ == "__main__":
    main()
