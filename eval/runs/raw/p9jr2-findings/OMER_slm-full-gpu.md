# OMER — slm-full-gpu

## Metadata

ticker: OMER
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 4a45e835fe88bac0bc5403d061c44cac2d78675b8ccf2e53fe49f29aa62cb8bc
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 778, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 16.336, "latency_s_total": 16.336, "parse_failure": 0, "prompt_tokens": 2632, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 378, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 8.244, "latency_s_total": 8.244, "parse_failure": 0, "prompt_tokens": 3034, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 155, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.633, "latency_s_total": 4.633, "parse_failure": 0, "prompt_tokens": 708, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 132, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.776, "latency_s_total": 3.776, "parse_failure": 0, "prompt_tokens": 702, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 139, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 7.584, "latency_s_total": 7.584, "parse_failure": 0, "prompt_tokens": 448, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 155, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 8.239, "latency_s_total": 8.239, "parse_failure": 0, "prompt_tokens": 856, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 914, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.502, "latency_s_total": 19.502, "parse_failure": 0, "prompt_tokens": 1536, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "OMER",
  "company_name": "Omeros Corporation",
  "current_price": 18.61,
  "currency": "USD",
  "market_cap": 1347146624.0,
  "pe_ratio": 15.254099,
  "forward_pe": 15.130081,
  "week_52_high": 21.24,
  "week_52_low": 4.06,
  "revenue": 38422000.0,
  "net_income": 116533000.0,
  "profit_margin": 3.2488198,
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

**Financial Position and Liquidity**
*   **Cash Reserves:** As of December 31, 2025, the company held $171.8 million in cash, cash equivalents, and short-term investments.
*   **Operating Losses:** The company has incurred cumulative operating losses since inception. For the year ended December 31, 2025, cash used in operations was $116.1 million, and the net loss was $3.4 million.
*   **Indebtedness:** The company had $70.8 million in outstanding principal on its 2029 Notes and approximately $1.2 million in finance lease obligations. The $17.1 million in 2026 Notes had matured and been repaid in full.
*   **Future Funding Needs:** The company expects to continue spending substantial amounts on clinical trials, manufacturing, commercializing YARTEMLEA, R&D, and debt service. It cannot guarantee sufficient revenue to fund operations and may need to raise additional capital through debt, equity, or partnerships. Failure to secure capital could force delays, scaling back, or discontinuation of development programs.

**Product Commercialization and Revenue Dependence**
*   **YARTEMLEA:** This is the company’s only commercialized product, approved by the FDA in December 2025. The company’s near-term commercial prospects and ability to achieve profitability are highly dependent on the success of YARTEMLEA.
*   **Commercialization Risks:** Success depends on physician and patient acceptance, reimbursement policies, and competition. Risks include limited experience in marketing and distribution, reliance on third-party manufacturers and suppliers, and potential regulatory hurdles in the EU or other territories.
*   **Reimbursement Challenges:** Revenue is heavily tied to coverage and reimbursement from government and private payers. Payers may challenge prices, require discounts, or limit coverage, which could adversely impact profitability.

**Partnerships and Milestone Payments**
*   **Novo Nordisk Collaboration:** The company has a partnership with Novo Nordisk regarding zaltenibart. Future payments are contingent on the successful development, regulatory approval, and commercialization of zaltenibart.
*   **Uncertainty of Payments:** If Novo Nordisk fails to successfully develop or commercialize zaltenibart, or if commercialization is less successful than anticipated, the company may receive substantially less in milestone and royalty payments than expected, or none at all. Royalty revenue may also vary significantly due to pricing, competition, and market conditions.

**Risks Related to Indebtedness**
*   **Cash Flow Constraints:** Indebtedness limits cash flow available for operations and requires a substantial portion of cash flow to service debt.
*   **Restrictive Covenants:** Future or existing debt may contain covenants that limit the company’s ability to operate, raise capital, or make other payments.
*   **Default Risks:** Failure to comply with covenants or make payments could result in default, making all indebtedness immediately payable.
*   **Competitive Disadvantage:** High leverage may place the company at a disadvantage compared to less leveraged competitors and increase vulnerability to adverse economic conditions. Additionally, converting notes could dilute existing stockholders.

