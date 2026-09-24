# OMER — local-model

## Metadata

ticker: OMER
arm: local-model
judge_prompt_version: v2
context_sha256: fd67dad6e9be6c000bb7ca27f7abfb5a81f2dd049555fa4034dbcbc49e6ba166
local_model_served_name: qwen2.5-1.5b-instruct
local_model_dir: qwen2.5-1.5b-instruct
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
- Profitability depends significantly on YARTEMLEA's commercial success

## Strategic Partnerships
- The company has an agreement with Novo Nordisk involving zaltenibart, with potential milestone and royalty payments contingent on successful development and commercialization
- Future royalty revenue may vary significantly based on pricing, reimbursement, sales volumes, and market conditions

## Key Risks and Challenges
- Significant capital requirements for clinical trials, manufacturing, commercialization, and R&D
- Dependence on limited manufacturers and suppliers
- Reimbursement and coverage uncertainties from government and private payers
- Competitive disadvantages related to debt levels and capital access
- Uncertainty regarding ability to achieve sustained profitability

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors in its SEC filing:

## Product Commercialization Risks
- **Dependence on YARTEMLEA**: The company's profitability is highly dependent on the commercial success of YARTEMLEA, its only commercialized product (FDA-approved in December 2025). Failure to successfully commercialize it could materially adversely affect the business and stock price.
- **Commercialization challenges** including lack of physician and patient acceptance, limited marketing experience, manufacturing and supply chain dependencies, and competition from alternative treatments.

## Reimbursement and Pricing Risks
- Inadequate coverage or reimbursement from government and private payers could impair revenue generation and profitability.
- Government and private payers increasingly demand predetermined discounts from list prices and challenge medical product pricing.
- Pricing negotiations can be time-consuming and may result in unfavorable terms or delayed reimbursement.
- In some countries, products may be subject to government price controls.

## Partnership Dependency Risk
- The company's ability to realize value from zaltenibart depends on Novo Nordisk's successful development and commercialization efforts under their partnership agreement, with payments contingent on factors outside the company's control.

## Financial and Capital Risks
- The company has incurred cumulative operating losses since inception and may be unable to raise additional capital when needed.
- Substantial ongoing cash burn for clinical trials, commercialization, R&D, and debt obligations.
- Existing indebtedness ($70.8 million in convertible notes due 2029 and other obligations) could limit available cash flow.

## Pre-written sections (judge input)

### Financial Health

**Price:** Omeros Corporation's current stock price is $20.74 per share, reflecting its performance within the healthcare sector.

**Market Cap:** With a market capitalization of $15.01 billion, Omeros Corporation stands as one of the largest players in the biotechnology industry.

**P/E Ratio:** The company has a Price-to-Earnings (P/E) ratio of 12.57, indicating that investors are willing to pay approximately 12.57 times earnings for each dollar of shareholder equity.

**Forward PE Ratio:** The forward P/E ratio of 16.86 suggests that analysts expect the company's earnings to grow at a rate faster than the overall market over the next fiscal year.

**Revenue:** Omeros Corporation reported revenue of $384.2 million for the most recent quarter, demonstrating strong growth compared to previous periods.

**Net Income:** The net income for the period was $116.53 million, representing a significant portion of the total revenue.

**Profit Margin:** The profit margin of 3.25% indicates that only a small percentage of revenues translates into profits, highlighting the competitive nature of the company's operations.

Overall, Omeros Corporation shows promising financial health with robust revenue growth and a relatively low profit margin, which reflects the high expectations placed on the company's products and programs. However, investors should remain vigilant given the inherent risks associated with the biotechnology industry.

### Recent Developments

No significant recent news announcements are currently available for Omeros Corporation. However, the company's most recent SEC filings (10-K filed March 31, 2026 and 10-Q filed August 12, 2026) emphasize substantial operational and commercial risks that investors should carefully evaluate. The company's ability to achieve sustained profitability remains dependent on successful commercialization of its product pipeline in a competitive biotechnology environment. Investors should monitor upcoming clinical trial results, regulatory approvals, and quarterly earnings reports for material updates on the company's commercial progress and financial trajectory.

### SEC Filing Highlights

