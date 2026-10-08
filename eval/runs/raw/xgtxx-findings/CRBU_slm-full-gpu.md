# CRBU — slm-full-gpu

## Metadata

ticker: CRBU
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 239261bcabbc977d51296e0931155f10993fdc22679b085b0781a574fe75f27b
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 543, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.614, "latency_s_total": 19.614, "parse_failure": 0, "prompt_tokens": 3132, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 535, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 18.011, "latency_s_total": 18.011, "parse_failure": 0, "prompt_tokens": 3121, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 131, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 6.772, "latency_s_total": 6.772, "parse_failure": 0, "prompt_tokens": 687, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 154, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.622, "latency_s_total": 4.622, "parse_failure": 0, "prompt_tokens": 681, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 257, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 14.927, "latency_s_total": 14.927, "parse_failure": 0, "prompt_tokens": 611, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 162, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 8.982, "latency_s_total": 8.982, "parse_failure": 0, "prompt_tokens": 627, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 992, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 25.034, "latency_s_total": 25.034, "parse_failure": 0, "prompt_tokens": 1794, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "CRBU",
  "company_name": "Caribou Biosciences, Inc.",
  "current_price": 0.6174,
  "currency": "USD",
  "market_cap": 66189916.0,
  "forward_pe": -0.4887084,
  "week_52_high": 3.535,
  "week_52_low": 0.546,
  "financial_currency": "USD",
  "revenue": 10035000.0,
  "net_income": -103403000.0,
  "profit_margin_pct": 0.0,
  "dividend_yield": 0.0,
  "sector": "Healthcare",
  "industry": "Biotechnology"
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
[From Pinecone cache] Based on the provided text from the Annual Report on Form 10-K for ticker CRBU, here are the key takeaways regarding the company's financial position and risks:

**Financial Performance and Status**
*   **Significant Operating Losses:** The company has incurred significant operating losses every year since its inception. Net losses were $148.1 million for the year ended December 31, 2025, and $149.1 million for the year ended December 31, 2024.
*   **Accumulated Deficit:** As of December 31, 2025, the company had an accumulated deficit of $596.5 million.
*   **No Revenue:** The company has not commercialized any products and has never generated revenue from product sales. Almost all financial resources have been devoted to research and development, including preclinical and clinical activities.

**Capital Requirements and Liquidity**
*   **Need for Additional Financing:** The company requires substantial additional capital to conduct its planned pivotal clinical trial for vispa-cel and to implement operating plans for its product candidates, vispa-cel and CB-011.
*   **Current Cash Position:** As of December 31, 2025, the company held $142.8 million in cash, cash equivalents, and marketable securities. This is expected to fund current operations for at least the next 12 months, though circumstances could cause capital to be consumed faster than anticipated.
*   **Insufficient Funds for Pivotal Trial:** The company currently does not have sufficient funds to conduct the planned pivotal clinical trial for vispa-cel. Failure to obtain additional financing would prevent the completion of development and commercialization for vispa-cel and/or CB-011.

**Future Expenses and Risks**
*   **Increasing Costs:** Expenses are expected to increase substantially as the company progresses clinical trials (particularly the pivotal trial for vispa-cel), hires employees, expands manufacturing capabilities, seeks regulatory approvals, and establishes commercialization infrastructure.
*   **Uncertainty of Profitability:** The company is unable to predict when it will become profitable, if at all, and may not be able to sustain profitability even if achieved.
*   **Risk Factors:** Additional capital needs depend on various factors, including clinical trial results, regulatory delays, costs of intellectual property maintenance, litigation, and the need to establish sales and marketing capabilities. If additional funding is not available on acceptable terms, the company’s ability to develop and commercialize its products will be adversely affected.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Financial Position and Need for Additional Capital:** The company has incurred significant operating losses since inception, with net losses of $148.1 million in 2025 and $149.1 million in 2024, resulting in an accumulated deficit of $596.5 million as of December 31, 2025. It has never generated revenue from product sales and anticipates continued operating losses.
*   **Inability to Achieve Profitability:** The company may not be able to achieve or sustain profitability, and even if it does, it may not be able to sustain or increase profitability on a quarterly or annual basis. The extent of future losses and the timing of profitability are unpredictable.
*   **Need for Substantial Financing:** The company requires substantial additional financing to conduct its planned pivotal clinical trial for vispa-cel and to implement operating plans for vispa-cel and CB-011. As of December 31, 2025, the company had $142.8 million in cash, cash equivalents, and marketable securities, which is expected to fund operations for at least the next 12 months, but this expectation is based on assumptions that may prove wrong.
*   **Failure to Obtain Financing:** If the company fails to obtain additional financing, it will be unable to complete the development and commercialization of its vispa-cel and/or CB-011 product candidates. Specifically, without additional funds, it cannot initiate the pivotal clinical trial for vispa-cel or develop CB-011 beyond dose expansion.
*   **High Costs of Development and Commercialization:** Costs increase substantially as product candidates advance through clinical phases with greater numbers of patients. Significant expenses are expected for clinical trials, hiring employees, acquiring intellectual property, expanding manufacturing capabilities, seeking regulatory approvals, and establishing sales and marketing infrastructure.
*   **Regulatory and Clinical Trial Risks:** Risks include delays, challenges, or failures in clinical trials, differing interpretations of data, potential safety issues, and difficulties in receiving regulatory clearances or approvals.
*   **Operational and Legal Risks:** These include costs associated with maintaining a supply chain, fulfilling contractual obligations (such as reimbursements to The Regents of the University of California), patent portfolio maintenance, litigation (including securities class actions), and the diversion of management attention during fundraising efforts.
*   **Market and Competitive Risks:** The company faces risks from competing technologies, the success or failure of similar products, and market developments.

