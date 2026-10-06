# UPST — slm-full-cpu

## Metadata

ticker: UPST
arm: slm-full-cpu
judge_prompt_version: v2
context_sha256: 738173267f3b57d0fdd5db12c7173caf85be4c041f792e80c516f372eec83359
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 773, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 226.439, "latency_s_total": 226.439, "parse_failure": 0, "prompt_tokens": 3011, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 535, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 177.369, "latency_s_total": 177.369, "parse_failure": 0, "prompt_tokens": 2333, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 122, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 53.36, "latency_s_total": 53.36, "parse_failure": 0, "prompt_tokens": 689, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 198, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 75.879, "latency_s_total": 75.879, "parse_failure": 0, "prompt_tokens": 683, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 154, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 74.076, "latency_s_total": 74.076, "parse_failure": 0, "prompt_tokens": 608, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 129, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 79.407, "latency_s_total": 79.407, "parse_failure": 0, "prompt_tokens": 854, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 927, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 109.48, "latency_s_total": 109.48, "parse_failure": 0, "prompt_tokens": 1586, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "UPST",
  "company_name": "Upstart Holdings, Inc.",
  "current_price": 23.975,
  "currency": "USD",
  "market_cap": 2333080320.0,
  "pe_ratio": 47.95,
  "forward_pe": 6.897375,
  "week_52_high": 55.22,
  "week_52_low": 22.555,
  "financial_currency": "USD",
  "revenue": 1285890048.0,
  "net_income": 60334000.0,
  "profit_margin_pct": 4.69,
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
    "filing_date": "2026-02-10",
    "summary": "ITEM 1A. RISK FACTORS RISK FACTORS Investing in our common stock involves a high degree of risk. The risks and uncertainties described below should be carefully considered, together with all of the other information in this Annual Report on Form 10-K, including the section titled \u201cManagement\u2019s Discussion and Analysis of Financial Condition and Results of Operations\u201d and our consolidated financial statements and related notes, before making a decision to invest in our common stock. Our business, financial condition, results of operations, or prospects could also be harmed by risks and uncertainties not currently known to us or that we currently do not believe are material. If any of the risks actually occur, our business, financial condition, results of operations, and prospects could be ad"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-04",
    "summary": "ITEM 1A. RISK FACTORS RISK FACTORS Investing in our common stock involves a high degree of risk. The risks and uncertainties described below should be carefully considered, together with all of the other information in this Quarterly Report on Form 10-Q, including the section titled \u201cManagement\u2019s Discussion and Analysis of Financial Condition and Results of Operations\u201d and our condensed consolidated financial statements and related notes, before making a decision to invest in our common stock. Our business, financial condition, results of operations, or prospects could also be harmed by risks and uncertainties not currently known to us or that we currently do not believe are material. If any of the risks actually occur, our business, financial condition, results of operations, and prospect"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] Based on the provided risk factors from the SEC EDGAR filings for Upstart (ticker: UPST), the key takeaways regarding the company's business, financial condition, and operational risks include:

**1. Sensitivity to Economic Conditions**
The company’s business is heavily influenced by uncontrollable macroeconomic factors. Adverse economic trends, such as inflation, higher interest rates, unemployment, or recession, can significantly reduce borrower demand, approval rates, and loan origination volumes. Because many borrowers have limited or poor credit histories, they are disproportionately affected by these conditions, potentially leading to higher delinquencies, defaults, and charge-offs.

**2. Dependence on Institutional Capital and Funding Risks**
Upstart relies on diverse and resilient sources of capital from institutional investors, including through whole loans, pass-through certificates, and asset-backed securities. Key risks include:
*   **Committed Capital and Co-Investment:** A significant portion of funding comes from arrangements that may require the company to compensate investors if loan performance deviates from expectations or if committed sale volumes are not met.
*   **Cost of Capital:** Capital arrangements made during high-interest periods may become more costly if rates decline while terms remain fixed.
*   **Liquidity Constraints:** If institutional capital becomes unavailable or less favorable, the company may need to rely more heavily on its balance sheet, incurring higher funding costs or accepting less efficient capital structures.

