#!/usr/bin/env python3
"""Draw a judge-v2 calibration sample from the new three-way, with all
three judgings' verdicts per claim.

Why: the judge moved by up to ~2x between judgings of identical inputs
(eval-methodology, "the judge's run-to-run noise on identical inputs",
2026-10-06), so a calibration of one judging calibrates one draw of the
noise. Each sampled claim carries its verdict from every judging, so
precision and recall can be reported per judging, for the majority vote,
and judge-judge agreement measured (eval/threejudge_report.py).

Population: every claim any of the three judgings listed, per brief, for
the given citable runs. The judgings list different claims, so claims are
unified per brief by matching their normalized text: equal, one contained
in the other, or content-word overlap (Jaccard) >= 0.6. A claim a judging
did not list gets NOT_LISTED from it (counted as "not flagged" in recall).
The wording shown is the first judging's that listed it. Free-form
verdicts without a CLAIM line cannot be labelled and are not in the pool.

Strata (mutually exclusive, first match wins), with targets:
  U  flagged UNSUPPORTED by at least one judging           up to 60
  I  else INFERENCE in at least one judging (borderline)   up to 30
  W  else an Outlook claim with no digit (watch-items)     up to 40
  S  else (SUPPORTED by every judging that listed it)      the rest, to 180
A stratum short of its target is taken whole and the shortfall goes to S.
Within a stratum: sort by (run, ticker, claim), seeded shuffle, take n — a
simple random draw. Weight per sampled claim = N_stratum / n_stratum, so
recall and the true rate reweight to the population.

Exclusions: claims already in an earlier labelled set (sample, holdout,
calibration batch, relabel sets), by normalized text.

Outputs (refuses to overwrite without --force):
  eval/judge_validation/threejudge_sample.csv   id, ticker, claim, context,
      human_label (blank) — blind: no run, arm, stratum or verdict; shuffled
  eval/judge_validation/threejudge_key.csv      per id: run, arm, ticker,
      section, qualitative, stratum, weight, j1, j2, j3, majority  (gitignored)
  eval/judge_validation/threejudge_method.json  populations, targets, seed

Labelling (blind; the labeller never opens a key and refuses one):
  python eval/label_cli.py --csv eval/judge_validation/threejudge_sample.csv

  python eval/build_threejudge_calibration.py --runs 4hsn2 nstp9 <cpu-run> \\
      --judgings raw eval/runs/rejudge-2026-10-06 eval/runs/rejudge-2026-10-06-r2
"""
import argparse
import csv
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from eval.label import parse_claims, parse_findings_file  # noqa: E402

RAW = ROOT / "eval" / "runs" / "raw"
JV = ROOT / "eval" / "judge_validation"
TARGETS = {"U": 60, "I": 30, "W": 40}
TOTAL = 180
STOP = {"the", "a", "an", "of", "and", "in", "to", "its", "for", "on", "with", "as", "at", "by",
        "is", "that", "from", "this", "be", "or", "it", "are", "while"}
EARLIER = ("sample.csv", "holdout_sample.csv", "calibration_batch.csv", "relabel_S.csv",
           "relabel_UI.csv", "fourarm_holdout_sample.csv")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").replace(",", "").replace('"', "")).strip().lower()


def words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9$%.]+", norm(s)) if w not in STOP}


def same_claim(a: str, b: str) -> bool:
    na, nb = norm(a), norm(b)
    if not na or not nb:
        return False
    if na == nb or na in nb or nb in na:
        return True
    wa, wb = words(a), words(b)
    return bool(wa and wb) and len(wa & wb) / len(wa | wb) >= 0.6


def unify(judgings: list[list[dict]]) -> list[dict]:
    """[{claim, verdicts: [v1, v2, v3]}] for one brief, from each judging's
    parsed claims (label in SUPPORTED/UNSUPPORTED/INFERENCE)."""
    out = []
    for j, claims in enumerate(judgings):
        for c in claims:
            if not c["claim"]:
                continue
            hit = next((u for u in out if u["verdicts"][j] == "NOT_LISTED"
                        and same_claim(u["claim"], c["claim"])), None)
            if hit is None:
                hit = {"claim": c["claim"], "verdicts": ["NOT_LISTED"] * len(judgings)}
                out.append(hit)
            hit["verdicts"][j] = c["label"]
    return out


def majority(verdicts: list[str]) -> str:
    """UNSUPPORTED when at least two judgings said so; else the most common
    of the other listed verdicts, SUPPORTED on ties; NOT_LISTED when one
    judging flagged it and no other listed it (not flagged either way)."""
    if sum(v == "UNSUPPORTED" for v in verdicts) >= 2:
        return "UNSUPPORTED"
    listed = Counter(v for v in verdicts if v in ("SUPPORTED", "INFERENCE"))
    if not listed:
        return "NOT_LISTED"
    return max(("SUPPORTED", "INFERENCE"), key=lambda v: listed[v])


def stratum(c: dict) -> str:
    v = c["verdicts"]
    if "UNSUPPORTED" in v:
        return "U"
    if "INFERENCE" in v:
        return "I"
    if c["section"] == "Outlook" and not re.search(r"\d", c["claim"]):
        return "W"
    return "S"


