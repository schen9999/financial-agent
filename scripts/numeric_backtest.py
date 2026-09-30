#!/usr/bin/env python3
"""Offline backtest of the deterministic numeric check (agent/numeric_check.py)
over the committed eval findings. No API calls, no LLM.

For every eval/runs/raw/<run>-findings/**/*.md it reads the STOCK DATA block
(the stock dict the pipeline held) and the brief text the file persists —
the "Pre-written sections" block (when the file has it) plus the "Audited"
Exec Summary + Outlook — and runs the check over all of it.

Outputs:
  eval/runs/numeric-backtest-<date>.json
      per run, per arm and per (arm, served model): briefs, checked and
      unchecked numbers (with out-of-scope reasons), briefs flagged,
      findings by kind, field and section; plus synthetic-injection recall
      per perturbation type with Wilson 95% CIs (eval/perturb.py
      inject_numeric, seeded).
  eval/numeric_check/adjudication.csv
      every distinct finding (identical repeats collapsed into
      `occurrences`) with an empty `verdict` column for a human to fill:
      TRUE_ERROR or FALSE_POSITIVE. Re-running keeps verdicts already
      entered (matched on run, ticker, section, kind, field, stated,
      sentence). The script never labels anything itself.

Required assertion: lsnnc CRBU is flagged for market_cap (ratio ~100) and for
the "[City Name]" placeholder; the script exits non-zero otherwise.

Nothing here is a number of record: the backtest counts flags, and a flag is
only an error once adjudicated.

Usage:
  python scripts/numeric_backtest.py [--date 2026-09-29] [--seed 42]
"""
import argparse
import csv
import datetime
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from agent import numeric_check as nc  # noqa: E402
from eval.label import parse_findings_file  # noqa: E402
from eval.perturb import NUMERIC_PERTURBATIONS, inject_numeric  # noqa: E402
from eval.section_attribution import canonical_section  # noqa: E402
from eval.stats import wilson_interval  # noqa: E402

RAW = REPO / "eval" / "runs" / "raw"
ADJ_FIELDS = ["id", "run", "arm", "ticker", "section", "kind", "field",
              "sentence", "stated", "source", "ratio", "occurrences", "verdict"]
_ADJ_KEY = ("run", "ticker", "section", "kind", "field", "stated", "sentence")


def stock_from_context(context: str) -> dict | None:
    """The JSON object after "STOCK DATA:" in a findings file's context."""
    at = context.find("STOCK DATA:")
    if at < 0:
        return None
    start = context.find("{", at)
    try:
        obj, _ = json.JSONDecoder().raw_decode(context[start:])
    except ValueError:
        return None
    return obj if isinstance(obj, dict) else None


def load_brief(path: Path, raw_dir: Path) -> dict | None:
    """One findings file -> {run, arm, model, ticker, stock, sections,
    has_prewritten}. None when the file has no parseable stock dict."""
    parsed = parse_findings_file(path.read_text(encoding="utf-8"))
    if not parsed:
        return None
    stock = stock_from_context(parsed["context"])
    if stock is None:
        return None
    meta = parsed.get("metadata", {})
    stem_ticker, _, stem_arm = path.stem.rpartition("_")
    run = path.relative_to(raw_dir).parts[0].removesuffix("-findings")
    audited = parsed["audited"].split("\n---\n")[0]  # drop the disclaimer
    prewritten = parsed.get("section_block")
    sections = (nc.split_sections(prewritten) if prewritten else []) \
        + nc.split_sections(audited)
    return {
        "path": str(path.relative_to(REPO)).replace("\\", "/"),
        "run": run,
        "arm": meta.get("arm", stem_arm),
        "model": meta.get("local_model_served_name",
                          "hosted" if meta.get("arm", stem_arm) == "baseline"
                          else "unrecorded"),
        "ticker": meta.get("ticker", stem_ticker),
        "stock": stock,
        "sections": sections,
        "has_prewritten": prewritten is not None,
    }


def section_key(heading: str) -> str:
    h = heading.lower()
    if "executive summary" in h:
        return "executive-summary"
    if "outlook" in h:
        return "outlook"
    if heading == "(preamble)":
        return "preamble"
    return canonical_section(heading)


def _new_bucket() -> dict:
    return {"briefs": 0, "briefs_with_prewritten": 0, "checked": 0,
            "unchecked": 0, "unchecked_reasons": Counter(),
            "briefs_flagged": 0, "briefs_flagged_mismatch": 0,
            "briefs_flagged_placeholder": 0, "findings": 0,
            "distinct_findings": 0, "by_kind": Counter(),
            "by_field": Counter(), "by_section": Counter()}


