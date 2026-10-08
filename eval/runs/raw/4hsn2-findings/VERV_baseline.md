# VERV — baseline

## Metadata

ticker: VERV
arm: baseline
judge_prompt_version: v2
context_sha256: e5bbb5a2e605bf1bcb6de1825f79114cedd0596de3af03e76201627268c1636f
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 415, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.048, "latency_s_total": 5.048, "parse_failure": 0, "prompt_tokens": 2772, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 386, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.056, "latency_s_total": 4.056, "parse_failure": 0, "prompt_tokens": 2490, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 183, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.421, "latency_s_total": 2.421, "parse_failure": 0, "prompt_tokens": 615, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 204, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.001, "latency_s_total": 3.001, "parse_failure": 0, "prompt_tokens": 608, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 167, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.955, "latency_s_total": 1.955, "parse_failure": 0, "prompt_tokens": 456, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 262, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.717, "latency_s_total": 2.717, "parse_failure": 0, "prompt_tokens": 493, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1313, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.97, "latency_s_total": 17.97, "parse_failure": 0, "prompt_tokens": 2030, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "VERV",
  "company_name": "N/A",
  "currency": "USD"
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
    "filing_date": "2025-02-27",
    "summary": "Item 1A. Risk Factors. Our future operating results could differ materially from the results described in this Annual Report on Form 10-K due to the risks and uncertainties described below. You should consider carefully the following information about risks below in evaluating our business. If any of the following risks actually occur, our business, financial conditions, results of operations and future growth prospects would likely be materially and adversely affected. In these circumstances, the market price of our common stock would likely decline. In addition, we cannot assure investors that our assumptions and expectations will prove to be correct. Important factors could cause our actual results to differ materially from those indicated or implied by forward-looking statements. See p"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2025-05-14",
    "summary": "Item 1A. Risk Factors 26 Item 2. Unregistered Sales of Equity Securities and Use of Proceeds 91 Item 5. Other Information 91 Item 6. Exhibits 92 Signatures 93 Part I \u2500 Financi al Information Item 1. Financi al Statements Verve Therapeutics, Inc. Condensed consolidat ed balance sheets (in thousands, except share and per share amounts) (unaudited) March 31, 2025 December 31, 2024 Assets Current assets: Cash and cash equivalents $ 96,554 $ 172,560 Marketable securities 400,523 351,721 Collaboration receivable 1,399 3,255 Prepaid expenses and other current assets 13,174 15,215 Total current assets 511,650 542,751 Property and equipment, net 18,457 18,644 Restricted cash 4,774 4,774 Operating lease right-of-use assets 76,217 78,082 Other long term assets 3,065 3,141 Total assets $ 614,163 $ 647"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] # Key Takeaways from VERV's Latest 10-K Filing

## Financial Position
- The company has accumulated significant losses since inception, with net losses of $198.7 million in 2024, $200.1 million in 2023, and $157.4 million in 2022
- Accumulated deficit stands at $743.0 million as of December 31, 2024
- No approved products or product sales revenue to date
- Cash, cash equivalents, and marketable securities totaled $524.3 million as of December 31, 2024, with an additional $20.0 million milestone payment received from Eli Lilly in February 2025

## Funding and Capital Requirements
- The company estimates its existing capital will fund operations into mid-2027
- Substantial additional funding will be needed to continue operations, particularly as clinical trials advance and commercialization efforts expand
- No committed credit facilities or external funding sources currently in place
- Operations have been financed through private placements, public stock offerings, and collaboration payments, including the Eli Lilly Research and Collaboration Agreement

## Development Pipeline and Expenses
- Ongoing clinical trials include Heart-2 Phase 1b for VERVE-102, Pulse-1 Phase 1b for VERVE-201, and planned Phase 2 for the PCSK9 program
- Significant expenses anticipated for clinical development, regulatory approvals, manufacturing, commercialization infrastructure, and intellectual property protection
- Milestone and success payments owed to various partners including Lilly, Acuitas, Broad Institute, Harvard, and Novartis

## Risk Outlook
- Profitability is uncertain and may never be achieved
- Continued operating losses expected for the foreseeable future
- Capital depletion risk if development timelines extend or funding becomes unavailable

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors related to its financial position and operations:

## Financial Losses and Lack of Revenue
- The company has incurred substantial losses since inception, with net losses of $198.7 million, $200.1 million, and $157.4 million for 2024, 2023, and 2022 respectively
- An accumulated deficit of $743.0 million exists as of December 31, 2024
- No products have been approved for sale and no revenue has been generated from product sales
- Losses are expected to continue for the foreseeable future with no assurance of achieving profitability

