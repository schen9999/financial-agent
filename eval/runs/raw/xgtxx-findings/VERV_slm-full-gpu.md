# VERV — slm-full-gpu

## Metadata

ticker: VERV
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 9cfa70d74b4205695fce43765882373cc01fcf4bee54a05a60d5568dc94b07d5
slm_endpoint: slm-gpu
slm_url: http://132.145.161.150:30880
slm_served_name: qwen3.6-35b-a3b-q4km
slm_artifact: ggml-org/Qwen3.6-35B-A3B-GGUF@baec3ebee244827cda0f4557eafa8b28f7545fa6:Qwen3.6-35B-A3B-Q4_K_M.gguf sha256:671e47e0ec53c665d048b98c3ecbfd5236b5ca9c3e02ed19fc8f81f7b85140c7
slm_build: b11347-5fc4f3c8c
slm_model_path: /models/Qwen3.6-35B-A3B-Q4_K_M.gguf
slm_model_ftype: Q4_K - Medium
slm_total_slots: 4
slm_n_ctx: 32768
slm_n_params: 34660610688
slm_model_size_bytes: 20408576512
slm_thinking: off
slm_sampling: {"planner": {"chat_template_kwargs": {"enable_thinking": false}, "dry_multiplier": 0.0, "frequency_penalty": 0.0, "max_tokens": 1024, "min_p": 0.0, "presence_penalty": 0.0, "repeat_penalty": 1.0, "temperature": 0.0, "top_k": 20, "top_n_sigma": -1.0, "top_p": 0.8, "typical_p": 1.0, "xtc_probability": 0.0}, "rag": {"chat_template_kwargs": {"enable_thinking": false}, "dry_multiplier": 0.0, "frequency_penalty": 0.0, "max_tokens": 2048, "min_p": 0.0, "presence_penalty": 0.0, "repeat_penalty": 1.0, "temperature": 0.1, "top_k": 20, "top_n_sigma": -1.0, "top_p": 0.8, "typical_p": 1.0, "xtc_probability": 0.0}, "react": {"chat_template_kwargs": {"enable_thinking": false}, "dry_multiplier": 0.0, "frequency_penalty": 0.0, "max_tokens": 1024, "min_p": 0.0, "presence_penalty": 0.0, "repeat_penalty": 1.0, "temperature": 0.0, "top_k": 20, "top_n_sigma": -1.0, "top_p": 0.8, "typical_p": 1.0, "xtc_probability": 0.0}, "section": {"chat_template_kwargs": {"enable_thinking": false}, "dry_multiplier": 0.0, "frequency_penalty": 0.0, "max_tokens": 768, "min_p": 0.0, "presence_penalty": 0.0, "repeat_penalty": 1.0, "temperature": 0.1, "top_k": 20, "top_n_sigma": -1.0, "top_p": 0.8, "typical_p": 1.0, "xtc_probability": 0.0}, "synthesis": {"chat_template_kwargs": {"enable_thinking": false}, "dry_multiplier": 0.0, "frequency_penalty": 0.0, "max_tokens": 4096, "min_p": 0.0, "presence_penalty": 0.0, "repeat_penalty": 1.0, "temperature": 0.2, "top_k": 20, "top_n_sigma": -1.0, "top_p": 0.8, "typical_p": 1.0, "xtc_probability": 0.0}}
llm_calls: 7
llm_endpoints: slm-gpu
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 758, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 27.009, "latency_s_total": 27.009, "parse_failure": 0, "prompt_tokens": 2651, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 532, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.458, "latency_s_total": 17.458, "parse_failure": 0, "prompt_tokens": 2399, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 159, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 14.001, "latency_s_total": 14.001, "parse_failure": 0, "prompt_tokens": 636, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 163, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 16.58, "latency_s_total": 16.58, "parse_failure": 0, "prompt_tokens": 630, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 130, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.39, "latency_s_total": 19.39, "parse_failure": 0, "prompt_tokens": 601, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 170, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 20.319, "latency_s_total": 20.319, "parse_failure": 0, "prompt_tokens": 835, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 952, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 25.764, "latency_s_total": 25.764, "parse_failure": 0, "prompt_tokens": 1616, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
[From Pinecone cache] Based on the provided risk factors from the Annual Report on Form 10-K for VERV, here are the key takeaways regarding the company's financial position, operational status, and future outlook:

