# OMER — slm-full-cpu

## Metadata

ticker: OMER
arm: slm-full-cpu
judge_prompt_version: v2
context_sha256: 0ba79b7470f91e3942541d2b044a5be77034b38da7d62757b81f0267e8f12bc7
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 737, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 207.74, "latency_s_total": 207.74, "parse_failure": 0, "prompt_tokens": 2632, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 434, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 168.12, "latency_s_total": 168.12, "parse_failure": 0, "prompt_tokens": 3034, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 145, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 46.685, "latency_s_total": 46.685, "parse_failure": 0, "prompt_tokens": 712, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 127, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 36.482, "latency_s_total": 36.482, "parse_failure": 0, "prompt_tokens": 706, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 156, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 54.41, "latency_s_total": 54.41, "parse_failure": 0, "prompt_tokens": 504, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 197, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 87.235, "latency_s_total": 87.235, "parse_failure": 0, "prompt_tokens": 815, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 925, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 150.971, "latency_s_total": 150.971, "parse_failure": 0, "prompt_tokens": 1624, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "OMER",
  "company_name": "Omeros Corporation",
  "current_price": 18.51,
  "currency": "USD",
  "market_cap": 1339907840.0,
  "pe_ratio": 15.172131,
  "forward_pe": 15.04878,
  "week_52_high": 21.24,
  "week_52_low": 4.06,
  "financial_currency": "USD",
  "revenue": 38422000.0,
  "net_income": 116533000.0,
  "profit_margin_pct": 324.88,
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
    "filing_date": "2026-03-31",
    "summary": "ITEM 1A. RISK FACTORS The risks and uncertainties described below may have a material adverse effect on our business, prospects, financial condition or operating results. In addition, we may be adversely affected by risks that we currently deem immaterial or by other risks that are not currently known to us. You should carefully consider these risks before making an investment decision. The trading price of our common stock could decline due to any of these risks and you may lose all or part of your investment. In assessing the risks described below, you should also refer to the other information contained in this Annual Report on Form 10-K. Risks Related to Our Products, Product Candidates, Programs and Operations Our ability to achieve profitability is highly dependent on the commercial "
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-12",
    "summary": "ITEM 1A. RISK FACTORS We operate in an environment that involves a number of risks and uncertainties. Before making an investment decision you should carefully consider the risks described in Part I, Item 1A, \u201cRisk Factors\u201d of our Annual Report on Form 10-K for the year ended December 31, 2025, as filed with the SEC on March 31, 2026. In assessing the risk factors set forth in our Annual Report on Form 10-K for the year ended December 31, 2025, you should also refer to the other information included therein and in this Quarterly Report on Form 10-Q, including the supplemental risk factor below. In addition, we may be adversely affected by risks that we currently deem to be immaterial or by other risks that are not currently known to us. Due to these risks and uncertainties, known and unkno"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] Based on the provided text from the SEC EDGAR filings for ticker OMER, here are the key takeaways regarding the company's financial condition, risks, and operational outlook:

**Financial Position and Indebtedness**
*   **Cash Reserves:** As of December 31, 2025, the company held $171.8 million in cash, cash equivalents, and short-term investments.
*   **Operating Losses:** The company has incurred cumulative operating losses since inception. For the year ended December 31, 2025, cash used in operations was $116.1 million, and the net loss was $3.4 million.
*   **Debt Structure:** The company had $70.8 million in outstanding aggregate principal amount of its 2029 Notes and approximately $1.2 million in outstanding finance lease obligations. The $17.1 million in 5.25% convertible senior notes due in February 2026 (the "2026 Notes") had matured and been repaid in full as of the reporting date.
*   **Future Capital Needs:** The company expects to continue spending substantial amounts on clinical trials, manufacturing, commercializing YARTEMLEA, supporting sales and marketing, and servicing its convertible senior notes. There is no assurance that sufficient revenue will be generated to fund operations, potentially requiring additional capital raises through debt, equity, or partnerships.

**Product Commercialization and Revenue Dependence**
*   **Reliance on YARTEMLEA:** The company’s ability to achieve profitability is highly dependent on the commercial success of YARTEMLEA, its only commercialized product approved by the FDA in the United States in December 2025.
*   **Commercialization Risks:** Success depends on overcoming several hurdles, including physician and patient acceptance, limited experience in marketing and third-party manufacturing, reliance on limited suppliers, and reimbursement policies from government and private payers.
*   **Reimbursement Challenges:** Revenue prospects are heavily influenced by the pricing, availability, and duration of coverage from third-party payers. Increasing demands for discounts and challenges to pricing by payers could adversely impact profitability.

