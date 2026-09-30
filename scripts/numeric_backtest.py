#!/usr/bin/env python3
"""Offline backtest of the deterministic numeric check (agent/numeric_check.py)
over the committed eval findings. No API calls, no LLM.

For every eval/runs/raw/<run>-findings/**/*.md it reads the STOCK DATA block
(the stock dict the pipeline held) and the brief text the file persists —
the "Pre-written sections" block (when the file has it) plus the "Audited"
Exec Summary + Outlook — and runs the check over all of it.

A run whose files lack the pre-written sections (9j2dj: Exec Summary +
Outlook only) is PARTIAL: it is listed on its own and kept out of every
per-arm and pooled figure, since fewer sections means fewer chances to flag.

Outputs:
  eval/runs/numeric-backtest-<date>.json   (+ a .md table beside it)
      per run (labelled: arm, served model, what the run was), per arm and
      per (arm, model) over full runs only: briefs, briefs flagged, checked
      and unchecked numbers (with out-of-scope reasons), distinct mismatches
      per distinct checked number (Wilson 95% CI), findings by kind, field
      and section; plus synthetic-injection recall per perturbation type
      (eval/perturb.py inject_numeric, seeded, Wilson 95% CIs).
  eval/numeric_check/adjudication.csv
      every distinct finding (identical repeats collapsed into
      `occurrences`) with an empty `verdict` column for a human to fill with
      one of VERDICTS. Re-running keeps verdicts already entered (matched
      on run, ticker, section, kind, field, stated, sentence). The script
      never labels anything itself.

--precision reads the adjudicated CSV instead and reports precision two
ways: OTHER_DEFECT counted as a true positive, and OTHER_DEFECT excluded.

Required assertion: lsnnc CRBU is flagged for market_cap (ratio ~100) and for
the "[City Name]" placeholder; the script exits non-zero otherwise.

Nothing here is a number of record: the backtest counts flags, and a flag is
only an error once adjudicated.

Usage:
  python scripts/numeric_backtest.py [--date 2026-09-29] [--seed 42]
  python scripts/numeric_backtest.py --precision
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
ADJ_PATH = REPO / "eval" / "numeric_check" / "adjudication.csv"
ADJ_FIELDS = ["id", "run", "scope", "arm", "model", "ticker", "section", "kind",
              "field", "sentence", "stated", "source", "ratio", "occurrences",
              "verdict"]
_ADJ_KEY = ("run", "ticker", "section", "kind", "field", "stated", "sentence")

# TRUE_ERROR: the brief states the field wrong. FALSE_POSITIVE: the check is
# wrong (misbinding, right number judged wrong). OTHER_DEFECT: the flag
# points at a real defect that is not a wrong number, e.g. a truncated brief
# whose figure is cut off ("net loss of -$3").
VERDICTS = ("TRUE_ERROR", "FALSE_POSITIVE", "OTHER_DEFECT")

# What each run was, from CLAUDE.md's dated records. `model` fills in the
# served model where the findings metadata predates the field (lsnnc).
RUN_INFO = {
    "j4cnp": {"label": "hosted baseline of record, 40 tickers, 2026-09-05/06"},
    "lsnnc": {"model": "financial-lora",
              "label": "financial-lora fine-tune, 40 tickers, 2026-09-05/06 "
                       "(the original A/B against j4cnp)"},
    "kcf7s": {"label": "hosted, four-arm set, 2026-09-23"},
    "v924f": {"label": "financial-lora fine-tune, four-arm set, 2026-09-23"},
    "4nfsm": {"label": "Qwen2.5-1.5B-Instruct base, four-arm set, 2026-09-23"},
    "cnkp2": {"label": "Qwen2.5-7B-Instruct base, four-arm set, 2026-09-23"},
    "dvvxk": {"label": "hosted, same-image rerun of kcf7s, 2026-09-24"},
    "r5nzh": {"label": "financial-lora GPTQ W4A16, 40 tickers, 2026-09-29"},
}
PARTIAL_SCOPE = "partial: Exec Summary + Outlook only"

# Brief-level cluster bootstrap. Numbers in one brief are not independent
# (one model output, one stock dict, repeated phrasing), so a Wilson interval
# over numbers treats a 40-brief run as ~400 independent trials and is too
# narrow. Resampling whole briefs keeps each brief's numbers together.
BOOT_DRAWS = 10_000
BOOT_SEED = 42

# Fine-tune run-to-run comparisons (difference = first minus second). lsnnc
# and v924f are the same BF16 model on different images, so their gap is the
# run-to-run yardstick for the W4A16 run r5nzh.
FINE_TUNE_COMPARISONS = (("lsnnc", "v924f"), ("r5nzh", "v924f"),
                         ("r5nzh", "lsnnc"))


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
    run = path.resolve().relative_to(raw_dir.resolve()).parts[0] \
        .removesuffix("-findings")
    arm = meta.get("arm", stem_arm)
    audited = parsed["audited"].split("\n---\n")[0]  # drop the disclaimer
    prewritten = parsed.get("section_block")
    sections = (nc.split_sections(prewritten) if prewritten else []) \
        + nc.split_sections(audited)
    model = meta.get("local_model_served_name") \
        or RUN_INFO.get(run, {}).get("model") \
        or ("hosted" if arm == "baseline" else "unrecorded")
    return {
        "path": _rel(path),
        "run": run, "arm": arm, "model": model,
        "ticker": meta.get("ticker", stem_ticker),
        "stock": stock, "sections": sections,
        "has_prewritten": prewritten is not None,
    }


def partial_runs(briefs: list[dict]) -> set[str]:
    """Runs with any file missing the pre-written sections."""
    return {b["run"] for b in briefs if not b["has_prewritten"]}


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
    return {"runs": set(), "briefs": 0, "briefs_flagged": 0,
            "briefs_flagged_mismatch": 0, "briefs_flagged_placeholder": 0,
            "checked": 0, "checked_distinct": 0, "unchecked": 0,
            "unchecked_reasons": Counter(), "findings": 0,
            "distinct_findings": 0, "distinct_mismatches": 0,
            "by_kind": Counter(), "by_field": Counter(),
            "by_section": Counter()}


def _rate(k: int, n: int) -> dict:
    lo, hi = wilson_interval(k, n) if n else (0.0, 1.0)
    return {"k": k, "n": n, "rate": round(k / n, 4) if n else None,
            "ci95": [round(lo, 4), round(hi, 4)]}


def _finish(bucket: dict) -> dict:
    out = dict(bucket)
    out["runs"] = sorted(bucket["runs"])
    for k in ("unchecked_reasons", "by_kind", "by_field", "by_section"):
        out[k] = dict(sorted(bucket[k].items()))
    total = bucket["checked"] + bucket["unchecked"]
    out["coverage"] = round(bucket["checked"] / total, 4) if total else None
    out["briefs_flagged_rate"] = _rate(bucket["briefs_flagged"], bucket["briefs"])
    # Flags per checked number, both counted distinct within a brief so a
    # degenerate repeated sentence counts once on each side.
    out["mismatches_per_checked"] = _rate(bucket["distinct_mismatches"],
                                          bucket["checked_distinct"])
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


def _checked_distinct(report: dict) -> int:
    return len({(b["section"], b["field"], b["stated"], b["sentence"])
                for b in report["bindings"] if b["status"] == "checked"})


def _quantiles(values: list[float]) -> list[float]:
    """2.5th and 97.5th percentiles (nearest rank on the sorted draws)."""
    v = sorted(values)
    lo = v[int(0.025 * (len(v) - 1))]
    hi = v[-1 - int(0.025 * (len(v) - 1))]
    return [round(lo, 4), round(hi, 4)]


def cluster_bootstrap_ci(strata: list[list[tuple[int, int]]],
                         draws: int = BOOT_DRAWS, seed: int = BOOT_SEED) -> dict:
    """Percentile CI for sum(k) / sum(n) resampling whole briefs with
    replacement. `strata` is a list of per-run lists of (k, n) per brief;
    each stratum is resampled at its own size (a pooled arm keeps its run
    composition). Draws with n = 0 are dropped and counted."""
    rng = random.Random(seed)
    stats, empty = [], 0
    for _ in range(draws):
        k = n = 0
        for s in strata:
            for bk, bn in rng.choices(s, k=len(s)):
                k += bk
                n += bn
        if n:
            stats.append(k / n)
        else:
            empty += 1
    return {"method": f"brief-level cluster bootstrap, {draws} draws, seed {seed}",
            "ci95": _quantiles(stats) if stats else [0.0, 1.0],
            "empty_draws": empty}


def bootstrap_difference(a: dict, b: dict, draws: int = BOOT_DRAWS,
                         seed: int = BOOT_SEED) -> dict:
    """Rate difference a - b, where a and b map ticker -> (k, n). With the
    same tickers on both sides the resample draws tickers and takes both
    runs' briefs for each (paired by ticker); otherwise each run is
    resampled on its own."""
    rng = random.Random(seed)

    def rate(pairs):
        n = sum(p[1] for p in pairs)
        return sum(p[0] for p in pairs) / n if n else None

    paired = set(a) == set(b)
    tickers = sorted(a) if paired else None
    diffs = []
    for _ in range(draws):
        if paired:
            pick = rng.choices(tickers, k=len(tickers))
            ra, rb = rate([a[t] for t in pick]), rate([b[t] for t in pick])
        else:
            ra = rate(rng.choices(list(a.values()), k=len(a)))
            rb = rate(rng.choices(list(b.values()), k=len(b)))
        if ra is not None and rb is not None:
            diffs.append(ra - rb)
    point = rate(list(a.values())) - rate(list(b.values()))
    lo, hi = _quantiles(diffs)
    below = sum(d <= 0 for d in diffs) / len(diffs)
    above = sum(d >= 0 for d in diffs) / len(diffs)
    return {"difference": round(point, 4), "ci95": [lo, hi],
            "p_two_sided_bootstrap": round(min(1.0, 2 * min(below, above)), 4),
            "excludes_zero": lo > 0 or hi < 0,
            "paired_by_ticker": paired,
            "method": f"cluster bootstrap on briefs, {draws} draws, seed {seed}"}


def fine_tune_comparisons(briefs: list[dict], draws: int = BOOT_DRAWS) -> dict:
    """The FINE_TUNE_COMPARISONS differences, plus the verdict on whether
    W4A16 vs BF16 separates from run-to-run variation on this metric: only
    if r5nzh differs from BOTH BF16 runs in the same direction with each
    difference CI excluding zero."""
    by_run = defaultdict(dict)
    for b in briefs:
        by_run[b["run"]][b["ticker"]] = b["counts"]
    out = {}
    for x, y in FINE_TUNE_COMPARISONS:
        if x in by_run and y in by_run:
            out[f"{x} - {y}"] = bootstrap_difference(by_run[x], by_run[y], draws)
    q = [out.get("r5nzh - v924f"), out.get("r5nzh - lsnnc")]
    separable = all(d and d["excludes_zero"] for d in q) and \
        len({d["difference"] > 0 for d in q}) == 1
    out["w4a16_vs_bf16_separable"] = separable
    bf16 = out.get("lsnnc - v924f")
    out["statement"] = (
        "On this metric (unadjudicated numeric-check mismatches per checked "
        "number), W4A16 vs BF16 "
        + ("IS separable from run-to-run variation: r5nzh differs from both "
           "BF16 runs in the same direction with bootstrap CIs excluding zero."
           if separable else
           "is not separable from run-to-run variation: r5nzh does not differ "
           "from both BF16 fine-tune runs in the same direction with bootstrap "
           "CIs excluding zero"
           + (f", and the two BF16 runs themselves differ by "
              f"{bf16['difference']:+.1%} (CI {bf16['ci95'][0]:+.1%} to "
              f"{bf16['ci95'][1]:+.1%})." if bf16 else ".")))
    return out


def backtest(briefs: list[dict]) -> tuple[dict, list[dict]]:
    """Per-run summary (every run, labelled) and per-arm / per-(arm, model) /
    pooled summaries over full runs only; plus adjudication rows."""
    partial = partial_runs(briefs)
    groups = defaultdict(_new_bucket)
    strata = defaultdict(lambda: defaultdict(list))  # group -> run -> [(k, n)]
    rows = []
    for b in briefs:
        report = nc.check_sections(b["sections"], b["stock"])
        b["report"] = report
        distinct = _distinct(report["findings"])
        b["counts"] = (sum(f["kind"] == "mismatch" for f in distinct),
                       _checked_distinct(report))
        keys = [("run", b["run"])]
        if b["run"] not in partial:
            keys += [("arm", b["arm"]), ("arm_model", f"{b['arm']}:{b['model']}"),
                     ("all_full", "all_full")]
        for key in keys:
            strata[key][b["run"]].append(b["counts"])
            g = groups[key]
            g["runs"].add(b["run"])
            g["briefs"] += 1
            g["briefs_flagged"] += bool(report["findings"])
            g["briefs_flagged_mismatch"] += bool(report["mismatches"])
            g["briefs_flagged_placeholder"] += bool(report["placeholders"])
            g["checked"] += report["checked"]
            g["checked_distinct"] += _checked_distinct(report)
            g["unchecked"] += report["unchecked"]
            g["unchecked_reasons"].update(report["unchecked_reasons"])
            g["findings"] += len(report["findings"])
            g["distinct_findings"] += len(distinct)
            g["distinct_mismatches"] += sum(f["kind"] == "mismatch" for f in distinct)
            for f in distinct:
                g["by_kind"][f["kind"]] += 1
                g["by_field"][f["field"] or "(placeholder)"] += 1
                g["by_section"][section_key(f["section"])] += 1
        for f in distinct:
            rows.append({
                "run": b["run"],
                "scope": "partial" if b["run"] in partial else "full",
                "arm": b["arm"], "model": b["model"], "ticker": b["ticker"],
                "section": f["section"], "kind": f["kind"],
                "field": f["field"] or "", "sentence": f["sentence"],
                "stated": f["stated"],
                "source": "" if f["source"] is None else f["source"],
                "ratio": "" if f["ratio"] is None else f"{f['ratio']:.4g}",
                "occurrences": f["occurrences"], "verdict": "",
            })
    summary = {"run": {}, "arm": {}, "arm_model": {},
               "partial_runs": sorted(partial)}
    for (kind, name), g in sorted(groups.items()):
        out = _finish(g)
        # Beside the naive Wilson CI, which is too narrow (see BOOT_DRAWS).
        out["mismatches_per_checked"]["cluster_bootstrap"] = cluster_bootstrap_ci(
            [strata[(kind, name)][r] for r in sorted(strata[(kind, name)])])
        if kind == "all_full":
            summary["all_full"] = out
            continue
        if kind == "run":
            first = next(b for b in briefs if b["run"] == name)
            out.update({
                "arm": first["arm"], "model": first["model"],
                "label": RUN_INFO.get(name, {}).get("label", ""),
                "scope": PARTIAL_SCOPE if name in partial else "full",
            })
        summary[kind][name] = out
    return summary, rows


def _pct(r: dict) -> str:
    return f"{r['rate']:.1%} ({r['ci95'][0]:.1%}–{r['ci95'][1]:.1%})"


def _ci(ci: list[float], signed: bool = False) -> str:
    f = "{:+.1%}" if signed else "{:.1%}"
    return f"{f.format(ci[0])} to {f.format(ci[1])}" if signed else \
        f"{f.format(ci[0])}–{f.format(ci[1])}"


TABLE_NOTE = (
    "Mismatches are unadjudicated numeric-check flags, counted distinct per "
    "brief on both sides of the rate. The Wilson CI treats every checked "
    "number as an independent trial; numbers in one brief share a model "
    "output and a stock dict, so **the naive Wilson intervals are too "
    f"narrow**. The cluster bootstrap resamples whole briefs ({BOOT_DRAWS:,} "
    f"draws, seed {BOOT_SEED}; pooled rows resample within each run) and is "
    "the interval to quote. Where the two come out close, mismatches in that "
    "run are spread thinly across briefs. With zero mismatches every "
    "resample is zero, so the bootstrap gives no interval (n/a); the Wilson "
    "upper bound is the only bound there.")


def table_markdown(summary: dict, comparisons: dict | None = None) -> str:
    """Per-run table (full runs grouped by arm, partial runs last), the
    per-arm rows, and the fine-tune run-to-run comparisons. Unadjudicated
    flags only."""
    head = ("| Run | Arm / model | What it was | Briefs | Briefs flagged | "
            "Checked (distinct) | Mismatches per checked number | "
            "Wilson 95% CI (naive, too narrow) | Cluster bootstrap 95% CI | "
            "Unchecked | Distinct findings |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|")
    runs = summary["run"]
    order = sorted(runs, key=lambda n: (runs[n]["scope"] != "full",
                                        runs[n]["arm"], runs[n]["model"], n))

    def row(name, g, what):
        m = g["mismatches_per_checked"]
        return (f"| {name} | {g.get('arm', '')}{' / ' + g['model'] if g.get('model') else ''}"
                f" | {what} | {g['briefs']} | {g['briefs_flagged']} "
                f"({g['briefs_flagged_rate']['rate']:.1%}) | {g['checked_distinct']} | "
                f"{g['distinct_mismatches']} = {m['rate']:.1%} | {_ci(m['ci95'])} | "
                f"{_ci(m['cluster_bootstrap']['ci95']) if m['k'] else 'n/a (0 events)'} | "
                f"{g['unchecked']} | {g['distinct_findings']} |")

    lines = ["Per run", "", head]
    for n in order:
        g = runs[n]
        what = g["label"] or ""
        if g["scope"] != "full":
            what = (what + "; " if what else "") + \
                f"**{g['scope']}; excluded from per-arm rates**"
        lines.append(row(n, g, what))
    lines += ["", "Per arm (full runs only)", "", head]
    for name, g in summary["arm"].items():
        lines.append(row(name, dict(g, arm=name, model=""),
                         "pooled: " + ", ".join(g["runs"])))
    for name, g in summary["arm_model"].items():
        arm, _, model = name.partition(":")
        lines.append(row(name, dict(g, arm=arm, model=model),
                         "pooled: " + ", ".join(g["runs"])))
    lines += ["", TABLE_NOTE]
    if comparisons:
        lines += ["", "Fine-tune run-to-run comparisons (difference = first "
                  "run minus second; cluster bootstrap on briefs, paired by "
                  "ticker)", "",
                  "| Comparison | What differs | Difference | Bootstrap 95% CI | "
                  "Bootstrap p (two-sided) | CI excludes 0 |",
                  "|---|---|---|---|---|---|"]
        what = {"lsnnc - v924f": "same BF16 model, different images (2026-09-05/06 vs 2026-09-23)",
                "r5nzh - v924f": "W4A16 vs BF16, same image, six days apart",
                "r5nzh - lsnnc": "W4A16 vs BF16, different images"}
        for key, d in comparisons.items():
            if not isinstance(d, dict):
                continue
            lines.append(f"| {key} | {what.get(key, '')} | {d['difference']:+.1%} | "
                         f"{_ci(d['ci95'], signed=True)} | {d['p_two_sided_bootstrap']} | "
                         f"{'yes' if d['excludes_zero'] else 'no'} |")
        lines += ["", comparisons["statement"]]
    return "\n".join(lines) + "\n"


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
    rows.sort(key=lambda r: (r["scope"] != "full", r["run"], r["ticker"],
                             r["section"], r["kind"], r["field"], r["stated"]))
    kept = _merge_verdicts(rows, path)
    for i, r in enumerate(rows, 1):
        r["id"] = i
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ADJ_FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return kept


def precision(rows: list[dict]) -> dict:
    """Adjudicated precision per run, per arm and per (arm, model) — arm and
    pooled figures over full runs only — two ways: OTHER_DEFECT counted as a
    true positive, and OTHER_DEFECT excluded from the denominator. The unit
    is a distinct finding (an adjudication row). Raises on any verdict
    outside VERDICTS."""
    bad = [(r["id"], r["verdict"]) for r in rows
           if r["verdict"].strip() and r["verdict"].strip() not in VERDICTS]
    if bad:
        raise ValueError(f"verdicts outside {VERDICTS}: {bad[:10]}")
    groups = defaultdict(Counter)
    for r in rows:
        v = r["verdict"].strip() or "UNLABELED"
        keys = [("run", r["run"])]
        if r["scope"] == "full":
            keys += [("arm", r["arm"]), ("arm_model", f"{r['arm']}:{r['model']}"),
                     ("all_full", "all_full")]
        for k in keys:
            groups[k][v] += 1
    out = {"run": {}, "arm": {}, "arm_model": {}}
    for (kind, name), c in sorted(groups.items()):
        tp, fp, od = c["TRUE_ERROR"], c["FALSE_POSITIVE"], c["OTHER_DEFECT"]
        res = {"rows": sum(c.values()), "unlabeled": c["UNLABELED"],
               "TRUE_ERROR": tp, "FALSE_POSITIVE": fp, "OTHER_DEFECT": od,
               "precision_other_defect_as_tp": _rate(tp + od, tp + fp + od),
               "precision_other_defect_excluded": _rate(tp, tp + fp)}
        if kind == "all_full":
            out["all_full"] = res
        else:
            out[kind][name] = res
    return out


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
    type with Wilson 95% CIs. Clean = the brief produced zero findings.
    Partial-run briefs take part: this measures the checker on brief text,
    not a flag rate."""
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


