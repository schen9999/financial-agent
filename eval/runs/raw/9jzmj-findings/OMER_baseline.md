# OMER — baseline

## Metadata

ticker: OMER
arm: baseline
judge_prompt_version: v2
context_sha256: 157fc96cc1b871d507c3c7513e153aaa3f430173235666b1f15db0c79a7297a5
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 399, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.563, "latency_s_total": 4.563, "parse_failure": 0, "prompt_tokens": 2764, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 407, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.846, "latency_s_total": 4.846, "parse_failure": 0, "prompt_tokens": 3239, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 181, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.301, "latency_s_total": 2.301, "parse_failure": 0, "prompt_tokens": 676, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 173, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.441, "latency_s_total": 2.441, "parse_failure": 0, "prompt_tokens": 669, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 225, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.006, "latency_s_total": 2.006, "parse_failure": 0, "prompt_tokens": 478, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 210, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.258, "latency_s_total": 2.258, "parse_failure": 0, "prompt_tokens": 478, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1341, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.266, "latency_s_total": 19.266, "parse_failure": 0, "prompt_tokens": 1978, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "OMER",
  "company_name": "Omeros Corporation",
  "current_price": 18.61,
  "currency": "USD",
  "market_cap": 1347146624.0,
  "pe_ratio": 11.278789,
  "forward_pe": 15.130081,
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
- Profitability is contingent on generating substantial revenue from YARTEMLEA sales

## Key Business Risks
- Commercialization challenges include physician and patient acceptance, reimbursement policies, manufacturing dependencies, and competition from alternative treatments
- The company faces risks related to regulatory compliance and potential safety issues
- International expansion depends on securing partnerships for markets outside the U.S.
- Reimbursement rates from government and private payers may not support profitability

## Strategic Partnerships
- The company has an agreement with Novo Nordisk involving zaltenibart, with milestone and royalty payments contingent on successful development and commercialization
- Future revenue from partnerships is uncertain and dependent on external factors

## Capital Requirements
- Substantial ongoing spending is expected for clinical trials, commercialization, R&D, and debt service
- Additional capital may be required to fund operations and advance product development

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors affecting its business:

## Product Commercialization Risks
- **YARTEMLEA dependency**: The company's profitability is heavily dependent on the commercial success of YARTEMLEA, its only commercialized product (FDA-approved in December 2025). Failure to successfully commercialize it could materially harm the business.
- **Commercialization challenges**: Potential obstacles include lack of physician and patient acceptance, limited marketing and sales experience, manufacturing and supply chain vulnerabilities, and unknown safety risks.

## Reimbursement and Pricing Risks
- **Coverage and reimbursement uncertainty**: Delays in obtaining adequate coverage or reimbursement from government and private payers could impair revenue generation and profitability.
- **Pricing pressures**: Government and private payers increasingly demand predetermined discounts and challenge medical product pricing, which could adversely impact product pricing and profitability.
- **Regulatory pricing controls**: Products may be subject to government price controls, particularly in the EU and other non-U.S. jurisdictions.

## Partnership and Dependency Risks
- **Novo Nordisk reliance**: The company's ability to realize value from zaltenibart depends entirely on Novo Nordisk's development and commercialization efforts, which are outside the company's control.

## Financial and Capital Risks
- **Cumulative operating losses**: The company has incurred cumulative operating losses since inception and expects to continue incurring losses.
- **Capital requirements**: Substantial additional capital will be needed for clinical trials, commercialization, R&D, and debt obligations, with no assurance that capital will be available on acceptable terms.
- **Debt obligations**: The company has convertible senior notes and other liabilities that could limit cash flow available for operations.

## Pre-written sections (judge input)

### Financial Health

Omeros Corporation trades at $18.61 with a market capitalization of $1.35 billion and an attractive forward P/E ratio of 15.1x, suggesting reasonable valuation relative to growth expectations. However, the company's financial profile reveals significant challenges: revenue of $38.4 million is modest for a $1.3 billion market cap, while the 3.25% profit margin indicates thin operational efficiency despite reported net income of $116.5 million. The current P/E of 11.3x appears deceptively low given the revenue-to-market cap ratio, raising questions about earnings quality and sustainability. Recent SEC filings emphasize material risks to profitability and commercial execution, suggesting investors should view current valuations cautiously until the company demonstrates consistent revenue growth and margin expansion.

