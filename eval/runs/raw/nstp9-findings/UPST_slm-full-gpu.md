# UPST — slm-full-gpu

## Metadata

ticker: UPST
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 4d3e03cf7f379375013d06a546542f298378ff4331855cead947233ab3e920d6
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 763, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 16.401, "latency_s_total": 16.401, "parse_failure": 0, "prompt_tokens": 3011, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 519, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 9.526, "latency_s_total": 9.526, "parse_failure": 0, "prompt_tokens": 2333, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 139, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.93, "latency_s_total": 3.93, "parse_failure": 0, "prompt_tokens": 692, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 181, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.408, "latency_s_total": 5.408, "parse_failure": 0, "prompt_tokens": 686, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 135, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 8.473, "latency_s_total": 8.473, "parse_failure": 0, "prompt_tokens": 592, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 129, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 7.687, "latency_s_total": 7.687, "parse_failure": 0, "prompt_tokens": 844, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 873, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.676, "latency_s_total": 17.676, "parse_failure": 0, "prompt_tokens": 1548, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "UPST",
  "company_name": "Upstart Holdings, Inc.",
  "current_price": 24.35,
  "currency": "USD",
  "market_cap": 2369572864.0,
  "pe_ratio": 45.943398,
  "forward_pe": 7.005259,
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
The company’s business is heavily influenced by uncontrollable macroeconomic factors. Adverse economic conditions, such as inflation, higher interest rates, unemployment, or recession, can reduce borrower demand, lower approval and acceptance rates, and increase delinquencies and defaults. Because Upstart’s operations are concentrated in U.S. consumer credit, negative developments in the U.S. economy or consumer credit markets could have a disproportionate impact on the business.

**2. Dependence on Institutional Capital and Funding Risks**
Upstart relies on diverse and resilient sources of capital from institutional investors, including through whole loans, pass-through certificates, and asset-backed securities. Key risks include:
*   **Committed Capital and Co-Investment:** A significant portion of funding comes from arrangements that may require Upstart to compensate investors if loan credit performance deviates from expectations or if committed loan sale volumes are not achieved.
*   **Cost of Capital:** Capital arrangements made during high-interest-rate periods may become more costly if rates decline while terms remain fixed.
*   **Capital Constraints:** If institutional investors reduce funding or if Upstart cannot secure new arrangements on reasonable terms, the company may need to rely more heavily on its balance sheet, incur higher funding costs, or accept less favorable terms.

**3. Securitization and Financing Exposures**
The company facilitates securitizations and uses warehouse credit facilities to finance loans. Risks in this area include:
*   **Risk Retention:** As a sole sponsor, Upstart must retain a portion of the credit risk under Regulation RR. If these retained interests decline in value or cannot be refinanced on acceptable terms, liquidity and results of operations could suffer.
*   **Representations and Warranties:** If representations regarding transferred loans are inaccurate and not cured, Upstart may be required to repurchase loans or make indemnification payments, which could strain liquidity and harm its reputation.
*   **Regulatory Compliance:** Changes in laws such as the Dodd-Frank Act, the Investment Company Act of 1940, and the "Volcker Rule" may limit the structure of securitizations or restrict access to capital markets.

**4. Technology and AI Model Effectiveness**
Upstart’s growth prospects are tied to the effectiveness of its artificial intelligence (AI) models. If these models fail to accurately or timely reflect changes in borrowers' credit risk due to economic shifts, or if there are significant disruptions or failures in the AI lending platform, the business could be adversely affected.