**Partnerships and Milestone Payments**
*   **Novo Nordisk Agreement:** Future value realization is contingent on the successful development, regulatory approval, and commercialization of zaltenibart. If Novo Nordisk fails to successfully develop or commercialize this product, the company may receive substantially less in milestone and royalty payments than expected, or none at all.
*   **Revenue Variability:** Even if commercialized, royalty revenue from zaltenibart may vary significantly due to pricing, reimbursement, sales volumes, and competition.

**General Risk Factors**
*   **Indebtedness Risks:** Existing and future indebtedness could limit cash flow available for operations, restrict the ability to obtain additional financing, dilute existing stockholders (via conversion of notes), and place the company at a competitive disadvantage against less leveraged competitors.
*   **Covenant Compliance:** Failure to comply with financial covenants or make scheduled payments could result in default, making all indebtedness immediately payable.
*   **Preclinical Programs:** The company may lack sufficient funds to advance preclinical programs to a point where they can generate revenue through partnerships, which could harm business prospects.
*   **Stock Price Volatility:** The trading price of common stock could decline due to these risks, and investors may lose all or part of their investment.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Dependence on YARTEMLEA:** The company’s ability to achieve profitability is highly dependent on the commercial success of YARTEMLEA, its only commercialized product. Failure to successfully commercialize this product could materially adversely affect the business, financial condition, and stock price.
*   **Commercialization Challenges:** There are risks associated with limited experience in marketing, selling, and distributing YARTEMLEA, reliance on a limited number of manufacturers and suppliers, and potential lack of acceptance by physicians, patients, and payers.
*   **Reimbursement and Pricing Risks:** Success depends heavily on obtaining adequate coverage and reimbursement from government and private payers. Risks include delays in reimbursement, limited coverage for approved uses, reimbursement rates that do not cover costs, and pressure from payers to provide discounts or challenge prices. Additionally, changes in government programs like the Inflation Reduction Act may reduce payments.
*   **Regulatory and International Risks:** There is a risk of failing to obtain regulatory approval in the EU or other foreign territories, as well as challenges in complying with post-approval regulatory requirements. In non-U.S. jurisdictions, products may be subject to government price controls and separate reimbursement approvals.
*   **Dependence on Novo Nordisk:** The value realized from zaltenibart depends on Novo Nordisk’s development, regulatory approval, and commercialization efforts. Novo Nordisk controls key decisions, and the company may receive little or no additional payments if Novo Nordisk fails to advance or commercialize the product successfully.
*   **Financial Losses and Capital Needs:** The company has incurred cumulative operating losses since inception and expects to continue incurring losses until significant revenue is generated. There is a risk that the company may be unable to raise additional capital when needed, which could force it to delay, scale back, or discontinue development or commercialization programs.
*   **Indebtedness:** The company has outstanding convertible senior notes and finance lease obligations, which could limit cash flow available for operations and expose the company to financial risks.

## Pre-written sections (judge input)

### Financial Health

Omeros Corporation (OMER) trades at $18.51 with a market capitalization of approximately $1.34 billion, reflecting a P/E ratio of 15.17. The company reports revenue of $38.42 million and a net income of $116.53 million, resulting in an exceptionally high profit margin of 324.88%. This disproportionate margin suggests significant non-operating income or accounting adjustments rather than core operational profitability from its biotechnology products. While the forward P/E remains stable at 15.05, investors should scrutinize the sustainability of these earnings given the company's early-stage commercial status.

### Recent Developments

Omeros Corporation (OMER) has filed its Annual Report on Form 10-K for the year ended December 31, 2025, with the SEC on March 31, 2026, alongside a subsequent Quarterly Report on Form 10-Q filed on August 12, 2026. These filings highlight ongoing risk factors related to the company's ability to achieve profitability and the commercial success of its product candidates. Investors should carefully review these documents to assess the material uncertainties and potential adverse effects on the company's financial condition and operating results.

