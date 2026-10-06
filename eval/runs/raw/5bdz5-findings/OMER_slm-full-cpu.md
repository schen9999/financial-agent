# OMER — slm-full-cpu

## Metadata

ticker: OMER
arm: slm-full-cpu
judge_prompt_version: v2
context_sha256: e2ad83169865759155cba1799e4e98cf05fbc8b0d4316a9750b3cb3a1a4d18dd
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 744, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 205.962, "latency_s_total": 205.962, "parse_failure": 0, "prompt_tokens": 2632, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 395, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 161.313, "latency_s_total": 161.313, "parse_failure": 0, "prompt_tokens": 3034, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 171, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 49.181, "latency_s_total": 49.181, "parse_failure": 0, "prompt_tokens": 692, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 109, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 32.525, "latency_s_total": 32.525, "parse_failure": 0, "prompt_tokens": 686, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 203, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 54.065, "latency_s_total": 54.065, "parse_failure": 0, "prompt_tokens": 465, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 199, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 83.269, "latency_s_total": 83.269, "parse_failure": 0, "prompt_tokens": 822, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1022, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 169.527, "latency_s_total": 169.527, "parse_failure": 0, "prompt_tokens": 1738, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "OMER",
  "company_name": "Omeros Corporation",
  "current_price": 18.9,
  "currency": "USD",
  "market_cap": 1368139264.0,
  "pe_ratio": 15.491802,
  "forward_pe": 15.365853,
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
[]

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
*   **Outstanding Debt:** As of December 31, 2025, the company had $70.8 million in aggregate principal outstanding for its 2029 Notes and approximately $1.2 million in outstanding finance lease obligations. The $17.1 million in 5.25% convertible senior notes due in February 2026 had matured and been repaid in full by that date.
*   **Future Capital Needs:** The company expects to continue spending substantial amounts on clinical trials, manufacturing, commercializing YARTEMLEA, supporting sales and marketing, and servicing its convertible notes. It anticipates incurring additional losses until significant revenue is generated from YARTEMLEA or partnerships.

**Product Commercialization and Revenue Dependence**
*   **YARTEMLEA:** This is the company’s only commercialized product, approved by the FDA for commercial sale in the United States in December 2025. The company’s near-term commercial prospects and ability to achieve profitability are highly dependent on the commercial success of YARTEMLEA.
*   **Commercialization Risks:** There are numerous risks to successfully commercializing YARTEMLEA, including limited experience in marketing and distribution, reliance on a limited number of manufacturers and suppliers, and potential lack of acceptance by physicians, patients, and payers.
*   **Reimbursement Challenges:** Success depends heavily on obtaining adequate coverage and reimbursement from government and private payers. There is no assurance that reimbursement rates will cover costs or allow for profit, and payers are increasingly challenging prices and requiring discounts.

**Partnerships and Milestone Payments**
*   **Novo Nordisk Agreement:** The company has a transaction with Novo Nordisk involving zaltenibart. Future payments are contingent on the successful development, regulatory approval, and commercialization of zaltenibart, factors outside the company's control. If commercialization is unsuccessful or less than anticipated, the company may receive substantially less or no additional milestone and royalty payments.

**Risks Related to Liquidity and Operations**
*   **Capital Access:** The company may need to raise additional capital through debt, equity financings, or corporate partnering. There is no assurance that capital will be available on acceptable terms. Failure to raise capital could force the company to delay, scale back, or discontinue development programs.
*   **Indebtedness Risks:** Existing and future indebtedness could limit cash flow available for operations, restrict the ability to obtain additional financing, dilute existing stockholders (via conversion of notes), and place the company at a competitive disadvantage. Failure to comply with restrictive covenants or make scheduled payments could result in default, making all indebtedness immediately payable.
*   **Preclinical Programs:** The company may have insufficient funds to advance preclinical programs to a point where they can generate revenue through partnerships.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Dependence on YARTEMLEA:** The company’s ability to achieve profitability is highly dependent on the commercial success of YARTEMLEA, its only commercialized product. Failure to successfully commercialize this product could materially adversely affect the business, financial condition, and stock price.
*   **Commercialization Challenges:** There are risks associated with limited experience in marketing, selling, and distributing YARTEMLEA, reliance on a limited number of manufacturers and suppliers, and potential lack of acceptance by physicians, patients, and payers.
*   **Reimbursement and Pricing Risks:** Success depends heavily on obtaining adequate coverage and reimbursement from government and private payers. Risks include delays in reimbursement, limited coverage for approved uses, reimbursement rates that do not cover costs, and pressure from payers to provide discounts or challenge prices. Additionally, pricing may be adversely affected by government programs like the Inflation Reduction Act and foreign price controls.
*   **Dependence on Novo Nordisk for Zaltenibart:** The company’s ability to realize value from zaltenibart depends entirely on Novo Nordisk’s development, regulatory approval, and commercialization efforts. Novo Nordisk controls key decisions, and the company may receive little to no milestone or royalty payments if Novo Nordisk fails to advance or commercialize the product successfully.
*   **Operating Losses and Capital Needs:** The company has incurred cumulative operating losses since inception and expects to continue incurring losses until significant revenue is generated. There is a risk that the company may be unable to raise additional capital on acceptable terms when needed, which could force it to delay, scale back, or discontinue development or commercialization programs.
*   **Indebtedness:** The company has significant liabilities, including convertible senior notes and finance lease obligations, which could limit cash flow available for operations and expose the company to financial risks.