**Financial Performance and Losses**
*   **Significant Operating Losses:** The company has incurred substantial net losses since inception, reporting $198.7 million for the year ended December 31, 2024, $200.1 million for 2023, and $157.4 million for 2022.
*   **Accumulated Deficit:** As of December 31, 2024, the company had an accumulated deficit of $743.0 million.
*   **No Revenue:** The company has no approved products and has not generated any revenue from product sales. It expects to incur significant operating expenses and net losses for the foreseeable future.

**Funding and Capital Resources**
*   **Current Liquidity:** As of December 31, 2024, the company held $524.3 million in cash, cash equivalents, and marketable securities. Additionally, in February 2025, the company received a $20.0 million milestone payment from Eli Lilly and Company (Lilly) under the Lp(a) program.
*   **Funding Horizon:** Management estimates that existing resources will fund operating expenses and capital requirements into mid-2027. However, this estimate is based on assumptions that may prove incorrect, and the company could deplete resources sooner than expected.
*   **Need for Additional Capital:** The company currently has no credit facility or committed sources of capital. If unable to raise sufficient funds on acceptable terms, the company may be forced to delay, limit, reduce, or terminate research and development programs or commercialization efforts.

**Operational Status and Clinical Trials**
*   **No Approved Products:** The company has not yet received regulatory approval for any of its product candidates.
*   **Active Clinical Programs:** The company is conducting ongoing Phase 1b clinical trials for VERVE-102 (Heart-2) and VERVE-201 (Pulse-1), and has a planned Phase 2 clinical trial for its PCSK9 program. It is also evaluating next steps for the VERVE-101 (Heart-1) Phase 1b trial.
*   **Expenses:** Operating expenses are expected to increase substantially due to ongoing and planned clinical trials, preclinical development, intellectual property maintenance, and potential commercialization infrastructure.

**Collaborations and Milestone Payments**
*   **Lilly Agreement:** The company has a Research and Collaboration Agreement with Eli Lilly and Company, which became effective in July 2023. This includes potential milestone payments and research services.
*   **Other Agreements:** The company has license agreements with Acuitas Therapeutics, The Broad Institute/Harvard, and Novartis, which may trigger milestone or success payments.

**Risks and Uncertainties**
*   **Commercialization Challenges:** Even if marketing approval is obtained, the company may not achieve commercial success, and revenues may not be sufficient to sustain operations.
*   **Regulatory and Development Risks:** The process of identifying and developing product candidates is time-consuming, expensive, and uncertain. Delays in clinical trials, additional regulatory requirements, or intellectual property challenges could increase expenses and adversely affect the business.
*   **Market Conditions:** Disruptions in global financial markets could reduce the company's ability to access capital, potentially negatively affecting liquidity.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Financial Position and Need for Capital:** The company has incurred significant losses since inception, with net losses of $198.7 million, $200.1 million, and $157.4 million for the years ended December 31, 2024, 2023, and 2022, respectively. As of December 31, 2024, the accumulated deficit was $743.0 million. The company has no approved products, has generated no revenue from product sales, and expects to incur losses for the foreseeable future.
*   **Lack of Revenue and Profitability:** The company has never generated revenue from product sales and may never achieve or maintain profitability. It expects that it will be many years, if ever, before a product candidate is ready for commercialization.
*   **Substantial Additional Funding Requirements:** The company expects to incur substantial additional research and development, commercialization, and public company operating expenses. It currently has no credit facility or committed sources of capital. If unable to raise capital when needed, the company may be forced to delay, reduce, or eliminate product development programs or commercialization efforts.
*   **Uncertainty of Product Development:** Identifying potential product candidates and conducting preclinical testing and clinical trials is time-consuming, expensive, and uncertain. There is no assurance that the company will successfully complete clinical trials, obtain regulatory approvals, or achieve commercial success.
*   **Dependence on Market Factors:** Revenue will depend on market size, accepted pricing, coverage and reimbursement, and commercial rights. If the addressable patient population is smaller than estimated, indications are narrower than expected, or competition narrows the treatment population, significant revenue may not be generated.
*   **Operational and External Risks:** Risks include unforeseen expenses, difficulties, and delays in development; the need to manage intellectual property costs and claims; and the potential disruption of global financial markets affecting the ability to access capital. Additionally, fundraising efforts may divert management from day-to-day activities.
*   **Cash Runway Assumptions:** While the company had $524.3 million in cash, cash equivalents, and marketable securities as of December 31, 2024, and received a $20.0 million milestone payment in February 2025, this estimate to fund operations into mid-2027 is based on assumptions that may prove incorrect, potentially leading to a need for additional funding sooner than planned.