**3. Securitization and Financing Complexities**
The company facilitates securitizations and uses warehouse credit facilities to finance loans. Risks in this area include:
*   **Risk Retention:** As a sole sponsor, Upstart must retain a portion of credit risk under Regulation RR. If these retained interests decline in value or cannot be refinanced on acceptable terms, liquidity and results of operations may suffer.
*   **Regulatory Compliance:** Changes in laws such as the Dodd-Frank Act, the Investment Company Act of 1940, and the "Volcker Rule" may limit the structure of securitizations or restrict access to capital markets.
*   **Repurchase Obligations:** If representations and warranties regarding transferred loans are inaccurate, the company may be forced to repurchase loans or make indemnification payments, which could strain liquidity and harm its reputation.

**4. Technology and Artificial Intelligence (AI) Reliance**
The business model is deeply integrated with its AI lending platform. Key technology-related risks include:
*   **Model Effectiveness:** If AI models fail to accurately or timely reflect changes in borrower credit risk due to economic shifts, growth prospects and financial results could be adversely affected.
*   **System Disruptions:** Any significant failure or disruption in technology systems, including the AI platform, could harm business operations and financial condition.

**5. Operational and Strategic Dependencies**
*   **Lending Partners:** The business depends on retaining a limited number of key lending partners who account for a significant portion of originations and revenue.
*   **Loan Aggregators:** Upstart relies on strategic relationships with loan aggregators to attract applicants; failure to maintain these relationships could negatively impact business.
*   **Product Concentration:** A significant portion of historical business has depended on a single loan product, making the company vulnerable to shifts in product demand.
*   **Profitability:** The company has incurred net losses in the past and faces uncertainty regarding its ability to sustain or achieve future profitability.

**6. Regulatory and Compliance Exposure**
The company operates under a wide range of evolving laws and regulations. Failure to comply, or even the perceived failure to comply, with these laws could harm the business, financial condition, and reputation. Additionally, security breaches or improper access to data could lead to liability and reputational damage.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Economic Conditions:** The business is adversely affected by uncontrollable economic factors, including uncertainty, volatility, and negative trends that impact capital supply, borrower demand, and repayment ability. Adverse macroeconomic conditions can reduce loan origination volumes, increase funding costs, and lead to higher delinquencies and defaults.
*   **Loan Funding and Capital Sources:** The company depends on diverse and resilient loan funding from institutional investors. Risks include the inability to maintain these sources, manage risks associated with committed capital and co-investment arrangements, and the potential for decreased capital availability or increased costs.
*   **AI Model Effectiveness:** The business relies on artificial intelligence models to approve borrowers. If these models are ineffective, fail to improve, or do not accurately reflect changes in economic conditions regarding credit risk, growth and financial results could be harmed.
*   **Concentration of Lending Partners:** A limited number of lending partners account for a significant portion of loan originations and revenue. The business depends on retaining existing partners and attracting new ones.
*   **Profitability and Financial Performance:** The company has incurred net losses in the past and may not achieve profitability in the future. Quarterly results may fluctuate significantly.
*   **Balance Sheet and Servicing Risks:** Risks include managing loans held on the balance sheet, loan servicing and collections obligations, and the Upstart Macro Index (UMI).
*   **Product Mix:** A significant portion of the business has historically depended on a single loan product, making it vulnerable to shifts in product demand or mix.
*   **Security and Technology:** Security breaches, improper data access, and disruptions or failures in technology systems, including the AI lending platform, could harm reputation and operations.
*   **Loan Aggregators:** The business relies on strategic relationships with loan aggregators to attract applicants. Failure to maintain these relationships or replace their services could adversely affect the business.
*   **Legal and Regulatory Compliance:** The business is subject to a wide range of evolving laws and regulations. Failure or perceived failure to comply could harm the business.
*   **Reputation and Brand:** Failure to maintain, protect, and promote the brand may harm the business.
*   **Securitization and Repurchase Obligations:** Inaccurate representations and warranties in securitization or loan sale arrangements may require loan repurchases or indemnification payments, which could strain liquidity and harm reputation.
*   **Counterparty Risk:** The company is subject to counterparty risk from derivative instruments, beneficial interests, warehouse facilities, and custodial arrangements.

## Pre-written sections (judge input)

### Financial Health

