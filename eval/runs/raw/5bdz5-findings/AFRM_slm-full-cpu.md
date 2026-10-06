# AFRM — slm-full-cpu

## Metadata

ticker: AFRM
arm: slm-full-cpu
judge_prompt_version: v2
context_sha256: 0878e58b7621a7fd62045ddeafd25abc07efae05bce8bb803e8482ed5dc8a891
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 730, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 199.926, "latency_s_total": 199.926, "parse_failure": 0, "prompt_tokens": 2358, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 654, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 191.633, "latency_s_total": 191.633, "parse_failure": 0, "prompt_tokens": 3026, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 144, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 51.743, "latency_s_total": 51.743, "parse_failure": 0, "prompt_tokens": 690, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 122, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 42.691, "latency_s_total": 42.691, "parse_failure": 0, "prompt_tokens": 684, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 221, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 73.907, "latency_s_total": 73.907, "parse_failure": 0, "prompt_tokens": 727, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 113, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 60.034, "latency_s_total": 60.034, "parse_failure": 0, "prompt_tokens": 811, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 859, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 130.74, "latency_s_total": 130.74, "parse_failure": 0, "prompt_tokens": 1580, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "AFRM",
  "company_name": "Affirm Holdings, Inc.",
  "current_price": 74.75,
  "currency": "USD",
  "market_cap": 25222238208.0,
  "pe_ratio": 13.517179,
  "forward_pe": 15.482955,
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
[]

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
[From Pinecone cache] Based on the provided text from the SEC EDGAR filings for ticker AFRM, here are the key takeaways regarding the company's risk factors and business environment:

**Intense and Evolving Competition**
The pay-over-time industry faces low barriers to entry, leading to intensifying competition. Competitors include large financial incumbents, such as credit card issuing banks, which possess significant advantages including diversified products, broader consumer and merchant bases, greater brand recognition, operational efficiencies, and the ability to cross-subsidize offerings. Additionally, merchants are increasingly offering proprietary pay-over-time options, which are presented alongside competitor options at checkout.

**Reliance on Commercial Partners**
The company’s business is heavily dependent on attracting, retaining, and growing relationships with commercial partners (merchants, e-commerce platforms, and payment platforms). Many of these agreements are non-exclusive and lack transaction volume commitments, meaning partners may engage with competitors. The success of these relationships, particularly with large early-stage retailers, is critical for revenue growth but is often unpredictable and not fully within the company's control.

**Dependence on Specific Bank Partners**
The company relies on a small number of originating bank partners, specifically Celtic Bank and Lead Bank, to facilitate substantially all loans through its platform. It also relies on a small number of card-issuing bank partners for the Affirm Card. The termination of these agreements without timely replacement could materially adversely affect the business. Furthermore, if this originating bank partner model is challenged or deemed impermissible, the company could face violations of licensing, interest rate limit, lending, or brokering laws.

**Financial and Operational Risks**
*   **Loan Performance:** If loans facilitated through the platform underperform, the company may incur financial losses, potentially impacting its financial condition and the confidence of its funding sources.
*   **Funding:** The business relies on various funding sources. If these arrangements are not renewed or replaced on acceptable terms, it could have a material adverse effect on cash flows and operations.
*   **Profitability and Growth:** There is no guarantee that the company can sustain its revenue, Gross Merchandise Volume (GMV), or growth rates, nor can it guarantee sustained profitability. Quarterly results may fluctuate significantly.
*   **Interest Rates:** Further increases or prolonged periods of elevated market interest rates could adversely affect the business.

**Regulatory, Legal, and Cybersecurity Risks**
*   **Regulation:** The business is subject to extensive and changing federal, state, and local regulations. Changes in laws, enforcement policies, or the political landscape may negatively impact operations.
*   **Litigation:** Regulatory actions, compliance issues, and litigation could result in fines, penalties, judgments, and reputational harm.
*   **Cybersecurity:** The company faces risks related to cyber-attacks, internal misconduct, and other disruptions that could compromise confidential or proprietary information.
*   **Platform Disruption:** Errors or disruptions in the platform or vendor services could prevent transaction processing and have a material adverse effect on the business.

