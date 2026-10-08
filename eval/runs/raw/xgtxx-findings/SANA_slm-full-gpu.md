# SANA — slm-full-gpu

## Metadata

ticker: SANA
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: ea690745ba55d4f64bc616decc04f8046274178d22fddfcaf9704817c327e23e
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 461, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 31.272, "latency_s_total": 31.272, "parse_failure": 0, "prompt_tokens": 2059, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 374, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 29.483, "latency_s_total": 29.483, "parse_failure": 0, "prompt_tokens": 2048, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 139, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 7.187, "latency_s_total": 7.187, "parse_failure": 0, "prompt_tokens": 619, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 160, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 9.847, "latency_s_total": 9.847, "parse_failure": 0, "prompt_tokens": 613, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 158, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 11.74, "latency_s_total": 11.74, "parse_failure": 0, "prompt_tokens": 448, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 125, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 12.355, "latency_s_total": 12.355, "parse_failure": 0, "prompt_tokens": 543, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 879, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 15.401, "latency_s_total": 15.401, "parse_failure": 0, "prompt_tokens": 1546, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "SANA",
  "company_name": "Sana Biotechnology, Inc.",
  "current_price": 2.72,
  "currency": "USD",
  "market_cap": 814260928.0,
  "forward_pe": -4.89993,
  "week_52_high": 6.55,
  "week_52_low": 2.61,
  "financial_currency": "USD",
  "net_income": -211822000.0,
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
    "filing_date": "2026-03-03",
    "summary": "Item 1A. Ris k Factors. Investing in shares of our common stock involves a high degree of risk. You should carefully consider the following risks and uncertainties, together with all of the other information contained in this Annual Report, including our financial statements and related notes included elsewhere in this Annual Report, before making an investment decision. The risks described below are not the only ones we face. Many of the following risks and uncertainties are, and will continue to be, exacerbated by any worsening of the global geo-political, business, and economic environment. The occurrence of any of the following risks, or of additional risks and uncertainties not presently known to us or that we currently believe to be immaterial, could materially and adversely affect o"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-10",
    "summary": "Item 1A. Ri sk Factors Investing in shares of our common stock involves a high degree of risk. You should carefully consider the following risks and uncertainties, together with all of the other information contained in this Quarterly Report, including our financial statements and related notes included elsewhere in this Quarterly Report, before making an investment decision. The risks described below are not the only ones we face. Many of the following risks and uncertainties are, and will continue to be, exacerbated by any worsening of the global geo-political, business, and economic environment. The occurrence of any of the following risks, or of additional risks and uncertainties not presently known to us or that we currently believe to be immaterial, could materially and adversely aff"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] Based on the provided text from the SEC EDGAR filings for ticker SANA, the key takeaways regarding risk factors and business outlook include:

**1. Unproven Technology and Development Risks**
*   The company’s *ex vivo* and *in vivo* cell engineering platforms rely on novel technologies that are unproven and may not result in approvable or marketable products.
*   There are no FDA-approved therapeutics currently known that are cell products derived from pluripotent stem cells (PSCs) or utilize the company’s fusogen technology.
*   Scientific evidence supporting the feasibility of these treatments is preliminary, limited, and ongoing.

**2. Uncertainty in Clinical and Preclinical Testing**
*   Testing is inherently unpredictable, particularly with novel technologies. Results from one cell type or microenvironment may not translate to others.
*   Current gene editing approaches use novel reagents that may have unanticipated or undesirable effects.
*   Most data is limited to animal models and preclinical assays, which may not accurately predict human safety and efficacy.
*   The company faces challenges in creating appropriate models and assays to evaluate safety and purity, potentially failing to satisfy regulatory authorities.

**3. Operational and Financial Challenges**
*   There is substantial doubt regarding the company’s ability to continue as a going concern.
*   The company requires additional funding to finance operations. Failure to raise capital on acceptable terms could force delays, reductions, or eliminations of product development or commercialization efforts.
*   Success depends on retaining key personnel and recruiting qualified staff, as well as managing growth in development and regulatory capabilities.

**4. Forward-Looking Statements and General Risks**
*   Forward-looking statements are based on current expectations but are subject to significant uncertainties and should not be relied upon as predictions of future events.
*   The company may not realize benefits from acquired or in-licensed technologies or strategic relationships.
*   Product candidates may exhibit unexpected differences in safety or efficacy across different indications, potentially requiring changes to manufacturing or clinical plans that delay development.
*   The occurrence of any described risks, or additional unknown risks, could materially and adversely affect the business, financial condition, reputation, or stock price.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Unproven Technology:** The company’s ex vivo and in vivo cell engineering platforms are based on novel technologies that are unproven and may not result in approvable or marketable products. There is substantial doubt regarding the feasibility of developing therapeutic treatments based on these platforms, as scientific evidence is preliminary and limited.
*   **Development and Regulatory Uncertainty:** Preclinical and clinical testing is inherently unpredictable, particularly for novel technologies. Results from animal models or preclinical assays may not accurately predict safety and efficacy in humans. Additionally, the company lacks FDA-approved therapeutics derived from pluripotent stem cells or utilizing its fusogen technology, and it may face challenges in creating appropriate models and assays to satisfy regulatory authorities.
*   **Product Candidate Failure:** If the company is unable to successfully identify, develop, and commercialize product candidates, or experiences significant delays, its business, financial condition, and results of operations will be materially adversely affected.
*   **Going Concern and Funding Needs:** There is substantial doubt as to the company’s ability to continue as a going concern. The company requires additional funding to finance operations, and failure to raise capital when needed could force the delay, reduction, or elimination of product development programs or commercialization efforts.
*   **Strategic and Partnership Risks:** The company may not realize the benefits of acquired or in-licensed technologies, nor may it successfully enter into or realize benefits from new strategic relationships.
*   **Operational and Personnel Risks:** The company’s growth depends on retaining key personnel and recruiting qualified staff. Additionally, the company may encounter difficulties in managing growth, including expanding development and regulatory capabilities, which could disrupt operations.
*   **External Factors:** Risks are exacerbated by worsening global geo-political, business, and economic environments.