def _finish(bucket: dict) -> dict:
    out = dict(bucket)
    for k in ("unchecked_reasons", "by_kind", "by_field", "by_section"):
        out[k] = dict(sorted(bucket[k].items()))
    total = bucket["checked"] + bucket["unchecked"]
    out["coverage"] = round(bucket["checked"] / total, 4) if total else None
    return out


def _distinct(findings: list[dict]) -> list[dict]:
    """Collapse identical findings (degenerate repetition in a brief)."""
    seen = {}
    for f in findings:
        key = (f["section"], f["kind"], f["field"], f["stated"], f["sentence"])
        if key in seen:
            seen[key]["occurrences"] += 1
        else:
            seen[key] = dict(f, occurrences=1)
    return list(seen.values())


def backtest(briefs: list[dict]) -> tuple[dict, list[dict]]:
    """Per-run / per-arm / per-(arm, model) summary, plus adjudication rows."""
    groups = defaultdict(_new_bucket)
    rows = []
    for b in briefs:
        report = nc.check_sections(b["sections"], b["stock"])
        b["report"] = report
        distinct = _distinct(report["findings"])
        keys = [("run", b["run"]), ("arm", b["arm"]),
                ("arm_model", f"{b['arm']}:{b['model']}"), ("all", "all")]
        for key in keys:
            g = groups[key]
            g["briefs"] += 1
            g["briefs_with_prewritten"] += b["has_prewritten"]
            g["checked"] += report["checked"]
            g["unchecked"] += report["unchecked"]
            g["unchecked_reasons"].update(report["unchecked_reasons"])
            g["briefs_flagged"] += bool(report["findings"])
            g["briefs_flagged_mismatch"] += bool(report["mismatches"])
            g["briefs_flagged_placeholder"] += bool(report["placeholders"])
            g["findings"] += len(report["findings"])
            g["distinct_findings"] += len(distinct)
            for f in distinct:
                g["by_kind"][f["kind"]] += 1
                g["by_field"][f["field"] or "(placeholder)"] += 1
                g["by_section"][section_key(f["section"])] += 1
        for f in distinct:
            rows.append({
                "run": b["run"], "arm": b["arm"], "ticker": b["ticker"],
                "section": f["section"], "kind": f["kind"],
                "field": f["field"] or "", "sentence": f["sentence"],
                "stated": f["stated"],
                "source": "" if f["source"] is None else f["source"],
                "ratio": "" if f["ratio"] is None else f"{f['ratio']:.4g}",
                "occurrences": f["occurrences"], "verdict": "",
            })
    summary = {kind: {} for kind in ("run", "arm", "arm_model")}
    for (kind, name), g in sorted(groups.items()):
        if kind == "all":
            summary["all"] = _finish(g)
        else:
            summary[kind][name] = _finish(g)
    return summary, rows


def assert_crbu(briefs: list[dict]) -> dict:
    """The motivating case must be caught: lsnnc CRBU market cap ~100x and
    the [City Name] placeholder."""
    crbu = [b for b in briefs if b["run"] == "lsnnc" and b["ticker"] == "CRBU"]
    if not crbu:
        raise AssertionError("lsnnc CRBU findings file not found")
    fs = crbu[0]["report"]["findings"]
    mc = [f for f in fs if f["kind"] == "mismatch" and f["field"] == "market_cap"
          and f["ratio"] and 90 <= f["ratio"] <= 110]
    ph = [f for f in fs if f["kind"] == "placeholder" and f["stated"] == "[City Name]"]
    if not mc or not ph:
        raise AssertionError(f"lsnnc CRBU not flagged as required: {fs}")
    return {"market_cap_ratio": round(mc[0]["ratio"], 2),
            "market_cap_stated": mc[0]["stated"],
            "placeholder": ph[0]["stated"], "passed": True}


def _merge_verdicts(rows: list[dict], path: Path) -> int:
    """Carry verdicts already entered in an existing adjudication file over
    to the regenerated rows. Returns how many were kept."""
    if not path.exists():
        return 0
    with open(path, newline="", encoding="utf-8") as f:
        old = {tuple(r[k] for k in _ADJ_KEY): r.get("verdict", "")
               for r in csv.DictReader(f)}
    kept = 0
    for r in rows:
        v = old.get(tuple(str(r[k]) for k in _ADJ_KEY), "")
        if v.strip():
            r["verdict"] = v
            kept += 1
    return kept


def write_adjudication(rows: list[dict], path: Path) -> int:
    rows.sort(key=lambda r: (r["run"], r["ticker"], r["section"], r["kind"],
                             r["field"], r["stated"]))
    kept = _merge_verdicts(rows, path)
    for i, r in enumerate(rows, 1):
        r["id"] = i
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ADJ_FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return kept


