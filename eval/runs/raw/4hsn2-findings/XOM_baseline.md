# XOM — baseline

## Metadata

ticker: XOM
arm: baseline
judge_prompt_version: v2
context_sha256: 84f93970bd7c760d386b78d519c7baad09eaf7d183fd618f614bf1eda99d46dd
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 393, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.935, "latency_s_total": 3.935, "parse_failure": 0, "prompt_tokens": 2481, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 324, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.851, "latency_s_total": 4.851, "parse_failure": 0, "prompt_tokens": 3314, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 187, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.411, "latency_s_total": 2.411, "parse_failure": 0, "prompt_tokens": 497, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 199, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.929, "latency_s_total": 2.929, "parse_failure": 0, "prompt_tokens": 490, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 206, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.906, "latency_s_total": 2.906, "parse_failure": 0, "prompt_tokens": 398, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 224, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.407, "latency_s_total": 2.407, "parse_failure": 0, "prompt_tokens": 475, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1354, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.758, "latency_s_total": 19.758, "parse_failure": 0, "prompt_tokens": 2038, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "XOM",
  "company_name": "ExxonMobil Holdings Corporation",
  "current_price": 164.0,
  "currency": "USD",
  "market_cap": 674353577984.0,
  "pe_ratio": 21.106821,
  "forward_pe": 14.451936,
  "week_52_high": 176.41,
  "week_52_low": 110.39,
  "financial_currency": "USD",
  "revenue": 361060007936.0,
  "net_income": 32757000192.0,
  "profit_margin_pct": 9.07,
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
- **Upstream Earnings**: Total upstream earnings reached $7.9 billion in Q2 2026 (compared to $5.4 billion in Q2 2025) and $13.7 billion for the first half of 2026 (versus $12.2 billion in the prior year period)
- **Shareholder Returns**: The company distributed $8.6 billion in dividends and repurchased $10.0 billion of common stock

## Production & Operations
- **Oil-Equivalent Production**: Declined to 4,514 thousand barrels daily in Q2 2026 from 4,630 in Q2 2025, primarily due to divestments and Middle East disruptions
- **Production Mix**: Crude oil and liquids production totaled 3,373 thousand barrels daily globally, while natural gas production was 6,849 million cubic feet daily

## Earnings Drivers
- **Positive Factors**: Higher crude oil realizations added $4.7 billion in Q2 earnings; advantaged volume growth (Guyana and Permian) contributed $1.1 billion
- **Negative Factors**: Middle East disruptions reduced earnings by $1.1 billion; higher depreciation expenses decreased earnings by $690 million; unfavorable derivatives mark-to-market impacts reduced earnings by $180 million
- **Identified Items**: A $1.2 billion loss from financial reserves was recorded

## Market Context
Market conditions were influenced by Middle East supply disruptions and global refining capacity reductions, with crude oil prices remaining within historical ranges and natural gas prices elevated above the 10-year average.

RAG — RISK FACTORS:
[From Pinecone cache] Based on the provided context, the primary risk factors disclosed relate to environmental and sustainability efforts. Specifically, the disclosure indicates that:

1. **Forward-looking environmental statements** - The company notes that forward-looking statements regarding environmental and sustainability efforts and aspirations are not necessarily material to investors or required for SEC disclosure.

2. **Evolving standards and processes** - Historical, current, and forward-looking environmental and sustainability-related statements may be based on standards for measuring progress that are still developing, internal controls and processes that continue to evolve, and assumptions subject to change in the future, including future rule-making.

3. **Net-zero pathway challenges** - Current trends for policy stringency and development of lower-emission solutions are not yet on a pathway to achieve net-zero by 2050. The company's reference case planning does not project the degree of required future policy and technology advancement and deployment needed to meet net-zero by 2050 targets.

4. **Project advancement uncertainties** - Individual projects or opportunities may advance based on various factors including availability of stable and supportive policy, permitting, technological advancement for cost-effective abatement, and alignment with partners and stakeholders.

5. **Capital investment contingencies** - Capital investment guidance in lower-emission investments is subject to the availability of the opportunity set and public policy support, with focus on returns.

For a comprehensive list of all risk factors, the context references Item 1A of the company's 2025 Form 10-K filing.