def _rel(p: Path) -> str:
    return str(p.resolve().relative_to(REPO)).replace("\\", "/")


def main():
    ap = argparse.ArgumentParser(description="Offline numeric-check backtest.")
    ap.add_argument("--raw-dir", default=str(RAW))
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", help="default eval/runs/numeric-backtest-<date>.json")
    ap.add_argument("--adjudication", default=str(ADJ_PATH))
    ap.add_argument("--precision", action="store_true",
                    help="report adjudicated precision from --adjudication")
    args = ap.parse_args()

    if args.precision:
        with open(args.adjudication, newline="", encoding="utf-8") as f:
            res = precision(list(csv.DictReader(f)))
        print(json.dumps(res, indent=2))
        return

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
    comparisons = fine_tune_comparisons(briefs)
    kept = write_adjudication(rows, Path(args.adjudication))

    result = {
        "date": args.date,
        "harness": "scripts/numeric_backtest.py",
        "check": "agent/numeric_check.py",
        "rel_tol": nc.DEFAULT_REL_TOL,
        "note": ("Flags are unadjudicated; a flag is an error only once a "
                 "human verdict says so (see adjudication.csv). Stock-field "
                 "numbers only; news and filing numbers are out of scope. "
                 "Partial runs are excluded from per-arm and pooled figures. "
                 "Not a number of record."),
        "files": len(files), "briefs": len(briefs), "skipped": skipped,
        "summary": summary,
        "crbu_assertion": crbu,
        "injection": recall,
        "fine_tune_comparisons": comparisons,
        "adjudication": {"path": _rel(Path(args.adjudication)),
                         "verdicts": list(VERDICTS),
                         "rows": len(rows), "verdicts_kept": kept},
    }
    out = Path(args.out) if args.out else \
        REPO / "eval" / "runs" / f"numeric-backtest-{args.date}.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8",
                   newline="\n")
    table = table_markdown(summary, comparisons)
    out.with_suffix(".md").write_text(
        f"# Numeric-check backtest, {args.date} (unadjudicated)\n\n"
        f"Generated by scripts/numeric_backtest.py; see {out.name}.\n\n"
        + table, encoding="utf-8", newline="\n")

    print(table)
    print(f"CRBU assertion: {crbu}")
    for kind, r in recall["by_type"].items():
        print(f"  inject {kind:12} {r['detected']:3}/{r['n']:3} "
              f"recall {r['recall']} CI {r['ci95']}")
    print(f"wrote {_rel(out)} (+ .md) and {len(rows)} adjudication rows "
          f"({kept} verdicts kept)")


if __name__ == "__main__":
    main()
