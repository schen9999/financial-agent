# XOM — baseline

## Metadata

ticker: XOM
arm: baseline
judge_prompt_version: v2
context_sha256: f1410741e8b00aed477161f29cad8b7d0873b87757635f3743d6a23c06b789ea
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 388, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.914, "latency_s_total": 3.914, "parse_failure": 0, "prompt_tokens": 2481, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 285, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.838, "latency_s_total": 3.838, "parse_failure": 0, "prompt_tokens": 3314, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 193, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.307, "latency_s_total": 2.307, "parse_failure": 0, "prompt_tokens": 487, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 170, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.37, "latency_s_total": 2.37, "parse_failure": 0, "prompt_tokens": 480, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 160, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.987, "latency_s_total": 1.987, "parse_failure": 0, "prompt_tokens": 359, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 212, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.27, "latency_s_total": 2.27, "parse_failure": 0, "prompt_tokens": 470, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1314, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.982, "latency_s_total": 19.982, "parse_failure": 0, "prompt_tokens": 1876, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "XOM",
  "company_name": "ExxonMobil Holdings Corporation",
  "current_price": 164.01,
  "currency": "USD",
  "market_cap": 674394669056.0,
  "pe_ratio": 21.108107,
  "forward_pe": 14.50511,
  "week_52_high": 176.41,
  "week_52_low": 110.39,
  "revenue": 361060007936.0,
  "net_income": 32757000192.0,
  "profit_margin": 0.09072,
  "dividend_yield": 2.51,
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
- **Upstream Earnings**: Total upstream earnings reached $7.9 billion in Q2 2026 (compared to $5.4 billion in Q2 2025) and $13.7 billion for the first half of 2026 (versus $12.2 billion in the same period of 2025)
- **Shareholder Returns**: The company distributed $8.6 billion in dividends and repurchased $10.0 billion of common stock

## Production & Operations
- **Oil-Equivalent Production**: Declined to 4,514 thousand barrels daily in Q2 2026 from 4,630 in Q2 2025, primarily due to divestments and Middle East disruptions
- **Natural Gas Production**: Worldwide natural gas production decreased significantly, from 8,219 million cubic feet daily in Q2 2025 to 6,849 in Q2 2026

## Earnings Drivers
- **Positive Factors**: Higher crude oil realizations added $4.65 billion, while advantaged volume growth (mainly from Guyana and Permian) contributed $1.14 billion
- **Negative Factors**: Middle East disruptions reduced earnings by $1.06 billion in Q2, and higher depreciation expenses decreased earnings by $690 million

## Market Conditions & Strategy
- Supply disruptions in the Middle East and global refining capacity reductions significantly influenced market conditions
- The company is focused on advantaged assets including Permian, Guyana, and LNG projects
- Environmental and sustainability efforts are being incorporated into medium-term business plans with annual updates

RAG — RISK FACTORS:
[From Pinecone cache] Based on the provided context, the document references risk factors but does not provide a comprehensive list of them. The context only mentions that detailed risk factors can be found in "Item 1A. Risk Factors" of ExxonMobil's 2025 Form 10-K.

The context does indicate that the company acknowledges risks related to:

1. **Environmental and sustainability efforts** - The document notes that forward-looking statements regarding environmental and sustainability efforts are subject to evolving standards, internal controls that continue to evolve, and assumptions that may change in the future, including future rule-making.

2. **Policy and technology advancement** - The company recognizes that current trends for policy stringency and development of lower-emission solutions are not yet on a pathway to achieve net-zero by 2050, and that future policies and technology advancements will need to be incorporated into business plans.

3. **Project execution** - References to projects or opportunities may not reflect actual investment decisions, as individual projects may advance based on factors including availability of stable and supportive policy, permitting, technological advancement, and alignment with partners and stakeholders.

For a complete discussion of primary risk factors, the full "Item 1A. Risk Factors" section from the 2025 Form 10-K would need to be consulted.

## Pre-written sections (judge input)

### Financial Health

