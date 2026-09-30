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
      one of VERDICTS, and a `note` column for the adjudicator. Re-running
      keeps verdicts and notes already entered (matched on run, ticker,
      section, kind, field, stated, sentence). The script never labels
      anything itself.

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
              "verdict", "note"]
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

# Fine-tune comparisons (difference = first minus second). r5nzh - v924f is
# the primary W4A16 comparison: same app image, WorkflowTemplate, eval-run
# parameters and vLLM args, only the weights' precision differs (see
# SAME_IMAGE_EVIDENCE). lsnnc - v924f (same BF16 weights, earlier image) shows
# what an image/pipeline change alone does to this metric. r5nzh - lsnnc
# mixes both and backs no claim.
FINE_TUNE_COMPARISONS = (("r5nzh", "v924f"), ("lsnnc", "v924f"),
                         ("r5nzh", "lsnnc"))
SAME_IMAGE_EVIDENCE = "eval/numeric_check/provenance-v924f-r5nzh.md"


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
    """The FINE_TUNE_COMPARISONS differences and their statements.

    Primary: r5nzh - v924f. Both ran the same app image, WorkflowTemplate,
    eval-run parameters and vLLM serving args; only the weights' precision
    (and the date) differ (evidence: SAME_IMAGE_EVIDENCE). lsnnc - v924f is
    reported on its own as evidence that pipeline/image changes also move
    this metric, not as noise that cancels the W4A16 effect. r5nzh - lsnnc
    confounds precision with image and is not used for any claim."""
    by_run = defaultdict(dict)
    for b in briefs:
        by_run[b["run"]][b["ticker"]] = b["counts"]
    out = {}
    for x, y in FINE_TUNE_COMPARISONS:
        if x in by_run and y in by_run:
            out[f"{x} - {y}"] = bootstrap_difference(by_run[x], by_run[y], draws)
    out["primary"] = "r5nzh - v924f"
    out["same_image_evidence"] = SAME_IMAGE_EVIDENCE

    def pts(v):
        return f"{v * 100:+.1f} pts"

    p = out.get("r5nzh - v924f")
    if p:
        ci = f"paired cluster bootstrap CI {pts(p['ci95'][0])[:-4]} to {pts(p['ci95'][1])}"
        out["statement"] = (
            f"W4A16 shows {pts(p['difference'])} section-level numeric mismatches "
            f"vs same-image BF16 ({ci}), on unadjudicated flags."
            if p["excludes_zero"] else
            f"W4A16 vs same-image BF16: {pts(p['difference'])} section-level "
            f"numeric mismatches ({ci}); the interval includes zero, so no "
            f"difference is shown, on unadjudicated flags.")
    i = out.get("lsnnc - v924f")
    if i:
        out["image_change_statement"] = (
            f"Separately, the same BF16 weights on an earlier image (lsnnc, "
            f"2026-09-05/06) sit {pts(i['difference'])} vs v924f (paired "
            f"cluster bootstrap CI {pts(i['ci95'][0])[:-4]} to "
            f"{pts(i['ci95'][1])}): pipeline/image changes also move this "
            f"metric. That is a second effect, not noise that cancels the "
            f"W4A16 one, which is measured within one image.")
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
                "occurrences": f["occurrences"], "verdict": "", "note": "",
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


# --- frozen-input replay (scripts/replay_sections.py) ------------------------
# Two labelled replays: the 3-sample "pilot" and the pre-registered
# 10-sample "replication" (eval/numeric_check/replication-plan.md). Every
# metric comes in two variants: "all" sections, and "no_trunc", which drops
# sections that hit the 512-token cap (vLLM finish_reason "length"); no_trunc
# is the replication's pre-registered primary metric.

LOCAL_SECTION_KEYS = {"financial-health", "risk-factors"}
REPLAY_ARMS = ("bf16", "w4a16")
REPLAY_LABELS = ("pilot", "replication")
VARIANTS = ("all", "no_trunc")
TOKEN_COUNTS = REPO / "eval" / "numeric_check" / "section-token-counts.json"
REPLICATION_SAMPLE = REPO / "eval" / "numeric_check" / "replication-sample.json"
SAMPLE_PER_ARM = 60
SAMPLE_SEED = 42


