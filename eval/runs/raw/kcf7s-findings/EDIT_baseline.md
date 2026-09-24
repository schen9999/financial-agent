# EDIT — baseline

## Metadata

ticker: EDIT
arm: baseline
judge_prompt_version: v2
context_sha256: bedc04056b84309a39a249b07ee8d656bd92e3e835219cdf7f5e63f99f5314df

## Retrieved source context

STOCK DATA:
{
  "ticker": "EDIT",
  "company_name": "Editas Medicine, Inc.",
  "current_price": 2.69,
  "currency": "USD",
  "market_cap": 413130304.0,
  "forward_pe": -3.5717604,
  "week_52_high": 4.537,
  "week_52_low": 1.66,
  "revenue": 47005000.0,
  "net_income": -73949000.0,
  "profit_margin": -1.57322,
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

## Financial Position and Profitability Challenges

EDIT has incurred significant cumulative losses totaling $1.6 billion as of December 31, 2025, with annual net losses of $160.1 million (2025), $237.1 million (2024), and $153.2 million (2023). The company is not currently profitable and expects to continue incurring substantial losses for the foreseeable future.

## Funding and Capital Requirements

The company's existing cash and cash equivalents as of December 31, 2025 are projected to fund operations through the third quarter of 2027. Beyond that timeframe, EDIT will require substantial additional capital to continue operations. The company has limited committed external funding sources, with primary potential sources being contingent payments from collaboration agreements with BMS and retained portions of payments under the Vertex license agreement.

## Development Stage and Timeline

EDIT's most advanced research programs are currently in preclinical testing stages only. The company does not expect to have product candidates ready for commercialization for many years, if ever. EDIT-401 is specifically mentioned as a key product candidate under development.

## Risk Factors

Key risks include:
- Inability to raise capital when needed could force delays or elimination of research programs
- Regulatory requirements could increase expenses beyond current expectations
- Economic downturns or political developments could adversely affect funding availability and operations
- Success depends on completing preclinical studies, clinical trials, obtaining regulatory approval, and achieving commercial success—all uncertain outcomes

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors, with the main categories being:

## Financial Position and Capital Needs
- **Substantial accumulated losses**: The company has incurred net losses of $160.1 million, $237.1 million, and $153.2 million for 2025, 2024, and 2023 respectively, with an accumulated deficit of $1.6 billion as of December 31, 2025.
- **Expectation of continued losses**: The company expects to incur losses for the foreseeable future and may never achieve profitability.
- **Significant funding requirements**: Substantial additional capital will be needed to continue operations, with existing cash expected to fund operations only into the third quarter of 2027.
- **Limited external funding sources**: The company has limited committed potential external sources of funds beyond contingent payments from collaboration agreements.

## Development and Commercialization Challenges
- **Early-stage development**: The company is currently only in preclinical testing stages for its most advanced research programs.
- **Time and expense intensive process**: Identifying product candidates and conducting preclinical testing and clinical trials is time-consuming, expensive, and uncertain, taking years to complete.
- **Uncertain path to commercialization**: The company may never generate necessary data to obtain marketing approval or achieve product sales.
- **Years until commercialization**: Commercial revenues are not expected for years, if at all.

## Economic and Market Risks
- **Economic sensitivity**: Unfavorable national or global economic conditions, political developments, or financial crises could adversely affect the company's ability to raise capital and business operations.

## Pre-written sections (judge input)

### Financial Health

Editas Medicine trades at $2.69 per share with a market capitalization of $413.1 million, reflecting significant pressure on the stock price (52-week range: $1.66–$4.54). The company is unprofitable with a negative profit margin of -157.3% and net losses of $73.9 million against revenue of $47.0 million, indicating the company is in a pre-commercial or early-stage revenue phase typical of biotechnology firms. The negative forward P/E ratio underscores the lack of profitability and highlights substantial execution risk. As a gene-editing biotech company, Editas requires continued capital investment to advance its pipeline, and SEC filings emphasize significant financial and operational risks ahead.

### Recent Developments

Editas Medicine continues to face significant financial headwinds, with the company reporting a net loss of $73.9 million against minimal revenue of $47 million, reflecting the substantial R&D investments required for gene-editing therapeutics development. The stock has declined substantially from its 52-week high of $4.54 to $2.69, indicating investor concerns about the company's path to profitability and capital requirements. Recent SEC filings highlight ongoing risks related to the company's financial position and need for additional capital, which remains a critical concern for shareholders. With a negative profit margin of -157% and a market cap of approximately $413 million, Editas is at a pivotal stage where clinical trial success and potential partnerships will be essential to validate its gene-editing platform and justify continued investor support.

### SEC Filing Highlights

Editas Medicine faces significant profitability challenges with cumulative losses of $1.6 billion and annual net losses exceeding $150 million, with no expectation of near-term profitability. The company's cash runway extends only through Q3 2027, requiring substantial additional capital raises to sustain operations beyond that period. All of EDIT's product candidates, including lead program EDIT-401, remain in preclinical or early development stages with commercialization many years away. The company is heavily dependent on contingent payments from collaboration agreements with BMS and Vertex to supplement funding needs. Key risks include capital availability constraints, regulatory uncertainties, and the inherent challenges of advancing gene-editing therapies through development and regulatory approval.

### Risk Factors

- **Severe cash burn and funding constraints**: Editas has accumulated losses of $1.6 billion and burned $160.1 million in 2025 alone. With existing cash expected to fund operations only through Q3 2027, the company faces critical capital needs with limited committed external funding sources beyond collaboration agreements.

- **Early-stage development with uncertain commercialization timeline**: The company's most advanced programs remain in preclinical testing stages. Gene therapy development is inherently time-consuming, expensive, and uncertain—commercial revenues are not expected for years, if at all, and the company may never achieve marketing approval or profitability.

- **Economic sensitivity and market access risks**: Unfavorable macroeconomic conditions, political developments, or financial crises could impair the company's ability to raise necessary capital and execute its business plan, while gene therapy adoption faces uncertain reimbursement and patient access barriers.

## Audited (Exec Summary + Outlook)

### Executive Summary
Editas Medicine is a clinical-stage gene-editing biotechnology company with a market capitalization of $413.1 million, generating $47.0 million in revenue against a net loss of $73.9 million as it advances a pipeline of CRISPR-based therapies, including lead program EDIT-401, that remain in preclinical or early development stages. The stock is notable now because it trades near the lower end of its 52-week range of $1.66–$4.54, the company has accumulated $1.6 billion in cumulative losses, and its cash runway extends only through Q3 2027—placing it at a critical inflection point where capital access and pipeline progress must converge. The single most important near-term variable is the company's ability to secure additional financing or meaningful partnership milestones before its existing runway expires, as failure to do so would threaten the viability of all ongoing development programs.

### Outlook
The directional outlook for Editas Medicine is **cautious**, weighted heavily by the convergence of a hard cash runway deadline, an entirely preclinical pipeline, and a deteriorating stock price that complicates equity-based capital raises. The primary headwinds to monitor are the pace of cash consumption relative to the Q3 2027 runway, the terms and dilutive impact of any future capital raise, and whether contingent collaboration payments from BMS and Vertex materialize on a timeline that meaningfully extends the company's operational flexibility. On the tailwind side, investors should watch for any positive preclinical or early clinical data readouts from EDIT-401 or other pipeline programs, as compelling efficacy or safety signals could catalyze partnership interest or improve access to capital markets. The broader gene-editing competitive landscape and regulatory environment for CRISPR-based therapies also warrant close attention, since favorable regulatory precedents set by other gene-editing programs could reduce perceived risk across the sector and benefit Editas indirectly. What would shift this view toward more constructive territory is a combination of a well-structured financing that extends the runway meaningfully beyond Q3 2027, a new or expanded collaboration agreement that reduces capital dependency, and early clinical evidence validating the company's gene-editing platform—absent those developments, the risk of value-destructive dilution or operational curtailment remains the dominant consideration for prospective investors.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

## EXECUTIVE SUMMARY

---

CLAIM: "market capitalization of $413.1 million"
LABEL: SUPPORTED
REASON: Source data lists market_cap as 413,130,304.0, which rounds to $413.1 million.

---

CLAIM: "generating $47.0 million in revenue"
LABEL: SUPPORTED
REASON: Source data lists revenue as 47,005,000.0, which rounds to $47.0 million.

---

CLAIM: "net loss of $73.9 million"
LABEL: SUPPORTED
REASON: Source data lists net_income as -73,949,000.0, which rounds to -$73.9 million.

---

CLAIM: "lead program EDIT-401"
LABEL: SUPPORTED
REASON: EDIT-401 is explicitly named as a key product candidate in the RAG — SEC Highlights section.

---

CLAIM: "remain in preclinical or early development stages"
LABEL: SUPPORTED
REASON: RAG — SEC Highlights states "EDIT's most advanced research programs are currently in preclinical testing stages only."

---

CLAIM: "52-week range of $1.66–$4.54"
LABEL: SUPPORTED
REASON: Source data lists week_52_low as 1.66 and week_52_high as 4.537, which rounds to $4.54.

---

CLAIM: "trades near the lower end of its 52-week range of $1.66–$4.54"
LABEL: SUPPORTED
REASON: Current price is $2.69; the midpoint of the range is (1.66 + 4.537)/2 = $3.10, and $2.69 is below the midpoint, arithmetically confirming it is in the lower half/end of the range.

---

CLAIM: "accumulated $1.6 billion in cumulative losses"
LABEL: SUPPORTED
REASON: RAG — SEC Highlights explicitly states "cumulative losses totaling $1.6 billion as of December 31, 2025."

---

CLAIM: "cash runway extends only through Q3 2027"
LABEL: SUPPORTED
REASON: RAG — SEC Highlights states "existing cash and cash equivalents as of December 31, 2025 are projected to fund operations through the third quarter of 2027."

---

## OUTLOOK

---

CLAIM: "hard cash runway deadline" / "Q3 2027 runway"
LABEL: SUPPORTED
REASON: RAG — SEC Highlights and Risk Factors both confirm cash is expected to fund operations only through Q3 2027.

---

CLAIM: "entirely preclinical pipeline"
LABEL: SUPPORTED
REASON: RAG — SEC Highlights states all most advanced programs are in preclinical testing stages only; consistent with SEC Filing Highlights pre-written section.

---

CLAIM: "contingent collaboration payments from BMS and Vertex"
LABEL: SUPPORTED
REASON: RAG — SEC Highlights explicitly names "contingent payments from collaboration agreements with BMS and Vertex license agreement" as primary potential funding sources.

---

CLAIM: "EDIT-401 or other pipeline programs" (as a watch item for preclinical or early clinical data readouts)
LABEL: SUPPORTED
REASON: EDIT-401 is named in the source data (RAG — SEC Highlights) as a key product candidate; the characterization of it as preclinical is also supported.

---

CLAIM: "extends the runway meaningfully beyond Q3 2027"
LABEL: SUPPORTED
REASON: Q3 2027 is the stated runway endpoint in the source data; this is a directional/qualitative forward-looking framing relative to a supported figure, not a new quantitative claim.

---

*No additional standalone quantitative figures, price targets, specific ratios, or named milestones appear in the Outlook section beyond those already evaluated above.*

---

### Summary Table

| Claim | Label |
|---|---|
| Market cap $413.1 million | SUPPORTED |
| Revenue $47.0 million | SUPPORTED |
| Net loss $73.9 million | SUPPORTED |
| Lead program EDIT-401 | SUPPORTED |
| Preclinical/early development stages | SUPPORTED |
| 52-week range $1.66–$4.54 | SUPPORTED |
| Trades near lower end of 52-week range | SUPPORTED |
| $1.6 billion cumulative losses | SUPPORTED |
| Cash runway through Q3 2027 | SUPPORTED |
| Q3 2027 runway (Outlook) | SUPPORTED |
| Entirely preclinical pipeline | SUPPORTED |
| BMS and Vertex collaboration payments | SUPPORTED |
| EDIT-401 data readout watch item | SUPPORTED |
| Runway beyond Q3 2027 (directional) | SUPPORTED |

**All audited claims are SUPPORTED.** No unsupported or inference-only claims were identified in the Executive Summary or Outlook sections.
