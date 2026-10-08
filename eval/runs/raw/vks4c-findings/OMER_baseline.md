# OMER — baseline

## Metadata

ticker: OMER
arm: baseline
judge_prompt_version: v2
context_sha256: dbbfb4adea8b7b2fe822262cd58b5e6eef7616dba9ede8a5e4e93d9d90dc3738
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 347, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.828, "latency_s_total": 3.828, "parse_failure": 0, "prompt_tokens": 2764, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 353, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.541, "latency_s_total": 4.541, "parse_failure": 0, "prompt_tokens": 3239, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 223, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.03, "latency_s_total": 3.03, "parse_failure": 0, "prompt_tokens": 672, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 168, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.245, "latency_s_total": 2.245, "parse_failure": 0, "prompt_tokens": 665, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 226, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.584, "latency_s_total": 2.584, "parse_failure": 0, "prompt_tokens": 424, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 187, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.996, "latency_s_total": 1.996, "parse_failure": 0, "prompt_tokens": 426, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1385, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.299, "latency_s_total": 19.299, "parse_failure": 0, "prompt_tokens": 2008, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "OMER",
  "company_name": "Omeros Corporation",
  "current_price": 18.75,
  "currency": "USD",
  "market_cap": 1357281024.0,
  "pe_ratio": 15.368852,
  "forward_pe": 15.243902,
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

## Debt Structure
- $70.8 million outstanding in convertible senior notes due June 15, 2029
- $17.1 million in convertible senior notes that matured February 15, 2026 and have been repaid
- Approximately $1.2 million in outstanding finance lease obligations

## Commercial Product
- YARTEMLEA is the company's only commercialized product, approved by the FDA in December 2025
- Near-term profitability is heavily dependent on YARTEMLEA's commercial success
- The company has limited experience in marketing, selling, and distributing the product

## Key Risks and Challenges
- Significant dependence on YARTEMLEA's market acceptance and physician/patient adoption
- Reliance on limited manufacturers and suppliers for the product
- Uncertainty around reimbursement and coverage from government and private payers
- Cumulative operating losses since inception
- Continued substantial cash burn expected for clinical trials, commercialization, R&D, and debt service

## Strategic Partnerships
- Agreement with Novo Nordisk involving zaltenibart with potential milestone and royalty payments contingent on successful development and commercialization

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors in its SEC filing:

## Product Commercialization Risks
- Heavy dependence on YARTEMLEA, the company's only commercialized product (FDA-approved in December 2025), for achieving profitability
- Potential lack of acceptance by physicians, patients, payers, and the medical community
- Limited experience in marketing, selling, and distributing the product
- Reliance on a limited number of manufacturers and suppliers
- Unknown safety risks
- Failure to obtain regulatory approval in foreign territories

## Reimbursement and Pricing Risks
- Significant delays in obtaining coverage or reimbursement for newly approved products
- Reimbursement rates may not allow the company to make a profit or cover costs
- Government and private payers increasingly demanding predetermined discounts from list prices
- Potential reductions in Medicare reimbursement
- Government price controls in certain countries, particularly in the EU
- Time-consuming and resource-intensive pricing negotiations with governmental authorities

## Partnership and Development Risks
- Dependence on Novo Nordisk's successful development and commercialization of zaltenibart, with milestone and royalty payments contingent on factors outside the company's control

## Financial and Capital Risks
- Cumulative operating losses since inception
- Substantial ongoing cash consumption for clinical trials, commercialization, and R&D
- Uncertainty about generating sufficient revenue to achieve profitability
- Potential inability to raise additional capital when needed
- Existing indebtedness obligations, including convertible senior notes

## Pre-written sections (judge input)

### Financial Health

Omeros Corporation trades at $18.75 with a market capitalization of $1.36 billion and a reasonable P/E ratio of 15.37x, suggesting moderate valuation relative to earnings. The company reported revenue of $38.4 million against net income of $116.5 million, yielding an exceptional 324.88% profit margin—an unusual metric indicating significant non-operating gains or one-time items that warrant deeper investigation. The stock has recovered substantially from its 52-week low of $4.06 to $18.75, though it remains below the 52-week high of $21.24, reflecting volatility typical of biotechnology firms. The absence of dividend yield is consistent with a growth-stage biotech company reinvesting capital into operations. While the profitability metrics appear strong on the surface, investors should scrutinize the composition of net income given the disproportionate margin relative to revenue, and carefully review SEC filings that highlight significant operational and commercial risks.

