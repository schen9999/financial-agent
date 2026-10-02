#!/usr/bin/env python3
"""Adjudicated numeric-check results: what the verdicts change.

Reads the committed verdicts in eval/numeric_check/adjudication.csv and
never writes them (nor replication-sample.json). Rebuilds every flag the way
scripts/numeric_backtest.py does (same raw files, same check, same distinct
keys), asserts that each live flag has exactly one verdict and that the
replication frame matches the registered sample record, then reports:

1. Precision per run, per arm and per (arm, model), two ways (OTHER_DEFECT
   as a true positive, and excluded), with Wilson 95% CIs and a brief-level
   cluster bootstrap (flags in one brief share a model output and a stock
   dict). Replication: the pre-registered stratum-weighted precision
   (numeric_backtest.replication_applied_precision, unchanged since
   registration) with the sample size, the strata without labels, and a
   within-stratum bootstrap.
2. Adjudicator notes: the doubt-note count (rule 8) and every note.
3. Mismatch rates on TRUE_ERROR flags only: per run / arm / (arm, model)
   and hosted vs local-model; the live same-image gap r5nzh - v924f on
   Financial Health + Risk Factors; the replication's primary gap with
   adjudication-adjusted counts (secondary: the pre-registered result on
   unadjudicated flags stays the primary result).
4. TRUE_ERRORs that trace to the two upstream data findings
   (eval/numeric_check/upstream-findings.md), per arm, hosted included.

Nothing here is a number of record.

Usage:
  python scripts/numeric_adjudicated.py [--date 2026-10-01]
"""
import argparse
import csv
import datetime
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from eval.numeric_check.label_cli import has_doubt  # noqa: E402
from scripts import numeric_backtest as nb  # noqa: E402

TE, FP, OD = nb.VERDICTS
MODES = ("other_defect_as_tp", "other_defect_excluded")
# Upstream finding (a): revenue/net_income in the filer's home currency,
# labelled USD. SAP is left out: EUR and USD are within 2x, so a 10x gap is
# the brief's own error (upstream-findings.md).
CURRENCY_TICKERS = {"TM", "TSM", "NVO", "BABA"}
CURRENCY_FIELDS = {"revenue", "net_income"}
LIVE_GAP = ("r5nzh", "v924f")


# --- classification --------------------------------------------------------------

def pow10(ratio) -> int | None:
    """The integer e when |ratio| is within ~2.3% of 10**e, else None."""
    try:
        x = abs(float(ratio))
    except (TypeError, ValueError):
        return None
    if not x:
        return None
    lg = math.log10(x)
    e = round(lg)
    return e if abs(lg - e) < 0.01 else None


def upstream_cause(r: dict) -> str | None:
    """'currency' or 'margin_fraction' when a TRUE_ERROR mismatch is the
    upstream defect showing through, by a fixed mechanical rule:
    currency: TM/TSM/NVO/BABA revenue or net_income whose stated figure is a
      power-of-ten rescaling (not 10**0) of the mislabelled home-currency
      source, i.e. built from the mislabelled number;
    margin_fraction: profit_margin with |source| > 1 stated at ratio ~0.01,
      the raw fraction written as a percent."""
    if r["verdict"].strip() != TE or r["kind"] != "mismatch":
        return None
    e = pow10(r["ratio"])
    if r["ticker"] in CURRENCY_TICKERS and r["field"] in CURRENCY_FIELDS:
        return "currency" if e not in (None, 0) else None
    if r["field"] == "profit_margin" and _abs_source(r) > 1 and e == -2:
        return "margin_fraction"
    return None


def upstream_adjacent(r: dict) -> str | None:
    """TRUE_ERRORs on the same fields that the rule above does not attribute:
    SAP revenue/net_income, and |source| > 1 margins off by another power of
    ten. Listed, never counted as upstream."""
    if r["verdict"].strip() != TE or r["kind"] != "mismatch" or upstream_cause(r):
        return None
    if r["ticker"] == "SAP" and r["field"] in CURRENCY_FIELDS:
        return "sap"
    if r["field"] == "profit_margin" and _abs_source(r) > 1:
        return "margin_other_scale"
    return None