def src_dir(source: str) -> Path:
    p = Path(source)
    return p if p.is_absolute() else ROOT / p


def section_of(claim: str, blocks: dict) -> str:
    """The audited section holding the claim: the one containing its
    normalized text, else the one sharing most of its content words (at
    least half); "" when neither (a paraphrase spanning both)."""
    nc, wc = norm(claim), words(claim)
    for s, b in blocks.items():
        if nc and nc in b:
            return s
    best = max(blocks, key=lambda s: len(wc & words(blocks[s])), default="")
    return best if best and wc and len(wc & words(blocks[best])) >= len(wc) / 2 else ""


def judging_findings(source: str, run: str, stem: str) -> str:
    if source == "raw":
        return parse_findings_file((RAW / f"{run}-findings" / f"{stem}.md").read_text(encoding="utf-8"))["findings"]
    return (src_dir(source) / run / f"{stem}.findings.txt").read_text(encoding="utf-8")


def population(runs: list[str], sources: list[str]) -> list[dict]:
    rows = []
    for run in runs:
        for f in sorted((RAW / f"{run}-findings").rglob("*_*.md")):
            stem = f.stem
            for src in sources[1:]:
                if not (src_dir(src) / run / f"{stem}.findings.txt").exists():
                    raise SystemExit(f"judging {src} lacks {run}/{stem}: all three judgings must exist")
            p = parse_findings_file(f.read_text(encoding="utf-8"))
            ticker, arm = stem.rsplit("_", 1)
            context = (f"=== RETRIEVED SOURCE CONTEXT ===\n{p['context']}\n\n"
                       f"=== AUDITED TEXT (Exec Summary + Outlook) ===\n{p['audited']}\n\n"
                       f"=== PRE-WRITTEN SECTIONS (judge input) ===\n{p.get('section_block', '')}")
            blocks = {m.group(1): norm(m.group(2)) for m in re.finditer(
                r"### (Executive Summary|Outlook)\n(.*?)(?=\n### |\Z)", p["audited"], re.S)}
            judged = [parse_claims(judging_findings(src, run, stem)) for src in sources]
            for c in unify(judged):
                c.update(run=run, arm=arm, ticker=ticker, context=context,
                         section=section_of(c["claim"], blocks),
                         qualitative=not re.search(r"\d", c["claim"]))
                c["stratum"] = stratum(c)
                c["majority"] = majority(c["verdicts"])
                rows.append(c)
    return rows


def draw(rows: list[dict], seed: int, earlier: set[str]) -> tuple[list[dict], dict]:
    pool = [r for r in rows if norm(r["claim"]) not in earlier]
    by = {k: sorted((r for r in pool if r["stratum"] == k),
                    key=lambda r: (r["run"], r["ticker"], r["claim"])) for k in "UIWS"}
    rng = random.Random(seed)
    n = {k: min(TARGETS[k], len(by[k])) for k in "UIW"}
    n["S"] = min(TOTAL - sum(n.values()), len(by["S"]))
    picked = []
    for k in "UIWS":
        pool_k = by[k][:]
        rng.shuffle(pool_k)
        for r in pool_k[:n[k]]:
            r["weight"] = len(by[k]) / n[k]
            picked.append(r)
    method = {"population": {k: len(by[k]) for k in "UIWS"}, "sample": n, "targets": TARGETS,
              "total": TOTAL, "seed": seed, "excluded_as_earlier": len(rows) - len(pool)}
    return picked, method


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--judgings", nargs=3, required=True,
                    help="raw (the original judging), then two rejudge_runs.py folders")
    ap.add_argument("--seed", type=int, default=20261006)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)
    out_csv, key_csv, meth = (JV / "threejudge_sample.csv", JV / "threejudge_key.csv",
                              JV / "threejudge_method.json")
    if meth.exists() and not args.force:
        raise SystemExit(f"{meth.name} exists: the sample is drawn; --force redraws")
    earlier = set()
    for name in EARLIER:
        if (JV / name).exists():
            with open(JV / name, newline="", encoding="utf-8") as f:
                earlier |= {norm(r["claim"]) for r in csv.DictReader(f)}
    rows = population(args.runs, args.judgings)
    picked, method = draw(rows, args.seed, earlier)
    random.Random(args.seed + 1).shuffle(picked)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "ticker", "claim", "context", "human_label"])
        for i, r in enumerate(picked):
            w.writerow([i, r["ticker"], r["claim"], r["context"], ""])
    with open(key_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "run", "arm", "ticker", "section", "qualitative", "stratum", "weight",
                    "j1", "j2", "j3", "majority"])
        for i, r in enumerate(picked):
            w.writerow([i, r["run"], r["arm"], r["ticker"], r["section"], int(r["qualitative"]),
                        r["stratum"], f"{r['weight']:.6f}", *r["verdicts"], r["majority"]])
    method.update(runs=args.runs, judgings=args.judgings,
                  matching="normalized equal / containment / content-word Jaccard >= 0.6")
    meth.write_text(json.dumps(method, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(method, indent=2))
    print(f"wrote {out_csv.name} ({len(picked)} rows, blind) and {key_csv.name} (gitignored)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
