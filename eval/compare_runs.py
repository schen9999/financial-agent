#!/usr/bin/env python3
"""Compare grounding-eval runs across images: pooled rates, label counting,
and retrieved-context drift. Reads committed run artifacts only.

Written for the 2026-09-25 hosted-arm drift finding (Sep 5 image: 9j2dj,
j4cnp; Sep 23 image: kcf7s, dvvxk). Three subcommands:

  pooled    Pool runs into two named groups from their claims.jsonl rows
            (per-claim deduped, the counting rule of record) and report each
            group's unsupported rate with a Wilson interval plus the exact
            two-sided Fisher p between the groups.
              --group NAME CLAIMS_JSONL [CLAIMS_JSONL ...]   (exactly twice)

  counts    Raw vs deduped label counts per findings directory: raw is
            agent.grounding.count_labels (every LABEL: line, the in-DAG rule
            before 4bc4e35), deduped is eval.label.count_labels_deduped (one
            label per CLAIM block, the rule since). Lists every ticker where
            the two differ.
              --run LABEL FINDINGS_DIR   (repeatable)

  contexts  Per ticker, whether each block of the retrieved source context
            (STOCK DATA, NEWS ARTICLES, SEC FILING SUMMARIES, RAG SEC
            HIGHLIGHTS, RAG RISK FACTORS) is byte-identical between two runs;
            for SEC FILING SUMMARIES also whether the filing forms and dates
            match, and for the RAG blocks whether each side had text or
            "(not available)".
              --a LABEL FINDINGS_DIR --b LABEL FINDINGS_DIR

Usage:
  python eval/compare_runs.py pooled \\
      --group sep5  eval/runs/9j2dj-claims.jsonl eval/runs/j4cnp-claims.jsonl \\
      --group sep23 eval/runs/kcf7s-claims.jsonl eval/runs/dvvxk-claims.jsonl
  python eval/compare_runs.py counts \\
      --run kcf7s eval/runs/raw/kcf7s-findings --run dvvxk eval/runs/raw/dvvxk-findings
  python eval/compare_runs.py contexts \\
      --a j4cnp eval/runs/raw/j4cnp-findings --b kcf7s eval/runs/raw/kcf7s-findings
"""
import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval.label import count_labels_deduped, parse_findings_file  # noqa: E402
from eval.stats import fisher_exact, format_rate_ci  # noqa: E402

BLOCKS = ("STOCK DATA", "NEWS ARTICLES", "SEC FILING SUMMARIES",
          "RAG — SEC HIGHLIGHTS", "RAG — RISK FACTORS")
_BLOCK_RE = re.compile(r"^(" + "|".join(re.escape(b) for b in BLOCKS) + r"):\n", re.M)
NOT_AVAILABLE = "(not available)"


def raw_counts(findings: str) -> dict:
    """agent.grounding.count_labels, restated here so this script stays
    import-light (that module pulls the model stack)."""
    return {k: len(re.findall(rf"\*{{0,2}}LABEL:\*{{0,2}}\s+{k.upper()}\b", findings, re.I))
            for k in ("supported", "unsupported", "inference")}


def split_blocks(context: str) -> dict:
    marks = list(_BLOCK_RE.finditer(context))
    return {m.group(1): context[m.end():(marks[i + 1].start() if i + 1 < len(marks)
                                          else len(context))].strip()
            for i, m in enumerate(marks)}


def findings_by_ticker(findings_dir: Path) -> dict:
    """ticker -> parsed findings, searching nested per-ticker dirs too."""
    out = {}
    for f in sorted(findings_dir.rglob("*_*.md")):
        parsed = parse_findings_file(f.read_text(encoding="utf-8"))
        if parsed:
            out[f.stem.rsplit("_", 1)[0]] = parsed
    return out


def filings(sec_block: str) -> dict:
    """form type -> filing date from the SEC FILING SUMMARIES JSON."""
    try:
        data = json.loads(sec_block)
    except (json.JSONDecodeError, TypeError):
        return {}
    return {k: v.get("filing_date") for k, v in data.items() if isinstance(v, dict)}


def news_changed(dir_a: Path, dir_b: Path) -> set:
    """Tickers whose NEWS ARTICLES block differs between two runs."""
    fa, fb = findings_by_ticker(dir_a), findings_by_ticker(dir_b)
    return {t for t in set(fa) & set(fb)
            if split_blocks(fa[t]["context"]).get("NEWS ARTICLES")
            != split_blocks(fb[t]["context"]).get("NEWS ARTICLES")}


def cmd_pooled(groups, tickers=None, label="all tickers"):
    tallies = []
    print(f"[{label}]")
    for name, *paths in groups:
        rows = [json.loads(line) for p in paths
                for line in Path(p).read_text(encoding="utf-8").splitlines()]
        if tickers is not None:
            rows = [r for r in rows if r["ticker"] in tickers]
        u, n = sum(r["judge_label"] == "UNSUPPORTED" for r in rows), len(rows)
        tallies.append((u, n))
        runs = ", ".join(Path(p).name.split("-claims")[0] for p in paths)
        print(f"{name:<8} ({runs}): {u}/{n} = {format_rate_ci(u, n)}")
    (a, n), (b, m) = tallies
    print(f"Fisher exact, two-sided: p = {fisher_exact(a, n - a, b, m - b):.4f}")


