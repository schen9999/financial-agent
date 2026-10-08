# AFRM — slm-full-cpu

## Metadata

ticker: AFRM
arm: slm-full-cpu
judge_prompt_version: v2
context_sha256: 0d2295873797e115c1b8f69d398e8fb1048ac4b2143e7486471d8aed15fb6874
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 632, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 150.65, "latency_s_total": 150.65, "parse_failure": 0, "prompt_tokens": 2358, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 576, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 144.76, "latency_s_total": 144.76, "parse_failure": 0, "prompt_tokens": 3026, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 148, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 45.618, "latency_s_total": 45.618, "parse_failure": 0, "prompt_tokens": 708, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 177, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 62.095, "latency_s_total": 62.095, "parse_failure": 0, "prompt_tokens": 702, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 166, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 54.279, "latency_s_total": 54.279, "parse_failure": 0, "prompt_tokens": 649, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 115, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 77.949, "latency_s_total": 77.949, "parse_failure": 0, "prompt_tokens": 713, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 901, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 137.97, "latency_s_total": 137.97, "parse_failure": 0, "prompt_tokens": 1592, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "AFRM",
  "company_name": "Affirm Holdings, Inc.",
  "current_price": 74.8,
  "currency": "USD",
  "market_cap": 25239109632.0,
  "pe_ratio": 13.52622,
  "forward_pe": 15.493312,
  "week_52_high": 90.44,
  "week_52_low": 42.095,
  "financial_currency": "USD",
  "revenue": 4261082112.0,
  "net_income": 1929793024.0,
  "profit_margin_pct": 45.29,
  "dividend_yield": 0.0,
  "sector": "Financial Services",
  "industry": "Credit Services"
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
    "filing_date": "2026-08-27",
    "summary": "Item 1A. Risk Factors Investing in our Class A common stock involves a high degree of risk. You should consider carefully the material factors, risks and uncertainties described below that make an investment in our Company speculative or risky, together with all of the other information in this Form 10-K, including the section titled \u201cManagement\u2019s Discussion and Analysis of Financial Condition and Results of Operations\u201d and our consolidated financial statements and the accompanying notes included elsewhere in this Form 10-K, before deciding whether to invest in shares of our Class A common stock. The risks and uncertainties described below are not the only ones we face. Additional risks and uncertainties of which we are currently unaware or that we currently deem immaterial may also become"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-05-07",
    "summary": "Item 1A. Risk Factors The risks described under the heading \u201cRisk Factors\u201d in our Annual Report on Form 10-K for the fiscal year ended June 30, 2025 could materially and adversely affect our business, financial condition, results of operations, cash flows, future prospects, and the trading price of our Class A common stock. The risks and uncertainties described therein are not the only ones we face. Additional risks and uncertainties that we are unaware of or that we currently deem immaterial may also become important factors that adversely affect our business. You should carefully read and consider such risks, together with all of the other information in our Annual Report on Form 10-K for the fiscal year ended June 30, 2025, in this Quarterly Report on Form 10-Q (including the disclosure"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] Based on the provided text from the SEC EDGAR filings for ticker AFRM, the key takeaways regarding risks and business operations include:

**Competitive Landscape**
*   The pay-over-time industry faces intensifying competition due to low barriers to entry, emerging technologies, and innovation by large financial incumbents.
*   Competitors, particularly credit card issuing banks, possess significant advantages, including larger size, longer operating histories, diversified products, broader consumer and merchant bases, greater brand recognition, and the ability to cross-subsidize offerings.
*   Merchants are increasingly offering proprietary pay-over-time options, which are presented alongside competitor options at checkout.

**Commercial Partnerships**
*   The company relies on a small number of commercial partners, and the loss of significant relationships could materially adversely affect business results.
*   Many agreements with commercial partners are non-exclusive and lack transaction volume commitments, meaning partners may engage with competitors.
*   Success depends on attracting and retaining partners by demonstrating value propositions such as higher checkout conversion rates and increased average order value (AOV).

**Financial and Operational Risks**
*   **Funding and Lending:** The business relies on specific originating bank partners (Celtic Bank and Lead Bank) and card-issuing partners. Termination of these agreements without replacement could severely impact operations. Additionally, the company relies on various funding sources; if these are not renewed or are unavailable on acceptable terms, it could have a material adverse effect.
*   **Loan Performance:** If loans facilitated through the platform underperform, the company may incur financial losses, potentially losing the confidence of funding sources.
*   **Profitability and Growth:** There is no guarantee that the company can sustain revenue, Gross Merchandise Volume (GMV), or profitability growth rates. Quarterly results may fluctuate significantly.

