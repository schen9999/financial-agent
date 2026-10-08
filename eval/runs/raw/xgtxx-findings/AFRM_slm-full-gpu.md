# AFRM — slm-full-gpu

## Metadata

ticker: AFRM
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: cf628ea7a8c2bd84407f8eb890856cc98777a21bdf3aa1f1b21de123e880e1c2
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 692, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 28.476, "latency_s_total": 28.476, "parse_failure": 0, "prompt_tokens": 2358, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 594, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 23.709, "latency_s_total": 23.709, "parse_failure": 0, "prompt_tokens": 3026, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 142, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 14.141, "latency_s_total": 14.141, "parse_failure": 0, "prompt_tokens": 711, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 161, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 18.715, "latency_s_total": 18.715, "parse_failure": 0, "prompt_tokens": 705, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 192, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 20.794, "latency_s_total": 20.794, "parse_failure": 0, "prompt_tokens": 667, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 137, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.985, "latency_s_total": 17.985, "parse_failure": 0, "prompt_tokens": 773, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 926, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 24.978, "latency_s_total": 24.978, "parse_failure": 0, "prompt_tokens": 1644, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "AFRM",
  "company_name": "Affirm Holdings, Inc.",
  "current_price": 75.31,
  "currency": "USD",
  "market_cap": 25411192832.0,
  "pe_ratio": 13.6184435,
  "forward_pe": 15.598947,
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
[From Pinecone cache] Based on the provided text from the SEC EDGAR filings for ticker AFRM, the key takeaways regarding the company's risk factors and business environment include:

**Competitive Landscape**
*   **Intensifying Competition:** The pay-over-time industry has low barriers to entry, leading to increased competition from emerging technologies and large financial incumbents.
*   **Merchant Alternatives:** Merchants are increasingly offering proprietary pay-over-time options, which are presented alongside the company’s offerings at checkout.
*   **Disadvantages vs. Incumbents:** Competitors, particularly credit card issuing banks, are substantially larger with longer operating histories. They possess advantages such as more diversified products, broader consumer and merchant bases, greater brand recognition, cross-selling capabilities, operational efficiencies, and the ability to cross-subsidize offerings.

**Operational and Partnership Risks**
*   **Commercial Partner Dependency:** The business relies on attracting and retaining commercial partners (merchants, e-commerce, and payment platforms). Many agreements are non-exclusive and lack transaction volume commitments, meaning partners may work with competitors.
*   **Banking Partners:** The company relies on a small number of originating bank partners (specifically Celtic Bank and Lead Bank) to facilitate loans and card-issuing banks for the Affirm Card. The termination of these agreements without replacement would materially adversely affect the business.
*   **Key Personnel:** The loss of the Founder and CEO, or the inability to attract and retain highly skilled employees, poses a significant risk.

**Financial and Economic Risks**
*   **Growth and Profitability:** There is no guarantee that the company can sustain revenue, Gross Merchandise Volume (GMV), or key operating metric growth rates, nor can it sustain profitability. Quarterly results may fluctuate significantly.
*   **Funding and Credit Risk:** The business relies on various funding sources; if these are not renewed or replaced on acceptable terms, it could have a material adverse effect. Additionally, if loans do not perform or underperform, the company may incur financial losses.
*   **Economic Sensitivity:** Revenue is significantly impacted by the general economy, U.S. consumer creditworthiness, and the financial performance of commercial partners.
*   **Interest Rates:** Further increases or prolonged periods of elevated market interest rates could adversely affect the business.

**Regulatory, Legal, and Technological Risks**
*   **Regulation and Compliance:** The business is subject to extensive and changing federal, state, and local regulations. Changes in laws, enforcement policies, or the political landscape could negatively impact operations. There is a risk that the originating bank partner model could be challenged as impermissible, leading to violations of licensing or lending laws.
*   **Litigation:** Legal actions, regulatory enforcement, and compliance issues could result in fines, penalties, judgments, and reputational harm.
*   **Cybersecurity and Platform Disruption:** The company faces risks from cyber-attacks, internal misconduct, and service disruptions that could prevent transaction processing or data protection.
*   **International Expansion:** Expanding into new international geographies presents various challenges and risks.

