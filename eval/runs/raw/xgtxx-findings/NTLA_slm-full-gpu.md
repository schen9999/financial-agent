# NTLA — slm-full-gpu

## Metadata

ticker: NTLA
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 548503787254d6467d4bee1e72add2fda16db9e8609707b75b6a6c29acd3f7b1
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 556, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 30.359, "latency_s_total": 30.359, "parse_failure": 0, "prompt_tokens": 3136, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 527, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 32.292, "latency_s_total": 32.292, "parse_failure": 0, "prompt_tokens": 3035, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 145, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 8.81, "latency_s_total": 8.81, "parse_failure": 0, "prompt_tokens": 693, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 150, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 9.836, "latency_s_total": 9.836, "parse_failure": 0, "prompt_tokens": 687, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 154, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 14.591, "latency_s_total": 14.591, "parse_failure": 0, "prompt_tokens": 602, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 144, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 12.895, "latency_s_total": 12.895, "parse_failure": 0, "prompt_tokens": 639, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 952, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.1, "latency_s_total": 17.1, "parse_failure": 0, "prompt_tokens": 1570, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "NTLA",
  "company_name": "Intellia Therapeutics, Inc.",
  "current_price": 11.71,
  "currency": "USD",
  "market_cap": 1640883584.0,
  "forward_pe": -4.5617986,
  "week_52_high": 28.25,
  "week_52_low": 7.95,
  "financial_currency": "USD",
  "revenue": 59506000.0,
  "net_income": -399975008.0,
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
    "filing_date": "2026-02-26",
    "summary": "Item 1A. Risk Factors Investing in our common stock involves a high degree of risk. In evaluating us and our business, careful consideration should be given to the following risk factors, in addition to the other information set forth in this Annual Report on Form 10-K for the year ended December 31, 2025 and in other documents that we file with the Securities and Exchange Commission (\u201cSEC\u201d). If any of the following risks and uncertainties actually occurs, our business, prospects, financial condition and results of operations could be materially and adversely affected. The risks described below are not intended to be exhaustive and are not the only risks facing us. New risk factors can emerge from time to time, and we cannot predict the impact that any factor or combination of factors may "
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-06",
    "summary": "Item 1A. Risk Factors Investing in our common stock involves a high degree of risk. In evaluating us and our business, careful consideration should be given to the following risk factors, in addition to the other information set forth in this Quarterly Report on Form 10-Q, our Annual Report on Form 10-K for the year ended December 31, 2025, and in other documents that we file with the Securities and Exchange Commission (\u201cSEC\u201d). If any of the following risks and uncertainties actually occurs, our business, prospects, financial condition and results of operations could be materially and adversely affected. The risks described below are not intended to be exhaustive and are not the only risks facing us. New risk factors can emerge from time to time, and we cannot predict the impact that any f"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] Based on the provided text from the Annual Report on Form 10-K for the year ended December 31, 2025, the key takeaways regarding risk factors for NTLA include:

**1. Unproven Nature of Core Technology**
CRISPR genome editing technology has only recently been clinically validated for human therapeutic use. The company’s focus on *in vivo* CRISPR-based genome editing is relatively new, and its therapeutic utility is largely unproven. The approaches used to discover and develop these novel therapeutics are unproven and may never result in marketable products.

**2. Development and Regulatory Challenges**
Successful product development requires solving complex issues, such as safely delivering therapeutic agents into target cells, optimizing efficacy and specificity, and demonstrating safety and potency. There is no assurance that these issues will be resolved. Specifically:
*   The company is in clinical-stage development for **nexiguran ziclumeran (nex-z/NTLA-2001)**, pending the resolution of a clinical hold on the IND for the MAGNITUDE trial, and for **lonvoguran ziclumeran (lonvo-z/NTLA-2002)**.
*   While one CRISPR-edited *ex vivo* therapy has been approved in the U.S. and EU, no genome editing *in vivo* therapy has been approved in these or other key jurisdictions. Consequently, the potential for regulatory approval remains uncertain.