def _abs_source(r: dict) -> float:
    try:
        return abs(float(r["source"]))
    except (TypeError, ValueError):
        return 0.0


def is_tp(verdict: str, mode: str) -> bool:
    return verdict == TE or (verdict == OD and mode == "other_defect_as_tp")


def counts_in(verdict: str, mode: str) -> bool:
    return mode == "other_defect_as_tp" or verdict != OD


# --- joining verdicts to flags ------------------------------------------------------

def adj_key(run: str, ticker: str, f: dict) -> tuple:
    return (run, ticker, f["section"], f["kind"], f["field"] or "", f["stated"], f["sentence"])


def attach_verdicts(briefs: list[dict], rows: list[dict]) -> None:
    """Give every distinct finding of every live brief its adjudication row
    (b['adj']); raises if a flag has no labelled row or rows are left over."""
    live = {tuple(str(r[k]) for k in nb._ADJ_KEY): r for r in rows if r["scope"] != "replication"}
    used, missing = set(), []
    for b in briefs:
        b["adj"] = []
        for f in nb._distinct(b["report"]["findings"]):
            k = adj_key(b["run"], b["ticker"], f)
            r = live.get(k)
            if r is None or not r["verdict"].strip():
                missing.append(k[:5])
                continue
            used.add(k)
            b["adj"].append((f, r))
    extra = set(live) - used
    if missing or extra:
        raise AssertionError(f"flags without a verdict: {missing[:5]} ({len(missing)}); "
                             f"rows without a flag: {sorted(extra)[:5]} ({len(extra)})")


# --- 1. precision ---------------------------------------------------------------------

def _groups(briefs: list[dict], partial: set) -> dict:
    g = defaultdict(list)
    for b in briefs:
        g[("run", b["run"])].append(b)
        if b["run"] not in partial:
            g[("arm", b["arm"])].append(b)
            g[("arm_model", f"{b['arm']}:{b['model']}")].append(b)
            g[("all_full", "all_full")].append(b)
    return g


def _by_run(bs: list[dict], fn) -> list[list[tuple[int, int]]]:
    per = defaultdict(list)
    for b in bs:
        per[b["run"]].append(fn(b))
    return [per[r] for r in sorted(per)]


def _rate_cb(bs: list[dict], fn, draws: int) -> dict:
    pairs = [fn(b) for b in bs]
    out = nb._rate(sum(p[0] for p in pairs), sum(p[1] for p in pairs))
    out["cluster_bootstrap"] = nb.cluster_bootstrap_ci(_by_run(bs, fn), draws=draws)
    return out


def live_precision(briefs: list[dict], partial: set, draws: int) -> dict:
    out = {"run": {}, "arm": {}, "arm_model": {}}
    for (kind, name), bs in sorted(_groups(briefs, partial).items()):
        v = Counter(r["verdict"].strip() for b in bs for _, r in b["adj"])
        res = {"rows": sum(v.values()), TE: v[TE], FP: v[FP], OD: v[OD]}
        for mode in MODES:
            fn = lambda b, m=mode: (sum(is_tp(r["verdict"].strip(), m) for _, r in b["adj"]),  # noqa: E731
                                    sum(counts_in(r["verdict"].strip(), m) for _, r in b["adj"]))
            res[mode] = _rate_cb(bs, fn, draws)
        if kind == "all_full":
            out["all_full"] = res
        else:
            out[kind][name] = res
    return out


def strata_precision(labels: dict, mode: str, pop: dict, rng=None) -> tuple[float | None, list]:
    """Stratum-weighted precision over the strata that have labels (the
    registered estimator); with `rng`, each stratum's labels are resampled
    with replacement first."""
    num = den = 0.0
    missing = []
    for h, n_h in pop.items():
        lab = labels.get(h, [])
        if rng is not None and lab:
            lab = rng.choices(lab, k=len(lab))
        d = sum(counts_in(v, mode) for v in lab)
        if d:
            num += n_h * sum(is_tp(v, mode) for v in lab) / d
            den += n_h
        else:
            missing.append(h)
    return (num / den if den else None), missing


