# VERV — slm-full-gpu

## Metadata

ticker: VERV
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: f606ec756534ae21ac14241e18ee318a25b89a2109b63889df5858b95cb2ab51
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 713, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 11.149, "latency_s_total": 11.149, "parse_failure": 0, "prompt_tokens": 2651, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 462, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 8.67, "latency_s_total": 8.67, "parse_failure": 0, "prompt_tokens": 2399, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 147, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.852, "latency_s_total": 4.852, "parse_failure": 0, "prompt_tokens": 636, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 163, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.115, "latency_s_total": 5.115, "parse_failure": 0, "prompt_tokens": 630, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 180, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.286, "latency_s_total": 5.286, "parse_failure": 0, "prompt_tokens": 531, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 155, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.994, "latency_s_total": 4.994, "parse_failure": 0, "prompt_tokens": 790, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 944, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 10.48, "latency_s_total": 10.48, "parse_failure": 0, "prompt_tokens": 1662, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
*   **Significant Net Losses:** The company incurred net losses of $198.7 million for the year ended December 31, 2024, $200.1 million for 2023, and $157.4 million for 2022.
*   **Accumulated Deficit:** As of December 31, 2024, the company had an accumulated deficit of $743.0 million.
*   **No Revenue:** The company has no approved products and has not generated any revenue from product sales. It expects to incur significant operating expenses and net losses for the foreseeable future.

**Funding and Capital Resources**
*   **Current Liquidity:** As of December 31, 2024, the company held $524.3 million in cash, cash equivalents, and marketable securities. Additionally, in February 2025, the company received a $20.0 million milestone payment from Eli Lilly and Company (Lilly) under the Lp(a) program.
*   **Funding Horizon:** The company believes its existing resources will fund operating expenses and capital expenditure requirements into mid-2027. However, this estimate is based on assumptions that may prove incorrect, and resources could be depleted sooner than expected.
*   **Need for Additional Capital:** The company currently has no credit facility or committed sources of capital. It will need to obtain substantial additional funding to continue operations. If unable to raise capital on acceptable terms, the company may be forced to delay, limit, reduce, or terminate research and development programs or commercialization efforts.

**Operational Expenses and Drivers**
*   **Increasing Costs:** Expenses are expected to increase substantially due to ongoing and planned clinical trials, including the Heart-2 Phase 1b trial of VERVE-102, the Pulse-1 Phase 1b trial of VERVE-201, and a planned Phase 2 clinical trial for the PCSK9 program.
*   **Key Expense Categories:** Costs are driven by research and development, preclinical studies, intellectual property maintenance and defense, regulatory approvals, and potential commercialization infrastructure. The company also faces potential milestone payments to partners such as Lilly, Acuitas Therapeutics, The Broad Institute, Harvard, and Novartis.
*   **Uncertainty:** The size of future net losses depends on the rate of expense growth and the ability to generate revenue. The company acknowledges that identifying and developing product candidates is time-consuming, expensive, and uncertain, with no guarantee of marketing approval or commercial success.

**Strategic Dependencies**
*   **Collaborations:** The company relies on collaboration agreements, such as the Research and Collaboration Agreement with Lilly effective July 2023, and other license agreements. The success of these collaborations and the achievement of milestones significantly impact financial requirements.
*   **Regulatory and Market Risks:** Future expenses may increase if regulatory authorities require additional trials, if there are delays in development, or if there are third-party challenges to intellectual property. Even with marketing approval, substantial expenditures are required for commercialization, including manufacturing, sales, and marketing.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Financial Position and Need for Capital:** The company has incurred significant losses since inception, with net losses of $198.7 million, $200.1 million, and $157.4 million for the years ended December 31, 2024, 2023, and 2022, respectively. As of December 31, 2024, the accumulated deficit was $743.0 million. The company has no approved products, has generated no revenue from product sales, and expects to incur losses for the foreseeable future.
*   **Product Development and Commercialization Risks:** The company has no products approved for sale and has not yet completed a clinical trial of any product candidate. It expects it will be many years, if ever, before a product candidate is ready for commercialization. There is no assurance that the company will successfully complete preclinical testing, obtain regulatory approvals, manufacture, market, or achieve market acceptance for any products.
*   **Substantial Additional Funding Requirements:** The company expects expenses to increase substantially as it advances preclinical activities and clinical trials, and potentially incurs significant commercialization expenses if marketing approval is obtained. The company currently has no credit facility or committed sources of capital. If unable to raise capital on acceptable terms, the company may be forced to delay, reduce, or eliminate product development programs or commercialization efforts.
*   **Dependence on Future Revenue and Market Factors:** Profitability depends on generating significant revenue from product sales, which is contingent on market size, accepted pricing, coverage and reimbursement, and commercial rights. If the addressable patient population is smaller than estimated or if competition narrows the treatment population, significant revenue may not be generated even if products are approved.
*   **Operational and External Risks:** The company’s operating expenses and net losses may fluctuate significantly. Additional fundraising efforts may divert management from day-to-day activities. Economic disruptions could reduce the ability to access capital. The company’s estimate that existing cash resources will fund operations into mid-2027 is based on assumptions that may prove incorrect, potentially leading to a need for additional funding sooner than planned.

## Pre-written sections (judge input)

### Financial Health

Specific price, market capitalization, P/E ratio, revenue, and profit margin data are not available in the provided source material. However, the company's balance sheet indicates a strong liquidity position, with cash and cash equivalents decreasing to $96.6 million and marketable securities increasing to $400.5 million as of March 31, 2025. Total current assets stand at $511.7 million, suggesting sufficient short-term resources to cover immediate obligations despite the overall reduction in total assets from $647 million to $614 million. Investors should note that the absence of standard valuation metrics limits a comprehensive assessment of the company's current financial health.

