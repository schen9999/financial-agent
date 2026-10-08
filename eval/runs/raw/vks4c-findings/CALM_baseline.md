# CALM — baseline

## Metadata

ticker: CALM
arm: baseline
judge_prompt_version: v2
context_sha256: f707af0a00f6ff6e2b1e7b9d66905ef78ed9c2b238fe2d0949ea97f6db46d519
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 512, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.819, "latency_s_total": 5.819, "parse_failure": 0, "prompt_tokens": 2912, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 395, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.072, "latency_s_total": 5.072, "parse_failure": 0, "prompt_tokens": 2911, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 179, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.168, "latency_s_total": 2.168, "parse_failure": 0, "prompt_tokens": 680, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 158, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.196, "latency_s_total": 2.196, "parse_failure": 0, "prompt_tokens": 673, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 177, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.175, "latency_s_total": 2.175, "parse_failure": 0, "prompt_tokens": 468, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 194, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.358, "latency_s_total": 2.358, "parse_failure": 0, "prompt_tokens": 593, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1241, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 18.035, "latency_s_total": 18.035, "parse_failure": 0, "prompt_tokens": 1820, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "CALM",
  "company_name": "Cal-Maine Foods, Inc.",
  "current_price": 62.7,
  "currency": "USD",
  "market_cap": 2928755456.0,
  "pe_ratio": 51.39344,
  "forward_pe": 61.7734,
  "week_52_high": 95.57,
  "week_52_low": 61.88,
  "financial_currency": "USD",
  "revenue": 2528636928.0,
  "net_income": 58727000.0,
  "profit_margin_pct": 2.32,
  "dividend_yield": 3.86,
  "sector": "Consumer Defensive",
  "industry": "Farm Products"
}

NEWS ARTICLES:
[]

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
Cal-Maine Foods is the largest egg company in the United States and a leading player in the egg-based food industry. Founded in 1957 and headquartered in Ridgeland, Mississippi, the company operates a vertically integrated business spanning shell eggs (conventional and specialty) and prepared foods.

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
Significant acquisitions in the past two fiscal years include:
- Echo Lake Foods ($289.5 million) - June 2025
- Creighton Brothers LLC ($129.3 million) - March 2026
- ISE America assets - First quarter fiscal 2025
- Van's Foods assets ($24.8 million) - May 2026
- Clean Egg LLC ($23.7 million) - October 2025
- Crepini Foods joint venture (51% stake) - Second quarter fiscal 2025

## Risk Factors
Key risks include HPAI (Highly Pathogenic Avian Influenza) impacts, feed cost volatility, market price fluctuations, integration challenges from acquisitions, and competitive pressures.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors affecting its business:

**Market and Operational Risks:**
- Fluctuations in wholesale shell egg market prices
- Changes in demand for shell eggs and prepared foods offerings
- Increases in feed costs and input costs for prepared foods
- Ability to predict and meet demand for cage-free and specialty eggs

**Disease and Production Hazards:**
- Risks inherent in shell egg, egg products, and prepared foods operations including disease, pests, and weather conditions
- The current outbreak of Highly Pathogenic Avian Influenza (HPAI) affecting poultry in the U.S., Canada, and other countries, which impacted the company's flocks in fiscal 2024 and again in March 2026
- Potential for product recalls

**Acquisition and Integration Risks:**
- Risks and changes resulting from recent or future acquisitions, such as the Echo Lake Foods acquisition completed in June 2025
- Risks that conditions for completing pending acquisitions may not be met
- Ability to successfully integrate recently acquired businesses and realize expected benefits including synergies, cost savings, and margin expansion

**Competitive and Commercial Risks:**
- Ability to compete effectively with existing competitors and new market entrants
- Ability to retain existing customers and acquire new customers
- Ability to grow the product mix, particularly prepared foods offerings

**External and Regulatory Risks:**
- Government, customer, and consumer reactions to high egg market prices and potential new regulations
- Changes in inflation, interest rates, and trade and tariff policies
- Global instability from geopolitical conflicts and other uncertainties
- Loss or expiration of registered trademarks or intellectual property
- Adverse results in pending litigation and legal matters

