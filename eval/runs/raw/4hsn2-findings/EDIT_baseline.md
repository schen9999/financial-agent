# EDIT — baseline

## Metadata

ticker: EDIT
arm: baseline
judge_prompt_version: v2
context_sha256: f9f433ea5fb3eca76c4cf70f96849909e5bcfc03dd7f638e0d97cd6c706317e9
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 334, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.802, "latency_s_total": 3.802, "parse_failure": 0, "prompt_tokens": 2492, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 353, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.06, "latency_s_total": 4.06, "parse_failure": 0, "prompt_tokens": 2480, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 164, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.854, "latency_s_total": 1.854, "parse_failure": 0, "prompt_tokens": 658, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 214, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.799, "latency_s_total": 2.799, "parse_failure": 0, "prompt_tokens": 651, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 202, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.425, "latency_s_total": 2.425, "parse_failure": 0, "prompt_tokens": 426, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 192, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.819, "latency_s_total": 1.819, "parse_failure": 0, "prompt_tokens": 415, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1245, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 18.828, "latency_s_total": 18.828, "parse_failure": 0, "prompt_tokens": 1948, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "EDIT",
  "company_name": "Editas Medicine, Inc.",
  "current_price": 2.79,
  "currency": "USD",
  "market_cap": 428488288.0,
  "forward_pe": -3.7045395,
  "week_52_high": 4.537,
  "week_52_low": 1.66,
  "financial_currency": "USD",
  "revenue": 47005000.0,
  "net_income": -73949000.0,
  "profit_margin_pct": -157.32,
  "dividend_yield": 0.0,
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
    "filing_date": "2026-03-09",
    "summary": "Item 1A. Risk Factors Our business is subject to numerous risks. The following important factors, among others, could cause our actual results to differ materially from those expressed in forward-looking statements made by us or on our behalf in this Annual Report on Form 10-K and other filings with the U.S. Securities and Exchange Commission (the \u201cSEC\u201d), press releases, communications with investors, and oral statements. Actual future results may differ materially from those anticipated in our forward-looking statements. We undertake no obligation to update any forward-looking statements, whether as a result of new information, future events, or otherwise. Risks Related to Our Financial Position and Need for Additional Capital We have incurred significant losses since inception. We expect"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-05",
    "summary": "Item 1A. Risk Factors,\u201d as updated by our subsequent filings with the SEC. We may not actually achieve the plans, intentions or expectations disclosed in our forward-looking statements, and you should not place undue reliance on our forward-looking statements. Actual results or events could differ materially from the plans, intentions and expectations disclosed in the forward-looking statements we make. Our forward-looking statements do not reflect the potential impact of any future acquisitions, mergers, dispositions, joint ventures or investments that we may make. You should read this Quarterly Report on Form 10-Q and the documents that we have filed as exhibits to this Quarterly Report on Form 10-Q completely and with the understanding that our actual future results may be materially di"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] # Key Takeaways from EDIT's SEC Filings

## Financial Position and Losses
- The company has accumulated significant operating losses totaling $1.6 billion as of December 31, 2025
- Net losses were $160.1 million (2025), $237.1 million (2024), and $153.2 million (2023)
- Losses are expected to continue for the foreseeable future, with no guarantee of achieving profitability

## Funding and Capital Requirements
- Current cash and equivalents are projected to fund operations through Q3 2027
- The company requires substantial additional capital to continue operations and advance its research programs
- Primary external funding sources are limited to contingent payments from BMS collaboration and retained portions of payments from the Vertex license agreement
- Future funding may come through equity offerings, debt financing, collaborations, and licensing arrangements

## Development Stage and Timeline
- The company is currently in preclinical testing stages for its most advanced research programs, including EDIT-401
- Years of development remain before any product candidates are ready for commercialization
- Significant expenses are expected to increase as the company progresses preclinical studies and clinical trials

## Key Risk Factors
- Inability to raise capital when needed could force delays or elimination of research and development programs
- Economic downturns or unfavorable political developments could impact the ability to secure funding and maintain operations
- Regulatory requirements could increase expenses beyond current expectations
- Even with approved products, profitability is not guaranteed

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors, with the main categories being:

