# SANA — baseline

## Metadata

ticker: SANA
arm: baseline
judge_prompt_version: v2
context_sha256: 52f8ee7ec6eb82c817f12b5a8c95ac82b1d37a56360f619663d3a4f45e3d6fbd
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 319, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.141, "latency_s_total": 4.141, "parse_failure": 0, "prompt_tokens": 2171, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 327, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.767, "latency_s_total": 3.767, "parse_failure": 0, "prompt_tokens": 2159, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 168, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.098, "latency_s_total": 2.098, "parse_failure": 0, "prompt_tokens": 623, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 173, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.354, "latency_s_total": 2.354, "parse_failure": 0, "prompt_tokens": 616, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 187, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.201, "latency_s_total": 2.201, "parse_failure": 0, "prompt_tokens": 403, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 175, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.814, "latency_s_total": 1.814, "parse_failure": 0, "prompt_tokens": 403, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1208, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.761, "latency_s_total": 17.761, "parse_failure": 0, "prompt_tokens": 1816, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "SANA",
  "company_name": "Sana Biotechnology, Inc.",
  "current_price": 2.72,
  "currency": "USD",
  "market_cap": 814260928.0,
  "forward_pe": -4.89993,
  "week_52_high": 6.55,
  "week_52_low": 2.61,
  "financial_currency": "USD",
  "net_income": -211822000.0,
  "profit_margin_pct": 0.0,
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
    "filing_date": "2026-03-03",
    "summary": "Item 1A. Ris k Factors. Investing in shares of our common stock involves a high degree of risk. You should carefully consider the following risks and uncertainties, together with all of the other information contained in this Annual Report, including our financial statements and related notes included elsewhere in this Annual Report, before making an investment decision. The risks described below are not the only ones we face. Many of the following risks and uncertainties are, and will continue to be, exacerbated by any worsening of the global geo-political, business, and economic environment. The occurrence of any of the following risks, or of additional risks and uncertainties not presently known to us or that we currently believe to be immaterial, could materially and adversely affect o"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-10",
    "summary": "Item 1A. Ri sk Factors Investing in shares of our common stock involves a high degree of risk. You should carefully consider the following risks and uncertainties, together with all of the other information contained in this Quarterly Report, including our financial statements and related notes included elsewhere in this Quarterly Report, before making an investment decision. The risks described below are not the only ones we face. Many of the following risks and uncertainties are, and will continue to be, exacerbated by any worsening of the global geo-political, business, and economic environment. The occurrence of any of the following risks, or of additional risks and uncertainties not presently known to us or that we currently believe to be immaterial, could materially and adversely aff"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] # Key Takeaways from SANA's SEC Filings

Based on the available SEC filing information, here are the primary takeaways:

## Technology and Development Risks

The company's business is centered on novel ex vivo and in vivo cell engineering platforms that remain unproven. There are no FDA-approved therapeutics currently based on pluripotent stem cells (PSCs) or utilizing the company's fusogen technology. The scientific evidence supporting these platforms is preliminary and ongoing, creating significant uncertainty around development timelines and costs.

## Clinical Development Challenges

Most current data comes from animal models and preclinical testing rather than human trials. The company faces unpredictability in translating results across different cell types and microenvironments. Additionally, novel gene editing reagents may have unanticipated effects, and there is limited understanding of how product candidates will perform across different disease indications.

## Going Concern and Funding Concerns

A critical issue is substantial doubt regarding the company's ability to continue as a going concern. The company will require additional funding to finance operations, and any inability to raise capital on acceptable terms could force delays or elimination of product development programs.

## Operational and Personnel Risks

Success depends on retaining key personnel and recruiting qualified staff. The company may also face challenges managing growth as it expands development and regulatory capabilities.

## Strategic Uncertainty

There is uncertainty around realizing benefits from acquired or in-licensed technologies and the success of strategic relationships.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed for SANA

The company discloses several primary risk factors:

