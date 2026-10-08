# UPST — slm-full-cpu

## Metadata

ticker: UPST
arm: slm-full-cpu
judge_prompt_version: v2
context_sha256: b990b21487d7a4854986ebb6b4e19773c7d6cfdcaf35f460cd10d208ea703ac2
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 777, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 225.71, "latency_s_total": 225.71, "parse_failure": 0, "prompt_tokens": 3011, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 529, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 176.411, "latency_s_total": 176.411, "parse_failure": 0, "prompt_tokens": 2333, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 137, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 79.958, "latency_s_total": 79.958, "parse_failure": 0, "prompt_tokens": 672, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 140, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 62.646, "latency_s_total": 62.646, "parse_failure": 0, "prompt_tokens": 666, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 131, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 81.055, "latency_s_total": 81.055, "parse_failure": 0, "prompt_tokens": 602, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 132, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 87.373, "latency_s_total": 87.373, "parse_failure": 0, "prompt_tokens": 858, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 880, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 101.781, "latency_s_total": 101.781, "parse_failure": 0, "prompt_tokens": 1460, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
[]

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
The company’s business is heavily influenced by uncontrollable macroeconomic factors. Uncertainty, volatility, and negative economic trends can reduce borrower demand, approval rates, and loan origination volumes. Because many borrowers have poor or limited credit histories, they are disproportionately affected by inflation, unemployment, and recessionary conditions. Adverse economic developments can lead to higher delinquencies, defaults, and charge-offs, while also increasing funding costs and reducing liquidity in capital markets.

**2. Dependence on Institutional Capital and Funding Risks**
Upstart relies on diverse and resilient sources of capital from institutional investors, including through whole loans, pass-through certificates, and asset-backed securities. Key risks include:
*   **Committed Capital and Co-Investment:** A significant portion of funding comes from arrangements that may require the company to compensate investors if loan credit performance deviates from expectations or if committed sale volumes are not met.
*   **Cost of Capital:** Capital arrangements made during high-interest-rate periods may become more costly if rates decline.
*   **Capital Constraints:** If institutional investors reduce funding or if the company cannot secure new arrangements on reasonable terms, it may be forced to rely more heavily on its balance sheet, incur higher funding costs, or accept less favorable terms.

**3. Securitization and Financing Exposures**
The company facilitates securitizations and uses warehouse credit facilities to finance loans. Risks associated with these activities include:
*   **Risk Retention:** As a sole sponsor, Upstart must retain a portion of the credit risk under Regulation RR. If these retained interests decline in value or cannot be refinanced on acceptable terms, liquidity and results of operations could suffer.
*   **Representations and Warranties:** If representations regarding transferred loans are inaccurate, the company may be required to repurchase loans or make indemnification payments. High volumes of such repurchases could harm the company’s reputation and liquidity.
*   **Regulatory Compliance:** Changes in laws, such as the Dodd-Frank Act, the Investment Company Act of 1940, and the "Volcker Rule," may limit the structure of securitizations or restrict access to capital markets.

**4. Technology and AI Model Effectiveness**
The company’s growth prospects are tied to the effectiveness of its artificial intelligence (AI) models. If these models fail to accurately or timely reflect changes in economic conditions regarding borrower credit risk, or if there are significant disruptions or failures in the AI lending platform, the business could be adversely affected.

