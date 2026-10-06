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
        L.append(f"  {rater:9} precision {pct(b['precision'])} (CI {pct(b['precision_ci'][0])}–"
                 f"{pct(b['precision_ci'][1])}); recall {pct(b['recall'])} (CI {pct(b['recall_ci'][0])}–"
                 f"{pct(b['recall_ci'][1])})")
    return L


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--sample", type=Path, default=JV / "threejudge_sample.csv")
    ap.add_argument("--key", type=Path, default=JV / "threejudge_key.csv")
    ap.add_argument("--method", type=Path, default=JV / "threejudge_method.json")
    ap.add_argument("--no-agreement", action="store_true")
    args = ap.parse_args(argv)
    method = json.loads(args.method.read_text(encoding="utf-8"))
    lines = report(load(args.sample, args.key, method), method)
    if not args.no_agreement:
        lines += agreement(btc.population(method["runs"], method["judgings"]))
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
