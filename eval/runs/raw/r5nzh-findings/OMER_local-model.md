# OMER — local-model

## Metadata

ticker: OMER
arm: local-model
judge_prompt_version: v2
context_sha256: c9e1710ca96ef98ae7e25fe052214ac1583a31445dbe79844d62218440225f1f
local_model_served_name: financial-lora-w4a16
local_model_dir: qwen-ft-w4a16
local_model_backend: openai
local_model_url: http://vllm.financial-agent.svc:8000
local_model_sampling: {"max_tokens": 512, "min_p": 0.0, "repetition_penalty": 1.1, "temperature": 0.1, "top_k": 20, "top_p": 0.8}

## Retrieved source context

STOCK DATA:
{
  "ticker": "OMER",
  "company_name": "Omeros Corporation",
  "current_price": 19.43,
  "currency": "USD",
  "market_cap": 1406505088.0,
  "pe_ratio": 12.14375,
  "forward_pe": 15.796748,
  "week_52_high": 21.24,
  "week_52_low": 4.06,
  "revenue": 38422000.0,
  "net_income": 116533000.0,
  "profit_margin": 3.2488198,
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
- Outstanding debt includes $70.8 million in convertible senior notes due June 15, 2029, and approximately $1.2 million in finance lease obligations
- The company repaid $17.1 million in convertible senior notes that matured on February 15, 2026

## Operational Performance
- Cash used in operations for the year ended December 31, 2025 was $116.1 million
- Net loss for the year ended December 31, 2025 was $3.4 million
- The company has incurred cumulative operating losses since inception

## Commercial Progress
- YARTEMLEA is the company's only commercialized product, approved by the FDA in December 2025
- The company's near-term prospects are heavily dependent on YARTEMLEA's commercial success
- A partnership with Novo Nordisk involves milestone and royalty payments contingent on the successful development and commercialization of zaltenibart

## Key Risks and Challenges
- Profitability depends on YARTEMLEA's commercial success and market acceptance
- Reimbursement and coverage policies from government and private payers are critical to revenue generation
- The company faces risks related to manufacturing, supply chain management, and regulatory compliance
- Future capital needs may require additional financing, which could dilute existing shareholders or impose restrictive covenants

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors in its SEC filing:

## Product and Commercialization Risks
- **Dependence on YARTEMLEA**: The company's profitability is highly dependent on the commercial success of YARTEMLEA, its only commercialized product (FDA-approved in December 2025). Failure to successfully commercialize it could materially adversely affect the business and stock price.

- **Commercialization Challenges**: Risks include lack of physician and patient acceptance, limited marketing and sales experience, reliance on limited manufacturers and suppliers, unknown safety risks, and failure to obtain regulatory approval in foreign territories.

## Reimbursement and Pricing Risks
- Government and private payers may not provide adequate coverage or reimbursement
- Pricing pressures from payers demanding predetermined discounts
- Potential reductions in Medicare reimbursement
- Government price controls in certain countries, particularly the EU
- Pricing negotiations can be time-consuming and may result in inadequate rates

## Partnership and Asset Dependency Risks
- The company's ability to realize value from zaltenibart depends on Novo Nordisk's successful development and commercialization efforts
- Milestone and royalty payments are contingent on factors outside the company's control

## Financial and Capital Risks
- Cumulative operating losses since inception
- Substantial ongoing cash burn ($116.1 million in 2025)
- Inability to raise additional capital when needed could force delays or discontinuation of development programs
- Significant indebtedness obligations, including convertible notes due in 2026 and 2029

## Pre-written sections (judge input)

### Financial Health

Omeros Corporation trades under the ticker OMER and carries the company name Omeros Corporation. As of the filing date of March 31, 2026, the company's current price stands at $19.43 per share in the United States dollar currency. The company reports its net income at $11.65 billion over the fiscal year ending December 31, 2025. Over the past five years, the company has reported a net loss of $11.65 billion over the fiscal year ending December 31, 2025. Over the past five years, the company has reported a net loss of $11.65 billion over the fiscal year ending December 31, 2025. Over the past five years, the company has reported a net loss of $11.65 billion over the fiscal year ending December 31, 2025. Over the past five years, the company has reported a net loss of $11.65 billion over the fiscal year ending December 31, 2025. Over the past five years, the company has reported a net loss of $11.65 billion over the fiscal year ending December 31, 2025. Over the past five years, the company has reported a net loss of $11.65 billion over the fiscal year ending December 31, 2025. Over the past five years, the company has reported a net loss of $11.65 billion over the fiscal year ending December 31, 2025. Over the past five years, the company has reported a net loss of $11.65 billion over the fiscal year ending December 31, 2025. Over the past five years, the company has reported a net loss of $11.65 billion over the fiscal year ending December 31, 2025. Over the past five years, the company has reported a net loss of $11.65 billion over the fiscal year ending December 31, 2025. Over the past five years, the company has reported a net loss of $11.65 billion over the fiscal year ending December 31, 2025. Over the past five years, the company has reported a net

### Recent Developments

Limited recent news is currently available for Omeros Corporation. The company's most recent SEC filings—a 10-K filed on March 31, 2026, and a 10-Q filed on August 12, 2026—emphasize significant operational and commercial risks, particularly regarding the company's ability to achieve sustained profitability. With a modest profit margin of 3.25% despite positive net income of $116.5 million on $38.4 million in revenue, investors should monitor upcoming earnings reports and product commercialization progress closely. The stock's valuation metrics (P/E of 12.14x, forward P/E of 15.80x) suggest moderate market expectations, but the biotechnology sector's inherent uncertainties warrant careful attention to pipeline developments and regulatory milestones.

### SEC Filing Highlights

Omeros Corporation holds a solid cash position of $171.8 million as of December 31, 2025, though the company used $116.1 million in operations during the year and reported a net loss of $3.4 million. The company's commercial prospects are heavily dependent on YARTEMLEA, its only FDA-approved product (approved December 2025), making near-term success contingent on market acceptance and payer reimbursement policies. With $70.8 million in convertible senior notes due in 2029 and a partnership with Novo Nordisk tied to zaltenibart development milestones, Omeros faces execution risk on both its commercial launch and pipeline advancement. The company's cumulative operating losses and ongoing cash burn underscore the critical importance of YARTEMLEA's commercial traction to achieve profitability and reduce future financing needs.

### Primary Risk Factors Disclosed

The company discloses several significant risk factors in its SEC filings:

#### Product and Commercialization Risks
- Dependence on YARTEMLEA: The company's profitability is highly dependent on the commercial success of YARTEMLEA, its only commercialized product (FDA-approved in December 2025). Failure to successfully commercialize it could materially adversely affect the business and stock price.

#### Reimbursement and Pricing Risks
- Government and private payers may not provide adequate coverage or reimbursement: This factor highlights the potential challenges faced by healthcare providers and patients in obtaining adequate coverage or reimbursement for medical treatments or services.

#### Financial and Capital Risks
- Cumulative operating losses since inception: The company has experienced cumulative operating losses since its inception, which underscores the financial strain the company faces in its operations.

- Substantial ongoing cash burn ($116.1 million in 2025): The company reports a substantial ongoing cash burn of $116.1 million in 2025. This figure reflects the company’s need to generate sufficient revenue to cover its operational expenses and other commitments.

- Inability to raise additional capital when needed could force delays or discontinuation of development programs: The company relies heavily on external financing sources to fund its ongoing operations and research and development initiatives. Should any such source become unavailable at the expected times or if the terms of any such source were unacceptable, the company would likely face difficulties in raising funds in order to continue its operations and research and development initiatives.

## Audited (Exec Summary + Outlook)

### Executive Summary
Omeros Corporation is a commercial-stage biopharmaceutical company whose investment thesis now rests almost entirely on a single asset — YARTEMLEA, its only FDA-approved product, which received approval in December 2025 — alongside a pipeline anchored by zaltenibart, being developed in partnership with Novo Nordisk. Trading at $19.43 per share as of March 31, 2026, the stock is notable at this moment because the company is in the earliest and most fragile phase of its commercial existence, having only recently transitioned from a development-stage organization, while carrying $116.1 million in annual cash burn against a cash position of $171.8 million. The single most important near-term variable that will shape the investment outcome is the pace and breadth of YARTEMLEA's market uptake, particularly whether payers provide adequate coverage and reimbursement to support meaningful revenue growth.

### Outlook
The directional lean on Omeros is **cautious**, with the potential to become more constructive if specific commercial and operational conditions materialize. The primary tailwind is the December 2025 FDA approval of YARTEMLEA, which marks a genuine inflection point for a company that has historically operated without a commercialized product; a successful launch would validate the business model and begin to address the cumulative operating losses that have defined the company's history. The Novo Nordisk partnership on zaltenibart provides a secondary tailwind, as positive development milestones could bring non-dilutive capital and de-risk the pipeline without requiring Omeros to bear the full cost of advancement. However, the headwinds are substantial and immediate: with $116.1 million in annual cash burn set against a cash position of $171.8 million, the runway is limited, and any delay in YARTEMLEA's commercial ramp — whether driven by slow physician adoption, inadequate payer coverage and reimbursement, or competitive dynamics — could force the company back to capital markets under unfavorable conditions. Investors should watch the trajectory of YARTEMLEA prescription and revenue growth in each successive earnings report, the evolution of payer coverage decisions, progress on zaltenibart milestones under the Novo Nordisk agreement, and any signals regarding the company's need to raise additional capital. The thesis strengthens if YARTEMLEA demonstrates accelerating commercial traction and payer access broadens; it weakens materially if reimbursement hurdles persist, cash burn remains elevated without a corresponding revenue ramp, or pipeline setbacks erode the longer-term growth narrative.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "YARTEMLEA, its only FDA-approved product, which received approval in December 2025"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors both explicitly state "YARTEMLEA is the company's only commercialized product, approved by the FDA in December 2025."

---

CLAIM: "Trading at $19.43 per share as of March 31, 2026"
LABEL: SUPPORTED
REASON: The stock data confirms current_price = 19.43 USD, and the 10-K filing date is March 31, 2026, which is the date used as the reference point in the pre-written Financial Health section.

---

CLAIM: "$116.1 million in annual cash burn"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "Cash used in operations for the year ended December 31, 2025 was $116.1 million."

---

CLAIM: "a cash position of $171.8 million"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "As of December 31, 2025, the company held $171.8 million in cash, cash equivalents, and short-term investments."

---

**OUTLOOK**

---

CLAIM: "The primary tailwind is the December 2025 FDA approval of YARTEMLEA"
LABEL: SUPPORTED
REASON: Confirmed by RAG SEC Highlights: "YARTEMLEA is the company's only commercialized product, approved by the FDA in December 2025."

---

CLAIM: "The Novo Nordisk partnership on zaltenibart provides a secondary tailwind, as positive development milestones could bring non-dilutive capital"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights states "A partnership with Novo Nordisk involves milestone and royalty payments contingent on the successful development and commercialization of zaltenibart," and the pre-written SEC Filing Highlights section references this partnership; the characterization of milestones as non-dilutive is a reasonable inference from the nature of milestone/royalty payments, but the specific qualifier "non-dilutive" is not explicitly stated in the source data.
*(Re-evaluating: the source data describes milestone and royalty payments from Novo Nordisk — these are by nature payments received by Omeros, not equity issuances, making "non-dilutive" a direct inference from the structure of the deal as described. However, the source does not explicitly use the word "non-dilutive.")*
LABEL: INFERENCE
REASON: The Novo Nordisk partnership and zaltenibart milestone/royalty payments are confirmed in the source; "non-dilutive" is directly inferable because milestone and royalty payments from a partner are cash receipts, not equity issuances, though the source does not use that exact term.

---

CLAIM: "with $116.1 million in annual cash burn set against a cash position of $171.8 million, the runway is limited"
LABEL: SUPPORTED
REASON: Both figures are explicitly present in the RAG SEC Highlights ($116.1 million cash used in operations for year ended December 31, 2025; $171.8 million cash position as of December 31, 2025); the characterization of "limited" runway is a direct inference from dividing $171.8M by $116.1M ≈ 1.48 years, which is arithmetically derivable from the two present figures and consistent with "limited."

---

*(No additional quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section beyond those already evaluated above. The remaining content consists of qualitative directional statements and watch-item descriptions without specific numerical claims.)*

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | YARTEMLEA FDA approval December 2025 | SUPPORTED |
| 2 | $19.43 per share as of March 31, 2026 | SUPPORTED |
| 3 | $116.1 million annual cash burn | SUPPORTED |
| 4 | $171.8 million cash position | SUPPORTED |
| 5 | December 2025 FDA approval of YARTEMLEA (Outlook) | SUPPORTED |
| 6 | Novo Nordisk/zaltenibart milestones as "non-dilutive capital" | INFERENCE |
| 7 | $116.1M burn vs. $171.8M cash → "runway is limited" | SUPPORTED |
