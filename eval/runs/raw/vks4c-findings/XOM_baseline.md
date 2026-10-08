# XOM — baseline

## Metadata

ticker: XOM
arm: baseline
judge_prompt_version: v2
context_sha256: 890b81838c02591ecb012337ef2779471a3ba99588e1f2f937ac4c03db8fe001
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 435, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.876, "latency_s_total": 4.876, "parse_failure": 0, "prompt_tokens": 2481, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 192, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.803, "latency_s_total": 2.803, "parse_failure": 0, "prompt_tokens": 3314, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 162, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.023, "latency_s_total": 2.023, "parse_failure": 0, "prompt_tokens": 497, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 147, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.934, "latency_s_total": 1.934, "parse_failure": 0, "prompt_tokens": 490, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 131, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.786, "latency_s_total": 1.786, "parse_failure": 0, "prompt_tokens": 266, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 206, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.242, "latency_s_total": 2.242, "parse_failure": 0, "prompt_tokens": 517, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1143, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.18, "latency_s_total": 17.18, "parse_failure": 0, "prompt_tokens": 1698, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "XOM",
  "company_name": "ExxonMobil Holdings Corporation",
  "current_price": 164.05,
  "currency": "USD",
  "market_cap": 674559164416.0,
  "pe_ratio": 21.113256,
  "forward_pe": 14.400975,
  "week_52_high": 176.41,
  "week_52_low": 110.39,
  "financial_currency": "USD",
  "revenue": 361060007936.0,
  "net_income": 32757000192.0,
  "profit_margin_pct": 9.07,
  "dividend_yield": 2.5,
  "sector": "Energy",
  "industry": "Oil & Gas Integrated"
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
    "message": "No 10-K found"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-03",
    "summary": "Item 1A. Risk Factors\" of ExxonMobil\u2019s 2025 Form 10-K. Forward-looking and other statements regarding environmental and other sustainability efforts and aspirations are not an indication that these statements are material to investors or require disclosure in our filing with the SEC or any other regulatory authority. In addition, historical, current, and forward-looking environmental and other sustainability-related statements may be based on standards for measuring progress that are still developing, internal controls and processes that continue to evolve, and assumptions that are subject to change in the future, including future rule-making. Actions needed to advance ExxonMobil\u2019s 2030 greenhouse gas emission-reductions plans are incorporated into its medium term business plans, which are"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] # Key Takeaways from ExxonMobil's Latest Filings

## Financial Performance
- **Upstream Earnings**: Total upstream earnings reached $7.9 billion in Q2 2026 (compared to $5.4 billion in Q2 2025) and $13.7 billion year-to-date
- **Shareholder Returns**: The company distributed $8.6 billion in dividends and repurchased $10.0 billion of common stock

## Production & Operations
- **Oil-Equivalent Production**: Declined to 4,514 thousand barrels daily in Q2 2026 from 4,630 in Q2 2025, primarily due to Middle East disruptions, divestments, and entitlement changes
- **Production Mix**: Crude oil production of 3,373 thousand barrels daily in Q2 2026, with natural gas production at 6,849 million cubic feet daily

## Earnings Drivers
- **Positive Factors**: Price increases added $4.65 billion in Q2 earnings (higher crude realizations), and advantaged volume growth contributed $1.14 billion, mainly from Guyana and Permian expansion
- **Negative Factors**: Middle East volume disruptions reduced earnings by $1.06 billion in Q2; higher depreciation expenses decreased earnings by $690 million

## Market Conditions
- Crude oil prices remained within the 10-year historical range despite supply disruptions in the Middle East
- Natural gas prices stayed elevated above the 10-year average
- Global refining margins were sharply above historical ranges due to unprecedented capacity reductions

## Strategic Focus
- Advantaged assets (Permian, Guyana, and LNG) continue driving growth
- Structural cost savings contributed $170 million in Q2 2026
- Environmental commitments are being incorporated into medium-term business plans with 2030 greenhouse gas reduction targets

