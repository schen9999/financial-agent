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


# --- frozen-input replay (scripts/replay_sections.py) ------------------------

LOCAL_SECTION_KEYS = {"financial-health", "risk-factors"}
REPLAY_ARMS = ("bf16", "w4a16")


def _read_replay_file(path: Path) -> dict:
    """scripts/replay_sections.py's reader (stdlib-only at import)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "replay_sections", REPO / "scripts" / "replay_sections.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.read_replay_file(path)


def local_section_counts(report: dict) -> tuple[int, int]:
    """(distinct mismatches, distinct checked numbers) restricted to the two
    sections the local model writes, so a live run compares like for like
    with a replay (which regenerates only those two)."""
    keep = lambda s: section_key(s) in LOCAL_SECTION_KEYS  # noqa: E731
    mism = {(f["section"], f["field"], f["stated"], f["sentence"])
            for f in report["findings"] if f["kind"] == "mismatch" and keep(f["section"])}
    chk = {(b["section"], b["field"], b["stated"], b["sentence"])
           for b in report["bindings"] if b["status"] == "checked" and keep(b["section"])}
    return len(mism), len(chk)


def load_replay(replay_dir: Path) -> list[dict]:
    """Every <replay_dir>/<arm>/<T>-s<k>.md as a checked brief."""
    out = []
    for arm in REPLAY_ARMS:
        for p in sorted((replay_dir / arm).glob("*-s*.md"), key=lambda p: p.name):
            r = _read_replay_file(p)
            m = r["meta"]
            report = nc.check_sections(r["sections"], r["stock"])
            distinct = _distinct(report["findings"])
            out.append({
                "replay": replay_dir.name, "arm": arm, "model": m["served_name"],
                "ticker": m["ticker"], "sample": int(m["sample"]),
                "report": report, "distinct": distinct,
                "counts": (sum(f["kind"] == "mismatch" for f in distinct),
                           _checked_distinct(report)),
            })
    return out


def _sum_by_ticker(briefs: list[dict], counts_key=lambda b: b["counts"]) -> dict:
    by = defaultdict(lambda: [0, 0])
    for b in briefs:
        k, n = counts_key(b)
        by[b["ticker"]][0] += k
        by[b["ticker"]][1] += n
    return {t: tuple(v) for t, v in by.items()}


def replay_analysis(replay_briefs: list[dict], live_briefs: list[dict],
                    draws: int = BOOT_DRAWS) -> dict:
    """Per-arm replay metrics, the within-arm spread over samples, the paired
    (by ticker) W4A16 - BF16 difference, the like-for-like live difference
    (r5nzh - v924f on Financial Health + Risk Factors only) and the
    generated statement."""
    out = {"replay": replay_briefs[0]["replay"] if replay_briefs else None,
           "arms": {}}
    for arm in REPLAY_ARMS:
        bs = [b for b in replay_briefs if b["arm"] == arm]
        if not bs:
            continue
        k = sum(b["counts"][0] for b in bs)
        n = sum(b["counts"][1] for b in bs)
        checked = sum(b["report"]["checked"] for b in bs)
        unchecked = sum(b["report"]["unchecked"] for b in bs)
        per_sample = {}
        for s in sorted({b["sample"] for b in bs}):
            ss = [b for b in bs if b["sample"] == s]
            sk, sn = sum(b["counts"][0] for b in ss), sum(b["counts"][1] for b in ss)
            per_sample[f"s{s}"] = {"briefs": len(ss),
                                   "briefs_flagged": sum(bool(b["report"]["findings"]) for b in ss),
                                   "mismatches": sk, "checked_distinct": sn,
                                   "rate": round(sk / sn, 4) if sn else None}
        rates = [v["rate"] for v in per_sample.values() if v["rate"] is not None]
        rate = _rate(k, n)
        rate["cluster_bootstrap"] = cluster_bootstrap_ci(
            [list(_sum_by_ticker(bs).values())], draws=draws)
        rate["cluster_bootstrap"]["method"] += " (clusters: tickers, 3 samples each)"
        out["arms"][arm] = {
            "model": bs[0]["model"], "briefs": len(bs),
            "tickers": len({b["ticker"] for b in bs}),
            "briefs_flagged": sum(bool(b["report"]["findings"]) for b in bs),
            "checked": checked, "checked_distinct": n, "unchecked": unchecked,
            "coverage": round(checked / (checked + unchecked), 4) if checked + unchecked else None,
            "mismatches_per_checked": rate,
            "per_sample": per_sample,
            "sample_spread": {"min": min(rates), "max": max(rates),
                              "range": round(max(rates) - min(rates), 4)} if rates else None,
        }
    if set(REPLAY_ARMS) <= set(out["arms"]):
        w = _sum_by_ticker([b for b in replay_briefs if b["arm"] == "w4a16"])
        f = _sum_by_ticker([b for b in replay_briefs if b["arm"] == "bf16"])
        out["difference_w4a16_minus_bf16"] = bootstrap_difference(w, f, draws)
    live = {r: _sum_by_ticker([b for b in live_briefs if b["run"] == r],
                              lambda b: local_section_counts(b["report"]))
            for r in ("r5nzh", "v924f")}
    if all(live.values()):
        out["live_fh_rf_r5nzh_minus_v924f"] = bootstrap_difference(
            live["r5nzh"], live["v924f"], draws)
        out["live_fh_rf_rates"] = {
            r: _rate(sum(v[0] for v in live[r].values()), sum(v[1] for v in live[r].values()))
            for r in live}
    d = out.get("difference_w4a16_minus_bf16")
    if d:
        ci = f"paired cluster bootstrap CI {100 * d['ci95'][0]:+.1f} to {100 * d['ci95'][1]:+.1f} pts"
        diff = f"W4A16 - BF16 = {100 * d['difference']:+.1f} pts ({ci})"
        if d["excludes_zero"] and d["difference"] > 0:
            out["statement"] = (
                f"The regression reproduces on identical inputs: {diff} on the "
                f"replayed Financial Health + Risk Factors sections, on "
                f"unadjudicated flags.")
        else:
            out["statement"] = (
                f"The live-run gap is not reproduced on identical inputs "
                f"({diff} on the replayed Financial Health + Risk Factors "
                f"sections, unadjudicated flags) and may reflect input drift.")
        # Context, also generated from the numbers.
        extra = []
        lv = out.get("live_fh_rf_r5nzh_minus_v924f")
        if lv and d["ci95"][0] <= lv["difference"] <= d["ci95"][1]:
            extra.append(
                f"The replay interval also contains the like-for-like live gap "
                f"({100 * lv['difference']:+.1f} pts), so the replay neither "
                f"confirms nor excludes it.")
        rates = out.get("live_fh_rf_rates", {})
        bf = out["arms"].get("bf16")
        if bf and "v924f" in rates:
            ps = " / ".join(f"{v['rate']:.1%}" for v in bf["per_sample"].values())
            extra.append(
                f"Same weights, same inputs: replayed BF16 gives "
                f"{bf['mismatches_per_checked']['rate']:.1%} (samples {ps}) "
                f"against v924f's single live draw of {rates['v924f']['rate']:.1%} "
                f"on these sections, so sampling alone moves this rate by that "
                f"much, which a one-draw-per-ticker live comparison cannot "
                f"separate from precision.")
        out["context_statements"] = extra
    return out


def replay_rows(replay_briefs: list[dict]) -> list[dict]:
    """Adjudication rows for replay findings, scope=replay."""
    rows = []
    for b in replay_briefs:
        for f in b["distinct"]:
            rows.append({
                "run": f"{b['replay']}/{b['arm']}/s{b['sample']}", "scope": "replay",
                "arm": b["arm"], "model": b["model"], "ticker": b["ticker"],
                "section": f["section"], "kind": f["kind"],
                "field": f["field"] or "", "sentence": f["sentence"],
                "stated": f["stated"],
                "source": "" if f["source"] is None else f["source"],
                "ratio": "" if f["ratio"] is None else f"{f['ratio']:.4g}",
                "occurrences": f["occurrences"], "verdict": "",
            })
    return rows


def replay_markdown(rep: dict) -> list[str]:
    lines = ["", f"Frozen-input replay ({rep['replay']}): the two local sections "
             "(Financial Health, Risk Factors) regenerated from v924f's recorded "
             "contexts with the pipeline's own prompts, 3 seeded samples per "
             "ticker per arm, same seeds in both arms (scripts/replay_sections.py)",
             "",
             "| Arm | Served model | Briefs (tickers x samples) | Briefs flagged | "
             "Checked (distinct) | Coverage | Mismatches per checked number | "
             "Wilson 95% CI (naive, too narrow) | Cluster bootstrap 95% CI (tickers) | "
             "Per-sample rates (s1 / s2 / s3) | Spread (max - min) |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for arm, a in rep["arms"].items():
        m = a["mismatches_per_checked"]
        ps = " / ".join(f"{v['rate']:.1%}" for v in a["per_sample"].values())
        sp = a["sample_spread"]
        lines.append(
            f"| {arm} | {a['model']} | {a['briefs']} ({a['tickers']} x "
            f"{len(a['per_sample'])}) | {a['briefs_flagged']} | {a['checked_distinct']} | "
            f"{a['coverage']:.1%} | {m['k']} = {m['rate']:.1%} | {_ci(m['ci95'])} | "
            f"{_ci(m['cluster_bootstrap']['ci95']) if m['k'] else 'n/a (0 events)'} | "
            f"{ps} | {100 * sp['range']:.1f} pts |")
    lines += ["", "| Comparison | Difference | Bootstrap 95% CI | Bootstrap p (two-sided) | CI excludes 0 |",
              "|---|---|---|---|---|"]
    for key, label in (("difference_w4a16_minus_bf16", "replay: W4A16 - BF16, identical inputs"),
                       ("live_fh_rf_r5nzh_minus_v924f",
                        "live, like for like: r5nzh - v924f, Financial Health + Risk Factors only")):
        d = rep.get(key)
        if d:
            lines.append(f"| {label} | {100 * d['difference']:+.1f} pts | "
                         f"{100 * d['ci95'][0]:+.1f} to {100 * d['ci95'][1]:+.1f} pts | "
                         f"{d['p_two_sided_bootstrap']} | {'yes' if d['excludes_zero'] else 'no'} |")
    if rep.get("statement"):
        lines += ["", rep["statement"]]
    for s in rep.get("context_statements", []):
        lines += ["", s]
    rates = rep.get("live_fh_rf_rates")
    if rates:
        lines += ["", "Live Financial Health + Risk Factors rates (one draw per "
                  "ticker): " + "; ".join(
                      f"{r} {v['k']}/{v['n']} = {v['rate']:.1%}" for r, v in rates.items()) + "."]
    lines += ["", "The live-run rows above also count the hosted Exec Summary and "
              "Outlook, which restate the local sections' figures; the replay "
              "regenerates only the two local sections, so its like-for-like "
              "live comparison is the Financial Health + Risk Factors row."]
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
                   replay: dict | None = None) -> str:
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
    if replay and replay.get("arms"):
        lines += replay_markdown(replay)
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
    order = {"full": 0, "partial": 1, "replay": 2}
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
        elif r["scope"] == "replay":
            keys += [("replay", f"{r['run'].split('/')[0]}:{r['arm']}")]
        for k in keys:
            groups[k][v] += 1
    out = {"run": {}, "arm": {}, "arm_model": {}, "replay": {}}
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
    ap.add_argument("--replay-dir", help="default: the latest eval/runs/replay-*")
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
    replay = None
    replay_dirs = sorted(p for p in (REPO / "eval" / "runs").glob("replay-*") if p.is_dir())
    if args.replay_dir or replay_dirs:
        rdir = Path(args.replay_dir) if args.replay_dir else replay_dirs[-1]
        rbriefs = load_replay(rdir)
        replay = replay_analysis(rbriefs, briefs)
        rows += replay_rows(rbriefs)
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
        "replay": replay,
        "adjudication": {"path": _rel(Path(args.adjudication)),
                         "verdicts": list(VERDICTS),
                         "rows": len(rows), "verdicts_kept": kept},
    }
    out = Path(args.out) if args.out else \
        REPO / "eval" / "runs" / f"numeric-backtest-{args.date}.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8",
                   newline="\n")
    table = table_markdown(summary, comparisons, replay)
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