**3. Operational and Commercial Risks**
*   **Profitability:** If the company fails to develop viable products, achieve regulatory approval, or successfully market and sell products, it may never achieve profitability.
*   **Program Abandonment:** The company may alter or abandon programs as new data becomes available. Progress in one CRISPR-based product does not guarantee success in others.
*   **Adoption Barriers:** Physicians, healthcare providers, and payors may be slow to adopt new technologies due to upfront costs, training requirements, and perceived complexity. Public perception, media coverage, and ethical concerns regarding genome editing could also negatively impact patient participation in trials and physician acceptance of treatments.
*   **Clinical Trial Delays:** The company faces numerous potential delays, including challenges in obtaining regulatory authorization (due to limited agency experience with CRISPR therapeutics), difficulties in patient enrollment, inadequate animal models, supply chain issues, and the potential for trials to be suspended or terminated due to safety concerns or non-compliance.

**4. Manufacturing and Supply Chain**
There are risks associated with manufacturing and sourcing materials, including the need for unforeseen manufacturing changes, insufficient supply quality, and challenges in importing or exporting materials between jurisdictions.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Unproven Technology and Development Risks:** CRISPR genome editing technology, particularly in vivo applications, is relatively new and its therapeutic utility is largely unproven. The approaches used to discover and develop novel therapeutics are unproven and may never lead to marketable products. There is no assurance that the company will successfully solve issues related to safe delivery, efficacy, specificity, potency, purity, and safety.
*   **Regulatory Approval Uncertainty:** While one CRISPR-edited ex vivo therapy has been approved in the U.S. and EU, no genome editing in vivo therapy has been approved in these or other key jurisdictions. The potential to obtain approval for the company’s product candidates remains uncertain.
*   **Profitability and Commercialization Risks:** The company may never achieve profitability if it fails to develop viable product candidates, obtain regulatory approval, or successfully market and sell products. Future success is highly dependent on the successful development of specific technologies and therapeutic applications.
*   **Public Perception and Adoption Barriers:** Public perception, media coverage, and ethical concerns regarding genome editing may negatively impact clinical trial participation and the acceptance of treatments by physicians and patients. Healthcare providers and payors may be slow to adopt new technologies due to upfront costs, training requirements, complexity, or perceived risks. Additionally, certain patients may not be candidates for these therapies due to health conditions or genetic profiles.
*   **Legislative and Regulatory Changes:** Responses by government agencies to negative public perception or ethical concerns may result in new legislation, regulations, or medical standards that could limit the ability to develop, commercialize, or obtain regulatory approval for products.
*   **Clinical Development Challenges:** Clinical development is lengthy, expensive, and uncertain. All programs are in early stages (discovery, preclinical, or clinical). There are risks associated with designing and implementing trials, establishing clinical endpoints, and the possibility that trials may fail at any stage. Interim results do not guarantee final success, and data are susceptible to varying interpretations.
*   **Manufacturing and Operational Risks:** Generating revenue requires substantial investment, establishing manufacturing capabilities, securing commercial manufacturing capacity, and significant marketing efforts. There are risks of delays or inability to complete development and commercialization.
*   **Clinical Trial Delays and Failures:** There is no guarantee that clinical trials will begin or complete on schedule. Regulatory requirements for later-phase trials are more stringent, and failure to meet these requirements could delay development. Unforeseen events during trials could also delay or prevent marketing approval.

## Pre-written sections (judge input)

### Financial Health

Intellia Therapeutics, Inc. (NTLA) currently trades at $11.71 with a market capitalization of approximately $1.64 billion. The company reported revenue of $59.5 million but incurred a net loss of nearly $400 million, resulting in a negative profit margin and a forward P/E ratio of -4.56. This significant net loss highlights the substantial cash burn typical of early-stage biotechnology firms focused on R&D. Consequently, the stock remains highly speculative, trading well below its 52-week high of $28.25 as investors weigh the company's long-term pipeline potential against its current lack of profitability.

### Recent Developments

Intellia Therapeutics continues to navigate significant financial headwinds, evidenced by a substantial net loss of nearly $400 million and a negative forward P/E ratio, highlighting the inherent risks of its pre-profitability stage. The company's stock has retreated significantly from its 52-week high of $28.25, currently trading near $11.71, reflecting investor caution amid ongoing operational challenges. Recent SEC filings reiterate high-risk factors, warning that adverse events could materially impact the business, which demands careful due diligence from shareholders. Investors should monitor upcoming clinical milestones and cash burn rates closely, as the company remains in a critical phase of sustaining operations while advancing its gene-editing pipeline.