**5. Operational and Strategic Risks**
*   **Lending Partners:** The business depends on retaining existing lending partners and attracting new ones, as a limited number of partners account for a significant portion of originations and revenue.
*   **Loan Aggregators:** Upstart relies on strategic relationships with loan aggregators to attract applicants; failure to maintain these relationships could harm the business.
*   **Product Mix:** A significant portion of historical business has depended on a single loan product, making the company vulnerable to shifts in product demand.
*   **Profitability:** The company has incurred net losses in the past and may not achieve or sustain profitability in the future.
*   **Regulatory Compliance:** The business is subject to a wide range of evolving laws and regulations. Failure to comply, or the perceived failure to do so, could harm the business.
*   **Security:** Security breaches or improper access to data could harm reputation and expose the company to liability.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Economic Conditions:** The business is adversely affected by uncontrollable economic factors, including uncertainty, volatility, and negative trends that impact capital supply, borrower demand, and repayment ability. Adverse macroeconomic conditions can reduce loan origination volumes, increase funding costs, and lead to higher delinquencies and defaults.
*   **Loan Funding and Capital Sources:** The company depends on diverse and resilient loan funding from institutional investors. Risks include the inability to maintain these sources, manage risks associated with committed capital and co-investment arrangements, and the potential for decreased capital availability or increased costs.
*   **AI Model Effectiveness:** The business relies on artificial intelligence models to approve borrowers. If these models are ineffective, fail to improve, or do not accurately reflect changes in economic conditions regarding credit risk, growth and financial results could be harmed.
*   **Concentration of Lending Partners:** A limited number of lending partners account for a significant portion of loan originations and revenue. The business depends on retaining existing partners and attracting new ones.
*   **Profitability and Financial Performance:** The company has incurred net losses in the past and may not achieve or sustain profitability. Quarterly results may fluctuate significantly.
*   **Balance Sheet and Servicing Risks:** Risks include managing loans held on the balance sheet, loan servicing and collections obligations, and the Upstart Macro Index (UMI).
*   **Product Mix and New Offerings:** A significant portion of business has historically depended on a single loan product. Shifts in demand or the failure of new loan products and service offerings could adversely affect the business.
*   **Technology and Security:** Significant disruptions or failures in technology systems, including the AI lending platform, and security breaches or improper access to data could harm reputation and results of operations.
*   **Strategic Relationships:** The company relies on strategic relationships with loan aggregators to attract applicants. Inability to maintain or replace these services could harm the business.
*   **Legal and Regulatory Compliance:** The business is subject to a wide range of evolving laws and regulations. Failure or perceived failure to comply could harm the business.
*   **Reputation and Brand:** Failure to maintain, protect, and promote the brand may harm the business.
*   **Repurchase and Counterparty Risks:** Inaccurate representations and warranties in securitization or loan sale arrangements may require loan repurchases or payments. Additionally, counterparty failures in derivative instruments or facilities could result in losses.

## Pre-written sections (judge input)

### Financial Health

Upstart Holdings, Inc. (UPST) is currently trading at $24.35 with a market capitalization of approximately $2.37 billion. The company reports annual revenue of $1.29 billion and maintains a net profit margin of 4.69%, reflecting a net income of $60.3 million. While the trailing P/E ratio stands at 45.94, the significantly lower forward P/E of 7.01 suggests market expectations for improved earnings efficiency in the near term. This divergence indicates that current valuation multiples may be elevated relative to recent historical performance but are anticipated to normalize as profitability scales.

### Recent Developments

Upstart Holdings, Inc. (UPST) is currently trading at $24.35, reflecting a significant decline from its 52-week high of $55.22, though it remains near its yearly low of $22.555. The company maintains a positive net income of $60.3 million with a profit margin of 4.69%, supported by revenues of $1.29 billion. Notably, the forward P/E ratio stands at a compelling 7.01, suggesting market expectations for substantial earnings growth despite the current high trailing P/E of 45.94. Investors should monitor upcoming filings, including the 10-K due in February 2026 and the 10-Q in August 2026, for updates on risk factors and operational performance.

