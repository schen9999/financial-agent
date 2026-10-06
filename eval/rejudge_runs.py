#!/usr/bin/env python3
"""Re-judge committed runs with today's judge, from their own findings files.

Question (2026-10-06): unsupported claims rose on all three arms between the
`1f51dad` runs (9jzmj, 8vpq6, p9jr2) and the stock-data-fix runs (4hsn2,
nstp9, 5bdz5), almost all qualitative Outlook watch-items. Was it the
judge or the briefs? Re-judge BOTH sides now, with identical inputs, and
compare.

Inputs are what the judge saw the first time: each findings file holds the
retrieved source context, the pre-written sections and the audited
Executive Summary + Outlook; `agent.grounding.grade_brief` gets those three,
with the current JUDGE_SYSTEM (v2) and the same temperature-0 Sonnet judge.
Counting is the aggregate's: labels per claim block, deduplicated
(`eval.label.count_labels_deduped`); a claim is qualitative when its text
has no digit; its section is found in the audited text as
`eval/parse_run_log.py` does.

Reading, stated before any re-judge call:
  - old and new runs re-judge to similar rates -> the rise was a judge-side
    shift (the same briefs now draw more UNSUPPORTED labels);
  - the new runs still re-judge clearly worse -> the rise is brief-side
    (the briefs changed).
One pass per brief at temperature 0, which is not deterministic: a single
re-judge carries the same run-to-run variance as the originals.

Writes eval/runs/rejudge-<date>/<run>/<ticker>_<arm>.findings.txt per brief
(resumable: an existing file is not re-judged) and summary.json, and prints
the table. Spends Anthropic credits: one Sonnet judge call per brief.

  python eval/rejudge_runs.py --date 2026-10-06 --runs 9jzmj 8vpq6 p9jr2 4hsn2 nstp9 5bdz5

Several re-judges of the same runs (the three-judgings protocol, adopted
2026-10-06: the original judging plus two re-judges per run) go to
separate folders: without --tag, eval/runs/rejudge-<date>/ (re-judge 1);
with --tag r2, eval/runs/rejudge-<date>-r2/ (re-judge 2). A folder's
summary.json keeps the runs of earlier invocations, so a run can be
added to a pass later.
"""
import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")  # ANTHROPIC_API_KEY for the judge, as scripts/cost_report.py loads it

from eval.label import count_labels_deduped, parse_claims, parse_findings_file  # noqa: E402

RAW = ROOT / "eval" / "runs" / "raw"


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace(",", "").replace('"', "")).strip().lower()


def summarize(findings: str, audited: str) -> dict:
    """Counts for one brief's findings: labels (deduplicated, as the
    aggregate counts), and UNSUPPORTED claims split qualitative/numeric and
    by audited section."""
    counts = count_labels_deduped(findings)
    blocks = {m.group(1): _norm(m.group(2)) for m in re.finditer(
        r"### (Executive Summary|Outlook)\n(.*?)(?=\n### |\Z)", audited, re.S)}
    out = {"supported": counts["supported"], "unsupported": counts["unsupported"],
           "inference": counts["inference"], "claims": 0, "numeric": 0,
           "unsupported_numeric": 0, "unsupported_outlook": 0}
    for c in parse_claims(findings):
        out["claims"] += 1
        numeric = bool(re.search(r"\d", c["claim"] or ""))
        out["numeric"] += numeric
        if c["label"] == "UNSUPPORTED":
            out["unsupported_numeric"] += numeric
            nc = _norm(c["claim"] or "")
            out["unsupported_outlook"] += bool(nc and nc in blocks.get("Outlook", ""))
    out["total"] = out["supported"] + out["unsupported"] + out["inference"]
    # Qualitative = everything not numeric, so a free-form verdict with no
    # CLAIM line (no text, no digit) counts as qualitative, as the claim
    # rows (eval/parse_run_log.py) count it.
    out["qualitative"] = out["total"] - out["numeric"]
    out["unsupported_qualitative"] = out["unsupported"] - out["unsupported_numeric"]
    return out


