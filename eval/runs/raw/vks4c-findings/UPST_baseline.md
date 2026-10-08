# UPST — baseline

## Metadata

ticker: UPST
arm: baseline
judge_prompt_version: v2
context_sha256: 0a8f1f54831f0a8ad7121c61343621d9b5d56f884e60f2696f05aa066dd3fb52
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 279, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.352, "latency_s_total": 3.352, "parse_failure": 0, "prompt_tokens": 3199, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 385, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.687, "latency_s_total": 4.687, "parse_failure": 0, "prompt_tokens": 2482, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 158, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.938, "latency_s_total": 1.938, "parse_failure": 0, "prompt_tokens": 676, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 179, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.402, "latency_s_total": 2.402, "parse_failure": 0, "prompt_tokens": 669, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 206, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.441, "latency_s_total": 2.441, "parse_failure": 0, "prompt_tokens": 459, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 126, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.631, "latency_s_total": 1.631, "parse_failure": 0, "prompt_tokens": 361, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1159, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.804, "latency_s_total": 17.804, "parse_failure": 0, "prompt_tokens": 1744, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "UPST",
  "company_name": "Upstart Holdings, Inc.",
  "current_price": 24.02,
  "currency": "USD",
  "market_cap": 2337459456.0,
  "pe_ratio": 48.04,
  "forward_pe": 6.910321,
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
[From Pinecone cache] I cannot provide a summary of the latest 10-K and 10-Q based on the context provided. The information available consists only of risk factor disclosures from a 10-K filing for Upstart (UPST), which represents just one section of the annual report.

To provide a comprehensive summary of the latest 10-K and 10-Q filings, I would need access to additional sections such as:

- Management's Discussion and Analysis (MD&A)
- Financial statements and results of operations
- Business overview and strategy
- Liquidity and capital resources
- Critical accounting policies
- Forward-looking statements

What I can tell you based on the risk factors disclosed is that Upstart faces several material challenges, including:

- Dependence on economic conditions and capital availability from institutional investors
- Reliance on AI model effectiveness for loan approval and credit risk assessment
- Concentration risk with a limited number of lending partners
- Exposure to loan performance risks through securitizations and warehouse facilities
- Regulatory compliance requirements across multiple areas
- Technology system reliability and cybersecurity risks

For a complete and accurate summary of the company's financial performance, operational results, and overall business status, you would need to review the full 10-K and 10-Q documents.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors affecting its business:

## Economic and Market Risks
- Adverse economic conditions, uncertainty, and volatility that impact borrower demand, approval rates, loan origination volume, and capital availability
- Macroeconomic factors affecting borrower ability and willingness to repay loans, particularly those with poor or limited credit history who are disproportionately affected by inflation, interest rates, and unemployment

## Capital and Funding Risks
- Inability to maintain diverse and resilient loan funding from institutional investors
- Dependence on committed capital and co-investment arrangements that expose the company to credit risk compensation obligations
- Risks associated with asset-backed securitizations, warehouse credit facilities, and whole loan sale arrangements, including potential repurchase obligations if loan representations and warranties prove inaccurate
- Counterparty risk from derivative instruments and custodial arrangements

## Operational and Technology Risks
- Inability to improve or maintain effective artificial intelligence models for credit assessment
- Significant disruption or failure in technology systems, including the AI lending platform
- Inability to approve a significant number of borrowers for loans

## Business Concentration Risks
- Dependence on a limited number of lending partners for a significant portion of loan originations and revenue
- Reliance on strategic relationships with loan aggregators to attract applicants
- Historical dependence on a single loan product

## Regulatory and Reputational Risks
- Compliance with a wide range of evolving laws and regulations
- Reputation and brand protection
- Risks related to loan servicing and collections obligations

## Financial Performance Risks
- History of net losses and uncertainty about achieving sustained profitability
- Significant quarterly result fluctuations

## Pre-written sections (judge input)

### Financial Health

Upstart Holdings trades at $24.02 with a market capitalization of $2.34 billion, currently trading near its 52-week low of $22.56. The company generated $1.29 billion in revenue with a modest 4.69% profit margin and net income of $60.3 million, reflecting tight operational efficiency in the credit services sector. The elevated trailing P/E ratio of 48.04 contrasts sharply with a forward P/E of 6.91, suggesting market expectations for significant earnings growth ahead. With no dividend yield and recent SEC filings highlighting substantial business risks, investors should view this as a growth-oriented play with elevated volatility and execution risk.

### Recent Developments

Limited recent news is available for analysis at this time. However, Upstart's most recent SEC filings (10-Q filed August 4, 2026 and 10-K filed February 10, 2026) emphasize significant risk factors affecting the business, suggesting investors should carefully review operational and market uncertainties. The company's valuation metrics show a stark disconnect—trading at a 48x trailing P/E while maintaining only a 4.7% profit margin and a forward P/E of 6.9x—indicating market expectations for substantial future growth or potential overvaluation risk. With no dividend yield and the stock trading near its 52-week low of $22.56, investors should monitor upcoming earnings reports and regulatory developments in the credit services sector for clarity on near-term performance.

### SEC Filing Highlights

