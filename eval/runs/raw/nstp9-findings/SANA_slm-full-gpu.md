# SANA — slm-full-gpu

## Metadata

ticker: SANA
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: a78750eac3b696d2532234b11e6d4718e03917473f08601bcd680c5434a4ed0e
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 567, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 16.005, "latency_s_total": 16.005, "parse_failure": 0, "prompt_tokens": 2059, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 404, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 13.474, "latency_s_total": 13.474, "parse_failure": 0, "prompt_tokens": 2048, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 120, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.738, "latency_s_total": 4.738, "parse_failure": 0, "prompt_tokens": 601, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 176, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 7.443, "latency_s_total": 7.443, "parse_failure": 0, "prompt_tokens": 595, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 155, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 6.532, "latency_s_total": 6.532, "parse_failure": 0, "prompt_tokens": 478, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 137, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.638, "latency_s_total": 5.638, "parse_failure": 0, "prompt_tokens": 649, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 885, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 16.937, "latency_s_total": 16.937, "parse_failure": 0, "prompt_tokens": 1558, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "SANA",
  "company_name": "Sana Biotechnology, Inc.",
  "current_price": 2.88,
  "currency": "USD",
  "market_cap": 862158656.0,
  "forward_pe": -5.1881614,
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
[]

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
[From Pinecone cache] Based on the provided text from the SEC EDGAR filing for ticker SANA, the key takeaways regarding risk factors and business outlook include:

**1. Unproven Technology and Development Risks**
*   The company’s *ex vivo* and *in vivo* cell engineering platforms rely on novel technologies that are unproven and may not result in approvable or marketable products.
*   There are no FDA-approved therapeutics currently known that are cell products derived from pluripotent stem cells (PSCs) or utilize the company’s fusogen technology.
*   Scientific evidence supporting these platforms is preliminary, limited, and ongoing. Preclinical and clinical testing is inherently unpredictable, and results from animal models or preclinical cell lines may not accurately predict safety and efficacy in humans.
*   The company has not tested its platforms on all cell types or microenvironments, and results may not translate across different contexts.

**2. Regulatory and Safety Challenges**
*   The company may face significant challenges in creating appropriate models and assays to evaluate the safety and purity of its product candidates.
*   There is a risk that regulatory authorities may not be satisfied with the data provided to explain unexpected results observed during testing.
*   Novel gene editing reagents and manufacturing materials may have unanticipated or undesirable effects on safety, efficacy, or manufacturability, potentially affecting multiple programs and causing delays.

**3. Financial and Operational Uncertainties**
*   There is substantial doubt as to the company’s ability to continue as a going concern.
*   The company requires additional funding to finance operations. Failure to raise capital when needed on acceptable terms could force the company to delay, reduce, or eliminate product development programs or commercialization efforts.
*   If the company fails to successfully identify, develop, and commercialize product candidates, or experiences significant delays, its business, financial condition, and results of operations will be materially adversely affected.

**4. Strategic and Personnel Dependencies**
*   The company’s ability to develop its platforms and achieve future growth depends on retaining key personnel and recruiting additional qualified staff.
*   The company may not realize the benefits of technologies it has acquired, in-licensed, or will acquire, nor may it successfully enter into or benefit from new strategic relationships.
*   Managing growth, particularly in development and regulatory capabilities, may lead to difficulties that could disrupt operations and harm the business.

**5. Forward-Looking Statements**
*   Forward-looking statements are based on current expectations and estimates but are subject to significant uncertainties. Actual results may differ materially from those expressed or implied.
*   The company does not undertake an obligation to publicly update any forward-looking statements, and new risk factors may emerge that management cannot currently predict.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Unproven Technology:** The company’s ex vivo and in vivo cell engineering platforms are based on novel technologies that are unproven and may not result in approvable or marketable products. There is substantial doubt regarding the feasibility of developing therapeutic treatments based on these platforms, as scientific evidence is preliminary and limited.
*   **Development and Regulatory Uncertainty:** Preclinical and clinical testing is inherently unpredictable. Results from animal models or preclinical assays may not accurately predict safety and efficacy in humans. Additionally, the company lacks FDA-approved therapeutics derived from pluripotent stem cells or utilizing its fusogen technology, and it may face challenges in creating appropriate models and assays to satisfy regulatory authorities.
*   **Product Candidate Performance:** Product candidates may reveal unexpected differences in safety or efficacy when developed for different indications or compared to other candidates using the same technologies. This could require changes to manufacturing processes or clinical development plans, leading to delays and increased costs.
*   **Financial and Operational Risks:** There is substantial doubt as to the company’s ability to continue as a going concern. The company will require additional funding to finance operations, and failure to raise capital when needed could force the delay, reduction, or elimination of product development programs.
*   **Strategic and Partnership Risks:** The company may not realize the benefits of acquired or in-licensed technologies, nor may it successfully enter into or realize benefits from new strategic relationships.
*   **Personnel and Growth Management:** The company’s ability to develop its platforms and achieve future growth depends on retaining key personnel and recruiting qualified staff. The company may also encounter difficulties in managing growth, including expanding development and regulatory capabilities, which could disrupt operations.
*   **General Business Risks:** If the company is unable to successfully identify, develop, and commercialize product candidates, or experiences significant delays in doing so, its business, financial condition, and results of operations will be materially adversely affected.

