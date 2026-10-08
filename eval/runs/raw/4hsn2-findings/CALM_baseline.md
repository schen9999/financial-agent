# CALM — baseline

## Metadata

ticker: CALM
arm: baseline
judge_prompt_version: v2
context_sha256: cbfe64c2b0f72e888fbd037fd87218bccba328a5845fd63c5791feb16876a73d
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 485, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.257, "latency_s_total": 5.257, "parse_failure": 0, "prompt_tokens": 2912, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 409, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.323, "latency_s_total": 5.323, "parse_failure": 0, "prompt_tokens": 2911, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 189, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.311, "latency_s_total": 2.311, "parse_failure": 0, "prompt_tokens": 703, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 189, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.638, "latency_s_total": 2.638, "parse_failure": 0, "prompt_tokens": 696, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 181, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.055, "latency_s_total": 2.055, "parse_failure": 0, "prompt_tokens": 482, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 221, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.602, "latency_s_total": 2.602, "parse_failure": 0, "prompt_tokens": 566, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1315, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.089, "latency_s_total": 19.089, "parse_failure": 0, "prompt_tokens": 1964, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "CALM",
  "company_name": "Cal-Maine Foods, Inc.",
  "current_price": 64.99,
  "currency": "USD",
  "market_cap": 3035722496.0,
  "pe_ratio": 52.837395,
  "forward_pe": 64.02956,
  "week_52_high": 95.57,
  "week_52_low": 63.5,
  "financial_currency": "USD",
  "revenue": 2528636928.0,
  "net_income": 58727000.0,
  "profit_margin_pct": 2.32,
  "dividend_yield": 3.77,
  "sector": "Consumer Defensive",
  "industry": "Farm Products"
}

NEWS ARTICLES:
[
  {
    "title": null,
    "source": null,
    "published_at": null,
    "description": null
  }
]

