# SANA — slm-full-gpu

## Metadata

ticker: SANA
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: e053290f06c7fed17eae1292d8383cd7b4913a327e2ad7ca04e2e8308ffab216
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 509, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 8.565, "latency_s_total": 8.565, "parse_failure": 0, "prompt_tokens": 2059, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 399, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 7.476, "latency_s_total": 7.476, "parse_failure": 0, "prompt_tokens": 2048, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 124, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.316, "latency_s_total": 4.316, "parse_failure": 0, "prompt_tokens": 619, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 149, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.707, "latency_s_total": 4.707, "parse_failure": 0, "prompt_tokens": 613, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 161, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.822, "latency_s_total": 4.822, "parse_failure": 0, "prompt_tokens": 473, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 130, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.424, "latency_s_total": 4.424, "parse_failure": 0, "prompt_tokens": 591, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 863, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 9.618, "latency_s_total": 9.618, "parse_failure": 0, "prompt_tokens": 1510, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
*   Scientific evidence supporting the feasibility of these treatments is preliminary and limited. Preclinical and clinical testing is inherently unpredictable, and results from animal models or specific cell types may not translate to humans or other microenvironments.

**2. Regulatory and Safety Challenges**
*   The company faces difficulties in creating appropriate models and assays to evaluate the safety and purity of its product candidates.
*   There is a risk that regulatory authorities may not be satisfied with the data provided to explain unexpected results observed during testing.
*   Novel gene editing reagents and manufacturing materials may have unanticipated adverse effects on safety, efficacy, or manufacturability, potentially affecting multiple programs simultaneously.

**3. Financial and Operational Uncertainties**
*   There is substantial doubt as to the company’s ability to continue as a going concern.
*   The company requires additional funding to finance operations. Failure to raise capital when needed could force the delay, reduction, or elimination of product development or commercialization efforts.
*   The company may fail to realize benefits from acquired or in-licensed technologies or strategic relationships.

**4. Forward-Looking Statements and General Risks**
*   Forward-looking statements are based on current expectations but are subject to significant uncertainties. Actual results may differ materially from these projections due to various risk factors, including geopolitical, business, and economic environments.
*   Success depends on retaining key personnel, recruiting qualified staff, and effectively managing growth.
*   Product candidates developed for different indications may exhibit unexpected differences in safety or efficacy, requiring changes to manufacturing or clinical plans that could cause delays.

**5. Risk Factor Summary**
*   Investing in the company’s securities is speculative and risky.
*   Material adverse effects on business, financial condition, and results of operations could occur if the company fails to successfully identify, develop, or commercialize product candidates, or experiences significant delays in doing so.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Unproven Technology:** The company’s ex vivo and in vivo cell engineering platforms are based on novel technologies that are unproven and may not result in approvable or marketable products. There is substantial doubt regarding the feasibility of developing therapeutic treatments based on these platforms, as scientific evidence is preliminary and limited.
*   **Development and Regulatory Uncertainty:** Preclinical and clinical testing is inherently unpredictable. Results from animal models or preclinical assays may not accurately predict safety and efficacy in humans. Additionally, the company lacks FDA-approved therapeutics derived from pluripotent stem cells or utilizing its fusogen technology, and it may face challenges in creating appropriate models and assays to satisfy regulatory authorities.
*   **Product Candidate Performance:** Product candidates may reveal unexpected differences in safety or efficacy when developed for different indications or compared to other candidates using the same technologies. This could require changes to manufacturing processes or clinical development plans, leading to delays and increased costs.
*   **Financial and Operational Risks:** There is substantial doubt as to the company’s ability to continue as a going concern. The company requires additional funding to finance operations; failure to raise capital when needed could force the delay, reduction, or elimination of product development programs.
*   **Strategic and Partnership Risks:** The company may not realize the benefits of acquired or in-licensed technologies, nor may it successfully enter into or realize benefits from new strategic relationships.
*   **Personnel and Growth Management:** The company’s ability to develop its platforms and achieve future growth depends on retaining key personnel and recruiting qualified staff. The company may also encounter difficulties in managing growth, including expanding development and regulatory capabilities, which could disrupt operations.
*   **General Business Risks:** If the company is unable to successfully identify, develop, and commercialize product candidates, or experiences significant delays, its business, financial condition, and results of operations will be materially adversely affected.

## Pre-written sections (judge input)

### Financial Health

Sana Biotechnology, Inc. (SANA) is currently trading at $2.72, reflecting a market capitalization of approximately $814.3 million. The company reports a negative forward P/E ratio of -4.90 and a 0.0% profit margin, driven by a net loss of $211.8 million, which is characteristic of its pre-profitability stage in the biotechnology sector. With no dividend yield and significant operational losses, the stock exhibits high financial risk and relies heavily on future clinical milestones and capital raises to sustain operations.