def replication_precision(rows: list[dict], record: dict, draws: int) -> dict:
    registered = nb.replication_applied_precision(rows, record)
    out = {}
    for arm, rec in record["arms"].items():
        labels = defaultdict(list)
        for r in rows:
            if r["scope"] == "replication" and r["arm"] == arm and r["verdict"].strip():
                labels[r["field"]].append(r["verdict"].strip())
        res = {"registered": registered[arm],
               "verdicts": dict(Counter(v for vs in labels.values() for v in vs)),
               "labels_by_field": {h: dict(Counter(vs)) for h, vs in sorted(labels.items())},
               "unlabelled_strata": {h: n for h, n in rec["population_by_field"].items()
                                     if not labels.get(h)}}
        for mode in MODES:
            rng = random.Random(nb.BOOT_SEED)
            stats = [strata_precision(labels, mode, rec["population_by_field"], rng)[0]
                     for _ in range(draws)]
            res[mode] = {"within_stratum_bootstrap_ci95": nb._quantiles([s for s in stats if s is not None]),
                         "method": f"labels resampled within field strata, {draws} draws, "
                                   f"seed {nb.BOOT_SEED}"}
        out[arm] = res
    return out


# --- 2. notes ---------------------------------------------------------------------------

def notes_report(rows: list[dict]) -> dict:
    labelled = [r for r in rows if r["verdict"].strip()]
    noted = [r for r in rows if r.get("note", "").strip()]
    return {"labelled": len(labelled),
            "doubt_notes": sum(has_doubt(r["note"]) for r in labelled),
            "notes": [{"id": r["id"], "run": r["run"], "ticker": r["ticker"],
                       "field": r["field"] or r["kind"], "verdict": r["verdict"],
                       "doubt": has_doubt(r["note"]), "note": r["note"]} for r in noted]}


# --- 3. TRUE_ERROR-only rates -------------------------------------------------------------

def _mism(b: dict, keep) -> int:
    return sum(1 for f, r in b["adj"] if f["kind"] == "mismatch" and keep(r))


COUNTS = {
    "flags": lambda b: b["counts"],
    "true_error": lambda b: (_mism(b, lambda r: r["verdict"].strip() == TE), b["counts"][1]),
    "true_error_ex_upstream": lambda b: (
        _mism(b, lambda r: r["verdict"].strip() == TE and not upstream_cause(r)), b["counts"][1]),
}


def live_rates(briefs: list[dict], partial: set, draws: int) -> dict:
    out = {}
    for name, fn in COUNTS.items():
        block = {"run": {}, "arm": {}, "arm_model": {}}
        for (kind, g), bs in sorted(_groups(briefs, partial).items()):
            r = _rate_cb(bs, fn, draws)
            if kind == "all_full":
                block["all_full"] = r
            else:
                block[kind][g] = r
        full = [b for b in briefs if b["run"] not in partial]
        local = nb._sum_by_ticker([b for b in full if b["arm"] == "local-model"], fn)
        hosted = nb._sum_by_ticker([b for b in full if b["arm"] == "baseline"], fn)
        block["local_minus_hosted"] = nb.bootstrap_difference(local, hosted, draws)
        out[name] = block
    return out


def _local_true(b: dict, exclude: frozenset, keep) -> tuple[int, int]:
    """local_section_counts with the mismatch side filtered by verdict."""
    sec = lambda s: nb.section_key(s) in nb.LOCAL_SECTION_KEYS - exclude  # noqa: E731
    k = len({(f["section"], f["field"], f["stated"], f["sentence"]) for f, r in b["adj"]
             if f["kind"] == "mismatch" and sec(f["section"]) and keep(r)})
    return k, nb.local_section_counts(b["report"], exclude)[1]