RAG — RISK FACTORS:
[From Pinecone cache] Based on the provided context, the document references risk factors but does not provide a detailed list of the primary risk factors themselves. The context only includes a brief mention that states: "Item 1A. Risk Factors" of ExxonMobil's 2025 Form 10-K."

This indicates that comprehensive risk factor disclosures are contained in that section of the 2025 Form 10-K filing, but the specific primary risk factors are not detailed in the excerpts provided. The context does mention that forward-looking statements regarding environmental and sustainability efforts are not necessarily material to investors or required SEC disclosure, and it notes that historical and forward-looking environmental statements may be based on developing standards and evolving internal controls.

To obtain the complete list of primary risk factors, you would need to refer directly to Item 1A of the 2025 Form 10-K filing.

## Pre-written sections (judge input)

### Financial Health

ExxonMobil trades at $164.05 with a market capitalization of $674.6 billion, demonstrating substantial scale within the energy sector. The company generated $361.1 billion in revenue with a net profit margin of 9.07%, translating to $32.8 billion in net income, reflecting solid operational profitability. The current P/E ratio of 21.1x appears elevated relative to the forward P/E of 14.4x, suggesting market expectations for earnings growth or potential valuation compression. With a 2.5% dividend yield and strong cash generation, XOM maintains financial stability, though investors should monitor commodity price exposure and energy transition risks outlined in recent SEC filings.

### Recent Developments

ExxonMobil's most recent 10-Q filing (August 3, 2026) highlights the company's ongoing integration of greenhouse gas emission-reduction targets into its medium-term business plans, with specific actions outlined to meet 2030 goals. The company continues to refine its sustainability measurement standards and internal controls, though it notes these frameworks remain evolving. With a forward P/E of 14.4x and a 2.5% dividend yield, XOM appears reasonably valued relative to its energy sector peers, though investors should monitor execution risks around the company's environmental commitments and their potential impact on capital allocation and profitability.

### SEC Filing Highlights

ExxonMobil delivered strong upstream earnings of $7.9 billion in Q2 2026, up 46% year-over-year, driven primarily by higher crude oil prices which added $4.65 billion in earnings, though production declined to 4,514 thousand barrels daily due to Middle East disruptions and divestments. The company returned $18.6 billion to shareholders in the first half of 2026 through $8.6 billion in dividends and $10.0 billion in share repurchases. Growth from advantaged assets in Guyana and the Permian contributed $1.14 billion in positive earnings, offsetting a $1.06 billion headwind from Middle East volume disruptions. Structural cost savings of $170 million in Q2 demonstrate operational efficiency gains, while global refining margins remained sharply above historical ranges despite elevated depreciation expenses.

### Risk Factors

• **Energy Transition and Regulatory Risk** – Evolving environmental regulations and the global shift toward renewable energy could impact demand for fossil fuels and require significant capital reallocation to maintain competitiveness.

• **Commodity Price Volatility** – Fluctuations in crude oil and natural gas prices directly affect revenues and profitability, exposing the company to market cyclicality and geopolitical uncertainties.

• **Environmental and Sustainability Compliance** – Increasing disclosure requirements and developing environmental standards may impose operational constraints and capital requirements as regulatory frameworks continue to evolve.

## Audited (Exec Summary + Outlook)

### Executive Summary
ExxonMobil is one of the world's largest integrated energy companies, generating $361.1 billion in revenue and $32.8 billion in net income, with a market capitalization of $674.6 billion that reflects its dominant scale across upstream, downstream, and refining operations. The stock is notable now because a meaningful gap between the current P/E of 21.1x and the forward P/E of 14.4x signals that the market is pricing in meaningful earnings growth, while Q2 2026 upstream earnings surged 46% year-over-year on higher crude prices — creating a compelling but commodity-dependent setup. The single most important near-term variable is the trajectory of crude oil prices, which drove the majority of the Q2 earnings beat and remain the primary lever over profitability and shareholder return capacity.