Omeros holds $171.8 million in cash and short-term investments as of December 31, 2025, with 2025 operating cash burn of $116.1 million, providing approximately 18 months of runway at current burn rates. The company's sole commercialized product, YARTEMLEA (approved by FDA in December 2025), represents the critical near-term driver of financial viability, though the company has limited commercial infrastructure experience. Outstanding debt of $70.8 million in convertible notes due 2029 and a history of cumulative operating losses underscore the need for YARTEMLEA revenue generation to achieve profitability. Strategic partnerships, including a Novo Nordisk agreement for zaltenibart with potential milestone and royalty payments, provide supplementary upside but remain contingent on successful development and commercialization. Key risks include significant capital requirements for R&D and manufacturing, reimbursement uncertainties, and dependence on limited suppliers.

### Risk Factors

1. **Product Commercialization Risks**
   - Dependence on YARTEMLEA: The company's profitability is highly dependent on the commercial success of YARTEMLEA, its only commercialized product (FDA-approved in December 2025). Failure to successfully commercialize it could materially adversely affect the business and stock price.

2. **Reimbursement and Pricing Risks**
   - Adequate coverage or reimbursement from government and private payers could impair revenue generation and profitability.
   - Increasing pressure from government and private payers to negotiate lower prices and discounts.
   - Potential delays in reimbursement approval or payment terms.

## Audited (Exec Summary + Outlook)

### Executive Summary
Omeros Corporation is a biotechnology company operating within one of the industry's most competitive landscapes, holding a market capitalization of $15.01 billion and reporting $384.2 million in revenue for its most recent quarter, yet carrying a profit margin of just 3.25% — a combination that reflects both the scale of its commercial ambitions and the cost intensity of its operations. The stock is notable now because the company is at a critical commercial inflection point: YARTEMLEA, its sole FDA-approved product (cleared in December 2025), has only recently entered the market, and the company's approximately 18 months of cash runway means the window for demonstrating commercial traction is narrow and consequential. The single most important near-term variable is the pace and breadth of YARTEMLEA's market uptake, particularly its ability to secure adequate reimbursement coverage from government and private payers, which will determine whether Omeros can reduce its cash burn and move toward sustained profitability before needing to raise additional capital.

### Outlook
The directional outlook for Omeros is **cautiously constructive, but contingent**. The primary tailwind is the recent FDA approval of YARTEMLEA, which transitions the company from a pre-revenue development stage into an active commercial enterprise — a meaningful de-risking event that the forward P/E ratio of 16.86 suggests the market is beginning to price in. The Novo Nordisk partnership for zaltenibart provides an additional layer of potential upside through milestone and royalty payments, offering some diversification beyond a single-product dependency. However, the headwinds are substantial and immediate: the company's limited commercial infrastructure experience introduces meaningful execution risk at precisely the moment execution matters most, and the approximately 18-month cash runway — against a backdrop of $70.8 million in convertible notes due 2029 and a history of cumulative operating losses — leaves little margin for a slow commercial ramp. Investors should watch YARTEMLEA's reimbursement coverage trajectory closely, as payer decisions from both government and private insurers will be the most direct leading indicator of revenue sustainability; they should also monitor quarterly cash burn trends for signs that commercial revenue is meaningfully offsetting operating expenses. The thesis would strengthen if YARTEMLEA achieves broad payer coverage, early prescription volume signals are favorable, and cash burn begins to moderate; it would weaken if reimbursement negotiations stall, commercial uptake disappoints, or the company signals a need for dilutive capital raises before the product reaches self-sustaining revenue levels.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative, forward-looking, and specific factual claim in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "holding a market capitalization of $15.01 billion"
LABEL: UNSUPPORTED
REASON: The raw source data shows market_cap = $1,501,333,760 (~$1.50 billion); the pre-written Financial Health section erroneously states "$15.01 billion," but that figure is a decimal-point error by a factor of 10, and the correct source figure is $1.50 billion — the claim reproduces the pre-written section's error and does not match the actual source data.

---

CLAIM: "reporting $384.2 million in revenue for its most recent quarter"
LABEL: UNSUPPORTED
REASON: The raw source data shows revenue = $38,422,000 (~$38.4 million); the pre-written section misrepresents this as "$384.2 million," and the AI brief reproduces that error — the actual figure is approximately one-tenth of the claimed amount, and the period label "most recent quarter" is also unverified (the source data does not specify a quarterly period).