def live_gap(briefs: list[dict], tc: dict | None, draws: int) -> dict:
    keeps = {"flags": lambda r: True,
             "true_error": lambda r: r["verdict"].strip() == TE}
    out = {}
    for name, keep in keeps.items():
        out[name] = {}
        for v in nb.VARIANTS:
            if v == "no_trunc" and not tc:
                continue
            per = {run: nb._sum_by_ticker(
                [b for b in briefs if b["run"] == run],
                lambda b, v=v, keep=keep: _local_true(
                    b, nb.live_truncated(tc, b["run"], b["ticker"]) if v == "no_trunc"
                    else frozenset(), keep)) for run in LIVE_GAP}
            d = nb.bootstrap_difference(per["r5nzh"], per["v924f"], draws)
            d["rates"] = {run: nb._rate(sum(x[0] for x in p.values()), sum(x[1] for x in p.values()))
                          for run, p in per.items()}
            out[name][v] = d
    return out


def replication_frame(rep_briefs: list[dict], record: dict) -> dict:
    """Per arm, per ticker: primary-metric flags by field and checked
    numbers; asserted against the registered sample record."""
    out = {}
    for arm in nb.REPLAY_ARMS:
        flags = defaultdict(Counter)
        checked = Counter()
        for b in rep_briefs:
            if b["arm"] != arm:
                continue
            v = b["variants"]["no_trunc"]
            checked[b["ticker"]] += v["counts"][1]
            for f in v["distinct"]:
                if f["kind"] == "mismatch":
                    flags[b["ticker"]][f["field"] or ""] += 1
        pop = Counter()
        for c in flags.values():
            pop.update(c)
        rec = record["arms"][arm]
        if dict(sorted(pop.items())) != rec["population_by_field"] or \
                sum(checked.values()) != rec["checked_distinct"]:
            raise AssertionError(f"{arm}: replication frame {dict(pop)} / {sum(checked.values())} "
                                 f"does not match the registered record")
        out[arm] = {"flags": {t: dict(c) for t, c in flags.items()}, "checked": dict(checked)}
    return out


def adjusted_gap(frame: dict, labels: dict, record: dict, draws: int,
                 unlabelled: str = "weighted") -> dict:
    """W4A16 - BF16 in the primary metric with each flag weighted by its
    field stratum's TRUE_ERROR share (TE / labelled; OTHER_DEFECT and
    FALSE_POSITIVE count as not true). A stratum without labels takes the
    arm's weighted share (as the registered estimator does), or 0 / 1 for
    the bounds. CI: paired ticker-cluster bootstrap whose ticker draws are
    exactly numeric_backtest.bootstrap_difference's (same seed, same calls),
    with each stratum's labels resampled alongside from a second generator;
    at 100% precision the interval therefore equals the registered one."""
    tickers = sorted(frame["bf16"]["checked"])

    def shares(arm, rng=None):
        lab = labels[arm]
        pop = record["arms"][arm]["population_by_field"]
        s = {}
        for h in pop:
            vs = lab.get(h, [])
            if rng is not None and vs:
                vs = rng.choices(vs, k=len(vs))
            if vs:
                s[h] = sum(v == TE for v in vs) / len(vs)
        w = sum(pop[h] * s[h] for h in s) / sum(pop[h] for h in s)
        fill = {"weighted": w, "zero": 0.0, "one": 1.0}[unlabelled]
        return {h: s.get(h, fill) for h in pop}

    def rate(arm, pick, s):
        k = sum(n * s[h] for t in pick for h, n in frame[arm]["flags"].get(t, {}).items())
        n = sum(frame[arm]["checked"].get(t, 0) for t in pick)
        return k / n

    s0 = {a: shares(a) for a in nb.REPLAY_ARMS}
    point = rate("w4a16", tickers, s0["w4a16"]) - rate("bf16", tickers, s0["bf16"])
    rng = random.Random(nb.BOOT_SEED)
    lab_rng = random.Random(nb.BOOT_SEED + 1)
    diffs = []
    for _ in range(draws):
        pick = rng.choices(tickers, k=len(tickers))
        s = {a: shares(a, lab_rng) for a in nb.REPLAY_ARMS}
        diffs.append(rate("w4a16", pick, s["w4a16"]) - rate("bf16", pick, s["bf16"]))
    lo, hi = nb._quantiles(diffs)
    return {"difference": round(point, 4), "ci95": [lo, hi],
            "excludes_zero": lo > 0 or hi < 0, "unlabelled_strata_as": unlabelled,
            "adjusted_rates": {a: round(rate(a, tickers, s0[a]), 4) for a in nb.REPLAY_ARMS},
            "estimated_true": {a: round(rate(a, tickers, s0[a]) * sum(frame[a]["checked"].values()), 1)
                               for a in nb.REPLAY_ARMS},
            "method": f"paired ticker-cluster bootstrap (seed {nb.BOOT_SEED}) with "
                      f"within-stratum label resampling (seed {nb.BOOT_SEED + 1}), {draws} draws"}


