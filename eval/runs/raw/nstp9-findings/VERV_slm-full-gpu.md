# VERV — slm-full-gpu

## Metadata

ticker: VERV
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 30d6e95ba3eb24a9e73aa1b6fce6b6e82d7ab8faa820d5026b37cdf13dbe860e
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 699, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.642, "latency_s_total": 17.642, "parse_failure": 0, "prompt_tokens": 2651, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 426, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 13.694, "latency_s_total": 13.694, "parse_failure": 0, "prompt_tokens": 2399, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 161, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 6.34, "latency_s_total": 6.34, "parse_failure": 0, "prompt_tokens": 616, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 152, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.58, "latency_s_total": 5.58, "parse_failure": 0, "prompt_tokens": 610, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 141, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 8.099, "latency_s_total": 8.099, "parse_failure": 0, "prompt_tokens": 495, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 164, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 6.978, "latency_s_total": 6.978, "parse_failure": 0, "prompt_tokens": 776, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 921, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.108, "latency_s_total": 17.108, "parse_failure": 0, "prompt_tokens": 1608, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
*   **Significant Operating Losses:** The company has incurred substantial net losses since inception, reporting $198.7 million for the year ended December 31, 2024, $200.1 million for 2023, and $157.4 million for 2022.
*   **Accumulated Deficit:** As of December 31, 2024, the company had an accumulated deficit of $743.0 million.
*   **No Revenue:** The company has no approved products and has not generated any revenue from product sales. It expects to incur losses for the foreseeable future and may never achieve profitability.

**Funding and Capital Resources**
*   **Current Liquidity:** As of December 31, 2024, the company held $524.3 million in cash, cash equivalents, and marketable securities. Additionally, in February 2025, the company received a $20.0 million milestone payment from Eli Lilly and Company (Lilly) under the Lp(a) program.
*   **Funding Horizon:** Management estimates that existing resources will fund operating expenses and capital expenditures into mid-2027. However, this estimate relies on assumptions that may prove incorrect, and the company could deplete resources sooner than expected.
*   **Need for Additional Capital:** The company currently has no credit facility or committed sources of capital. It will need to obtain substantial additional funding to continue operations. If unable to raise capital on acceptable terms, the company may be forced to delay, limit, reduce, or terminate research and development programs or commercialization efforts.

**Operational Expenses and Growth Drivers**
*   **Increasing Costs:** Expenses are expected to increase substantially due to ongoing and planned clinical trials, including the Heart-2 Phase 1b trial of VERVE-102, the Pulse-1 Phase 1b trial of VERVE-201, and a planned Phase 2 clinical trial for the PCSK9 program. Costs will also rise from preclinical development, intellectual property maintenance, regulatory approvals, and potential commercialization infrastructure.
*   **Collaboration Payments:** The company is obligated to make milestone payments to various partners, including Lilly, Acuitas Therapeutics, The Broad Institute, Harvard, and Novartis, under existing license and collaboration agreements.
*   **Commercialization Risks:** Even if marketing approval is obtained, the company faces risks related to commercial success, including the need for post-approval studies (such as cardiovascular outcomes trials) and the potential for commercial revenues to be insufficient to sustain operations.

**Strategic Risks**
*   **Uncertainty of Development:** Identifying product candidates and conducting clinical trials is time-consuming, expensive, and uncertain. The company may never generate the necessary data for marketing approval or achieve commercial success.
*   **External Factors:** Global financial market disruptions could reduce the company's ability to access capital. Additionally, delays in clinical trials, regulatory requirements for additional studies, or intellectual property challenges could further increase expenses and adversely affect the business.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Financial Position and Need for Capital:** The company has incurred significant losses since inception, with net losses of $198.7 million, $200.1 million, and $157.4 million for the years ended December 31, 2024, 2023, and 2022, respectively. As of December 31, 2024, the accumulated deficit was $743.0 million. The company has no approved products, has generated no revenue from product sales, and expects to incur losses for the foreseeable future.
*   **Operational and Development Risks:** The company has no products approved for sale and has not yet completed a clinical trial of any product candidate. Pharmaceutical product development is time-consuming, expensive, and uncertain, with no assurance that product candidates will receive marketing approval or achieve commercial success.
*   **Substantial Funding Requirements:** The company expects to incur substantial additional research and development, commercialization, and public company operating expenses. It currently has no credit facility or committed sources of capital. If unable to raise capital on acceptable terms, the company may be forced to delay, reduce, or eliminate product development programs or commercialization efforts.
*   **Revenue Uncertainty:** Even if products are approved, revenue depends on market size, pricing, reimbursement, and commercial rights. There is no assurance that revenues will be significant enough to achieve profitability.
*   **Liquidity and Market Conditions:** While the company had $524.3 million in cash, cash equivalents, and marketable securities as of December 31, 2024, and received a $20.0 million milestone payment in February 2025, these resources may be depleted sooner than expected. Disruptions in global financial markets could reduce the ability to access capital.
*   **Management Distraction:** Additional fundraising efforts may divert management from day-to-day activities, adversely affecting the ability to develop and commercialize product candidates.

## Pre-written sections (judge input)

### Financial Health

