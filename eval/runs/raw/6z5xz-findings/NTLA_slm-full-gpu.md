# NTLA — slm-full-gpu

## Metadata

ticker: NTLA
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: dc39d75ba91fc835a89d79fe23f49a2284baa03b5dbad006e8da7c6c22007e12
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 706, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.986, "latency_s_total": 19.986, "parse_failure": 0, "prompt_tokens": 3136, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 521, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 14.431, "latency_s_total": 14.431, "parse_failure": 0, "prompt_tokens": 3035, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 135, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.718, "latency_s_total": 5.718, "parse_failure": 0, "prompt_tokens": 693, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 139, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.78, "latency_s_total": 5.78, "parse_failure": 0, "prompt_tokens": 687, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 183, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 6.224, "latency_s_total": 6.224, "parse_failure": 0, "prompt_tokens": 596, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 131, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.636, "latency_s_total": 5.636, "parse_failure": 0, "prompt_tokens": 789, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 879, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 9.912, "latency_s_total": 9.912, "parse_failure": 0, "prompt_tokens": 1560, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
*   CRISPR genome editing technology has only recently been clinically validated for human therapeutic use.
*   In vivo CRISPR-based genome editing technologies are relatively new, and their therapeutic utility is largely unproven.
*   The approaches used to discover and develop novel therapeutics using CRISPR systems are unproven and may never result in marketable products.

**2. Development and Regulatory Challenges**
*   Successful product development requires solving complex issues, such as safely delivering therapeutic agents into target cells, optimizing efficacy and specificity, and demonstrating safety, potency, and purity.
*   The company is in clinical-stage development for nexiguran ziclumeran (NTLA-2001), pending the resolution of a clinical hold on the IND for the MAGNITUDE trial, and for lonvoguran ziclumeran (NTLA-2002).
*   While one CRISPR-edited ex vivo therapy has been approved in the U.S. and EU, no genome editing in vivo therapy has been approved in these or other key jurisdictions. Consequently, the potential for obtaining approval for the company’s CRISPR product candidates remains uncertain.
*   Regulatory agencies (such as the FDA, MHRA, and EMA) have limited or no experience with the clinical development of CRISPR-based in vivo therapeutics, which may lead to additional testing requirements or delays.

**3. Commercialization and Adoption Risks**
*   If the company fails to develop viable product candidates, achieve regulatory approval, or successfully market and sell products, it may never achieve profitability.
*   Public perception, media coverage of safety issues, and ethical concerns regarding genome editing may negatively impact subject participation in clinical trials and physician/patient acceptance of treatments.
*   Physicians, healthcare providers, and third-party payors are often slow to adopt new technologies, particularly those requiring additional upfront costs and training. Physicians may deem the therapies too complex or risky to adopt without extensive training.

**4. Operational and Clinical Trial Risks**
*   The company faces numerous potential delays and unforeseen events during preclinical studies and clinical trials, including:
    *   Inability to reach agreement on terms with trial sites or contract research organizations (CROs).
    *   Clinical trials failing to show safety or efficacy, or producing negative/inconclusive results.
    *   Challenges in patient enrollment, retention, and follow-up.
    *   Insufficient or inadequate supply of product candidates or materials.
    *   Potential suspension or termination of trials due to safety concerns, noncompliance, or unacceptable health risks.
    *   Higher-than-anticipated costs for preclinical and clinical studies.
    *   Inadequate or non-existent animal models for certain human diseases.