## Pre-written sections (judge input)

### Financial Health

Omeros Corporation (OMER) trades at $18.90 with a market capitalization of approximately $1.37 billion, reflecting a P/E ratio of 15.49. The company reported revenue of $38.42 million and a net income of $116.53 million, resulting in an exceptionally high profit margin of 324.88%. This disproportionate margin suggests significant non-operating income or accounting adjustments rather than core operational profitability from the reported revenue base. While the valuation metrics appear reasonable relative to peers, investors should scrutinize the sustainability of these earnings given the low revenue-to-income ratio. The stock remains well below its 52-week high of $21.24, indicating potential market skepticism regarding the durability of its current financial performance.

### Recent Developments

Omeros Corporation (OMER) has filed its Annual Report on Form 10-K for the fiscal year ended December 31, 2025, with the SEC on March 31, 2026. The filing highlights that the company's ability to achieve sustained profitability remains highly dependent on the commercial success of its products and pipeline programs. Investors should carefully review the detailed risk factors outlined in the report, as these uncertainties could materially impact the company's financial condition and operating results.

### SEC Filing Highlights
Omeros reported $171.8 million in cash and short-term investments as of December 31, 2025, following the full repayment of its $17.1 million convertible senior notes due in February 2026. The company’s near-term financial viability remains heavily dependent on the commercial success of YARTEMLEA, its only FDA-approved product, which launched in December 2025. Despite a net loss of $3.4 million for the year, Omeros continues to face substantial operating cash burn of $116.1 million while managing $70.8 million in outstanding 2029 Notes. Future liquidity and milestone payments from the Novo Nordisk partnership are contingent on the successful development and regulatory approval of zaltenibart, introducing significant execution risk. Management anticipates incurring additional losses until significant revenue is generated from YARTEMLEA sales or strategic partnerships.

### Risk Factors

*   **Product Concentration and Commercialization Risk:** Profitability is heavily dependent on the commercial success of YARTEMLEA, the company’s only commercialized product. Limited experience in marketing and distribution, coupled with potential lack of acceptance by physicians, patients, and payers, could materially adversely affect the business and stock price.
*   **Reimbursement and Pricing Pressures:** Revenue is contingent on obtaining adequate coverage and reimbursement from government and private payers. Risks include delays in reimbursement, limited coverage, unfavorable reimbursement rates, and adverse impacts from government programs like the Inflation Reduction Act and foreign price controls.
*   **Pipeline Dependency and Financial Sustainability:** The value of the zaltenibart pipeline depends entirely on Novo Nordisk’s development and commercialization efforts, with no guarantee of milestone or royalty payments. Additionally, the company has a history of cumulative operating losses, significant indebtedness, and faces risks related to its ability to raise necessary capital on acceptable terms.

## Audited (Exec Summary + Outlook)

### Executive Summary
Omeros Corporation is a biopharmaceutical company focused on inflammatory diseases, currently trading with a market capitalization of approximately $1.37 billion and reporting a net income of $116.53 million against revenue of $38.42 million. The stock is notable for its significant cash position of $171.8 million and the recent launch of its sole commercial product, YARTEMLEA, which serves as the primary catalyst for future growth. The single most important near-term variable shaping the investment outcome is the commercial execution and payer acceptance of YARTEMLEA, as the company’s financial viability remains heavily dependent on generating sufficient revenue to offset its substantial operating cash burn.

