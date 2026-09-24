# OMER — local-model

## Metadata

ticker: OMER
arm: local-model
judge_prompt_version: v2
context_sha256: 05185b2046e0a2fc1d7d2f11dfa4594e1532a3826b4304c7826731ff202dc9b9
local_model_served_name: qwen2.5-7b-instruct
local_model_dir: qwen2.5-7b-instruct
local_model_backend: openai
local_model_url: http://vllm.financial-agent.svc:8000
local_model_sampling: {"max_tokens": 512, "min_p": 0.0, "repetition_penalty": 1.1, "temperature": 0.1, "top_k": 20, "top_p": 0.8}

## Retrieved source context

STOCK DATA:
{
  "ticker": "OMER",
  "company_name": "Omeros Corporation",
  "current_price": 20.74,
  "currency": "USD",
  "market_cap": 1501333760.0,
  "pe_ratio": 12.569697,
  "forward_pe": 16.861788,
  "week_52_high": 21.24,
  "week_52_low": 4.06,
  "revenue": 38422000.0,
  "net_income": 116533000.0,
  "profit_margin": 3.2488198,
  "sector": "Healthcare",
  "industry": "Biotechnology"
}

NEWS ARTICLES:
[]

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
- Profitability is contingent on generating substantial revenue from YARTEMLEA sales

## Strategic Partnerships
- The company has an agreement with Novo Nordisk involving zaltenibart, with future milestone and royalty payments contingent on successful development and commercialization
- Revenue from this partnership may vary significantly based on market conditions, pricing, and sales volumes

## Key Risks and Challenges
- Significant capital requirements for clinical trials, manufacturing, R&D, and commercialization
- Dependence on limited manufacturers and suppliers
- Reimbursement and coverage uncertainties from government and private payers
- Competitive disadvantages due to leverage and capital constraints
- Uncertainty regarding ability to achieve sustained profitability

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors in its SEC filing:

## Product and Commercialization Risks
- **Dependence on YARTEMLEA**: The company's profitability is highly dependent on the commercial success of YARTEMLEA, its only commercialized product (FDA-approved in December 2025). Failure to successfully commercialize it could materially adversely affect the business.
- **Commercialization challenges**: Including lack of physician and patient acceptance, limited marketing and sales experience, reliance on third-party manufacturers and suppliers, and unknown safety risks.

## Reimbursement and Pricing Risks
- **Coverage and reimbursement uncertainty**: Significant delays may occur in obtaining adequate coverage or reimbursement from government and private payers, and reimbursement rates may not allow the company to achieve profitability.
- **Price controls and negotiations**: Government price controls and pricing negotiations can be time-consuming and may result in unfavorable terms.

## Partnership Dependency Risk
- **Reliance on Novo Nordisk**: The company's ability to realize value from zaltenibart depends on Novo Nordisk's development and commercialization efforts, which are outside the company's control.

## Financial and Capital Risks
- **Cumulative operating losses**: The company has incurred cumulative operating losses since inception and expects to continue incurring losses.
- **Capital requirements**: Substantial additional capital may be needed to complete development and commercialization of products, with no assurance that capital will be available on acceptable terms.
- **Debt obligations**: The company has convertible senior notes and finance lease obligations that require principal, interest, and fee payments.

## Pre-written sections (judge input)

### Financial Health

Omeros Corporation (OMER) has a current stock price of $20.74 USD, with a market capitalization of approximately $150.13 million. The company's trailing P/E ratio stands at 12.57, while the forward P/E ratio is higher at 16.86, indicating potential growth expectations. Revenue for the period was $38.42 million, and the net income was $11.65 million, resulting in a modest profit margin of 3.25%. These metrics suggest a stable but cautious financial position within the healthcare sector.

### Recent Developments

No significant recent news announcements are currently available for Omeros Corporation. However, the company's most recent SEC filings (10-K filed March 31, 2026 and 10-Q filed August 12, 2026) emphasize substantial operational and commercial risks that investors should carefully evaluate. The company's ability to achieve sustained profitability remains dependent on successful commercialization of its product pipeline in a competitive biotechnology environment. Investors should monitor upcoming clinical trial results and commercial execution metrics, as these will be critical drivers of future stock performance.

### SEC Filing Highlights

Omeros holds $171.8 million in cash and short-term investments as of December 31, 2025, with 2025 operating cash burn of $116.1 million, providing approximately 18 months of runway at current burn rates. The company's sole commercialized product, YARTEMLEA (approved by FDA in December 2025), represents the critical near-term driver for achieving profitability, though the company has limited commercial infrastructure experience. Outstanding debt of $70.8 million in convertible senior notes due 2029 and a history of cumulative operating losses underscore the company's dependence on YARTEMLEA revenue generation and the Novo Nordisk partnership for zaltenibart. Key risks include significant capital requirements for R&D and commercialization, reimbursement uncertainties, and reliance on limited manufacturers, which could constrain growth despite the recent FDA approval.

### Risk Factors

- **Dependence on YARTEMLEA**: Profitability hinges on the successful commercialization of YARTEMLEA; failure to do so could significantly impact the business.
- **Partnership Dependency Risk**: Realizing value from zaltenibart depends on Novo Nordisk’s development and commercialization efforts, which are beyond Omeros’ control.

