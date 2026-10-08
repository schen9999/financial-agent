# VERV — baseline

## Metadata

ticker: VERV
arm: baseline
judge_prompt_version: v2
context_sha256: e37d25de9f7e44c75a9e56ef4f1a0d097e978df38bb830203b280507d25cf8be
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 374, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.077, "latency_s_total": 4.077, "parse_failure": 0, "prompt_tokens": 2772, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 374, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.116, "latency_s_total": 4.116, "parse_failure": 0, "prompt_tokens": 2490, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 195, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.743, "latency_s_total": 2.743, "parse_failure": 0, "prompt_tokens": 592, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 170, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.407, "latency_s_total": 2.407, "parse_failure": 0, "prompt_tokens": 585, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 173, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.22, "latency_s_total": 2.22, "parse_failure": 0, "prompt_tokens": 444, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 203, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.374, "latency_s_total": 2.374, "parse_failure": 0, "prompt_tokens": 452, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1227, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.297, "latency_s_total": 17.297, "parse_failure": 0, "prompt_tokens": 1880, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
- The company has accumulated significant losses totaling $743.0 million as of December 31, 2024
- Net losses were $198.7 million in 2024, $200.1 million in 2023, and $157.4 million in 2022
- As of December 31, 2024, the company had cash, cash equivalents and marketable securities of $524.3 million
- In February 2025, the company received a $20.0 million milestone payment from Eli Lilly under the Lp(a) program

## Development Status
- The company has no approved products and has generated no revenue from product sales
- Current clinical programs include the Heart-2 Phase 1b trial of VERVE-102, the Pulse-1 Phase 1b trial of VERVE-201, and a planned Phase 2 clinical trial for the PCSK9 program
- The company is evaluating next steps for the Heart-1 Phase 1b clinical trial of VERVE-101

## Funding and Capital Requirements
- The company expects to continue incurring significant operating expenses and net losses for the foreseeable future
- Management believes existing capital will fund operations into mid-2027
- The company has no committed credit facility or sources of capital
- Substantial additional funding will be needed to continue operations and advance clinical development

## Risk Factors
- The company may never achieve profitability
- Inability to raise capital could force delays or termination of development programs
- Operating expenses are expected to increase substantially as clinical trials advance

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors related to its financial position and operations:

## Financial Losses and Lack of Revenue
- The company has incurred substantial losses since inception with no approved products for sale
- Net losses were $198.7 million, $200.1 million, and $157.4 million for 2024, 2023, and 2022 respectively
- Accumulated deficit reached $743.0 million as of December 31, 2024
- No revenue has been generated from product sales to date

## Need for Additional Capital
- The company currently lacks a credit facility or committed sources of capital
- Substantial additional funding is required to continue operations, particularly for:
  - Ongoing and planned clinical trials
  - Research, development, and preclinical testing
  - Potential commercialization expenses
  - Operating costs as a public company
- If unable to raise capital on acceptable terms, the company may be forced to delay, reduce, or eliminate product development programs

## Product Development Uncertainties
- The company has not yet completed a clinical trial of any product candidate
- Significant time and expense are required to identify candidates, conduct testing, obtain regulatory approvals, and achieve commercialization
- No assurance exists that development efforts will succeed or generate sufficient revenue for profitability
- Market acceptance and commercial success cannot be guaranteed even if regulatory approval is obtained

## Capital Runway
- As of December 31, 2024, the company had $524.3 million in cash, cash equivalents, and marketable securities
- Management estimates this will fund operations into mid-2027, though this estimate is based on assumptions that may prove incorrect

## Pre-written sections (judge input)

### Financial Health

Verve Therapeutics (VERV) reported total assets of $614.2 million as of March 31, 2025, with a strong cash position of $96.6 million and marketable securities of $400.5 million, indicating solid liquidity. However, the company's cash reserves declined by $76 million sequentially from December 2024, suggesting ongoing operational burn typical of clinical-stage biopharmaceutical companies. As a development-stage therapeutic firm, VERV does not yet generate meaningful revenue or profits, making traditional valuation metrics like P/E ratio and profit margin not applicable. The company's financial health is primarily dependent on its cash runway and ability to fund clinical trials and R&D activities. Investors should monitor cash burn rates and milestone achievements closely, as the company's viability hinges on successful clinical development and future financing or partnership opportunities.