ExxonMobil trades at $164.01 with a market capitalization of $674.4 billion, demonstrating its position as a major energy sector player. The company generated $361.1 billion in revenue with a net profit margin of 9.1%, translating to $32.8 billion in net income, reflecting solid operational efficiency despite energy sector volatility. The current P/E ratio of 21.1x appears elevated relative to the forward P/E of 14.5x, suggesting market expectations for earnings growth or potential valuation compression. With a 2.51% dividend yield, XOM provides income-focused investors with steady returns while maintaining profitability. Overall, the company exhibits strong financial fundamentals with substantial cash generation, though valuation metrics warrant monitoring given energy sector cyclicality and the company's ongoing transition toward lower-carbon initiatives.

### Recent Developments

ExxonMobil's most recent 10-Q filing (August 3, 2026) highlights the company's ongoing integration of greenhouse gas emission-reduction targets into its medium-term business plans, with specific actions outlined to meet 2030 goals. The company continues to emphasize that sustainability efforts, while important to operations, remain subject to evolving measurement standards and regulatory frameworks. With a forward P/E of 14.5x and a solid 2.51% dividend yield, XOM appears reasonably valued relative to its earnings power, though investors should monitor how energy transition investments impact near-term profitability. The absence of detailed recent news suggests a period of operational stability, though the energy sector remains sensitive to commodity price fluctuations and regulatory changes.

### SEC Filing Highlights

ExxonMobil's upstream earnings surged to $7.9 billion in Q2 2026, up 46% year-over-year, driven primarily by higher crude oil realizations (+$4.65 billion) and advantaged volume growth from Guyana and Permian assets (+$1.14 billion). The company returned $18.6 billion to shareholders through $8.6 billion in dividends and $10.0 billion in share repurchases during the period. Production declined to 4,514 thousand barrels daily in Q2 2026 from 4,630 in the prior year, reflecting divestments and Middle East disruptions that reduced earnings by $1.06 billion. ExxonMobil remains strategically focused on high-return, low-cost projects in Guyana, Permian, and LNG while integrating sustainability initiatives into its medium-term planning.

### Risk Factors

• **Energy Transition and Climate Policy Risk** – Evolving environmental regulations, net-zero commitments, and accelerating policy stringency could impact long-term demand for fossil fuels and require significant capital reallocation toward lower-emission solutions, which remain underdeveloped at scale.

• **Project Execution and Regulatory Uncertainty** – Capital-intensive projects depend on stable policy environments, permitting approvals, and technological advancement; delays or unfavorable regulatory changes could impair returns on major investments.

• **Commodity Price Volatility** – Exposure to fluctuating oil and natural gas prices directly affects profitability and cash flow, with limited ability to fully hedge against sustained price downturns.

## Audited (Exec Summary + Outlook)

### Executive Summary
ExxonMobil is one of the world's largest integrated energy companies, generating $361.1 billion in revenue and $32.8 billion in net income, with a market capitalization of $674.4 billion that underscores its dominant position in the global energy sector. The stock is notable now because upstream earnings surged 46% year-over-year to $7.9 billion in Q2 2026 — driven by stronger crude oil realizations and high-return production growth in Guyana and the Permian — while the gap between the current P/E of 21.1x and the forward P/E of 14.5x signals that the market is pricing in meaningful earnings improvement, creating both opportunity and valuation risk depending on how that gap closes. The single most important near-term variable is the trajectory of crude oil prices, which directly determines whether the earnings growth implied by that forward multiple materializes or disappoints.