**Leadership and Structural Risks**
*   **Key Personnel:** The loss of the Founder and Chief Executive Officer, or the inability to attract and retain highly skilled employees, could materially adversely affect the business.
*   **Dual-Class Stock Structure:** The dual-class structure concentrates voting control with Class B common stockholders (including executives and directors), which may depress the trading price of the Class A common stock.
*   **International Expansion:** Expanding into new international geographies presents various challenges and risks.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Commercial Partner Relationships:** The inability to attract, retain, or grow relationships with commercial partners (merchants, e-commerce platforms, and payment platforms), particularly given that many agreements are non-exclusive, lack transaction volume commitments, and can be terminated with short notice.
*   **Consumer Acquisition and Retention:** The failure to attract new consumers or retain and grow relationships with existing ones, which directly impacts revenue derived from consumer transaction volume.
*   **Competition:** Operating in a highly competitive industry with low barriers to entry, facing competition from legacy payment methods (credit/debit cards), mobile wallets, other pay-over-time solutions (e.g., PayPal, Block, Klarna), and proprietary merchant options.
*   **Banking and Underwriting Dependencies:** Reliance on a small number of originating bank partners (specifically Celtic Bank and Lead Bank) and card-issuing bank partners for loan origination and underwriting. The termination of these agreements without replacement could materially adversely affect the business.
*   **Funding Sources:** Reliance on various funding sources; if these are not renewed, replaced, or provided on acceptable terms, it could have a material adverse effect on the business.
*   **Loan Performance:** Financial losses resulting from loans that do not perform or significantly underperform, which could also lead to a loss of confidence among funding sources.
*   **Growth Sustainability:** The potential inability to sustain revenue, Gross Merchandise Volume (GMV), and key operating metric growth rates.
*   **Strategic Transactions:** Risks associated with acquisitions, strategic investments, alliances, or divestitures, including the potential failure to achieve strategic objectives or operational disruption.
*   **International Expansion:** Challenges and risks related to expanding into new international geographies.
*   **Key Personnel and Talent:** The loss of the Founder and Chief Executive Officer, or the inability to attract and retain highly skilled employees.
*   **Profitability and Financial Results:** The potential inability to sustain profitability and significant fluctuations in quarterly results that may not reflect underlying business performance.
*   **Legal and Regulatory Issues:** Exposure to litigation, regulatory actions, compliance issues, fines, penalties, and reputational harm. This includes extensive regulation subject to change, and the risk that the originating bank partner model could be deemed impermissible, leading to violations of licensing, interest rate, lending, or brokering laws.
*   **Interest Rates:** Adverse effects from further increases in market interest rates or prolonged periods of elevated interest rates.
*   **Economic Factors:** Revenue impact from the general economy, U.S. consumer creditworthiness, and the financial performance of commercial partners.
*   **Operational Disruptions:** Ineffective collection efforts on delinquent loans, or significant disruptions/errors in platform services or vendor operations.
*   **Cybersecurity:** Risks to confidential, proprietary, or sensitive information from cyber-attacks, internal misconduct, viruses, or break-ins.
*   **Dual Class Stock Structure:** The concentration of voting control with Class B common stockholders (including executives and directors), which may depress the trading price of Class A common stock.

## Pre-written sections (judge input)

### Financial Health

Affirm Holdings, Inc. (AFRM) is currently trading at $74.75 with a market capitalization of approximately $25.2 billion. The company demonstrates robust profitability, reporting a net income of $1.93 billion against revenues of $4.26 billion, resulting in an impressive profit margin of 45.29%. This strong earnings performance is reflected in a trailing P/E ratio of 13.52, suggesting the stock may be reasonably valued relative to its current earnings power. While the forward P/E of 15.48 indicates modest expected growth, the high margin profile underscores the efficiency of its credit services model.

### Recent Developments

