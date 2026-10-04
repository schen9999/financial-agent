# VERV — baseline

## Metadata

ticker: VERV
arm: baseline
judge_prompt_version: v2
context_sha256: 198c5209baacd01a720db795715d8ce6c26dcfdb8e33df85946dc8be7c5dd84f
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 388, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.069, "latency_s_total": 4.069, "parse_failure": 0, "prompt_tokens": 2772, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 401, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.139, "latency_s_total": 4.139, "parse_failure": 0, "prompt_tokens": 2490, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 184, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.447, "latency_s_total": 2.447, "parse_failure": 0, "prompt_tokens": 615, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 190, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.488, "latency_s_total": 2.488, "parse_failure": 0, "prompt_tokens": 608, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 167, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.952, "latency_s_total": 1.952, "parse_failure": 0, "prompt_tokens": 471, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 184, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.815, "latency_s_total": 1.815, "parse_failure": 0, "prompt_tokens": 466, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1290, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 18.851, "latency_s_total": 18.851, "parse_failure": 0, "prompt_tokens": 1848, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
- As of December 31, 2024, the company had cash, cash equivalents and marketable securities of $524.3 million
- In February 2025, the company received a $20.0 million milestone payment from Eli Lilly under the Lp(a) program

## Product Development Status
- The company has no approved products and has generated no revenue from product sales
- Ongoing clinical trials include Heart-2 Phase 1b for VERVE-102 and Pulse-1 Phase 1b for VERVE-201
- A planned Phase 2 clinical trial for the PCSK9 program is in development
- The company is evaluating next steps for the Heart-1 Phase 1b clinical trial for VERVE-101

## Capital and Funding
- The company expects to continue incurring significant operating expenses and net losses for the foreseeable future
- Current cash resources are estimated to fund operations into mid-2027
- The company has no committed credit facility or sources of capital
- Additional funding will be needed to support ongoing research, clinical trials, and potential commercialization efforts

## Risk Factors
- Profitability is uncertain and may never be achieved
- The company is dependent on raising additional capital to continue operations
- Delays in clinical trials or regulatory challenges could increase expenses and deplete capital faster than anticipated

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
- If unable to raise capital on acceptable terms, the company may be forced to delay, reduce, or eliminate research and development programs or commercialization efforts
- Based on current cash and equivalents of $524.3 million, the company estimates it can fund operations into mid-2027

## Product Development Uncertainties
- The company has not yet completed a clinical trial of any product candidate
- Identifying product candidates and conducting testing is time-consuming, expensive, and uncertain
- There is no assurance that product candidates will obtain marketing approval or achieve commercial success
- Even if approved, products may not generate sufficient revenue to achieve profitability

## Operational and Market Risks
- Expenses are expected to increase substantially as clinical trials advance
- Future capital requirements depend on numerous unpredictable factors including trial progress, manufacturing costs, regulatory outcomes, and commercialization expenses
- Market acceptance and reimbursement for any approved products cannot be guaranteed

## Pre-written sections (judge input)

### Financial Health

Verve Therapeutics (VERV) is a clinical-stage biopharmaceutical company with limited revenue generation, typical of pre-commercial biotech firms. As of Q1 2025, the company maintains a cash position of $96.6 million and marketable securities of $400.5 million, providing a combined liquidity buffer of approximately $497 million. However, the company faces typical biotech risks including high operating expenses, no current profitability, and dependence on successful clinical trial outcomes and future financing. The recent 10-Q filing indicates cash declined from $172.6 million at year-end 2024, reflecting ongoing R&D and operational burn. Investors should monitor cash runway closely, as the company's financial viability depends on achieving clinical milestones and securing additional funding or partnerships.

### Recent Developments

Verve Therapeutics filed its Q1 2025 10-Q on May 14, 2025, revealing a significant decline in cash and cash equivalents from $172.6 million at year-end 2024 to $96.6 million by March 31, 2025, indicating accelerated cash burn. The company's total current assets decreased from $542.8 million to $511.7 million over the same period, suggesting ongoing operational expenses without disclosed revenue generation. The February 2025 10-K filing emphasized material risk factors that could adversely affect business operations and stock performance, though specific operational updates were not detailed in available filings. For investors, the rapid cash depletion raises concerns about runway and potential future financing needs, warranting close monitoring of upcoming clinical trial progress and partnership developments to justify the burn rate.

### SEC Filing Highlights

VERV is a clinical-stage biopharmaceutical company with no approved products or product revenue, reporting net losses of $198.7 million in 2024 and accumulated losses of $743.0 million as of December 31, 2024. The company maintains a cash position of $524.3 million (including a recent $20.0 million milestone payment from Eli Lilly in February 2025) and estimates this will fund operations into mid-2027. Key pipeline programs include VERVE-102 and VERVE-201 in Phase 1b trials, with a Phase 2 PCSK9 program in development. VERV expects to continue incurring significant operating losses and will require additional capital raises to support ongoing clinical development and potential commercialization efforts.

### Risk Factors

