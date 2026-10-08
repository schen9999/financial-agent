# OMER — slm-full-cpu

## Metadata

ticker: OMER
arm: slm-full-cpu
judge_prompt_version: v2
context_sha256: 6c99ab71139fd86383e139ad649896d126cd680826be771259687968ab345d44
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 715, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 201.024, "latency_s_total": 201.024, "parse_failure": 0, "prompt_tokens": 2632, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 377, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 159.107, "latency_s_total": 159.107, "parse_failure": 0, "prompt_tokens": 3034, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 156, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 46.194, "latency_s_total": 46.194, "parse_failure": 0, "prompt_tokens": 678, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 116, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 33.061, "latency_s_total": 33.061, "parse_failure": 0, "prompt_tokens": 672, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 159, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 46.457, "latency_s_total": 46.457, "parse_failure": 0, "prompt_tokens": 447, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 186, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 62.202, "latency_s_total": 62.202, "parse_failure": 0, "prompt_tokens": 793, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 880, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 152.717, "latency_s_total": 152.717, "parse_failure": 0, "prompt_tokens": 1608, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "OMER",
  "company_name": "Omeros Corporation",
  "current_price": 18.61,
  "currency": "USD",
  "market_cap": 1347146624.0,
  "pe_ratio": 11.278789,
  "forward_pe": 15.130081,
  "week_52_high": 21.24,
  "week_52_low": 4.06,
  "revenue": 38422000.0,
  "net_income": 116533000.0,
  "profit_margin": 3.2488198,
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
*   **Debt Structure:** The company had $70.8 million in outstanding aggregate principal amount of its 2029 Notes and approximately $1.2 million in outstanding finance lease obligations. The $17.1 million in 5.25% convertible senior notes due in February 2026 (the "2026 Notes") had matured and been repaid in full.
*   **Cash Flow Risks:** Indebtedness limits cash flow available for operations and exposes the company to risks such as requiring substantial cash flow for debt service, limiting access to additional financing, and diluting existing stockholders if notes are converted.

**Product Commercialization and Revenue Dependence**
*   **Reliance on YARTEMLEA:** The company’s ability to achieve profitability is highly dependent on the commercial success of YARTEMLEA, its only commercialized product, which received FDA approval for commercial sale in the United States in December 2025.
*   **Commercialization Risks:** Success depends on physician and patient acceptance, reimbursement policies, and the company’s limited experience in marketing, selling, and managing third-party manufacturing. Failure to commercialize YARTEMLEA successfully could materially adversely affect the business and stock price.
*   **Reimbursement Challenges:** Revenue prospects are heavily influenced by coverage and reimbursement from government and private payers. Payers may require discounts, challenge prices, or limit coverage to specific approved uses, potentially impacting profitability.

**Future Funding and Development**
*   **Capital Needs:** The company expects to continue spending substantial amounts on clinical trials, manufacturing, commercializing YARTEMLEA, supporting sales and marketing, and servicing debt.
*   **Funding Uncertainty:** There is no assurance that the company will generate sufficient revenue to fund operations fully. If additional capital is not raised through debt, equity, or partnerships, the company may need to delay, scale back, or discontinue development programs.
*   **Partnership Dependencies:** Future value realization is contingent on the successful development and commercialization of zaltenibart in partnership with Novo Nordisk. If this product fails to develop or commercialize as expected, milestone and royalty payments may be significantly reduced or eliminated.

**Risk Factors**
*   **General Risks:** The trading price of common stock could decline due to various risks, including those currently deemed immaterial or unknown.
*   **Operational Risks:** The company faces risks related to supply chain reliance, regulatory compliance (both U.S. and international), and adverse economic conditions.
*   **Default Risks:** Failure to comply with financial covenants or make scheduled debt payments could result in default, making indebtedness immediately payable in full.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Dependence on YARTEMLEA:** The company’s ability to achieve profitability is highly dependent on the commercial success of YARTEMLEA, its only commercialized product. Failure to successfully commercialize this product could materially adversely affect the business, financial condition, and stock price.
*   **Commercialization Challenges:** There are risks related to limited experience in marketing, selling, and distributing YARTEMLEA, reliance on a limited number of manufacturers and suppliers, and potential lack of acceptance by physicians, patients, and payers.
*   **Reimbursement and Pricing Risks:** Success depends heavily on obtaining adequate coverage and reimbursement from government and private payers. Risks include delays in reimbursement, limited coverage, pricing challenges, government price controls, and the requirement for predetermined discounts. Reductions in reimbursement from programs like Medicare could negatively impact payments from private payers.
*   **Dependence on Novo Nordisk for Zaltenibart:** The company’s ability to realize value from zaltenibart depends on Novo Nordisk’s development, regulatory approval, and commercialization efforts. Novo Nordisk controls key decisions, and the company may receive little to no milestone or royalty payments if Novo Nordisk fails to advance or commercialize the product successfully.
*   **Operating Losses and Capital Needs:** The company has incurred cumulative operating losses since inception and expects to continue incurring losses until generating significant revenue. There is a risk that the company may be unable to raise additional capital when needed, which could force it to delay, scale back, or discontinue development or commercialization programs.
*   **Indebtedness:** The company has outstanding liabilities, including convertible senior notes and finance lease obligations, which could limit cash flow available for operations and expose the company to financial risks.

