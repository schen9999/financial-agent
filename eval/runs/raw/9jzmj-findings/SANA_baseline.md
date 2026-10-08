# SANA — baseline

## Metadata

ticker: SANA
arm: baseline
judge_prompt_version: v2
context_sha256: 483caca98876f7b302800ef51692797967bb641b3222264c447b148795acc0b7
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 323, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.171, "latency_s_total": 4.171, "parse_failure": 0, "prompt_tokens": 2147, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 417, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.046, "latency_s_total": 4.046, "parse_failure": 0, "prompt_tokens": 2135, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 184, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.626, "latency_s_total": 2.626, "parse_failure": 0, "prompt_tokens": 625, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 153, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.886, "latency_s_total": 1.886, "parse_failure": 0, "prompt_tokens": 618, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 211, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.43, "latency_s_total": 2.43, "parse_failure": 0, "prompt_tokens": 493, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 167, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.077, "latency_s_total": 2.077, "parse_failure": 0, "prompt_tokens": 408, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1199, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.115, "latency_s_total": 17.115, "parse_failure": 0, "prompt_tokens": 1840, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "SANA",
  "company_name": "Sana Biotechnology, Inc.",
  "current_price": 2.89,
  "currency": "USD",
  "market_cap": 865152256.0,
  "forward_pe": -5.206176,
  "week_52_high": 6.55,
  "week_52_low": 2.61,
  "net_income": -211822000.0,
  "profit_margin": 0.0,
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
[Indexed to Pinecone] # Key Takeaways from SANA's SEC Filings

Based on the available SEC filing information, the primary takeaways are:

## Critical Risk Factors

**Going Concern Uncertainty**: The company faces substantial doubt regarding its ability to continue as a going concern, which is a significant concern for investors.

**Technology and Development Risks**: The company's business relies on novel, unproven cell engineering platforms (both ex vivo and in vivo). There is considerable uncertainty about whether these technologies will result in approvable or marketable products, and development timelines and costs are difficult to predict.

**Capital Requirements**: The company will require additional funding to finance operations. Inability to raise capital on acceptable terms could force delays or elimination of product development and commercialization efforts.

## Operational Challenges

**Clinical Development Complexity**: The path to regulatory approval is lengthy, expensive, and uncertain. Clinical trials may fail to demonstrate safety, efficacy, or meet FDA requirements, potentially preventing or delaying commercialization.

**Manufacturing and Supply Chain**: Product manufacturing is complex, and the company depends on third-party contract manufacturers and suppliers. Any disruptions could delay or halt clinical trial supply or commercial sales.

**Personnel and Growth Management**: Success depends on retaining key personnel and recruiting qualified staff. The company may face difficulties managing growth as operations expand.

## Strategic Dependencies

The company relies on third-party relationships for research, manufacturing, and clinical trial activities, and depends on licensed intellectual property from external sources.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company has disclosed numerous material risk factors affecting its business, which can be organized into several key categories:

## Technology and Development Risks
- The cell engineering platforms are based on novel, unproven technologies that may not result in approvable or marketable products
- Inability to successfully identify, develop, and commercialize product candidates, or experiencing significant delays in doing so
- Preclinical testing may be delayed or unsuccessful, harming the ability to commence clinical trials
- Clinical trials may fail to demonstrate that product candidates meet regulatory requirements for safety, purity, potency, and efficacy

## Financial and Operational Risks
- Substantial doubt regarding the company's ability to continue as a going concern
- Need for additional funding to finance operations, with potential inability to raise capital on acceptable terms
- Potential need to delay, reduce, or eliminate product development programs or commercialization efforts
- Difficulties in managing growth and expansion of operations

## Personnel and Strategic Risks
- Dependence on retaining key personnel and recruiting qualified staff
- Inability to realize benefits from acquired or in-licensed technologies
- Failure to enter into or realize benefits from strategic relationships

## Manufacturing and Supply Chain Risks
- Complex manufacturing processes with potential production difficulties
- Exposure to supply chain risks for materials required in manufacturing
- Reliance on third parties (CDMOs, CROs) that may fail to perform obligations

## Regulatory and Intellectual Property Risks
- Extensive regulatory requirements and lengthy, unpredictable approval processes
- Inability to adequately protect intellectual property rights
- Dependence on licensed intellectual property from third parties
- Risks related to human stem cell use, including ethical, legal, and social implications

## Safety and Commercial Risks
- Product candidates may cause serious adverse side effects or have unacceptable properties
- Cybersecurity vulnerabilities in internal and third-party systems

## Pre-written sections (judge input)

### Financial Health

Sana Biotechnology trades at $2.89 per share with a market capitalization of $865 million, down significantly from its 52-week high of $6.55. The company operates at a substantial loss, with a negative net income of $211.8 million and a forward P/E ratio of -5.21, indicating unprofitability and typical early-stage biotech cash burn. With no positive revenue or profit margin reported, SANA remains a pre-commercial or early-stage development company dependent on capital reserves and financing to fund operations. The SEC filings emphasize high investment risk and multiple uncertainties, reflecting the inherent challenges of biotechnology ventures. Investors should view this as a high-risk, speculative position suitable only for those with significant risk tolerance and conviction in the company's pipeline potential.

### Recent Developments

Limited recent news is available for Sana Biotechnology at this time. The company's most recent SEC filings—a 10-K filed in March 2026 and a 10-Q filed in August 2026—emphasize significant risk factors inherent to biotech investing, including exposure to geopolitical and economic uncertainties. With a market capitalization of $865 million, negative net income of $211.8 million, and a stock trading near its 52-week low of $2.61 (current price $2.89), investors should monitor upcoming clinical trial results and pipeline announcements, as these will be critical catalysts for the stock's recovery.