def cmd_counts(runs):
    for label, d in runs:
        raw_t = {"supported": 0, "unsupported": 0, "inference": 0}
        ded_t = dict(raw_t)
        diffs = []
        for ticker, parsed in findings_by_ticker(Path(d)).items():
            raw = raw_counts(parsed["findings"])
            ded = count_labels_deduped(parsed["findings"])
            for k in raw_t:
                raw_t[k] += raw[k]
                ded_t[k] += ded[k]
            if any(raw[k] != ded[k] for k in raw):
                diffs.append((ticker, raw, {k: ded[k] for k in raw}))
        fmt = lambda c: f"{c['supported']} S / {c['unsupported']} U / {c['inference']} I = {sum(c.values())}"
        print(f"{label}: raw {fmt(raw_t)}; deduped {fmt(ded_t)}")
        for ticker, raw, ded in diffs:
            print(f"  {ticker}: raw {fmt(raw)} vs deduped {fmt(ded)}")
        if not diffs:
            print("  no ticker differs")


def cmd_contexts(a, b):
    (la, da), (lb, db) = a, b
    fa, fb = findings_by_ticker(Path(da)), findings_by_ticker(Path(db))
    common = sorted(set(fa) & set(fb))
    print(f"{la} vs {lb}: {len(common)} tickers in common")
    same = {blk: 0 for blk in BLOCKS}
    sim = {blk: [] for blk in BLOCKS}
    avail = {}
    filing_diff = []
    for t in common:
        ba = split_blocks(fa[t]["context"])
        bb = split_blocks(fb[t]["context"])
        for blk in BLOCKS:
            x, y = ba.get(blk, ""), bb.get(blk, "")
            same[blk] += x == y
            sim[blk].append(SequenceMatcher(None, x, y, autojunk=False).ratio())
            if blk.startswith("RAG"):
                key = (blk, x == NOT_AVAILABLE, y == NOT_AVAILABLE)
                avail[key] = avail.get(key, 0) + 1
        ga, gb = filings(ba.get("SEC FILING SUMMARIES")), filings(bb.get("SEC FILING SUMMARIES"))
        if ga != gb:
            filing_diff.append((t, ga, gb))
    print("\nbyte-identical blocks (and mean difflib similarity):")
    for blk in BLOCKS:
        mean = sum(sim[blk]) / len(sim[blk]) if sim[blk] else 0.0
        print(f"  {blk:<22} {same[blk]:>3}/{len(common)} identical   similarity {mean:.3f}")
    print("\nRAG availability (a unavailable, b unavailable): tickers")
    for (blk, xa, xb), n in sorted(avail.items()):
        print(f"  {blk:<22} ({xa!s:<5}, {xb!s:<5}): {n}")
    print(f"\nSEC filings (form -> filing date) differ for {len(filing_diff)}/{len(common)} tickers")
    for t, ga, gb in filing_diff:
        print(f"  {t}: {la} {ga} | {lb} {gb}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pooled")
    p.add_argument("--group", nargs="+", action="append", required=True,
                   metavar="NAME_THEN_CLAIMS_JSONL")
    p.add_argument("--news-split", nargs=2, metavar=("FINDINGS_DIR_A", "FINDINGS_DIR_B"),
                   help="also split by tickers whose NEWS ARTICLES block differs "
                        "between these two runs")
    c = sub.add_parser("counts")
    c.add_argument("--run", nargs=2, action="append", required=True,
                   metavar=("LABEL", "FINDINGS_DIR"))
    x = sub.add_parser("contexts")
    x.add_argument("--a", nargs=2, required=True, metavar=("LABEL", "FINDINGS_DIR"))
    x.add_argument("--b", nargs=2, required=True, metavar=("LABEL", "FINDINGS_DIR"))
    args = ap.parse_args(argv)
    if args.cmd == "pooled":
        if len(args.group) != 2 or any(len(g) < 2 for g in args.group):
            ap.error("pooled needs exactly two --group NAME CLAIMS_JSONL ...")
        if args.news_split:
            changed = news_changed(Path(args.news_split[0]), Path(args.news_split[1]))
            all_t = {json.loads(line)["ticker"] for p in args.group[0][1:]
                     for line in Path(p).read_text(encoding="utf-8").splitlines()}
            print(f"news changed ({len(changed)}): {', '.join(sorted(changed))}\n")
            cmd_pooled(args.group, changed, f"news changed, {len(changed)} tickers")
            print()
            cmd_pooled(args.group, all_t - changed,
                       f"news unchanged, {len(all_t - changed)} tickers")
        else:
            cmd_pooled(args.group)
    elif args.cmd == "counts":
        cmd_counts(args.run)
    else:
        cmd_contexts(args.a, args.b)


if __name__ == "__main__":
    main()