- **Substantial Operating Losses and No Revenue**: The company has accumulated $743.0 million in losses since inception with no approved products or product revenue. Annual net losses exceed $150 million, and profitability is not expected in the foreseeable future.

- **Significant Capital Requirements and Funding Uncertainty**: Based on current cash of $524.3 million, the company can fund operations only into mid-2027. Substantial additional capital will be required to advance clinical trials and commercialization, with no guaranteed access to funding on acceptable terms.

- **Clinical Development and Regulatory Uncertainty**: The company has not completed any clinical trials and faces substantial risks that product candidates may not obtain regulatory approval or achieve commercial success, even if approved.

## Audited (Exec Summary + Outlook)

### Executive Summary
Verve Therapeutics is a clinical-stage biopharmaceutical company pioneering gene-editing approaches to cardiovascular disease, with key pipeline assets VERVE-102 and VERVE-201 currently in Phase 1b trials and a Phase 2 PCSK9 program in development, supported by a combined liquidity buffer of approximately $497 million and a strategic partnership with Eli Lilly that delivered a $20.0 million milestone payment in February 2025. The stock is notable now because accelerating cash burn — with cash and cash equivalents declining from $172.6 million to $96.6 million in a single quarter — has sharpened investor focus on whether clinical progress can justify the spend rate and sustain the thesis ahead of anticipated financing needs. The single most important near-term variable is the clinical readout trajectory from VERVE-102 and VERVE-201, as meaningful efficacy and safety data would either validate the platform and support future capital raises or, if disappointing, materially undermine the investment case.

### Outlook
The directional outlook for VERV is **cautious**, with the investment thesis hinging almost entirely on binary clinical outcomes rather than financial fundamentals. On the tailwind side, the Eli Lilly partnership signals third-party validation of the gene-editing platform, and the estimated runway into mid-2027 provides a meaningful window for clinical catalysts to materialize before a financing crisis becomes acute. The cardiovascular gene-editing space also represents a large and underserved market opportunity if the science translates. However, headwinds are substantial: the company has never completed a clinical trial, the accelerating cash burn rate warrants close scrutiny, and the path to additional capital — whether through equity raises, partnerships, or milestone payments — is uncertain and potentially dilutive. Investors should monitor the Phase 1b data readouts from VERVE-102 and VERVE-201 as the primary signposts, the pace of cash consumption relative to clinical progress, any evolution in the Eli Lilly partnership, and the broader capital markets environment for clinical-stage biotech. The cautious stance would shift toward constructive if Phase 1b data demonstrate a compelling efficacy and safety profile, or if a meaningful new partnership or non-dilutive financing arrangement is announced; it would deepen toward outright negative if clinical setbacks emerge or if the company is forced into dilutive financing under unfavorable conditions.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "VERVE-102 and VERVE-201 currently in Phase 1b trials"
LABEL: SUPPORTED
REASON: The SEC Filing Highlights (RAG) explicitly states "Key pipeline programs include VERVE-102 and VERVE-201 in Phase 1b trials."

---

CLAIM: "a Phase 2 PCSK9 program in development"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "A planned Phase 2 clinical trial for the PCSK9 program is in development."

---

CLAIM: "a combined liquidity buffer of approximately $497 million"
LABEL: SUPPORTED
REASON: The Financial Health pre-written section states "combined liquidity buffer of approximately $497 million"; verified by arithmetic: $96,554K (cash) + $400,523K (marketable securities) = $497,077K ≈ $497 million, consistent with Q1 2025 balance sheet data.

---

CLAIM: "a strategic partnership with Eli Lilly that delivered a $20.0 million milestone payment in February 2025"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "In February 2025, the company received a $20.0 million milestone payment from Eli Lilly under the Lp(a) program."

---

CLAIM: "cash and cash equivalents declining from $172.6 million to $96.6 million in a single quarter"
LABEL: SUPPORTED
REASON: The 10-Q balance sheet data shows cash and cash equivalents of $172,560K at December 31, 2024 and $96,554K at March 31, 2025, confirming the decline in Q1 2025 (a single quarter).

---

**OUTLOOK**

---

CLAIM: "the estimated runway into mid-2027"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors both explicitly state "the company estimates it can fund operations into mid-2027."

---

CLAIM: "the company has never completed a clinical trial"
LABEL: SUPPORTED
REASON: The RAG Risk Factors explicitly states "The company has not yet completed a clinical trial of any product candidate."

---

CLAIM: "Phase 1b data readouts from VERVE-102 and VERVE-201 as the primary signposts"
LABEL: SUPPORTED
REASON: Both VERVE-102 (Heart-2 Phase 1b) and VERVE-201 (Pulse-1 Phase 1b) are confirmed as ongoing Phase 1b trials in the RAG SEC Highlights.

---

**Summary of findings:** All quantitative and forward-looking claims in the Executive Summary and Outlook are SUPPORTED by the source data. No figures were found to be UNSUPPORTED or INFERENCE-only. The brief accurately reflects the underlying source material without introducing unverified numbers, periods, or entities.