**General Risk Factors**
*   The trading price of common stock could decline due to these risks. The company faces uncertainties related to product development, regulatory approvals, and market conditions that could materially adversely affect business, financial condition, and operating results.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Dependence on YARTEMLEA:** The company’s ability to achieve profitability is highly dependent on the commercial success of YARTEMLEA, its only commercialized product. Failure to successfully commercialize this product could materially adversely affect the business, financial condition, and stock price.
*   **Commercialization Challenges:** There are risks related to a lack of acceptance by the medical community, limited experience in marketing and distribution, reliance on limited manufacturers and suppliers, and insufficient resources.
*   **Reimbursement and Pricing Risks:** Success depends heavily on obtaining adequate coverage and reimbursement from government and private payers. Risks include delays in reimbursement, limited coverage for approved uses, reimbursement rates that do not cover costs, and pressure from payers to provide discounts or challenge prices. Additionally, pricing may be affected by government programs like the Inflation Reduction Act and foreign price controls.
*   **Dependence on Novo Nordisk for Zaltenibart:** The company’s ability to realize value from zaltenibart depends on Novo Nordisk’s development, regulatory approval, and commercialization efforts. Novo Nordisk controls key decisions, and the company may receive little or no milestone or royalty payments if Novo Nordisk fails to advance or commercialize the product successfully.
*   **Operating Losses and Capital Needs:** The company has incurred cumulative operating losses since inception and expects to continue incurring losses until significant revenue is generated. There is a risk that the company may be unable to raise additional capital when needed, which could force it to delay, scale back, or discontinue development or commercialization programs.
*   **Indebtedness:** The company has significant indebtedness, including convertible senior notes and finance lease obligations, which limits cash flow available for operations and exposes the company to financial risks.

## Pre-written sections (judge input)

### Financial Health

Omeros Corporation (OMER) trades at $18.61 with a market capitalization of approximately $1.35 billion, reflecting a P/E ratio of 15.25. The company reported revenue of $38.42 million and a net income of $116.53 million, resulting in a healthy profit margin of 3.25%. This positive net income suggests a strong recent financial performance relative to its top-line revenue. However, investors should note the absence of dividend yields, indicating a focus on growth or reinvestment rather than shareholder returns. The valuation appears reasonable given the forward P/E of 15.13, though the biotech sector inherently carries significant operational risks.

### Recent Developments

Omeros Corporation (OMER) recently filed its Annual Report on Form 10-K on March 31, 2026, and its Quarterly Report on Form 10-Q on August 12, 2026, both of which highlight significant risk factors related to the company's path to profitability and commercial execution. The filings emphasize that the trading price of the common stock could decline materially due to uncertainties inherent in its product candidates and operational challenges. Investors should carefully review these disclosed risks, as they underscore the potential volatility and the critical nature of achieving sustainable commercial success for the biotechnology firm.

### SEC Filing Highlights
Omeros reported $171.8 million in cash and short-term investments as of December 31, 2025, while incurring a net loss of $3.4 million and using $116.1 million in operating cash. The company’s near-term viability is heavily dependent on the commercial success of its sole approved product, YARTEMLEA, amid ongoing clinical trials and debt service obligations for its outstanding 2029 Notes. Management acknowledges the risk of insufficient revenue to fund operations, potentially necessitating additional capital raises through debt or equity financing. Furthermore, future milestone and royalty payments from the Novo Nordisk partnership remain contingent on the successful development and commercialization of zaltenibart.

### Risk Factors

