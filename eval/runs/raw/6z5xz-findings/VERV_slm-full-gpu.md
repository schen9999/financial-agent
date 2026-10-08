# VERV — slm-full-gpu

## Metadata

ticker: VERV
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 2665b4ddea60f6c934dd624246630ce3467eaab045c7d6cd970d845866508ace
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 697, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 23.822, "latency_s_total": 23.822, "parse_failure": 0, "prompt_tokens": 2651, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 480, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 14.688, "latency_s_total": 14.688, "parse_failure": 0, "prompt_tokens": 2399, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 182, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 10.727, "latency_s_total": 10.727, "parse_failure": 0, "prompt_tokens": 636, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 180, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 11.566, "latency_s_total": 11.566, "parse_failure": 0, "prompt_tokens": 630, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 194, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 15.321, "latency_s_total": 15.321, "parse_failure": 0, "prompt_tokens": 549, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 188, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.408, "latency_s_total": 17.408, "parse_failure": 0, "prompt_tokens": 774, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1083, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 31.171, "latency_s_total": 31.171, "parse_failure": 0, "prompt_tokens": 1860, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
[From Pinecone cache] Based on the provided risk factors from the Annual Report on Form 10-K for VERV, the key takeaways regarding the company's financial position and operational outlook are as follows:

**Financial Performance and Losses**
*   **Significant Operating Losses:** The company has incurred substantial net losses since inception, reporting $198.7 million for 2024, $200.1 million for 2023, and $157.4 million for 2022.
*   **Accumulated Deficit:** As of December 31, 2024, the company had an accumulated deficit of $743.0 million.
*   **No Revenue:** The company has no approved products and has not generated any revenue from product sales. It expects to incur significant operating expenses and net losses for the foreseeable future.

**Funding and Capital Resources**
*   **Current Liquidity:** As of December 31, 2024, the company held $524.3 million in cash, cash equivalents, and marketable securities. Additionally, in February 2025, the company received a $20.0 million milestone payment from Eli Lilly and Company (Lilly) under the Lp(a) program.
*   **Funding Horizon:** Management estimates that existing resources will fund operating expenses and capital expenditures into mid-2027. However, this estimate relies on assumptions that may prove incorrect, and the company could deplete resources sooner than expected.
*   **Need for Additional Capital:** The company currently has no credit facility or committed sources of capital. If unable to raise sufficient funds on acceptable terms, the company may be forced to delay, limit, reduce, or terminate research and development programs or commercialization efforts.

**Operational Expenses and Drivers**
*   **Increasing Costs:** Expenses are expected to increase substantially due to ongoing and planned clinical trials, including the Heart-2 Phase 1b trial of VERVE-102, the Pulse-1 Phase 1b trial of VERVE-201, and a planned Phase 2 clinical trial for the PCSK9 program.
*   **Key Cost Drivers:** Future expenses will be driven by:
    *   Clinical trials and preclinical development for various product candidates.
    *   Milestone payments to collaborators, including Lilly, Acuitas Therapeutics, The Broad Institute, Harvard, and Novartis.
    *   Intellectual property maintenance, enforcement, and defense.
    *   Regulatory approvals and post-approval requirements, such as cardiovascular outcomes trials (CVOT).
    *   Establishing commercial-scale manufacturing and sales infrastructure.
    *   Costs associated with operating as a public company.

**Strategic Risks**
*   **Uncertainty of Success:** Identifying and developing product candidates is time-consuming, expensive, and uncertain. There is no guarantee that the company will obtain marketing approval or achieve commercial success.
*   **Market and Economic Factors:** Disruptions in global financial markets could reduce the company's ability to access capital, potentially negatively affecting liquidity.
*   **Dependency on Collaborations:** The company relies on collaboration agreements, such as the Lilly Agreement effective July 2023, and the success of these partnerships will impact its financial position.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Financial Position and Need for Capital:** The company has incurred significant losses since inception, with net losses of $198.7 million, $200.1 million, and $157.4 million for the years ended December 31, 2024, 2023, and 2022, respectively. As of December 31, 2024, the accumulated deficit was $743.0 million. The company has no approved products, has generated no revenue from product sales, and expects to incur losses for the foreseeable future.
*   **Operational and Development Risks:** The company has no products approved for sale and has not yet completed a clinical trial of any product candidate. Pharmaceutical product development is time-consuming, expensive, and uncertain, with no assurance that the company will successfully identify, develop, or obtain regulatory approval for product candidates. Even if approved, there is no guarantee of commercial success or that revenues will be sufficient to sustain operations.
*   **Substantial Funding Requirements:** The company expects to incur substantial additional research and development, commercialization, and public company operating expenses. It currently has no credit facility or committed sources of capital. If the company cannot raise capital when needed or on acceptable terms, it may be forced to delay, reduce, limit, or terminate its research and development programs or commercialization efforts.
*   **Market and Revenue Uncertainty:** Revenue depends on factors such as market size, product pricing, coverage and reimbursement, and commercial rights. If the addressable patient population is smaller than estimated, indications are narrower than expected, or competition narrows the treatment population, the company may not generate significant revenue.
*   **Liquidity and Capital Access:** While the company had $524.3 million in cash, cash equivalents, and marketable securities as of December 31, 2024, and received a $20.0 million milestone payment in February 2025, it believes these resources will only fund operations into mid-2027. This estimate is based on assumptions that may prove incorrect, and the company could deplete its capital resources sooner than expected. Disruption in global financial markets could further reduce the ability to access capital.