### Outlook
The directional outlook for Omeros is cautiously constructive but heavily contingent on binary execution risks. The primary tailwind is the successful commercial ramp-up of YARTEMLEA, which must demonstrate robust payer acceptance and physician adoption to offset the company’s substantial operating cash burn and fund ongoing operations. Conversely, headwinds include the inherent uncertainty of the Novo Nordisk partnership for zaltenibart, where milestone payments are not guaranteed, and the broader macroeconomic pressures on healthcare reimbursement. Investors should closely monitor early sales data for YARTEMLEA and any updates regarding payer coverage decisions; a sustained acceleration in commercial revenue would strengthen the thesis by improving liquidity and reducing reliance on external financing, whereas slower-than-expected uptake or unfavorable reimbursement terms would weaken the view by exacerbating cash burn concerns.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of approximately $1.37 billion"
LABEL: SUPPORTED
REASON: Source data shows market_cap = $1,368,139,264, which rounds to approximately $1.37 billion; the pre-written Financial Health section also states "approximately $1.37 billion."

---

CLAIM: "net income of $116.53 million"
LABEL: SUPPORTED
REASON: Source data shows net_income = $116,533,000 = $116.53 million, confirmed in the Financial Health pre-written section.

---

CLAIM: "revenue of $38.42 million"
LABEL: SUPPORTED
REASON: Source data shows revenue = $38,422,000 = $38.42 million, confirmed in the Financial Health pre-written section.

---

CLAIM: "significant cash position of $171.8 million"
LABEL: SUPPORTED
REASON: RAG — SEC Highlights explicitly states "As of December 31, 2025, the company held $171.8 million in cash, cash equivalents, and short-term investments," confirmed in the SEC Filing Highlights pre-written section.

---

CLAIM: "recent launch of its sole commercial product, YARTEMLEA"
LABEL: SUPPORTED
REASON: RAG — SEC Highlights states YARTEMLEA was "approved by the FDA for commercial sale in the United States in December 2025" and is described as "its only commercialized product."

---

CLAIM: "the company's financial viability remains heavily dependent on generating sufficient revenue to offset its substantial operating cash burn"
LABEL: SUPPORTED
REASON: The SEC Filing Highlights pre-written section states "Omeros continues to face substantial operating cash burn of $116.1 million" and that "near-term financial viability remains heavily dependent on the commercial success of YARTEMLEA"; this is a direct restatement of sourced content.

---

**OUTLOOK**

---

CLAIM: "milestone payments are not guaranteed" (re: Novo Nordisk / zaltenibart)
LABEL: SUPPORTED
REASON: RAG — SEC Highlights states "Future payments are contingent on the successful development, regulatory approval, and commercialization of zaltenibart…the company may receive substantially less or no additional milestone and royalty payments," directly supporting this characterization.

---

CLAIM: "the company's substantial operating cash burn" (referenced as a figure to offset)
LABEL: SUPPORTED
REASON: The SEC Filing Highlights pre-written section explicitly quantifies operating cash burn at $116.1 million, and the Outlook's qualitative reference to "substantial operating cash burn" is grounded in that figure.

---

**ADDITIONAL CHECK — figures present in source but NOT misrepresented in the audited sections:**

The Outlook section contains no additional standalone quantitative figures (no specific dollar amounts, percentages, ratios, price targets, or period-specific numbers beyond those already audited above). All forward-looking statements are qualitative or directional and are grounded in sourced risk disclosures.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | Market cap ~$1.37 billion | SUPPORTED |
| 2 | Net income $116.53 million | SUPPORTED |
| 3 | Revenue $38.42 million | SUPPORTED |
| 4 | Cash position $171.8 million | SUPPORTED |
| 5 | YARTEMLEA as sole commercial product, recently launched | SUPPORTED |
| 6 | Financial viability dependent on offsetting substantial operating cash burn | SUPPORTED |
| 7 | Novo Nordisk milestone payments not guaranteed | SUPPORTED |
| 8 | Substantial operating cash burn (qualitative reference) | SUPPORTED |

All auditable claims in the Executive Summary and Outlook sections are **SUPPORTED** by the source data or pre-written sections. No unsupported or inference-only claims were identified.
