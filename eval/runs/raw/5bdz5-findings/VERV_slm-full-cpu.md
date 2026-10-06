# VERV — slm-full-cpu

## Metadata

ticker: VERV
arm: slm-full-cpu
judge_prompt_version: v2
context_sha256: 436801bfaf43b7367260c935dd0ebcd6c689095703ad1bbc14a37e63ad30725f
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 695, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 188.73, "latency_s_total": 188.73, "parse_failure": 0, "prompt_tokens": 2651, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 428, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 158.173, "latency_s_total": 158.173, "parse_failure": 0, "prompt_tokens": 2399, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 106, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 37.472, "latency_s_total": 37.472, "parse_failure": 0, "prompt_tokens": 616, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 148, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 49.267, "latency_s_total": 49.267, "parse_failure": 0, "prompt_tokens": 610, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 175, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 58.95, "latency_s_total": 58.95, "parse_failure": 0, "prompt_tokens": 497, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 184, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 82.457, "latency_s_total": 82.457, "parse_failure": 0, "prompt_tokens": 772, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 933, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 130.64, "latency_s_total": 130.64, "parse_failure": 0, "prompt_tokens": 1598, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
[From Pinecone cache] Based on the provided risk factors from the Annual Report on Form 10-K for VERV, the key takeaways regarding the company's financial position and operational outlook are as follows:

**Financial Performance and Losses**
*   **Significant Net Losses:** The company has incurred substantial operating losses since inception, with net losses of $198.7 million for 2024, $200.1 million for 2023, and $157.4 million for 2022.
*   **Accumulated Deficit:** As of December 31, 2024, the company had an accumulated deficit of $743.0 million.
*   **No Revenue:** The company has no approved products and has not generated any revenue from product sales. It expects to incur significant operating expenses and net losses for the foreseeable future.

**Funding and Liquidity**
*   **Cash Position:** As of December 31, 2024, the company held $524.3 million in cash, cash equivalents, and marketable securities. Additionally, in February 2025, the company received a $20.0 million milestone payment from Eli Lilly and Company (Lilly) under the Lp(a) program.
*   **Funding Horizon:** The company estimates that its existing capital resources will fund operating expenses and capital expenditure requirements into mid-2027. However, this estimate is based on assumptions that may prove incorrect, and the company could deplete resources sooner than expected.
*   **Need for Additional Capital:** The company currently has no credit facility or committed sources of capital. It will need to obtain substantial additional funding to continue operations. If unable to raise capital on acceptable terms, the company may be forced to delay, limit, reduce, or terminate research and development programs or commercialization efforts.

**Operational Expenses and Drivers**
*   **Increasing Costs:** Expenses are expected to increase substantially due to ongoing and planned clinical trials, including the Heart-2 Phase 1b trial of VERVE-102, the Pulse-1 Phase 1b trial of VERVE-201, and a planned Phase 2 clinical trial for the PCSK9 program. Costs will also rise from preclinical development, intellectual property maintenance, regulatory approvals, and potential commercialization infrastructure.
*   **Collaboration Payments:** The company is obligated to make milestone payments to various partners, including Lilly, Acuitas Therapeutics, The Broad Institute, Harvard, and Novartis, under existing license and collaboration agreements.
*   **Commercialization Costs:** If marketing approval is obtained, the company expects to incur significant expenses related to product manufacturing, sales, marketing, and distribution.

**Risks and Uncertainties**
*   **Development Risks:** Identifying product candidates and conducting clinical trials is time-consuming, expensive, and uncertain. The company may never generate the necessary data to obtain marketing approval or achieve commercial success.
*   **Regulatory and External Factors:** Expenses could increase further due to regulatory requirements (such as cardiovascular outcomes trials), delays in clinical trials, or third-party intellectual property challenges.
*   **Market Conditions:** Disruptions in global financial markets could reduce the company's ability to access capital, negatively affecting liquidity.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Financial Position and Need for Capital:** The company has incurred significant losses since inception, with net losses of $198.7 million, $200.1 million, and $157.4 million for the years ended December 31, 2024, 2023, and 2022, respectively. As of December 31, 2024, the accumulated deficit was $743.0 million. The company has no approved products, has generated no revenue from product sales, and expects to incur losses for the foreseeable future.
*   **Operational and Development Risks:** The company has no products approved for sale and has not yet completed a clinical trial of any product candidate. Pharmaceutical product development is time-consuming, expensive, and uncertain, with no assurance that product candidates will receive marketing approval or achieve commercial success.
*   **Substantial Funding Requirements:** The company expects to incur substantial additional research and development, commercialization, and public company operating expenses. It currently has no credit facility or committed sources of capital. If unable to raise capital on acceptable terms, the company may be forced to delay, reduce, or eliminate product development programs or commercialization efforts.
*   **Revenue Uncertainty:** Even if products are approved, revenue depends on market size, pricing, reimbursement, and commercial rights. There is no assurance that revenues will be significant enough to achieve profitability.
*   **Capital Resource Depletion:** Although the company had $524.3 million in cash, cash equivalents, and marketable securities as of December 31, 2024, and received a $20.0 million milestone payment in February 2025, these resources may be depleted sooner than expected due to unknown factors. Additional fundraising efforts may divert management attention, and there is no certainty that additional funding will be available.
*   **External Factors:** Economic disruptions and global financial market volatility could reduce the ability to access capital and negatively affect liquidity.

## Pre-written sections (judge input)

### Financial Health

Specific price, market cap, P/E ratio, revenue, and profit margin data are not available in the provided source material. The available SEC filings indicate a strong liquidity position, with cash and marketable securities totaling approximately $497 million as of March 31, 2025. However, the absence of income statement metrics prevents a comprehensive assessment of profitability or valuation efficiency. Investors should consult the full 10-Q filing for detailed revenue and earnings figures to complete this financial profile.