Based on available risk disclosures, Upstart faces material dependencies on economic conditions and institutional investor capital availability, which directly impact its lending platform operations. The company's business model relies heavily on AI model effectiveness for loan underwriting and credit risk assessment, with concentration risk evident in its reliance on a limited number of lending partners. Upstart is exposed to loan performance risks through securitizations and warehouse facilities, while navigating complex regulatory compliance requirements across multiple jurisdictions. Technology system reliability and cybersecurity represent critical operational risks given the company's digital-first platform architecture.

### Risk Factors

• **Economic Sensitivity and Credit Risk** – Adverse macroeconomic conditions directly impact borrower demand, approval rates, and loan origination volume. The company's target borrowers (those with poor or limited credit history) are disproportionately vulnerable to inflation, interest rates, and unemployment, creating cyclical revenue volatility and potential credit losses.

• **Funding and Capital Dependence** – Upstart relies on institutional investors and committed capital arrangements to fund loans. Inability to maintain diverse funding sources, combined with potential repurchase obligations from loan securitizations and warehouse facilities, exposes the company to significant counterparty and liquidity risks.

• **AI Model Performance and Technology Risk** – The company's core competitive advantage depends on maintaining effective artificial intelligence models for credit assessment. Significant disruption or failure in the technology platform, or inability to improve model accuracy, could impair loan approvals and undermine the business model.

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings is an AI-driven consumer lending platform operating in the credit services sector, generating $1.29 billion in revenue by connecting borrowers — particularly those with poor or limited credit history — to institutional lending partners through proprietary AI underwriting models. The stock is notable now because it trades near its 52-week low of $22.56 at a price of $24.02, while simultaneously presenting a dramatic valuation divergence between a trailing P/E of 48.04 and a forward P/E of 6.91, signaling that the market is pricing in a substantial earnings inflection that has yet to materialize. The single most important near-term variable is whether Upstart's AI models can sustain and improve loan performance in a challenging macroeconomic environment, as that outcome will determine both institutional funding availability and the credibility of the earnings growth the forward multiple implies.

### Outlook
The directional outlook for Upstart is **cautiously neutral, leaning constructive only on confirmed execution**. The primary tailwind is the dramatic compression implied by the gap between the trailing and forward P/E ratios, which suggests the market already anticipates a meaningful earnings recovery — a thesis that would be strengthened by stabilizing or declining interest rates, improving consumer credit performance, and demonstrated expansion of the institutional lending partner base. Headwinds are substantial: the company's borrower base is disproportionately exposed to macroeconomic stress, funding availability remains contingent on institutional appetite that can evaporate quickly, and the thin profit margin leaves little buffer against operational or credit surprises. Investors should watch the trajectory of AI model performance and loan approval rates as the clearest leading indicator of platform health, alongside any changes in the concentration of lending partners and the terms of securitization and warehouse facilities. Regulatory developments in consumer credit and AI-based underwriting represent a slow-moving but potentially decisive variable. The cautious lean would shift more constructively if upcoming earnings reports demonstrate durable margin expansion and broadening capital partnerships; it would deteriorate if credit losses rise, funding sources narrow, or macroeconomic conditions weaken further.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

## EXECUTIVE SUMMARY

---

CLAIM: "$1.29 billion in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $1,285,890,048, which rounds to $1.29 billion; the pre-written Financial Health section also states "$1.29 billion in revenue."

---

CLAIM: "52-week low of $22.56"
LABEL: SUPPORTED
REASON: Source data lists `week_52_low: 22.555`, which rounds to $22.56; the pre-written sections also confirm this figure.

---

CLAIM: "a price of $24.02"
LABEL: SUPPORTED
REASON: Source data explicitly states `current_price: 24.02`.

---

CLAIM: "trailing P/E of 48.04"
LABEL: SUPPORTED
REASON: Source data explicitly states `pe_ratio: 48.04`.

---

CLAIM: "forward P/E of 6.91"
LABEL: SUPPORTED
REASON: Source data states `forward_pe: 6.910321`, which rounds to 6.91.

---

## OUTLOOK

---

CLAIM: "dramatic compression implied by the gap between the trailing and forward P/E ratios"
LABEL: SUPPORTED
REASON: The trailing P/E of 48.04 and forward P/E of 6.91 are both present in the source data; the directional characterization of a large gap between them is arithmetically verifiable (48.04 vs. 6.91, a difference of ~41 points), making this a supported positional/comparative claim.

---

CLAIM: "thin profit margin"
LABEL: SUPPORTED
REASON: Source data states `profit_margin_pct: 4.69`, and the pre-written sections describe it as a "modest 4.69% profit margin," which is objectively thin; the directional characterization is grounded in the explicit figure.

---

*(No other specific quantitative figures, price targets, thresholds, ratios, named product milestones, or forward-looking numbers appear in the Outlook section. All remaining language is qualitative or directional without specific numeric claims.)*

---

## SUMMARY TABLE

| # | Claim | Label |
|---|-------|-------|
| 1 | $1.29 billion in revenue | SUPPORTED |
| 2 | 52-week low of $22.56 | SUPPORTED |
| 3 | price of $24.02 | SUPPORTED |
| 4 | trailing P/E of 48.04 | SUPPORTED |
| 5 | forward P/E of 6.91 | SUPPORTED |
| 6 | dramatic gap between trailing and forward P/E | SUPPORTED |
| 7 | thin profit margin | SUPPORTED |

**No unsupported or inference-labeled claims were identified.** All quantitative figures in the Executive Summary and Outlook are directly traceable to the raw source data, and all derived comparisons check out arithmetically.
