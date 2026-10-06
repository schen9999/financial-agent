# OMER — baseline

## Metadata

ticker: OMER
arm: baseline
judge_prompt_version: v2
context_sha256: 2999ab10d7825bb86bcb9e64f1e4a3565dd7c31693233a0e9fc7b4af55cd1a58
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 384, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.25, "latency_s_total": 4.25, "parse_failure": 0, "prompt_tokens": 2764, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 413, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.117, "latency_s_total": 5.117, "parse_failure": 0, "prompt_tokens": 3239, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 222, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.901, "latency_s_total": 2.901, "parse_failure": 0, "prompt_tokens": 695, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 162, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.851, "latency_s_total": 1.851, "parse_failure": 0, "prompt_tokens": 688, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 227, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.261, "latency_s_total": 2.261, "parse_failure": 0, "prompt_tokens": 484, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 205, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.138, "latency_s_total": 2.138, "parse_failure": 0, "prompt_tokens": 463, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1381, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 20.074, "latency_s_total": 20.074, "parse_failure": 0, "prompt_tokens": 2032, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "OMER",
  "company_name": "Omeros Corporation",
  "current_price": 18.9,
  "currency": "USD",
  "market_cap": 1368139264.0,
  "pe_ratio": 15.491802,
  "forward_pe": 15.365853,
  "week_52_high": 21.24,
  "week_52_low": 4.06,
  "financial_currency": "USD",
  "revenue": 38422000.0,
  "net_income": 116533000.0,
  "profit_margin_pct": 324.88,
  "dividend_yield": 0.0,
  "sector": "Healthcare",
  "industry": "Biotechnology"
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
    "filing_date": "2026-03-31",
    "summary": "ITEM 1A. RISK FACTORS The risks and uncertainties described below may have a material adverse effect on our business, prospects, financial condition or operating results. In addition, we may be adversely affected by risks that we currently deem immaterial or by other risks that are not currently known to us. You should carefully consider these risks before making an investment decision. The trading price of our common stock could decline due to any of these risks and you may lose all or part of your investment. In assessing the risks described below, you should also refer to the other information contained in this Annual Report on Form 10-K. Risks Related to Our Products, Product Candidates, Programs and Operations Our ability to achieve profitability is highly dependent on the commercial "
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-12",
    "summary": "ITEM 1A. RISK FACTORS We operate in an environment that involves a number of risks and uncertainties. Before making an investment decision you should carefully consider the risks described in Part I, Item 1A, \u201cRisk Factors\u201d of our Annual Report on Form 10-K for the year ended December 31, 2025, as filed with the SEC on March 31, 2026. In assessing the risk factors set forth in our Annual Report on Form 10-K for the year ended December 31, 2025, you should also refer to the other information included therein and in this Quarterly Report on Form 10-Q, including the supplemental risk factor below. In addition, we may be adversely affected by risks that we currently deem to be immaterial or by other risks that are not currently known to us. Due to these risks and uncertainties, known and unkno"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] # Key Takeaways from the Latest SEC Filings

## Financial Position
- As of December 31, 2025, the company held $171.8 million in cash, cash equivalents, and short-term investments
- Cash used in operations for 2025 was $116.1 million
- Net loss for 2025 was $3.4 million
- Outstanding debt includes $70.8 million in convertible senior notes due June 15, 2029, and approximately $1.2 million in finance lease obligations
- The company has a history of cumulative operating losses since inception

## Product Commercialization
- YARTEMLEA is the company's only commercialized product, approved by the FDA in December 2025
- Near-term commercial prospects are heavily dependent on YARTEMLEA's success
- The company has limited experience in marketing, selling, and distributing the product
- Profitability is contingent on generating substantial revenue from YARTEMLEA

## Key Business Risks
- Commercialization challenges including physician and patient acceptance, reimbursement policies, and competition
- Reliance on a limited number of manufacturers and suppliers
- Dependence on third-party partnerships for international distribution
- Vulnerability to regulatory changes and post-approval compliance requirements
- Uncertainty regarding coverage and reimbursement rates from government and private payers

## Future Outlook
- The company expects to continue incurring substantial expenses for clinical trials, commercialization, R&D, and debt service
- Additional capital will likely be needed to fund operations and achieve profitability
- Success depends on YARTEMLEA sales, partnership arrangements (including a deal with Novo Nordisk), and potential future product approvals

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors in its SEC filing:

## Product and Commercialization Risks
- **Dependence on YARTEMLEA**: The company's profitability is highly dependent on the commercial success of YARTEMLEA, its only commercialized product (FDA-approved in December 2025). Failure to successfully commercialize it could materially adversely affect the business and stock price.
- **Commercialization challenges**: These include lack of physician and patient acceptance, limited marketing and sales experience, reliance on third-party manufacturers and suppliers, and unknown safety risks.
- **Regulatory and compliance risks**: Failure to obtain regulatory approval in foreign territories, inability to comply with post-approval requirements, and changing regulatory restrictions could impair commercialization.

