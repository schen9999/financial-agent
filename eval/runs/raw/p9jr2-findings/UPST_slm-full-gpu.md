# UPST — slm-full-gpu

## Metadata

ticker: UPST
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: acdf85ee57243276e68236b050c7381341cd6b2f25b53403db5a4b87da486582
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 888, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 24.703, "latency_s_total": 24.703, "parse_failure": 0, "prompt_tokens": 3011, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 533, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 15.869, "latency_s_total": 15.869, "parse_failure": 0, "prompt_tokens": 2333, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 134, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.132, "latency_s_total": 5.132, "parse_failure": 0, "prompt_tokens": 687, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 191, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 7.124, "latency_s_total": 7.124, "parse_failure": 0, "prompt_tokens": 681, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 166, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 6.865, "latency_s_total": 6.865, "parse_failure": 0, "prompt_tokens": 606, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 144, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 6.391, "latency_s_total": 6.391, "parse_failure": 0, "prompt_tokens": 969, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 910, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 13.787, "latency_s_total": 13.787, "parse_failure": 0, "prompt_tokens": 1650, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "UPST",
  "company_name": "Upstart Holdings, Inc.",
  "current_price": 22.81,
  "currency": "USD",
  "market_cap": 2219710464.0,
  "pe_ratio": 45.62,
  "forward_pe": 6.562216,
  "week_52_high": 55.22,
  "week_52_low": 22.555,
  "revenue": 1285890048.0,
  "net_income": 60334000.0,
  "profit_margin": 0.046919998,
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
The company’s business is heavily influenced by uncontrollable macroeconomic factors. Negative economic trends, such as inflation, higher interest rates, unemployment, or recession, can reduce borrower demand, lower approval and acceptance rates, and increase delinquencies and defaults. Because the company’s operations are concentrated in U.S. consumer credit, adverse developments in the U.S. economy or consumer credit markets could have a disproportionate negative impact on its results.

**2. Dependence on Institutional Capital and Funding Risks**
Upstart relies on diverse and resilient sources of capital from institutional investors, including through whole loans, pass-through certificates, and asset-backed securities. Key risks in this area include:
*   **Committed Capital and Co-Investment:** A significant portion of funding comes from arrangements that may require the company to compensate investors if loan credit performance deviates from expectations or if committed loan sale volumes are not achieved.
*   **Cost of Capital:** Capital arrangements made during high-interest-rate periods may become more costly if rates decline while terms remain fixed.
*   **Capital Constraints:** If institutional investors reduce funding or if the company cannot secure new arrangements on reasonable terms, it may be forced to rely more heavily on its balance sheet, incur higher funding costs, or accept less favorable terms.

**3. Securitization and Financing Exposures**
The company facilitates securitizations and uses warehouse credit facilities to finance loans. Risks associated with these activities include:
*   **Risk Retention:** As a sole sponsor, the company must retain a portion of the credit risk (under Regulation RR). If these retained interests decline in value or cannot be refinanced on acceptable terms, liquidity and results of operations could suffer.
*   **Representations and Warranties:** If representations regarding transferred loans are inaccurate and not cured, the company may be required to repurchase loans or make indemnification payments, which could strain liquidity and harm its reputation.
*   **Regulatory Compliance:** Changes in laws, such as the Dodd-Frank Act, the Investment Company Act of 1940, or the "Volcker Rule," may limit the structure of securitizations or restrict access to capital markets.

**4. Technology and Artificial Intelligence (AI) Reliance**
The company’s growth and operational success depend on the effectiveness of its AI lending platform. Risks include:
*   **Model Effectiveness:** If AI models fail to accurately or timely reflect changes in economic conditions regarding borrower credit risk, or if they are ineffective, growth prospects and financial results could be adversely affected.
*   **System Disruptions:** Significant disruptions or failures in technology systems, including the AI platform, could harm business operations and financial condition.

**5. Operational and Strategic Risks**
*   **Lending Partners:** The business depends on retaining existing lending partners and attracting new ones, as a limited number of partners account for a significant portion of loan originations and revenue.
*   **Loan Aggregators:** The company relies on strategic relationships with loan aggregators to attract applicants; failure to maintain these relationships could adversely affect business.
*   **Product Mix:** A significant portion of historical business has depended on a single loan product. Shifts in product demand or mix, or the failure of new product introductions, could harm the business.
*   **Profitability:** The company has incurred net losses in the past and may not be able to sustain or achieve profitability in the future.
*   **Reputation and Brand:** Failure to maintain, protect, and promote its brand, or issues related to loan servicing and collections, could harm the business.
*   **Security:** Security breaches or improper access to data could harm reputation, result in liability, and adversely affect results of operations.