### Recent Developments

Verve Therapeutics filed its Form 10-Q for the period ended March 31, 2025, on May 14, 2025, providing updated financial disclosures for investors. The filing reveals a significant decline in cash and cash equivalents to $96.6 million, down from $172.6 million at the end of 2024, indicating accelerated capital deployment. Conversely, marketable securities increased to $400.5 million, suggesting a strategic shift in asset allocation or proceeds from recent financing activities. Investors should monitor these liquidity changes closely as the company navigates its operational risks and growth prospects outlined in the associated risk factors.

### SEC Filing Highlights
VERV reported a net loss of $198.7 million for 2024, maintaining an accumulated deficit of $743.0 million as the company has yet to generate revenue from product sales. Despite these losses, the firm holds $524.3 million in cash and equivalents, supplemented by a $20.0 million milestone payment from Eli Lilly in February 2025. Management estimates that existing capital resources will fund operations into mid-2027, though this projection relies on assumptions that may prove incorrect. The company faces substantial and increasing expenses driven by ongoing clinical trials for its Lp(a) and PCSK9 programs, as well as mandatory milestone payments to partners. VERV acknowledges the need for additional funding to sustain operations and warns that failure to secure capital could force delays or termination of its research and development efforts.

### Risk Factors

*   **History of Losses and No Revenue:** The company has incurred significant net losses since inception (accumulated deficit of $743.0 million), has no approved products, and has generated no revenue from product sales, with expectations of continued losses for the foreseeable future.
*   **Early-Stage Development and Regulatory Uncertainty:** The company has not yet completed any clinical trials for its product candidates, and there is no assurance that these candidates will receive marketing approval or achieve commercial success, given the time-consuming and expensive nature of pharmaceutical development.
*   **Substantial Capital Requirements and Funding Risk:** The company requires substantial additional funding for R&D and operations but currently lacks committed capital sources; failure to raise capital on acceptable terms could force delays or cancellations of development programs, while existing cash resources may be depleted sooner than expected.

## Audited (Exec Summary + Outlook)

### Executive Summary
Verve Therapeutics is a clinical-stage biotechnology company focused on developing genetic medicines for cardiovascular disease, currently navigating a period of accelerated capital deployment while holding a significant cash and marketable securities position. The stock is notable now due to the stark contrast between its substantial liquidity reserves and the persistent, heavy net losses that have accumulated to $743.0 million, highlighting the intense burn rate associated with its early-stage development. The single most important near-term variable is the company’s ability to manage its cash runway through mid-2027 while securing necessary additional funding to sustain its Lp(a) and PCSK9 clinical programs.

### Outlook
The directional outlook for Verve Therapeutics is cautiously constructive but heavily contingent on execution and capital management. Tailwinds include the strategic milestone payment from Eli Lilly and the potential for significant value realization if its genetic medicine candidates successfully advance through clinical trials for Lp(a) and PCSK9. However, substantial headwinds persist, including the company’s history of deep net losses, the absence of any revenue-generating products, and the inherent regulatory uncertainty of early-stage pharmaceutical development. Investors should closely monitor the trend in cash burn relative to the stated mid-2027 runway and the company’s ability to secure additional financing on favorable terms; a failure to raise capital or unexpected delays in clinical progress would significantly weaken the investment thesis by forcing potential program delays or termination.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "accumulated to $743.0 million"
LABEL: SUPPORTED
REASON: The accumulated deficit of $743.0 million as of December 31, 2024 is explicitly stated in both the RAG — SEC Highlights and RAG — Risk Factors sections, as well as the SEC Filing Highlights pre-written section.

---

CLAIM: "cash runway through mid-2027"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights explicitly states "the company estimates that its existing capital resources will fund operating expenses and capital expenditure requirements into mid-2027," which is also echoed in the SEC Filing Highlights pre-written section.

---

CLAIM: "significant cash and marketable securities position"
LABEL: SUPPORTED
REASON: The Financial Health pre-written section states approximately $497 million in cash and marketable securities as of March 31, 2025 (derived from $96,554K + $400,523K = $497,077K per the 10-Q balance sheet data), confirming a significant position.

---

**OUTLOOK**

---

CLAIM: "strategic milestone payment from Eli Lilly"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights and RAG — Risk Factors both explicitly state that in February 2025, the company received a $20.0 million milestone payment from Eli Lilly and Company under the Lp(a) program.

---

CLAIM: "mid-2027 runway"
LABEL: SUPPORTED
REASON: Explicitly stated in the RAG — SEC Highlights: "the company estimates that its existing capital resources will fund operating expenses and capital expenditure requirements into mid-2027."

---

CLAIM: "history of deep net losses"
LABEL: SUPPORTED
REASON: Net losses of $198.7 million (2024), $200.1 million (2023), and $157.4 million (2022) are explicitly documented in both RAG sections and the SEC Filing Highlights pre-written section.

---

CLAIM: "absence of any revenue-generating products"
LABEL: SUPPORTED
REASON: Both RAG sections and the Risk Factors pre-written section explicitly state the company has no approved products and has generated no revenue from product sales.

---

**No additional quantitative figures, price targets, specific thresholds, ratios, percentages, or named product milestones with attached numbers appear in the Executive Summary or Outlook sections beyond those evaluated above.** The references to "Lp(a) and PCSK9 clinical programs" are qualitative program names confirmed present in the source data (RAG — SEC Highlights mentions "Heart-2 Phase 1b trial of VERVE-102, the Pulse-1 Phase 1b trial of VERVE-201, and a planned Phase 2 clinical trial for the PCSK9 program"), and carry no attached quantitative claims requiring separate audit entries.