## Pre-written sections (judge input)

### Financial Health

Caribou Biosciences, Inc. (CRBU) currently trades at $0.6174 with a market capitalization of approximately $66.2 million. The company reported revenue of $10.04 million but incurred a net loss of $103.4 million, resulting in a negative profit margin and an ineffective forward P/E ratio. This significant net loss highlights the substantial cash burn typical of early-stage biotechnology firms focused on R&D. Consequently, the stock remains highly speculative, trading near its 52-week low of $0.546 amidst ongoing operational risks.

### Recent Developments

Caribou Biosciences continues to face significant financial headwinds, evidenced by a net loss of $103.4 million and a market capitalization hovering near $66 million. The company’s stock has traded within a narrow range between $0.546 and $3.535 over the past year, currently trading at $0.6174, reflecting sustained investor caution. Recent SEC filings, including the 10-K and 10-Q reports, highlight persistent risk factors without noting material changes in unregistered equity sales or insider transactions. For investors, these developments underscore the high-risk nature of the position, characterized by negative profitability and limited near-term catalysts visible in current disclosures.

### SEC Filing Highlights
Caribou Biosciences reported a net loss of $148.1 million for the year ended December 31, 2025, maintaining its history of significant operating losses and zero revenue from product sales. The company holds $142.8 million in cash and equivalents, which is projected to fund operations for at least the next 12 months, though this runway is insufficient to complete the pivotal clinical trial for vispa-cel. Consequently, CRBU faces a critical need for substantial additional financing to advance its product candidates, vispa-cel and CB-011, through development and potential commercialization. Failure to secure necessary capital on acceptable terms would severely impair the company’s ability to execute its strategic plans and achieve profitability.

### Risk Factors

*   **Substantial Capital Requirements and Liquidity Risk:** The company has incurred significant operating losses (accumulated deficit of $596.5 million as of Dec 31, 2025) and has never generated revenue from product sales. While current cash reserves are expected to fund operations for at least 12 months, the company requires substantial additional financing to complete pivotal trials for vispa-cel and develop CB-011; failure to secure this funding would halt development and commercialization efforts.
*   **Uncertainty of Profitability and Path to Commercialization:** There is no assurance that the company will ever achieve or sustain profitability, as future losses and timing remain unpredictable. The company faces high costs associated with clinical trials, regulatory approvals, and establishing commercial infrastructure, with significant expenses expected as product candidates advance.
*   **Regulatory, Clinical, and Operational Execution Risks:** Development is subject to risks including clinical trial delays, safety issues, and potential failure to obtain regulatory clearances. Additionally, the company faces operational challenges such as maintaining supply chains, fulfilling contractual obligations (e.g., to the University of California), managing patent portfolios, and potential litigation, all of which could divert management attention and increase costs.

## Audited (Exec Summary + Outlook)

### Executive Summary
Caribou Biosciences is an early-stage biotechnology firm focused on developing gene-editing therapies, currently operating with a market capitalization of approximately $66.2 million and facing significant operational losses. The stock is notable for its highly speculative nature, trading near its 52-week low amidst persistent cash burn and a lack of near-term commercial revenue. The single most important near-term variable is the company’s ability to secure substantial additional financing, as its current cash runway is insufficient to complete the pivotal clinical trial for vispa-cel.

### Outlook
The directional outlook for Caribou Biosciences is cautiously cautious, defined by the tension between its proprietary gene-editing technology and the immediate threat of liquidity constraints. Key variables to monitor include the timing and terms of any potential capital raises, as well as progress updates on the vispa-cel and CB-011 clinical programs, which serve as the primary catalysts for value realization. The thesis would strengthen if the company successfully bridges its funding gap without excessive dilution and demonstrates tangible clinical milestones; conversely, any delay in financing or adverse safety signals would significantly weaken the investment case by extending the timeline to commercialization and increasing the risk of operational failure.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of approximately $66.2 million"
LABEL: SUPPORTED
REASON: The raw source data lists market_cap as $66,189,916.0, which rounds to approximately $66.2 million, consistent with the Financial Health pre-written section.

---

CLAIM: "trading near its 52-week low"
LABEL: SUPPORTED
REASON: The current price is $0.6174 and the 52-week low is $0.546; $0.6174 is 13.1% above the low and 82.5% below the 52-week high of $3.535, confirming the stock is arithmetically near its 52-week low rather than its high.

---

CLAIM: "current cash runway is insufficient to complete the pivotal clinical trial for vispa-cel"
LABEL: SUPPORTED
REASON: The SEC Highlights explicitly state "The company currently does not have sufficient funds to conduct the planned pivotal clinical trial for vispa-cel," and the SEC Filing Highlights pre-written section repeats this directly.

---

**OUTLOOK**

---

CLAIM: "vispa-cel and CB-011 clinical programs"
LABEL: SUPPORTED
REASON: Both vispa-cel and CB-011 are explicitly named as product candidates in the RAG SEC Highlights, Risk Factors, and SEC Filing Highlights pre-written section.

---

No additional quantitative figures, price targets, thresholds, ratios, metrics, percentages, or specific forward-looking numbers appear in the Outlook section beyond the named product milestones and qualitative directional statements already evaluated above. All remaining language ("funding gap," "excessive dilution," "adverse safety signals," "timeline to commercialization") is qualitative and directional, not a specific quantitative or named-milestone claim subject to audit under the defined scope.