def precision_bound_sensitivity(frame: dict, rows: list[dict]) -> dict:
    """The adjusted gap if one arm's TRUE_ERROR share were at its sample
    Wilson lower bound and the other's at its point estimate: how far
    precision uncertainty the bootstrap cannot see (a 60/60 sample resamples
    to 60/60) could move the gap."""
    def total(arm):
        return (sum(sum(c.values()) for c in frame[arm]["flags"].values()),
                sum(frame[arm]["checked"].values()))
    share = {}
    for arm in nb.REPLAY_ARMS:
        vs = [r["verdict"].strip() for r in rows if r["scope"] == "replication" and r["arm"] == arm]
        share[arm] = nb._rate(sum(v == TE for v in vs), len(vs))
    (kw, nw), (kb, nb_) = total("w4a16"), total("bf16")
    pw, pb = share["w4a16"]["rate"], share["bf16"]["rate"]
    lw, lb = share["w4a16"]["ci95"][0], share["bf16"]["ci95"][0]
    return {"sample_true_error_share": share,
            "w4a16_at_lower_bound": round(kw * lw / nw - kb * pb / nb_, 4),
            "bf16_at_lower_bound": round(kw * pw / nw - kb * lb / nb_, 4)}


# --- 4. upstream ----------------------------------------------------------------------------

def upstream_report(rows: list[dict]) -> dict:
    def arm_of(r):
        if r["scope"] == "replication":
            return f"replication:{r['arm']} (sample of 60)"
        if r["scope"] == "partial":
            return f"{r['arm']} (partial runs)"
        return r["arm"]

    groups = defaultdict(list)
    for r in rows:
        groups[arm_of(r)].append(r)
        if r["scope"] == "full":
            groups[f"{r['arm']}:{r['model']}"].append(r)
    out = {}
    for g, rs in sorted(groups.items()):
        te = [r for r in rs if r["verdict"].strip() == TE]
        c = Counter(upstream_cause(r) for r in te)
        a = Counter(upstream_adjacent(r) for r in te)
        out[g] = {"true_errors": len(te),
                  "true_error_mismatches": sum(r["kind"] == "mismatch" for r in te),
                  "currency": c["currency"], "margin_fraction": c["margin_fraction"],
                  "upstream_total": c["currency"] + c["margin_fraction"],
                  "not_attributed_sap": a["sap"],
                  "not_attributed_margin_other_scale": a["margin_other_scale"]}
    listing = [{"id": r["id"], "run": r["run"], "ticker": r["ticker"], "field": r["field"],
                "stated": r["stated"], "ratio": r["ratio"],
                "cause": upstream_cause(r) or f"not attributed ({upstream_adjacent(r)})"}
               for r in rows if upstream_cause(r) or upstream_adjacent(r)]
    return {"by_group": out, "rows": listing}


# --- markdown -------------------------------------------------------------------------------

def _p(r: dict) -> str:
    return f"{r['k']}/{r['n']} = {r['rate']:.1%}" if r["n"] else "n/a"


def _ci(ci) -> str:
    return f"{ci[0]:.1%}–{ci[1]:.1%}"


def _cb(r: dict) -> str:
    """The cluster bootstrap CI, or n/a where every resample is identical
    (all flags one way): the Wilson bound is then the only bound."""
    if not r["n"] or r["k"] in (0, r["n"]):
        return "n/a (no variation)"
    return _ci(r["cluster_bootstrap"]["ci95"])


def _pval(d: dict) -> str:
    p = d["p_two_sided_bootstrap"]
    return f"< {2 / nb.BOOT_DRAWS:g}" if p == 0 else f"{p}"