## Pre-written sections (judge input)

### Financial Health

Omeros Corporation (OMER) is currently trading at $18.61, reflecting a market capitalization of approximately $1.35 billion. The company demonstrates strong valuation metrics with a P/E ratio of 11.28 and a forward P/E of 15.13, suggesting potential upside relative to current earnings. Recent financial data indicates a revenue of $38.42 million and a net income of $116.53 million, resulting in a healthy profit margin of 3.25%. This profitability profile, combined with a valuation below the 52-week high of $21.24, positions the stock as a potentially undervalued opportunity within the biotechnology sector.

### Recent Developments

Omeros Corporation (OMER) has recently filed its Annual Report on Form 10-K for the fiscal year ended December 31, 2025, alongside a subsequent Quarterly Report on Form 10-Q for the period ending August 12, 2026. These filings highlight ongoing risk factors related to the company's ability to achieve profitability and the commercial success of its product candidates. Investors should carefully review these documents to assess the material uncertainties and potential adverse effects on the company's financial condition and operating results.

### SEC Filing Highlights
As of December 31, 2025, Omeros Corporation held $171.8 million in cash and short-term investments, though it reported a net loss of $3.4 million and $116.1 million in operating cash usage for the year. The company’s financial outlook remains heavily dependent on the commercial success of its newly approved product, YARTEMLEA, which received FDA approval in December 2025. While the $17.1 million convertible senior notes due in February 2026 were repaid in full, the firm still carries $70.8 million in 2029 Notes and faces significant risks regarding reimbursement policies and limited commercialization experience. Future viability hinges on generating sufficient revenue from YARTEMLEA and securing continued funding, as the company has incurred cumulative operating losses since inception.

### Risk Factors

*   **Concentration on YARTEMLEA:** Profitability is heavily dependent on the commercial success of YARTEMLEA, with significant risks related to limited commercialization experience, supply chain reliance, and potential lack of market acceptance.
*   **Reimbursement and Pricing Uncertainty:** Success relies on adequate coverage from government and private payers, exposing the company to risks such as delayed approvals, limited coverage, government price controls, and potential reductions in Medicare payments.
*   **Dependence on Novo Nordisk for Zaltenibart:** The value of the zaltenibart pipeline is contingent on Novo Nordisk’s development and commercialization efforts, with the company receiving little to no revenue if Novo Nordisk fails to advance the product.

## Audited (Exec Summary + Outlook)

### Executive Summary
Omeros Corporation is a biotechnology firm leveraging its $171.8 million in cash reserves to commercialize its newly FDA-approved product, YARTEMLEA, while maintaining a valuation profile that appears undervalued relative to its current earnings metrics. The stock is notable now as it transitions from a development-stage entity to a commercial operator, with its near-term trajectory entirely dependent on the market adoption and reimbursement success of YARTEMLEA.

### Outlook
The directional outlook for Omeros is cautiously constructive, driven by the successful launch of YARTEMLEA and the elimination of near-term debt obligations, yet tempered by the inherent risks of a small-cap biotech entering the commercial phase. Investors should closely monitor the pace of YARTEMLEA adoption, the stability of payer reimbursement policies, and the company’s ability to manage operating cash burn as it scales commercial operations. The thesis would be strengthened by evidence of sustained revenue growth and improved cash flow generation, while a weakening view would result from slower-than-expected market penetration, adverse reimbursement decisions, or a failure to secure adequate funding to support ongoing commercialization efforts.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$171.8 million in cash reserves"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights explicitly states "As of December 31, 2025, the company held $171.8 million in cash, cash equivalents, and short-term investments," and the SEC Filing Highlights pre-written section repeats this figure.

---

CLAIM: "newly FDA-approved product, YARTEMLEA"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights states YARTEMLEA "received FDA approval for commercial sale in the United States in December 2025," confirming it is newly FDA-approved.

---

CLAIM: "valuation profile that appears undervalued relative to its current earnings metrics"
LABEL: INFERENCE
REASON: This is a directional interpretive claim derivable from the P/E of 11.28 and forward P/E of 15.13 figures present in the source data and Financial Health section, which the pre-written section explicitly characterizes as suggesting "potential upside relative to current earnings."

---

**OUTLOOK**

---

CLAIM: "successful launch of YARTEMLEA"
LABEL: UNSUPPORTED
REASON: The source data confirms FDA approval in December 2025 but contains no data on actual launch success, sales figures, or commercial performance metrics to support characterizing the launch as "successful."

---

CLAIM: "elimination of near-term debt obligations"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights confirms "The $17.1 million in 5.25% convertible senior notes due in February 2026 (the '2026 Notes') had matured and been repaid in full," supporting the claim that the nearest-term debt obligation was eliminated.

---

No additional quantitative figures, price targets, thresholds, ratios, specific percentages, named product milestones with attached numbers, or forward-looking numerical claims appear in the Outlook section beyond those evaluated above. The remaining Outlook language is qualitative and directional (e.g., "pace of adoption," "stability of payer reimbursement," "sustained revenue growth") and does not constitute specific quantitative or forward-looking numerical claims subject to audit under the defined criteria.