## Technology and Development Risks
- The ex vivo and in vivo cell engineering platforms are based on novel, unproven technologies that may not result in approvable or marketable products
- Preclinical and clinical testing is inherently unpredictable and may lead to unexpected results
- Most current data are limited to animal models and preclinical testing, which may not accurately predict safety and efficacy in humans
- There is no FDA-approved therapeutics currently based on pluripotent stem cells (PSCs) or utilizing the company's fusogen technology

## Product Development Risks
- Inability to successfully identify, develop, and commercialize product candidates could materially adversely affect the business
- Significant delays in development could harm financial condition and results of operations
- Unexpected differences in product candidate performance across different indications may require changes to manufacturing processes or clinical development plans

## Financial and Operational Risks
- Substantial doubt exists regarding the company's ability to continue as a going concern
- Additional funding will be required to finance operations
- Inability to raise capital when needed could force delays or elimination of product development programs

## Personnel and Growth Risks
- Dependence on retaining key personnel and recruiting qualified staff
- Potential difficulties in managing growth and expansion of operations, development, and regulatory capabilities

These risks are compounded by uncertainties in the global geo-political, business, and economic environment.

## Pre-written sections (judge input)

### Financial Health

Sana Biotechnology trades at $2.72 per share with a market capitalization of approximately $814 million, down significantly from its 52-week high of $6.55. The company is unprofitable with a negative net income of $211.8 million and a forward P/E ratio of -4.90, reflecting its pre-revenue or early-stage commercialization status typical of clinical-stage biotechnology firms. With zero profit margin and no dividend yield, SANA is a high-risk, cash-burn investment dependent on successful clinical trial outcomes and future product commercialization. The company's financial position underscores the inherent risks of biotech investing, where valuation is driven by pipeline potential rather than current earnings power.

### Recent Developments

Sana Biotechnology has not released significant recent news announcements, though the company filed its latest 10-Q on August 10, 2026, reiterating substantial risk factors inherent to its biotech operations. The stock remains under pressure, trading at $2.72—near its 52-week low of $2.61—with a negative forward P/E ratio reflecting ongoing losses (net income of -$211.8M). Investors should note that the company continues to emphasize geopolitical and economic headwinds as material risks to its business, suggesting operational challenges persist. The lack of positive catalysts and sustained unprofitability indicate SANA remains a high-risk, pre-revenue or early-stage clinical play requiring careful monitoring of pipeline progress.

### SEC Filing Highlights

Sana Biotechnology's business centers on novel ex vivo and in vivo cell engineering platforms utilizing pluripotent stem cells and fusogen technology, with no FDA-approved therapeutics currently on the market, creating significant uncertainty around development timelines and costs. The company faces substantial doubt regarding its ability to continue as a going concern and will require additional capital to finance operations, with any inability to secure funding on acceptable terms potentially forcing delays or elimination of product programs. Most clinical data derives from animal models and preclinical testing rather than human trials, and the company faces unpredictability in translating results across different cell types and disease indications. Success depends heavily on retaining key personnel and managing growth as development and regulatory capabilities expand, while realizing benefits from acquired or in-licensed technologies remains uncertain.

### Risk Factors

• **Unproven Technology and Clinical Uncertainty** – SANA's cell engineering platforms rely on novel technologies with no FDA-approved therapeutics currently based on pluripotent stem cells or the company's fusogen technology. Most data are limited to preclinical and animal models, creating significant uncertainty around human safety and efficacy.

• **Going Concern and Funding Risk** – The company has disclosed substantial doubt regarding its ability to continue as a going concern and will require additional capital to finance operations. Inability to secure funding when needed could force delays or elimination of product development programs.

• **Development and Commercialization Execution Risk** – Success depends on identifying, developing, and commercializing multiple product candidates across different indications. Unexpected performance differences, manufacturing challenges, or clinical setbacks could materially delay timelines and harm financial results.

## Audited (Exec Summary + Outlook)