## Need for Substantial Additional Capital
- The company currently lacks a credit facility or committed sources of capital
- Significant funding will be required to advance preclinical activities, conduct clinical trials, and pursue commercialization efforts
- If unable to raise capital on acceptable terms, the company may be forced to delay, reduce, or eliminate research and development programs
- Capital requirements depend on numerous factors including clinical trial progress, manufacturing costs, regulatory review timelines, and commercialization expenses

## Product Development Uncertainties
- Clinical development is time-consuming, expensive, and uncertain
- The company has not yet completed a clinical trial of any product candidate
- There is no assurance of successfully developing viable products or achieving market acceptance
- Even if products are approved, revenue may not be sufficient to sustain operations or achieve profitability

## Liquidity Concerns
- While the company had $524.3 million in cash and marketable securities as of December 31, 2024, management estimates these funds will support operations only into mid-2027
- This estimate is based on assumptions that may prove incorrect

## Pre-written sections (judge input)

### Financial Health

Verve Therapeutics (VERV) is a clinical-stage biopharmaceutical company with limited revenue generation, typical of pre-commercial biotech firms. As of Q1 2025, the company maintains a cash position of $96.6 million and marketable securities of $400.5 million, providing a combined liquidity buffer of approximately $497 million to fund operations and clinical development. However, the company faces typical biotech risks including high cash burn rates, no current profitability, and dependence on successful clinical trial outcomes and future financing. The recent 10-K and 10-Q filings emphasize substantial operational risks that could materially impact financial performance and stock valuation. Investors should monitor cash runway closely, as this metric is critical for pre-revenue biotech companies pursuing drug development programs.

### Recent Developments

Verve Therapeutics filed its Q1 2025 10-Q on May 14, 2025, revealing a significant cash position decline from $172.6 million at year-end 2024 to $96.6 million by March 31, 2025, indicating accelerated cash burn as the company advances its pipeline. The company maintains a combined liquid position of approximately $497 million when including marketable securities, providing runway for ongoing clinical development and operations. The 10-K filing on February 27, 2025 emphasized material risk factors that could adversely affect business operations and stock performance, suggesting investors should carefully monitor clinical trial progress and partnership developments. For investors, the key takeaway is that while Verve has adequate near-term funding, the burn rate trajectory warrants close attention to upcoming clinical milestones and potential partnership announcements that could validate the therapeutic approach and extend the cash runway.

### SEC Filing Highlights

Verve Therapeutics reported a net loss of $198.7 million in 2024 with an accumulated deficit of $743.0 million, reflecting its pre-commercial stage as a gene-editing company with no approved products or revenue. The company maintains $524.3 million in cash and equivalents as of December 31, 2024, plus a $20.0 million milestone payment from Eli Lilly received in February 2025, estimated to fund operations into mid-2027. Key clinical programs include Phase 1b trials for VERVE-102 (Heart-2) and VERVE-201 (Pulse-1), with a planned Phase 2 for the PCSK9 program, though substantial additional funding will be required as development advances. The company faces significant capital requirements for clinical trials, regulatory approvals, manufacturing scale-up, and commercialization infrastructure, with milestone payments owed to partners including Eli Lilly, Acuitas, and Broad Institute. Profitability remains uncertain with continued operating losses expected for the foreseeable future, creating material risk if development timelines extend or external funding becomes unavailable.

### Risk Factors

- **Substantial Ongoing Losses with No Revenue**: The company has accumulated $743.0 million in deficits and reported net losses exceeding $157 million annually, with no approved products or revenue generation. Losses are expected to continue indefinitely with no assurance of achieving profitability.

- **Critical Funding Dependency**: The company lacks committed capital sources and will require substantial additional funding to advance clinical trials and commercialization. Without securing capital on acceptable terms, the company may be forced to delay or eliminate R&D programs.

- **Clinical Development Uncertainty**: No product candidates have completed clinical trials. Success is uncertain and time-consuming, with no guarantee of regulatory approval, market acceptance, or revenue sufficiency even if products reach market.

## Audited (Exec Summary + Outlook)

### Executive Summary
Verve Therapeutics is a clinical-stage gene-editing company targeting cardiovascular disease, carrying an accumulated deficit of $743.0 million and no approved products or revenue, but supported by a combined liquidity position of approximately $497 million as of Q1 2025. The stock is notable now because the company is actively advancing Phase 1b trials for VERVE-102 and VERVE-201 while navigating an accelerating cash burn rate — cash on hand alone declined from $172.6 million to $96.6 million in a single quarter — making the near-term clinical and financing picture unusually consequential. The single most important variable shaping the outcome is whether upcoming clinical trial data from the Heart-2 and Pulse-1 programs demonstrate sufficient safety and efficacy to attract partnership capital and support continued development into and beyond the planned Phase 2.