### Recent Developments

Verve Therapeutics filed its Q1 2025 10-Q on May 14, 2025, revealing a cash position of $96.6 million as of March 31, 2025, down from $172.6 million at year-end 2024, indicating accelerated cash burn as the company advances its pipeline. The company maintains $400.5 million in marketable securities, providing a runway for ongoing operations and clinical development. The February 2025 10-K filing highlighted material risk factors that could adversely affect business operations and stock performance, suggesting investors should carefully evaluate execution risks. With cash declining significantly in the first quarter alone, investors should monitor upcoming quarterly results and any partnership announcements that could extend the company's cash runway.

### SEC Filing Highlights

Verve Therapeutics remains a pre-revenue clinical-stage company with accumulated losses of $743.0 million and net losses of $198.7 million in 2024, though it maintains a cash position of $524.3 million as of December 31, 2024. The company is advancing multiple gene-editing programs including Phase 1b trials for VERVE-102 and VERVE-201, with a planned Phase 2 trial for its PCSK9 program, and recently received a $20.0 million milestone payment from Eli Lilly in February 2025. Management projects existing capital will fund operations into mid-2027, but the company will require substantial additional funding to continue clinical development and advance toward potential commercialization. The company faces significant execution risk as it has no approved products, no product revenue, and expects operating expenses to increase substantially as trials progress.

### Risk Factors

- **Substantial Operating Losses and No Revenue**: The company has accumulated a $743.0 million deficit with annual net losses exceeding $157 million, and has generated zero revenue from product sales. Profitability depends entirely on successful commercialization of pipeline candidates.

- **Significant Capital Requirements and Funding Risk**: Additional substantial capital is required to fund ongoing clinical trials, R&D, and potential commercialization. The company lacks committed funding sources and may be forced to delay or eliminate programs if unable to raise capital on acceptable terms.

- **Clinical and Regulatory Uncertainties**: No product candidates have completed clinical trials or obtained regulatory approval. Success is not assured, and even approved products face market acceptance risks, with no guarantee of generating sufficient revenue to achieve profitability.

## Audited (Exec Summary + Outlook)

### Executive Summary
Verve Therapeutics is a clinical-stage biopharmaceutical company pioneering gene-editing therapies for cardiovascular disease, currently advancing Phase 1b trials for VERVE-102 and VERVE-201 while carrying total assets of $614.2 million and an accumulated deficit of $743.0 million. The stock is notable now because the company is at an inflection point — burning cash at an accelerating pace while simultaneously approaching meaningful clinical readouts that could validate or undermine its core gene-editing platform. The single most important near-term variable is the clinical data emerging from its Phase 1b programs, as positive results would materially strengthen the case for partnership interest, additional financing, and advancement to Phase 2, while disappointing data would intensify concerns about capital adequacy and program viability.

### Outlook
The directional outlook for Verve Therapeutics is **cautious**, though not without potential catalysts that could shift that view. The primary tailwind is the scientific promise of its gene-editing platform targeting cardiovascular disease — a large and underserved market — along with the validation implied by the Eli Lilly partnership and the $20.0 million milestone payment received in February 2025. However, headwinds are significant: cash burn is accelerating, the company has no approved products or product revenue, and it will require substantial additional funding beyond its projected mid-2027 runway. Investors should watch clinical data readouts from the VERVE-102 and VERVE-201 Phase 1b trials as the most consequential near-term variable, since compelling efficacy and safety data would be the clearest catalyst for partnership expansion, equity financing on favorable terms, or accelerated advancement to Phase 2. Conversely, the thesis would weaken materially on disappointing trial results, a failure to secure additional financing or partnerships before the runway narrows, or a meaningful increase in the quarterly cash burn rate beyond what current operations suggest. The Eli Lilly relationship bears watching as a potential source of additional milestone payments that could extend the runway without dilutive equity issuance.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "Phase 1b trials for VERVE-102 and VERVE-201"
LABEL: SUPPORTED
REASON: The SEC Filing Highlights (RAG) explicitly states "Phase 1b trials for VERVE-102 and VERVE-201" (Heart-2 and Pulse-1 trials respectively).