### Executive Summary
Sana Biotechnology is a clinical-stage biotechnology company developing novel ex vivo and in vivo cell engineering platforms utilizing pluripotent stem cells and fusogen technology, with no FDA-approved therapeutics currently on the market and a market capitalization of approximately $814 million despite a net loss of $211.8 million. Trading near its 52-week low of $2.61 at $2.72 per share — well off its 52-week high of $6.55 — the stock is notable for the severity of its drawdown and the company's disclosed going concern doubt, which together signal that the investment thesis is at a critical inflection point. The single most important near-term variable is the company's ability to secure additional capital on acceptable terms, as failure to do so could force the delay or outright elimination of its product development programs.

### Outlook
The directional lean on SANA is **cautious**, and that view would need to shift materially on multiple fronts before warranting greater conviction. The most consequential variable to monitor is the company's capital runway and its ability to raise additional funding without severely diluting existing shareholders — any financing announcement should be evaluated for its terms and the operational flexibility it affords. Beyond funding, investors should watch for the emergence of human clinical data from the company's ex vivo and in vivo platforms, as a successful translation from preclinical and animal models to human safety and efficacy results would represent the most meaningful positive catalyst available to the stock. Conversely, clinical setbacks, manufacturing failures, or the loss of key personnel would further weaken an already fragile thesis. Geopolitical and macroeconomic headwinds flagged by management add an additional layer of uncertainty that could complicate both fundraising efforts and operational execution. The thesis could become more constructive if the company secures non-dilutive or favorably structured capital, advances candidates into human trials with encouraging early data, and demonstrates progress in building out its regulatory and development infrastructure — but absent those developments, the combination of going concern doubt, sustained cash burn, and an absence of near-term positive catalysts keeps the risk-reward profile firmly skewed to the downside.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

## EXECUTIVE SUMMARY

---

CLAIM: "market capitalization of approximately $814 million"
LABEL: SUPPORTED
REASON: The raw source data lists `market_cap: 814260928.0`, which rounds to approximately $814 million, and the pre-written Financial Health section states "market capitalization of approximately $814 million."

---

CLAIM: "net loss of $211.8 million"
LABEL: SUPPORTED
REASON: The raw source data lists `net_income: -211822000.0`, which equals approximately -$211.8 million, consistent with the pre-written sections.

---

CLAIM: "Trading near its 52-week low of $2.61 at $2.72 per share"
LABEL: SUPPORTED
REASON: The raw source data explicitly lists `week_52_low: 2.61` and `current_price: 2.72`; the characterization "near its 52-week low" is arithmetically verified ($2.72 vs. $2.61 low).

---

CLAIM: "well off its 52-week high of $6.55"
LABEL: SUPPORTED
REASON: The raw source data lists `week_52_high: 6.55`; at $2.72 the stock is 58.5% below its 52-week high, confirming it is "well off" that level.

---

CLAIM: "the company's disclosed going concern doubt"
LABEL: SUPPORTED
REASON: Both the RAG SEC Highlights and Risk Factors sections explicitly state "substantial doubt exists regarding the company's ability to continue as a going concern," and this is repeated in the pre-written SEC Filing Highlights and Risk Factors sections.

---

CLAIM: "failure to do so could force the delay or outright elimination of its product development programs"
LABEL: SUPPORTED
REASON: The RAG Risk Factors and pre-written Risk Factors section explicitly state "inability to raise capital when needed could force delays or elimination of product development programs."

---

## OUTLOOK

No explicit quantitative figures, price targets, ratios, or specific numeric thresholds appear in the Outlook section. The section contains only qualitative and directional statements (e.g., "cautious," "non-dilutive," "favorably structured capital," "human trials," "encouraging early data"). These are directional/qualitative characterizations rather than specific quantitative claims, and therefore fall outside the scope of the audit criteria (which covers "specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number").

No auditable quantitative or forward-looking numeric claims are present in the Outlook section to evaluate.

---

**Summary:** All five auditable quantitative claims in the Executive Summary are **SUPPORTED** by the raw source data. The Outlook section contains no specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers requiring audit entries.