## Pre-written sections (judge input)

### Financial Health

Sana Biotechnology, Inc. (SANA) is currently trading at $2.88, reflecting a market capitalization of approximately $862.16 million. The company reports a negative forward P/E ratio of -5.19 and a net income loss of $211.82 million, indicating it is not yet profitable. Consequently, the profit margin stands at 0.0%, consistent with its early-stage biotechnology profile. Investors should note the absence of dividend yields, as the firm prioritizes reinvestment over shareholder distributions.

### Recent Developments

Sana Biotechnology, Inc. has filed its 10-K annual report for the fiscal year ending in early 2026, alongside a subsequent 10-Q quarterly filing in August 2026, both of which highlight significant risk factors related to the global geopolitical and economic environment. The company continues to operate with a net loss of approximately $211.8 million, reflecting the high-risk, pre-revenue nature typical of its biotechnology sector. With the stock trading near its 52-week low of $2.61 at $2.88, investors are closely monitoring the firm's ability to navigate these macroeconomic headwinds while managing its substantial cash burn. The absence of recent specific news updates suggests a period of operational consolidation or waiting for key clinical or partnership milestones to drive future valuation.

### SEC Filing Highlights
Sana Biotechnology faces significant risks as its novel *ex vivo* and *in vivo* cell engineering platforms remain unproven, with no FDA-approved therapeutics currently existing in these specific categories. The company has disclosed substantial doubt regarding its ability to continue as a going concern, highlighting a critical need for additional funding to sustain operations and development programs. Regulatory hurdles are further compounded by challenges in establishing safety models for new gene editing reagents and the inherent unpredictability of translating preclinical results to human trials. Consequently, the firm’s financial condition and future growth are heavily dependent on successfully securing capital and retaining key personnel to navigate these scientific and operational uncertainties.

### Risk Factors

*   **Unproven Technology and Feasibility:** The company’s ex vivo and in vivo cell engineering platforms are novel and unproven, with preliminary scientific evidence creating substantial doubt regarding the feasibility of developing approvable or marketable therapeutic treatments.
*   **Regulatory and Clinical Uncertainty:** Preclinical and clinical testing is inherently unpredictable, and the company lacks FDA-approved therapeutics derived from its platforms, facing significant challenges in demonstrating safety and efficacy to satisfy regulatory authorities.
*   **Financial Viability and Capital Needs:** There is substantial doubt regarding the company’s ability to continue as a going concern, as it requires additional funding to finance operations; failure to raise capital could force the delay, reduction, or elimination of product development programs.

## Audited (Exec Summary + Outlook)

### Executive Summary
Sana Biotechnology operates as an early-stage cell engineering firm leveraging novel *ex vivo* and *in vivo* platforms, currently trading at $2.88 with a market capitalization of approximately $862.16 million despite reporting a net income loss of $211.82 million. The stock is notable for its proximity to the 52-week low of $2.61 and the disclosed substantial doubt regarding its ability to continue as a going concern, highlighting a critical dependency on external capital. The single most important near-term variable is the company's success in securing sufficient funding to sustain operations while navigating the inherent scientific and regulatory uncertainties of its unproven therapeutic pipeline.

### Outlook
The directional outlook for Sana Biotechnology is cautiously cautious, characterized by significant binary risks tied to its survival and technological validation. Key variables to monitor include the company’s ability to secure necessary capital to address substantial doubt about its going concern status, as well as progress in establishing safety models for its gene editing reagents. The thesis would be strengthened by evidence of successful preclinical-to-clinical translation or strategic partnerships that alleviate funding pressures; conversely, any indication of further cash burn without clear milestones or a failure to raise capital would significantly weaken the investment case.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "currently trading at $2.88"
LABEL: SUPPORTED
REASON: The source data explicitly lists `"current_price": 2.88`.

---

CLAIM: "market capitalization of approximately $862.16 million"
LABEL: SUPPORTED
REASON: The source data lists `"market_cap": 862158656.0`, which rounds to $862.16 million; the pre-written Financial Health section also states this figure explicitly.

---

CLAIM: "net income loss of $211.82 million"
LABEL: SUPPORTED
REASON: The source data lists `"net_income": -211822000.0`, which equals a loss of $211.822 million, consistent with the stated $211.82 million (within rounding).

---

CLAIM: "proximity to the 52-week low of $2.61"
LABEL: SUPPORTED
REASON: The source data lists `"week_52_low": 2.61`; the current price of $2.88 is $0.27 above the low, confirming proximity, and the exact figure $2.61 is present in the source data.

---

CLAIM: "disclosed substantial doubt regarding its ability to continue as a going concern"
LABEL: SUPPORTED
REASON: Both the RAG — SEC Highlights and RAG — Risk Factors sections explicitly state "There is substantial doubt as to the company's ability to continue as a going concern," and this is echoed in the pre-written SEC Filing Highlights section.

---

**OUTLOOK**

---

CLAIM: (No specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section.)
LABEL: N/A
REASON: The Outlook section contains only qualitative directional statements and narrative risk descriptions; there are no quantitative or specifically enumerated forward-looking figures to audit.

---

**SUMMARY**

All quantitative claims in the Executive Summary are **SUPPORTED** by the raw source data. The Outlook section contains no quantitative or specifically enumerable forward-looking figures requiring audit entries.
