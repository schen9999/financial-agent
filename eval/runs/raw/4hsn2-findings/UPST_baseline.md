# UPST — baseline

## Metadata

ticker: UPST
arm: baseline
judge_prompt_version: v2
context_sha256: 34849f4dd2effb536e3df76cafc66f639385fdf61e1a49d31c7db93286ea4581
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 202, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.585, "latency_s_total": 2.585, "parse_failure": 0, "prompt_tokens": 3199, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 374, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.14, "latency_s_total": 4.14, "parse_failure": 0, "prompt_tokens": 2482, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 157, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.073, "latency_s_total": 2.073, "parse_failure": 0, "prompt_tokens": 677, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 190, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.226, "latency_s_total": 2.226, "parse_failure": 0, "prompt_tokens": 670, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 201, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.337, "latency_s_total": 2.337, "parse_failure": 0, "prompt_tokens": 448, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 105, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.23, "latency_s_total": 1.23, "parse_failure": 0, "prompt_tokens": 284, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1095, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 16.306, "latency_s_total": 16.306, "parse_failure": 0, "prompt_tokens": 1712, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "UPST",
  "company_name": "Upstart Holdings, Inc.",
  "current_price": 24.35,
  "currency": "USD",
  "market_cap": 2369572864.0,
  "pe_ratio": 45.943398,
  "forward_pe": 7.005259,
  "week_52_high": 55.22,
  "week_52_low": 22.555,
  "financial_currency": "USD",
  "revenue": 1285890048.0,
  "net_income": 60334000.0,
  "profit_margin_pct": 4.69,
  "dividend_yield": 0.0,
  "sector": "Financial Services",
  "industry": "Credit Services"
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
    "filing_date": "2026-02-10",
    "summary": "ITEM 1A. RISK FACTORS RISK FACTORS Investing in our common stock involves a high degree of risk. The risks and uncertainties described below should be carefully considered, together with all of the other information in this Annual Report on Form 10-K, including the section titled \u201cManagement\u2019s Discussion and Analysis of Financial Condition and Results of Operations\u201d and our consolidated financial statements and related notes, before making a decision to invest in our common stock. Our business, financial condition, results of operations, or prospects could also be harmed by risks and uncertainties not currently known to us or that we currently do not believe are material. If any of the risks actually occur, our business, financial condition, results of operations, and prospects could be ad"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-04",
    "summary": "ITEM 1A. RISK FACTORS RISK FACTORS Investing in our common stock involves a high degree of risk. The risks and uncertainties described below should be carefully considered, together with all of the other information in this Quarterly Report on Form 10-Q, including the section titled \u201cManagement\u2019s Discussion and Analysis of Financial Condition and Results of Operations\u201d and our condensed consolidated financial statements and related notes, before making a decision to invest in our common stock. Our business, financial condition, results of operations, or prospects could also be harmed by risks and uncertainties not currently known to us or that we currently do not believe are material. If any of the risks actually occur, our business, financial condition, results of operations, and prospect"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] I cannot provide a summary of the latest 10-K and 10-Q based on the context provided. The information available consists only of risk factor disclosures from a 10-K filing for Upstart (ticker: UPST), which represents just one section of the annual report.

To provide a comprehensive summary of the latest 10-K and 10-Q filings, I would need access to additional sections such as:

- Management's Discussion and Analysis (MD&A)
- Financial statements and results of operations
- Business overview and strategy
- Liquidity and capital resources
- Critical accounting policies
- Forward-looking statements

The risk factors section alone does not capture the full picture of the company's financial performance, operational results, or overall business status. If you'd like, I can summarize the specific risks disclosed in the provided context, or you could provide additional sections from the filings for a more complete analysis.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors affecting its business:

## Economic and Market Risks
- Adverse economic conditions, uncertainty, and volatility that impact borrower demand, approval rates, loan origination volume, and capital availability
- Macroeconomic factors beyond management's control that affect the supply of capital and borrower ability to repay loans
- Concentration of operations in U.S. consumer credit, making the business vulnerable to domestic economic downturns

## Capital and Funding Risks
- Inability to maintain diverse and resilient loan funding from institutional investors
- Dependence on committed capital and co-investment arrangements that expose the company to credit risk compensation obligations
- Risks associated with asset-backed securitizations, warehouse credit facilities, and whole loan sale arrangements
- Potential need to repurchase loans or make payments if representations and warranties prove inaccurate
- Counterparty risk from derivative instruments and custodial arrangements

## Operational and Technology Risks
- Failure to improve or maintain effective artificial intelligence models for credit assessment
- Significant disruption or failure in technology systems, including the AI lending platform
- Inability to approve sufficient borrowers for loans

## Business Model Risks
- Dependence on a limited number of lending partners for a significant portion of loan originations and revenue
- Reliance on strategic relationships with loan aggregators to attract applicants
- Historical net losses and inability to sustain profitability
- Significant fluctuations in quarterly results

## Regulatory and Reputational Risks
- Compliance with a wide range of evolving laws and regulations
- Security breaches and data protection failures
- Reputation and brand protection challenges

## Pre-written sections (judge input)

### Financial Health

Upstart Holdings trades at $24.35 with a market capitalization of $2.37 billion, currently trading near its 52-week low of $22.56. The stock's elevated trailing P/E ratio of 45.9x contrasts sharply with a forward P/E of 7.0x, suggesting significant expected earnings growth ahead. Revenue of $1.29 billion supports a modest 4.69% net profit margin, indicating the company is profitable but operating with thin margins typical of fintech lending platforms. The substantial gap between trailing and forward valuations reflects market expectations for substantial margin expansion, though investors should note the company carries meaningful risk factors as disclosed in recent SEC filings.

