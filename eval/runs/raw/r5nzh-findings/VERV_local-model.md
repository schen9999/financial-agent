# VERV — local-model

## Metadata

ticker: VERV
arm: local-model
judge_prompt_version: v2
context_sha256: f56009acc3cba7434f3f6a70d55e9acfbacbdcd0db36d77b02ed46ad9f829a87
local_model_served_name: financial-lora-w4a16
local_model_dir: qwen-ft-w4a16
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
- The company has accumulated significant losses totaling $743.0 million as of December 31, 2024
- Net losses were $198.7 million in 2024, $200.1 million in 2023, and $157.4 million in 2022
- No approved products or product sales revenue to date
- Current cash, cash equivalents, and marketable securities total $524.3 million
- A $20.0 million milestone payment was received from Eli Lilly in February 2025

## Funding and Capital Requirements
- The company expects existing capital to fund operations into mid-2027
- Substantial additional funding will be needed to continue operations and advance development programs
- No committed credit facilities or external funding sources currently in place
- Primary financing has come from private placements, public stock offerings, and collaboration payments

## Operational Focus
- Multiple ongoing clinical trials including Heart-2 (VERVE-102), Pulse-1 (VERVE-201), and planned Phase 2 trials for the PCSK9 program
- Significant expenses anticipated for clinical development, regulatory approvals, manufacturing, and commercialization
- Active collaboration with Eli Lilly under agreements effective since July 2023
- Continued investment in base editing and gene editing technology development

## Risk Outlook
- Expectation of continued substantial operating losses for the foreseeable future
- Profitability is uncertain and may never be achieved
- Capital depletion could occur sooner than anticipated if operational plans change

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors related to its financial position and operations:

## Financial Losses and Lack of Revenue
- The company has incurred substantial losses since inception with no approved products for sale
- Net losses were $198.7 million, $200.1 million, and $157.4 million for 2024, 2023, and 2022 respectively
- An accumulated deficit of $743.0 million exists as of December 31, 2024
- No revenue has been generated from product sales to date

## Need for Additional Capital
- The company currently lacks a credit facility or committed sources of capital
- Substantial additional funding is required to continue operations, particularly for clinical trials and preclinical activities
- If unable to raise capital on acceptable terms, the company may be forced to delay, reduce, or eliminate research and development programs or commercialization efforts

## Product Development Uncertainties
- Identifying product candidates and conducting preclinical testing and clinical trials is time-consuming, expensive, and uncertain
- The company has not yet completed a clinical trial of any product candidate
- Many years may pass before any product candidate is ready for commercialization, if ever
- Even if products are approved, there is no assurance of commercial success or profitability

## Capital Depletion Risk
- While existing cash and marketable securities of $524.3 million are expected to fund operations into mid-2027, this estimate is based on assumptions that may prove incorrect
- The company could deplete capital resources sooner than expected

## Pre-written sections (judge input)

### Financial Health
The company reports $96,554 in cash and cash equivalents as of March 31, 2025. The company also carries out $400,523 in marketable securities as of the same date. Additionally, the company holds $3,255 in collaboration receivables as of the same date.

### Recent Developments

VERV filed its Q1 2025 10-Q on May 14, 2025, revealing a significant cash position decline from $172.6 million at year-end 2024 to $96.6 million by March 31, 2025, indicating accelerated cash burn as the company advances its pipeline. The company maintains a combined liquid position of approximately $497 million when including marketable securities, providing runway for ongoing operations and clinical development. The February 2025 10-K filing highlighted material risk factors that could adversely affect business operations and stock performance, suggesting investors should carefully monitor execution on clinical programs and partnership developments. For investors, the key concern is the burn rate trajectory and whether upcoming clinical milestones or collaboration announcements can validate the company's therapeutic approach and extend its cash runway.

### SEC Filing Highlights

VERV is a pre-revenue clinical-stage biotech company with accumulated losses of $743.0 million and net losses of $198.7 million in 2024, supported by $524.3 million in cash and equivalents. The company expects its existing capital to fund operations into mid-2027, with a $20.0 million milestone payment received from Eli Lilly in February 2025 under their ongoing collaboration. VERV is advancing multiple clinical programs including the Heart-2 trial for its lead PCSK9 base editing therapy and the Pulse-1 trial, but faces substantial ongoing losses and will require significant additional funding to complete development and achieve commercialization. The company anticipates continued operating losses for the foreseeable future, with profitability uncertain and dependent on successful clinical outcomes and regulatory approvals.

### Primary Risk Factors Disclosed

The company discloses several significant risk factors related to its financial position and operations:

#### Financial Losses and Lack of Revenue
- Since inception, the company has incurred substantial net losses of $198.7 million in 2024, $200.1 million in 2023, and $157.4 million in 2022.
- As of December 31, 2024, the company's accumulated deficit stands at $743.0 million.
- No revenue has been generated from product sales to date.

#### Need for Additional Capital
- The company currently lacks a credit facility or committed sources of capital.
- Substantial additional funding is required to continue operations, particularly for clinical trials and preclinical activities.
- If unable to raise capital on acceptable terms, the company may be forced to delay, reduce, or eliminate research and development programs or commercialization efforts.

#### Product Development Uncertainties
- Identifying product candidates and conducting preclinical testing and clinical trials is time-consuming, expensive, and uncertain.
- The company has not yet completed a clinical trial of any product candidate.
- Many years may pass before any product candidate is ready for commercialization, if ever.
- Even if products are approved, there is no assurance of commercial success or profitability.

## Audited (Exec Summary + Outlook)