## Pre-written sections (judge input)

### Financial Health

ExxonMobil trades at $164.00 USD with a market capitalization of $674.4 billion, demonstrating substantial scale within the energy sector. The company generated $361.1 billion in revenue with a net profit margin of 9.07%, translating to $32.8 billion in net income, reflecting solid operational profitability. The P/E ratio of 21.1x appears elevated relative to the forward P/E of 14.5x, suggesting the market may be pricing in near-term headwinds, though the forward valuation indicates potential value as earnings are expected to improve. With a 2.51% dividend yield and strong cash generation, XOM maintains financial stability to support shareholder returns. The company's financial position supports its medium-term business plans, including capital allocation toward emissions reduction initiatives.

### Recent Developments

ExxonMobil's most recent 10-Q filing (August 3, 2026) highlights the company's ongoing integration of greenhouse gas emission-reduction targets into its medium-term business plans, with specific actions outlined to meet 2030 goals. The company continues to emphasize that environmental and sustainability statements represent aspirational commitments rather than material disclosure requirements, suggesting management is balancing climate initiatives with operational flexibility. With a solid 9.07% profit margin and $32.8 billion in net income on $361 billion in revenue, ExxonMobil maintains strong financial fundamentals to fund both energy transition investments and shareholder returns, evidenced by its 2.51% dividend yield. The forward P/E of 14.45x appears reasonable relative to the current 21.1x trailing multiple, suggesting potential valuation support if the company executes on its strategic plans.

### SEC Filing Highlights

ExxonMobil reported strong upstream earnings of $7.9 billion in Q2 2026, up 46% year-over-year, driven primarily by higher crude oil realizations that added $4.7 billion in earnings. The company returned $18.6 billion to shareholders through $8.6 billion in dividends and $10.0 billion in share repurchases during the period. Production declined modestly to 4,514 thousand barrels of oil equivalent daily due to divestments and Middle East disruptions, which reduced earnings by $1.1 billion, though this was partially offset by advantaged volume growth from Guyana and Permian operations. A $1.2 billion loss from financial reserves was recorded as an identified item. Despite operational headwinds, the company's first-half 2026 upstream earnings of $13.7 billion exceeded the prior year period, reflecting the benefit of elevated commodity prices in a market shaped by Middle East supply constraints.

### Risk Factors

• **Energy Transition and Net-Zero Pathway Uncertainty** - Current policy and technology trends are not aligned with net-zero by 2050 targets. The company's planning does not assume sufficient future policy stringency or technology deployment to meet climate goals, creating uncertainty around long-term business model viability and capital allocation effectiveness.

• **Environmental and Sustainability Disclosure Limitations** - Forward-looking environmental statements and sustainability aspirations may not reflect material risks or be subject to rigorous SEC disclosure standards. Measurement standards and internal processes remain evolving, with assumptions subject to change, potentially limiting investor visibility into actual progress and commitments.

• **Policy and Project Execution Risks** - Lower-emission investment returns depend on stable policy support, permitting approvals, technological cost-effectiveness, and stakeholder alignment—factors largely outside management control. Withdrawal or changes in public policy support could materially impact capital deployment and returns on green energy investments.

## Audited (Exec Summary + Outlook)

### Executive Summary
ExxonMobil is one of the world's largest integrated energy companies, generating $361.1 billion in revenue and $32.8 billion in net income while commanding a $674.4 billion market capitalization, underscoring its dominant scale across upstream, downstream, and chemical operations. The stock is notable now because a meaningful gap exists between the trailing P/E of 21.1x and the forward P/E of 14.5x, reflecting market uncertainty about near-term earnings, even as the company demonstrated strong momentum with upstream earnings up 46% year-over-year in Q2 2026 and returned $18.6 billion to shareholders in a single period. The single most important near-term variable is the trajectory of crude oil realizations — the same commodity price tailwind that drove the Q2 2026 earnings surge is the factor most capable of either validating the forward valuation or exposing it to downside pressure.