Upstart Holdings, Inc. (UPST) is currently trading at $23.98 with a market capitalization of approximately $2.33 billion. The company reports annual revenue of $1.29 billion and maintains a healthy net profit margin of 4.69%. While the trailing P/E ratio stands at 47.95, the significantly lower forward P/E of 6.90 suggests strong expected earnings growth in the near term. This valuation discrepancy indicates that the market anticipates a substantial improvement in profitability relative to current earnings levels.

### Recent Developments

Upstart Holdings, Inc. (UPST) is currently trading near its 52-week low of $22.56, reflecting ongoing market caution despite a significantly lower forward P/E ratio of 6.90 compared to its trailing P/E of 47.95. The company recently filed its 10-K annual report on February 10, 2026, and is scheduled to submit its next 10-Q quarterly report on August 4, 2026, both of which highlight substantial risk factors that investors must carefully evaluate. With a modest profit margin of 4.69% and no dividend yield, the stock's near-term trajectory will likely depend on its ability to navigate credit service sector headwinds and demonstrate sustained operational efficiency. Investors should monitor upcoming regulatory filings and earnings data closely, as the wide disparity between current valuation metrics suggests high volatility and uncertainty regarding future growth prospects.

### SEC Filing Highlights
Upstart’s financial performance remains highly sensitive to macroeconomic headwinds, with rising interest rates and potential recessions threatening to suppress borrower demand and increase default rates. The company faces significant funding risks due to its reliance on institutional capital, where unfavorable market conditions or fixed-cost arrangements could strain liquidity and increase the cost of capital. Operational resilience is further challenged by dependencies on a limited number of key lending partners and the continuous effectiveness of its proprietary AI models in predicting credit risk. Additionally, regulatory complexities surrounding securitization and data privacy pose ongoing compliance risks that could impact the company’s ability to scale and maintain profitability.

### Risk Factors

*   **Macroeconomic Sensitivity and Credit Risk:** Adverse economic conditions, volatility, or negative trends can significantly reduce loan origination volumes, increase funding costs, and lead to higher delinquencies and defaults, directly impacting financial performance.
*   **Reliance on AI Models and Capital Sources:** The business is heavily dependent on the continued effectiveness of its AI lending models to accurately assess credit risk, as well as its ability to secure diverse and resilient funding from institutional investors without facing increased costs or capital shortages.
*   **Concentration and Regulatory Risks:** Significant revenue concentration among a limited number of lending partners and loan aggregators, combined with exposure to evolving legal and regulatory compliance requirements, poses substantial operational and reputational threats.

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings, Inc. operates as an AI-powered lending platform that connects borrowers with capital partners, currently reporting annual revenue of $1.29 billion and maintaining a net profit margin of 4.69%. The stock is notable for its significant valuation discrepancy, with a trailing P/E of 47.95 contrasting sharply against a forward P/E of 6.90, suggesting the market anticipates substantial near-term earnings growth despite trading near its 52-week low. The single most important near-term variable shaping the investment outcome is the company’s ability to demonstrate sustained operational efficiency and navigate credit service sector headwinds while proving the continued resilience of its AI models.

### Outlook
The directional outlook for Upstart is cautiously constructive, driven by the market’s expectation of substantial earnings improvement as reflected in the low forward P/E, yet tempered by the stock’s proximity to its 52-week low and inherent macroeconomic sensitivities. Key variables to monitor include the stability of institutional funding costs, the continued efficacy of AI models in predicting credit risk during economic shifts, and the company’s ability to maintain its 4.69% profit margin amidst potential headwinds. The thesis would be strengthened by evidence of sustained operational efficiency and successful navigation of regulatory complexities, while a deterioration in credit quality or a failure to secure diverse capital sources would weaken the investment case and likely exacerbate the current volatility.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative, forward-looking, and specific factual claim in the Executive Summary and Outlook sections.

---

## EXECUTIVE SUMMARY

---

**CLAIM:** "currently reporting annual revenue of $1.29 billion"
**LABEL:** SUPPORTED
**REASON:** Source data shows revenue of $1,285,890,048, which rounds to $1.29 billion; the pre-written Financial Health section also states "$1.29 billion."

---

