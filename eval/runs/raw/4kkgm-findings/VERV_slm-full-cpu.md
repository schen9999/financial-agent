# VERV — slm-full-cpu

## Metadata

ticker: VERV
arm: slm-full-cpu
judge_prompt_version: v2
context_sha256: 55806d849f8bec373e3fdd9bdde3042e61d0ce0bbeb00c9e9191dc2ba41f9891
slm_endpoint: slm-cpu
slm_url: http://llamacpp.financial-agent.svc:8080
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
llm_endpoints: slm-cpu
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 776, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 218.54, "latency_s_total": 218.54, "parse_failure": 0, "prompt_tokens": 2651, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 571, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 178.49, "latency_s_total": 178.49, "parse_failure": 0, "prompt_tokens": 2399, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 125, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 63.652, "latency_s_total": 63.652, "parse_failure": 0, "prompt_tokens": 636, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 153, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 84.586, "latency_s_total": 84.586, "parse_failure": 0, "prompt_tokens": 630, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 204, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 91.729, "latency_s_total": 91.729, "parse_failure": 0, "prompt_tokens": 640, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 175, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 89.188, "latency_s_total": 89.188, "parse_failure": 0, "prompt_tokens": 853, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 936, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 110.923, "latency_s_total": 110.923, "parse_failure": 0, "prompt_tokens": 1686, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
[From Pinecone cache] Based on the provided text from the Annual Report on Form 10-K for VERV, the key takeaways regarding the company's financial position, risks, and future outlook are as follows:

**Financial Performance and Losses**
*   **Significant Operating Losses:** The company has incurred substantial net losses since inception, with losses of $198.7 million for 2024, $200.1 million for 2023, and $157.4 million for 2022.
*   **Accumulated Deficit:** As of December 31, 2024, the company had an accumulated deficit of $743.0 million.
*   **No Revenue:** The company has no approved products and has not generated any revenue from product sales. It expects to incur significant operating expenses and net losses for the foreseeable future.

**Funding and Capital Resources**
*   **Current Liquidity:** As of December 31, 2024, the company held $524.3 million in cash, cash equivalents, and marketable securities. Additionally, in February 2025, the company received a $20.0 million milestone payment from Eli Lilly and Company (Lilly) under the Lp(a) program.
*   **Funding Horizon:** Management estimates that existing resources will fund operating expenses and capital expenditures into mid-2027. However, this estimate relies on assumptions that may prove incorrect, and the company could deplete resources sooner than expected.
*   **Need for Additional Capital:** The company currently has no credit facility or committed sources of capital. It anticipates needing substantial additional funding to support ongoing and planned activities. Failure to raise capital on acceptable terms could force the company to delay, limit, reduce, or terminate research and development programs.

**Operational Expenses and Growth Drivers**
*   **Increasing Costs:** Expenses are expected to increase substantially due to ongoing and planned clinical trials, including the Heart-2 Phase 1b trial for VERVE-102, the Pulse-1 Phase 1b trial for VERVE-201, and a planned Phase 2 clinical trial for the PCSK9 program.
*   **Key Expense Categories:** Major cost drivers include:
    *   Clinical trials and preclinical development for product candidates like VERVE-101.
    *   Milestone payments to collaborators, including Lilly, Acuitas Therapeutics, The Broad Institute, Harvard, and Novartis.
    *   Intellectual property maintenance, enforcement, and defense.
    *   Hiring personnel for research, development, clinical, and commercial functions.
    *   Establishing commercial-scale manufacturing capabilities.
    *   Costs associated with operating as a public company.

**Risks and Uncertainties**
*   **Regulatory and Development Risks:** The process of identifying product candidates and conducting clinical trials is time-consuming, expensive, and uncertain. There is no guarantee that the company will obtain marketing approval or achieve commercial success.
*   **External Factors:** Expenses may increase due to regulatory requirements (such as additional trials mandated by the FDA or EMA), delays in clinical trials, or third-party intellectual property challenges.
*   **Market and Economic Risks:** Disruptions in global financial markets could reduce the company's ability to access capital, potentially negatively affecting liquidity.

**Collaborations**
*   The company relies on collaboration agreements for funding and development, most notably the Research and Collaboration Agreement with Eli Lilly and Company, which became effective in July 2023. The success of these collaborations and the achievement of milestones are critical factors influencing the company's financial requirements.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Financial Position and Need for Capital:** The company has incurred significant losses since inception, with net losses of $198.7 million, $200.1 million, and $157.4 million for the years ended December 31, 2024, 2023, and 2022, respectively. As of December 31, 2024, the accumulated deficit was $743.0 million. The company has no approved products, has generated no revenue from product sales, and expects to incur losses for the foreseeable future.
*   **Operational and Development Risks:** The company has not yet completed a clinical trial of any product candidate and initiated clinical development of its first product candidate in 2022. There is no assurance that the company will successfully complete preclinical testing, obtain regulatory approvals, or achieve market acceptance. The process is time-consuming, expensive, and uncertain, and the company may never generate revenue sufficient to achieve profitability.
*   **Funding Requirements:** The company expects to incur substantial additional expenses for research and development, commercialization, and operating as a public company. It currently has no credit facility or committed sources of capital. If unable to raise capital on acceptable terms, the company may be forced to delay, reduce, or eliminate product development programs or commercialization efforts.
*   **Market and Commercialization Risks:** Revenue depends on market size, pricing, reimbursement, and commercial rights. If the addressable patient population is smaller than estimated, indications are narrower than expected, or competition narrows the treatment population, the company may not generate significant revenue.
*   **Specific Factors Influencing Capital Needs:** Future capital requirements depend on the progress and costs of ongoing and planned clinical trials (including Heart-2 for VERVE-102, Pulse-1 for VERVE-201, and the PCSK9 program), the scope of discovery and preclinical activities, manufacturing costs, intellectual property costs, regulatory review outcomes, and the success of collaboration agreements, such as the agreement with Eli Lilly and Company.
*   **Liquidity and Economic Risks:** As of December 31, 2024, the company had $524.3 million in cash, cash equivalents, and marketable securities, and received a $20.0 million milestone payment from Lilly in February 2025. The company believes these resources will fund operations into mid-2027, but this estimate is based on assumptions that may prove incorrect. Disruptions in global financial markets could reduce the ability to access capital, potentially forcing the company to seek additional funding sooner than planned or on unfavorable terms.