## Reimbursement and Pricing Risks
- Significant delays in obtaining adequate coverage or reimbursement from government and private payers
- Reimbursement rates may not allow the company to make a profit or cover costs
- Government and private payers increasingly demanding predetermined discounts from list prices
- Potential adverse effects from Medicare reimbursement changes, including those from the Inflation Reduction Act
- Government price controls in certain jurisdictions like the EU

## Partnership and Development Risks
- Dependence on Novo Nordisk's successful development and commercialization of zaltenibart, with milestone and royalty payments contingent on factors outside the company's control

## Financial and Capital Risks
- Cumulative operating losses since inception
- Substantial ongoing cash burn ($116.1 million in 2025)
- Uncertainty about generating sufficient revenue to achieve profitability
- Need for additional capital to continue operations and development programs
- Existing indebtedness ($70.8 million in convertible notes due 2029 and other obligations)

## Pre-written sections (judge input)

### Financial Health

Omeros Corporation trades at $18.90 with a market capitalization of $1.37 billion and a reasonable P/E ratio of 15.49x, suggesting moderate valuation relative to earnings. However, the company's financial profile is highly unusual, with reported revenue of $38.4 million against net income of $116.5 million, resulting in an exceptional 324.88% profit margin that warrants scrutiny regarding accounting methodology or one-time gains. The stock has recovered significantly from its 52-week low of $4.06 to $18.90, indicating investor confidence, though the lack of dividend yield suggests reinvestment focus. As a biotechnology company, Omeros faces inherent operational risks tied to product commercialization and regulatory approval, as highlighted in recent SEC filings emphasizing dependence on achieving sustained profitability. The elevated profit margin relative to modest revenue suggests the company may be in a transitional phase, requiring careful monitoring of upcoming quarterly results to validate financial sustainability.

### Recent Developments

Limited recent news is currently available for Omeros Corporation. The company's most recent SEC filings include a 10-K filed on March 31, 2026, and a 10-Q filed on August 12, 2026, both emphasizing significant risk factors related to product commercialization and profitability achievement. Investors should note the company's unusual financial profile, with a reported profit margin of 324.88% on $38.4 million in revenue, which warrants careful scrutiny of accounting methods and sustainability. The stock's 52-week range of $4.06 to $21.24 reflects considerable volatility, suggesting investors should monitor upcoming clinical or commercial developments closely before making investment decisions.

### SEC Filing Highlights

Omeros Corporation held $171.8 million in cash and short-term investments as of December 31, 2025, with annual operating cash burn of $116.1 million, providing approximately 18 months of runway. The company's sole commercialized product, YARTEMLEA, received FDA approval in December 2025, making near-term financial performance heavily dependent on successful market adoption and physician/patient acceptance. With $70.8 million in convertible senior notes due 2029 and a history of cumulative operating losses, the company will likely require additional capital to fund operations and achieve profitability. Key risks include commercialization execution, reimbursement uncertainty, reliance on limited manufacturers, and dependence on third-party partnerships including a distribution deal with Novo Nordisk. Management expects continued substantial expenses for clinical trials, R&D, and debt service while scaling YARTEMLEA sales.

### Risk Factors

• **Heavy Dependence on YARTEMLEA Commercialization**: Omeros' profitability relies almost entirely on the commercial success of YARTEMLEA, its only FDA-approved product (approved December 2025). Failure to achieve market acceptance, physician adoption, or adequate reimbursement could materially harm the business and stock price.

• **Significant Cash Burn and Path to Profitability Uncertain**: The company burned $116.1 million in cash during 2025 with cumulative operating losses since inception. Omeros must generate sufficient revenue from YARTEMLEA sales to offset ongoing expenses and achieve profitability, with no guarantee of success.

• **Reimbursement and Pricing Pressures**: Government and private payers are increasingly demanding discounts from list prices, and delays in obtaining adequate reimbursement coverage could impair commercialization. Changes to Medicare reimbursement policies and government price controls in key markets like the EU pose additional headwinds to revenue generation.

## Audited (Exec Summary + Outlook)

### Executive Summary
Omeros Corporation is a commercial-stage biotechnology company whose investment thesis now rests almost entirely on YARTEMLEA, its sole FDA-approved product launched in December 2025, with the stock trading at $18.90 and a market capitalization of $1.37 billion after rebounding sharply from a 52-week low of $4.06. The stock is notable today because it sits at an inflection point: reported financials show an unusual 324.88% profit margin on $38.4 million in revenue that demands explanation, while $171.8 million in cash against $116.1 million in annual operating cash burn leaves the company with a limited runway to prove its commercial model before likely needing additional capital. The single most important near-term variable is the pace and breadth of YARTEMLEA market adoption — specifically whether physician uptake and payer reimbursement decisions accelerate quickly enough to reduce cash burn and validate a sustainable revenue trajectory.