### Executive Summary
Verve Therapeutics is a clinical-stage biotech company pioneering base editing therapies for cardiovascular disease, carrying an accumulated deficit of $743.0 million and no product revenue to date, yet supported by a combined liquid position of approximately $497 million and a validated partnership with Eli Lilly that delivered a $20.0 million milestone payment in February 2025. The stock is notable now because the company sits at an inflection point — advancing its Heart-2 and Pulse-1 trials while absorbing accelerating cash burn, creating a high-stakes window where clinical data and partnership developments will disproportionately drive valuation. The single most important near-term variable is whether readouts from the Heart-2 trial for its lead PCSK9 base editing therapy demonstrate sufficient efficacy and safety to validate the platform and attract the additional capital the company will ultimately require beyond its projected mid-2027 runway.

### Outlook
The directional outlook for VERV is **cautious**, with the potential to become constructive contingent on clinical execution. The primary tailwind is the company's differentiated base editing platform in a large and underserved cardiovascular market, reinforced by the credibility of the Eli Lilly collaboration and a capital runway that extends into mid-2027 — providing meaningful time for key data readouts. However, headwinds are substantial: the burn rate is accelerating, no clinical trial has been completed, and the company will require significant additional funding beyond its current runway with no committed credit facility in place. Investors should closely monitor the pace and trajectory of cash consumption quarter over quarter, the clinical progress and data quality emerging from the Heart-2 and Pulse-1 trials, any expansion or deepening of the Eli Lilly collaboration or announcement of new partnerships, and the broader capital markets environment for clinical-stage biotech, which will determine how favorably VERV can access future financing. Positive clinical signals from the Heart-2 trial — particularly on safety and durability of effect — would be the clearest catalyst to shift this view toward constructive, while a deterioration in burn rate, a clinical setback, or difficulty raising capital on acceptable terms would meaningfully deepen the cautious stance.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "accumulated deficit of $743.0 million"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights, RAG Risk Factors, and Pre-written SEC Filing Highlights section all explicitly state "accumulated deficit of $743.0 million as of December 31, 2024."

---

CLAIM: "combined liquid position of approximately $497 million"
LABEL: UNSUPPORTED
REASON: The Pre-written Recent Developments section states "approximately $497 million when including marketable securities," but the underlying source data shows cash of $96,554K + marketable securities of $400,523K = $497,077K as of March 31, 2025, which rounds to ~$497 million; however, the Pre-written Financial Health section incorrectly states the collaboration receivable figure as of December 31, 2024 ($3,255K) rather than the March 31, 2025 figure ($1,399K), and the 10-K RAG data separately cites $524.3 million (cash + marketable securities as of December 31, 2024). The $497M figure is arithmetically derivable from the Q1 2025 balance sheet figures ($96,554K + $400,523K = $497,077K ≈ $497M), but the Pre-written Recent Developments section introduces this figure with an error in its own narrative (it describes the cash decline to $96.6M correctly but then states "approximately $497 million" — which is consistent with the Q1 2025 data). On recomputation: $96,554 + $400,523 = $497,077 ≈ $497M. This is SUPPORTED by arithmetic from the source balance sheet data.
LABEL: SUPPORTED
REASON: Recomputed from Q1 2025 balance sheet: $96,554K (cash) + $400,523K (marketable securities) = $497,077K ≈ $497 million, consistent with the claim.

---

CLAIM: "$20.0 million milestone payment in February 2025"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "A $20.0 million milestone payment was received from Eli Lilly in February 2025," and this is echoed in the Pre-written SEC Filing Highlights section.

---

CLAIM: "mid-2027 runway"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Pre-written SEC Filing Highlights both explicitly state "the company expects existing capital to fund operations into mid-2027."

---

CLAIM: "Heart-2 and Pulse-1 trials" (named product milestones)
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly names "Heart-2 (VERVE-102)" and "Pulse-1 (VERVE-201)" as ongoing clinical trials.

---

CLAIM: "lead PCSK9 base editing therapy" (in context of Heart-2 trial)
LABEL: SUPPORTED
REASON: The Pre-written SEC Filing Highlights states "the Heart-2 trial for its lead PCSK9 base editing therapy," consistent with the RAG SEC Highlights which references "planned Phase 2 trials for the PCSK9 program."

---

**OUTLOOK**

---

CLAIM: "capital runway that extends into mid-2027"
LABEL: SUPPORTED
REASON: Explicitly stated in RAG SEC Highlights and Pre-written SEC Filing Highlights: "the company expects existing capital to fund operations into mid-2027."

---

CLAIM: "no clinical trial has been completed"
LABEL: SUPPORTED
REASON: The RAG Risk Factors and Pre-written Risk Factors section both explicitly state "The company has not yet completed a clinical trial of any product candidate."

---

CLAIM: "no committed credit facility in place"
LABEL: SUPPORTED
REASON: The RAG Risk Factors and Pre-written Risk Factors section both explicitly state "The company currently lacks a credit facility or committed sources of capital."

---

CLAIM: "Heart-2 and Pulse-1 trials" (Outlook section reference)
LABEL: SUPPORTED
REASON: Both trial names are explicitly present in the RAG SEC Highlights as ongoing clinical programs.

---

**Summary of findings:** All quantitative and forward-looking claims in the Executive Summary and Outlook are either directly supported by the source data or verified by arithmetic recomputation. No claims were found to be UNSUPPORTED or INFERENCE-only. The $497M liquid position figure, while introduced with some narrative inconsistency in the pre-written sections, is arithmetically verified from the Q1 2025 balance sheet data provided.
