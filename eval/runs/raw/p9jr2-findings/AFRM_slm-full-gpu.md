# AFRM — slm-full-gpu

## Metadata

ticker: AFRM
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 3b6acfcb3bfec597350b2fad08ee87a5a03491067afcf4de437da02b6ccc65b1
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 590, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.657, "latency_s_total": 17.657, "parse_failure": 0, "prompt_tokens": 2358, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 596, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.807, "latency_s_total": 17.807, "parse_failure": 0, "prompt_tokens": 3026, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 180, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 6.227, "latency_s_total": 6.227, "parse_failure": 0, "prompt_tokens": 704, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 168, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 6.018, "latency_s_total": 6.018, "parse_failure": 0, "prompt_tokens": 698, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 171, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 9.911, "latency_s_total": 9.911, "parse_failure": 0, "prompt_tokens": 669, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 126, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.616, "latency_s_total": 4.616, "parse_failure": 0, "prompt_tokens": 671, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 929, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 18.399, "latency_s_total": 18.399, "parse_failure": 0, "prompt_tokens": 1670, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
*   The pay-over-time industry has low barriers to entry, leading to intensifying competition.
*   Competitors include merchants offering proprietary pay-over-time options, emerging technologies, and large financial incumbents (such as credit card issuing banks).
*   Larger competitors possess significant advantages, including diversified products, broader consumer and merchant bases, greater brand recognition, operational efficiencies, and the ability to cross-subsidize offerings.

**Commercial Partnerships**
*   The company relies heavily on a small number of commercial partners, including originating banks (Celtic Bank and Lead Bank) and card-issuing bank partners.
*   Loss of these significant relationships, or the inability to replace them, could materially adversely affect the business.
*   Many agreements with commercial partners are non-exclusive and lack transaction volume commitments, meaning partners may engage with competitors.
*   Success depends on retaining partners and demonstrating value propositions such as higher checkout conversion rates and increased average order value.

**Financial and Operational Risks**
*   **Loan Performance:** Financial losses may occur if loans facilitated through the platform do not perform or underperform, potentially leading to a loss of confidence among funding sources.
*   **Funding:** The business relies on various funding sources; if these are not renewed or replaced on acceptable terms, it could have a material adverse effect.
*   **Profitability and Growth:** There is no guarantee that the company can sustain revenue, Gross Merchandise Volume (GMV), or profitability growth rates. Quarterly results may fluctuate significantly.
*   **Interest Rates:** Further increases or prolonged periods of elevated market interest rates could adversely affect the business.

**Regulatory and Legal Risks**
*   The business is subject to extensive and changing federal, state, and local regulations.
*   If the originating bank partner model is deemed impermissible, the company could face violations of licensing, interest rate limit, lending, or brokering laws, resulting in penalties, fines, or litigation.
*   Litigation, regulatory actions, and compliance issues could lead to increased expenses and reputational harm.

