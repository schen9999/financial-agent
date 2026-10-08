# AFRM — slm-full-gpu

## Metadata

ticker: AFRM
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 4dc6b2c7c42cee31a841aaddd24104172507eaa763e04fd563d49a3ea9dda339
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 621, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.22, "latency_s_total": 19.22, "parse_failure": 0, "prompt_tokens": 2358, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 629, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 20.876, "latency_s_total": 20.876, "parse_failure": 0, "prompt_tokens": 3026, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 142, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.244, "latency_s_total": 5.244, "parse_failure": 0, "prompt_tokens": 711, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 162, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 10.571, "latency_s_total": 10.571, "parse_failure": 0, "prompt_tokens": 705, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 150, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 13.932, "latency_s_total": 13.932, "parse_failure": 0, "prompt_tokens": 702, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 119, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 12.976, "latency_s_total": 12.976, "parse_failure": 0, "prompt_tokens": 702, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 858, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 30.985, "latency_s_total": 30.985, "parse_failure": 0, "prompt_tokens": 1526, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
[From Pinecone cache] Based on the provided text from the SEC EDGAR filings for ticker AFRM, the key takeaways regarding risks and business operations include:

**Competitive Landscape**
*   The pay-over-time industry faces intensifying competition due to low barriers to entry, emerging technologies, and innovation by large financial incumbents.
*   Competitors, particularly credit card issuing banks, possess significant advantages over the company, including larger size, longer operating histories, more diversified products, broader consumer and merchant bases, greater brand recognition, and the ability to cross-subsidize offerings.
*   Merchants are increasingly offering proprietary pay-over-time options, which are presented alongside the company’s offerings at checkout.

**Commercial Partnerships**
*   The business relies heavily on a small number of commercial partners, including originating bank partners (Celtic Bank and Lead Bank) and card-issuing bank partners. The loss of these relationships, or the inability to replace them, could materially adversely affect the business.
*   Many agreements with commercial partners are non-exclusive and lack transaction volume commitments, meaning partners may engage with competitors.
*   Success depends on attracting and retaining partners by demonstrating value propositions such as higher conversion rates and increased average order value (AOV).

**Financial and Operational Risks**
*   **Growth and Profitability:** The company may not be able to sustain current revenue, Gross Merchandise Volume (GMV), or growth rates, nor sustain profitability. Quarterly results may fluctuate significantly.
*   **Funding and Credit Risk:** The business relies on various funding sources; if these are not renewed or replaced on acceptable terms, it could have a material adverse effect. Additionally, if loans facilitated through the platform underperform, the company may incur financial losses.
*   **Interest Rates:** Further increases or prolonged periods of elevated market interest rates could adversely affect the business.

**Regulatory and Legal Risks**
*   The business is subject to extensive and changing federal, state, and local regulations. Changes in laws or enforcement priorities could negatively impact operations.
*   There is a risk that the originating bank partner model could be challenged as impermissible, potentially leading to violations of licensing, interest rate limit, lending, or brokering laws, resulting in penalties or litigation.
*   Litigation, regulatory actions, and compliance issues could result in fines, penalties, and reputational harm.

**Other Key Risks**
*   **Cybersecurity and Technology:** Disruptions in service, errors in platform operations, or cyber-attacks could prevent transaction processing and adversely affect the business.
*   **Leadership and Talent:** The loss of the Founder and CEO, or the inability to attract and retain highly skilled employees, could materially affect the company.
*   **International Expansion:** Expanding into new international geographies presents various challenges and risks.
*   **Stock Structure:** The dual-class structure concentrates voting control with Class B common stockholders, which may depress the trading price of Class A common stock.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Commercial Partner Relationships:** The inability to attract, retain, or grow relationships with commercial partners, including the loss of significant relationships and the non-exclusive nature of many agreements which may allow partners to work with competitors.
*   **Consumer Acquisition and Retention:** The inability to attract new consumers or retain and grow relationships with existing ones, which directly impacts revenue derived from consumer transaction volume.
*   **Competition:** Operating in a highly competitive industry with low barriers to entry, facing competition from legacy payment methods, mobile wallets, other pay-over-time solutions, and merchants offering proprietary options.
*   **Banking and Underwriting Partners:** Reliance on a small number of originating bank partners (specifically Celtic Bank and Lead Bank) and card issuing bank partners. The termination of these agreements or the inability to replace them could materially adversely affect the business.
*   **Growth Sustainability:** The potential inability to sustain revenue, Gross Merchandise Volume (GMV), and key operating metric growth rates.
*   **Funding Sources:** Reliance on various funding sources, with the risk that existing arrangements may not be renewed or replaced on acceptable terms.
*   **Loan Performance:** Financial losses resulting from loans that do not perform or significantly underperform, which could also lead to a loss of confidence among funding sources.
*   **Strategic Transactions:** The risk that acquisitions, strategic investments, or other transactions may fail to achieve strategic objectives or disrupt ongoing operations.
*   **International Expansion:** Challenges and risks associated with expanding into new international geographies.
*   **Key Personnel and Talent:** The loss of the Founder and Chief Executive Officer, or the inability to attract and retain highly skilled employees.
*   **Profitability and Financial Results:** The potential inability to sustain profitability and significant fluctuations in quarterly results that may not reflect underlying business performance.
*   **Legal and Regulatory Issues:** Exposure to litigation, regulatory actions, compliance issues, fines, penalties, and reputational harm. This includes extensive regulation subject to change, the risk that the originating bank partner model could be deemed impermissible, and the impact of changing political landscapes on enforcement policies.
*   **Interest Rates:** Adverse effects from further increases in market interest rates or prolonged periods of elevated interest rates.
*   **Economic and Consumer Factors:** Revenue impacted by the general economy, U.S. consumer creditworthiness, and the financial performance of commercial partners.
*   **Collection Effectiveness:** Ineffective or unsuccessful collection efforts on delinquent loans adversely affecting loan performance.
*   **Platform and Vendor Disruptions:** Service disruptions or errors on the platform or related to vendors that prevent transaction processing or payment posting.
*   **Cybersecurity and Data Protection:** Risks related to cyber-attacks, internal misconduct, viruses, or break-ins compromising confidential, proprietary, or sensitive information.
*   **Stock Structure:** The dual class structure of common stock concentrates voting control with Class B shareholders, which may depress the trading price of Class A common stock.