**Regulatory and Legal Risks**
*   The business is subject to extensive and changing regulations, including federal, state, and local laws. Changes in regulatory enforcement or political landscapes could negatively impact operations.
*   If the originating bank partner model is deemed impermissible, the company could face violations of licensing, interest rate limit, lending, or brokering laws, resulting in penalties, fines, or litigation.
*   Litigation, regulatory actions, and compliance issues could lead to fines, penalties, and reputational harm.

**Other Key Risks**
*   **Interest Rates:** Further increases or prolonged periods of elevated market interest rates could adversely affect the business.
*   **Cybersecurity and Technology:** Disruptions in service, errors in platform operations, or cyber-attacks could prevent transaction processing and harm the business.
*   **Leadership and Talent:** The loss of the Founder and CEO or an inability to attract and retain highly skilled employees could materially affect the company.
*   **Stock Structure:** The dual-class structure concentrates voting control with Class B shareholders, which may depress the trading price of Class A common stock.
*   **International Expansion:** Expanding into new international geographies presents various challenges and risks.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Commercial Partner Relationships:** The inability to attract, retain, or grow relationships with commercial partners, including the loss of significant relationships and the non-exclusive nature of many agreements which may allow partners to work with competitors.
*   **Consumer Base:** The inability to attract new consumers or retain and grow relationships with existing consumers, which impacts revenue derived from consumer transaction volume.
*   **Competition:** Operating in a highly competitive industry with low barriers to entry, facing competition from legacy payment methods, mobile wallets, other pay-over-time solutions, and merchants offering proprietary options.
*   **Banking Partners:** Reliance on a small number of originating bank partners (specifically Celtic Bank and Lead Bank) and card issuing bank partners. Termination of these agreements without replacement could adversely affect the business.
*   **Growth and Profitability:** The potential inability to sustain revenue, Gross Merchandise Volume (GMV), and key operating metric growth rates, as well as the inability to sustain profitability.
*   **Funding:** Reliance on various funding sources, with the risk that existing arrangements may not be renewed or replaced on acceptable terms.
*   **Loan Performance:** Financial losses resulting from loans that do not perform or underperform, which could also lead to a loss of confidence among funding sources.
*   **Strategic Transactions:** The risk that acquisitions, investments, or other transactions may fail to achieve strategic objectives or disrupt ongoing operations.
*   **International Expansion:** Challenges and risks associated with expanding into new international geographies.
*   **Key Personnel:** The loss of the Founder and Chief Executive Officer, or the inability to attract and retain highly skilled employees.
*   **Financial Fluctuations:** Significant fluctuations in quarterly results that may not reflect underlying business performance.
*   **Legal and Regulatory Issues:** Exposure to litigation, regulatory actions, compliance issues, fines, penalties, and reputational harm. This includes extensive regulation subject to change and the risk that the originating bank partner model could be deemed impermissible.
*   **Interest Rates:** Adverse effects from further increases in market interest rates or prolonged periods of elevated interest rates.
*   **Economic Factors:** Revenue impact from the general economy, U.S. consumer creditworthiness, and the financial performance of commercial partners.
*   **Operational Disruptions:** Ineffective collection efforts on delinquent loans, or significant disruptions/errors in platform service or vendor services.
*   **Cybersecurity:** Risks related to the protection of confidential, proprietary, or sensitive information against cyber-attacks, misconduct, or other disruptions.
*   **Stock Structure:** The dual class structure of common stock concentrating voting control with Class B shareholders, which may depress the trading price of Class A common stock.

## Pre-written sections (judge input)

### Financial Health

Affirm Holdings, Inc. (AFRM) currently trades at $74.80 with a market capitalization of approximately $25.24 billion. The company demonstrates strong profitability, reporting a net income of $1.93 billion against $4.26 billion in revenue, resulting in an impressive profit margin of 45.29%. This robust margin is supported by a reasonable trailing P/E ratio of 13.53, suggesting the stock is not overly extended relative to its current earnings power. While the forward P/E of 15.49 indicates modest expected growth, the overall financial profile highlights efficient operations and solid earnings generation within the credit services sector.

### Recent Developments