### SEC Filing Highlights
Upstart’s financial performance remains highly sensitive to macroeconomic headwinds, including rising interest rates and potential recessions, which directly impact borrower demand and credit quality. The company faces significant funding risks due to its reliance on institutional capital, particularly where committed capital arrangements may require compensation if loan performance deviates from expectations. Operational resilience is further challenged by the necessity to retain credit risk in securitizations and maintain critical relationships with a concentrated base of lending partners and loan aggregators. Additionally, the firm’s growth trajectory is contingent on the continued effectiveness of its AI models in accurately assessing credit risk amidst shifting economic conditions.

### Risk Factors

*   **Macroeconomic Sensitivity:** Adverse economic conditions, volatility, and negative trends can significantly reduce loan origination volumes, increase funding costs, and lead to higher delinquencies and defaults.
*   **AI Model Dependency:** The business relies heavily on artificial intelligence models for credit approval; if these models fail to improve, become ineffective, or inaccurately reflect changes in credit risk, financial results could be harmed.
*   **Capital and Partner Concentration:** The company depends on diverse institutional funding sources and a limited number of lending partners; any inability to maintain these capital sources or retain key partners could adversely impact operations and revenue.

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings, Inc. leverages artificial intelligence to facilitate consumer lending, currently operating with a market capitalization of approximately $2.37 billion and generating $1.29 billion in annual revenue. The stock is notable for its significant price depreciation from its 52-week high of $55.22 to the current $24.35, juxtaposed against a forward P/E ratio of 7.01 that signals strong market expectations for near-term earnings efficiency. The single most important near-term variable shaping the investment outcome is the stability of macroeconomic conditions and interest rates, which directly dictate borrower demand and credit quality.

### Outlook
The directional outlook for Upstart is cautiously constructive, driven by the market’s anticipation of improved earnings efficiency as reflected in the low forward P/E, yet tempered by substantial macroeconomic and operational risks. Key variables to monitor include the stability of interest rates, which influence borrower demand, and the ongoing performance of the AI credit models in maintaining accurate risk assessment during economic shifts. The thesis would be strengthened by evidence of sustained loan origination volumes and stable credit quality metrics, while a deterioration in the macroeconomic environment or a failure to retain key institutional funding partners would significantly weaken the investment case.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of approximately $2.37 billion"
LABEL: SUPPORTED
REASON: Source data lists market_cap = 2,369,572,864.0 USD, which rounds to approximately $2.37 billion; the pre-written Financial Health section also states "approximately $2.37 billion."

---

CLAIM: "$1.29 billion in annual revenue"
LABEL: SUPPORTED
REASON: Source data lists revenue = 1,285,890,048.0 USD, which rounds to $1.29 billion; confirmed in both pre-written sections.

---

CLAIM: "52-week high of $55.22"
LABEL: SUPPORTED
REASON: Source data explicitly states week_52_high = 55.22.

---

CLAIM: "current $24.35"
LABEL: SUPPORTED
REASON: Source data explicitly states current_price = 24.35.

---

CLAIM: "forward P/E ratio of 7.01"
LABEL: SUPPORTED
REASON: Source data lists forward_pe = 7.005259, which rounds to 7.01; confirmed in pre-written sections.

---

CLAIM: "signals strong market expectations for near-term earnings efficiency"
LABEL: INFERENCE
REASON: This is a directional interpretive restatement of the forward P/E of 7.01 being significantly lower than the trailing P/E of 45.94, both of which are present in the source data; the inference step is a standard valuation interpretation explicitly made in the pre-written sections.

---

**OUTLOOK**

---

CLAIM: "low forward P/E"
LABEL: SUPPORTED
REASON: The forward P/E of 7.005259 (≈7.01) is explicitly present in the source data and is materially lower than the trailing P/E of 45.94, making "low" arithmetically accurate in context.

---

*No additional standalone quantitative figures, price targets, thresholds, named product milestones, or specific percentages appear in the Outlook section beyond the qualitative/directional language already addressed above. All remaining language in the Outlook is qualitative risk narrative drawn from the SEC Filing Highlights and Risk Factors pre-written sections, containing no discrete quantitative claims requiring separate audit entries.*