**CLAIM:** "maintaining a net profit margin of 4.69%"
**LABEL:** SUPPORTED
**REASON:** Source data explicitly lists `profit_margin_pct: 4.69`, confirmed in both the Financial Health and Recent Developments pre-written sections.

---

**CLAIM:** "trailing P/E of 47.95"
**LABEL:** SUPPORTED
**REASON:** Source data explicitly lists `pe_ratio: 47.95`.

---

**CLAIM:** "forward P/E of 6.90"
**LABEL:** SUPPORTED
**REASON:** Source data lists `forward_pe: 6.897375`, which rounds to 6.90; confirmed in pre-written sections.

---

**CLAIM:** "trading near its 52-week low"
**LABEL:** SUPPORTED
**REASON:** Current price is $23.975; 52-week low is $22.555 and 52-week high is $55.22. The current price is approximately $1.42 above the 52-week low and $31.245 below the 52-week high, placing it very close to (within ~6% of) the 52-week low, confirming the positional claim arithmetically.

---

**CLAIM:** "the market anticipates substantial near-term earnings growth"
**LABEL:** INFERENCE
**REASON:** This is a standard market interpretation directly derivable from the contrast between the trailing P/E of 47.95 and forward P/E of 6.90, both present in the source data, without requiring any additional external fact.

---

## OUTLOOK

---

**CLAIM:** "the market's expectation of substantial earnings improvement as reflected in the low forward P/E"
**LABEL:** INFERENCE
**REASON:** Directly derivable from the forward P/E of 6.90 versus trailing P/E of 47.95, both present in the source data; this is a standard interpretive step requiring no external facts.

---

**CLAIM:** "the stock's proximity to its 52-week low"
**LABEL:** SUPPORTED
**REASON:** Current price $23.975 is approximately 6.3% above the 52-week low of $22.555, arithmetically confirming proximity to the 52-week low.

---

**CLAIM:** "the company's ability to maintain its 4.69% profit margin amidst potential headwinds"
**LABEL:** SUPPORTED
**REASON:** The 4.69% profit margin figure is explicitly present in the source data (`profit_margin_pct: 4.69`) and is used here as a reference benchmark, not a forward projection.

---

**CLAIM:** "stability of institutional funding costs" (as a key variable to monitor)
**LABEL:** SUPPORTED
**REASON:** The RAG SEC Highlights and Risk Factors sections explicitly identify reliance on institutional capital and cost of capital as key disclosed risks.

---

**CLAIM:** "continued efficacy of AI models in predicting credit risk during economic shifts" (as a key variable to monitor)
**LABEL:** SUPPORTED
**REASON:** Both the RAG SEC Highlights and Risk Factors sections explicitly identify AI model effectiveness and economic sensitivity as primary disclosed risks.

---

**CLAIM:** "a deterioration in credit quality or a failure to secure diverse capital sources would weaken the investment case"
**LABEL:** SUPPORTED
**REASON:** Both risks — credit quality deterioration and inability to secure diverse institutional capital — are explicitly enumerated in the RAG Risk Factors and SEC Highlights sections.

---

### Summary Table

| # | Claim | Label |
|---|-------|-------|
| 1 | Annual revenue of $1.29 billion | SUPPORTED |
| 2 | Net profit margin of 4.69% | SUPPORTED |
| 3 | Trailing P/E of 47.95 | SUPPORTED |
| 4 | Forward P/E of 6.90 | SUPPORTED |
| 5 | Trading near its 52-week low | SUPPORTED |
| 6 | Market anticipates substantial near-term earnings growth | INFERENCE |
| 7 | Market expectation of substantial earnings improvement (forward P/E) | INFERENCE |
| 8 | Stock's proximity to its 52-week low (Outlook) | SUPPORTED |
| 9 | Ability to maintain 4.69% profit margin | SUPPORTED |
| 10 | Stability of institutional funding costs as key variable | SUPPORTED |
| 11 | AI model efficacy as key variable | SUPPORTED |
| 12 | Credit quality deterioration / capital sourcing failure as downside risks | SUPPORTED |

**No UNSUPPORTED claims were identified.** All quantitative figures are traceable to the source data, and all forward-looking directional statements are grounded in explicitly disclosed risk factors or arithmetically derivable from present figures.