### Outlook
The directional outlook for ExxonMobil is **cautiously constructive**, supported by meaningful tailwinds: the Q2 2026 upstream earnings surge demonstrates the operating leverage embedded in the business when crude realizations are favorable, and the continued ramp of high-return, low-cost assets in Guyana and the Permian provides a credible volume growth runway that does not depend solely on commodity prices. The robust shareholder return program — combining dividends and buybacks — further underpins the investment case for patient, income-oriented holders. However, several headwinds temper conviction. Production has already shown vulnerability to geopolitical disruption and divestment activity, and the capital demands of integrating 2030 emissions-reduction targets into medium-term planning introduce an ongoing tension between near-term cash deployment and longer-term strategic repositioning. Key variables to monitor include: the direction and stability of crude oil and natural gas prices, which remain the primary earnings driver; execution and volume delivery from Guyana and Permian projects, where any delays would directly pressure the earnings growth implied by the forward multiple; the pace and cost of energy transition investments and how regulators evolve measurement and compliance standards; and geopolitical developments in the Middle East, which have already demonstrated the ability to disrupt production and compress earnings. The thesis would strengthen if sustained crude price support coincides with disciplined project execution and production recovery; it would weaken if a prolonged commodity downturn, regulatory tightening, or material project setbacks erode the earnings trajectory the current valuation anticipates.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative, forward-looking, and specific factual claim in the **Executive Summary** and **Outlook** sections.

---

## EXECUTIVE SUMMARY

---

CLAIM: "generating $361.1 billion in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $361,060,007,936, which rounds to $361.1 billion; also confirmed in the Financial Health pre-written section.

---

CLAIM: "$32.8 billion in net income"
LABEL: SUPPORTED
REASON: Source data shows net_income of $32,757,000,192, which rounds to $32.8 billion; also confirmed in the Financial Health pre-written section.

---

CLAIM: "market capitalization of $674.4 billion"
LABEL: SUPPORTED
REASON: Source data shows market_cap of $674,394,669,056, which rounds to $674.4 billion; confirmed in the Financial Health pre-written section.

---

CLAIM: "upstream earnings surged 46% year-over-year to $7.9 billion in Q2 2026"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states upstream earnings were $7.9 billion in Q2 2026 vs. $5.4 billion in Q2 2025; the SEC Filing Highlights pre-written section states "up 46% year-over-year." Verification: ($7.9B − $5.4B) / $5.4B = 46.3%, which rounds to 46% — within 0.15 pp tolerance.

---

CLAIM: "current P/E of 21.1x"
LABEL: SUPPORTED
REASON: Source data shows pe_ratio of 21.108107, which rounds to 21.1x; confirmed in the Financial Health pre-written section.

---

CLAIM: "forward P/E of 14.5x"
LABEL: SUPPORTED
REASON: Source data shows forward_pe of 14.50511, which rounds to 14.5x; confirmed in the Financial Health pre-written section.

---

## OUTLOOK

---

CLAIM: "Q2 2026 upstream earnings surge"
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly states upstream earnings reached $7.9 billion in Q2 2026, up from $5.4 billion in Q2 2025.

---

CLAIM: "continued ramp of high-return, low-cost assets in Guyana and the Permian"
LABEL: SUPPORTED
REASON: RAG SEC Highlights and the SEC Filing Highlights pre-written section both identify Guyana and Permian as advantaged assets contributing to volume growth.

---

CLAIM: "robust shareholder return program — combining dividends and buybacks"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states the company distributed $8.6 billion in dividends and repurchased $10.0 billion of common stock; the SEC Filing Highlights pre-written section confirms $18.6 billion total returned.

---

CLAIM: "Production has already shown vulnerability to geopolitical disruption and divestment activity"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states production declined from 4,630 to 4,514 thousand barrels daily "primarily due to divestments and Middle East disruptions."

---

CLAIM: "integrating 2030 emissions-reduction targets into medium-term planning"
LABEL: SUPPORTED
REASON: The 10-Q filing summary and RAG SEC Highlights both reference ExxonMobil's 2030 greenhouse gas emission-reduction plans being incorporated into medium-term business plans.

---

CLAIM: "geopolitical developments in the Middle East, which have already demonstrated the ability to disrupt production and compress earnings"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states Middle East disruptions reduced earnings by $1.06 billion in Q2 and contributed to the production decline from 4,630 to 4,514 thousand barrels daily.

---

**No additional quantitative figures, price targets, thresholds, ratios, percentages, named product milestones, or forward-looking numbers appear in the Executive Summary or Outlook sections beyond those audited above.** All claims audited are either directly present in the source data or derivable by verified arithmetic from figures explicitly present in the source data.