Specific quantitative metrics such as price, market cap, P/E ratio, revenue, and profit margin are not provided in the available data. However, the company’s balance sheet indicates a strong liquidity position, with cash and cash equivalents decreasing from $172.56 million to $96.55 million, alongside a significant increase in marketable securities to $400.52 million as of March 31, 2025. Total assets declined slightly from $647 million to $614 million, reflecting ongoing operational expenditures or investment shifts. The absence of profitability metrics suggests the company is likely in a pre-profit or growth stage, typical for biotechnology firms, relying on its substantial cash and securities reserves to fund future operations.

### Recent Developments

Verve Therapeutics, Inc. filed its Form 10-K on February 27, 2025, and its Form 10-Q for the period ending March 31, 2025, on May 14, 2025. The most significant recent development is a substantial reduction in cash and cash equivalents, which fell from $172.6 million to $96.6 million, indicating accelerated capital deployment. While marketable securities increased to $400.5 million, the net decrease in total assets suggests ongoing operational expenditures or strategic investments. Investors should monitor the company's burn rate and liquidity position closely as it navigates these financial shifts.

### SEC Filing Highlights
VERV reported a net loss of $198.7 million for 2024, maintaining an accumulated deficit of $743.0 million as the company continues to generate no revenue from product sales. Despite these losses, the firm holds $524.3 million in cash and marketable securities, supplemented by a $20.0 million milestone payment from Eli Lilly in February 2025. Management estimates that current liquidity will fund operations through mid-2027, though this projection assumes no significant delays or cost overruns in ongoing clinical trials. The company faces substantial risks related to its need for additional capital, as it lacks committed funding sources and may be forced to curtail development programs if unable to raise funds on acceptable terms.

### Risk Factors

*   **Substantial Financial Losses and Capital Needs:** The company has incurred significant net losses (accumulated deficit of $743.0 million) and generated no revenue, requiring substantial additional funding to cover R&D and operating expenses without committed capital sources.
*   **Pre-Commercial Development Risks:** The company has no approved products and has not completed any clinical trials, facing high uncertainty regarding regulatory approval, commercial success, and the timeline for generating revenue.
*   **Liquidity and Execution Risks:** Despite current cash reserves, resources may be depleted sooner than expected, and ongoing fundraising efforts may distract management from critical product development and commercialization activities.

## Audited (Exec Summary + Outlook)

### Executive Summary
Verve Therapeutics is a pre-commercial biotechnology firm focused on developing gene-editing therapies, currently relying on a liquidity pool of $524.3 million to fund operations through mid-2027 despite an accumulated deficit of $743.0 million. The stock is notable now due to the accelerated deployment of capital, evidenced by the drop in cash equivalents to $96.6 million, which highlights the intense burn rate associated with its ongoing clinical trials. The single most important near-term variable is the execution of these clinical programs without significant delays or cost overruns, as any deviation threatens the company's ability to sustain operations without raising additional capital.

### Outlook
The directional outlook for Verve Therapeutics is cautiously constructive, anchored by its substantial cash and securities reserves that provide a runway through mid-2027, yet tempered by the inherent risks of a pre-revenue biotech firm with no approved products. Key variables to monitor include the pace of clinical trial execution, the potential for cost overruns, and the company's ability to secure additional funding if current reserves are depleted faster than anticipated. The thesis would be strengthened by positive clinical data updates and sustained operational efficiency, while it would be weakened by any significant delays in development timelines or adverse regulatory feedback that could necessitate immediate and dilutive capital raises.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "a liquidity pool of $524.3 million"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and SEC Filing Highlights pre-written section both explicitly state the company held "$524.3 million in cash, cash equivalents, and marketable securities as of December 31, 2024."

---

CLAIM: "fund operations through mid-2027"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "Management estimates that existing resources will fund operating expenses and capital expenditures into mid-2027," and this is echoed in the SEC Filing Highlights pre-written section.

---

CLAIM: "an accumulated deficit of $743.0 million"
LABEL: SUPPORTED
REASON: Both the RAG SEC Highlights and RAG Risk Factors explicitly state "As of December 31, 2024, the accumulated deficit was $743.0 million."

---

CLAIM: "the drop in cash equivalents to $96.6 million"
LABEL: SUPPORTED
REASON: The 10-Q summary shows cash and cash equivalents of $96,554 thousand (≈$96.6 million) as of March 31, 2025, and the Financial Health and Recent Developments pre-written sections confirm this figure.

---

**OUTLOOK**

---

CLAIM: "substantial cash and securities reserves that provide a runway through mid-2027"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and SEC Filing Highlights pre-written section both explicitly state management estimates current resources will fund operations into mid-2027.

---

CLAIM: "no approved products"
LABEL: SUPPORTED
REASON: Both the RAG SEC Highlights and RAG Risk Factors explicitly state "The company has no approved products and has not generated any revenue from product sales."

---

*No additional quantitative figures, price targets, thresholds, ratios, percentages, named product milestones, or other forward-looking numbers appear in the Outlook section beyond those already evaluated above.*

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | Liquidity pool of $524.3 million | SUPPORTED |
| 2 | Fund operations through mid-2027 | SUPPORTED |
| 3 | Accumulated deficit of $743.0 million | SUPPORTED |
| 4 | Drop in cash equivalents to $96.6 million | SUPPORTED |
| 5 | Runway through mid-2027 (Outlook) | SUPPORTED |
| 6 | No approved products (Outlook) | SUPPORTED |

All six verifiable quantitative and forward-looking claims in the Executive Summary and Outlook are **SUPPORTED** by the source data. No unsupported or inference-only claims were identified.