### SEC Filing Highlights
As of December 31, 2025, Omeros Corporation held $171.8 million in cash and short-term investments, though it reported a net loss of $3.4 million and $116.1 million in operating cash usage for the year. The company’s financial outlook is heavily dependent on the commercial success of YARTEMLEA, its sole FDA-approved product, as it faces significant hurdles regarding physician acceptance, reimbursement policies, and manufacturing scalability. While the 2026 convertible notes were repaid in full, the firm retains $70.8 million in 2029 Notes and anticipates substantial future spending on clinical trials and commercialization efforts. Consequently, Omeros may need to raise additional capital through debt, equity, or partnerships to sustain operations, with future value also contingent on the development and commercialization of zaltenibart under its agreement with Novo Nordisk.

### Risk Factors

*   **Product and Commercialization Concentration:** Profitability is heavily dependent on the commercial success of YARTEMLEA, the company’s only commercialized product, with significant risks related to limited marketing experience, supply chain reliance, and potential lack of market acceptance.
*   **Reimbursement and Regulatory Uncertainty:** Success hinges on obtaining adequate payer coverage and navigating complex regulatory landscapes, including risks of delayed reimbursements, price pressures, and potential failures in securing approvals for international expansion.
*   **Strategic and Financial Dependencies:** The company faces substantial risks tied to its partnership with Novo Nordisk for zaltenibart, where value realization is contingent on their development efforts, alongside ongoing financial losses and potential liquidity constraints due to indebtedness.

## Audited (Exec Summary + Outlook)

### Executive Summary
Omeros Corporation is a biotechnology firm focused on developing therapies for inflammatory and immune-mediated diseases, currently trading with a market capitalization of approximately $1.34 billion and reporting a net income of $116.53 million against $38.42 million in revenue. The stock is notable for its complex financial profile, where reported profitability masks significant operating cash burn and reliance on non-operating income, creating a divergence between accounting metrics and operational reality. The single most important near-term variable shaping the investment outcome is the commercial traction and physician adoption of YARTEMLEA, which remains the sole driver of near-term revenue and cash flow sustainability.

### Outlook
The directional outlook for Omeros is cautiously constructive but heavily weighted toward execution risk, as the company stands at a critical juncture where reported accounting profits mask underlying operational cash consumption. Key variables to monitor include the rate of physician adoption for YARTEMLEA, the stability of reimbursement policies, and the progress of the zaltenibart partnership with Novo Nordisk, which serves as a potential long-term value driver. The thesis would be strengthened by evidence of scalable commercial operations and improved operating cash flow efficiency, while it would be weakened by persistent reliance on external capital raises or slower-than-expected market penetration of its sole commercial product.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of approximately $1.34 billion"
LABEL: SUPPORTED
REASON: Source data lists market_cap = 1,339,907,840.0 USD, which rounds to approximately $1.34 billion; the Pre-written Financial Health section also states "approximately $1.34 billion."

---

CLAIM: "net income of $116.53 million"
LABEL: SUPPORTED
REASON: Source data lists net_income = 116,533,000.0 USD = $116.533 million, which matches $116.53 million when rounded to two decimal places.

---

CLAIM: "$38.42 million in revenue"
LABEL: SUPPORTED
REASON: Source data lists revenue = 38,422,000.0 USD = $38.422 million, which rounds to $38.42 million; confirmed in the Pre-written Financial Health section.

---

CLAIM: "sole driver of near-term revenue and cash flow sustainability" (referring to YARTEMLEA as the sole commercial product)
LABEL: SUPPORTED
REASON: The SEC Filing Highlights and Risk Factors sections explicitly state YARTEMLEA is the company's "sole FDA-approved product" and "only commercialized product," making this a direct restatement of source content.

---

**OUTLOOK**

---

No additional quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section beyond qualitative directional statements and the named entities (YARTEMLEA, zaltenibart, Novo Nordisk) already confirmed as present in the source data. The Outlook contains no new numerical claims requiring arithmetic verification.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | Market cap ~$1.34 billion | SUPPORTED |
| 2 | Net income $116.53 million | SUPPORTED |
| 3 | Revenue $38.42 million | SUPPORTED |
| 4 | YARTEMLEA as sole commercial product / revenue driver | SUPPORTED |

All four verifiable quantitative or factual claims in the Executive Summary and Outlook are **SUPPORTED** by the source data. The Outlook section is otherwise composed entirely of qualitative directional language with no additional quantitative claims requiring verification.