**6. Regulatory and Compliance Risks**
The business is subject to a wide range of evolving laws and regulations. Failure or perceived failure to comply with these regulations could harm the business, financial condition, and results of operations. Additionally, changes in fiscal, monetary, or regulatory policy priorities across presidential administrations may contribute to economic volatility.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Economic Conditions:** The business is adversely affected by uncontrollable economic factors, including uncertainty, volatility, and negative trends that impact capital supply, borrower demand, and repayment ability. Adverse macroeconomic conditions can reduce loan origination volumes, increase funding costs, and lead to higher delinquencies and defaults.
*   **Loan Funding and Capital Sources:** The company depends on diverse and resilient loan funding from institutional investors. Risks include the inability to maintain these sources, manage risks associated with committed capital and co-investment arrangements, and the potential for decreased capital availability or increased costs.
*   **AI Model Effectiveness:** The business relies on artificial intelligence models to approve borrowers. If these models are ineffective, fail to improve, or do not accurately reflect changes in economic conditions regarding credit risk, growth and financial results could be harmed.
*   **Concentration of Lending Partners:** A limited number of lending partners account for a significant portion of loan originations and revenue. The business depends on retaining existing partners and attracting new ones.
*   **Profitability and Financial Performance:** The company has incurred net losses in the past and may not achieve or sustain profitability. Quarterly results may fluctuate significantly.
*   **Balance Sheet and Loan Risks:** The company faces risks related to managing loans on its balance sheet, including counterparty risk, representations and warranties on transferred loans, and the potential need to repurchase loans if those warranties are inaccurate.
*   **Upstart Macro Index (UMI):** Failure to manage risks associated with the UMI could adversely affect credibility, reputation, and financial results.
*   **Reputation and Brand:** Failure to maintain, protect, and promote the brand may harm the business.
*   **Loan Servicing and Collections:** Inability to manage risks related to servicing and collecting loans could negatively impact the business.
*   **Product Dependence and Innovation:** A significant portion of business historically depends on a single loan product. Additionally, new loan products and service offerings may not be successful or may introduce unmanaged risks.
*   **Security and Technology:** Security breaches, improper data access, or disruptions/failures in technology systems, including the AI lending platform, could harm reputation and operations.
*   **Loan Aggregators:** The business relies on strategic relationships with loan aggregators to attract applicants; failure to maintain these relationships could adversely affect the business.
*   **Regulatory Compliance:** The business is subject to a wide range of evolving laws and regulations. Failure or perceived failure to comply could harm the business.

## Pre-written sections (judge input)

### Financial Health

Upstart Holdings, Inc. (UPST) is currently trading at $22.81 with a market capitalization of approximately $2.22 billion. The company reports annual revenue of $1.29 billion and maintains a net profit margin of roughly 4.7%, reflecting a net income of $60.3 million. While the trailing P/E ratio stands at 45.62, the significantly lower forward P/E of 6.56 suggests market expectations for substantial earnings growth in the near term. This divergence indicates that current valuation multiples are heavily influenced by anticipated future profitability rather than historical performance.

### Recent Developments

Upstart Holdings, Inc. (UPST) is currently trading near its 52-week low of $22.56, reflecting ongoing market caution despite a significantly lower forward P/E ratio of 6.56 compared to its trailing P/E of 45.62. The company recently filed its 10-K annual report on February 10, 2026, and is scheduled to submit its next 10-Q quarterly report on August 4, 2026, both of which highlight substantial risk factors that investors must carefully evaluate. With a modest profit margin of 4.69% and no dividend yield, the stock remains a high-risk, growth-oriented play in the credit services sector. Investors should monitor upcoming regulatory filings and macroeconomic interest rate trends closely, as these factors will likely dictate the stock's ability to recover from its current depressed valuation.

### SEC Filing Highlights