**5. Strategic Uncertainty**
*   The company may alter or abandon programs as new data becomes available.
*   Success in developing one CRISPR-based therapeutic does not guarantee success in developing others.
*   There is no assurance that CRISPR efforts will yield products that are safe, effective, pure, potent, manufacturable, scalable, or profitable.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Unproven Technology and Development Risks:** CRISPR genome editing technology, particularly in vivo applications, is relatively new and its therapeutic utility is largely unproven. The approaches to discover and develop novel therapeutics using CRISPR systems are unproven and may never lead to marketable products. There is no assurance that the company will successfully solve issues related to safe delivery, efficacy, specificity, potency, purity, and safety.
*   **Regulatory Approval Uncertainty:** While one CRISPR-edited ex vivo therapy has been approved in the U.S. and EU, no genome editing in vivo therapy has been approved in these or other key jurisdictions. The potential to obtain approval for any CRISPR product candidates remains uncertain.
*   **Profitability and Commercialization Risks:** If the company fails to develop viable product candidates, achieve regulatory approval, or successfully market and sell products, it may never achieve profitability. Future success is highly dependent on the successful development of specific technologies and therapeutic applications.
*   **Public Perception and Adoption Barriers:** Public perception, media coverage of safety or efficacy issues, and ethical concerns regarding genome editing may negatively impact clinical trial participation and the acceptance of treatments by physicians and patients. Healthcare providers and payors may be slow to adopt new technologies due to upfront costs, training requirements, and perceived complexity or risk.
*   **Legislative and Regulatory Changes:** Responses by government agencies to negative public perception or ethical concerns may result in new legislation, regulations, or medical standards that could limit the ability to develop, commercialize, or obtain regulatory approval for product candidates.
*   **Clinical Development Challenges:** Clinical development is a lengthy, expensive, and uncertain process. Preclinical and clinical testing is difficult to design and implement, can take many years, and outcomes are not always predictive of later success. Clinical trials can fail at any stage, and interim results do not necessarily predict final results.
*   **Manufacturing and Operational Risks:** Generating revenue requires substantial investment, establishing manufacturing capabilities, securing commercial manufacturing capacity, and significant marketing efforts. The company may incur additional costs or experience delays in completing development and commercialization.
*   **Specific Product Candidate Status:** The company is in clinical-stage development for nexiguran ziclumeran (NTLA-2001), which is pending the resolution of a clinical hold on the IND for the MAGNITUDE trial, and for lonvoguran ziclumeran (NTLA-2002).

## Pre-written sections (judge input)

### Financial Health

Intellia Therapeutics, Inc. (NTLA) currently trades at $11.71 with a market capitalization of approximately $1.64 billion. The company reported revenue of $59.5 million, yet remains unprofitable with a net loss of nearly $400 million, resulting in a negative profit margin. This loss profile is reflected in a negative forward P/E ratio of -4.56, indicating that earnings expectations do not currently support a traditional valuation multiple. As a biotechnology firm in the development phase, NTLA’s financial health is characterized by significant cash burn rather than current profitability.

### Recent Developments

Intellia Therapeutics continues to navigate significant financial headwinds, evidenced by a substantial net loss of nearly $400 million and negative forward earnings, reflecting the high-risk nature of its biotechnology operations. The company's stock has traded within a wide range, currently sitting near the lower end of its 52-week band, which underscores ongoing investor caution regarding its path to profitability. With no dividend yield and a market capitalization under $1.7 billion, the firm remains heavily dependent on its pipeline execution and potential partnerships to sustain growth. Investors should closely monitor upcoming regulatory milestones and cash burn rates as critical indicators of the company's near-term viability.

### SEC Filing Highlights
Intellia Therapeutics highlights that its in vivo CRISPR genome editing technology remains largely unproven, with no prior approvals in key jurisdictions creating significant regulatory uncertainty. The company faces substantial development hurdles, including resolving a clinical hold on the MAGNITUDE trial for nexiguran ziclumeran and navigating agencies with limited experience in this therapeutic class. Operational risks are compounded by potential trial delays, supply chain constraints, and the challenge of achieving commercial adoption amid public skepticism and high upfront costs. Consequently, the filing emphasizes that failure to secure regulatory approval or demonstrate viable product candidates could prevent the company from ever achieving profitability.

### Risk Factors