## Pre-written sections (judge input)

### Financial Health

Affirm Holdings, Inc. (AFRM) currently trades at $75.31 with a market capitalization of approximately $25.4 billion. The company demonstrates strong profitability, reporting a net income of $1.93 billion against $4.26 billion in revenue, resulting in an impressive profit margin of 45.29%. This robust earnings performance supports a trailing P/E ratio of 13.62, suggesting the stock is reasonably valued relative to its recent earnings power. While the forward P/E of 15.60 indicates modest expected growth, the current valuation reflects a balance between strong historical margins and future market expectations.

### Recent Developments

Affirm Holdings, Inc. (AFRM) is currently trading at $75.31, reflecting a robust profit margin of 45.29% and a P/E ratio of 13.62, which suggests the market is pricing in strong operational efficiency. The company’s most recent 10-Q filing on May 7, 2026, and upcoming 10-K for August 27, 2026, highlight ongoing risk factors that investors must monitor closely, particularly regarding potential uncertainties that could impact future cash flows. With a market cap exceeding $25 billion and no dividend yield, the stock remains a growth-oriented play within the credit services sector, appealing to investors focused on capital appreciation rather than income.

### SEC Filing Highlights
Affirm faces intensifying competition from large financial incumbents and merchants offering proprietary pay-over-time options, which may pressure market share and pricing power. The company’s reliance on a limited number of non-exclusive commercial partners for funding and origination creates significant concentration risk, as the loss of these relationships could materially adversely affect operations. Additionally, prolonged elevated interest rates and potential regulatory challenges to the bank-partner model pose ongoing threats to profitability and legal compliance. Investors should also note that quarterly results may fluctuate significantly due to the inherent volatility in growth rates and credit performance.

### Risk Factors

*   **Regulatory and Legal Exposure:** The company faces significant risks from evolving regulations, including potential challenges to its originating bank partner model, as well as exposure to litigation, fines, and reputational harm from compliance failures.
*   **Credit and Economic Sensitivity:** Financial performance is heavily dependent on consumer creditworthiness and loan performance; adverse economic conditions, rising interest rates, or ineffective collection efforts could lead to substantial financial losses and reduced confidence from funding sources.
*   **Competitive and Operational Dependencies:** Affirm operates in a highly competitive landscape with low barriers to entry, while relying on a limited number of key banking partners and commercial relationships that are non-exclusive and subject to termination or non-renewal.

## Audited (Exec Summary + Outlook)

### Executive Summary
Affirm Holdings, Inc. (AFRM) operates as a leading digital-first platform for buy-now-pay-later services, leveraging a robust 45.29% profit margin and a $25.4 billion market capitalization to maintain a strong position in the credit services sector. The stock is currently notable for its reasonable valuation, evidenced by a trailing P/E of 13.62, which reflects market confidence in its operational efficiency despite the absence of dividend income. The single most important near-term variable shaping the investment outcome is the company’s ability to navigate intensifying competition and regulatory scrutiny while maintaining its reliance on key banking partners.

### Outlook
The directional outlook for Affirm is cautiously constructive, supported by strong historical profitability and a valuation that appears reasonable relative to earnings power. However, this thesis is contingent on the company’s ability to defend its market share against entrenched financial incumbents and proprietary merchant financing options. Investors should closely monitor the stability of its non-exclusive banking partnerships and the evolving regulatory landscape surrounding its bank-partner model, as any disruption to these funding sources or compliance frameworks could significantly weaken the investment case. Conversely, sustained operational efficiency and successful navigation of credit cycles would reinforce the current positive sentiment.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "45.29% profit margin"
LABEL: SUPPORTED
REASON: The raw source data explicitly states `"profit_margin_pct": 45.29`, and the pre-written Financial Health section confirms "a profit margin of 45.29%."

---

CLAIM: "a $25.4 billion market capitalization"
LABEL: SUPPORTED
REASON: The raw source data states `"market_cap": 25411192832.0`; dividing by 1 billion gives ~$25.41 billion, which rounds to $25.4 billion as stated.

---

CLAIM: "a trailing P/E of 13.62"
LABEL: SUPPORTED
REASON: The raw source data states `"pe_ratio": 13.6184435`, which rounds to 13.62 as claimed; the pre-written Financial Health section also confirms "a trailing P/E ratio of 13.62."

---

**OUTLOOK**

The Outlook section contains no specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers. All statements are qualitative and directional in nature (e.g., "cautiously constructive," "reasonable relative to earnings power," "intensifying competition," "non-exclusive banking partnerships"). There are therefore no additional quantitative or forward-looking claims to audit in this section.

---

**SUMMARY TABLE**

| Claim | Label |
|---|---|
| 45.29% profit margin | SUPPORTED |
| $25.4 billion market capitalization | SUPPORTED |
| Trailing P/E of 13.62 | SUPPORTED |

All three quantitative claims in the audited sections are supported by the raw source data. The Outlook section is entirely qualitative and contains no auditable quantitative claims.