def briefs(run: str) -> list[tuple[str, dict]]:
    out = []
    for f in sorted((RAW / f"{run}-findings").rglob("*_*.md")):
        parsed = parse_findings_file(f.read_text(encoding="utf-8"))
        if not parsed or "section_block" not in parsed:
            raise SystemExit(f"{f}: no complete judge inputs (context, sections, audited)")
        out.append((f.stem, parsed))
    return out


def rejudge_one(parsed: dict, attempts: int = 3) -> str:
    from agent.grounding import grade_brief
    from eval.runtime_guards import check_fatal_api_error
    for i in range(attempts):
        try:
            return grade_brief(parsed["context"], parsed["section_block"], parsed["audited"]).findings
        except Exception as e:  # noqa: BLE001
            check_fatal_api_error(e)  # an exhausted balance stops the run loudly
            if i == attempts - 1:
                raise
            time.sleep(5 * (i + 1))


def run_all(runs: list[str], out_dir: Path, workers: int = 4) -> dict:
    jobs = []
    for run in runs:
        (out_dir / run).mkdir(parents=True, exist_ok=True)
        for stem, parsed in briefs(run):
            path = out_dir / run / f"{stem}.findings.txt"
            jobs.append((run, stem, parsed, path))
    todo = [j for j in jobs if not j[3].exists()]
    print(f"{len(jobs)} briefs, {len(todo)} to re-judge, {len(jobs) - len(todo)} already done", flush=True)

    def work(job):
        run, stem, parsed, path = job
        path.write_text(rejudge_one(parsed), encoding="utf-8", newline="\n")
        print(f"  {run} {stem}", flush=True)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(work, todo))
    summary = {}
    for run in runs:
        agg = {}
        for stem, parsed in briefs(run):
            s = summarize((out_dir / run / f"{stem}.findings.txt").read_text(encoding="utf-8"),
                          parsed["audited"])
            for k, v in s.items():
                agg[k] = agg.get(k, 0) + v
        summary[run] = agg
    return summary


def merge_summary(path: Path, new: dict) -> dict:
    """Earlier invocations' runs kept, this invocation's runs updated."""
    old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    old.update(new)
    return old


def table(summary: dict, pairs: list[tuple[str, str]]) -> str:
    L = ["| Run | Unsupported / judged | Qualitative unsupported / qualitative claims | Outlook unsupported |",
         "|---|---|---|---|"]
    for run, s in summary.items():
        L.append(f"| {run} | {s['unsupported']}/{s['total']} = {s['unsupported'] / s['total']:.2%} | "
                 f"{s['unsupported_qualitative']}/{s['qualitative']} = "
                 f"{s['unsupported_qualitative'] / s['qualitative']:.1%} | {s['unsupported_outlook']} |")
    if pairs:
        from eval.stats import fisher_exact
        L += ["", "| Old vs new (re-judged) | All claims | Fisher p |", "|---|---|---|"]
        for old, new in pairs:
            a, b = summary[old], summary[new]
            p = fisher_exact(a["unsupported"], a["total"] - a["unsupported"],
                             b["unsupported"], b["total"] - b["unsupported"])
            L.append(f"| {old} vs {new} | {a['unsupported']}/{a['total']} vs "
                     f"{b['unsupported']}/{b['total']} | {p:.4f} |")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--date", required=True)
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--pairs", nargs="*", default=[], metavar="OLD:NEW")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--tag", help="pass label, e.g. r2: writes eval/runs/rejudge-<date>-<tag>/")
    args = ap.parse_args(argv)
    out_dir = ROOT / "eval" / "runs" / (f"rejudge-{args.date}-{args.tag}" if args.tag
                                         else f"rejudge-{args.date}")
    summary = merge_summary(out_dir / "summary.json", run_all(args.runs, out_dir, args.workers))
    pairs = [tuple(p.split(":")) for p in args.pairs]
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n",
                                          encoding="utf-8", newline="\n")
    t = table(summary, pairs)
    (out_dir / "summary.md").write_text(t, encoding="utf-8", newline="\n")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(t)
    return 0


if __name__ == "__main__":
    sys.exit(main())