**Other Key Risks**
*   **Cybersecurity:** The company faces risks related to cyber-attacks, internal misconduct, and data breaches involving confidential consumer information.
*   **Leadership and Talent:** The loss of the Founder and CEO, or the inability to attract and retain highly skilled employees, could materially affect the business.
*   **International Expansion:** Expanding into new international geographies presents various challenges and risks.
*   **Stock Structure:** The dual-class structure of common stock concentrates voting control with Class B shareholders, which may depress the trading price of Class A common stock.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Commercial Partner Relationships:** The inability to attract, retain, or grow relationships with commercial partners, including the loss of significant relationships and the non-exclusive nature of many agreements which may allow partners to work with competitors.
*   **Consumer Base:** The inability to attract new consumers or retain and grow relationships with existing consumers, which impacts revenue derived from consumer transaction volume.
*   **Competition:** Operating in a highly competitive industry with low barriers to entry, facing competition from legacy payment methods, mobile wallets, other pay-over-time solutions, and merchants offering proprietary options.
*   **Banking Partners:** Reliance on a small number of originating bank partners (specifically Celtic Bank and Lead Bank) and card issuing bank partners. Termination of these agreements without replacement could adversely affect the business.
*   **Growth and Metrics:** The potential inability to sustain revenue, Gross Merchandise Volume (GMV), and key operating metric growth rates.
*   **Funding:** Reliance on various funding sources; if these are not renewed, replaced, or provided on acceptable terms, it could materially adversely affect the business.
*   **Loan Performance:** Financial losses from loans that do not perform or underperform, which could also lead to a loss of confidence among funding sources.
*   **Strategic Transactions:** The risk that acquisitions, investments, alliances, or divestitures may fail to achieve strategic objectives or disrupt ongoing operations.
*   **International Expansion:** Challenges and risks associated with expanding into new international geographies.
*   **Key Personnel:** The loss of the Founder and Chief Executive Officer, or the inability to attract and retain highly skilled employees.
*   **Profitability and Results:** The potential inability to sustain profitability and significant fluctuations in quarterly results that may not reflect underlying performance.
*   **Legal and Regulatory Issues:** Exposure to litigation, regulatory actions, compliance issues, fines, penalties, and reputational harm. This includes extensive regulation subject to change and the risk that the originating bank partner model could be deemed impermissible.
*   **Interest Rates:** Adverse effects from further increases in market interest rates or prolonged periods of elevated interest rates.
*   **Economic Factors:** Revenue impact from the general economy, U.S. consumer creditworthiness, and the financial performance of commercial partners.
*   **Collection Efforts:** Ineffective or unsuccessful collection efforts on delinquent loans.
*   **Platform Disruptions:** Service disruptions or errors on the platform or related to vendors that prevent transaction processing or payment posting.
*   **Cybersecurity:** Risks to confidential, proprietary, or sensitive information from cyber-attacks, internal misconduct, viruses, or break-ins.
*   **Stock Structure:** The dual class structure of common stock concentrates voting control with Class B shareholders, which may depress the trading price of Class A common stock.

## Pre-written sections (judge input)

### Financial Health

Affirm Holdings, Inc. (AFRM) currently trades at $70.77 with a market capitalization of approximately $23.88 billion. The company demonstrates strong profitability, reporting a net income of $1.93 billion against revenues of $4.26 billion, resulting in an impressive profit margin of 45.29%. This robust earnings performance is reflected in a trailing P/E ratio of 12.80, suggesting the stock may be reasonably valued relative to its current earnings power. While the forward P/E of 14.66 indicates modest expected growth, the absence of a dividend yield highlights the company's focus on reinvesting capital for expansion. Overall, the financial profile is characterized by high margins and solid earnings, though investors should monitor the sustainability of these margins within the competitive credit services sector.

### Recent Developments

Affirm Holdings reported a robust profit margin of 45.3% and a net income of approximately $1.93 billion, underscoring strong operational efficiency despite the absence of dividend payouts. The company’s valuation metrics, including a P/E ratio of 12.8 and a forward P/E of 14.7, suggest the market is pricing in steady growth relative to its $23.9 billion market capitalization. While recent SEC filings highlight standard risk disclosures regarding market uncertainties, the stock’s current price of $70.77 reflects a significant recovery from its 52-week low of $42.10. Investors should monitor the company’s ability to sustain these high margins amidst potential macroeconomic headwinds and competitive pressures in the credit services sector.

### SEC Filing Highlights
Affirm faces intensifying competition from merchants and large financial incumbents, while relying heavily on a limited number of non-exclusive commercial partners for funding and origination. The company’s profitability and growth trajectory remain subject to significant volatility, influenced by loan performance, fluctuating interest rates, and the ability to sustain revenue expansion. Regulatory scrutiny poses a critical risk, particularly regarding the permissibility of the originating bank partner model, which could result in substantial penalties or operational restrictions. Additionally, the business must navigate cybersecurity threats, talent retention challenges, and the concentrated voting control inherent in its dual-class stock structure.

### Risk Factors

*   **Regulatory and Legal Exposure:** The company faces significant risks from evolving consumer lending regulations, potential litigation, and the specific risk that its originating bank partner model could be deemed impermissible, leading to fines, penalties, or operational disruptions.
*   **Credit and Funding Dependency:** Affirm is highly dependent on a small number of banking partners for capital origination and relies on external funding sources; adverse changes in interest rates, economic conditions, or the termination of these agreements could materially impair its ability to lend and sustain growth.
*   **Intense Competition and Partner Retention:** Operating in a low-barrier-to-entry market, the company risks losing market share to legacy payment methods, proprietary merchant options, and competitors, while also facing the challenge of retaining non-exclusive commercial partners who may choose to work with rivals.

## Audited (Exec Summary + Outlook)

