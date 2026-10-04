# AFRM — slm-full-cpu

## Metadata

ticker: AFRM
arm: slm-full-cpu
judge_prompt_version: v2
context_sha256: f68673562c6033d2504a0e4f2deaf75173a982a6ce13da4d6c8f544d6d1e5ad1
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 658, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 184.991, "latency_s_total": 184.991, "parse_failure": 0, "prompt_tokens": 2358, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 597, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 178.742, "latency_s_total": 178.742, "parse_failure": 0, "prompt_tokens": 3026, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 145, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 44.724, "latency_s_total": 44.724, "parse_failure": 0, "prompt_tokens": 674, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 145, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 44.724, "latency_s_total": 44.724, "parse_failure": 0, "prompt_tokens": 668, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 164, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 58.54, "latency_s_total": 58.54, "parse_failure": 0, "prompt_tokens": 670, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 111, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 65.993, "latency_s_total": 65.993, "parse_failure": 0, "prompt_tokens": 739, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 859, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 135.872, "latency_s_total": 135.872, "parse_failure": 0, "prompt_tokens": 1510, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "AFRM",
  "company_name": "Affirm Holdings, Inc.",
  "current_price": 70.77,
  "currency": "USD",
  "market_cap": 23879301120.0,
  "pe_ratio": 12.797467,
  "forward_pe": 14.658577,
  "week_52_high": 90.44,
  "week_52_low": 42.095,
  "revenue": 4261082112.0,
  "net_income": 1929793024.0,
  "profit_margin": 0.45289,
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
[From Pinecone cache] Based on the provided text from the SEC EDGAR filings for ticker AFRM, the key takeaways regarding risks and business operations include:

**Competitive Landscape**
*   The pay-over-time industry faces intensifying competition due to low barriers to entry, emerging technologies, and innovation by large financial incumbents.
*   Competitors, particularly credit card issuing banks, possess significant advantages, including larger size, longer operating histories, diversified products, broader consumer and merchant bases, greater brand recognition, and the ability to cross-subsidize offerings.
*   Merchants are increasingly offering proprietary pay-over-time options, which are presented alongside competitor options at checkout.

**Commercial Partnerships**
*   The business relies heavily on a small number of commercial partners, including originating banks (Celtic Bank and Lead Bank) and card-issuing bank partners. The loss of these relationships, or the inability to replace them, could materially adversely affect the business.
*   Many agreements with commercial partners are non-exclusive and lack transaction volume commitments, meaning partners may engage with competitors.
*   Success depends on attracting and retaining partners by demonstrating value propositions such as higher conversion rates, increased average order value (AOV), and a robust technology platform.

**Financial and Operational Risks**
*   **Growth and Profitability:** The company may not be able to sustain current revenue, Gross Merchandise Volume (GMV), or growth rates, nor sustain profitability. Quarterly results may fluctuate significantly.
*   **Funding and Credit Risk:** The business relies on various funding sources that may not be renewed on acceptable terms. If loans facilitated through the platform underperform, the company may incur financial losses, potentially losing the confidence of funding sources.
*   **Interest Rates:** Further increases or prolonged periods of elevated market interest rates could adversely affect the business.
*   **Economic Factors:** Revenue is significantly impacted by the general economy, U.S. consumer creditworthiness, and the financial performance of commercial partners.

**Regulatory and Legal Risks**
*   The business is subject to extensive and changing regulations, including federal, state, and local laws. Changes in regulatory enforcement or political landscapes could negatively impact operations.
*   There is a risk that the originating bank partner model could be challenged as impermissible, potentially leading to violations of licensing, interest rate limit, lending, or brokering laws, resulting in fines, penalties, or litigation.
*   Litigation, regulatory actions, and compliance issues could lead to fines, penalties, and reputational harm.