Affirm Holdings, Inc. (AFRM) is currently trading at $74.80, reflecting a robust profit margin of 45.29% and a P/E ratio of 13.53, which suggests the market is pricing in strong near-term earnings potential. The company’s latest 10-Q filing for the quarter ended May 7, 2026, reiterates standard risk disclosures without introducing new material adverse events, indicating operational stability. Investors should monitor the upcoming 10-K filing scheduled for August 27, 2026, for detailed insights into long-term risk factors and strategic direction. With the stock trading below its 52-week high of $90.44, there is potential upside if the company maintains its current growth trajectory in the credit services sector.

### SEC Filing Highlights
Affirm faces intensifying competition from large financial incumbents and merchants offering proprietary pay-over-time options, which may pressure market share. The company’s operations are heavily reliant on a limited number of non-exclusive commercial and funding partners, creating significant risk if these relationships are terminated. Regulatory scrutiny remains a critical concern, particularly regarding the permissibility of the originating bank partner model and evolving lending laws. Additionally, the business must navigate macroeconomic headwinds, including elevated interest rates and potential loan underperformance, to sustain its growth and profitability trajectory.

### Risk Factors

*   **Regulatory and Legal Exposure:** The company faces significant risks from evolving regulations, potential litigation, and the specific legal vulnerability of its originating bank partner model, which could be deemed impermissible or result in substantial fines and reputational harm.
*   **Credit and Funding Dependency:** AFRM’s profitability is heavily reliant on the performance of its loan portfolio and its relationships with a limited number of key banking partners; increased delinquencies or the termination of these funding agreements could severely disrupt operations and capital access.
*   **Intense Competition and Market Volatility:** Operating in a low-barrier-to-entry market with numerous competitors, the company risks losing market share to legacy payment methods and proprietary merchant solutions, while also facing revenue pressure from fluctuating consumer creditworthiness and interest rate environments.

## Audited (Exec Summary + Outlook)

### Executive Summary
Affirm Holdings, Inc. (AFRM) operates as a key player in the credit services sector, leveraging a robust profit margin of 45.29% and a trailing P/E ratio of 13.53 to demonstrate efficient earnings generation. The stock is currently notable for trading below its 52-week high of $90.44, offering potential upside if the company sustains its current growth trajectory amid operational stability. The single most important near-term variable shaping the outcome is the regulatory clarity surrounding the permissibility of its originating bank partner model.

### Outlook
The directional outlook for Affirm is cautiously constructive, underpinned by strong current profitability and efficient operations, yet tempered by significant structural risks. Investors should closely monitor the regulatory landscape, specifically the legal viability of the originating bank partner model, as well as the stability of funding relationships with key banking partners. Tailwinds from the company's robust profit margins and potential upside from current valuation levels below the 52-week high could strengthen the thesis, provided that loan underperformance remains contained and competitive pressures from incumbents do not erode market share. Conversely, any adverse regulatory rulings or termination of critical funding agreements would significantly weaken the investment case by introducing existential operational and capital access risks.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "robust profit margin of 45.29%"
LABEL: SUPPORTED
REASON: The source data explicitly states `"profit_margin_pct": 45.29`, and the pre-written Financial Health section confirms "a profit margin of 45.29%."

---

CLAIM: "trailing P/E ratio of 13.53"
LABEL: SUPPORTED
REASON: The source data provides `"pe_ratio": 13.52622`; rounding to two decimal places yields 13.53, within the 0.1x tolerance threshold.

---

CLAIM: "trading below its 52-week high of $90.44"
LABEL: SUPPORTED
REASON: The source data confirms `"current_price": 74.8` and `"week_52_high": 90.44`; arithmetically, 74.80 < 90.44, so the positional claim holds and the figure $90.44 is explicitly present.

---

**OUTLOOK**

---

CLAIM: (no new quantitative figures, price targets, ratios, percentages, or forward-looking numbers are introduced in the Outlook section beyond directional/qualitative language)
LABEL: N/A
REASON: The Outlook section contains no additional specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers beyond those already evaluated above; all content is qualitative or directional in nature and therefore falls outside the scope of this audit.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | Profit margin of 45.29% | SUPPORTED |
| 2 | Trailing P/E ratio of 13.53 | SUPPORTED |
| 3 | Trading below 52-week high of $90.44 | SUPPORTED |

All three quantitative claims in the Executive Summary and Outlook are supported by the raw source data. No unsupported or inference-only claims were identified.