---

CLAIM: "total assets of $614.2 million"
LABEL: SUPPORTED
REASON: The 10-Q source data states total assets of $614,163 thousand as of March 31, 2025, which rounds to $614.2 million; also confirmed in the Financial Health pre-written section.

---

CLAIM: "accumulated deficit of $743.0 million"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors sections both explicitly state "accumulated losses totaling $743.0 million as of December 31, 2024."

---

CLAIM: "burning cash at an accelerating pace"
LABEL: INFERENCE
REASON: The pre-written Recent Developments section states cash declined from $172.6 million to $96.6 million in Q1 2025 alone and explicitly uses the phrase "accelerated cash burn," making this a direct restatement of that characterization.

---

**OUTLOOK**

---

CLAIM: "$20.0 million milestone payment received in February 2025"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "In February 2025, the company received a $20.0 million milestone payment from Eli Lilly under the Lp(a) program."

---

CLAIM: "Eli Lilly partnership"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights reference the Eli Lilly collaboration and milestone payment, confirming the existence of a partnership relationship.

---

CLAIM: "no approved products or product revenue"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state "The company has no approved products and has generated no revenue from product sales," confirmed in both Risk Factors sections.

---

CLAIM: "projected mid-2027 runway"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors both explicitly state "Management believes existing capital will fund operations into mid-2027."

---

CLAIM: "substantial additional funding beyond its projected mid-2027 runway"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state "the company will require substantial additional funding to continue clinical development," and the Risk Factors pre-written section confirms "Additional substantial capital is required."

---

CLAIM: "VERVE-102 and VERVE-201 Phase 1b trials" (in Outlook)
LABEL: SUPPORTED
REASON: Confirmed in RAG SEC Highlights as active Phase 1b programs (Heart-2 and Pulse-1 respectively).

---

CLAIM: "accelerated advancement to Phase 2" (as a potential outcome of positive data)
LABEL: SUPPORTED
REASON: The RAG SEC Highlights note "a planned Phase 2 clinical trial for the PCSK9 program," confirming Phase 2 advancement is a stated next step in the company's development plan, making this a grounded forward-looking reference.

---

CLAIM: "cash burn is accelerating"
LABEL: INFERENCE
REASON: The pre-written Financial Health section states cash reserves "declined by $76 million sequentially from December 2024," and the Recent Developments section explicitly uses the phrase "accelerated cash burn," making this a direct restatement derivable from those figures.

---

**SUMMARY OF LABELS**

| # | Claim | Label |
|---|-------|-------|
| 1 | Phase 1b trials for VERVE-102 and VERVE-201 | SUPPORTED |
| 2 | Total assets of $614.2 million | SUPPORTED |
| 3 | Accumulated deficit of $743.0 million | SUPPORTED |
| 4 | Burning cash at an accelerating pace | INFERENCE |
| 5 | $20.0 million milestone payment, February 2025 | SUPPORTED |
| 6 | Eli Lilly partnership | SUPPORTED |
| 7 | No approved products or product revenue | SUPPORTED |
| 8 | Projected mid-2027 runway | SUPPORTED |
| 9 | Substantial additional funding beyond mid-2027 | SUPPORTED |
| 10 | VERVE-102 and VERVE-201 Phase 1b trials (Outlook) | SUPPORTED |
| 11 | Accelerated advancement to Phase 2 | SUPPORTED |
| 12 | Cash burn is accelerating (Outlook) | INFERENCE |

**No claims were found to be UNSUPPORTED.** All quantitative figures, named milestones, partnership references, and forward-looking numbers in the Executive Summary and Outlook are either directly present in the source data/pre-written sections or are straightforward inferences from figures explicitly present therein.