### Recent Developments

Recent SEC filings (10-K filed February 2026 and 10-Q filed August 2026) highlight significant risk factors for Upstart Holdings, emphasizing the high-risk nature of the business and potential uncertainties affecting financial performance. The company's stock has declined substantially from its 52-week high of $55.22 to $24.35, reflecting investor concerns about profitability and growth prospects in the competitive fintech lending space. With a forward P/E ratio of 7.0x versus a current P/E of 45.9x, the market is pricing in meaningful earnings growth expectations, though the company's modest 4.69% profit margin suggests execution challenges. Investors should closely monitor upcoming quarterly results and management commentary regarding loan origination volumes and credit quality, as these will be critical to validating the forward valuation.

### SEC Filing Highlights

Unable to provide SEC filing highlights at this time. The available data contains only risk factor disclosures from Upstart's 10-K filing, which is insufficient for a comprehensive summary of financial performance, operational results, and business developments. A complete analysis would require access to additional sections including Management's Discussion and Analysis (MD&A), financial statements, and results of operations. Please provide complete 10-K or 10-Q filing documents for accurate filing highlights.

### Risk Factors

- **Economic Sensitivity and Capital Dependence**: Upstart's business is highly vulnerable to macroeconomic downturns and credit market disruptions. Adverse economic conditions reduce borrower demand and approval rates, while the company depends on institutional investors and co-investment arrangements for loan funding, exposing it to capital availability risks beyond management's control.

- **AI Model Performance and Technology Risk**: The company's core competitive advantage relies on artificial intelligence models for credit assessment. Failure to maintain or improve these models, or significant disruption to the technology platform, could severely impair loan origination capabilities and underwriting accuracy.

- **Concentration Risk and Limited Lending Partners**: Upstart generates a significant portion of revenue from a limited number of lending partners and loan aggregators. This concentration creates dependency on key relationships and exposes the company to revenue volatility if these partnerships are disrupted or renegotiated unfavorably.

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings is an AI-driven fintech lending platform that partners with banks and credit unions to originate consumer loans, generating $1.29 billion in revenue while operating with the thin margins characteristic of the sector. The stock is notable today because it trades near its 52-week low of $24.35 — down sharply from a 52-week high of $55.22 — while simultaneously carrying a forward P/E of 7.0x that implies the market expects a dramatic earnings recovery, creating a high-stakes divergence between current results and future expectations. The single most important near-term variable is whether loan origination volumes and credit quality can inflect positively enough to validate that forward valuation, a question that upcoming quarterly results and management commentary will begin to answer.

### Outlook
The directional outlook for Upstart is **cautiously constructive but contingent**, with the investment thesis resting almost entirely on execution rather than current fundamentals. The primary tailwind is the dramatic compression in the forward P/E relative to the trailing multiple, which suggests the market has already priced in meaningful improvement — leaving room for positive surprise if origination volumes recover and profit margins expand. Key variables to monitor include the trajectory of loan origination volumes, the credit quality of the underlying loan book, the stability and breadth of lending partner relationships, and the broader macroeconomic environment, particularly credit market conditions and consumer credit health. On the headwind side, the company's dependence on institutional capital and a concentrated set of lending partners means that any deterioration in those relationships or a tightening of credit markets could quickly erode the earnings recovery the forward valuation assumes. The view would become more constructive if upcoming quarterly results demonstrate sustained origination growth, improving margins, and expanding lending partnerships; it would turn cautious if credit quality deteriorates, key partners reduce activity, or macroeconomic conditions weaken demand for consumer credit.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

## EXECUTIVE SUMMARY

---

CLAIM: "generating $1.29 billion in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $1,285,890,048, which rounds to $1.29 billion; the pre-written Financial Health section also states "$1.29 billion."

---

CLAIM: "trades near its 52-week low of $24.35"
LABEL: UNSUPPORTED
REASON: The 52-week low is $22.555 per the source data; $24.35 is the current price, not the 52-week low — the claim conflates the two figures.

---

CLAIM: "down sharply from a 52-week high of $55.22"
LABEL: SUPPORTED
REASON: Source data explicitly states week_52_high = 55.22.

---

CLAIM: "forward P/E of 7.0x"
LABEL: SUPPORTED
REASON: Source data shows forward_pe = 7.005259, which rounds to 7.0x.

---

## OUTLOOK

---

CLAIM: "dramatic compression in the forward P/E relative to the trailing multiple"
LABEL: SUPPORTED
REASON: Source data shows trailing P/E of 45.943398 versus forward P/E of 7.005259 — a compression of approximately 38.9 points, which is arithmetically dramatic and consistent with the pre-written sections.

---

*(No additional specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section beyond the directional/qualitative language already covered above.)*

---

## SUMMARY TABLE

| Claim | Label |
|---|---|
| "$1.29 billion in revenue" | SUPPORTED |
| "trades near its 52-week low of $24.35" | UNSUPPORTED |
| "52-week high of $55.22" | SUPPORTED |
| "forward P/E of 7.0x" | SUPPORTED |
| "dramatic compression in the forward P/E relative to the trailing multiple" | SUPPORTED |

---

**Key Finding:** The most material error is the misidentification of the current price ($24.35) as the 52-week low. The actual 52-week low is $22.555. While the stock does trade *near* its 52-week low (it is approximately 8% above it), the brief incorrectly states the 52-week low *is* $24.35, which is factually wrong per the source data.