## Pre-written sections (judge input)

### Financial Health

Verve Therapeutics, Inc. (VERV) maintains a robust liquidity position with $96.6 million in cash and cash equivalents alongside $400.5 million in marketable securities as of March 31, 2025. Total assets stand at $614.2 million, reflecting a slight decrease from $647 million at the end of 2024, primarily driven by operational expenditures. Specific metrics such as market capitalization, P/E ratio, and revenue are not explicitly detailed in the provided summary, though the company’s substantial cash reserves indicate a focus on sustaining operations and R&D efforts. The balance sheet structure suggests a pre-profitability biotech profile where capital preservation is critical for future growth milestones. Investors should monitor cash burn rates closely given the absence of reported profit margins or positive net income in the available data.

### Recent Developments

Verve Therapeutics filed its Annual Report on Form 10-K on February 27, 2025, and its Quarterly Report on Form 10-Q on May 14, 2025, providing updated financial disclosures for investors. The most recent 10-Q filing reveals a significant decline in cash and cash equivalents to $96.6 million as of March 31, 2025, down from $172.6 million at the end of 2024, indicating increased cash burn. Conversely, the company’s marketable securities portfolio grew to $400.5 million, suggesting a strategic shift in asset allocation or proceeds from recent financing activities. Investors should closely monitor these liquidity trends alongside the risk factors outlined in the filings to assess the company's runway and operational sustainability.

### SEC Filing Highlights
VERV reported a net loss of $198.7 million for 2024, maintaining an accumulated deficit of $743.0 million as the company has yet to generate revenue from product sales. Despite these losses, the firm holds $524.3 million in cash and equivalents, supplemented by a $20.0 million milestone payment from Eli Lilly in February 2025. Management estimates that existing resources will fund operations into mid-2027, though this projection assumes no disruptions in capital access or unexpected cost overruns. Future expenses are expected to rise substantially due to ongoing clinical trials for VERVE-102, VERVE-201, and the PCSK9 program, alongside milestone payments to collaborators. The company faces significant risks related to its ability to secure additional financing and achieve regulatory approval for its gene-editing candidates.

### Risk Factors

*   **History of Losses and No Revenue:** The company has incurred significant net losses since inception (accumulated deficit of $743.0 million as of Dec 2024), has no approved products, and has generated no revenue from product sales, with expectations of continued losses for the foreseeable future.
*   **Early-Stage Development and Regulatory Uncertainty:** The company has not yet completed any clinical trials for its product candidates; there is no assurance it will successfully identify, develop, or obtain regulatory approval for any products, nor guarantee commercial success if approved.
*   **Liquidity Constraints and Capital Needs:** While the company holds $524.3 million in cash and equivalents, these resources are projected to fund operations only into mid-2027. The company has no committed sources of capital and may be forced to delay or terminate programs if it cannot raise additional funds on acceptable terms.

## Audited (Exec Summary + Outlook)

### Executive Summary
Verve Therapeutics is a pre-revenue biotech company focused on developing gene-editing therapies for cardiovascular disease, supported by a partnership with Eli Lilly that included a $20.0 million milestone payment in February 2025. The stock is notable for its substantial liquidity position, holding $524.3 million in cash and equivalents, which management estimates will fund operations into mid-2027 despite a significant accumulated deficit of $743.0 million. The single most important near-term variable shaping the outcome is the successful execution and data readouts from ongoing clinical trials for VERVE-102, VERVE-201, and the PCSK9 program.