def _read_replay_file(path: Path) -> dict:
    """scripts/replay_sections.py's reader (stdlib-only at import)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "replay_sections", REPO / "scripts" / "replay_sections.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.read_replay_file(path)


def local_section_counts(report: dict, exclude: frozenset = frozenset()) -> tuple[int, int]:
    """(distinct mismatches, distinct checked numbers) restricted to the two
    sections the local model writes, minus any canonical section in
    `exclude`, so a live run compares like for like with a replay."""
    keep = lambda s: section_key(s) in LOCAL_SECTION_KEYS - exclude  # noqa: E731
    mism = {(f["section"], f["field"], f["stated"], f["sentence"])
            for f in report["findings"] if f["kind"] == "mismatch" and keep(f["section"])}
    chk = {(b["section"], b["field"], b["stated"], b["sentence"])
           for b in report["bindings"] if b["status"] == "checked" and keep(b["section"])}
    return len(mism), len(chk)


def load_token_counts(path: Path = TOKEN_COUNTS) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def live_truncated(tc: dict | None, run: str, ticker: str) -> frozenset:
    """Canonical sections of a live brief estimated to have hit the cap
    (scripts/section_token_counts.py)."""
    if not tc:
        return frozenset()
    counts = tc["live"].get(run, {}).get(ticker, {})
    return frozenset(k for k, v in counts.items() if v is not None and v >= tc["threshold"])


def find_replays() -> dict:
    """{label: latest eval/runs/replay-<label>-<date>/ directory}."""
    out = {}
    for label in REPLAY_LABELS:
        dirs = sorted(p for p in (REPO / "eval" / "runs").glob(f"replay-{label}-*") if p.is_dir())
        if dirs:
            out[label] = dirs[-1]
    return out


def _variant(report: dict) -> dict:
    distinct = _distinct(report["findings"])
    return {"report": report, "distinct": distinct,
            "counts": (sum(f["kind"] == "mismatch" for f in distinct),
                       _checked_distinct(report))}


def load_replay(replay_dir: Path, label: str) -> list[dict]:
    """Every <replay_dir>/<arm>/<T>-s<k>.md as a checked brief, in both
    variants (all sections; truncated sections dropped)."""
    out = []
    for arm in REPLAY_ARMS:
        for p in sorted((replay_dir / arm).glob("*-s*.md"), key=lambda p: p.name):
            r = _read_replay_file(p)
            m = r["meta"]
            finish = {name: m.get(f"{name.lower().replace(' ', '_')}_finish_reason")
                      for name, _ in r["sections"]}
            kept = [(n, t) for n, t in r["sections"] if finish[n] != "length"]
            out.append({
                "label": label, "replay": replay_dir.name, "arm": arm,
                "model": m["served_name"], "ticker": m["ticker"],
                "sample": int(m["sample"]), "sections": len(r["sections"]),
                "truncated": [n for n, _ in r["sections"] if finish[n] == "length"],
                "variants": {"all": _variant(nc.check_sections(r["sections"], r["stock"])),
                             "no_trunc": _variant(nc.check_sections(kept, r["stock"]))},
            })
    return out


def _sum_by_ticker(briefs: list[dict], counts_key=lambda b: b["counts"]) -> dict:
    by = defaultdict(lambda: [0, 0])
    for b in briefs:
        k, n = counts_key(b)
        by[b["ticker"]][0] += k
        by[b["ticker"]][1] += n
    return {t: tuple(v) for t, v in by.items()}


def _arm_metrics(bs: list[dict], variant: str, draws: int) -> dict:
    vs = [b["variants"][variant] for b in bs]
    k = sum(v["counts"][0] for v in vs)
    n = sum(v["counts"][1] for v in vs)
    checked = sum(v["report"]["checked"] for v in vs)
    unchecked = sum(v["report"]["unchecked"] for v in vs)
    per_sample = {}
    for s in sorted({b["sample"] for b in bs}):
        ss = [b["variants"][variant] for b in bs if b["sample"] == s]
        sk, sn = sum(v["counts"][0] for v in ss), sum(v["counts"][1] for v in ss)
        per_sample[f"s{s}"] = {"briefs_flagged": sum(bool(v["report"]["findings"]) for v in ss),
                               "mismatches": sk, "checked_distinct": sn,
                               "rate": round(sk / sn, 4) if sn else None}
    rates = [v["rate"] for v in per_sample.values() if v["rate"] is not None]
    rate = _rate(k, n)
    rate["cluster_bootstrap"] = cluster_bootstrap_ci(
        [list(_sum_by_ticker(bs, lambda b: b["variants"][variant]["counts"]).values())],
        draws=draws)
    rate["cluster_bootstrap"]["method"] += (
        f" (clusters: tickers, {len(per_sample)} samples each)")
    return {
        "model": bs[0]["model"], "briefs": len(bs), "tickers": len({b["ticker"] for b in bs}),
        "samples": len(per_sample),
        "briefs_flagged": sum(bool(v["report"]["findings"]) for v in vs),
        "checked": checked, "checked_distinct": n, "unchecked": unchecked,
        "coverage": round(checked / (checked + unchecked), 4) if checked + unchecked else None,
        "mismatches_per_checked": rate, "per_sample": per_sample,
        "sample_spread": {"min": min(rates), "max": max(rates),
                          "range": round(max(rates) - min(rates), 4)} if rates else None,
    }


def _gap(d: dict) -> str:
    return (f"W4A16 - BF16 = {100 * d['difference']:+.1f} pts (paired ticker-cluster "
            f"bootstrap CI {100 * d['ci95'][0]:+.1f} to {100 * d['ci95'][1]:+.1f} pts)")


def replication_statement(d: dict) -> str:
    """The pre-registered wording (replication-plan.md, "Decision rule")."""
    tail = ("on the replayed Financial Health + Risk Factors sections, truncated "
            "sections excluded, unadjudicated flags.")
    if d["excludes_zero"] and d["difference"] > 0:
        return f"The W4A16 regression replicates on identical inputs: {_gap(d)} {tail}"
    if d["excludes_zero"]:
        return f"On identical inputs W4A16 has fewer mismatches than BF16: {_gap(d)} {tail}"
    return f"The W4A16 regression does not replicate on identical inputs: {_gap(d)} {tail}"


def replay_analysis(label_briefs: dict, live_briefs: list[dict], tc: dict | None,
                    draws: int = BOOT_DRAWS) -> dict:
    """Per label (pilot, replication): truncation per arm, per-arm metrics and
    the paired W4A16 - BF16 difference in both variants, and statements; plus
    the like-for-like live difference (r5nzh - v924f, FH + RF only) with and
    without estimated-truncated sections, and live truncation per run."""
    out = {"labels": {}}
    for label, bs in label_briefs.items():
        if not bs:
            continue
        L = {"replay": bs[0]["replay"], "truncation": {}, "arms": {}, "difference": {}}
        for arm in REPLAY_ARMS:
            ab = [b for b in bs if b["arm"] == arm]
            if not ab:
                continue
            t = sum(len(b["truncated"]) for b in ab)
            s = sum(b["sections"] for b in ab)
            L["truncation"][arm] = {"sections": s, "truncated": t, "rate": round(t / s, 4)}
            L["arms"].setdefault("all", {})[arm] = _arm_metrics(ab, "all", draws)
            L["arms"].setdefault("no_trunc", {})[arm] = _arm_metrics(ab, "no_trunc", draws)
        if set(REPLAY_ARMS) <= set(L["truncation"]):
            for v in VARIANTS:
                w = _sum_by_ticker([b for b in bs if b["arm"] == "w4a16"],
                                   lambda b, v=v: b["variants"][v]["counts"])
                f = _sum_by_ticker([b for b in bs if b["arm"] == "bf16"],
                                   lambda b, v=v: b["variants"][v]["counts"])
                L["difference"][v] = bootstrap_difference(w, f, draws)
        out["labels"][label] = L

    live_runs = ("r5nzh", "v924f")
    live = {}
    for v in VARIANTS:
        live[v] = {r: _sum_by_ticker(
            [b for b in live_briefs if b["run"] == r],
            lambda b, v=v: local_section_counts(
                b["report"], live_truncated(tc, b["run"], b["ticker"]) if v == "no_trunc"
                else frozenset()))
            for r in live_runs}
    if all(live["all"].values()):
        out["live"] = {
            "difference": {v: bootstrap_difference(live[v]["r5nzh"], live[v]["v924f"], draws)
                           for v in VARIANTS if tc or v == "all"},
            "rates": {v: {r: _rate(sum(x[0] for x in live[v][r].values()),
                                   sum(x[1] for x in live[v][r].values()))
                          for r in live_runs}
                      for v in VARIANTS if tc or v == "all"},
        }
    if tc:
        out["live_truncation"] = {
            run: {"sections": sum(len(d) for d in t.values()),
                  "unknown": sum(x is None for d in t.values() for x in d.values()),
                  "truncated_est": sum(x is not None and x >= tc["threshold"]
                                       for d in t.values() for x in d.values())}
            for run, t in tc["live"].items()}
        out["truncation_method"] = {"threshold": tc["threshold"], "cap": tc["cap"],
                                    "validation_on_pilot": tc["validation_on_pilot"]}

    P = out["labels"].get("pilot")
    if P and P["difference"]:
        d, dn = P["difference"]["all"], P["difference"]["no_trunc"]
        P["statement"] = (
            f"Pilot: the live-run gap is not reproduced on identical inputs "
            f"({_gap(d)} on the replayed Financial Health + Risk Factors "
            f"sections, unadjudicated flags) and may reflect input drift."
            if not (d["excludes_zero"] and d["difference"] > 0) else
            f"Pilot: the regression reproduces on identical inputs: {_gap(d)} on "
            f"the replayed Financial Health + Risk Factors sections, on "
            f"unadjudicated flags.")
        extra = [f"With truncated sections excluded, the pilot gap is {_gap(dn)}."]
        lv = out.get("live", {}).get("difference", {}).get("all")
        if lv and d["ci95"][0] <= lv["difference"] <= d["ci95"][1]:
            extra.append(f"The pilot interval also contains the like-for-like live gap "
                         f"({100 * lv['difference']:+.1f} pts), so the pilot neither "
                         f"confirms nor excludes it.")
        rates = out.get("live", {}).get("rates", {}).get("all", {})
        bf = P["arms"]["all"].get("bf16")
        if bf and "v924f" in rates:
            ps = " / ".join(f"{v['rate']:.1%}" for v in bf["per_sample"].values())
            extra.append(
                f"Same weights, same inputs: replayed BF16 gives "
                f"{bf['mismatches_per_checked']['rate']:.1%} (samples {ps}) against "
                f"v924f's single live draw of {rates['v924f']['rate']:.1%} on these "
                f"sections, so sampling alone moves this rate by that much, which a "
                f"one-draw-per-ticker live comparison cannot separate from precision.")
        P["context_statements"] = extra
    R = out["labels"].get("replication")
    if R and R["difference"]:
        R["statement"] = replication_statement(R["difference"]["no_trunc"])
        R["secondary_statement"] = (
            f"Secondary (all sections, truncated included): {_gap(R['difference']['all'])}.")
    return out


# --- replication adjudication sample -------------------------------------------

def _row(b: dict, f: dict, scope: str) -> dict:
    return {
        "run": f"{b['replay']}/{b['arm']}/s{b['sample']}", "scope": scope,
        "arm": b["arm"], "model": b["model"], "ticker": b["ticker"],
        "section": f["section"], "kind": f["kind"], "field": f["field"] or "",
        "sentence": f["sentence"], "stated": f["stated"],
        "source": "" if f["source"] is None else f["source"],
        "ratio": "" if f["ratio"] is None else f"{f['ratio']:.4g}",
        "occurrences": f["occurrences"], "verdict": "", "note": "",
    }


def _allocate(sizes: dict, total: int) -> dict:
    """Proportional allocation with largest remainders; all rows if the
    frame is smaller than `total`."""
    n = sum(sizes.values())
    if n <= total:
        return dict(sizes)
    quotas = {k: total * v / n for k, v in sizes.items()}
    alloc = {k: int(q) for k, q in quotas.items()}
    for k in sorted(quotas, key=lambda k: (-(quotas[k] - alloc[k]), k))[:total - sum(alloc.values())]:
        alloc[k] += 1
    return alloc


def replication_sample(briefs: list[dict], per_arm: int = SAMPLE_PER_ARM,
                       seed: int = SAMPLE_SEED) -> tuple[list[dict], dict]:
    """The pre-registered adjudication sample: per arm, `per_arm` mismatch
    rows from the primary metric's flags (truncated sections excluded),
    stratified by field with proportional allocation, drawn with
    random.Random(seed) per arm over a deterministically ordered frame.
    Returns (rows, record)."""
    rows, record = [], {"per_arm": per_arm, "seed": seed, "stratified_by": "field",
                        "frame": "distinct mismatch findings, truncated sections excluded",
                        "arms": {}}
    for arm in REPLAY_ARMS:
        frame = sorted(
            (_row(b, f, "replication") for b in briefs if b["arm"] == arm
             for f in b["variants"]["no_trunc"]["distinct"] if f["kind"] == "mismatch"),
            key=lambda r: (r["ticker"], r["run"], r["section"], r["field"], r["stated"], r["sentence"]))
        strata = defaultdict(list)
        for r in frame:
            strata[r["field"]].append(r)
        alloc = _allocate({k: len(v) for k, v in strata.items()}, per_arm)
        rng = random.Random(seed)
        picked = []
        for field in sorted(strata):
            picked += rng.sample(strata[field], alloc[field])
        rows += picked
        record["arms"][arm] = {
            "flags": len(frame),
            "checked_distinct": sum(b["variants"]["no_trunc"]["counts"][1]
                                    for b in briefs if b["arm"] == arm),
            "population_by_field": {k: len(v) for k, v in sorted(strata.items())},
            "allocation_by_field": dict(sorted(alloc.items())),
            "sampled": len(picked),
            "sampled_keys": [[r[k] for k in _ADJ_KEY] for r in picked],
        }
    return rows, record


def replication_applied_precision(rows: list[dict], record: dict) -> dict:
    """Per arm: stratum-weighted precision from the labelled sample (two
    ways), applied to the replication's primary flag count and rate; the
    sample size is stated. Strata without a label contribute nothing and are
    listed."""
    out = {}
    for arm, rec in record["arms"].items():
        labelled = [r for r in rows if r["scope"] == "replication" and r["arm"] == arm
                    and r["verdict"].strip()]
        pop = rec["population_by_field"]
        res = {"sample_size": rec["sampled"], "labelled": len(labelled),
               "flags": rec["flags"]}
        for mode in ("other_defect_as_tp", "other_defect_excluded"):
            num = den = 0.0
            missing = []
            for field, n_h in pop.items():
                lab = [r["verdict"].strip() for r in labelled if r["field"] == field]
                tp = lab.count("TRUE_ERROR") + (lab.count("OTHER_DEFECT") if mode == "other_defect_as_tp" else 0)
                d = tp + lab.count("FALSE_POSITIVE") + (lab.count("OTHER_DEFECT") if mode == "other_defect_as_tp" else 0)
                if d:
                    num += n_h * tp / d
                    den += n_h
                else:
                    missing.append(field)
            p = num / den if den else None
            lab_all = [r["verdict"].strip() for r in labelled]
            tp_all = lab_all.count("TRUE_ERROR") + (lab_all.count("OTHER_DEFECT") if mode == "other_defect_as_tp" else 0)
            d_all = tp_all + lab_all.count("FALSE_POSITIVE") + (lab_all.count("OTHER_DEFECT") if mode == "other_defect_as_tp" else 0)
            entry = {"precision_weighted": round(p, 4) if p is not None else None,
                     "sample_unweighted": _rate(tp_all, d_all),
                     "strata_without_labels": missing}
            if p is not None:
                k, n = rec["flags"], rec["checked_distinct"]
                entry["estimated_true_mismatches"] = round(p * k, 1)
                entry["adjusted_rate"] = round(p * k / n, 4) if n else None
            res[mode] = entry
        out[arm] = res
    return out


def replay_markdown(rep: dict, applied: dict | None = None) -> list[str]:
    lines = []
    if rep.get("live_truncation") or any(L["truncation"] for L in rep["labels"].values()):
        lines += ["", "Truncation at the 512-token cap (sections whose generation hit "
                  "max_tokens): replays from vLLM's recorded finish_reason; live runs "
                  "estimated by re-tokenizing the saved section text "
                  "(scripts/section_token_counts.py)", "",
                  "| Source | Arm / run | Sections | Truncated | Rate |", "|---|---|---|---|---|"]
        for label, L in rep["labels"].items():
            for arm, t in L["truncation"].items():
                lines.append(f"| {label} (exact) | {arm} | {t['sections']} | {t['truncated']} | {t['rate']:.1%} |")
        for run, t in rep.get("live_truncation", {}).items():
            known = t["sections"] - t["unknown"]
            unk = f" ({t['unknown']} not located)" if t["unknown"] else ""
            lines.append(f"| live (estimated) | {run} | {t['sections']}{unk} | "
                         f"{t['truncated_est']} | {t['truncated_est'] / known:.1%} |")
        tm = rep.get("truncation_method")
        if tm:
            v = tm["validation_on_pilot"]
            lines += ["", f"Estimation check on the pilot's {v['sections']} sections: "
                      f"re-tokenized counts equal vLLM's recorded counts for "
                      f"{v['exact_count_matches']} (largest difference {v['max_abs_diff']} "
                      f"tokens); the >= {v['threshold']}-token rule agrees with "
                      f"finish_reason for {v['threshold_agrees_with_finish_reason']}."]

    head = ("| Arm | Variant | Served model | Briefs (tickers x samples) | Briefs flagged | "
            "Checked (distinct) | Coverage | Mismatches per checked number | "
            "Wilson 95% CI (naive, too narrow) | Cluster bootstrap 95% CI (tickers) | "
            "Per-sample rate range | Spread (max - min) |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|---|")
    diff_head = ("| Comparison | Difference | Bootstrap 95% CI | Bootstrap p (two-sided) | CI excludes 0 |\n"
                 "|---|---|---|---|---|")
    vname = {"all": "all sections", "no_trunc": "truncated excluded"}

    def drow(label, d):
        return (f"| {label} | {100 * d['difference']:+.1f} pts | "
                f"{100 * d['ci95'][0]:+.1f} to {100 * d['ci95'][1]:+.1f} pts | "
                f"{d['p_two_sided_bootstrap']} | {'yes' if d['excludes_zero'] else 'no'} |")

    titles = {
        "pilot": "Pilot frozen-input replay ({}): 3 seeded samples per ticker per arm "
                 "(seed base 42), exploratory",
        "replication": "Pre-registered replication ({}): 10 seeded samples per ticker per "
                       "arm (seed base 1000000, disjoint from the pilot); plan: "
                       "eval/numeric_check/replication-plan.md; primary metric: "
                       "mismatches per checked number, truncated sections excluded",
    }
    for label, L in rep["labels"].items():
        lines += ["", titles[label].format(L["replay"]) + ". Financial Health and Risk "
                  "Factors regenerated from v924f's recorded contexts with the pipeline's "
                  "own prompts, same seeds in both arms (scripts/replay_sections.py).", "", head]
        for v in VARIANTS:
            for arm, a in L["arms"].get(v, {}).items():
                m = a["mismatches_per_checked"]
                sp = a["sample_spread"]
                lines.append(
                    f"| {arm} | {vname[v]} | {a['model']} | {a['briefs']} ({a['tickers']} x "
                    f"{a['samples']}) | {a['briefs_flagged']} | {a['checked_distinct']} | "
                    f"{a['coverage']:.1%} | {m['k']} = {m['rate']:.1%} | {_ci(m['ci95'])} | "
                    f"{_ci(m['cluster_bootstrap']['ci95']) if m['k'] else 'n/a (0 events)'} | "
                    f"{sp['min']:.1%}–{sp['max']:.1%} | {100 * sp['range']:.1f} pts |")
        lines += ["", diff_head]
        for v in VARIANTS:
            if v in L["difference"]:
                lines.append(drow(f"{label}: W4A16 - BF16, {vname[v]}", L["difference"][v]))
        for s in [L.get("statement"), L.get("secondary_statement"), *L.get("context_statements", [])]:
            if s:
                lines += ["", s]
        if label == "replication" and applied:
            lines += ["", "Adjudication sample (pre-registered): per arm, "
                      f"{SAMPLE_PER_ARM} of the primary metric's mismatch flags, stratified by "
                      f"field, seed {SAMPLE_SEED}. Stratum-weighted precision is applied to "
                      "that arm's flag count.", "",
                      "| Arm | Flags | Sample size | Labelled | Precision, OTHER_DEFECT as TP | "
                      "Precision, OTHER_DEFECT excluded | Adjusted rate (as TP / excluded) |",
                      "|---|---|---|---|---|---|---|"]
            for arm, a in applied.items():
                t, x = a["other_defect_as_tp"], a["other_defect_excluded"]
                f = lambda e: "pending" if e["precision_weighted"] is None else f"{e['precision_weighted']:.1%}"  # noqa: E731
                adj = ("pending" if t.get("adjusted_rate") is None else
                       f"{t['adjusted_rate']:.1%} / {x['adjusted_rate']:.1%}")
                lines.append(f"| {arm} | {a['flags']} | {a['sample_size']} | {a['labelled']} | "
                             f"{f(t)} | {f(x)} | {adj} |")

    live = rep.get("live")
    if live:
        lines += ["", "Live, like for like (one draw per ticker; FH + RF only)", "", diff_head]
        for v, d in live["difference"].items():
            name = vname[v] + (" (estimated)" if v == "no_trunc" else "")
            lines.append(drow(f"live: r5nzh - v924f, {name}", d))
        for v, rates in live["rates"].items():
            lines += ["", f"Live FH + RF rates, {vname[v]}: " + "; ".join(
                f"{r} {x['k']}/{x['n']} = {x['rate']:.1%}" for r, x in rates.items()) + "."]
    lines += ["", "The live-run rows further up also count the hosted Exec Summary and "
              "Outlook, which restate the local sections' figures; the replays "
              "regenerate only the two local sections, so their like-for-like live "
              "comparison is the FH + RF block above."]
    return lines


def _pct(r: dict) -> str:
    return f"{r['rate']:.1%} ({r['ci95'][0]:.1%}–{r['ci95'][1]:.1%})"


def _ci(ci: list[float]) -> str:
    return f"{ci[0]:.1%}–{ci[1]:.1%}"


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


def table_markdown(summary: dict, comparisons: dict | None = None,
                   replay: dict | None = None, applied: dict | None = None) -> str:
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
        lines += ["", "Fine-tune comparisons (difference = first run minus "
                  "second; cluster bootstrap on briefs, paired by ticker)", "",
                  "| Comparison | What differs | Difference | Bootstrap 95% CI | "
                  "Bootstrap p (two-sided) | CI excludes 0 |",
                  "|---|---|---|---|---|---|"]
        what = {"r5nzh - v924f": "**primary**: W4A16 vs BF16, same image, "
                                 "template and serving args, six days apart",
                "lsnnc - v924f": "same BF16 weights, earlier image (2026-09-05/06 "
                                 "vs 2026-09-23): the image/pipeline effect",
                "r5nzh - lsnnc": "precision and image both differ: confounded, "
                                 "backs no claim"}
        for key, d in comparisons.items():
            if not isinstance(d, dict):
                continue
            lo, hi = (100 * v for v in d["ci95"])
            lines.append(f"| {key} | {what.get(key, '')} | "
                         f"{100 * d['difference']:+.1f} pts | "
                         f"{lo:+.1f} to {hi:+.1f} pts | {d['p_two_sided_bootstrap']} | "
                         f"{'yes' if d['excludes_zero'] else 'no'} |")
        lines += ["", comparisons["statement"], "",
                  comparisons.get("image_change_statement", ""), "",
                  f"Same-image evidence: {comparisons['same_image_evidence']}."]
    if replay and replay.get("labels"):
        lines += replay_markdown(replay, applied)
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
    """Carry verdicts (and adjudicator notes) already entered in an existing
    adjudication file over to the regenerated rows. Returns how many
    verdicts were kept."""
    if not path.exists():
        return 0
    with open(path, newline="", encoding="utf-8") as f:
        old = {tuple(r[k] for k in _ADJ_KEY): (r.get("verdict", ""), r.get("note") or "")
               for r in csv.DictReader(f)}
    kept = 0
    for r in rows:
        v, note = old.get(tuple(str(r[k]) for k in _ADJ_KEY), ("", ""))
        r["note"] = note
        if v.strip():
            r["verdict"] = v
            kept += 1
    return kept


def write_adjudication(rows: list[dict], path: Path) -> int:
    order = {"full": 0, "partial": 1, "replication": 2}
    rows.sort(key=lambda r: (order.get(r["scope"], 3), r["run"], r["ticker"],
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
        elif r["scope"] == "replication":
            keys += [("replication", f"{r['run'].split('/')[0]}:{r['arm']}")]
        for k in keys:
            groups[k][v] += 1
    out = {"run": {}, "arm": {}, "arm_model": {}, "replication": {}}
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
            adj_rows = list(csv.DictReader(f))
        res = precision(adj_rows)
        if REPLICATION_SAMPLE.exists():
            res["replication_applied"] = replication_applied_precision(
                adj_rows, json.loads(REPLICATION_SAMPLE.read_text(encoding="utf-8")))
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
    replay = applied = None
    replays = find_replays()
    if replays:
        label_briefs = {label: load_replay(d, label) for label, d in replays.items()}
        replay = replay_analysis(label_briefs, briefs, load_token_counts())
        if label_briefs.get("replication"):
            srows, record = replication_sample(label_briefs["replication"])
            rows += srows
            REPLICATION_SAMPLE.write_text(json.dumps(record, indent=2) + "\n",
                                          encoding="utf-8", newline="\n")
    kept = write_adjudication(rows, Path(args.adjudication))
    if REPLICATION_SAMPLE.exists() and replay and "replication" in replay["labels"]:
        with open(args.adjudication, newline="", encoding="utf-8") as f:
            applied = replication_applied_precision(
                list(csv.DictReader(f)),
                json.loads(REPLICATION_SAMPLE.read_text(encoding="utf-8")))

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
        "replay": replay,
        "replication_applied_precision": applied,
        "adjudication": {"path": _rel(Path(args.adjudication)),
                         "verdicts": list(VERDICTS),
                         "rows": len(rows), "verdicts_kept": kept},
    }
    out = Path(args.out) if args.out else \
        REPO / "eval" / "runs" / f"numeric-backtest-{args.date}.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8",
                   newline="\n")
    table = table_markdown(summary, comparisons, replay, applied)
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
