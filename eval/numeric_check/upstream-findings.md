# Numeric check: upstream data findings (2026-09-29, not fixed)

Found while building the deterministic numeric check (agent/numeric_check.py,
branch numeric-check) and its backtest over the committed findings
(scripts/numeric_backtest.py, eval/runs/numeric-backtest-2026-09-29.json).
Neither is fixed on this branch, on purpose: both live in the stock data the
pipeline hands the generators, so a fix changes eval inputs and every run
after it stops being comparable with the committed ones. Fix them in a
separate, dated change with a fresh baseline.

## (a) Reporting currency is dropped for foreign filers

`agent/tools/stock.py` fills `currency` from yfinance `info["currency"]`
(the trading currency of the listing, USD for these ADRs) and never reads
`info["financialCurrency"]`. `revenue` and `net_income` come from
`totalRevenue` / `netIncomeToCommon`, which yfinance reports in the filer's
financial currency. The stock dict therefore labels home-currency figures
as USD.

What the committed dicts hold (j4cnp files; every dict says
`"currency": "USD"`):

| Ticker | revenue | net_income | Scale consistent with |
|---|---|---|---|
| TM | 51,957,024,686,080 | 4,483,796,959,232 | JPY |
| TSM | 4,440,492,343,296 | 2,216,808,415,232 | TWD |
| NVO | 329,430,990,848 | 116,442,996,736 | DKK |
| BABA | 1,044,970,995,712 | 73,325,002,752 | CNY |
| SAP | 38,192,001,024 | 7,795,999,744 | EUR (close to USD scale, so it hides) |

The currency column is inferred from magnitudes; it was not checked against a
live yfinance call (the backtest is offline by design). market_cap and
current_price look like USD.

Effect on the backtest: every 40-ticker full run has at least one TM, TSM,
NVO or BABA revenue/net_income flag, hosted included (for example TM "$52.0
billion" in annual revenue against 51.96T, ratio 0.001, in j4cnp, kcf7s and
dvvxk); 2nh8v's 10 tickers include none of them. These flags
compare the brief against a source whose unit is itself mislabeled, so a
verdict on them is a judgment about which figure the brief should have
stated. Keep that in mind when adjudicating. SAP's net_income flags (ratio
10.0 in lsnnc, v924f, r5nzh) are not currency effects: EUR and USD are
within 2x, so a 10x gap is the brief's own error.

Fix, later: carry `financialCurrency` into the stock dict (for example
`financial_currency`) and make the section prompts and the numeric check use
it for revenue and net_income.

## (b) profit_margin is a raw fraction, and briefs write it as a percent

`profit_margin` is passed straight from yfinance `profitMargins`, a fraction
(0.453 = 45.3%). For |fraction| < 1 the generators convert it correctly. Where
|fraction| > 1, briefs from every arm write the raw fraction with a percent
sign, 100x too small: LCID -2.49214 (-249%) becomes "-2.49%".

The four tickers in the corpus with |profit_margin| > 1, and how many of each
run's briefs stated the raw fraction as a percent (a profit_margin flag at
ratio ~0.01):

| Run | Arm / model | Briefs that wrote the fraction as a percent |
|---|---|---|
| j4cnp | hosted | 3 of 4 (BYND, LCID, OMER) |
| kcf7s | hosted | 2 of 4 (BYND, OMER) |
| dvvxk | hosted | 2 of 4 (LCID, OMER) |
| lsnnc | financial-lora | 3 of 4 (BYND, LCID, OMER) |
| v924f | financial-lora | 1 of 4 (OMER) |
| r5nzh | financial-lora-w4a16 | 3 of 4 (BYND, LCID, OMER) |
| 4nfsm | Qwen2.5-1.5B base | 1 of 4 (OMER) |
| cnkp2 | Qwen2.5-7B base | 4 of 4 (BYND, EDIT, LCID, OMER) |
| 9j2dj | hosted, partial (Exec Summary + Outlook only) | 0 of 4 |

Dict values: OMER 3.2488198, BYND 1.15852, EDIT -1.57322, LCID -2.49214.
2nh8v has none of the four tickers.

This is a data-presentation defect rather than a model defect: the hosted
arm makes it too. The unadjudicated counts above are flags; each still gets
a verdict in eval/numeric_check/adjudication.csv.

Fix, later: pass profit_margin as a percentage (or with an explicit
`profit_margin_pct` field) so no generator has to convert.