**Corporate Structure**
*   **Dual Class Stock:** The dual class structure concentrates voting control with Class B common stockholders (including executives and directors), which may depress the trading price of the Class A common stock.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Commercial Partner Relationships:** Inability to attract, retain, or grow relationships with commercial partners, including the loss of significant relationships and the non-exclusive nature of many agreements which may allow partners to work with competitors.
*   **Consumer Base:** Failure to attract new consumers or retain and grow relationships with existing consumers.
*   **Competition:** Operating in a highly competitive industry with low barriers to entry, facing competition from legacy payment methods, mobile wallets, other pay-over-time solutions, and merchants’ proprietary options.
*   **Banking Partners:** Reliance on a small number of originating bank partners (specifically Celtic Bank and Lead Bank) and card issuing bank partners; termination of these agreements without replacement could adversely affect the business.
*   **Growth Sustainability:** Inability to sustain revenue, Gross Merchandise Volume (GMV), and key operating metric growth rates.
*   **Funding:** Reliance on various funding sources; if these are not renewed, replaced, or provided on acceptable terms, it could materially adversely affect the business.
*   **Loan Performance:** Financial losses from loans that do not perform or underperform, which could impact financial condition and lose the confidence of funding sources.
*   **Strategic Transactions:** Inability to achieve strategic objectives or operational disruption from acquisitions, investments, alliances, or divestitures.
*   **International Expansion:** Challenges and risks associated with expanding into new international geographies.
*   **Key Personnel:** Loss of the Founder and CEO or inability to attract and retain highly skilled employees.
*   **Profitability:** Inability to sustain profitability.
*   **Financial Results:** Significant fluctuation in quarterly results that may not reflect underlying business performance.
*   **Legal and Regulatory:** Litigation, regulatory actions, compliance issues, fines, penalties, and reputational harm.
*   **Interest Rates:** Adverse effects from further increases or prolonged periods of elevated market interest rates.
*   **Economic Factors:** Revenue impact from the general economy, U.S. consumer creditworthiness, and the financial performance of commercial partners.
*   **Collections:** Ineffective or unsuccessful collection efforts on delinquent loans.
*   **Operational Disruptions:** Service disruptions or errors on the platform or related to vendors that prevent transaction processing or payment posting.
*   **Cybersecurity:** Risks to confidential, proprietary, or sensitive information from cyber-attacks, internal misconduct, viruses, or break-ins.
*   **Regulatory Environment:** Extensive regulation and oversight subject to change, including potential violations of licensing, interest rate limit, lending, or brokering laws if the originating bank partner model is challenged.
*   **Stock Structure:** The dual class structure concentrating voting control with Class B common stockholders, which may depress the trading price of Class A common stock.

## Pre-written sections (judge input)

### Financial Health

Affirm Holdings, Inc. (AFRM) is currently trading at $75.31 with a market capitalization of approximately $25.4 billion. The company demonstrates strong profitability, reporting a net income of $1.93 billion against revenues of $4.26 billion, resulting in an impressive profit margin of 45.29%. This robust margin is reflected in a trailing P/E ratio of 13.62, suggesting the stock may be reasonably valued relative to its earnings power. While the forward P/E of 15.60 indicates modest expected growth, the current financials highlight significant operational efficiency and cash generation capabilities.

### Recent Developments

Affirm Holdings, Inc. (AFRM) is currently trading at $75.31, reflecting a strong valuation with a P/E ratio of 13.62 and an impressive profit margin of 45.29%. The company recently filed its 10-K annual report on August 27, 2026, and its 10-Q quarterly report on May 7, 2026, both of which highlight significant risk factors that investors should carefully evaluate. Despite these disclosed uncertainties, Affirm continues to demonstrate robust financial health with a market capitalization exceeding $25 billion and substantial net income. Investors should monitor upcoming earnings reports to see if the company can sustain its high profitability amidst the identified operational risks.

### SEC Filing Highlights
Affirm faces intensifying competition from both emerging technologies and large financial incumbents, while merchants increasingly offer proprietary pay-over-time options that could displace the company’s market share. The business remains heavily dependent on a limited number of originating bank partners, such as Celtic and Lead Bank, where the loss of these agreements without replacement would materially adversely affect operations. Financial performance is highly sensitive to macroeconomic conditions, consumer creditworthiness, and interest rate fluctuations, with no guarantee of sustained revenue or profitability growth. Additionally, the company navigates significant regulatory risks, including potential challenges to its bank-partner lending model and evolving compliance requirements across federal and state jurisdictions.