### Recent Developments

Limited recent news is currently available for Omeros Corporation. The company's most recent SEC filings—a 10-K filed March 31, 2026, and a 10-Q filed August 12, 2026—emphasize significant operational and commercial risks, particularly regarding the company's ability to achieve sustained profitability. With a modest profit margin of 3.25% despite positive net income of $116.5 million on $38.4 million in revenue, investors should monitor upcoming earnings reports and pipeline developments closely. The stock's recent trading range ($4.06–$21.24 over 52 weeks) reflects volatility typical of biotech firms, warranting attention to clinical trial results and regulatory milestones that could materially impact valuation.

### SEC Filing Highlights

Omeros Corporation held $171.8 million in cash and short-term investments as of December 31, 2025, with annual operating cash burn of $116.1 million, providing approximately 18 months of runway without additional financing. The company's sole commercialized product, YARTEMLEA, received FDA approval in December 2025, making near-term profitability entirely dependent on successful market adoption and reimbursement. Key risks include limited commercial infrastructure, physician/patient acceptance uncertainty, and reliance on third-party manufacturing and distribution partners. The company carries $70.8 million in convertible senior notes due 2029 and maintains a strategic partnership with Novo Nordisk for zaltenibart development, with future revenues contingent on milestone achievements. Substantial capital will be required for ongoing clinical trials, commercialization efforts, and debt service, necessitating either significant YARTEMLEA revenue generation or additional financing.

### Risk Factors

- **YARTEMLEA Commercialization Dependency**: Omeros' profitability is heavily dependent on the commercial success of YARTEMLEA, its only FDA-approved product (approved December 2025). The company faces significant commercialization challenges including limited sales experience, physician/patient acceptance uncertainty, supply chain vulnerabilities, and unknown safety risks that could materially harm the business.

- **Reimbursement and Pricing Pressures**: Delays or inadequate coverage from government and private payers could impair revenue generation. Additionally, increasing pricing pressures and government price controls—particularly in non-U.S. markets—could adversely impact product profitability and margins.

- **Capital Requirements and Financial Losses**: The company has incurred cumulative operating losses since inception and expects continued losses. Substantial additional capital will be required for clinical trials, commercialization, and R&D, with no assurance funding will be available on acceptable terms. Existing debt obligations may further constrain operational cash flow.

## Audited (Exec Summary + Outlook)

### Executive Summary
Omeros Corporation is a commercial-stage biopharmaceutical company whose investment case now rests almost entirely on YARTEMLEA, its sole FDA-approved product (December 2025), as it trades at $18.61 with a market capitalization of $1.35 billion against revenue of just $38.4 million and approximately 18 months of cash runway supported by $171.8 million in cash and short-term investments. The stock is notable today because it sits at a critical inflection point: the wide 52-week trading range of $4.06–$21.24 reflects the market's deep uncertainty about whether early commercial momentum can justify a valuation that currently dwarfs reported revenues. The single most important near-term variable is the pace and breadth of YARTEMLEA's market adoption — specifically whether payer coverage and physician acceptance materialize quickly enough to reduce cash burn and forestall the need for dilutive additional financing.

### Outlook
The directional lean on Omeros is **cautious**, with a path to becoming more constructive that is narrow but real. The primary tailwind is the novelty and potential of YARTEMLEA as a freshly approved product, complemented by the strategic optionality embedded in the Novo Nordisk partnership for zaltenibart, where positive milestone achievements could meaningfully supplement the balance sheet without immediate dilution. Against these tailwinds, the headwinds are substantial: an annual operating cash burn of $116.1 million against an approximately 18-month runway creates a ticking clock, the company's limited commercial infrastructure introduces meaningful execution risk in the critical early launch window, and reimbursement uncertainty from both government and private payers could slow revenue ramp at precisely the moment it is most needed. Investors should monitor YARTEMLEA prescription volume trends and payer coverage decisions as the most immediate signals of commercial viability, watch for any updates on zaltenibart milestones from Novo Nordisk, and track the pace of cash burn relative to revenue generation in each quarterly filing. The thesis would strengthen materially if YARTEMLEA demonstrates accelerating adoption and broad reimbursement coverage, reducing the probability of dilutive financing; it would weaken if payer pushback, safety signals, or slower-than-expected physician uptake force the company back to capital markets on unfavorable terms before the product has established a durable revenue base.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative, forward-looking, and specific factual claim in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "YARTEMLEA, its sole FDA-approved product (December 2025)"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state "YARTEMLEA is the company's only commercialized product, approved by the FDA in December 2025," and the Risk Factors section confirms "FDA-approved in December 2025."

