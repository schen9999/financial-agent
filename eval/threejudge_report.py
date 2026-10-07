#!/usr/bin/env python3
"""Judge v2 precision and recall per judging and for the majority vote, and
judge-judge agreement, from the three-judging calibration sample
(eval/build_threejudge_calibration.py).

Truth is the human label: UNSUPPORTED is the positive class; SUPPORTED and
INFERENCE are not. A judging "flags" a claim when its verdict is
UNSUPPORTED; NOT_LISTED and any other verdict do not flag. The majority
flags when at least two of the three judgings said UNSUPPORTED.

Precision and recall are population-weighted: each labelled claim stands
for N_k / n_k claims of its stratum (n_k = the labelled rows of stratum k,
so skipped rows drop out of the weights), the 2x2 cells are estimated as
weighted sums, and precision = TP / (TP + FP), recall = TP / (TP + FN).
95% intervals: stratified bootstrap (resample within each stratum), seeded.
Recall is over the claims at least one judging listed — a figure no
judging listed is outside the population, as in every earlier calibration.

Recall as each judging's single-judging calibration would measure it
(September 2026: over the claims that judging listed) is reported beside
it as "listed-only recall": the same weighted estimate over the rows that
judging listed. It is higher by construction — a claim the judging never
listed cannot count against it — and is the figure comparable with the
calibration of record. The majority has no listed-only form.

True-rate estimate per run (post-stratified within the run): the claims
of the run that any judging listed (the population, earlier-labelled claims
excluded as in the draw), each stratum's human-UNSUPPORTED share taken from
that run's own labelled rows, rate = sum_k N_k,run * p_k,run / N_run. 95%
interval from Jeffreys posteriors per stratum (Beta(x + 0.5, n - x + 0.5),
seeded Monte Carlo), as eval/reweight_calibration.py does; a stratum
labelled in full (n = N) has no sampling error and enters exactly. The strata were
drawn pooled over runs, so a run's rows in a stratum are a random subsample
of it; few rows per run and stratum make these intervals wide.

Agreement needs no human labels, so it is computed on the whole
population (rebuilt from the method file's runs and judgings):
  listing     share of the union of claims each pair both listed
  verdict     Cohen's kappa on the three labels, claims both listed;
              Fleiss' kappa, claims all three listed
  flag        Cohen's kappa on flagged / not flagged over the union
              (NOT_LISTED = not flagged); Fleiss' likewise

  python eval/threejudge_report.py
"""
import argparse
import csv
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from eval import build_threejudge_calibration as btc  # noqa: E402

JV = btc.JV
DRAWS = 2000
SEED = 20261006
RATERS = ("j1", "j2", "j3", "majority")


def flags(row: dict, rater: str) -> bool:
    if rater == "majority":
        return sum(row[j] == "UNSUPPORTED" for j in ("j1", "j2", "j3")) >= 2
    return row[rater] == "UNSUPPORTED"


def load(sample: Path, key: Path, method: dict) -> list[dict]:
    with open(sample, newline="", encoding="utf-8") as f:
        labels = {r["id"]: r["human_label"].strip().upper() for r in csv.DictReader(f)}
    with open(key, newline="", encoding="utf-8") as f:
        rows = [dict(r, human=labels.get(r["id"], "")) for r in csv.DictReader(f)]
    rows = [r for r in rows if r["human"] in ("SUPPORTED", "UNSUPPORTED", "INFERENCE")]
    n = Counter(r["stratum"] for r in rows)
    for r in rows:
        r["w"] = method["population"][r["stratum"]] / n[r["stratum"]]
    return rows


def pr(rows: list[dict], rater: str) -> tuple[float | None, float | None]:
    tp = fp = fn = 0.0
    for r in rows:
        f, u = flags(r, rater), r["human"] == "UNSUPPORTED"
        tp += r["w"] * (f and u)
        fp += r["w"] * (f and not u)
        fn += r["w"] * (u and not f)
    return (tp / (tp + fp) if tp + fp else None, tp / (tp + fn) if tp + fn else None)


def listed(rows: list[dict], rater: str) -> list[dict]:
    """The rows the judging listed, weights unchanged (an estimate over that
    judging's own listed claims)."""
    return [r for r in rows if r[rater] != "NOT_LISTED"]


def boot(rows: list[dict], rater: str, draws: int = DRAWS, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    by = defaultdict(list)
    for r in rows:
        by[r["stratum"]].append(r)
    ps, rs = [], []
    for _ in range(draws):
        res = [rng.choice(v) for v in by.values() for _ in v]
        p, rc = pr(res, rater)
        if p is not None:
            ps.append(p)
        if rc is not None:
            rs.append(rc)
    ci = lambda v: (sorted(v)[int(0.025 * len(v))], sorted(v)[int(0.975 * len(v)) - 1]) if v else (None, None)  # noqa: E731
    p, rc = pr(rows, rater)
    return {"precision": p, "precision_ci": ci(ps), "recall": rc, "recall_ci": ci(rs)}


def true_rates(rows: list[dict], pop: list[dict], draws: int = DRAWS, seed: int = SEED) -> dict:
    """{run: {N, est, rate, ci, strata: {k: (N, x, n)}}} from the labelled rows
    and the population (btc.population, earlier-labelled claims removed)."""
    rng = random.Random(seed)
    out = {}
    for run in sorted({p["run"] for p in pop}):
        N = Counter(p["stratum"] for p in pop if p["run"] == run)
        lab = [r for r in rows if r["run"] == run]
        st = {k: (N[k], sum(r["human"] == "UNSUPPORTED" for r in lab if r["stratum"] == k),
                  sum(1 for r in lab if r["stratum"] == k)) for k in "UIWS" if N[k]}
        if any(n == 0 for _, _, n in st.values()):
            raise SystemExit(f"{run}: a stratum with claims has no labelled rows")
        tot = sum(N.values())
        est = sum(Nk * x / n for Nk, x, n in st.values())
        sims = sorted(sum(Nk * (x / n if n == Nk else rng.betavariate(x + 0.5, n - x + 0.5))
                          for Nk, x, n in st.values()) / tot
                      for _ in range(draws))
        out[run] = {"N": tot, "est": est, "rate": est / tot,
                    "ci": (sims[int(0.025 * draws)], sims[int(0.975 * draws) - 1]), "strata": st}
    return out


def true_rate_lines(tr_: dict) -> list[str]:
    L = ["True unsupported rate, estimated from the human labels (per run, post-stratified; WIDE intervals)"]
    for run, t in tr_.items():
        st = ", ".join(f"{k} {x}/{n} of {Nk}" for k, (Nk, x, n) in t["strata"].items())
        L.append(f"  {run:8} {t['est']:.1f}/{t['N']} = {t['rate']:.1%} (95% CI {t['ci'][0]:.1%}–{t['ci'][1]:.1%}); "
                 f"strata human-U/labelled of N: {st}")
    return L


def cohen(a: list[str], b: list[str]) -> float | None:
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in ca) / n / n
    return (po - pe) / (1 - pe) if pe < 1 else None