## Audited (Exec Summary + Outlook)

### Executive Summary
Omeros Corporation is a commercial-stage biopharmaceutical company operating within the healthcare sector, currently generating $38.42 million in revenue and $11.65 million in net income against a market capitalization of approximately $150.13 million. The stock is notable now because the company sits at a genuine commercial inflection point — YARTEMLEA received FDA approval in December 2025 and is the sole commercialized product, while the company holds $171.8 million in cash against an annual operating cash burn of $116.1 million, creating a finite and visible window to prove out its commercial model. The single most important near-term variable is the pace and trajectory of YARTEMLEA's commercial uptake, which will determine whether Omeros can reduce its cash burn meaningfully before its approximately 18-month runway is exhausted.

### Outlook
The directional lean on Omeros is **cautious**, with the potential to become more constructive if early commercial signals from YARTEMLEA prove convincing. The primary tailwind is the FDA approval itself — a meaningful de-risking event that gives the company a legitimate revenue engine for the first time — alongside the financial backstop provided by the Novo Nordisk partnership for zaltenibart, which reduces the burden on Omeros to self-fund that program's advancement. The headwinds, however, are substantial: the company is building commercial infrastructure largely from scratch, reimbursement and payer coverage for YARTEMLEA remains an open and critical question, manufacturing concentration creates supply-chain fragility, and the cash runway, while not immediately alarming, leaves limited margin for a slow commercial ramp. Investors should watch the cadence of YARTEMLEA prescription and revenue growth quarter over quarter, the speed and breadth of payer coverage decisions, any updates from Novo Nordisk on zaltenibart's development timeline, and the trajectory of operating cash burn relative to the existing runway. A faster-than-expected YARTEMLEA launch combined with favorable reimbursement outcomes would meaningfully strengthen the thesis; a slow uptake, coverage denials, or any manufacturing disruption would deepen concerns about the company's path to self-sufficiency before its current cash position is depleted.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "currently generating $38.42 million in revenue"
LABEL: SUPPORTED
REASON: The raw source data lists revenue as $38,422,000, and the pre-written Financial Health section states "$38.42 million," matching exactly.

---

CLAIM: "$11.65 million in net income"
LABEL: UNSUPPORTED
REASON: The raw source data lists net income as $116,533,000 (approximately $116.5 million), not $11.65 million; the pre-written Financial Health section erroneously states "$11.65 million," and the AI brief reproduces this error — the figure fails the presence/accuracy check against the actual source data.

---

CLAIM: "market capitalization of approximately $150.13 million"
LABEL: UNSUPPORTED
REASON: The raw source data lists market_cap as $1,501,333,760 (approximately $1.50 billion), not $150.13 million; the pre-written section misplaces the decimal by a factor of 10, and the AI brief reproduces this error.

---

CLAIM: "YARTEMLEA received FDA approval in December 2025"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors sections both explicitly state "YARTEMLEA… approved by the FDA in December 2025."

---

CLAIM: "the sole commercialized product"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state "YARTEMLEA is the company's only commercialized product."

---

CLAIM: "the company holds $171.8 million in cash against an annual operating cash burn of $116.1 million"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "$171.8 million in cash, cash equivalents, and short-term investments" and "Cash used in operations for 2025 was $116.1 million."

---

CLAIM: "approximately 18-month runway"
LABEL: SUPPORTED
REASON: The pre-written SEC Filing Highlights section explicitly states "approximately 18 months of runway at current burn rates," derived from $171.8M ÷ $116.1M/year ≈ 1.48 years ≈ 17.8 months, which rounds to approximately 18 months.

---

**OUTLOOK**

---

CLAIM: (Novo Nordisk partnership for zaltenibart) "reduces the burden on Omeros to self-fund that program's advancement"
LABEL: INFERENCE
REASON: The RAG SEC Highlights confirm the Novo Nordisk agreement involves "future milestone and royalty payments contingent on successful development and commercialization," and the Risk Factors confirm Novo Nordisk bears development responsibility; the conclusion that this reduces Omeros's self-funding burden is a direct logical derivation from those stated facts.

---

CLAIM: (no explicit new quantitative figures appear in the Outlook beyond those already evaluated above; the Outlook references "18-month runway" implicitly via "existing runway" and "current cash position")
LABEL: N/A — no additional distinct quantitative claims requiring separate entries beyond those already audited above.

---

**SUMMARY OF KEY FINDINGS**

| Claim | Label |
|---|---|
| $38.42 million in revenue | SUPPORTED |
| $11.65 million in net income | UNSUPPORTED (actual: ~$116.5M) |
| ~$150.13 million market cap | UNSUPPORTED (actual: ~$1.50B) |
| FDA approval December 2025 | SUPPORTED |
| Sole commercialized product | SUPPORTED |
| $171.8 million in cash | SUPPORTED |
| $116.1 million operating cash burn | SUPPORTED |
| ~18-month runway | SUPPORTED |
| Novo Nordisk reduces self-funding burden | INFERENCE |
