# OMER — baseline

## Metadata

ticker: OMER
arm: baseline
judge_prompt_version: v2
context_sha256: 95cb269eebb404d996bf8984c678e4f4a98fc62c37920d44eefb8251cfe78cf2

## Retrieved source context

STOCK DATA:
{
  "ticker": "OMER",
  "company_name": "Omeros Corporation",
  "current_price": 20.13,
  "currency": "USD",
  "market_cap": 1457176832.0,
  "pe_ratio": 12.2,
  "forward_pe": 16.365852,
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
- Commercialization challenges include physician and patient acceptance, reimbursement policies, manufacturing dependencies, and competition from alternative treatments
- The company faces risks related to regulatory compliance and potential safety issues
- International expansion depends on securing acceptable partnership arrangements
- Reimbursement rates from government and private payers may not support profitability

## Strategic Partnerships
- The company has an agreement with Novo Nordisk involving zaltenibart, with milestone and royalty payments contingent on successful development and commercialization
- Future revenue from partnerships is uncertain and subject to external factors

## Capital Requirements
- Substantial ongoing spending is expected for clinical trials, commercialization, R&D, and debt service
- Additional capital may be required to fund operations and advance product development

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors affecting its business:

## Product Commercialization Risks
- **YARTEMLEA dependency**: The company's profitability is heavily dependent on the commercial success of YARTEMLEA, its only commercialized product (FDA-approved in December 2025). Failure to successfully commercialize it could materially harm the business.
- **Commercialization challenges**: Potential obstacles include lack of physician and patient acceptance, limited marketing and sales experience, manufacturing and supply chain dependencies, and unknown safety risks.

## Reimbursement and Pricing Risks
- Inadequate coverage or reimbursement from government and private payers could severely impact revenue prospects
- Government and private payers increasingly demand predetermined discounts from list prices
- Pricing negotiations can be time-consuming and may result in unfavorable terms
- Some countries impose government price controls on pharmaceutical products
- Reimbursement approval in one jurisdiction does not guarantee similar approval elsewhere

## Partnership and Development Risks
- The company's ability to realize value from zaltenibart depends on Novo Nordisk's successful development and commercialization efforts, which are outside the company's control
- Milestone and royalty payments from the Novo Nordisk partnership are contingent on factors beyond the company's control

## Financial and Capital Risks
- The company has incurred cumulative operating losses since inception
- Substantial ongoing cash burn ($116.1 million in 2025) with uncertain ability to generate sufficient revenue
- May require additional capital financing, which may not be available on acceptable terms
- Existing indebtedness obligations could limit operational cash flow

## Pre-written sections (judge input)

### Financial Health

Omeros Corporation trades at $20.13 with a market capitalization of $1.46 billion and a reasonable P/E ratio of 12.2x, suggesting moderate valuation relative to earnings. However, the company's financial profile reveals significant challenges: revenue of $38.4 million is minimal relative to market cap, while the net income of $116.5 million appears anomalous given the low revenue base, indicating potential one-time gains or accounting adjustments rather than sustainable operational profitability. The 3.25% profit margin is thin, and the forward P/E of 16.4x suggests investor expectations for future growth that may be difficult to achieve. The stock's 52-week range ($4.06–$21.24) reflects substantial volatility, typical of early-stage biotech firms dependent on product commercialization success. Overall, Omeros presents a speculative investment profile with execution risk outweighing current financial metrics.

### Recent Developments

Limited recent news is currently available for Omeros Corporation. The company's most recent SEC filings—a 10-K filed on March 31, 2026, and a 10-Q filed on August 12, 2026—emphasize significant risk factors related to product commercialization and profitability achievement, suggesting ongoing operational challenges in the biotechnology sector. With a modest forward P/E of 16.4x and a 52-week trading range of $4.06 to $21.24, the stock reflects considerable volatility typical of biotech companies dependent on clinical and commercial milestones. Investors should monitor upcoming product developments and earnings reports for clarity on the company's path to sustained profitability.

### SEC Filing Highlights

Omeros Corporation held $171.8 million in cash and short-term investments as of December 31, 2025, with annual operating cash burn of $116.1 million, providing approximately 18 months of runway at current burn rates. The company's commercial prospects are heavily concentrated on YARTEMLEA, which received FDA approval in December 2025 and represents the company's only commercialized product, though management acknowledges limited experience in marketing and distribution. Outstanding debt of $70.8 million in convertible senior notes due 2029 and ongoing R&D spending create significant capital requirements, with profitability contingent on achieving substantial YARTEMLEA revenue and successful reimbursement negotiations. The company faces material commercialization risks including physician/patient adoption, payer reimbursement policies, manufacturing dependencies, and competitive pressures from alternative treatments. Strategic partnerships, including a Novo Nordisk agreement for zaltenibart, provide potential future revenue but remain subject to development and commercialization milestones.

### Risk Factors

- **YARTEMLEA Commercialization Dependency**: Omeros' profitability depends almost entirely on the commercial success of YARTEMLEA, its only FDA-approved product (approved December 2025). The company faces significant commercialization challenges including limited sales experience, physician/patient acceptance uncertainty, supply chain dependencies, and unknown safety risks that could materially harm the business.

- **Reimbursement and Pricing Uncertainty**: Inadequate coverage or unfavorable reimbursement decisions from government and private payers could severely impact revenue prospects. Payers increasingly demand substantial discounts from list prices, and reimbursement approval varies by jurisdiction, creating unpredictable revenue streams.

- **Substantial Cash Burn with Limited Financial Runway**: The company burned $116.1 million in cash during 2025 with uncertain ability to generate sufficient revenue to offset ongoing losses. Additional capital financing may be required but may not be available on acceptable terms, and existing debt obligations could further constrain operational flexibility.

## Audited (Exec Summary + Outlook)

### Executive Summary
Omeros Corporation is a commercial-stage biotechnology company whose investment profile is now defined almost entirely by YARTEMLEA, its sole FDA-approved product (approved December 2025), launched against a backdrop of $38.4 million in revenue and a $1.46 billion market capitalization that prices in substantial future commercial success. The stock is notable now because it sits near the top of its 52-week range ($4.06–$21.24) at $20.13, reflecting early optimism around the YARTEMLEA launch, yet the company carries approximately 18 months of cash runway at its current burn rate of $116.1 million annually — a timeline that leaves little margin for a slow commercial ramp. The single most important near-term variable is the pace and breadth of payer reimbursement decisions for YARTEMLEA, which will determine whether the company can generate sufficient revenue to reduce cash burn before it must seek additional financing.

### Outlook
The directional lean on Omeros is **cautious**, with the balance of near-term risk tilted to the downside given the company's concentrated single-product exposure, limited commercialization experience, and a cash runway that narrows meaningfully if YARTEMLEA adoption is slow. The primary tailwind is the product's recent FDA approval and the potential for the Novo Nordisk partnership on zaltenibart to provide non-dilutive capital and pipeline optionality; a secondary tailwind would be any favorable and broad payer reimbursement decisions that accelerate physician adoption. The key variables investors should monitor are: the trajectory of YARTEMLEA prescription and revenue growth in quarterly earnings reports, the breadth and speed of payer coverage determinations, any updates to the zaltenibart development timeline and milestone triggers under the Novo Nordisk agreement, and whether management signals a need for additional capital financing. The cautious view would shift toward a more constructive stance if YARTEMLEA demonstrates clear commercial momentum — evidenced by improving reimbursement coverage, growing physician adoption, and a meaningful reduction in quarterly cash burn — while the thesis would weaken further if payer pushback limits access, if a dilutive capital raise is announced, or if any safety signal emerges that disrupts the commercial launch.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "YARTEMLEA, its sole FDA-approved product (approved December 2025)"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors both explicitly state "YARTEMLEA is the company's only commercialized product, approved by the FDA in December 2025."

---

CLAIM: "$38.4 million in revenue"
LABEL: SUPPORTED
REASON: The raw source data lists revenue of $38,422,000, which rounds to $38.4 million; the Financial Health pre-written section also states "revenue of $38.4 million."

---

CLAIM: "$1.46 billion market capitalization"
LABEL: SUPPORTED
REASON: The raw source data lists market_cap of $1,457,176,832, which rounds to $1.46 billion; the Financial Health section also states "market capitalization of $1.46 billion."

---

CLAIM: "sits near the top of its 52-week range ($4.06–$21.24) at $20.13"
LABEL: SUPPORTED
REASON: The 52-week low is $4.06 and high is $21.24 per source data; $20.13 is the current price. The range width is $17.18; $20.13 sits ($20.13 − $4.06) / ($21.24 − $4.06) = $16.07 / $17.18 ≈ 93.5% of the way from low to high, confirming it is near the top of the range. The positional claim holds arithmetically.

---

CLAIM: "approximately 18 months of cash runway at its current burn rate of $116.1 million annually"
LABEL: SUPPORTED
REASON: The SEC Highlights state cash of $171.8 million and operating cash burn of $116.1 million for 2025; $171.8M / $116.1M ≈ 1.48 years ≈ 17.8 months, which rounds to approximately 18 months, consistent with the pre-written SEC Filing Highlights section which also states "approximately 18 months of runway."

---

**OUTLOOK**

---

CLAIM: "the Novo Nordisk partnership on zaltenibart to provide non-dilutive capital and pipeline optionality"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors both explicitly reference "an agreement with Novo Nordisk involving zaltenibart, with milestone and royalty payments contingent on successful development and commercialization," confirming the partnership and zaltenibart product name exist in the source data.

---

CLAIM: "any updates to the zaltenibart development timeline and milestone triggers under the Novo Nordisk agreement"
LABEL: SUPPORTED
REASON: The RAG Risk Factors explicitly state "milestone and royalty payments from the Novo Nordisk partnership are contingent on factors beyond the company's control," confirming the existence of milestone triggers under the Novo Nordisk/zaltenibart agreement in the source data.

---

**No additional standalone quantitative figures, price targets, specific ratios, named percentages, or forward-looking numerical thresholds appear in the Outlook section beyond those already evaluated above.** The remaining Outlook content consists of qualitative directional statements and scenario descriptions that do not contain specific quantitative claims requiring arithmetic verification.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | YARTEMLEA sole FDA-approved product, approved December 2025 | SUPPORTED |
| 2 | $38.4 million in revenue | SUPPORTED |
| 3 | $1.46 billion market capitalization | SUPPORTED |
| 4 | Near top of 52-week range ($4.06–$21.24) at $20.13 | SUPPORTED |
| 5 | ~18 months cash runway at $116.1M annual burn | SUPPORTED |
| 6 | Novo Nordisk partnership on zaltenibart | SUPPORTED |
| 7 | Milestone triggers under Novo Nordisk agreement | SUPPORTED |

All audited claims in the Executive Summary and Outlook are **SUPPORTED** by the source data. No unsupported or inference-only claims were identified.
