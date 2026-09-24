# VERV — local-model

## Metadata

ticker: VERV
arm: local-model
judge_prompt_version: v2
context_sha256: f9490feb0877132838de8d0ab8cd6eebb48f7561f63ec5507fd77fdec7e9c247
local_model_served_name: qwen2.5-7b-instruct
local_model_dir: qwen2.5-7b-instruct
local_model_backend: openai
local_model_url: http://vllm.financial-agent.svc:8000
local_model_sampling: {"max_tokens": 512, "min_p": 0.0, "repetition_penalty": 1.1, "temperature": 0.1, "top_k": 20, "top_p": 0.8}

## Retrieved source context

STOCK DATA:
{
  "ticker": "VERV",
  "company_name": "N/A",
  "currency": "USD"
}

NEWS ARTICLES:
[]

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

## Operational Status
- Currently conducting multiple clinical trials: Heart-2 Phase 1b (VERVE-102), Pulse-1 Phase 1b (VERVE-201), and planned Phase 2 for PCSK9 program
- Evaluating next steps for Heart-1 Phase 1b clinical trial (VERVE-101)
- Continuing preclinical development and research programs

## Capital Requirements
- Expects substantial increases in operating expenses as clinical trials advance and commercialization activities expand
- Management estimates existing capital will fund operations into mid-2027
- No committed credit facility or external funding sources currently in place
- Will require significant additional capital for regulatory approvals, manufacturing scale-up, and commercialization

## Key Risks
- Expects continued losses for the foreseeable future with no guarantee of achieving profitability
- Dependent on ability to raise additional capital on acceptable terms
- Subject to regulatory uncertainties and potential delays in clinical development

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors related to its financial position and operations:

## Financial Losses and Lack of Revenue
- The company has incurred substantial losses since inception, with net losses of $198.7 million, $200.1 million, and $157.4 million for 2024, 2023, and 2022 respectively
- An accumulated deficit of $743.0 million exists as of December 31, 2024
- No approved products exist and no revenue has been generated from product sales
- Losses are expected to continue for the foreseeable future with no assurance of achieving profitability

## Need for Substantial Additional Capital
- The company currently lacks a credit facility or committed sources of capital
- Significant funding will be required for ongoing clinical trials, preclinical activities, and potential commercialization efforts
- If unable to raise capital on acceptable terms, the company may be forced to delay, reduce, or eliminate research and development programs
- Capital depletion could occur sooner than currently projected

## Product Development Uncertainties
- Clinical development of the first product candidate only began in 2022, with many years potentially needed before commercialization
- No clinical trials have been completed
- Success requires effectiveness in multiple challenging activities including completing trials, obtaining regulatory approvals, manufacturing, and achieving market acceptance
- Even if products are approved, there is no assurance of generating sufficient revenue for profitability

## Operational and Market Risks
- Operating expenses are expected to increase substantially
- Future revenue will depend on market size, pricing, reimbursement coverage, and competitive factors
- The addressable patient population may be smaller than estimated, or approved indications may be narrower than expected

## Pre-written sections (judge input)

### Financial Health

The company's market capitalization is not available. As of the latest filing date, the stock price is not provided. The P/E ratio is not calculable without earnings data. Revenue and profit margin details are also unavailable. The condensed consolidated balance sheet shows total assets of $614,163K as of March 31, 2025, down slightly from $647K at the end of the previous year. Given the significant risk factors disclosed in the SEC filings, investors should exercise caution.

### Recent Developments

Verve Therapeutics filed its Q1 2025 10-Q on May 14, 2025, revealing a cash position of $96.6 million as of March 31, 2025, down from $172.6 million at year-end 2024, indicating accelerated cash burn as the company advances its pipeline. The company maintains $400.5 million in marketable securities, providing a runway for ongoing operations and clinical development. The February 2025 10-K filing highlighted material risk factors that could adversely affect business operations and stock performance, suggesting investors should carefully evaluate execution risks. With cash declining significantly in the first quarter, investors should monitor upcoming milestones and partnership developments to assess the sustainability of the company's financial position and clinical progress.

### SEC Filing Highlights

VERV reported a net loss of $198.7 million in 2024 with an accumulated deficit of $743.0 million, reflecting its pre-commercial stage as a gene-editing company with no approved products or product revenue to date. The company maintains a cash position of $524.3 million as of December 31, 2024, plus a $20.0 million milestone payment from Eli Lilly received in February 2025, which management estimates will fund operations into mid-2027. VERV is advancing multiple clinical programs including the Heart-2 Phase 1b trial (VERVE-102) and Pulse-1 Phase 1b trial (VERVE-201), while evaluating next steps for its Heart-1 program. The company expects substantial increases in operating expenses as trials progress and will require significant additional capital for regulatory approvals, manufacturing scale-up, and commercialization. Management anticipates continued losses for the foreseeable future with no guarantee of profitability, making future funding availability a critical risk factor.

### Risk Factors

- **Substantial Financial Losses and Lack of Revenue:** The company has incurred significant losses and has not yet generated any revenue from product sales. Continued losses and the absence of a clear path to profitability pose a major risk.
- **Need for Substantial Additional Capital:** The company requires significant funding for ongoing operations and development. Failure to secure adequate capital could lead to delays or termination of critical programs.