### Recent Developments

No significant news announcements were identified for Omeros Corporation during the review period. However, the company's most recent SEC filings (10-K filed March 31, 2026 and 10-Q filed August 12, 2026) emphasize substantial operational and commercial risks, particularly regarding the company's ability to achieve sustained profitability. Investors should note the company's unusual financial profile, with a reported profit margin of 324.88% and net income of $116.5M on revenue of $38.4M, which warrants careful scrutiny of accounting practices and sustainability. The absence of recent positive catalysts, combined with the company's risk disclosures, suggests investors should monitor upcoming clinical or commercial developments closely before making investment decisions.

### SEC Filing Highlights

Omeros holds $171.8 million in cash and short-term investments as of December 31, 2025, with 2025 operating cash burn of $116.1 million, while carrying $70.8 million in convertible senior notes due 2029. The company's commercial viability hinges on YARTEMLA, its only FDA-approved product (approved December 2025), though the company has limited commercialization experience and faces significant reimbursement uncertainty. Near-term profitability depends entirely on YARTEMLA's market adoption, while the company continues substantial cash burn for clinical trials, R&D, and debt service. A strategic partnership with Novo Nordisk for zaltenibart provides potential milestone and royalty upside, though success remains contingent on development and commercialization progress.

### Risk Factors

• **YARTEMLEA Commercialization Risk** – The company's profitability depends heavily on successful market adoption of its sole commercialized product (FDA-approved December 2025). Omeros has limited commercial experience and faces uncertainty around physician/patient acceptance, pricing power, and reimbursement coverage, which could significantly delay or limit revenue generation.

• **Reimbursement and Pricing Pressure** – Payers are increasingly demanding discounts from list prices, and government price controls (particularly in the EU) may constrain margins. Delays in obtaining reimbursement coverage or unfavorable reimbursement rates could prevent the company from achieving profitability or covering operating costs.

• **Cash Burn and Financing Risk** – Omeros has cumulative operating losses since inception and substantial ongoing cash consumption for R&D and commercialization. The company may be unable to raise additional capital when needed or may face unfavorable financing terms, threatening its ability to fund operations and reach profitability.

## Audited (Exec Summary + Outlook)

### Executive Summary
Omeros Corporation is a commercial-stage biopharmaceutical company whose investment case now rests almost entirely on YARTEMLA, its sole FDA-approved product (approved December 2025), supported by a strategic partnership with Novo Nordisk for pipeline asset zaltenibart and $171.8 million in cash and short-term investments as of December 31, 2025. The stock is notable today because it has rebounded sharply from its 52-week low of $4.06 to $18.75, yet the headline financial profile—$116.5 million in net income on only $38.4 million in revenue—raises immediate questions about earnings quality and sustainability that investors must resolve before assigning confidence to the current valuation. The single most important near-term variable is the pace and breadth of YARTEMLA's commercial adoption, including the speed at which the company secures favorable reimbursement coverage, as this will determine whether Omeros can convert its unusual reported profitability into durable, operationally generated cash flow.

### Outlook
The directional outlook for Omeros is **cautious**, with the potential to become more constructive if early YARTEMLA commercialization signals prove favorable. The primary tailwind is the company's first-mover position with a newly approved product and the optionality embedded in the Novo Nordisk partnership for zaltenibart, which could provide non-dilutive milestone and royalty income without requiring Omeros to bear the full cost of development. The headwinds, however, are substantial: operating cash burn of $116.1 million in 2025 against a cash position of $171.8 million creates a narrow runway, the convertible senior notes due 2029 add a fixed financing obligation, and the company's limited commercialization experience introduces meaningful execution risk at the most critical juncture in its history. Investors should watch the trajectory of YARTEMLA physician adoption and prescription volume, the speed and breadth of payer reimbursement decisions, the composition and sustainability of reported net income relative to operating cash flow, and any updates on zaltenibart's development milestones under the Novo Nordisk partnership. The thesis would strengthen materially on evidence of accelerating YARTEMLA uptake, favorable broad reimbursement coverage, and a narrowing gap between reported net income and operating cash generation; it would weaken on signs of slow adoption, payer pushback, or the need to raise dilutive capital to fund ongoing operations.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "YARTEMLA, its sole FDA-approved product (approved December 2025)"
LABEL: UNSUPPORTED
REASON: The source data and pre-written sections consistently spell the product name as "YARTEMLEA" (not "YARTEMLA"), making this a factual mismatch on the named entity; the December 2025 FDA approval date is correct per the SEC highlights, but the misspelled product name renders the claim unsupported.