Affirm Holdings, Inc. (AFRM) recently filed its Annual Report on Form 10-K on August 27, 2026, and its Quarterly Report on Form 10-Q on May 7, 2026, with both filings emphasizing significant risk factors that could adversely affect business operations and stock price. These regulatory submissions highlight the speculative nature of the investment, urging shareholders to carefully consider uncertainties beyond those currently identified. Investors should monitor these filings closely for updates on material risks that may impact the company's financial condition and future prospects.

### SEC Filing Highlights
Affirm faces intensifying competition from financial incumbents and merchants offering proprietary pay-over-time options, while its growth remains heavily dependent on non-exclusive relationships with key commercial and originating bank partners. The company’s operational stability is closely tied to the continued performance of loans facilitated through its platform and the availability of favorable funding sources, with no guarantee of sustained profitability or GMV growth. Additionally, Affirm must navigate a complex landscape of evolving federal and state regulations, potential litigation, and cybersecurity risks that could materially impact its business and financial condition.

### Risk Factors

*   **Regulatory and Banking Model Vulnerability:** The company faces significant legal and regulatory risks, particularly concerning its reliance on a small number of originating bank partners (Celtic Bank and Lead Bank). If this "banking partner model" is deemed impermissible or if these agreements are terminated without replacement, it could violate lending laws and materially disrupt operations.
*   **Intense Competition and Partner Dependency:** AFRM operates in a highly competitive landscape with low barriers to entry, facing rivals from legacy payment methods, fintechs (e.g., Klarna, PayPal), and proprietary merchant solutions. Furthermore, its growth is heavily dependent on attracting and retaining commercial partners through non-exclusive, short-notice agreements, creating high churn risk.
*   **Credit Performance and Funding Sensitivity:** The business is exposed to loan performance risks, where underperforming loans can lead to financial losses and erode confidence among funding sources. This is compounded by reliance on specific funding channels and the potential adverse impact of rising interest rates on both consumer creditworthiness and the company’s profitability.

## Audited (Exec Summary + Outlook)

### Executive Summary
Affirm Holdings, Inc. (AFRM) operates as a leading fintech lender with a market capitalization of approximately $25.2 billion, distinguished by its robust profitability and a 45.29% net profit margin. The stock is currently notable for its reasonable valuation relative to earnings power, yet it faces heightened scrutiny due to recent regulatory filings that underscore significant operational and legal uncertainties. The single most important near-term variable shaping the investment outcome is the regulatory stability of its banking partner model and the company's ability to maintain its funding sources amidst intensifying competition.

### Outlook
The directional outlook for Affirm is cautiously constructive, anchored by its strong margin profile and efficient credit model, but heavily contingent on regulatory clarity and competitive positioning. Investors should closely monitor the stability of its banking partner relationships and the evolving regulatory landscape, as any adverse rulings regarding its lending structure or funding sources would significantly weaken the investment thesis. Conversely, the thesis would be strengthened by evidence of sustained partner retention, resilient loan performance despite economic headwinds, and successful navigation of compliance challenges without material disruption to operations.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of approximately $25.2 billion"
LABEL: SUPPORTED
REASON: The raw source data lists market_cap as $25,222,238,208.0, which rounds to approximately $25.2 billion, consistent with the pre-written Financial Health section.

---

CLAIM: "45.29% net profit margin"
LABEL: SUPPORTED
REASON: The raw source data explicitly states profit_margin_pct = 45.29, and the pre-written Financial Health section confirms "profit margin of 45.29%."

---

**OUTLOOK**

The Outlook section contains no specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers. It is composed entirely of qualitative, directional, and conditional statements (e.g., "cautiously constructive," "strong margin profile," "regulatory clarity," "competitive positioning"). There are therefore no quantitative or forward-looking numerical claims to audit in this section.

---

**SUMMARY**

Only two quantitative claims appear across both audited sections, and both are fully supported by the source data. The Outlook section is purely qualitative and contains no auditable numerical or forward-looking quantitative claims.