### Recent Developments

Verve Therapeutics filed its 10-K annual report on February 27, 2025, and its 10-Q quarterly report on May 14, 2025, providing updated financial disclosures for investors. The most significant recent development is a substantial reduction in cash and cash equivalents, which fell from $172.6 million at the end of 2024 to $96.6 million as of March 31, 2025. Concurrently, the company increased its holdings in marketable securities to $400.5 million, indicating a strategic shift in liquidity management. These filings highlight ongoing operational risks and the need for careful monitoring of the company's burn rate and capital preservation strategies.

### SEC Filing Highlights
VERV reported a net loss of $198.7 million for 2024, maintaining an accumulated deficit of $743.0 million as the company has yet to generate revenue from product sales. Despite these losses, the firm holds $524.3 million in cash and marketable securities, supplemented by a $20.0 million milestone payment from Eli Lilly in February 2025. Management estimates that current resources will fund operations into mid-2027, though this projection relies on assumptions that may prove incorrect. The company faces substantial and increasing expenses driven by ongoing clinical trials for its Lp(a) and PCSK9 programs, necessitating future capital raises to sustain development.

### Risk Factors

*   **Substantial Financial Losses and Capital Needs:** The company has incurred significant net losses since inception (accumulated deficit of $743.0 million as of Dec 31, 2024), has no approved products or revenue, and lacks committed capital sources, requiring substantial additional funding to continue operations.
*   **Early-Stage Product Development Risks:** No product candidates have completed clinical trials or received regulatory approval, with commercialization potentially many years away; there is no assurance that preclinical testing, manufacturing, or market acceptance will be successful.
*   **Liquidity and Operational Uncertainty:** The company’s estimate that existing cash will fund operations into mid-2027 relies on assumptions that may prove incorrect, potentially forcing a need for additional capital sooner than planned or leading to the delay or elimination of development programs.

## Audited (Exec Summary + Outlook)

### Executive Summary
Verve Therapeutics is a clinical-stage biotechnology company focused on developing gene-editing therapies for cardiovascular diseases, currently holding $524.3 million in cash and marketable securities to support its pipeline. The investment case is notable due to the company’s reliance on a $20.0 million milestone payment from Eli Lilly and management’s projection that existing resources will fund operations into mid-2027. The single most important near-term variable is the successful execution of ongoing clinical trials for its Lp(a) and PCSK9 programs, which will determine the need for future capital raises and the potential for regulatory milestones.

### Outlook
The directional outlook for Verve Therapeutics is cautiously constructive, anchored by a robust liquidity buffer that extends the runway into mid-2027, yet heavily weighted by binary clinical risks. Key variables to monitor include the safety and efficacy data emerging from the Lp(a) and PCSK9 programs, as well as the company’s ability to manage its burn rate without dilutive capital raises. The thesis would be strengthened by positive clinical readouts that validate the gene-editing platform and potentially trigger further milestone payments, while it would be weakened by adverse safety signals, slower-than-expected trial progress, or a deterioration in cash reserves that forces earlier-than-anticipated financing.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$524.3 million in cash and marketable securities"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights and SEC Filing Highlights pre-written section both explicitly state "the firm holds $524.3 million in cash and marketable securities" as of December 31, 2024.

---

CLAIM: "$20.0 million milestone payment from Eli Lilly"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights explicitly states "in February 2025, the company received a $20.0 million milestone payment from Eli Lilly and Company (Lilly) under the Lp(a) program," and this is echoed in the SEC Filing Highlights pre-written section.

---

CLAIM: "management's projection that existing resources will fund operations into mid-2027"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights, RAG — Risk Factors, and SEC Filing Highlights pre-written section all explicitly state that management estimates current resources will fund operations into mid-2027.

---

**OUTLOOK**

---

CLAIM: "liquidity buffer that extends the runway into mid-2027"
LABEL: SUPPORTED
REASON: Consistent with the source data and pre-written sections, which explicitly state the company's existing resources are estimated to fund operations into mid-2027.

---

CLAIM: "further milestone payments" (as a potential future trigger from positive clinical readouts)
LABEL: INFERENCE
REASON: The source data confirms the existence of the Lilly collaboration and a prior $20.0 million milestone payment, making the inference that additional milestones could be triggered by positive clinical readouts a direct derivation from the collaboration structure described; however, no specific future milestone amounts or triggering conditions are named, so no absent figures are asserted.

---

**ADDITIONAL OBSERVATIONS — Claims that are qualitative or directional (no quantitative figure to audit):**

The following claims in the Executive Summary and Outlook are purely qualitative or directional and contain no specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones with attached numbers, or forward-looking numbers requiring arithmetic verification. They are therefore outside the scope of this audit per the instructions (which focus on "specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number"):

- "clinical-stage biotechnology company focused on developing gene-editing therapies for cardiovascular diseases"
- "Lp(a) and PCSK9 programs" (named programs — no attached quantitative claim)
- "binary clinical risks," "cautiously constructive," "robust liquidity buffer," "dilutive capital raises," "adverse safety signals," "slower-than-expected trial progress"

These are noted as qualitative characterizations consistent with the source material but not subject to the quantitative audit checks defined in the instructions.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | $524.3 million in cash and marketable securities | SUPPORTED |
| 2 | $20.0 million milestone payment from Eli Lilly | SUPPORTED |
| 3 | Resources fund operations into mid-2027 (Executive Summary) | SUPPORTED |
| 4 | Runway extends into mid-2027 (Outlook) | SUPPORTED |
| 5 | Further milestone payments from positive clinical readouts | INFERENCE |