## Pre-written sections (judge input)

### Financial Health

Sana Biotechnology, Inc. (SANA) is currently trading at $2.72, reflecting a market capitalization of approximately $814.26 million. The company reports a negative forward P/E ratio of -4.90 and a net income loss of $211.82 million, indicating it is not yet profitable. Consequently, the profit margin stands at 0.0%, underscoring the firm's reliance on capital raises to fund its biotechnology operations. Investors should note that the stock is trading near its 52-week low of $2.61, highlighting significant near-term volatility and financial risk.

### Recent Developments

Sana Biotechnology, Inc. (SANA) is currently trading near its 52-week low of $2.61 at $2.72, reflecting significant investor caution amid persistent profitability challenges with a negative forward P/E ratio and a net loss of $211.8 million. The company’s most recent 10-K filing in March 2026 and subsequent 10-Q in August 2026 highlight elevated risk factors exacerbated by a worsening global geopolitical and economic environment, signaling potential headwinds for near-term operations. With no dividend yield and a market capitalization under $820 million, the stock remains highly speculative, requiring investors to closely monitor clinical milestones and cash runway management to mitigate downside risk.

### SEC Filing Highlights
Sana Biotechnology faces significant risks as its novel *ex vivo* and *in vivo* cell engineering platforms remain unproven, with no FDA-approved therapeutics currently existing in these specific categories. The company’s clinical and preclinical data are largely derived from animal models, creating uncertainty regarding the translation of safety and efficacy to human applications. Financially, there is substantial doubt about the company’s ability to continue as a going concern, necessitating additional capital to sustain operations and development efforts. Consequently, failure to secure funding or retain key personnel could force delays or reductions in its product pipeline.

### Risk Factors

*   **Unproven Technology and Scientific Feasibility:** The company’s novel ex vivo and in vivo cell engineering platforms are based on preliminary scientific evidence, creating substantial doubt regarding the feasibility of developing approvable or marketable therapeutic treatments.
*   **Regulatory Uncertainty and Product Failure:** As a company with no FDA-approved therapeutics derived from its platforms, Sana faces inherent unpredictability in preclinical and clinical testing, with significant risks that product candidates may fail to demonstrate safety or efficacy in humans.
*   **Going Concern and Funding Risks:** There is substantial doubt regarding the company’s ability to continue as a going concern, as it requires additional capital to finance operations; failure to raise funds could force the delay or elimination of development programs.

## Audited (Exec Summary + Outlook)

### Executive Summary
Sana Biotechnology operates as a cell engineering company utilizing novel *ex vivo* and *in vivo* platforms, currently valued at approximately $814.26 million despite reporting a net income loss of $211.82 million. The stock is notable now as it trades near its 52-week low of $2.61, reflecting significant investor caution amid persistent profitability challenges and a negative forward P/E ratio. The single most important near-term variable shaping the outcome is the company’s ability to secure additional capital to sustain operations and mitigate substantial doubt regarding its ability to continue as a going concern.

### Outlook
The directional outlook for Sana Biotechnology is cautiously cautious, characterized by high uncertainty due to the unproven nature of its cell engineering platforms and the absence of FDA-approved therapeutics. Key variables investors should monitor include the progression of preclinical and clinical data from animal models to human applications, as well as the company’s success in securing necessary capital to address substantial doubt regarding its going concern status. The thesis would strengthen if the company demonstrates credible translation of safety and efficacy in human trials or successfully closes a significant funding round; conversely, the view would weaken further if key personnel depart or if development programs are delayed or eliminated due to funding constraints.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "currently valued at approximately $814.26 million"
LABEL: SUPPORTED
REASON: The source data lists market_cap as 814,260,928.0 USD, which rounds to approximately $814.26 million as stated.

---

CLAIM: "net income loss of $211.82 million"
LABEL: SUPPORTED
REASON: The source data lists net_income as -211,822,000.0 USD, which equals a loss of approximately $211.82 million.

---

CLAIM: "trades near its 52-week low of $2.61"
LABEL: SUPPORTED
REASON: The source data explicitly lists week_52_low as 2.61, and the current price of 2.72 is indeed near that figure.

---

CLAIM: "negative forward P/E ratio"
LABEL: SUPPORTED
REASON: The source data lists forward_pe as -4.89993, which is a negative value, confirming this characterization.

---

**OUTLOOK**

---

CLAIM: "absence of FDA-approved therapeutics"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights and RAG — Risk Factors both explicitly state "There are no FDA-approved therapeutics currently known that are cell products derived from pluripotent stem cells (PSCs) or utilize the company's fusogen technology."

---

CLAIM: "progression of preclinical and clinical data from animal models to human applications"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights explicitly states "Most data is limited to animal models and preclinical assays, which may not accurately predict human safety and efficacy," directly grounding this watch-item.

---

CLAIM: "substantial doubt regarding its going concern status"
LABEL: SUPPORTED
REASON: Both the RAG — SEC Highlights and RAG — Risk Factors explicitly state "There is substantial doubt regarding the company's ability to continue as a going concern."

---

**No additional quantitative figures, price targets, thresholds, ratios, specific percentages, named product milestones, or forward-looking numbers appear in the Executive Summary or Outlook sections beyond those evaluated above.** All claims audited are either directly present in or directly derivable from the source data.