## Pre-written sections (judge input)

### Financial Health

Cal-Maine Foods trades at $62.70 with a market capitalization of $2.93 billion and generates $2.53 billion in annual revenue. The company's valuation appears stretched with a P/E ratio of 51.4x and forward P/E of 61.8x, significantly above industry averages, while profitability remains thin at a 2.32% net profit margin with only $58.7 million in net income. The elevated valuation multiples relative to modest earnings suggest the market is pricing in future growth or recovery, though the company's exposure to commodity egg prices and input cost volatility presents material risk. A 3.86% dividend yield provides some income support, but investors should monitor operational efficiency and margin expansion given the cyclical nature of the farm products sector.

### Recent Developments

Cal-Maine Foods' most recent filings reveal ongoing operational challenges typical of the egg production industry, with the company facing volatility in wholesale shell egg prices, feed cost pressures, and demand fluctuations for specialty products like cage-free eggs. The company maintains an active share repurchase program, suggesting management confidence despite a challenging operating environment. However, the stock's elevated forward P/E ratio of 61.77x and thin profit margin of 2.32% reflect the cyclical nature of commodity egg production and limited pricing power. Investors should monitor upcoming quarterly results for trends in feed costs and cage-free product adoption, as these will be critical drivers of profitability in an industry facing structural headwinds.

### SEC Filing Highlights

Cal-Maine Foods, the largest U.S. egg producer, is executing an aggressive diversification strategy through significant acquisitions in prepared foods, including Echo Lake Foods ($289.5M), Creighton Brothers ($129.3M), and a majority stake in Crepini Foods, with combined capacity expansions expected to grow prepared foods output over 30% by 2028. The company maintains a vertically integrated portfolio spanning conventional and specialty shell eggs alongside branded prepared food products (Eggland's Best®, Van's®, Sunups®, Crepini®), positioning it to capture higher-margin value-added segments. However, the company faces material risks from Highly Pathogenic Avian Influenza (HPAI), feed cost volatility, and integration execution challenges from its recent acquisition spree, which could pressure margins and operational efficiency.

### Risk Factors

- **Highly Pathogenic Avian Influenza (HPAI) Exposure**: The company's flocks have been directly impacted by HPAI outbreaks in fiscal 2024 and March 2026, creating significant production disruptions and potential for future flock losses that could materially affect supply and profitability.

- **Commodity Price Volatility**: Wholesale shell egg prices and feed costs are subject to substantial fluctuations driven by market supply/demand dynamics and input inflation, directly impacting margins and earnings predictability.

- **Acquisition Integration Risk**: Recent acquisitions (Echo Lake Foods in June 2025) and pending deals carry execution risk; failure to successfully integrate operations and realize expected synergies and cost savings could impair shareholder value.

## Audited (Exec Summary + Outlook)

### Executive Summary
Cal-Maine Foods is the largest U.S. egg producer, operating a vertically integrated portfolio across conventional and specialty shell eggs and branded prepared food products, generating $2.53 billion in annual revenue with a market capitalization of $2.93 billion. The stock is notable now because its valuation — a P/E of 51.4x and forward P/E of 61.8x — appears significantly stretched relative to a 2.32% net profit margin, even as the company pursues an aggressive acquisition-driven pivot toward higher-margin prepared foods that the market may be pricing in ahead of demonstrated results. The single most important near-term variable is whether Cal-Maine can successfully integrate its recent acquisitions while managing HPAI-related flock disruptions, as the combination of execution risk and biological risk could determine whether the premium valuation is ultimately justified or unwound.