SEC FILING SUMMARIES:
{
  "10-K": {
    "form_type": "10-K",
    "filing_date": "2026-07-22",
    "summary": "Item 1A. Risk Factors and elsewhere in this report as well as those included in other reports we file from time to time with the Securities and Exchange Commission (the \u201cSEC\u201d) (including our Quarterly Reports on Form 10-Q and Current Reports on Form 8-K), (ii) changes in wholesale shell egg market prices, (iii) changes in the demand for shell eggs and our prepared foods offerings, (iv) increases in feed costs for our shell egg operations as well as increases in input costs for prepared foods, (v) our ability to predict and meet demand for cage -free and other specialty eggs, (vi) the risks and hazards inherent in shell egg, egg products and prepared foods operations (including, as applicable, disease, pests, weather conditions, and potential for product recall), including but not limited t"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-09-30",
    "summary": "Item 1A Risk Factors of our 202 6 Annual Report, as well as those included in other reports we file from time to time with the Securities and Exchange Commission (the \u201cSEC\u201d) (including our Quarterly Reports on Form 10-Q and Current Reports on Form 8-K). The actual timing, number and value of shares repurchased under our share repurchase program will be determined by management in its discretion and will depend on a number of factors, including but not limited to, the market price of our Common Stock and general market and economic conditions. The share repurchase program may be suspended, modified or discontinued at any time without prior notice. Readers are cautioned not to place undue reliance on forward -looking statements because, while we believe the assumptions on which the forward -"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] # Key Takeaways from Cal-Maine Foods' Recent SEC Filings

## Company Overview
Cal-Maine Foods is the largest egg company in the United States and a leading player in the egg-based food industry. Founded in 1957 and headquartered in Ridgeland, Mississippi, the company operates a vertically integrated business spanning conventional and specialty shell eggs, egg products, and prepared foods.

## Business Portfolio
The company offers a comprehensive range of products including:
- **Shell eggs**: Conventional, cage-free, nutritionally enhanced, organic, brown, pasture-raised, and free-range varieties
- **Prepared foods**: Pre-cooked egg patties, omelets, scrambled eggs, hard-cooked eggs, pancakes, waffles, and specialty wraps
- **Branded offerings**: Eggland's Best®, Land O'Lakes®, Farmhouse Eggs®, 4Grain®, Sunups®, Van's®, MeadowCreek Foods®, and Crepini®

## Strategic Growth Initiatives
The company is pursuing several expansion projects:
- Echo Lake Foods capacity expansion adding 17 million pounds of scrambled egg production and 12 million pounds of pancake production by mid-to-late fiscal 2027
- Crepini Foods joint venture adding 18 million pounds of production capacity by early-to-mid fiscal 2028
- Overall prepared foods capacity expected to grow over 30% from mid-2027 through 2028

## Recent Acquisitions
Significant acquisitions completed include:
- Echo Lake Foods ($289.5 million) - June 2025
- Creighton Brothers ($129.3 million) - March 2026
- ISE America - First quarter fiscal 2025
- Van's Foods assets ($24.8 million) - May 2026
- Clean Egg assets ($23.7 million) - October 2025

## Risk Factors
Key risks include HPAI (Highly Pathogenic Avian Influenza) impacts, feed cost volatility, market price fluctuations, integration challenges from acquisitions, and regulatory changes.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors

The company discloses the following primary risk factors:

1. **Market Price Volatility** - Changes in wholesale shell egg market prices and demand for shell eggs and prepared foods offerings

2. **Input Cost Increases** - Rising feed costs for shell egg operations and increased input costs for prepared foods

3. **Specialty Product Demand** - Ability to predict and meet demand for cage-free and other specialty eggs

4. **Operational Hazards** - Risks inherent in shell egg, egg products, and prepared foods operations including disease, pests, weather conditions, and product recall potential. Notably, this includes the current outbreak of Highly Pathogenic Avian Influenza (HPAI) affecting poultry in the U.S., Canada, and other countries, which impacted operations in fiscal 2024 and again in March 2026

5. **Acquisition Integration** - Risks related to acquiring new flocks or businesses and the ability to successfully integrate and manage recently acquired businesses while realizing expected benefits such as synergies, cost savings, and margin expansion

6. **Operational Efficiency** - Ability to produce, supply, and distribute products efficiently and reliably

7. **Competition** - Ability to compete effectively with existing competitors and new market entrants, retain customers, and grow product mix

8. **Regulatory and Market Reactions** - Government, customer, and consumer reactions to high egg market prices, including potential new regulations

9. **Economic Factors** - Changes in inflation, interest rates, and trade and tariff policies

10. **Intellectual Property** - Loss or expiration of registered trademarks and other intellectual property

11. **Litigation** - Adverse results in pending litigation and legal matters

12. **Geopolitical Risks** - Global instability from geopolitical conflicts and other uncertainties

## Pre-written sections (judge input)

### Financial Health

Cal-Maine Foods trades at $64.99 with a market capitalization of $3.04 billion, generating $2.53 billion in annual revenue. However, the company's profitability is notably thin, with a net profit margin of just 2.32%, reflecting the commodity-driven nature of egg production and exposure to volatile feed costs. The elevated P/E ratio of 52.84x and forward P/E of 64.03x suggest the stock is priced at a significant premium relative to current earnings, indicating market expectations for future improvement or reflecting cyclical recovery pricing. The 3.77% dividend yield provides some income support, though investors should monitor margin pressures from input cost inflation and commodity price fluctuations. Overall, CALM presents a capital-intensive, low-margin business with meaningful operational risks that warrant careful valuation consideration.

### Recent Developments

Cal-Maine Foods' most recent SEC filings highlight ongoing operational challenges including volatile feed costs, demand fluctuations for specialty egg products, and inherent production risks such as disease and weather conditions. The company's latest 10-Q filing (September 30, 2026) indicates management is actively managing capital through share repurchase programs, though execution remains discretionary based on market conditions and stock price. With a forward P/E of 64.03x significantly elevated above the current 52.84x P/E ratio, the market is pricing in expectations for improved profitability that may be difficult to achieve given the thin 2.32% profit margin and commodity-driven industry dynamics. Investors should monitor upcoming quarterly results for trends in cage-free egg adoption and input cost management, as these will be critical to justifying the stock's current valuation premium.

### SEC Filing Highlights

Cal-Maine Foods, the largest U.S. egg producer, is executing an aggressive growth strategy centered on prepared foods expansion, with major capacity additions planned through 2028 via the Echo Lake Foods and Crepini Foods joint venture projects expected to increase prepared foods capacity by over 30%. The company has completed several strategic acquisitions including Echo Lake Foods ($289.5M), Creighton Brothers ($129.3M), and Van's Foods assets ($24.8M), diversifying its portfolio beyond commodity shell eggs into higher-margin prepared food products. However, the company faces significant operational risks from Highly Pathogenic Avian Influenza (HPAI), feed cost volatility, and integration challenges from recent acquisitions that could impact profitability and execution timelines. Cal-Maine's vertically integrated model and portfolio of premium brands (Eggland's Best®, Van's®, Crepini®) position it to capture growing consumer demand for specialty and convenience egg products.

### Risk Factors

• **Avian Influenza and Operational Disruptions** - Highly Pathogenic Avian Influenza (HPAI) outbreaks pose significant operational and financial risks, having impacted operations in fiscal 2024 and again in March 2026, with potential for future flock losses and production disruptions.

• **Commodity Price Volatility** - Exposure to volatile wholesale shell egg market prices and rising input costs (particularly feed) directly impact margins, with limited ability to pass through cost increases to customers in a competitive market.

• **Specialty Product Demand Uncertainty** - Difficulty predicting and meeting evolving consumer demand for cage-free and specialty egg products, combined with competitive pressures and potential regulatory changes around production methods, could affect market share and profitability.

## Audited (Exec Summary + Outlook)

### Executive Summary
Cal-Maine Foods is the largest U.S. egg producer, generating $2.53 billion in annual revenue through a vertically integrated model that spans commodity shell eggs and a growing portfolio of premium and prepared food brands including Eggland's Best®, Van's®, and Crepini®. The stock is notable now because it trades at a significant valuation premium — a 52.84x current P/E and 64.03x forward P/E — despite a net profit margin of just 2.32%, creating a tension between the market's optimism around the company's prepared foods expansion strategy and the harsh realities of a commodity-driven, low-margin business undergoing simultaneous integration of multiple large acquisitions. The single most important near-term variable is whether Cal-Maine can successfully absorb its recent acquisitions and expand prepared foods capacity on schedule, as execution on that strategy is the primary justification for the stock's elevated valuation.

### Outlook
The directional outlook for Cal-Maine is **cautious**, with a path to becoming more constructive contingent on clear evidence of execution. The primary tailwind is the company's strategic pivot toward higher-margin prepared foods and premium branded products, which — if successfully integrated and scaled through the planned capacity additions — could meaningfully reduce its dependence on volatile commodity egg pricing over time. However, the headwinds are substantial and immediate: the stock's elevated valuation premium leaves little room for error, HPAI remains an unpredictable and recurring operational threat, feed cost inflation continues to pressure an already thin margin structure, and the company is simultaneously digesting multiple large acquisitions whose integration complexity should not be underestimated. Investors should watch four key variables — the pace and cost of prepared foods capacity expansion toward the 2028 targets, trends in cage-free and specialty egg adoption relative to the capital being deployed to serve that demand, the frequency and severity of any new HPAI outbreaks, and whether quarterly results show any meaningful improvement in profit margins. What would shift the view toward more constructive would be sustained evidence of margin expansion driven by the prepared foods mix shift and clean acquisition integration; what would deepen the caution would be further HPAI disruptions, integration setbacks, or continued margin compression that widens the gap between the stock's valuation and its underlying earnings power.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically identify every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections, then evaluate each one.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "generating $2.53 billion in annual revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $2,528,636,928, which rounds to $2.53 billion; the pre-written Financial Health section also states "$2.53 billion in annual revenue."

---

CLAIM: "a 52.84x current P/E"
LABEL: SUPPORTED
REASON: Source data lists pe_ratio as 52.837395, which rounds to 52.84x; confirmed in the pre-written Financial Health section as "52.84x."

---

CLAIM: "64.03x forward P/E"
LABEL: SUPPORTED
REASON: Source data lists forward_pe as 64.02956, which rounds to 64.03x; confirmed in the pre-written Financial Health section as "64.03x."

---

CLAIM: "a net profit margin of just 2.32%"
LABEL: SUPPORTED
REASON: Source data explicitly states profit_margin_pct as 2.32; confirmed in the pre-written Financial Health section.

---

**OUTLOOK**

---

CLAIM: "the planned capacity additions" toward "the 2028 targets"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state Crepini Foods joint venture adds capacity "by early-to-mid fiscal 2028," and overall prepared foods capacity is expected to grow "over 30% from mid-2027 through 2028," establishing 2028 as a stated target horizon.

---

CLAIM: "prepared foods capacity expansion toward the 2028 targets"
LABEL: SUPPORTED
REASON: Same as above — the RAG SEC Highlights explicitly reference fiscal 2028 as the endpoint for the capacity expansion program.

---

*(No additional standalone quantitative figures, price targets, specific thresholds, ratios, or percentages appear in the Outlook section beyond the 2028 milestone reference already evaluated above. The remaining Outlook language is qualitative/directional and contains no further auditable quantitative claims.)*

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | $2.53 billion in annual revenue | SUPPORTED |
| 2 | 52.84x current P/E | SUPPORTED |
| 3 | 64.03x forward P/E | SUPPORTED |
| 4 | Net profit margin of 2.32% | SUPPORTED |
| 5 | Prepared foods capacity expansion toward 2028 targets | SUPPORTED |

All five auditable quantitative or milestone claims in the Executive Summary and Outlook are **SUPPORTED** by the source data. No figures failed arithmetic recheck, no period labels were mismatched, and no figures were found to be absent from the source context.