Upstart’s financial performance remains highly sensitive to macroeconomic headwinds, with rising interest rates and potential recessions threatening to increase delinquencies and reduce borrower demand. The company faces significant funding risks due to its reliance on institutional capital, particularly regarding committed capital arrangements and the potential for higher costs if interest rate environments shift unfavorably. Operational resilience is further challenged by the necessity to retain credit risk through securitizations and warehouse facilities, which exposes the firm to liquidity strains if retained interests decline in value. Additionally, Upstart’s growth is contingent on the continued effectiveness of its AI lending models and its ability to maintain key relationships with a concentrated group of lending partners and loan aggregators.

### Risk Factors

*   **Macroeconomic Sensitivity and Credit Risk:** Adverse economic conditions, including volatility and negative trends, can significantly reduce loan origination volumes, increase funding costs, and lead to higher delinquencies and defaults, directly impacting financial performance.
*   **Reliance on AI Models and Capital Sources:** The business is heavily dependent on the continued effectiveness of its AI lending models to accurately assess credit risk, as well as its ability to secure diverse and resilient funding from institutional investors; failures in either area could severely harm growth and profitability.
*   **Concentration and Regulatory Risks:** A significant portion of revenue depends on a limited number of lending partners and loan aggregators, while the company faces substantial risks from evolving regulatory compliance requirements and potential reputational damage from technology or data security breaches.

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings, Inc. leverages artificial intelligence to facilitate consumer lending, currently generating $1.29 billion in annual revenue with a net income of $60.3 million. The stock is notable for its significant valuation divergence, trading near a 52-week low with a forward P/E of 6.56 that contrasts sharply with a trailing P/E of 45.62, signaling market expectations for substantial near-term earnings growth. The single most important near-term variable shaping this outcome is the trajectory of macroeconomic interest rates and the resulting stability of borrower demand.

### Outlook
The directional outlook for Upstart is cautiously constructive, predicated on the assumption that the market’s forward-looking earnings expectations will materialize as macroeconomic conditions stabilize. Key variables to monitor include the stability of institutional funding costs, the continued efficacy of AI-driven credit underwriting in mitigating delinquencies, and the regulatory landscape surrounding algorithmic lending. A strengthening thesis would be supported by sustained borrower demand and successful diversification of capital sources, whereas a weakening view would result from prolonged high-interest rate environments, increased credit losses, or adverse regulatory shifts that constrain lending partner relationships.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "currently generating $1.29 billion in annual revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $1,285,890,048, which rounds to $1.29 billion; the pre-written Financial Health section also states "$1.29 billion," confirming the figure.

---

CLAIM: "net income of $60.3 million"
LABEL: SUPPORTED
REASON: Source data shows net_income of $60,334,000, which rounds to $60.3 million; the pre-written Financial Health section also states "$60.3 million."

---

CLAIM: "trading near a 52-week low"
LABEL: SUPPORTED
REASON: Current price is $22.81 and the 52-week low is $22.555; $22.81 is only $0.255 above the low, confirming the stock is trading near its 52-week low arithmetically.

---

CLAIM: "forward P/E of 6.56"
LABEL: SUPPORTED
REASON: Source data shows forward_pe of 6.562216, which rounds to 6.56; confirmed in pre-written sections as well.

---

CLAIM: "trailing P/E of 45.62"
LABEL: SUPPORTED
REASON: Source data explicitly lists pe_ratio as 45.62.

---

CLAIM: "signaling market expectations for substantial near-term earnings growth"
LABEL: INFERENCE
REASON: This is a directional interpretation derived directly from the observable contrast between the trailing P/E of 45.62 and the forward P/E of 6.56 present in the source data, and is also stated explicitly in the pre-written Financial Health section.

---

**OUTLOOK**

The Outlook section contains no specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers. All statements are qualitative and directional (e.g., "cautiously constructive," "sustained borrower demand," "prolonged high-interest rate environments"). There are no numerical claims to audit in this section.

---

**SUMMARY TABLE**

| Claim | Label |
|---|---|
| $1.29 billion in annual revenue | SUPPORTED |
| Net income of $60.3 million | SUPPORTED |
| Trading near a 52-week low | SUPPORTED |
| Forward P/E of 6.56 | SUPPORTED |
| Trailing P/E of 45.62 | SUPPORTED |
| Substantial near-term earnings growth (implied by P/E divergence) | INFERENCE |

No claims in the audited sections are UNSUPPORTED. All quantitative figures are either directly present in the source data or arithmetically verifiable from it.