## Pre-written sections (judge input)

### Financial Health

Verve Therapeutics, Inc. (VERV) maintains a robust liquidity position with $96.6 million in cash and cash equivalents alongside $400.5 million in marketable securities as of March 31, 2025. Total assets stand at $614.2 million, reflecting a slight decrease from $647 million at the end of 2024, primarily driven by reduced cash reserves. Specific data points for market capitalization, P/E ratio, revenue, and profit margin are not available in the provided filings, likely due to the company's pre-revenue or early-stage development status. The balance sheet indicates a strong cash runway, though detailed profitability metrics are currently absent from the disclosed financial statements.

### Recent Developments

Verve Therapeutics filed its 10-K annual report on February 27, 2025, and its 10-Q quarterly report on May 14, 2025, providing updated financial disclosures for investors. The most significant recent development is a substantial reduction in cash and cash equivalents, which fell from $172.6 million at the end of 2024 to $96.6 million as of March 31, 2025. Concurrently, the company increased its holdings in marketable securities to $400.5 million, indicating a strategic shift in liquidity management. These filings highlight ongoing operational risks and the need for careful monitoring of the company's burn rate and capital preservation strategies.

### SEC Filing Highlights
VERV reported a net loss of $198.7 million for 2024, maintaining its accumulated deficit at $743.0 million while generating no revenue from product sales. The company holds $524.3 million in cash and marketable securities, supplemented by a $20.0 million milestone payment from Eli Lilly in February 2025, which management estimates will fund operations into mid-2027. Despite this liquidity, VERV has no approved products and continues to advance candidates like VERVE-102 and VERVE-201 through Phase 1b trials, with expenses expected to rise substantially. The company lacks committed capital sources and faces significant risks regarding future funding needs, regulatory delays, and the uncertainty of achieving commercial success.

### Risk Factors

*   **Persistent Losses and Lack of Revenue:** The company has incurred significant net losses (accumulated deficit of $743.0 million as of Dec 2024), has never generated product revenue, and may never achieve profitability.
*   **Substantial Capital Requirements:** The company lacks committed capital sources and faces high R&D and operational costs; failure to raise necessary funds could force delays or termination of development programs.
*   **High Uncertainty in Product Development:** Success depends on completing time-consuming and expensive clinical trials and obtaining regulatory approvals, with no assurance of commercial viability or market acceptance.

## Audited (Exec Summary + Outlook)

### Executive Summary
Verve Therapeutics is a pre-revenue biotechnology company advancing gene-editing candidates like VERVE-102 and VERVE-201, supported by a liquidity position of $524.3 million in cash and marketable securities as of early 2025. The stock is notable now due to the company’s reliance on a $20.0 million milestone payment from Eli Lilly and its current Phase 1b trial progress, which must sustain investor confidence despite a $198.7 million net loss in 2024. The single most important near-term variable is the successful execution of clinical trials and the subsequent ability to secure additional capital or partnerships to bridge the gap to mid-2027.

