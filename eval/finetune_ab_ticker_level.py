#!/usr/bin/env python3
"""Ticker-level checks on the 40-ticker fine-tune A/B (j4cnp vs lsnnc,
2026-09-05/06, judge v2, one judging each).

The recorded Fisher p = 0.0023 treats the 760 claims as independent; claims
cluster within briefs. This prints, from the committed findings:

  - the pooled counts (reproducing 30/368 vs 12/392) and claim-level Fisher;
  - a paired, ticker-level bootstrap on per-ticker unsupported rates
    (eval/multi_arm_stats.py `paired`, 10,000 resamples, seed 0, the method
    eval/three_judging_stats.py uses), so the point estimate is the
    TICKER-AVERAGED rate, not the pooled one, with its exact sign test;
  - claim-level Fisher with each ticker left out in turn (range, and the
    ticker whose removal moves p most).

Counting is eval/three_judging_stats.judging_counts on the original
judging (rejudge_runs.summarize).

  python eval/finetune_ab_ticker_level.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from eval import multi_arm_stats as mas  # noqa: E402
from eval import three_judging_stats as tjs  # noqa: E402
from eval.stats import fisher_exact  # noqa: E402

LOCAL, HOSTED = "lsnnc", "j4cnp"


def fisher(a: dict, b: dict, drop: str | None = None) -> tuple:
    ua = sum(v["unsupported"] for t, v in a.items() if t != drop)
    na = sum(v["total"] for t, v in a.items() if t != drop)
    ub = sum(v["unsupported"] for t, v in b.items() if t != drop)
    nb = sum(v["total"] for t, v in b.items() if t != drop)
    return ua, na, ub, nb, fisher_exact(ua, na - ua, ub, nb - ub)


def main() -> int:
    a, b = tjs.judging_counts(LOCAL, "raw"), tjs.judging_counts(HOSTED, "raw")
    ua, na, ub, nb, p = fisher(a, b)
    print(f"Pooled (claim-level): {LOCAL} {ua}/{na} = {ua / na:.2%} vs {HOSTED} {ub}/{nb} = "
          f"{ub / nb:.2%}; exact two-sided Fisher p = {mas.fmt_p(p)}")

    pr = tjs.paired_only(tjs.ticker_rates([a]), tjs.ticker_rates([b]), "rate")
    print(f"Paired ticker-level bootstrap on per-ticker rates (multi_arm_stats.paired, seed 0, "
          f"10,000 resamples), {pr['tickers']} tickers:")
    print(f"  ticker-averaged {pr['mean_a']:.2%} vs {pr['mean_b']:.2%}; difference "
          f"{pr['mean_diff'] * 100:+.2f} pts (95% bootstrap CI {pr['ci'][0] * 100:+.2f} to "
          f"{pr['ci'][1] * 100:+.2f})")
    print(f"  {LOCAL} higher on {pr['a_more']} tickers, equal on {pr['equal']}, {HOSTED} higher on "
          f"{pr['b_more']}; exact two-sided sign test p = {mas.fmt_p(pr['sign_p'])}")

    loo = sorted((fisher(a, b, t)[4], t) for t in sorted(set(a) & set(b)))
    hi_p, hi_t = loo[-1]
    ua, na, ub, nb, _ = fisher(a, b, hi_t)
    print(f"Leave-one-ticker-out Fisher (claim-level), {len(loo)} drops: p from "
          f"{mas.fmt_p(loo[0][0])} to {mas.fmt_p(hi_p)}; the largest p drops {hi_t} "
          f"({a[hi_t]['unsupported']}/{a[hi_t]['total']} vs {b[hi_t]['unsupported']}/{b[hi_t]['total']}): "
          f"{ua}/{na} vs {ub}/{nb}")
    over = [t for p_, t in loo if p_ >= 0.01]
    print(f"  drops leaving p >= 0.01: {', '.join(over) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
