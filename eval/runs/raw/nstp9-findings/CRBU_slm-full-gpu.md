# CRBU — slm-full-gpu

## Metadata

ticker: CRBU
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: e87efe2f4f6a306259dea979adda09709ad259eaf0f977f83f6cabe01a84b50e
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 566, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 16.494, "latency_s_total": 16.494, "parse_failure": 0, "prompt_tokens": 3132, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 487, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 15.341, "latency_s_total": 15.341, "parse_failure": 0, "prompt_tokens": 3121, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 139, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 9.613, "latency_s_total": 9.613, "parse_failure": 0, "prompt_tokens": 666, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 157, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 11.287, "latency_s_total": 11.287, "parse_failure": 0, "prompt_tokens": 660, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 173, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 11.798, "latency_s_total": 11.798, "parse_failure": 0, "prompt_tokens": 563, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 133, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 11.543, "latency_s_total": 11.543, "parse_failure": 0, "prompt_tokens": 650, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 949, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 13.871, "latency_s_total": 13.871, "parse_failure": 0, "prompt_tokens": 1590, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "CRBU",
  "company_name": "Caribou Biosciences, Inc.",
  "current_price": 1.19,
  "currency": "USD",
  "market_cap": 127576944.0,
  "forward_pe": -0.94195503,
  "week_52_high": 3.535,
  "week_52_low": 1.17,
  "financial_currency": "USD",
  "revenue": 10035000.0,
  "net_income": -103403000.0,
  "profit_margin_pct": 0.0,
  "dividend_yield": 0.0,
  "sector": "Healthcare",
  "industry": "Biotechnology"
}

NEWS ARTICLES:
[]