---

CLAIM: "trades at $18.61"
LABEL: SUPPORTED
REASON: The stock data explicitly lists `"current_price": 18.61`.

---

CLAIM: "market capitalization of $1.35 billion"
LABEL: SUPPORTED
REASON: The stock data lists `"market_cap": 1347146624.0`, which rounds to $1.35 billion; the Financial Health section also states "$1.35 billion."

---

CLAIM: "revenue of just $38.4 million"
LABEL: SUPPORTED
REASON: The stock data lists `"revenue": 38422000.0`, which rounds to $38.4 million, consistent with the pre-written sections.

---

CLAIM: "approximately 18 months of cash runway"
LABEL: INFERENCE
REASON: The SEC Highlights report $171.8 million in cash and $116.1 million annual operating cash burn; dividing $171.8M ÷ $116.1M ≈ 1.48 years ≈ 17.8 months, which the pre-written SEC Filing Highlights section explicitly rounds to "approximately 18 months," making this a directly derivable and pre-stated figure.

---

CLAIM: "$171.8 million in cash and short-term investments"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state "As of December 31, 2025, the company held $171.8 million in cash, cash equivalents, and short-term investments."

---

CLAIM: "52-week trading range of $4.06–$21.24"
LABEL: SUPPORTED
REASON: The stock data lists `"week_52_low": 4.06` and `"week_52_high": 21.24`.

---

CLAIM: "the wide 52-week trading range of $4.06–$21.24 reflects the market's deep uncertainty"
LABEL: INFERENCE
REASON: This is a directional interpretive statement derived from the observable spread between the 52-week low ($4.06) and high ($21.24) — a ratio of more than 5x — which is a straightforward characterization of volatility from two figures present in the source data.

---

CLAIM: "a valuation that currently dwarfs reported revenues"
LABEL: SUPPORTED
REASON: Market cap of ~$1.35 billion versus revenue of ~$38.4 million yields a price-to-sales ratio of approximately 35x, arithmetically confirming that market cap dwarfs revenues; both figures are present in the source data.

---

**OUTLOOK**

---

CLAIM: "an annual operating cash burn of $116.1 million"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state "Cash used in operations for 2025 was $116.1 million."

---

CLAIM: "approximately 18-month runway"
LABEL: INFERENCE
REASON: Same derivation as above: $171.8M ÷ $116.1M ≈ 17.8 months, explicitly pre-stated as "approximately 18 months" in the SEC Filing Highlights section, and arithmetically verifiable from source figures.

---

CLAIM: "the Novo Nordisk partnership for zaltenibart, where positive milestone achievements could meaningfully supplement the balance sheet without immediate dilution"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors both confirm "an agreement with Novo Nordisk involving zaltenibart, with milestone and royalty payments contingent on successful development and commercialization," and the pre-written SEC Filing Highlights section references this partnership with future revenues contingent on milestone achievements.

---

CLAIM: "the company's limited commercial infrastructure introduces meaningful execution risk in the critical early launch window"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state "The company has limited experience in marketing, selling, and distributing the product," and the Risk Factors section confirms "limited sales experience" as a named commercialization challenge.

---

CLAIM: "reimbursement uncertainty from both government and private payers could slow revenue ramp"
LABEL: SUPPORTED
REASON: The RAG Risk Factors explicitly state "Delays in obtaining adequate coverage or reimbursement from government and private payers could impair revenue generation and profitability."

---

No additional quantitative figures, price targets, specific thresholds, named ratios, or forward-looking numbers appear in the Outlook section beyond those already audited above. All claims in the Outlook are either qualitative/directional or reference figures already evaluated.
