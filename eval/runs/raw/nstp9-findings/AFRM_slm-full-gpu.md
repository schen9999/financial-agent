# AFRM — slm-full-gpu

## Metadata

ticker: AFRM
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 99412019285bde70be746c70c46b99184e90165776f757968c0a3add1d9c0367
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 614, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.701, "latency_s_total": 17.701, "parse_failure": 0, "prompt_tokens": 2358, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 607, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.562, "latency_s_total": 17.562, "parse_failure": 0, "prompt_tokens": 3026, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 138, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.588, "latency_s_total": 4.588, "parse_failure": 0, "prompt_tokens": 710, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 172, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.83, "latency_s_total": 5.83, "parse_failure": 0, "prompt_tokens": 704, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 173, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.852, "latency_s_total": 5.852, "parse_failure": 0, "prompt_tokens": 680, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 129, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 7.096, "latency_s_total": 7.096, "parse_failure": 0, "prompt_tokens": 695, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 900, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 11.652, "latency_s_total": 11.652, "parse_failure": 0, "prompt_tokens": 1604, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
*   Success depends on attracting and retaining partners by demonstrating value propositions such as higher conversion rates, increased average order value (AOV), and a robust technology platform.

**Financial and Operational Risks**
*   **Lending and Underwriting:** The business depends on originating bank partners (specifically Celtic Bank and Lead Bank) for underwriting and credit risk pricing. Termination of these agreements without replacement would be materially adverse.
*   **Funding:** The company relies on various funding sources; if these are not renewed or replaced on acceptable terms, it could negatively impact cash flows and operations.
*   **Loan Performance:** If loans facilitated through the platform underperform, the company may incur financial losses and lose the confidence of funding sources.
*   **Profitability and Growth:** There is no guarantee that revenue, Gross Merchandise Volume (GMV), or profitability growth rates can be sustained. Quarterly results may fluctuate significantly.

**Regulatory and Legal Risks**
*   The business is subject to extensive and changing federal, state, and local regulations.
*   There is a risk that the originating bank partner model could be challenged as impermissible, potentially leading to violations of licensing, interest rate limit, lending, or brokering laws.
*   Litigation, regulatory actions, and compliance issues could result in fines, penalties, and reputational harm.

**Other Key Risks**
*   **Interest Rates:** Increases in market interest rates or prolonged periods of elevated rates could adversely affect the business.
*   **Cybersecurity:** The company faces risks related to cyber-attacks, internal misconduct, and data breaches.
*   **Leadership and Talent:** The loss of the Founder and CEO, or an inability to retain highly skilled employees, could materially affect the business.
*   **Stock Structure:** The dual-class structure concentrates voting control with Class B shareholders, which may depress the trading price of Class A common stock.
*   **International Expansion:** Expanding into new international geographies presents various challenges and risks.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Commercial Partner Relationships:** The inability to attract, retain, or grow relationships with commercial partners, including the loss of significant relationships and the non-exclusive nature of many agreements which may allow partners to work with competitors.
*   **Consumer Acquisition and Retention:** The inability to attract new consumers or retain and grow relationships with existing ones, which directly impacts revenue derived from consumer transaction volume.
*   **Competition:** Operating in a highly competitive industry with low barriers to entry, facing competition from legacy payment methods, mobile wallets, other pay-over-time solutions, and merchants offering proprietary options.
*   **Banking Partnerships:** Reliance on a small number of originating bank partners (specifically Celtic Bank and Lead Bank) and card issuing bank partners. The termination of these agreements without replacement could materially adversely affect the business.
*   **Growth Sustainability:** The potential inability to sustain revenue, Gross Merchandise Volume (GMV), and key operating metric growth rates.
*   **Funding Sources:** Reliance on various funding sources, with the risk that existing arrangements may not be renewed or replaced on acceptable terms.
*   **Loan Performance:** Financial losses resulting from loans that do not perform or significantly underperform, which could also lead to a loss of confidence among funding sources.
*   **Strategic Transactions:** The risk that acquisitions, strategic investments, alliances, or divestitures may fail to achieve strategic objectives or disrupt ongoing operations.
*   **International Expansion:** Challenges and risks associated with expanding into new international geographies.
*   **Key Personnel and Talent:** The loss of the Founder and Chief Executive Officer, or the inability to attract and retain highly skilled employees.
*   **Profitability and Financial Results:** The potential inability to sustain profitability and significant fluctuations in quarterly results that may not reflect underlying business performance.
*   **Legal and Regulatory Issues:** Exposure to litigation, regulatory actions, compliance issues, fines, penalties, and reputational harm. This includes extensive regulation subject to change and the risk that the originating bank partner model could be deemed impermissible.
*   **Interest Rates:** Adverse effects from further increases in market interest rates or prolonged periods of elevated interest rates.
*   **Economic Factors:** Revenue impact from the general economy, U.S. consumer creditworthiness, and the financial performance of commercial partners.
*   **Collection Effectiveness:** Ineffective or unsuccessful collection efforts on delinquent loans.
*   **Platform and Vendor Disruptions:** Service disruptions or errors on the platform or related to vendors that prevent transaction processing or payment posting.
*   **Cybersecurity:** Risks related to the protection of confidential, proprietary, or sensitive information against cyber-attacks, internal misconduct, or other disruptions.
*   **Stock Structure:** The dual class structure of common stock concentrates voting control with Class B shareholders, which may depress the trading price of Class A common stock.