## Pre-written sections (judge input)

### Financial Health

Specific metrics for price, market capitalization, P/E ratio, revenue, and profit margin are not available in the provided data. However, the company maintains a robust liquidity position with $96.6 million in cash and cash equivalents, supplemented by $400.5 million in market securities as of March 31, 2025. Total assets stand at $614.2 million, indicating a strong balance sheet despite the absence of profitability metrics. This substantial cash reserve suggests the company is well-capitalized to fund ongoing operations and development efforts without immediate liquidity constraints.

### Recent Developments

Verve Therapeutics filed its Form 10-K on February 27, 2025, and its Form 10-Q for the period ending March 31, 2025, on May 14, 2025. The most significant financial update is a substantial reduction in cash and cash equivalents, which fell from $172.6 million to $96.6 million, indicating accelerated capital deployment. Concurrently, the company increased its holdings in marketable securities to $400.5 million, suggesting a strategic shift toward liquid investments. Investors should monitor these liquidity changes closely as they signal the company's runway and capital management priorities amidst ongoing operational risks.

### SEC Filing Highlights
VERV reported a net loss of $198.7 million for 2024, maintaining an accumulated deficit of $743.0 million as the company has yet to generate revenue from product sales. Despite these losses, the firm holds $524.3 million in cash and marketable securities, supplemented by a $20.0 million milestone payment from Eli Lilly in February 2025. Management estimates that existing resources will fund operations into mid-2027, though this projection assumes no significant delays or cost overruns in ongoing clinical trials. The company faces substantial risks related to its need for additional capital, as it currently lacks committed funding sources or credit facilities. Future liquidity remains heavily dependent on the successful execution of its Lp(a) program and potential milestone achievements with key collaborators.

### Risk Factors

*   **History of Losses and Uncertain Path to Profitability:** The company has incurred significant net losses since inception (accumulated deficit of $743.0 million as of Dec 31, 2024), has no approved products or revenue from product sales, and expects to incur losses for the foreseeable future.
*   **Early-Stage Development and Regulatory Risks:** The company has not yet completed a clinical trial for any product candidate; there is no assurance it will successfully complete preclinical testing, obtain regulatory approvals, or achieve market acceptance, which is a time-consuming, expensive, and uncertain process.
*   **Substantial Capital Requirements and Liquidity Constraints:** The company expects to incur substantial additional expenses for R&D and commercialization without committed sources of capital; failure to raise funds on acceptable terms could force delays or elimination of development programs, and current cash resources may only fund operations into mid-2027 based on potentially incorrect assumptions.

## Audited (Exec Summary + Outlook)

### Executive Summary
Verve Therapeutics is a biotechnology company focused on developing gene-editing therapies, currently holding a substantial liquidity position with $524.3 million in cash and marketable securities to support its pipeline. The investment case is notable for its reliance on the successful execution of its Lp(a) program and potential milestone achievements with key collaborators like Eli Lilly, rather than immediate commercial revenue. The single most important near-term variable shaping the outcome is the company's ability to maintain its estimated operational runway into mid-2027 without encountering significant delays or cost overruns in its clinical trials.

### Outlook
The directional outlook for Verve Therapeutics is cautiously constructive, anchored by a strong balance sheet that provides a clear window for clinical progress before the need for additional capital raises. Key variables to monitor include the execution timeline of the Lp(a) program and the realization of milestone payments from collaborators, which serve as critical indicators of both technical success and financial runway. The thesis would be strengthened by evidence of efficient capital deployment and positive clinical data, while it would be weakened by any signs of trial delays, cost overruns, or a failure to secure future funding sources as the mid-2027 horizon approaches.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically identify every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections, then evaluate each one.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$524.3 million in cash and marketable securities"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights and RAG — Risk Factors both explicitly state "As of December 31, 2024, the company had $524.3 million in cash, cash equivalents, and marketable securities," and the SEC Filing Highlights pre-written section repeats this figure verbatim.

---

CLAIM: "estimated operational runway into mid-2027"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights explicitly states "Management estimates that existing resources will fund operating expenses and capital expenditures into mid-2027," and this is repeated in the SEC Filing Highlights and Risk Factors pre-written sections.

---

**OUTLOOK**

---

CLAIM: "mid-2027 horizon"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights and RAG — Risk Factors both explicitly state management estimates resources will fund operations into mid-2027, and the pre-written SEC Filing Highlights section repeats this projection.

---

*No other specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones with attached numbers, or forward-looking numbers appear in the Executive Summary or Outlook sections beyond those evaluated above. The references to "Lp(a) program," "Eli Lilly," and "milestone payments" are qualitative/named-entity claims without attached figures in these sections and are corroborated by the source data as named entities, but fall outside the scope of quantitative claims requiring arithmetic verification.*