### Recent Developments

Sana Biotechnology, Inc. (SANA) continues to navigate significant financial headwinds, evidenced by a net income loss of $211.8 million and a negative forward P/E ratio, underscoring the high-risk nature of the investment. The company’s stock price has contracted sharply from its 52-week high of $6.55 to its current level of $2.72, nearing its yearly low and reflecting sustained investor caution. Recent SEC filings highlight persistent macroeconomic and geopolitical risks that could further exacerbate operational uncertainties and adversely affect financial performance. Investors should remain vigilant regarding the company’s cash burn rate and the timeline for potential commercialization milestones amidst this challenging economic environment.

### SEC Filing Highlights
Sana Biotechnology faces significant risks as its novel *ex vivo* and *in vivo* cell engineering platforms remain unproven, with no FDA-approved therapeutics currently existing in these specific categories. The company has disclosed substantial doubt regarding its ability to continue as a going concern, highlighting the critical need for additional funding to sustain operations and development efforts. Regulatory challenges persist, particularly in establishing appropriate safety models and addressing potential adverse effects from novel gene editing reagents. Consequently, the firm’s future success is heavily contingent on securing capital, retaining key personnel, and navigating the inherent unpredictability of preclinical and clinical testing.

### Risk Factors

*   **Unproven Technology and Scientific Feasibility:** The company’s ex vivo and in vivo cell engineering platforms are novel and unproven, with preliminary scientific evidence creating substantial doubt regarding the feasibility of developing approvable or marketable therapeutic treatments.
*   **Regulatory and Clinical Development Uncertainty:** There is a lack of FDA-approved therapeutics derived from the company’s core technologies, and inherent unpredictability in preclinical and clinical testing may lead to safety or efficacy failures, regulatory challenges, and significant delays.
*   **Financial Viability and Capital Requirements:** There is substantial doubt regarding the company’s ability to continue as a going concern, as it requires additional funding to finance operations; failure to raise capital could force the reduction or elimination of product development programs.

## Audited (Exec Summary + Outlook)

### Executive Summary
Sana Biotechnology operates as a pre-profitability cell engineering firm utilizing novel *ex vivo* and *in vivo* platforms, currently trading at $2.72 with a market capitalization of approximately $814.3 million amidst significant operational losses. The stock is notable now due to the intersection of its sharp price contraction from recent highs and the SEC’s disclosure of substantial doubt regarding its ability to continue as a going concern. The single most important near-term variable is the company’s ability to secure additional capital to sustain operations while navigating the inherent unpredictability of its unproven therapeutic pipelines.

### Outlook
The directional outlook for Sana Biotechnology is cautiously cautious, characterized by severe headwinds stemming from unproven scientific feasibility and acute financial viability concerns. Investors should closely monitor the company’s cash burn rate and the timeline for any successful capital raises, as these are the primary determinants of whether the firm can continue its development efforts. The thesis would be strengthened only by clear evidence of sustained funding and positive, reproducible data from its *ex vivo* and *in vivo* platforms that alleviates regulatory and safety doubts; conversely, any further dilution, delayed milestones, or inability to secure financing would significantly weaken the investment case and increase the risk of program termination.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "currently trading at $2.72"
LABEL: SUPPORTED
REASON: The source data explicitly lists `"current_price": 2.72`.

---

CLAIM: "market capitalization of approximately $814.3 million"
LABEL: SUPPORTED
REASON: The source data lists `"market_cap": 814260928.0`, which rounds to approximately $814.3 million; the pre-written Financial Health section also states this figure explicitly.

---

CLAIM: "sharp price contraction from recent highs"
LABEL: SUPPORTED
REASON: The source data shows a 52-week high of $6.55 versus a current price of $2.72, confirming a sharp contraction of approximately 58.5% from the 52-week high.

---

CLAIM: "SEC's disclosure of substantial doubt regarding its ability to continue as a going concern"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights and RAG — Risk Factors sections both explicitly state "There is substantial doubt as to the company's ability to continue as a going concern," and this is echoed in the pre-written SEC Filing Highlights section.

---

**OUTLOOK**

No specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section. All claims in the Outlook are qualitative or directional in nature (e.g., "cautiously cautious," "cash burn rate," "successful capital raises," "positive, reproducible data," "dilution," "delayed milestones"). There are no numerical claims to audit in this section.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | Trading at $2.72 | SUPPORTED |
| 2 | Market cap ~$814.3 million | SUPPORTED |
| 3 | Sharp price contraction from recent highs | SUPPORTED |
| 4 | SEC disclosure of going concern doubt | SUPPORTED |

No quantitative claims in the Outlook section require evaluation. All four auditable claims in the Executive Summary are **SUPPORTED**.