### Outlook
The directional outlook for Verve Therapeutics is **cautious**, though with asymmetric upside contingent on clinical execution. The primary tailwind is the company's estimated funding runway into mid-2027 and its existing partnership with Eli Lilly, which provides both validation of the gene-editing approach and a precedent for future milestone-driven capital. The large and underserved cardiovascular disease market also represents a meaningful long-term commercial opportunity if the science translates. However, the headwinds are substantial: the accelerating cash burn rate, the absence of any approved product or revenue, and the binary nature of clinical trial outcomes create meaningful downside risk. Investors should closely watch the pace and direction of data readouts from the Heart-2 (VERVE-102) and Pulse-1 (VERVE-201) Phase 1b trials, the trajectory of quarterly cash consumption relative to the mid-2027 runway estimate, and any announcements regarding new partnerships or financing arrangements. The thesis would strengthen materially on positive clinical data that de-risks the PCSK9 program and attracts additional partnership capital; it would weaken on adverse safety signals, trial delays, or an inability to secure funding on acceptable terms before the runway narrows meaningfully.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "carrying an accumulated deficit of $743.0 million"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights, RAG Risk Factors, and SEC Filing Highlights pre-written section all explicitly state "accumulated deficit of $743.0 million as of December 31, 2024."

---

CLAIM: "supported by a combined liquidity position of approximately $497 million as of Q1 2025"
LABEL: SUPPORTED
REASON: The Financial Health and Recent Developments pre-written sections both state "approximately $497 million" as the combined liquidity; verified by arithmetic from the 10-Q balance sheet: $96,554K (cash) + $400,523K (marketable securities) = $497,077K ≈ $497 million.

---

CLAIM: "actively advancing Phase 1b trials for VERVE-102 and VERVE-201"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and SEC Filing Highlights pre-written section explicitly name "Phase 1b trials for VERVE-102 (Heart-2) and VERVE-201 (Pulse-1)."

---

CLAIM: "cash on hand alone declined from $172.6 million to $96.6 million in a single quarter"
LABEL: SUPPORTED
REASON: The Recent Developments pre-written section states "cash position decline from $172.6 million at year-end 2024 to $96.6 million by March 31, 2025"; the 10-Q balance sheet confirms $172,560K (Dec 31, 2024) and $96,554K (Mar 31, 2025), both rounding to the stated figures.

---

CLAIM: "the Heart-2 and Pulse-1 programs"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and SEC Filing Highlights pre-written section explicitly name "Heart-2 Phase 1b for VERVE-102" and "Pulse-1 Phase 1b for VERVE-201."

---

CLAIM: "planned Phase 2" (for the PCSK9 program)
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and SEC Filing Highlights pre-written section both state "planned Phase 2 for the PCSK9 program."

---

**OUTLOOK**

---

CLAIM: "the company's estimated funding runway into mid-2027"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights, RAG Risk Factors, and SEC Filing Highlights pre-written section all explicitly state "management estimates these funds will support operations only into mid-2027."

---

CLAIM: "its existing partnership with Eli Lilly"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights references "the Eli Lilly Research and Collaboration Agreement" and the SEC Filing Highlights pre-written section names "Eli Lilly" as a partner providing a "$20.0 million milestone payment."

---

CLAIM: "$20.0 million milestone payment" (implied via "milestone-driven capital" referencing the Eli Lilly precedent)
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and SEC Filing Highlights pre-written section explicitly state "a $20.0 million milestone payment received from Eli Lilly in February 2025." The Outlook references this only directionally ("milestone-driven capital"), but the underlying figure is present in the source.

---

CLAIM: "the Heart-2 (VERVE-102) and Pulse-1 (VERVE-201) Phase 1b trials"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and SEC Filing Highlights pre-written section explicitly name both programs with these identifiers.

---

CLAIM: "the mid-2027 runway estimate" (referenced as a benchmark for quarterly cash consumption monitoring)
LABEL: SUPPORTED
REASON: Consistent with the mid-2027 runway figure explicitly stated in the RAG SEC Highlights and RAG Risk Factors sections.

---

CLAIM: "the PCSK9 program" (as the program de-risked by positive clinical data)
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and SEC Filing Highlights pre-written section both reference "a planned Phase 2 for the PCSK9 program," confirming this program exists in the source data.

---

**Summary of findings:** All quantitative figures, named milestones, program identifiers, and forward-looking metrics in the Executive Summary and Outlook are SUPPORTED by the source data or pre-written sections. No claims were found to be UNSUPPORTED or INFERENCE-only. The brief does not introduce any figures, thresholds, ratios, or named entities that are absent from the provided context.