### Outlook
The directional outlook for Verve Therapeutics is cautiously constructive, anchored by a clear runway into mid-2027 that provides sufficient time to de-risk its pipeline without immediate pressure for dilutive capital raises. Key variables to monitor include the clinical data readouts for VERVE-102, VERVE-201, and the PCSK9 program, as well as the execution of the strategic partnership with Eli Lilly. A positive shift in the investment thesis would occur if clinical trials demonstrate robust efficacy and safety profiles, thereby validating the gene-editing platform and potentially triggering further milestone payments or partnership expansions. Conversely, the view would weaken significantly if trial results are inconclusive or if the company encounters unexpected operational hurdles that accelerate cash burn, necessitating earlier and potentially unfavorable financing rounds.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

### EXECUTIVE SUMMARY

---

**CLAIM:** "a partnership with Eli Lilly that included a $20.0 million milestone payment in February 2025"
**LABEL:** SUPPORTED
**REASON:** The RAG SEC Highlights, RAG Risk Factors, and SEC Filing Highlights pre-written section all explicitly state that "in February 2025, the company received a $20.0 million milestone payment from Eli Lilly and Company (Lilly) under the Lp(a) program."

---

**CLAIM:** "holding $524.3 million in cash and equivalents"
**LABEL:** UNSUPPORTED
**REASON:** The $524.3 million figure refers specifically to "cash, cash equivalents, and marketable securities" as of December 31, 2024 (per the RAG sources and SEC Filing Highlights); the Executive Summary labels it solely "cash and equivalents," which is an inaccurate characterization of the figure's composition and date — the actual cash and cash equivalents alone were $172.6 million at December 31, 2024, and $96.6 million at March 31, 2025.

---

**CLAIM:** "management estimates will fund operations into mid-2027"
**LABEL:** SUPPORTED
**REASON:** The RAG SEC Highlights, RAG Risk Factors, and SEC Filing Highlights pre-written section all explicitly state that "Management estimates that existing resources will fund operating expenses and capital expenditures into mid-2027."

---

**CLAIM:** "a significant accumulated deficit of $743.0 million"
**LABEL:** SUPPORTED
**REASON:** The RAG SEC Highlights, RAG Risk Factors, Risk Factors pre-written section, and SEC Filing Highlights all explicitly state the accumulated deficit was $743.0 million as of December 31, 2024.

---

**CLAIM:** "ongoing clinical trials for VERVE-102, VERVE-201, and the PCSK9 program"
**LABEL:** SUPPORTED
**REASON:** The RAG SEC Highlights explicitly names "the Heart-2 Phase 1b trial of VERVE-102, the Pulse-1 Phase 1b trial of VERVE-201, and a planned Phase 2 clinical trial for the PCSK9 program," and the SEC Filing Highlights pre-written section references all three programs.

---

### OUTLOOK

---

**CLAIM:** "a clear runway into mid-2027"
**LABEL:** SUPPORTED
**REASON:** The RAG SEC Highlights, RAG Risk Factors, and SEC Filing Highlights pre-written section all explicitly state management estimates existing resources will fund operations into mid-2027.

---

**CLAIM:** "clinical data readouts for VERVE-102, VERVE-201, and the PCSK9 program"
**LABEL:** SUPPORTED
**REASON:** All three programs are explicitly named in the RAG SEC Highlights and SEC Filing Highlights pre-written section as active clinical programs.

---

**CLAIM:** "the strategic partnership with Eli Lilly"
**LABEL:** SUPPORTED
**REASON:** The RAG SEC Highlights explicitly references "the Lilly Agreement effective July 2023" and Eli Lilly is named as a collaborator throughout the source data.

---

**CLAIM:** "potentially triggering further milestone payments or partnership expansions"
**LABEL:** UNSUPPORTED
**REASON:** No source data specifies the existence, structure, amount, or conditions of any additional milestone payments beyond the $20.0 million already received, nor any terms for partnership expansion; this forward-looking claim introduces specifics absent from the context.

---

### SUMMARY TABLE

| # | Claim | Label |
|---|-------|-------|
| 1 | $20.0 million milestone payment from Eli Lilly in February 2025 | SUPPORTED |
| 2 | $524.3 million in "cash and equivalents" | UNSUPPORTED |
| 3 | Fund operations into mid-2027 | SUPPORTED |
| 4 | Accumulated deficit of $743.0 million | SUPPORTED |
| 5 | Ongoing clinical trials for VERVE-102, VERVE-201, and PCSK9 program | SUPPORTED |
| 6 | Clear runway into mid-2027 | SUPPORTED |
| 7 | Clinical data readouts for VERVE-102, VERVE-201, and PCSK9 | SUPPORTED |
| 8 | Strategic partnership with Eli Lilly | SUPPORTED |
| 9 | Potentially triggering further milestone payments or partnership expansions | UNSUPPORTED |