---

CLAIM: "$171.8 million in cash and short-term investments as of December 31, 2025"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "As of December 31, 2025, the company held $171.8 million in cash, cash equivalents, and short-term investments."

---

CLAIM: "52-week low of $4.06"
LABEL: SUPPORTED
REASON: The stock data field "week_52_low" is exactly $4.06.

---

CLAIM: "to $18.75"
LABEL: SUPPORTED
REASON: The stock data field "current_price" is exactly $18.75.

---

CLAIM: "$116.5 million in net income"
LABEL: SUPPORTED
REASON: The stock data field "net_income" is $116,533,000, which rounds to $116.5 million.

---

CLAIM: "only $38.4 million in revenue"
LABEL: SUPPORTED
REASON: The stock data field "revenue" is $38,422,000, which rounds to $38.4 million.

---

**OUTLOOK**

---

CLAIM: "operating cash burn of $116.1 million in 2025"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "Cash used in operations for 2025 was $116.1 million."

---

CLAIM: "a cash position of $171.8 million"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "the company held $171.8 million in cash, cash equivalents, and short-term investments" as of December 31, 2025.

---

CLAIM: "the convertible senior notes due 2029"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "$70.8 million outstanding in convertible senior notes due June 15, 2029."

---

CLAIM: "narrow runway" (implied by $116.1M burn vs. $171.8M cash)
LABEL: INFERENCE
REASON: Dividing $171.8M cash by $116.1M annual burn yields approximately 1.48 years of runway, which is directly derivable from the two figures present in the source data and supports characterizing the runway as narrow.

---

CLAIM: "non-dilutive milestone and royalty income" (from Novo Nordisk partnership for zaltenibart)
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors both confirm the Novo Nordisk agreement involving zaltenibart with "potential milestone and royalty payments contingent on successful development and commercialization"; characterizing these as non-dilutive is a standard, directly derivable inference from the nature of milestone/royalty payments (they are not equity issuances).

---

CLAIM: "YARTEMLA physician adoption and prescription volume" (as a watch item)
LABEL: UNSUPPORTED
REASON: The product name is misspelled as "YARTEMLA" rather than "YARTEMLEA" as consistently used in all source data and pre-written sections; the misspelled entity name is absent from the context.

---

CLAIM: "YARTEMLA uptake" (in the thesis-strengthening sentence)
LABEL: UNSUPPORTED
REASON: Same as above — the product is named "YARTEMLEA" in all source materials; "YARTEMLA" does not appear in the context and constitutes a factual mismatch on the named entity.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | YARTEMLA approved December 2025 (misspelled name) | UNSUPPORTED |
| 2 | $171.8M cash/short-term investments as of Dec 31, 2025 | SUPPORTED |
| 3 | 52-week low of $4.06 | SUPPORTED |
| 4 | Current price $18.75 | SUPPORTED |
| 5 | $116.5M net income | SUPPORTED |
| 6 | $38.4M revenue | SUPPORTED |
| 7 | $116.1M operating cash burn in 2025 | SUPPORTED |
| 8 | Cash position of $171.8M | SUPPORTED |
| 9 | Convertible senior notes due 2029 | SUPPORTED |
| 10 | "Narrow runway" (implied ratio) | INFERENCE |
| 11 | Non-dilutive milestone and royalty income (Novo Nordisk/zaltenibart) | SUPPORTED |
| 12 | "YARTEMLA physician adoption" (misspelled watch item) | UNSUPPORTED |
| 13 | "YARTEMLA uptake" (misspelled thesis item) | UNSUPPORTED |