def _pts(d: dict) -> str:
    return (f"{100 * d['difference']:+.1f} pts (CI {100 * d['ci95'][0]:+.1f} to "
            f"{100 * d['ci95'][1]:+.1f})")


def markdown(res: dict) -> str:
    L = [f"# Numeric-check adjudication results, {res['date']}", "",
         f"Generated by scripts/numeric_adjudicated.py from {res['adjudication']} "
         f"(verdicts committed in {res['verdicts_commit']}, before any of these "
         "figures existed; rules: eval/numeric_check/README.md). Not a number of record.", "",
         "## 1. Precision", "",
         "Unit: a distinct finding (an adjudication row). Two ways: OTHER_DEFECT as a "
         "true positive, and OTHER_DEFECT excluded from the denominator. The cluster "
         "bootstrap resamples whole briefs (pooled rows within each run); where every "
         "flag got the same verdict it has no variation to resample, and the Wilson "
         "lower bound (which treats flags as independent, so is optimistic) is the only bound.", "",
         "| Group | Rows | TRUE_ERROR | FALSE_POSITIVE | OTHER_DEFECT | Precision, OD as TP "
         "| Wilson 95% | Cluster bootstrap 95% | Precision, OD excluded | Wilson 95% | "
         "Cluster bootstrap 95% |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    P = res["precision"]["live"]

    def prow(name, r):
        if not r["rows"]:
            return f"| {name} | 0 | – | – | – | no flags | | | | | |"
        t, x = r["other_defect_as_tp"], r["other_defect_excluded"]
        return (f"| {name} | {r['rows']} | {r[TE]} | {r[FP]} | {r[OD]} | {_p(t)} | "
                f"{_ci(t['ci95'])} | {_cb(t)} | {_p(x)} | {_ci(x['ci95'])} | {_cb(x)} |")
    for name, r in P["run"].items():
        L.append(prow(f"run {name}", r))
    for name, r in P["arm"].items():
        L.append(prow(f"arm {name} (full runs)", r))
    for name, r in P["arm_model"].items():
        L.append(prow(f"{name} (full runs)", r))
    L.append(prow("all full runs", P["all_full"]))

    L += ["", "Replication (pre-registered estimator: stratum-weighted precision of the "
          "60-per-arm stratified sample, applied to that arm's primary flag count):", "",
          "| Arm | Primary flags | Sample size | Labelled | Verdicts | Weighted precision "
          "(OD as TP / excluded) | Sample Wilson 95% | Within-stratum bootstrap 95% | "
          "Unlabelled strata (flags) | Estimated true / adjusted rate |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for arm, r in res["precision"]["replication"].items():
        g = r["registered"]
        t, x = g["other_defect_as_tp"], g["other_defect_excluded"]
        un = ", ".join(f"{h} ({n}, unlabelled)" for h, n in r["unlabelled_strata"].items()) or "none"
        L.append(f"| {arm} | {g['flags']} | {g['sample_size']} | {g['labelled']} | "
                 f"{', '.join(f'{k} {v}' for k, v in r['verdicts'].items())} | "
                 f"{t['precision_weighted']:.1%} / {x['precision_weighted']:.1%} | "
                 f"{_ci(t['sample_unweighted']['ci95'])} | "
                 f"{_ci(r['other_defect_as_tp']['within_stratum_bootstrap_ci95'])} | {un} | "
                 f"{t['estimated_true_mismatches']} / {t['adjusted_rate']:.1%} |")
    L += ["", "The registered estimator gives an unlabelled stratum the weighted precision "
          "of the labelled ones; the bounds in section 3 set it to 0 and 1 instead."]

    n = res["notes"]
    L += ["", "## 2. Adjudicator notes", "",
          f"Doubt notes (rule 8): {n['doubt_notes']} of {n['labelled']} labelled rows. "
          f"Notes of any kind: {len(n['notes'])}."]
    for x in n["notes"]:
        L.append(f"- id {x['id']} ({x['run']} {x['ticker']} {x['field']}, {x['verdict']}"
                 f"{', doubt' if x['doubt'] else ''}): {x['note']}")

    R = res["true_error_rates"]
    L += ["", "## 3. Mismatch rates on TRUE_ERROR flags only", "",
          "Mismatches per distinct checked number, all sections, full runs. 'Flags' is "
          "the unadjudicated rate; 'TRUE_ERROR' counts only flags adjudicated TRUE_ERROR "
          "(OTHER_DEFECT and FALSE_POSITIVE drop out); the last column also drops the "
          "TRUE_ERRORs that trace to the two upstream data defects (section 4).", "",
          "| Group | Flags | TRUE_ERROR | Cluster bootstrap 95% | TRUE_ERROR, upstream excluded "
          "| Cluster bootstrap 95% |", "|---|---|---|---|---|---|"]
    for kind in ("run", "arm", "arm_model"):
        for name in R["flags"][kind]:
            a, b, c = (R[m][kind][name] for m in COUNTS)
            L.append(f"| {kind} {name} | {_p(a)} | {_p(b)} | {_cb(b)} | {_p(c)} | {_cb(c)} |")
    L += ["", "Local-model minus hosted (pooled arms; paired by ticker, cluster bootstrap):", ""]
    for m in COUNTS:
        L.append(f"- {m}: {_pts(R[m]['local_minus_hosted'])}, bootstrap p "
                 f"{_pval(R[m]['local_minus_hosted'])}")

    G = res["live_gap"]
    L += ["", "Live same-image gap, r5nzh (W4A16) - v924f (BF16), Financial Health + Risk "
          "Factors only, one draw per ticker:", "",
          "| Counting | Sections | r5nzh | v924f | Difference | Bootstrap p |", "|---|---|---|---|---|---|"]
    for m, vs in G.items():
        for v, d in vs.items():
            sec = "all" if v == "all" else "truncated excluded (estimated)"
            if m == "true_error" and v == "no_trunc":
                sec += "; exploratory, post hoc"
            L.append(f"| {m} | {sec} | "
                     f"{_p(d['rates']['r5nzh'])} | {_p(d['rates']['v924f'])} | {_pts(d)} | "
                     f"{_pval(d)} |")
    t = G.get("true_error", {}).get("no_trunc")
    if t:
        L += ["", f"The truncation-excluded TRUE_ERROR gap ({_pts(t)}, p = {_pval(t)}) is "
              "exploratory and post hoc: one draw per ticker, and the truncation subset was "
              "chosen after the pilot. The pre-registered replication below remains the "
              "primary result."]

    A = res["replication_adjusted"]
    L += ["", "Replication, primary metric (truncated sections excluded). The pre-registered "
          "result on unadjudicated flags stays the primary result; the adjusted rows are "
          "secondary.", "",
          f"- Primary (registered, unadjudicated): {A['primary_statement']}",
          f"- Recomputed here from the rebuilt frame: {_pts(A['unadjusted'])} "
          f"({'matches' if A['reproduces_registered'] else 'DOES NOT match'} the committed result)."]
    for k, lab in (("weighted", "unlabelled stratum at the arm's weighted share"),
                   ("zero", "unlabelled stratum counted as 0% true"),
                   ("one", "unlabelled stratum counted as 100% true")):
        d = A["adjusted"][k]
        L.append(f"- Adjusted, TRUE_ERROR only, {lab}: {_pts(d)}; adjusted rates W4A16 "
                 f"{d['adjusted_rates']['w4a16']:.1%}, BF16 {d['adjusted_rates']['bf16']:.1%}.")
    s = A["precision_bound_sensitivity"]
    L.append(f"- Precision at its sample Wilson lower bound in one arm only: W4A16 at bound "
             f"{100 * s['w4a16_at_lower_bound']:+.1f} pts; BF16 at bound "
             f"{100 * s['bf16_at_lower_bound']:+.1f} pts (point estimates; the bootstrap "
             f"cannot see this, since a 60/60 sample resamples to 60/60).")

    U = res["upstream"]
    L += ["", "## 4. TRUE_ERRORs tracing to the upstream data findings", "",
          "Mechanical rule (scripts/numeric_adjudicated.py upstream_cause): currency = TM, "
          "TSM, NVO or BABA revenue/net_income whose stated figure is a power-of-ten "
          "rescaling of the mislabelled home-currency source; margin_fraction = a "
          "profit_margin with |source| > 1 stated at ratio ~0.01 (the fraction written as "
          "a percent). SAP and margins off by another power of ten are listed, not attributed.", "",
          "| Group | TRUE_ERRORs | of which mismatches | Currency | Margin fraction | "
          "Upstream total | Not attributed: SAP | Not attributed: margin, other scale |",
          "|---|---|---|---|---|---|---|---|"]
    for g, r in U["by_group"].items():
        L.append(f"| {g} | {r['true_errors']} | {r['true_error_mismatches']} | {r['currency']} | "
                 f"{r['margin_fraction']} | {r['upstream_total']} | {r['not_attributed_sap']} | "
                 f"{r['not_attributed_margin_other_scale']} |")
    return "\n".join(L) + "\n"


# --- main -------------------------------------------------------------------------------------

def run(date: str, draws: int = nb.BOOT_DRAWS) -> dict:
    with open(nb.ADJ_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if any(not r["verdict"].strip() for r in rows):
        raise SystemExit("adjudication.csv has unlabelled rows")
    nb.precision(rows)  # raises on a verdict outside VERDICTS
    record = json.loads(nb.REPLICATION_SAMPLE.read_text(encoding="utf-8"))

    briefs = [b for b in (nb.load_brief(p, nb.RAW) for p in sorted(nb.RAW.glob("*-findings/**/*.md"))) if b]
    nb.backtest(briefs)
    partial = nb.partial_runs(briefs)
    attach_verdicts(briefs, rows)
    tc = nb.load_token_counts()

    rep_dir = nb.find_replays()["replication"]
    rep = nb.load_replay(rep_dir, "replication")
    frame = replication_frame(rep, record)
    labels = {arm: defaultdict(list) for arm in nb.REPLAY_ARMS}
    for r in rows:
        if r["scope"] == "replication":
            labels[r["arm"]][r["field"]].append(r["verdict"].strip())
    unadj = nb.bootstrap_difference(
        nb._sum_by_ticker([b for b in rep if b["arm"] == "w4a16"], lambda b: b["variants"]["no_trunc"]["counts"]),
        nb._sum_by_ticker([b for b in rep if b["arm"] == "bf16"], lambda b: b["variants"]["no_trunc"]["counts"]),
        draws)
    committed = json.loads((REPO / "eval" / "runs" / "numeric-backtest-2026-09-29.json")
                           .read_text(encoding="utf-8"))
    reg = committed["replay"]["labels"]["replication"]

    return {
        "date": date,
        "harness": "scripts/numeric_adjudicated.py",
        "adjudication": nb._rel(nb.ADJ_PATH),
        "verdicts_commit": "a27264b",
        "note": "Adjudicated numeric-check results. Not a number of record.",
        "precision": {"live": live_precision(briefs, partial, draws),
                      "replication": replication_precision(rows, record, draws)},
        "notes": notes_report(rows),
        "true_error_rates": live_rates(briefs, partial, draws),
        "live_gap": live_gap(briefs, tc, draws),
        "replication_adjusted": {
            "replay": rep_dir.name,
            "primary_statement": reg["statement"],
            "unadjusted": unadj,
            "reproduces_registered": (unadj["difference"] == reg["difference"]["no_trunc"]["difference"]
                                      and unadj["ci95"] == reg["difference"]["no_trunc"]["ci95"]),
            "adjusted": {k: adjusted_gap(frame, labels, record, draws, k)
                         for k in ("weighted", "zero", "one")},
            "precision_bound_sensitivity": precision_bound_sensitivity(frame, rows),
        },
        "upstream": upstream_report(rows),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    args = ap.parse_args()
    res = run(args.date)
    out = REPO / "eval" / "runs" / f"numeric-adjudicated-{args.date}.json"
    out.write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8", newline="\n")
    md = markdown(res)
    out.with_suffix(".md").write_text(md, encoding="utf-8", newline="\n")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(md)
    print(f"wrote {nb._rel(out)} (+ .md)")


if __name__ == "__main__":
    main()