**5. Operational and Strategic Risks**
*   **Lending Partners:** The business depends on retaining existing lending partners and attracting new ones, as a limited number of partners account for a significant portion of originations and revenue.
*   **Loan Aggregators:** The company relies on strategic relationships with loan aggregators to attract applicants; failure to maintain these relationships could harm the business.
*   **Product Mix:** A significant portion of historical business has depended on a single loan product, making the company vulnerable to shifts in product demand.
*   **Profitability:** The company has incurred net losses in the past and may not achieve or sustain profitability in the future.
*   **Reputation and Brand:** Failure to maintain, protect, and promote the brand, or issues related to data security and improper access to borrower data, could harm the business.
*   **Regulatory Compliance:** The business is subject to a wide range of evolving laws and regulations. Failure or perceived failure to comply could harm financial condition and operations.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Economic Conditions:** The business is adversely affected by uncontrollable economic factors, including uncertainty, volatility, and negative trends that impact capital supply, borrower demand, and repayment ability. Adverse macroeconomic conditions can reduce loan origination volumes, increase funding costs, and lead to higher delinquencies and defaults.
*   **Loan Funding and Capital Sources:** The company depends on diverse and resilient loan funding from institutional investors, lending partners, and securitization programs. Inability to maintain these sources, manage risks associated with committed capital, or secure economical financing could decrease capital supply or force reliance on more costly alternatives.
*   **AI Model Effectiveness:** Growth and financial results depend on the ability to improve AI models and ensure they accurately reflect changes in economic conditions and borrower credit risk. Ineffective models could adversely affect business prospects.
*   **Borrower Approval and Demand:** The business relies on approving a significant number of borrowers. Failure to do so, or shifts in product demand, could negatively impact growth and operations.
*   **Concentration of Lending Partners:** A limited number of lending partners account for a significant portion of loan originations and revenue. Dependence on retaining these partners and attracting new ones poses a risk.
*   **Profitability and Financial Performance:** The company has incurred net losses in the past and may not achieve profitability in the future. Quarterly results may fluctuate significantly.
*   **Balance Sheet and Credit Risks:** Risks associated with loans held on the balance sheet, the Upstart Macro Index (UMI), and loan servicing and collections obligations could harm the business.
*   **Reputation and Brand:** Failure to maintain, protect, and promote the brand may harm the business. Additionally, high volumes of loan repurchases due to inaccurate representations and warranties could harm reputation.
*   **Technology and Security:** Security breaches, improper data access, or disruptions/failures in technology systems, including the AI lending platform, could adversely affect results and expose the company to liability.
*   **Strategic Relationships:** The business relies on strategic relationships with loan aggregators to attract applicants. Inability to maintain or replace these services could harm the business.
*   **Regulatory Compliance:** The business is subject to a wide range of evolving laws and regulations. Failure or perceived failure to comply could harm the business.
*   **Counterparty Risk:** Risks arising from derivative instruments, beneficial interests, warehouse facilities, and custodial arrangements, where a counterparty’s failure to perform could result in losses.

## Pre-written sections (judge input)

### Financial Health

Upstart Holdings, Inc. (UPST) is currently trading at $24.35 with a market capitalization of approximately $2.37 billion. The company reports annual revenue of $1.29 billion and maintains a healthy net profit margin of 4.69%, reflecting a net income of $60.3 million. While the trailing P/E ratio stands at 45.94, the significantly lower forward P/E of 7.01 suggests market expectations for improved earnings efficiency in the near term. This divergence indicates that current valuation multiples may be driven by recent profitability normalization rather than long-term growth premiums.

### Recent Developments

Upstart Holdings, Inc. recently filed its Annual Report on Form 10-K on February 10, 2026, and its Quarterly Report on Form 10-Q on August 4, 2026, both of which reiterate the high degree of risk inherent in investing in the company's common stock. These filings highlight that the business, financial condition, and prospects could be harmed by risks and uncertainties not currently known to management or deemed immaterial at the time of filing. For investors, this underscores the speculative nature of the stock and the importance of carefully considering these disclosed risk factors alongside other financial metrics before making investment decisions.

### SEC Filing Highlights
Upstart’s financial performance remains highly sensitive to macroeconomic volatility, with adverse trends potentially triggering higher delinquencies, increased funding costs, and reduced loan origination volumes. The company faces significant capital risks due to its reliance on institutional investors, particularly regarding committed capital arrangements and the potential for higher costs if interest rate environments shift unfavorably. Operational resilience is further challenged by regulatory exposures in securitizations, including risk retention requirements and potential repurchase obligations for inaccurate loan representations. Additionally, sustained growth depends on the continued effectiveness of its AI credit models and the stability of key lending partner relationships, amid ongoing challenges in achieving consistent profitability.