**Other Key Risks**
*   **Leadership and Talent:** The loss of the Founder and CEO, or the inability to attract and retain highly skilled employees, could materially affect the business.
*   **International Expansion:** Expanding into new international geographies presents various challenges and risks.
*   **Technology and Security:** Disruptions in service, errors in platform operations, or cyber-attacks (including internal misconduct) could prevent transaction processing and adversely affect the business.
*   **Stock Structure:** The dual-class structure concentrates voting control with Class B common stockholders, which may depress the trading price of Class A common stock.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Commercial Partner Relationships:** The inability to attract, retain, or grow relationships with commercial partners, including the loss of significant relationships and the non-exclusive nature of many agreements which may allow partners to work with competitors.
*   **Consumer Base:** The inability to attract new consumers or retain and grow relationships with existing ones, which impacts revenue derived from consumer transaction volume.
*   **Competition:** Operating in a highly competitive industry with low barriers to entry, facing competition from legacy payment methods, mobile wallets, other pay-over-time solutions, and merchants’ proprietary options.
*   **Banking Partners:** Reliance on a small number of originating bank partners (specifically Celtic Bank and Lead Bank) and card issuing bank partners. Termination of these agreements without replacement could materially adversely affect the business.
*   **Growth Sustainability:** The potential inability to sustain revenue, Gross Merchandise Volume (GMV), and key operating metric growth rates.
*   **Funding:** Reliance on various funding sources, with the risk that existing arrangements may not be renewed or replaced on acceptable terms.
*   **Loan Performance:** Financial losses resulting from loans that do not perform or significantly underperform, which could also lead to a loss of confidence among funding sources.
*   **Strategic Transactions:** The risk that acquisitions, strategic investments, alliances, or divestitures may fail to achieve strategic objectives or disrupt ongoing operations.
*   **International Expansion:** Challenges and risks associated with expanding into new international geographies.
*   **Key Personnel:** The loss of the Founder and Chief Executive Officer, or the inability to attract and retain highly skilled employees.
*   **Profitability and Financial Results:** The potential inability to sustain profitability and significant fluctuations in quarterly results that may not reflect underlying business performance.
*   **Legal and Regulatory Issues:** Exposure to litigation, regulatory actions, compliance issues, fines, penalties, and reputational harm. This includes extensive regulation subject to change and the risk that the originating bank partner model could be deemed impermissible.
*   **Interest Rates:** Adverse effects from further increases in market interest rates or prolonged periods of elevated interest rates.
*   **Economic Factors:** Revenue impact from the general economy, U.S. consumer creditworthiness, and the financial performance of commercial partners.
*   **Collection Effectiveness:** Ineffective collection efforts on delinquent loans adversely affecting loan performance.
*   **Operational Disruptions:** Service disruptions or errors on the platform or involving vendors that prevent transaction processing or payment posting.
*   **Cybersecurity:** Risks to confidential, proprietary, or sensitive information from cyber-attacks, internal misconduct, viruses, or break-ins.
*   **Stock Structure:** The dual class structure of common stock concentrates voting control with Class B shareholders, which may depress the trading price of Class A common stock.

## Pre-written sections (judge input)

### Financial Health

Affirm Holdings, Inc. (AFRM) is currently trading at $70.77 with a market capitalization of approximately $23.88 billion. The company demonstrates strong profitability, reporting a net income of $1.93 billion against revenues of $4.26 billion, resulting in an impressive profit margin of 45.29%. This robust margin is reflected in a trailing P/E ratio of 12.80, suggesting the stock may be undervalued relative to its earnings power. With a forward P/E of 14.66, the valuation indicates moderate growth expectations while maintaining a healthy balance sheet within the credit services sector.

### Recent Developments

Affirm Holdings, Inc. recently filed its Annual Report on Form 10-K on August 27, 2026, and its Quarterly Report on Form 10-Q on May 7, 2026. These filings reiterate significant risk factors, warning that uncertainties could materially and adversely affect the company's business, financial condition, and stock price. Investors should carefully review these disclosures alongside the company's strong recent profitability metrics, which include a 45.3% profit margin and a P/E ratio of 12.8. The reports emphasize that additional, currently unknown risks may emerge, necessitating cautious evaluation of the stock's speculative nature.

### SEC Filing Highlights
Affirm faces intensifying competition from large financial incumbents and merchant-owned alternatives, while relying heavily on non-exclusive partnerships with a limited number of originating banks. The company highlights significant risks related to sustaining current growth rates and profitability amid fluctuating quarterly results and elevated market interest rates. Operational resilience is further challenged by potential regulatory shifts regarding the bank-partner model and broader economic pressures on consumer creditworthiness. Additionally, the firm warns of vulnerabilities in its technology infrastructure and the concentration of voting control within its dual-class stock structure.