def _detected(inj: dict, report: dict) -> bool:
    targets = set(inj["targets"])
    for f in report["findings"]:
        if f["kind"] != inj["expect"]:
            continue
        if inj["expect"] == "placeholder":
            if any(f["section_index"] == i for i, _ in targets):
                return True
        elif (f["section_index"], f["field"]) in targets:
            return True
    return False


def injection_recall(briefs: list[dict], seed: int) -> dict:
    """One injection per (clean brief, perturbation type), seeded; recall per
    type with Wilson 95% CIs. Clean = the brief produced zero findings."""
    rng = random.Random(seed)
    clean = [b for b in briefs if not b["report"]["findings"]]
    out = {"seed": seed, "clean_briefs": len(clean), "by_type": {},
           "placeholder_by_token": {}}
    tokens = defaultdict(lambda: [0, 0])
    for kind in NUMERIC_PERTURBATIONS:
        n = hit = 0
        misses = []
        for b in clean:
            inj = inject_numeric(b["sections"], b["report"]["bindings"], kind, rng)
            if inj is None:
                continue
            r = nc.check_sections(inj["sections"], b["stock"])
            ok = _detected(inj, r)
            n += 1
            hit += ok
            if kind == "placeholder":
                tokens[inj["token"]][0] += 1
                tokens[inj["token"]][1] += ok
            if not ok and len(misses) < 10:
                misses.append(f"{b['run']} {b['ticker']}: {inj['note']}")
        lo, hi = wilson_interval(hit, n) if n else (0.0, 1.0)
        out["by_type"][kind] = {
            "n": n, "detected": hit,
            "recall": round(hit / n, 4) if n else None,
            "ci95": [round(lo, 4), round(hi, 4)],
            "example_misses": misses,
        }
    for tok, (n, hit) in sorted(tokens.items()):
        lo, hi = wilson_interval(hit, n)
        out["placeholder_by_token"][tok] = {
            "n": n, "detected": hit, "recall": round(hit / n, 4),
            "ci95": [round(lo, 4), round(hi, 4)]}
    return out


def main():
    ap = argparse.ArgumentParser(description="Offline numeric-check backtest.")
    ap.add_argument("--raw-dir", default=str(RAW))
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", help="default eval/runs/numeric-backtest-<date>.json")
    ap.add_argument("--adjudication",
                    default=str(REPO / "eval" / "numeric_check" / "adjudication.csv"))
    args = ap.parse_args()

    raw_dir = Path(args.raw_dir)
    files = sorted(raw_dir.glob("*-findings/**/*.md"))
    briefs, skipped = [], []
    for p in files:
        b = load_brief(p, raw_dir)
        (briefs.append(b) if b else skipped.append(str(p)))
    if not briefs:
        sys.exit(f"no findings files under {raw_dir}")

    summary, rows = backtest(briefs)
    crbu = assert_crbu(briefs)
    recall = injection_recall(briefs, args.seed)
    kept = write_adjudication(rows, Path(args.adjudication))

    result = {
        "date": args.date,
        "harness": "scripts/numeric_backtest.py",
        "check": "agent/numeric_check.py",
        "rel_tol": nc.DEFAULT_REL_TOL,
        "note": ("Flags are unadjudicated; a flag is an error only once a "
                 "human verdict says so (see adjudication.csv). Stock-field "
                 "numbers only; news and filing numbers are out of scope. "
                 "Not a number of record."),
        "files": len(files), "briefs": len(briefs), "skipped": skipped,
        "summary": summary,
        "crbu_assertion": crbu,
        "injection": recall,
        "adjudication": {"path": str(Path(args.adjudication).relative_to(REPO))
                         .replace("\\", "/"),
                         "rows": len(rows), "verdicts_kept": kept},
    }
    out = Path(args.out) if args.out else \
        REPO / "eval" / "runs" / f"numeric-backtest-{args.date}.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8",
                   newline="\n")

    a = summary["all"]
    print(f"{a['briefs']} briefs: {a['checked']} checked, {a['unchecked']} "
          f"unchecked (coverage {a['coverage']:.1%}); {a['briefs_flagged']} "
          f"flagged, {a['distinct_findings']} distinct findings")
    for name, g in summary["run"].items():
        print(f"  {name:6} {g['briefs']:3} briefs  checked {g['checked']:4}  "
              f"unchecked {g['unchecked']:4}  flagged {g['briefs_flagged']:3}  "
              f"distinct findings {g['distinct_findings']}")
    print(f"CRBU assertion: {crbu}")
    for kind, r in recall["by_type"].items():
        print(f"  inject {kind:12} {r['detected']:3}/{r['n']:3} "
              f"recall {r['recall']} CI {r['ci95']}")
    print(f"wrote {out.relative_to(REPO)} and {len(rows)} adjudication rows "
          f"({kept} verdicts kept)")


if __name__ == "__main__":
    main()