### Outlook
The directional outlook for XOM is **cautiously constructive**, supported by a robust shareholder return program, advantaged production growth in Guyana and the Permian, and a forward valuation that appears more reasonable than the trailing multiple suggests — provided commodity prices remain supportive. The primary tailwind is the elevated crude oil price environment shaped by Middle East supply constraints, which has already demonstrated its earnings power through the year-over-year upstream surge in Q2 2026; investors should watch crude oil realizations closely, as any sustained softening would be the most direct threat to the thesis. On the operational side, the pace of volume recovery — particularly whether Guyana and Permian growth can offset the production drag from divestments and regional disruptions — is a key variable to monitor each quarter. Headwinds include the evolving and uncertain policy landscape around energy transition, which creates ambiguity around the returns profile of lower-emission capital investments, as well as the limited transparency into how aspirational sustainability commitments translate into measurable financial outcomes. The constructive lean would strengthen if crude realizations hold, production volumes stabilize or grow, and management demonstrates disciplined capital allocation across both conventional and lower-emission investments; it would weaken if commodity prices retreat materially, geopolitical disruptions deepen, or policy support for green energy investments erodes faster than the company can adapt its capital plans.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$361.1 billion in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $361,060,007,936, which rounds to $361.1 billion; also confirmed in the Financial Health pre-written section.

---

CLAIM: "$32.8 billion in net income"
LABEL: SUPPORTED
REASON: Source data shows net income of $32,757,000,192, which rounds to $32.8 billion; also confirmed in the Financial Health pre-written section.

---

CLAIM: "$674.4 billion market capitalization"
LABEL: SUPPORTED
REASON: Source data shows market cap of $674,353,577,984, which rounds to $674.4 billion; confirmed in the Financial Health pre-written section.

---

CLAIM: "trailing P/E of 21.1x"
LABEL: SUPPORTED
REASON: Source data shows pe_ratio of 21.106821, which rounds to 21.1x.

---

CLAIM: "forward P/E of 14.5x"
LABEL: SUPPORTED
REASON: Source data shows forward_pe of 14.451936, which rounds to 14.5x.

---

CLAIM: "upstream earnings up 46% year-over-year in Q2 2026"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states upstream earnings were $7.9 billion in Q2 2026 vs. $5.4 billion in Q2 2025; recomputed: (7.9 − 5.4) / 5.4 = 46.3%, which is within 0.15 pp of 46%; the SEC Filing Highlights pre-written section also states "up 46% year-over-year."

---

CLAIM: "returned $18.6 billion to shareholders in a single period"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states $8.6 billion in dividends plus $10.0 billion in share repurchases = $18.6 billion; confirmed in the SEC Filing Highlights pre-written section.

---

**OUTLOOK**

---

CLAIM: "advantaged production growth in Guyana and the Permian"
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly names "advantaged volume growth (Guyana and Permian)" as a positive earnings factor; confirmed in the SEC Filing Highlights pre-written section.

---

CLAIM: "forward valuation that appears more reasonable than the trailing multiple suggests"
LABEL: INFERENCE
REASON: This is a direct qualitative comparison of the two present figures (forward P/E 14.5x vs. trailing P/E 21.1x), derivable by straightforward comparison of the two figures in the source data.

---

CLAIM: "elevated crude oil price environment shaped by Middle East supply constraints"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "Market conditions were influenced by Middle East supply disruptions" and "crude oil prices remaining within historical ranges," and the SEC Filing Highlights pre-written section references Middle East supply constraints shaping the market.

---

CLAIM: "year-over-year upstream surge in Q2 2026"
LABEL: SUPPORTED
REASON: RAG SEC Highlights confirms Q2 2026 upstream earnings of $7.9 billion vs. $5.4 billion in Q2 2025, a clear year-over-year increase; the 46% figure was already verified above.

---

CLAIM: "production drag from divestments and regional disruptions"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states production "Declined to 4,514 thousand barrels daily in Q2 2026 from 4,630 in Q2 2025, primarily due to divestments and Middle East disruptions"; confirmed in the SEC Filing Highlights pre-written section.

---

*No additional standalone quantitative figures, price targets, specific thresholds, named ratios, or forward-looking numerical claims appear in the Outlook section beyond those addressed above. All directional and qualitative statements (e.g., "cautiously constructive," "most direct threat," "would weaken if") are non-quantitative and outside the audit scope.*