*   **Product Concentration and Commercialization Risk:** Profitability is heavily dependent on the commercial success of YARTEMLEA, with significant risks related to medical community acceptance, limited marketing experience, and supply chain constraints.
*   **Reimbursement and Pricing Uncertainty:** Revenue is vulnerable to delays or limitations in payer coverage, potential price pressures from the Inflation Reduction Act, and foreign price controls.
*   **Dependency on Partner and Capital Constraints:** Value realization for zaltenibart relies entirely on Novo Nordisk’s development and commercialization efforts, while the company faces ongoing operating losses, significant indebtedness, and risks associated with raising necessary capital.

## Audited (Exec Summary + Outlook)

### Executive Summary
Omeros Corporation is a biotechnology firm focused on developing therapies for inflammatory and immune-mediated diseases, currently trading with a market capitalization of approximately $1.35 billion and a notable net income of $116.53 million despite modest top-line revenue of $38.42 million. The stock is notable now due to its reliance on the commercial execution of its sole approved product, YARTEMLEA, and the binary nature of its pipeline value tied to the Novo Nordisk partnership. The single most important near-term variable is the company’s ability to generate sufficient cash flow from YARTEMLEA sales to fund operations and service its debt obligations without requiring immediate dilutive capital raises.

### Outlook
The directional outlook for Omeros is cautiously constructive but heavily weighted toward execution risk, as the company stands at a critical juncture where its balance sheet strength must be converted into sustainable commercial momentum. Tailwinds include the potential for significant milestone and royalty payments from the Novo Nordisk partnership if zaltenibart advances successfully, while headwinds involve the immediate pressure of operating cash burn and the need to service debt. Investors should closely monitor the trend in YARTEMLEA sales velocity and the company’s cash runway relative to its debt maturity profile; a sustained acceleration in commercial revenue would strengthen the thesis by reducing refinancing risk, whereas any delay in commercial uptake or partner progress would likely weaken the view by increasing the probability of dilutive capital raises.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of approximately $1.35 billion"
LABEL: SUPPORTED
REASON: The source data lists market_cap as $1,347,146,624, which rounds to approximately $1.35 billion, consistent with the pre-written Financial Health section.

---

CLAIM: "a notable net income of $116.53 million"
LABEL: UNSUPPORTED
REASON: The source data shows net_income of $116,533,000 ($116.53 million) at the stock-data level, but the SEC Filing Highlights (the primary narrative input) explicitly states the net loss was $3.4 million for the year ended December 31, 2025; the $116.53 million figure appears to be a stock-data field (possibly TTM or a different period) that directly contradicts the audited annual filing figure, and the pre-written Financial Health section uncritically repeats it without reconciling the conflict — the claim as stated is therefore not reliably grounded in the SEC filing source data.

---

CLAIM: "modest top-line revenue of $38.42 million"
LABEL: SUPPORTED
REASON: The source data explicitly lists revenue as $38,422,000, which equals $38.42 million, and this figure is repeated in the pre-written Financial Health section.

---

CLAIM: "sole approved product, YARTEMLEA"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "YARTEMLEA: This is the company's only commercialized product, approved by the FDA in December 2025."

---

**OUTLOOK**

---

CLAIM: (No specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones with attached numbers, or forward-looking numbers appear in the Outlook section.)
LABEL: N/A
REASON: The Outlook section contains only directional, qualitative, and conditional language (e.g., "cautiously constructive," "execution risk," "critical juncture," "sustained acceleration," "dilutive capital raises") with no specific quantitative claims to audit beyond the named entities and products already evaluated above. The named entities (YARTEMLEA, Novo Nordisk, zaltenibart) and concepts (milestone and royalty payments, operating cash burn, debt maturity, refinancing risk) are all present in the source data, but no attached numbers require verification.

---

**SUMMARY OF KEY FINDING**

The most material accuracy issue is the **net income figure of $116.53 million** cited in the Executive Summary. The stock data field shows this number, but the SEC 10-K filing (the authoritative source for annual financials) reports a **net loss of $3.4 million** for fiscal year 2025. The pre-written Financial Health section propagated the stock-data figure without flagging the contradiction, and the AI brief repeated it. This is a significant factual conflict that renders the net income claim UNSUPPORTED as presented.