### Risk Factors

*   **Macroeconomic Sensitivity:** Adverse economic conditions, including volatility and negative trends, can significantly reduce loan origination volumes, increase funding costs, and lead to higher delinquencies and defaults.
*   **AI Model and Technology Reliance:** The company’s financial performance is heavily dependent on the continuous effectiveness of its AI models to accurately assess credit risk; model failures or technology disruptions could severely impact business prospects.
*   **Capital and Counterparty Dependence:** Growth is constrained by the ability to secure diverse, economical funding sources and maintain strategic relationships with a limited number of key lending partners and aggregators.

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings, Inc. operates as an AI-driven lending platform that connects borrowers with institutional capital, currently reporting annual revenue of $1.29 billion and a net profit margin of 4.69%. The stock is notable for its significant valuation divergence, evidenced by a trailing P/E of 45.94 versus a forward P/E of 7.01, which signals market expectations for near-term earnings efficiency despite the speculative risks highlighted in recent 10-K and 10-Q filings. The single most important near-term variable shaping the investment outcome is the stability of the macroeconomic environment and interest rate trajectory, which directly dictates loan origination volumes and funding costs.

### Outlook
The directional outlook for Upstart is cautiously constructive, contingent upon the company’s ability to navigate a complex macroeconomic landscape while maintaining the efficacy of its proprietary AI credit models. Key variables to monitor include the stability of institutional funding costs, the health of consumer credit metrics such as delinquency rates, and the regulatory environment surrounding AI-driven lending and securitizations. A strengthening thesis would be supported by evidence of resilient loan origination volumes despite interest rate fluctuations and successful adaptation to regulatory changes, whereas a weakening view would emerge from sustained macroeconomic downturns, increased funding spreads, or any degradation in the predictive accuracy of the core technology. Investors should remain attentive to the gap between current profitability normalization and long-term growth sustainability, as the stock’s speculative nature requires careful consideration of the disclosed risk factors.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, and forward-looking number in the **Executive Summary** and **Outlook** sections.

---

## EXECUTIVE SUMMARY

---

CLAIM: "annual revenue of $1.29 billion"
LABEL: SUPPORTED
REASON: Source data shows revenue of $1,285,890,048, which rounds to $1.29 billion; the pre-written Financial Health section also states "$1.29 billion."

---

CLAIM: "net profit margin of 4.69%"
LABEL: SUPPORTED
REASON: Source data explicitly lists `profit_margin_pct: 4.69`, and the pre-written Financial Health section confirms "4.69%."

---

CLAIM: "trailing P/E of 45.94"
LABEL: SUPPORTED
REASON: Source data lists `pe_ratio: 45.943398`, which rounds to 45.94; the pre-written Financial Health section also states "45.94."

---

CLAIM: "forward P/E of 7.01"
LABEL: SUPPORTED
REASON: Source data lists `forward_pe: 7.005259`, which rounds to 7.01; the pre-written Financial Health section also states "7.01."

---

CLAIM: "recent 10-K and 10-Q filings"
LABEL: SUPPORTED
REASON: SEC filing data confirms a 10-K filed 2026-02-10 and a 10-Q filed 2026-08-04, both explicitly referenced in the pre-written Recent Developments section.

---

## OUTLOOK

No explicit quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section. All claims in the Outlook are qualitative or directional in nature (e.g., "cautiously constructive," "key variables to monitor," "strengthening thesis," "weakening view"). There are no numerical claims to audit.

---

## SUMMARY TABLE

| Claim | Label |
|---|---|
| Annual revenue of $1.29 billion | SUPPORTED |
| Net profit margin of 4.69% | SUPPORTED |
| Trailing P/E of 45.94 | SUPPORTED |
| Forward P/E of 7.01 | SUPPORTED |
| Recent 10-K and 10-Q filings | SUPPORTED |

**No unsupported or inference-labeled claims were identified.** All quantitative figures in the Executive Summary are directly traceable to the raw source data, and the Outlook section contains no quantitative or forward-looking numerical claims requiring verification.