## Financial Position and Capital Needs
- **Substantial accumulated losses**: The company has incurred net losses of $160.1 million, $237.1 million, and $153.2 million for 2025, 2024, and 2023 respectively, with an accumulated deficit of $1.6 billion as of December 31, 2025.
- **Ongoing losses expected**: The company anticipates continued significant losses for the foreseeable future and may never achieve profitability.
- **Funding requirements**: Substantial additional capital will be needed to support preclinical studies, clinical trials, research programs, intellectual property maintenance, and potential commercialization efforts.
- **Limited funding sources**: The company's existing cash is expected to fund operations only into the third quarter of 2027, with limited committed external funding sources beyond contingent payments from collaboration agreements.

## Development and Commercialization Challenges
- **Early-stage development**: The company is currently only in preclinical testing stages for its most advanced research programs.
- **Time and expense**: Identifying product candidates and conducting testing is described as time-consuming, expensive, and uncertain, taking years to complete.
- **No guarantee of success**: There is no assurance the company will generate necessary data for marketing approval or achieve product sales.

## Economic and Market Risks
- **Economic sensitivity**: Unfavorable economic conditions, political developments, or financial crises could adversely affect the company's ability to raise capital and business operations.

## Pre-written sections (judge input)

### Financial Health

Editas Medicine trades at $2.79 per share with a market capitalization of $428.5 million, reflecting significant financial distress for the biotechnology company. The company generated $47.0 million in revenue but posted a net loss of $73.9 million, resulting in a concerning -157.32% profit margin, indicating substantial cash burn. The forward P/E ratio of -3.70 is not meaningful given the company's unprofitability. SEC filings highlight ongoing risk factors related to the company's financial position and need for additional capital, with accumulated losses since inception. Investors should view EDIT as a high-risk, pre-profitability biotech play dependent on successful clinical development and future funding.

### Recent Developments

Editas Medicine's most recent SEC filings highlight significant financial challenges and operational risks facing the company. The company reported a net loss of $73.9 million against revenue of $47 million, reflecting a negative profit margin of -157.32%, indicating the company is not yet profitable and continues to burn cash. Recent 10-K and 10-Q filings emphasize substantial risks related to the company's financial position and capital needs, with management noting ongoing losses since inception and uncertainty about achieving stated objectives. For investors, this underscores that Editas remains in a pre-commercial or early-stage revenue phase typical of gene-editing biotechnology companies, requiring continued capital raises and successful clinical trial progression to justify valuations. The stock's depressed valuation (trading at $2.79 with a negative forward P/E) reflects market skepticism about near-term profitability and the execution risks inherent in bringing CRISPR-based therapies to market.

### SEC Filing Highlights

Editas Medicine reported accumulated operating losses of $1.6 billion as of December 31, 2025, with net losses of $160.1 million in 2025, and management expects continued losses for the foreseeable future. The company's cash position is projected to fund operations only through Q3 2027, necessitating substantial additional capital through equity offerings, debt financing, or strategic partnerships to advance its pipeline. Most advanced programs including EDIT-401 remain in preclinical stages with years of development required before commercialization, while expenses are expected to increase significantly as the company progresses toward clinical trials. Key risks include potential inability to secure future funding, regulatory cost increases, and no guarantee of profitability even with approved products. Primary external funding sources are limited to contingent payments from the BMS collaboration and retained portions of the Vertex license agreement.

### Risk Factors

- **Severe cash burn and funding uncertainty**: Editas has accumulated losses of $1.6 billion and burned $160.1 million in 2025 alone. With existing cash expected to last only through Q3 2027 and no guarantee of profitability, the company faces critical funding needs for clinical trials and commercialization with limited committed external sources.

- **Early-stage development with no approved products**: All programs remain in preclinical or early clinical stages with no marketed products. Gene therapy development is inherently time-consuming, expensive, and uncertain, with no assurance the company will achieve regulatory approval or generate meaningful revenue.

- **Capital markets and economic dependency**: The company's survival depends on its ability to raise substantial additional capital in potentially unfavorable market conditions. Economic downturns, geopolitical instability, or investor sentiment shifts could severely constrain access to funding and threaten operations.

## Audited (Exec Summary + Outlook)