---

CLAIM: "carrying a profit margin of just 3.25%"
LABEL: SUPPORTED
REASON: The raw source data shows profit_margin = 3.2488198, which rounds to 3.25%; within 0.15 percentage points of the stated figure.

---

CLAIM: "YARTEMLEA, its sole FDA-approved product (cleared in December 2025)"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors sections both explicitly state "YARTEMLEA is the company's only commercialized product, approved by the FDA in December 2025."

---

CLAIM: "the company's approximately 18 months of cash runway"
LABEL: INFERENCE
REASON: The pre-written SEC Filing Highlights section states this directly ("approximately 18 months of runway at current burn rates"), and it is derivable from the source data: $171.8M cash ÷ $116.1M annual burn ≈ 1.48 years (~17.8 months), which rounds to approximately 18 months.

---

CLAIM: "the single most important near-term variable is the pace and breadth of YARTEMLEA's market uptake, particularly its ability to secure adequate reimbursement coverage from government and private payers"
LABEL: SUPPORTED
REASON: The RAG Risk Factors and SEC Highlights sections explicitly identify YARTEMLEA commercialization and reimbursement/coverage from government and private payers as the primary near-term risks and drivers of profitability.

---

**OUTLOOK**

---

CLAIM: "the forward P/E ratio of 16.86 suggests the market is beginning to price in [the de-risking event of FDA approval]"
LABEL: SUPPORTED
REASON: The raw source data shows forward_pe = 16.861788, which rounds to 16.86; the interpretive framing is an inference from the data, but the figure itself is accurate and present in the source.

---

CLAIM: "The Novo Nordisk partnership for zaltenibart provides an additional layer of potential upside through milestone and royalty payments"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "The company has an agreement with Novo Nordisk involving zaltenibart, with potential milestone and royalty payments contingent on successful development and commercialization."

---

CLAIM: "the approximately 18-month cash runway"
LABEL: INFERENCE
REASON: Same derivation as above: $171.8M ÷ $116.1M ≈ 17.8 months, consistent with "approximately 18 months"; the pre-written section also states this figure explicitly.

---

CLAIM: "$70.8 million in convertible notes due 2029"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "Outstanding debt includes $70.8 million in convertible senior notes due June 15, 2029."

---

CLAIM: "a history of cumulative operating losses"
LABEL: SUPPORTED
REASON: Both the RAG SEC Highlights and Risk Factors sections explicitly state "The company has a history of cumulative operating losses since inception."

---

CLAIM: "the company's limited commercial infrastructure experience introduces meaningful execution risk"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights states "the company has limited experience in marketing, selling, and distributing the product," and the Risk Factors section identifies commercialization challenges including "limited marketing experience."

---

CLAIM: "payer decisions from both government and private insurers will be the most direct leading indicator of revenue sustainability"
LABEL: SUPPORTED
REASON: The RAG Risk Factors and SEC Highlights both explicitly identify reimbursement and coverage from government and private payers as a primary risk to revenue generation and profitability.

---

**SUMMARY TABLE OF LABELS**

| # | Claim | Label |
|---|-------|-------|
| 1 | Market cap $15.01 billion | UNSUPPORTED |
| 2 | Revenue $384.2 million (most recent quarter) | UNSUPPORTED |
| 3 | Profit margin 3.25% | SUPPORTED |
| 4 | YARTEMLEA sole FDA-approved product, December 2025 | SUPPORTED |
| 5 | ~18 months cash runway (Executive Summary) | INFERENCE |
| 6 | Reimbursement coverage as key near-term variable | SUPPORTED |
| 7 | Forward P/E of 16.86 | SUPPORTED |
| 8 | Novo Nordisk / zaltenibart milestone and royalty payments | SUPPORTED |
| 9 | ~18 months cash runway (Outlook) | INFERENCE |
| 10 | $70.8 million convertible notes due 2029 | SUPPORTED |
| 11 | History of cumulative operating losses | SUPPORTED |
| 12 | Limited commercial infrastructure experience | SUPPORTED |
| 13 | Government and private payer decisions as leading indicator | SUPPORTED |