### Outlook
The directional outlook for XOM is cautiously constructive, supported by several identifiable tailwinds: continued above-historical refining margins, growing production contributions from advantaged low-cost assets in Guyana and the Permian, a demonstrated commitment to shareholder returns, and ongoing structural cost discipline. However, the thesis carries meaningful headwinds that investors must monitor closely. Crude oil price direction remains the dominant variable — a sustained decline would compress upstream earnings sharply, given how heavily Q2 results depended on price rather than volume. Production recovery in the Middle East and the pace of divestment activity will determine whether volume headwinds ease or persist. On the longer-duration side, investors should watch the pace and stringency of evolving environmental regulations, the credibility of ExxonMobil's execution against its 2030 emissions targets, and how those commitments shape capital allocation over time. What would strengthen the thesis: stabilizing or rising crude prices, volume recovery from disrupted regions, and demonstrated progress on sustainability frameworks that reduce regulatory overhang. What would weaken it: a sustained commodity price downturn, escalating geopolitical disruptions to production, or regulatory developments that accelerate capital reallocation away from core fossil fuel operations before low-carbon alternatives reach sufficient scale.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$361.1 billion in revenue"
LABEL: SUPPORTED
REASON: Source data lists revenue as $361,060,007,936, which rounds to $361.1 billion; also confirmed in the Financial Health pre-written section.

---

CLAIM: "$32.8 billion in net income"
LABEL: SUPPORTED
REASON: Source data lists net income as $32,757,000,192, which rounds to $32.8 billion; also confirmed in the Financial Health pre-written section.

---

CLAIM: "market capitalization of $674.6 billion"
LABEL: SUPPORTED
REASON: Source data lists market_cap as $674,559,164,416, which rounds to $674.6 billion; confirmed in the Financial Health pre-written section.

---

CLAIM: "current P/E of 21.1x"
LABEL: SUPPORTED
REASON: Source data lists pe_ratio as 21.113256, which rounds to 21.1x; confirmed in the Financial Health pre-written section.

---

CLAIM: "forward P/E of 14.4x"
LABEL: SUPPORTED
REASON: Source data lists forward_pe as 14.400975, which rounds to 14.4x; confirmed in the Financial Health pre-written section.

---

CLAIM: "Q2 2026 upstream earnings surged 46% year-over-year"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states upstream earnings were $7.9 billion in Q2 2026 vs. $5.4 billion in Q2 2025; computed YoY growth = (7.9 − 5.4) / 5.4 = 46.3%, which rounds to 46% — within 0.15 pp; also stated explicitly in the SEC Filing Highlights pre-written section.

---

**OUTLOOK**

---

CLAIM: "above-historical refining margins"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "Global refining margins were sharply above historical ranges due to unprecedented capacity reductions," which directly supports this directional claim.

---

CLAIM: "growing production contributions from advantaged low-cost assets in Guyana and the Permian"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "advantaged volume growth contributed $1.14 billion, mainly from Guyana and Permian expansion," and the Strategic Focus section confirms these as advantaged assets driving growth.

---

CLAIM: "ExxonMobil's execution against its 2030 emissions targets"
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly references "2030 greenhouse gas emission-reductions plans," and the 10-Q summary references "2030 greenhouse gas reduction targets"; the 2030 milestone is present in the source data.

---

CLAIM: "how heavily Q2 results depended on price rather than volume"
LABEL: SUPPORTED
REASON: RAG SEC Highlights shows price increases added $4.65 billion vs. advantaged volume growth of $1.14 billion in Q2 2026, confirming price was the dominant earnings driver relative to volume — this is a directional/qualitative claim fully supported by those figures.

---

*No additional standalone quantitative figures, price targets, specific thresholds, ratios, or named product milestones appear in the Outlook section beyond those audited above. All claims in the Executive Summary and Outlook have been evaluated.*