### Executive Summary
Editas Medicine is a clinical-stage CRISPR gene-editing biotechnology company with a market capitalization of $428.5 million, pursuing a pipeline of therapies that have yet to reach commercialization and that have generated accumulated operating losses of $1.6 billion to date. The stock is notable now precisely because of its distressed profile — trading at $2.79 per share with a cash runway projected only through Q3 2027 — placing the company at a critical inflection point where capital access and pipeline progress will determine whether it survives as an independent entity. The single most important near-term variable is the company's ability to secure substantial additional funding, whether through equity offerings, debt financing, or expanded strategic partnerships, before its existing cash position is exhausted.

### Outlook
The directional outlook for Editas Medicine is **cautious**, weighted heavily by the convergence of a hard cash runway deadline, an entirely preclinical-to-early-stage pipeline, and a capital markets environment that has shown limited appetite for pre-revenue gene-editing names. The primary tailwind is the broader scientific and commercial validation of CRISPR-based medicine as a therapeutic modality, which could attract partnership interest or improve investor sentiment toward the sector; meaningful progress on EDIT-401 or any other pipeline program advancing toward clinical milestones would be a material positive catalyst. Headwinds, however, are substantial: investors should closely watch the pace of cash consumption relative to the Q3 2027 funding horizon, the terms and dilutive impact of any future capital raise, and whether contingent payments from the BMS collaboration or the Vertex license agreement materialize in a manner that meaningfully extends the runway. A new strategic partnership, a non-dilutive funding arrangement, or a positive clinical data readout would be the conditions most likely to shift this view in a constructive direction; conversely, failure to secure additional capital on reasonable terms, an adverse regulatory development, or a deterioration in broader biotech funding conditions would further pressure an already fragile thesis.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, and forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of $428.5 million"
LABEL: SUPPORTED
REASON: Source data shows market_cap = 428,488,288.0, which rounds to $428.5 million.

---

CLAIM: "accumulated operating losses of $1.6 billion to date"
LABEL: SUPPORTED
REASON: RAG — SEC Highlights and RAG — Risk Factors both explicitly state accumulated losses totaling $1.6 billion as of December 31, 2025.

---

CLAIM: "trading at $2.79 per share"
LABEL: SUPPORTED
REASON: Source data shows current_price = 2.79 USD.

---

CLAIM: "cash runway projected only through Q3 2027"
LABEL: SUPPORTED
REASON: RAG — SEC Highlights explicitly states "Current cash and equivalents are projected to fund operations through Q3 2027," and the SEC Filing Highlights pre-written section repeats this.

---

**OUTLOOK**

---

CLAIM: "meaningful progress on EDIT-401 or any other pipeline program advancing toward clinical milestones would be a material positive catalyst"
LABEL: SUPPORTED
REASON: RAG — SEC Highlights explicitly names EDIT-401 as the most advanced program, currently in preclinical stages, making a clinical milestone advance a directly grounded forward-looking reference.

---

CLAIM: "the Q3 2027 funding horizon"
LABEL: SUPPORTED
REASON: Consistent with the source data's explicit statement that cash is projected to fund operations through Q3 2027.

---

CLAIM: "contingent payments from the BMS collaboration or the Vertex license agreement"
LABEL: SUPPORTED
REASON: RAG — SEC Highlights and the SEC Filing Highlights pre-written section both explicitly name the BMS collaboration and the Vertex license agreement as the primary limited external funding sources.

---

**NO ADDITIONAL QUANTITATIVE OR FORWARD-LOOKING CLAIMS FOUND**

The Outlook section contains no additional specific numerical figures, price targets, ratios, percentages, or named product milestones beyond those already audited above. All directional and qualitative statements (e.g., "cautious," "limited appetite," "substantial headwinds") are editorial characterizations, not specific quantitative or factual claims subject to this audit framework.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | Market cap $428.5 million | SUPPORTED |
| 2 | Accumulated operating losses $1.6 billion | SUPPORTED |
| 3 | Trading at $2.79 per share | SUPPORTED |
| 4 | Cash runway through Q3 2027 | SUPPORTED |
| 5 | EDIT-401 pipeline / clinical milestones | SUPPORTED |
| 6 | Q3 2027 funding horizon (Outlook) | SUPPORTED |
| 7 | BMS collaboration / Vertex license agreement | SUPPORTED |

All auditable claims in the Executive Summary and Outlook are **SUPPORTED** by the source data. No unsupported or inference-only claims were identified.