### Executive Summary
Affirm Holdings operates as a key player in the credit services sector, leveraging a $23.88 billion market capitalization and a robust 45.29% profit margin to maintain its competitive position. The stock is notable for its significant recovery from a 52-week low of $42.10 to $70.77, reflecting strong operational efficiency and a trailing P/E ratio of 12.80 that suggests reasonable valuation relative to current earnings. The single most important near-term variable shaping the investment outcome is the regulatory scrutiny surrounding the permissibility of its originating bank partner model, which could materially impact operational continuity and profitability.

### Outlook
The directional outlook for Affirm is cautiously constructive, supported by strong current profitability and a valuation that appears reasonable relative to earnings power. However, this positive stance is tempered by significant headwinds, including intense competition, reliance on a limited set of funding partners, and the critical regulatory risk regarding the bank partner model. Investors should closely monitor the trajectory of services margins and the regulatory environment surrounding lending practices, as favorable clarity on the partner model would strengthen the thesis, whereas adverse regulatory rulings or a deterioration in loan performance would weaken it.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "a $23.88 billion market capitalization"
LABEL: SUPPORTED
REASON: The source data lists market_cap = 23,879,301,120.0, which rounds to $23.88 billion, and the pre-written Financial Health section states "approximately $23.88 billion."

---

CLAIM: "a robust 45.29% profit margin"
LABEL: SUPPORTED
REASON: The source data lists profit_margin = 0.45289, which equals 45.289%, rounding to 45.29%; this figure also appears explicitly in the Financial Health pre-written section.

---

CLAIM: "a 52-week low of $42.10"
LABEL: SUPPORTED
REASON: The source data lists week_52_low = 42.095, which rounds to $42.10, consistent with the Recent Developments pre-written section.

---

CLAIM: "to $70.77"
LABEL: SUPPORTED
REASON: The source data lists current_price = 70.77, explicitly matching the claim.

---

CLAIM: "a trailing P/E ratio of 12.80"
LABEL: SUPPORTED
REASON: The source data lists pe_ratio = 12.797467, which rounds to 12.80, and the Financial Health section states "trailing P/E ratio of 12.80."

---

**OUTLOOK**

---

CLAIM: "strong current profitability"
LABEL: SUPPORTED
REASON: This is a directional restatement of the 45.29% profit margin and $1.93 billion net income present in the source data and pre-written sections.

---

CLAIM: "a valuation that appears reasonable relative to earnings power"
LABEL: SUPPORTED
REASON: This is a direct restatement of the pre-written Financial Health section's characterization of the trailing P/E of 12.80 as suggesting the stock "may be reasonably valued relative to its current earnings power."

---

CLAIM: "intense competition"
LABEL: SUPPORTED
REASON: Explicitly supported by the SEC Filing Highlights and Risk Factors pre-written sections, as well as the RAG data describing "intensifying competition" and a "highly competitive industry with low barriers to entry."

---

CLAIM: "reliance on a limited set of funding partners"
LABEL: SUPPORTED
REASON: Explicitly supported by the pre-written Risk Factors section ("highly dependent on a small number of banking partners") and RAG data naming Celtic Bank and Lead Bank.

---

CLAIM: "the critical regulatory risk regarding the bank partner model"
LABEL: SUPPORTED
REASON: Explicitly present in the pre-written SEC Filing Highlights and Risk Factors sections, and in the RAG risk factor data regarding the originating bank partner model potentially being deemed impermissible.

---

CLAIM: "Investors should closely monitor the trajectory of services margins"
LABEL: UNSUPPORTED
REASON: The term "services margins" does not appear anywhere in the source data, pre-written sections, or RAG content; the source discusses profit margins generally, not a specifically defined "services margins" metric.

---

CLAIM: "favorable clarity on the partner model would strengthen the thesis"
LABEL: INFERENCE
REASON: This is a logical forward-looking inference directly derivable from the pre-written Risk Factors section's identification of the bank partner model regulatory risk as a key threat to operations and profitability.

---

CLAIM: "adverse regulatory rulings or a deterioration in loan performance would weaken it"
LABEL: INFERENCE
REASON: Both "adverse regulatory rulings" and "loan performance deterioration" are explicitly identified as risk factors in the source data and pre-written sections; the directional conclusion that they would weaken the investment thesis is a straightforward logical derivation from those stated risks.