### Risk Factors

*   **Regulatory and Banking Model Vulnerability:** The company faces significant legal and operational risks tied to its reliance on a small number of originating bank partners (Celtic and Lead Bank) and its "banking partner model," which is subject to evolving lending laws, interest rate limits, and potential regulatory challenges that could disrupt funding or compliance.
*   **Intense Competition and Partner Dependency:** Operating in a low-barrier-to-entry market, AFRM must continuously attract and retain both consumers and commercial partners who are free to work with competitors; failure to maintain these relationships or sustain growth metrics could materially harm revenue and market position.
*   **Credit Performance and Macroeconomic Sensitivity:** As a consumer credit provider, the business is highly exposed to loan defaults, collection inefficiencies, and broader economic downturns, where rising interest rates or declining consumer creditworthiness could lead to significant financial losses and reduced profitability.

## Audited (Exec Summary + Outlook)

### Executive Summary
Affirm Holdings, Inc. (AFRM) operates as a leading digital-first platform for buy-now-pay-later services, currently commanding a market capitalization of approximately $25.4 billion with a notable profit margin of 45.29%. The stock is notable for its attractive trailing P/E ratio of 13.62, which suggests reasonable valuation relative to its strong earnings power despite modest expected growth. The single most important near-term variable shaping the outcome is the company's ability to sustain its high profitability while navigating intensifying competition and evolving regulatory scrutiny of its banking partner model.

### Outlook
The directional outlook for Affirm is cautiously constructive, supported by strong current profitability and operational efficiency, but tempered by significant structural headwinds. Key variables to monitor include the stability of the banking partner relationships with Celtic and Lead Bank, the trajectory of consumer credit quality amid potential macroeconomic shifts, and the intensity of competitive pressures from both fintech entrants and merchant-owned financing options. The thesis would be strengthened by evidence of sustained margin expansion and successful navigation of regulatory changes without material disruption to funding sources; conversely, the view would weaken if regulatory challenges force a costly restructuring of the lending model or if rising default rates erode the current high profit margins.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of approximately $25.4 billion"
LABEL: SUPPORTED
REASON: The source data lists market_cap as $25,411,192,832, which rounds to approximately $25.4 billion, consistent with the pre-written Financial Health section.

---

CLAIM: "profit margin of 45.29%"
LABEL: SUPPORTED
REASON: The source data explicitly states profit_margin_pct = 45.29, and this figure appears verbatim in the pre-written sections.

---

CLAIM: "trailing P/E ratio of 13.62"
LABEL: SUPPORTED
REASON: The source data lists pe_ratio = 13.6184435, which rounds to 13.62; this figure also appears in the pre-written sections.

---

CLAIM: "modest expected growth" (in context of forward P/E)
LABEL: INFERENCE
REASON: The forward P/E of 15.60 (from source: forward_pe = 15.598947) is higher than the trailing P/E of 13.62, which directly implies the market prices in modest growth; this directional characterization is derivable from comparing the two present figures.

---

**OUTLOOK**

---

CLAIM: "banking partner relationships with Celtic and Lead Bank"
LABEL: SUPPORTED
REASON: Celtic Bank and Lead Bank are explicitly named as originating bank partners in both the RAG SEC Highlights and the pre-written SEC Filing Highlights and Risk Factors sections.

---

*(No additional specific quantitative figures, price targets, thresholds, ratios, named product milestones, or forward-looking numbers appear in the Outlook section. All remaining language — "cautiously constructive," "sustained margin expansion," "rising default rates," "costly restructuring," "material disruption" — is qualitative and directional, containing no specific quantitative claims subject to audit under the defined criteria.)*

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | Market cap ~$25.4 billion | SUPPORTED |
| 2 | Profit margin 45.29% | SUPPORTED |
| 3 | Trailing P/E 13.62 | SUPPORTED |
| 4 | Modest expected growth (forward P/E context) | INFERENCE |
| 5 | Celtic and Lead Bank as banking partners | SUPPORTED |