### SEC Filing Highlights
Intellia Therapeutics faces significant risks due to the unproven nature of its *in vivo* CRISPR technology, with no prior approvals for genome editing therapies in key jurisdictions. The company’s clinical pipeline, including nexiguran ziclumeran and lonvoguran ziclumeran, remains subject to regulatory uncertainty and potential delays, such as the pending resolution of a clinical hold on the MAGNITUDE trial. Operational challenges include the possibility of program abandonment, manufacturing supply chain disruptions, and slow market adoption driven by high upfront costs and ethical concerns. Consequently, the company may never achieve profitability if it fails to secure regulatory approval or successfully commercialize its novel therapeutics.

### Risk Factors

*   **Unproven In Vivo Technology and Clinical Failure:** CRISPR in vivo genome editing is a nascent field with no approved therapies in key jurisdictions; the company faces significant risks regarding safe delivery, efficacy, and potency, with early-stage clinical trials subject to high failure rates and delays.
*   **Regulatory and Legislative Uncertainty:** Approval pathways for in vivo gene editing are unestablished, and the company faces potential hurdles from evolving regulations, ethical concerns, or new legislation that could restrict development or commercialization.
*   **Commercialization and Profitability Challenges:** Success depends on overcoming public perception barriers, securing payer adoption despite high upfront costs, and establishing scalable manufacturing, with no assurance the company will ever achieve profitability.

## Audited (Exec Summary + Outlook)

### Executive Summary
Intellia Therapeutics is a pioneering biotechnology firm focused on developing *in vivo* CRISPR gene-editing therapies, currently trading at $11.71 with a market capitalization of approximately $1.64 billion despite reporting a net loss of nearly $400 million. The stock is notable for its significant retreat from its 52-week high of $28.25, reflecting investor caution as the market weighs the company's long-term pipeline potential against its current lack of profitability and substantial cash burn. The single most important near-term variable shaping the outcome is the resolution of regulatory uncertainties, particularly the pending resolution of a clinical hold on the MAGNITUDE trial, which will determine the viability of its lead assets.

### Outlook
The directional outlook for Intellia Therapeutics remains cautiously constructive but heavily contingent on clinical and regulatory execution. While the company possesses a differentiated platform in *in vivo* gene editing, significant headwinds persist, including the unproven nature of its technology, potential program abandonment, and the challenge of establishing scalable manufacturing. Investors should closely monitor the resolution of the clinical hold on the MAGNITUDE trial and the company’s cash burn rates as primary indicators of operational stability. A positive resolution to regulatory hurdles and evidence of successful clinical progression would strengthen the investment thesis by validating the commercial potential of nexiguran ziclumeran and lonvoguran ziclumeran; conversely, further delays or adverse safety signals would likely weaken the view given the company's pre-profitability status and reliance on external financing to sustain operations.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "currently trading at $11.71"
LABEL: SUPPORTED
REASON: The source data explicitly lists `"current_price": 11.71`.

---

CLAIM: "market capitalization of approximately $1.64 billion"
LABEL: SUPPORTED
REASON: Source data shows `"market_cap": 1640883584.0`, which rounds to approximately $1.64 billion.

---

CLAIM: "net loss of nearly $400 million"
LABEL: SUPPORTED
REASON: Source data shows `"net_income": -399975008.0`, which is approximately $400 million net loss.

---

CLAIM: "52-week high of $28.25"
LABEL: SUPPORTED
REASON: Source data explicitly lists `"week_52_high": 28.25`.

---

CLAIM: "pending resolution of a clinical hold on the MAGNITUDE trial"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights section explicitly states "pending the resolution of a clinical hold on the IND for the MAGNITUDE trial."

---

**OUTLOOK**

---

CLAIM: "resolution of the clinical hold on the MAGNITUDE trial"
LABEL: SUPPORTED
REASON: Directly referenced in the RAG — SEC Highlights as "pending the resolution of a clinical hold on the IND for the MAGNITUDE trial."

---

CLAIM: "nexiguran ziclumeran and lonvoguran ziclumeran"
LABEL: SUPPORTED
REASON: Both product names are explicitly listed in the RAG — SEC Highlights: "nexiguran ziclumeran (nex-z/NTLA-2001)" and "lonvoguran ziclumeran (lonvo-z/NTLA-2002)."

---

*No additional quantitative figures, price targets, thresholds, ratios, metrics, percentages, or forward-looking numbers appear in the Outlook section beyond those already evaluated above.*