def fleiss(items: list[list[str]]) -> float | None:
    if not items:
        return None
    m = len(items[0])
    cats = sorted({v for it in items for v in it})
    p_j = {c: sum(it.count(c) for it in items) / (len(items) * m) for c in cats}
    p_i = [(sum(it.count(c) ** 2 for c in cats) - m) / (m * (m - 1)) for it in items]
    pbar, pe = sum(p_i) / len(p_i), sum(v * v for v in p_j.values())
    return (pbar - pe) / (1 - pe) if pe < 1 else None


def agreement(pop: list[dict]) -> list[str]:
    L = [f"Judge-judge agreement, whole population ({len(pop)} claims listed by at least one judging)"]
    fl = [["U" if v == "UNSUPPORTED" else "-" for v in c["verdicts"]] for c in pop]
    for a, b in ((0, 1), (0, 2), (1, 2)):
        both = [c for c in pop if "NOT_LISTED" not in (c["verdicts"][a], c["verdicts"][b])]
        k3 = cohen([c["verdicts"][a] for c in both], [c["verdicts"][b] for c in both])
        kf = cohen([f[a] for f in fl], [f[b] for f in fl])
        L.append(f"  j{a + 1}-j{b + 1}: both listed {len(both)}/{len(pop)} = {len(both) / len(pop):.1%}; "
                 f"verdict kappa {fmt(k3)}; flag kappa (union) {fmt(kf)}")
    all3 = [c["verdicts"] for c in pop if "NOT_LISTED" not in c["verdicts"]]
    L.append(f"  Fleiss, all three listed ({len(all3)}): verdict kappa {fmt(fleiss(all3))}; "
             f"flag kappa (union, {len(fl)}) {fmt(fleiss(fl))}")
    per = [sum(c["verdicts"][j] == "UNSUPPORTED" for c in pop) for j in range(3)]
    L.append(f"  flagged UNSUPPORTED: j1 {per[0]}, j2 {per[1]}, j3 {per[2]}; "
             f"by all three {sum(f.count('U') == 3 for f in fl)}, by exactly one {sum(f.count('U') == 1 for f in fl)}")
    return L


def fmt(x) -> str:
    return "n/a" if x is None else f"{x:.3f}"


def pct(x) -> str:
    return "n/a" if x is None else f"{x:.1%}"


def report(rows: list[dict], method: dict) -> list[str]:
    L = [f"Labelled {len(rows)} claims (judge v2, three judgings); runs {' '.join(method['runs'])}",
         "Stratum  population  labelled  human UNSUPPORTED"]
    for k in "UIWS":
        rk = [r for r in rows if r["stratum"] == k]
        L.append(f"  {k:6} {method['population'][k]:10} {len(rk):9} {sum(r['human'] == 'UNSUPPORTED' for r in rk):10}")
    L.append("Population-weighted precision and recall on UNSUPPORTED (95% stratified bootstrap)")
    for rater in RATERS:
        b = boot(rows, rater)
        line = (f"  {rater:9} precision {pct(b['precision'])} (CI {pct(b['precision_ci'][0])}–"
                f"{pct(b['precision_ci'][1])}); recall {pct(b['recall'])} (CI {pct(b['recall_ci'][0])}–"
                f"{pct(b['recall_ci'][1])})")
        if rater != "majority":
            lb = boot(listed(rows, rater), rater)
            line += (f"; listed-only recall {pct(lb['recall'])} (CI {pct(lb['recall_ci'][0])}–"
                     f"{pct(lb['recall_ci'][1])})")
        L.append(line)
    return L


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--sample", type=Path, default=JV / "threejudge_sample.csv")
    ap.add_argument("--key", type=Path, default=JV / "threejudge_key.csv")
    ap.add_argument("--method", type=Path, default=JV / "threejudge_method.json")
    ap.add_argument("--no-agreement", action="store_true")
    args = ap.parse_args(argv)
    method = json.loads(args.method.read_text(encoding="utf-8"))
    rows = load(args.sample, args.key, method)
    lines = report(rows, method)
    if not args.no_agreement:
        pop = btc.population(method["runs"], method["judgings"])
        earlier = btc.earlier_claims()
        lines += true_rate_lines(true_rates(rows, [p for p in pop if btc.norm(p["claim"]) not in earlier]))
        lines += agreement(pop)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