### Outlook
The directional outlook for Omeros is **cautiously constructive but highly contingent**, with the balance of near-term evidence tilting toward meaningful binary risk rather than a straightforward growth story. The primary tailwind is the recency of YARTEMLEA's FDA approval in December 2025, which positions the company at the earliest and potentially steepest part of a commercial ramp, supported by the Novo Nordisk distribution partnership as a meaningful commercial infrastructure advantage. Against that, the headwinds are substantial: the cash runway of approximately 18 months leaves little margin for a slow launch, reimbursement coverage gaps could meaningfully delay physician adoption, and the reported financials — particularly the disconnect between modest revenue and exceptional reported profit margin — raise unresolved questions about earnings quality that investors must clarify before sizing a position with confidence. The key variables to monitor are the trajectory of YARTEMLEA prescription volume and net revenue in successive quarterly filings, the speed and breadth of payer coverage decisions, any updates to the Novo Nordisk distribution arrangement, and whether management signals a need to raise additional capital ahead of the convertible notes due 2029. The thesis would strengthen materially if quarterly results show accelerating YARTEMLEA revenue, narrowing cash burn, and broad reimbursement wins; it would weaken — potentially sharply — if adoption stalls, a dilutive capital raise is announced, or the unusual profit margin is revealed to reflect non-recurring items rather than durable earnings power.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, and forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "YARTEMLEA, its sole FDA-approved product launched in December 2025"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors both explicitly state "YARTEMLEA is the company's only commercialized product, approved by the FDA in December 2025."

---

CLAIM: "the stock trading at $18.90"
LABEL: SUPPORTED
REASON: The source data lists current_price as 18.9 (USD), which equals $18.90.

---

CLAIM: "a market capitalization of $1.37 billion"
LABEL: SUPPORTED
REASON: Source data shows market_cap = 1,368,139,264.0, which rounds to $1.37 billion.

---

CLAIM: "rebounding sharply from a 52-week low of $4.06"
LABEL: SUPPORTED
REASON: Source data explicitly lists week_52_low as 4.06.

---

CLAIM: "reported financials show an unusual 324.88% profit margin"
LABEL: SUPPORTED
REASON: Source data lists profit_margin_pct as 324.88, and the pre-written Financial Health section confirms "324.88% profit margin."

---

CLAIM: "$38.4 million in revenue"
LABEL: SUPPORTED
REASON: Source data lists revenue as 38,422,000, which rounds to $38.4 million; confirmed in pre-written sections.

---

CLAIM: "$171.8 million in cash against $116.1 million in annual operating cash burn"
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly states "$171.8 million in cash, cash equivalents, and short-term investments" and "Cash used in operations for 2025 was $116.1 million."

---

CLAIM: "leaves the company with a limited runway to prove its commercial model before likely needing additional capital"
LABEL: INFERENCE
REASON: This is a directional inference directly derivable from the two present figures ($171.8M cash ÷ $116.1M annual burn ≈ 1.5 years), consistent with the pre-written SEC Filing Highlights section's "approximately 18 months of runway," and the RAG note that "Additional capital will likely be needed."

---

**OUTLOOK**

---

CLAIM: "the recency of YARTEMLEA's FDA approval in December 2025"
LABEL: SUPPORTED
REASON: RAG SEC Highlights and Risk Factors both explicitly confirm FDA approval in December 2025.

---

CLAIM: "the Novo Nordisk distribution partnership as a meaningful commercial infrastructure advantage"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "a deal with Novo Nordisk" and Risk Factors reference "Dependence on Novo Nordisk's successful development and commercialization of zaltenibart, with milestone and royalty payments contingent on factors outside the company's control"; the pre-written SEC Filing Highlights also references "a distribution deal with Novo Nordisk." Note: the source characterizes this as a partnership involving zaltenibart milestones/royalties and third-party distribution, not purely a "distribution partnership" for YARTEMLEA — however, the pre-written SEC Filing Highlights section (direct model input) explicitly calls it "a distribution deal with Novo Nordisk," so the claim is grounded in the pre-written input.

---

CLAIM: "the cash runway of approximately 18 months"
LABEL: SUPPORTED
REASON: The pre-written SEC Filing Highlights section explicitly states "approximately 18 months of runway," derived from $171.8M ÷ $116.1M ≈ 1.48 years (~17.8 months), which is consistent with "approximately 18 months."

---

CLAIM: "the convertible notes due 2029"
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly states "$70.8 million in convertible senior notes due June 15, 2029."

---

CLAIM: "the disconnect between modest revenue and exceptional reported profit margin"
LABEL: SUPPORTED
REASON: Source data confirms revenue of $38.4 million and profit_margin_pct of 324.88%, and the pre-written sections explicitly flag this disconnect; no new figure is introduced.

---

CLAIM: "whether management signals a need to raise additional capital ahead of the convertible notes due 2029"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "Additional capital will likely be needed to fund operations and achieve profitability," and convertible notes due 2029 are explicitly cited in the source data.

---

CLAIM: "if the unusual profit margin is revealed to reflect non-recurring items rather than durable earnings power"
LABEL: INFERENCE
REASON: This is a qualitative inference directly derivable from the pre-written Financial Health section's explicit statement that the 324.88% profit margin "warrants scrutiny regarding accounting methodology or one-time gains" — no new fact is introduced, and the derivation step is a restatement of that concern.