### Outlook
The directional outlook for Verve Therapeutics is cautiously constructive, anchored by a defined cash runway extending into mid-2027 but heavily dependent on binary clinical outcomes. Key variables to monitor include the safety and efficacy data from the Phase 1b trials for VERVE-102 and VERVE-201, as well as the company’s ability to manage its burn rate amid rising operational expenses. The thesis would be strengthened by positive clinical readouts that validate the gene-editing platform and attract further partnership or licensing opportunities, while it would be weakened by adverse safety signals, regulatory delays, or indications that the current liquidity is insufficient to cover extended development timelines without dilutive financing.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

### EXECUTIVE SUMMARY

---

**CLAIM:** "a liquidity position of $524.3 million in cash and marketable securities as of early 2025"
**LABEL:** UNSUPPORTED
**REASON:** The $524.3 million figure is explicitly tied in the source data to **December 31, 2024** (year-end 2024), not "early 2025"; the actual early-2025 (March 31, 2025) figure from the 10-Q is $96.6M cash + $400.5M marketable securities = $497.1M, making the period qualifier "early 2025" factually incorrect for the $524.3M figure.

---

**CLAIM:** "a $20.0 million milestone payment from Eli Lilly"
**LABEL:** SUPPORTED
**REASON:** The RAG SEC Highlights and Risk Factors sections both explicitly state "the company received a $20.0 million milestone payment from Eli Lilly and Company (Lilly) under the Lp(a) program" in February 2025.

---

**CLAIM:** "a $198.7 million net loss in 2024"
**LABEL:** SUPPORTED
**REASON:** The RAG SEC Highlights, RAG Risk Factors, and SEC Filing Highlights pre-written section all explicitly state a net loss of $198.7 million for the year ended December 31, 2024.

---

**CLAIM:** "VERVE-102 and VERVE-201" (as named product milestones/candidates in Phase 1b trials)
**LABEL:** SUPPORTED
**REASON:** The RAG SEC Highlights explicitly states "the company is conducting ongoing Phase 1b clinical trials for VERVE-102 (Heart-2) and VERVE-201 (Pulse-1)," and the SEC Filing Highlights pre-written section confirms both candidates advancing through Phase 1b trials.

---

**CLAIM:** "bridge the gap to mid-2027"
**LABEL:** SUPPORTED
**REASON:** The RAG SEC Highlights and RAG Risk Factors both explicitly state "Management estimates that existing resources will fund operating expenses and capital requirements into mid-2027."

---

### OUTLOOK

---

**CLAIM:** "a defined cash runway extending into mid-2027"
**LABEL:** SUPPORTED
**REASON:** Directly stated in both RAG sections: "Management estimates that existing resources will fund operating expenses and capital requirements into mid-2027."

---

**CLAIM:** "Phase 1b trials for VERVE-102 and VERVE-201"
**LABEL:** SUPPORTED
**REASON:** The RAG SEC Highlights explicitly confirms "ongoing Phase 1b clinical trials for VERVE-102 (Heart-2) and VERVE-201 (Pulse-1)," consistent with the SEC Filing Highlights pre-written section.

---

**CLAIM:** "rising operational expenses"
**LABEL:** SUPPORTED
**REASON:** The RAG SEC Highlights explicitly states "Operating expenses are expected to increase substantially due to ongoing and planned clinical trials, preclinical development, intellectual property maintenance, and potential commercialization infrastructure," and the SEC Filing Highlights pre-written section echoes "expenses expected to rise substantially."

---

*No price targets, specific percentage thresholds, P/E ratios, or other quantitative forward-looking figures appear in the Outlook section beyond those audited above.*

---

### SUMMARY TABLE

| # | Claim | Label |
|---|-------|-------|
| 1 | $524.3M liquidity "as of early 2025" | UNSUPPORTED |
| 2 | $20.0M milestone payment from Eli Lilly | SUPPORTED |
| 3 | $198.7M net loss in 2024 | SUPPORTED |
| 4 | VERVE-102 and VERVE-201 in Phase 1b | SUPPORTED |
| 5 | Bridge to mid-2027 | SUPPORTED |
| 6 | Cash runway into mid-2027 (Outlook) | SUPPORTED |
| 7 | Phase 1b trials for VERVE-102 and VERVE-201 (Outlook) | SUPPORTED |
| 8 | Rising operational expenses | SUPPORTED |