### Risk Factors

*   **Regulatory and Legal Exposure:** The company faces significant risks from evolving consumer lending regulations, potential litigation, and the specific regulatory scrutiny surrounding its originating bank partner model, which could result in fines, operational restrictions, or reputational harm.
*   **Credit Performance and Funding Reliance:** Financial stability is heavily dependent on the performance of consumer loans and the continuity of funding arrangements with a limited number of banking partners; rising interest rates or economic downturns could increase delinquencies and restrict access to capital.
*   **Intense Competition and Partner Dependency:** As a non-exclusive provider in a low-barrier-to-entry market, AFRM risks losing commercial partners to competitors or proprietary merchant solutions, while also facing pressure to attract and retain consumers in a crowded pay-over-time landscape.

## Audited (Exec Summary + Outlook)

### Executive Summary
Affirm Holdings, Inc. operates as a key player in the consumer credit services sector, leveraging a strong profitability profile with a 45.29% profit margin and a trailing P/E ratio of 12.80 to support its market position. The stock is notable now for its apparent valuation disconnect, where robust earnings power contrasts with significant regulatory and competitive risks highlighted in recent 10-K and 10-Q filings. The single most important near-term variable shaping the outcome is the regulatory environment surrounding its bank-partner model, which dictates both operational continuity and long-term strategic viability.

### Outlook
The directional outlook for Affirm is cautiously constructive, anchored by exceptional current profitability but tempered by substantial structural and regulatory headwinds. Investors should closely monitor the stability of the bank-partner model and the broader regulatory landscape, as any adverse shifts here would significantly weaken the investment thesis by threatening funding continuity and operational flexibility. Conversely, the thesis would be strengthened if the company demonstrates resilience against intensifying competition from incumbents and successfully navigates economic pressures without compromising its high-margin profile. While the current valuation metrics suggest room for appreciation, the speculative nature of the business requires vigilance regarding emerging risks and the sustainability of growth rates in a fluctuating interest rate environment.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically identify every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections, then evaluate each.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "45.29% profit margin"
LABEL: SUPPORTED
REASON: The raw source data explicitly states `"profit_margin": 0.45289`, which equals 45.29% (rounded to two decimal places), and the pre-written Financial Health section confirms "profit margin of 45.29%."

---

CLAIM: "trailing P/E ratio of 12.80"
LABEL: SUPPORTED
REASON: The raw source data explicitly states `"pe_ratio": 12.797467`, which rounds to 12.80, and the pre-written Financial Health section confirms "trailing P/E ratio of 12.80."

---

CLAIM: "recent 10-K and 10-Q filings"
LABEL: SUPPORTED
REASON: The SEC Filing Summaries confirm a 10-K filed 2026-08-27 and a 10-Q filed 2026-05-07, both explicitly present in the source data.

---

**OUTLOOK**

---

CLAIM: "exceptional current profitability" (directional/qualitative)
LABEL: INFERENCE
REASON: This is a qualitative characterization directly derivable from the 45.29% profit margin figure present in the source data, which is an objectively high margin for the credit services sector.

---

*(No additional specific quantitative figures, price targets, thresholds, ratios, named product milestones, or forward-looking numbers appear in the Outlook section beyond what is already captured above. The remaining claims in the Outlook — "cautiously constructive," "structural and regulatory headwinds," "bank-partner model," "intensifying competition from incumbents," "high-margin profile," "speculative nature," "sustainability of growth rates," "fluctuating interest rate environment" — are qualitative characterizations or directional statements without specific quantitative content requiring arithmetic verification.)*

---

**SUMMARY NOTE:** The Executive Summary and Outlook sections contain only two specific quantitative figures (45.29% profit margin and 12.80 trailing P/E), both of which are SUPPORTED by the raw source data. No price targets, forward P/E references, market cap figures, revenue figures, net income figures, 52-week high/low references, or other specific metrics from the source data appear in these two sections, so no further claims require evaluation. The forward P/E of 14.66 and other figures present in the pre-written sections were not carried into the Executive Summary or Outlook and therefore fall outside the audit scope.