### SEC Filing Highlights

Sana Biotechnology faces substantial doubt regarding its ability to continue as a going concern, requiring additional capital to finance ongoing operations and product development. The company's business depends entirely on novel, unproven cell engineering platforms (ex vivo and in vivo) with considerable uncertainty around regulatory approval, development timelines, and commercialization success. Clinical development presents significant risks, as the path to FDA approval is lengthy, expensive, and uncertain, with potential for trial failures to delay or prevent product launches. Manufacturing complexity and reliance on third-party contract manufacturers and suppliers create supply chain vulnerabilities that could disrupt clinical trials and commercial operations. Success is contingent on retaining key personnel, recruiting qualified staff, and maintaining strategic partnerships for research, manufacturing, and clinical activities.

### Risk Factors

- **Unproven Technology and Clinical Development Risk**: Sana's cell engineering platforms are based on novel, unproven technologies with no guarantee of successful commercialization. Product candidates must demonstrate safety, efficacy, and purity in clinical trials to meet regulatory requirements, with potential for significant delays or failure that could halt development programs entirely.

- **Going Concern and Funding Risk**: The company faces substantial doubt regarding its ability to continue as a going concern and requires additional capital to finance operations. Inability to raise funding on acceptable terms could force delays, reductions, or elimination of product development and commercialization efforts.

- **Manufacturing and Third-Party Dependency Risk**: Sana relies on complex manufacturing processes and third-party contract manufacturers (CDMOs) and research organizations (CROs) to execute its strategy. Supply chain disruptions, manufacturing difficulties, or failure by these partners to perform could significantly impair the company's ability to develop and deliver products.

## Audited (Exec Summary + Outlook)

### Executive Summary
Sana Biotechnology is a pre-commercial, early-stage biotechnology company developing novel ex vivo and in vivo cell engineering platforms, currently trading at $2.89 per share with a market capitalization of $865 million — well off its 52-week high of $6.55 and hovering near its 52-week low of $2.61. The stock is notable now precisely because of this compressed valuation alongside a going concern designation, a negative net income of $211.8 million, and an absence of commercial revenue, creating a high-risk, high-optionality setup that demands careful scrutiny rather than passive observation. The single most important near-term variable is whether clinical trial data from the company's pipeline candidates can demonstrate sufficient safety and efficacy to justify continued investment and unlock the additional capital the company explicitly requires to sustain operations.

### Outlook
The directional lean on SANA is **cautious**, with the possibility of turning more constructive only under a specific and narrow set of conditions. The primary headwinds are structural and immediate: a going concern designation, an absence of commercial revenue, dependence on unproven cell engineering technology, and reliance on external capital and third-party manufacturing partners — all of which create compounding execution risk. The key variables an investor should monitor are clinical trial readouts for pipeline candidates, the company's ability to secure additional financing on acceptable terms, and any meaningful updates to its manufacturing and partnership arrangements. On the tailwind side, the broader cell therapy and gene engineering space continues to attract scientific and investor interest, and a positive clinical data event could serve as a meaningful re-rating catalyst. What would strengthen the thesis: demonstrated safety and efficacy data from ongoing trials, a successful capital raise that meaningfully extends the operational runway, or a strategic partnership that validates the platform and reduces funding dependency. What would further weaken the thesis: clinical trial failures or holds, an inability to raise capital, deterioration of key partnerships, or loss of critical personnel — any of which could accelerate the going concern risk and materially impair the company's ability to continue development.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "currently trading at $2.89 per share"
LABEL: SUPPORTED
REASON: The raw source data explicitly lists `"current_price": 2.89` for SANA.

---

CLAIM: "market capitalization of $865 million"
LABEL: SUPPORTED
REASON: The raw source data lists `"market_cap": 865152256.0`, which rounds to $865 million; the pre-written Financial Health section also states "$865 million."

---

CLAIM: "well off its 52-week high of $6.55"
LABEL: SUPPORTED
REASON: The raw source data explicitly lists `"week_52_high": 6.55`; at $2.89 the stock is 55.9% below that high, confirming "well off."

---

CLAIM: "hovering near its 52-week low of $2.61"
LABEL: SUPPORTED
REASON: The raw source data lists `"week_52_low": 2.61`; at $2.89 the stock is $0.28 above the low, and the pre-written Recent Developments section uses identical language, confirming both the figure and the positional characterization arithmetically ($2.89 vs. $2.61 = 10.7% above the low, consistent with "hovering near").

---

CLAIM: "a negative net income of $211.8 million"
LABEL: SUPPORTED
REASON: The raw source data lists `"net_income": -211822000.0`, which rounds to -$211.8 million; the pre-written Financial Health section also states "$211.8 million."

---

**OUTLOOK**

No specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section. All claims in the Outlook are qualitative or directional in nature (e.g., "cautious," "going concern designation," "absence of commercial revenue," "unproven cell engineering technology," "clinical trial readouts," "successful capital raise," "strategic partnership"). None of these constitute auditable quantitative or forward-looking numerical claims under the defined scope.

---

**SUMMARY TABLE**

| Claim | Label |
|---|---|
| $2.89 per share | SUPPORTED |
| Market cap of $865 million | SUPPORTED |
| 52-week high of $6.55 | SUPPORTED |
| 52-week low of $2.61 | SUPPORTED |
| Negative net income of $211.8 million | SUPPORTED |

All five auditable quantitative claims in the Executive Summary are fully supported by the raw source data. The Outlook section contains no auditable quantitative or forward-looking numerical claims.