SEC FILING SUMMARIES:
{
  "10-K": {
    "form_type": "10-K",
    "filing_date": "2026-03-05",
    "summary": "Item 1A. Risk Factors. Investing in shares of our common stock involves a high degree of risk. You should carefully consider the following risks and uncertainties, together with all of the other information contained in this Annual Report on Form 10-K, including our financial statements and related notes, before making an investment decision. These disclosures reflect our beliefs and opinions as to factors that could materially and adversely affect our company and its securities in the future. References to past events are provided by way of example only and are not intended to be a complete listing or a representation as to whether or not such factors have occurred in the past or their likelihood of occurring in the future. Furthermore, the risks described below are not the only ones faci"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-13",
    "summary": "Item 1A. Risk Factors. There have been no material changes to the Risk Factors previously disclosed in Item 1A. to Part I of our Form 10-K. The risks described in our Form 10-K are not the only risks facing our company. Additional risks and uncertainties not currently known to us or that we currently deem to be immaterial also may materially adversely affect our business, financial condition, and/or operating results. Item 2. Unregistered Sales of Equity Securities, Use of Proceeds, and Issuer Purchases of Equity Securities. Unregistered Sales of Equity Securities during the Three Months Ended June 30, 2026 There were no unregistered sales of equity securities during the three months ended June 30, 2026. Item 5. Other Information. During the quarter ended June 30, 2026, none of our directo"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] Based on the provided text from the Annual Report on Form 10-K for ticker CRBU, the key takeaways regarding the company's financial position and risks are as follows:

**Financial Performance and Status**
*   **Significant Operating Losses:** The company has incurred significant operating losses every year since its inception. For the years ended December 31, 2025, and 2024, net losses were $148.1 million and $149.1 million, respectively.
*   **Accumulated Deficit:** As of December 31, 2025, the company had an accumulated deficit of $596.5 million.
*   **No Revenue:** The company has not commercialized any products and has never generated revenue from product sales. Almost all financial resources have been devoted to research and development, including preclinical and clinical activities.

**Capital Requirements and Liquidity**
*   **Need for Additional Financing:** The company requires substantial additional capital to conduct its planned pivotal clinical trial for vispa-cel and to implement operating plans for its product candidates, vispa-cel and CB-011.
*   **Current Cash Position:** As of December 31, 2025, the company held $142.8 million in cash, cash equivalents, and marketable securities. This is expected to fund current operations for at least the next 12 months, though circumstances could cause capital to be consumed faster than anticipated.
*   **Insufficient Funds for Pivotal Trial:** The company currently does not have sufficient funds to conduct the planned pivotal clinical trial for vispa-cel. Failure to obtain additional financing would prevent the completion of development and commercialization for vispa-cel and/or CB-011.

**Future Expenses and Risks**
*   **Increasing Costs:** Expenses are expected to increase substantially as the company progresses clinical trials (particularly the pivotal trial for vispa-cel), hires employees, expands manufacturing and supply chain capabilities, seeks regulatory approvals, and potentially establishes sales and marketing infrastructure.
*   **Unpredictability:** The company cannot predict the extent of future losses or when it will become profitable, if at all. Even if profitable, sustainability is not guaranteed.
*   **Additional Capital Needs:** Beyond the proceeds from its IPO and other historical sources, the company will continue to need additional capital. Future capital requirements depend on numerous factors, including clinical trial results, regulatory delays, litigation costs, and the need to establish internal manufacturing capabilities.
*   **Management Distraction:** Fundraising efforts may divert management’s attention from day-to-day activities, potentially adversely affecting the development and commercialization of product candidates.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Financial Position and Need for Additional Capital:** The company has incurred significant operating losses since inception, with net losses of $148.1 million in 2025 and $149.1 million in 2024, resulting in an accumulated deficit of $596.5 million as of December 31, 2025. The company has never generated revenue from product sales and anticipates continued operating losses for the foreseeable future.
*   **Inability to Achieve Profitability:** The company is unable to predict when it will become profitable, if at all, and may not be able to sustain or increase profitability even if it does become profitable.
*   **Insufficient Funds for Clinical Trials:** As of December 31, 2025, the company had $142.8 million in cash, cash equivalents, and marketable securities, which is expected to fund operations for at least 12 months. However, the company currently lacks sufficient funds to conduct its planned pivotal clinical trial for vispa-cel and will need substantial additional financing. Failure to obtain this financing would prevent the completion of development and commercialization for vispa-cel and/or CB-011.
*   **High Costs of Development and Commercialization:** Costs increase substantially as product candidates advance through clinical phases with greater numbers of patients. Significant expenses are expected for advancing vispa-cel into a large, multicenter pivotal trial, expanding manufacturing capabilities, seeking regulatory approvals, and establishing sales, marketing, and distribution infrastructure.
*   **Operational and Regulatory Risks:** Risks include potential delays or failures in clinical trials, difficulties in receiving regulatory clearances, changes in the economic or regulatory environment, pandemics, and the need to hire additional employees or acquire intellectual property.
*   **Litigation and Public Company Costs:** The company faces risks associated with operating as a public company, including defending against securities class action litigation and costs related to maintaining its patent portfolio.
*   **Management Distraction:** Additional fundraising efforts may divert management’s attention from day-to-day activities, adversely affecting the ability to develop and commercialize product candidates.
*   **Uncertainty of Future Funding:** There is no certainty that additional funding will be available when needed, on acceptable terms, or at all.

## Pre-written sections (judge input)

### Financial Health

Caribou Biosciences, Inc. (CRBU) currently trades at $1.19, reflecting a market capitalization of approximately $127.6 million. The company reports minimal revenue of $10.0 million and a negative net income of $103.4 million, resulting in a negative profit margin and an unfavorable forward P/E ratio of -0.94. This financial profile indicates that the company is in a pre-profitability stage, heavily reliant on capital raises to fund its biotechnology operations. Investors should note the significant gap between current valuation and fundamental earnings, highlighting the high-risk nature of this speculative growth asset.

### Recent Developments

Caribou Biosciences recently filed its 2026 Annual Report on Form 10-K on March 5, 2026, alongside a subsequent 10-Q filing on August 13, 2026, which confirmed no material changes to previously disclosed risk factors. The company reported a net loss of approximately $103.4 million, reflecting the ongoing high-risk profile inherent in its biotechnology operations. Investors should note that the stock is trading near its 52-week low of $1.17, indicating significant market pressure and limited liquidity. With no recent news catalysts or unregistered equity sales reported, the current outlook remains heavily dependent on future clinical milestones and capital management strategies.

### SEC Filing Highlights
Caribou Biosciences reported net losses of $148.1 million for 2025 and maintains an accumulated deficit of $596.5 million, having generated no revenue to date. While the company holds $142.8 million in cash to fund operations for at least the next 12 months, it explicitly states that current funds are insufficient to complete the pivotal clinical trial for vispa-cel. Consequently, the firm faces a critical need for substantial additional financing to advance its product candidates, vispa-cel and CB-011, through development and potential commercialization.

### Risk Factors

*   **Severe Liquidity Constraints and Capital Needs:** The company has incurred significant operating losses and an accumulated deficit of $596.5 million, with current cash reserves insufficient to fund the planned pivotal clinical trial for vispa-cel, necessitating substantial additional financing that may not be available on acceptable terms.
*   **Uncertainty of Profitability and Commercialization:** As a pre-revenue entity, the company has never generated product sales and cannot predict when it will become profitable; failure to advance product candidates through clinical trials or obtain regulatory approvals would prevent commercialization and revenue generation.
*   **High Development Costs and Operational Risks:** Advancing product candidates involves substantial expenses for clinical trials, manufacturing, and regulatory approvals, alongside risks of trial delays, regulatory rejections, and management distraction due to ongoing fundraising efforts.

## Audited (Exec Summary + Outlook)

### Executive Summary
Caribou Biosciences is a pre-revenue biotechnology company specializing in CRISPR-based therapies, currently trading at $1.19 with a market capitalization of approximately $127.6 million despite reporting an accumulated deficit of $596.5 million. The stock is notable for its extreme proximity to its 52-week low of $1.17 and its critical liquidity gap, as existing cash reserves are explicitly insufficient to fund the pivotal clinical trial for its lead candidate, vispa-cel. The single most important near-term variable shaping the investment outcome is the company’s ability to secure substantial additional financing to bridge the gap between current capital and the costs of advancing vispa-cel and CB-011 through development.

### Outlook
The directional outlook for Caribou Biosciences is cautiously cautious, characterized by a binary risk profile where the primary driver is capital accessibility rather than immediate operational performance. Key variables to monitor include the timing and terms of any equity or debt financing rounds, as well as the progress of the pivotal trial for vispa-cel, which currently lacks sufficient funding. A strengthening of the investment thesis would require the successful closure of substantial capital to ensure trial continuity without excessive dilution, while a weakening view would result from delayed financing, trial setbacks, or further erosion of cash reserves below the threshold needed for near-term operations. Investors should remain vigilant regarding the company’s ability to navigate the pre-revenue landscape without compromising the development timeline of its core assets.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

### EXECUTIVE SUMMARY

---

CLAIM: "currently trading at $1.19"
LABEL: SUPPORTED
REASON: The raw source data explicitly lists `"current_price": 1.19`.

---

CLAIM: "market capitalization of approximately $127.6 million"
LABEL: SUPPORTED
REASON: The raw source data lists `"market_cap": 127576944.0`, which rounds to approximately $127.6 million.

---

CLAIM: "accumulated deficit of $596.5 million"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors sections both explicitly state "an accumulated deficit of $596.5 million as of December 31, 2025."

---

CLAIM: "extreme proximity to its 52-week low of $1.17"
LABEL: SUPPORTED
REASON: The raw source data lists `"week_52_low": 1.17`, and the current price of $1.19 is arithmetically $0.02 above that low, confirming extreme proximity.

---

CLAIM: "existing cash reserves are explicitly insufficient to fund the pivotal clinical trial for its lead candidate, vispa-cel"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "the company currently does not have sufficient funds to conduct the planned pivotal clinical trial for vispa-cel."

---

CLAIM: "advancing vispa-cel and CB-011 through development"
LABEL: SUPPORTED
REASON: Both product candidates, vispa-cel and CB-011, are explicitly named in the RAG SEC Highlights and Risk Factors sections as the company's product candidates requiring additional financing.

---

### OUTLOOK

---

CLAIM: "pivotal trial for vispa-cel, which currently lacks sufficient funding"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "the company currently does not have sufficient funds to conduct the planned pivotal clinical trial for vispa-cel."

---

CLAIM: "cash reserves below the threshold needed for near-term operations"
LABEL: INFERENCE
REASON: The source data states $142.8 million in cash is expected to fund operations for "at least the next 12 months," so a "threshold needed for near-term operations" is directly derivable as a level below $142.8 million; the claim is a directional restatement of this disclosed runway figure without introducing any absent fact.

---

*No additional quantitative figures, price targets, specific ratios, percentages, or named forward-looking numbers appear in the Outlook section beyond those evaluated above.*