*   **Unproven In Vivo Technology and Clinical Uncertainty:** CRISPR in vivo genome editing is a nascent field with no approved therapies in key jurisdictions; the company faces significant risks regarding safe delivery, efficacy, and specificity, with clinical trials (such as the MAGNITUDE trial) subject to potential delays, holds, or failure.
*   **Regulatory, Legislative, and Public Perception Barriers:** Approval is uncertain and contingent on navigating evolving regulatory standards, while negative public perception, ethical concerns, or new legislation regarding genome editing could severely hinder clinical trial participation, physician adoption, and commercial viability.
*   **Commercialization and Profitability Challenges:** The company is not yet profitable and requires substantial capital for manufacturing, marketing, and operational scaling; failure to successfully develop viable products, secure regulatory approval, or achieve market adoption could prevent the company from ever generating revenue.

## Audited (Exec Summary + Outlook)

### Executive Summary
Intellia Therapeutics operates as a developer of in vivo CRISPR genome editing technologies, currently trading at $11.71 with a market capitalization of approximately $1.64 billion despite reporting a net loss of nearly $400 million. The stock is notable for its position near the lower end of its 52-week range, reflecting investor caution regarding the company's path to profitability and its reliance on pipeline execution. The single most important near-term variable shaping the outcome is the resolution of the clinical hold on the MAGNITUDE trial and the subsequent regulatory trajectory for nexiguran ziclumeran.

### Outlook
The directional outlook for Intellia Therapeutics is cautiously constructive but heavily contingent on binary clinical and regulatory events. Key variables to monitor include the successful resolution of the clinical hold on the MAGNITUDE trial, the company’s ability to manage its substantial cash burn, and the evolving landscape of public and legislative sentiment regarding genome editing. A positive resolution to the regulatory hurdles surrounding nexiguran ziclumeran would strengthen the thesis by validating the in vivo platform and potentially unlocking partnership opportunities, whereas continued delays or negative safety signals would weaken the view by exacerbating financial pressures and extending the timeline to commercial viability.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

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
REASON: Source data shows `"net_income": -399975008.0`, which is approximately $400 million in net loss; "nearly $400 million" is accurate.

---

CLAIM: "position near the lower end of its 52-week range"
LABEL: SUPPORTED
REASON: The 52-week high is $28.25 and the 52-week low is $7.95; the current price of $11.71 sits at ($11.71 − $7.95) / ($28.25 − $7.95) = $3.76 / $20.30 ≈ 18.5% of the way up the range, which is arithmetically near the lower end.

---

CLAIM: "resolution of the clinical hold on the MAGNITUDE trial"
LABEL: SUPPORTED
REASON: The SEC Filing Highlights and RAG sections explicitly reference "a clinical hold on the IND for the MAGNITUDE trial" for nexiguran ziclumeran (NTLA-2001).

---

CLAIM: "nexiguran ziclumeran"
LABEL: SUPPORTED
REASON: Named explicitly in both RAG sections and the pre-written SEC Filing Highlights section as NTLA-2001.

---

**OUTLOOK**

---

CLAIM: "resolution of the clinical hold on the MAGNITUDE trial"
LABEL: SUPPORTED
REASON: Directly referenced in the RAG SEC Highlights and Risk Factors sections as a pending clinical hold on the IND for the MAGNITUDE trial.

---

*(No additional specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, or forward-looking numbers appear in the Outlook section beyond the qualitative/directional statements and the named product/trial milestones already evaluated above.)*

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | Trading at $11.71 | SUPPORTED |
| 2 | Market cap ~$1.64 billion | SUPPORTED |
| 3 | Net loss of nearly $400 million | SUPPORTED |
| 4 | Near lower end of 52-week range | SUPPORTED |
| 5 | Clinical hold on the MAGNITUDE trial | SUPPORTED |
| 6 | Nexiguran ziclumeran (named milestone) | SUPPORTED |
| 7 | Resolution of MAGNITUDE clinical hold (Outlook) | SUPPORTED |

All quantitative and forward-looking claims in the Executive Summary and Outlook are supported by the source data. No unsupported or inference-only claims were identified.