## Audited (Exec Summary + Outlook)

### Executive Summary
Verve Therapeutics is a pre-commercial gene-editing company with no approved products or product revenue, carrying an accumulated deficit of $743.0 million and total assets of $614,163K as of March 31, 2025, as it advances a pipeline targeting cardiovascular disease through base-editing technology. The stock is notable now because the company is simultaneously burning cash at an accelerated pace — with cash declining from $172.6 million to $96.6 million in a single quarter — while advancing two active Phase 1b trials and relying on a management-estimated operational runway that extends only into mid-2027. The single most important near-term variable is clinical data readouts from the Heart-2 (VERVE-102) and Pulse-1 (VERVE-201) trials, as positive results would materially strengthen the company's ability to raise additional capital or attract partnership interest, while disappointing data could jeopardize both programs and the broader investment thesis.

### Outlook
The directional outlook for VERV is **cautious**, though not without potential catalysts that could shift the view. The primary tailwind is the company's existing relationship with Eli Lilly — evidenced by the $20.0 million milestone payment received in February 2025 — and the active advancement of two Phase 1b trials, which together signal that the scientific and partnership foundation remains intact. However, headwinds are significant: cash burn is accelerating, the operational runway extends only into mid-2027 by management's own estimate, and the company has no product revenue to offset mounting losses. Investors should closely watch clinical data emerging from the Heart-2 and Pulse-1 trials, the pace of cash consumption relative to the $400.5 million in marketable securities, any expansion or deepening of the Eli Lilly partnership or new partnership announcements, and the company's ability to access capital markets on favorable terms. The thesis would strengthen meaningfully on positive and differentiated clinical data, a new or expanded partnership providing non-dilutive capital, or a moderation in cash burn. Conversely, clinical setbacks, an inability to raise additional capital, or further acceleration in operating expenses without corresponding pipeline progress would weaken the thesis considerably.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "accumulated deficit of $743.0 million"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors both explicitly state "Accumulated deficit stands at $743.0 million as of December 31, 2024."

---

CLAIM: "total assets of $614,163K as of March 31, 2025"
LABEL: SUPPORTED
REASON: The 10-Q summary in the raw source data explicitly shows "Total assets $ 614,163" as of March 31, 2025.

---

CLAIM: "cash declining from $172.6 million to $96.6 million in a single quarter"
LABEL: SUPPORTED
REASON: The 10-Q balance sheet shows cash and cash equivalents of $96,554K (≈$96.6M) as of March 31, 2025 and $172,560K (≈$172.6M) as of December 31, 2024, confirming the single-quarter decline; the Recent Developments pre-written section also states these figures explicitly.

---

CLAIM: "two active Phase 1b trials"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly names two active Phase 1b trials: Heart-2 Phase 1b (VERVE-102) and Pulse-1 Phase 1b (VERVE-201).

---

CLAIM: "operational runway that extends only into mid-2027"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights states "Management estimates existing capital will fund operations into mid-2027," and the SEC Filing Highlights pre-written section repeats this verbatim.

---

CLAIM: "Heart-2 (VERVE-102) and Pulse-1 (VERVE-201) trials"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly names both trials with these exact designations: "Heart-2 Phase 1b (VERVE-102)" and "Pulse-1 Phase 1b (VERVE-201)."

---

**OUTLOOK**

---

CLAIM: "$20.0 million milestone payment received in February 2025"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "an additional $20.0 million milestone payment received from Eli Lilly in February 2025," and the SEC Filing Highlights pre-written section repeats this.

---

CLAIM: "two Phase 1b trials" (in Outlook)
LABEL: SUPPORTED
REASON: Same basis as above — Heart-2 Phase 1b (VERVE-102) and Pulse-1 Phase 1b (VERVE-201) are both explicitly named in the source data.

---

CLAIM: "operational runway extends only into mid-2027 by management's own estimate"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights states "Management estimates existing capital will fund operations into mid-2027," directly attributing this estimate to management.

---

CLAIM: "$400.5 million in marketable securities"
LABEL: SUPPORTED
REASON: The 10-Q balance sheet in the raw source data shows "Marketable securities 400,523" (thousands) as of March 31, 2025, which rounds to $400.5 million; the Recent Developments pre-written section also states "$400.5 million in marketable securities."

---

CLAIM: "Heart-2 and Pulse-1 trials" (in Outlook, as watch items)
LABEL: SUPPORTED
REASON: Both trial names are explicitly present in the RAG SEC Highlights and the SEC Filing Highlights pre-written section.

---

CLAIM: "Eli Lilly partnership" / "expansion or deepening of the Eli Lilly partnership"
LABEL: SUPPORTED
REASON: Eli Lilly is explicitly named in the RAG SEC Highlights as the source of the $20.0 million milestone payment, establishing the existence of a relationship; the claim does not assert specific terms beyond what is in the source.

---

**SUMMARY OF FINDINGS**

All quantitative and forward-looking claims in the Executive Summary and Outlook are SUPPORTED by the source data. No figures were found to be UNSUPPORTED or INFERENCE-only. The brief accurately reflects the figures present in the raw source data and pre-written sections without introducing extraneous numbers, fabricated metrics, or period mismatches.