### Outlook
The directional outlook for Cal-Maine Foods is **cautious**, with the investment thesis hinging on the company's ability to execute a meaningful business transformation rather than on the strength of its current fundamentals. The primary tailwind is the strategic pivot toward higher-margin, value-added prepared foods — a credible long-term direction that, if executed well, could reduce the company's dependence on volatile commodity egg prices and justify a premium valuation over time. However, the headwinds are substantial and immediate: HPAI remains an unpredictable biological risk that has already disrupted operations in fiscal 2024 and March 2026; feed cost inflation can compress already thin margins with little warning; and the company is simultaneously digesting multiple large acquisitions, each carrying its own integration complexity. Investors should watch the trajectory of prepared foods margins and revenue contribution in upcoming quarterly results, the pace and cost of cage-free adoption, any new HPAI developments affecting flock size, and early evidence of synergy realization from the Echo Lake Foods and Creighton Brothers integrations. The cautious stance would shift toward more constructive if Cal-Maine demonstrates meaningful margin expansion in its prepared foods segment, maintains flock stability through the current HPAI environment, and shows disciplined integration execution — conversely, further flock losses, rising feed costs without offsetting pricing power, or acquisition missteps would reinforce and deepen the cautious view.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

## EXECUTIVE SUMMARY

---

CLAIM: "the largest U.S. egg producer"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "Cal-Maine Foods is the largest egg company in the United States."

---

CLAIM: "$2.53 billion in annual revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $2,528,636,928, which rounds to $2.53 billion; the pre-written Financial Health section also states "$2.53 billion in annual revenue."

---

CLAIM: "market capitalization of $2.93 billion"
LABEL: SUPPORTED
REASON: Source data shows market_cap of $2,928,755,456, which rounds to $2.93 billion; confirmed in the pre-written Financial Health section.

---

CLAIM: "a P/E of 51.4x"
LABEL: SUPPORTED
REASON: Source data shows pe_ratio of 51.39344, which rounds to 51.4x.

---

CLAIM: "forward P/E of 61.8x"
LABEL: SUPPORTED
REASON: Source data shows forward_pe of 61.7734, which rounds to 61.8x.

---

CLAIM: "2.32% net profit margin"
LABEL: SUPPORTED
REASON: Source data explicitly states profit_margin_pct of 2.32.

---

CLAIM: "HPAI-related flock disruptions"
LABEL: SUPPORTED
REASON: The RAG Risk Factors section confirms HPAI outbreaks impacted the company's flocks in fiscal 2024 and March 2026.

---

## OUTLOOK

---

CLAIM: "HPAI remains an unpredictable biological risk that has already disrupted operations in fiscal 2024 and March 2026"
LABEL: SUPPORTED
REASON: The RAG Risk Factors section explicitly states HPAI "impacted the company's flocks in fiscal 2024 and again in March 2026."

---

CLAIM: "the Echo Lake Foods and Creighton Brothers integrations"
LABEL: SUPPORTED
REASON: Both acquisitions are named in the RAG SEC Highlights (Echo Lake Foods at $289.5M, June 2025; Creighton Brothers LLC at $129.3M, March 2026) and in the pre-written SEC Filing Highlights section.

---

CLAIM: "the pace and cost of cage-free adoption" [as a watch item]
LABEL: SUPPORTED
REASON: The RAG Risk Factors and SEC filing summaries explicitly identify "ability to predict and meet demand for cage-free and other specialty eggs" as a disclosed risk and operational variable.

---

**No additional quantitative figures, price targets, thresholds, ratios, named product milestones, or forward-looking numbers appear in the Outlook section beyond those already audited above.** The remaining content of the Outlook is qualitative directional language (e.g., "cautious," "meaningful margin expansion," "disciplined integration execution") without specific numerical claims requiring verification.

---

### Summary Table

| Claim | Label |
|---|---|
| Largest U.S. egg producer | SUPPORTED |
| $2.53 billion annual revenue | SUPPORTED |
| $2.93 billion market cap | SUPPORTED |
| P/E of 51.4x | SUPPORTED |
| Forward P/E of 61.8x | SUPPORTED |
| 2.32% net profit margin | SUPPORTED |
| HPAI flock disruptions | SUPPORTED |
| HPAI disruptions in fiscal 2024 and March 2026 | SUPPORTED |
| Echo Lake Foods and Creighton Brothers integrations | SUPPORTED |
| Cage-free adoption as watch item | SUPPORTED |

**All audited claims are SUPPORTED.** No unsupported or inference-only quantitative claims were identified in the Executive Summary or Outlook sections.