## Pre-written sections (judge input)

### Financial Health

Affirm Holdings, Inc. (AFRM) is currently trading at $74.75 with a market capitalization of approximately $25.2 billion. The company demonstrates strong profitability, reporting a net income of $1.93 billion against revenues of $4.26 billion, resulting in an impressive profit margin of 45.29%. This robust earnings performance is reflected in a trailing P/E ratio of 13.52, suggesting the stock may be reasonably valued relative to its current earnings power. While the company does not currently pay a dividend, its high margin profile indicates efficient operational execution and strong cash generation capabilities.

### Recent Developments

Affirm Holdings (AFRM) is currently trading at $74.75, reflecting a strong profit margin of 45.29% and a P/E ratio of 13.52, indicating robust operational efficiency despite the absence of dividend yields. The company's most recent 10-K filing on August 27, 2026, highlights significant risk factors that investors must weigh against the firm's substantial net income of nearly $1.93 billion. While the stock remains below its 52-week high of $90.44, the current valuation suggests market confidence in Affirm's credit services model within the financial sector. Investors should monitor upcoming quarterly reports for any shifts in these risk profiles, as the company continues to navigate a competitive landscape without offering shareholder dividends.

### SEC Filing Highlights
Affirm faces intensifying competition from large financial incumbents and merchant-owned alternatives, while relying on a limited number of non-exclusive commercial partners for growth. The company’s operational model depends heavily on originating bank partners for underwriting and credit risk, creating significant concentration risk if these relationships are terminated. Additionally, Affirm is subject to extensive regulatory scrutiny, particularly regarding the permissibility of its bank-partner lending structure, which could result in substantial legal and compliance costs. Financial performance remains sensitive to macroeconomic factors, including interest rate fluctuations and potential loan underperformance, with no guarantee of sustained profitability or growth rates.

### Risk Factors

*   **Regulatory and Legal Exposure:** The company faces significant risks from evolving consumer lending regulations, potential litigation, and the specific regulatory scrutiny surrounding its originating bank partner model, which could result in fines, operational restrictions, or reputational harm.
*   **Credit Performance and Funding Reliance:** Financial stability is heavily dependent on the performance of consumer loans and the continuity of funding from a limited number of banking partners; increased delinquencies or the loss of these critical funding sources could materially adversely affect liquidity and profitability.
*   **Intense Competition and Partner Dependency:** As a non-exclusive provider in a low-barrier-to-entry market, Affirm competes with legacy payment methods, proprietary merchant solutions, and other BNPL providers, while also relying on the retention of key commercial partners whose relationships may be terminated or diluted by competitors.

## Audited (Exec Summary + Outlook)

### Executive Summary
Affirm Holdings operates as a leading digital platform for modern commerce, leveraging a robust operational model that has generated $1.93 billion in net income against $4.26 billion in revenues. The stock is currently notable for its attractive trailing P/E ratio of 13.52 and strong 45.29% profit margin, suggesting the market may be undervaluing the company's earnings power relative to its peers. The single most important near-term variable shaping the investment outcome is the regulatory clarity surrounding Affirm’s bank-partner lending structure, which dictates both its operational continuity and competitive positioning.

### Outlook
The directional outlook for Affirm is cautiously constructive, supported by strong underlying profitability and a reasonable valuation multiple, but tempered by significant structural risks. Key variables to monitor include the trajectory of consumer credit quality, the stability of relationships with originating bank partners, and the evolving regulatory landscape regarding the permissibility of the company’s lending model. The investment thesis would be strengthened by sustained margin expansion and clear regulatory guidance that validates the bank-partner structure; conversely, the view would weaken materially if regulatory actions restrict the lending model or if macroeconomic headwinds lead to a sharp deterioration in loan performance or partner retention.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$1.93 billion in net income"
LABEL: SUPPORTED
REASON: The source data lists net_income = $1,929,793,024, which rounds to $1.93 billion, and the pre-written Financial Health and Recent Developments sections both confirm "net income of $1.93 billion" / "nearly $1.93 billion."

---

CLAIM: "$4.26 billion in revenues"
LABEL: SUPPORTED
REASON: The source data lists revenue = $4,261,082,112, which rounds to $4.26 billion, consistent with the pre-written Financial Health section's "$4.26 billion."

---

CLAIM: "trailing P/E ratio of 13.52"
LABEL: SUPPORTED
REASON: The source data lists pe_ratio = 13.517179, which rounds to 13.52; the pre-written sections also state 13.52.

---

CLAIM: "strong 45.29% profit margin"
LABEL: SUPPORTED
REASON: The source data explicitly lists profit_margin_pct = 45.29, confirmed in the pre-written Financial Health and Recent Developments sections.

---

**OUTLOOK**

The Outlook section contains no specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers. All statements are qualitative and directional (e.g., "cautiously constructive," "sustained margin expansion," "sharp deterioration"). There are therefore no quantitative or forward-looking numerical claims to audit in this section.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | $1.93 billion in net income | SUPPORTED |
| 2 | $4.26 billion in revenues | SUPPORTED |
| 3 | Trailing P/E ratio of 13.52 | SUPPORTED |
| 4 | 45.29% profit margin | SUPPORTED |

All four quantitative claims in the audited sections are **SUPPORTED** by the raw source data. The Outlook section introduces no additional quantitative claims requiring verification.
