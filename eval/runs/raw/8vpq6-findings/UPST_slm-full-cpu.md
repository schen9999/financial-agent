# UPST — slm-full-cpu

## Metadata

ticker: UPST
arm: slm-full-cpu
judge_prompt_version: v2
context_sha256: bff59c688136986d5a6e022750b96ed026ecc15df27b603dcf298a24743151d3
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 721, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 221.211, "latency_s_total": 221.211, "parse_failure": 0, "prompt_tokens": 3011, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 598, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 188.319, "latency_s_total": 188.319, "parse_failure": 0, "prompt_tokens": 2333, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 122, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 59.72, "latency_s_total": 59.72, "parse_failure": 0, "prompt_tokens": 661, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 150, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 77.227, "latency_s_total": 77.227, "parse_failure": 0, "prompt_tokens": 655, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 156, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 79.71, "latency_s_total": 79.71, "parse_failure": 0, "prompt_tokens": 671, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 109, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 75.642, "latency_s_total": 75.642, "parse_failure": 0, "prompt_tokens": 802, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 815, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 96.492, "latency_s_total": 96.492, "parse_failure": 0, "prompt_tokens": 1454, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "UPST",
  "company_name": "Upstart Holdings, Inc.",
  "current_price": 22.81,
  "currency": "USD",
  "market_cap": 2219710464.0,
  "pe_ratio": 43.865387,
  "forward_pe": 6.562216,
  "week_52_high": 55.22,
  "week_52_low": 22.555,
  "revenue": 1285890048.0,
  "net_income": 60334000.0,
  "profit_margin": 0.046919998,
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
[From Pinecone cache] Based on the provided risk factors from the SEC EDGAR filings for Upstart (ticker: UPST), the key takeaways regarding the company's business risks and operational challenges include:

**Economic and Market Sensitivity**
*   **Macroeconomic Impact:** The business is heavily influenced by uncontrollable economic conditions, including inflation, interest rates, unemployment, and recessionary trends. Adverse macroeconomic conditions can reduce borrower demand, approval rates, and loan origination volumes while increasing funding costs and reliance on the company’s balance sheet.
*   **Borrower Vulnerability:** Many borrowers have poor, limited, or no credit history, making them disproportionately susceptible to economic downturns, which can lead to higher delinquencies, defaults, and charge-offs.

**Funding and Capital Risks**
*   **Dependence on Institutional Investors:** The company relies on diverse and resilient sources of capital from institutional investors. A sustained decline in investor demand or the unavailability of capital on commercially reasonable terms could adversely affect financial results.
*   **Committed Capital and Co-Investment:** A significant portion of funding comes from committed capital arrangements that may include downside credit risk protection. If loan performance deviates from expectations or if committed sale volumes are not met, the company may be required to compensate investors, potentially leading to unfavorable fair value adjustments.
*   **Securitization and Financing:** The company facilitates securitizations and uses warehouse credit facilities. Risks include the potential decline in value of retained interests, inability to refinance on acceptable terms, and regulatory constraints (such as the Dodd-Frank Act and Volcker Rule) that may limit securitization structures. Failure to meet representations and warranties on transferred loans could trigger repurchase obligations that strain liquidity.

**Operational and Technology Risks**
*   **AI Model Effectiveness:** The company’s growth depends on the continuous improvement of its artificial intelligence models. If these models fail to accurately reflect changes in economic conditions or borrower credit risk, or if they are ineffective, business prospects could be harmed.
*   **Technology Disruption:** Any significant disruption or failure in technology systems, including the AI lending platform, could negatively impact business operations and financial condition.
*   **Loan Aggregators:** The business relies on strategic relationships with loan aggregators to attract applicants. Inability to maintain these relationships or replace their services could adversely affect the business.

**Financial Performance and Product Mix**
*   **Profitability and Volatility:** The company has incurred net losses in the past and may not achieve profitability in the future. Quarterly results are subject to significant fluctuation, which can impact stock price.
*   **Product Concentration:** A significant portion of the business has historically depended on a single loan product. Shifts in product demand or mix, or the failure of new product introductions, could harm business prospects.
*   **Lending Partner Concentration:** A limited number of lending partners account for a significant portion of loan originations and revenue. The business depends on retaining these partners and attracting new ones.

**Regulatory and Reputational Risks**
*   **Compliance:** The business is subject to a wide range of evolving laws and regulations. Failure to comply, or the perceived failure to do so, could harm the business.
*   **Brand and Security:** Maintaining reputation and brand is critical. Security breaches, improper data access, or failures in loan servicing and collections could harm reputation, result in liability, and adversely affect results of operations.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Economic Conditions:** The business is adversely affected by uncontrollable economic factors, including uncertainty, volatility, and negative trends that impact capital supply, borrower demand, and repayment ability. Adverse macroeconomic conditions can reduce loan origination volumes, increase funding costs, and lead to higher delinquencies and defaults, particularly among borrowers with poor or limited credit history.
*   **Loan Funding and Capital Sources:** The company depends on diverse and resilient loan funding from institutional investors, lending partners, and securitization programs. Inability to maintain these sources, manage risks associated with committed capital and co-investment arrangements, or secure economical financing could decrease capital supply or force reliance on more costly alternatives.
*   **AI Model Effectiveness:** Growth and financial results depend on the ability to improve AI models and ensure they accurately reflect changes in economic conditions and borrower credit risk. Ineffective models could adversely affect approval rates and business prospects.
*   **Borrower Approval and Product Mix:** The business may suffer if it cannot approve a significant number of borrowers or if there are shifts in demand for its primary loan product. While new products are being developed, failure to manage risks associated with them could harm the business.
*   **Lending Partner Concentration:** A limited number of lending partners account for a significant portion of loan originations and revenue, making the retention of existing partners and attraction of new ones critical.
*   **Profitability and Financial Performance:** The company has incurred net losses in the past and may not achieve profitability in the future. Quarterly results may fluctuate significantly, potentially affecting stock price.
*   **Upstart Macro Index (UMI):** Failure to manage risks associated with the UMI could adversely affect credibility, reputation, and financial results.
*   **Reputation and Brand:** Failure to maintain, protect, and promote the brand may harm the business.
*   **Loan Servicing and Collections:** Inability to manage risks related to servicing and collections obligations could negatively impact the business.
*   **Security and Technology:** Security breaches, improper data access, or significant disruptions/failures in technology systems, including the AI lending platform, could harm reputation and operations.
*   **Loan Aggregators:** The business relies on strategic relationships with loan aggregators to attract applicants; failure to maintain these relationships or replace their services could be detrimental.
*   **Legal and Regulatory Compliance:** The business is subject to a wide range of evolving laws and regulations. Failure or perceived failure to comply could harm the business.
*   **Representations and Warranties:** Inaccurate representations and warranties in connection with loan transfers, securitizations, or other arrangements may require loan repurchases or indemnification payments, potentially affecting liquidity and reputation.
*   **Counterparty Risk:** Failure by counterparties in derivative instruments, beneficial interests, or warehouse facilities could result in losses.

## Pre-written sections (judge input)

### Financial Health

Upstart Holdings, Inc. (UPST) currently trades at $22.81 with a market capitalization of approximately $2.22 billion. The company reports annual revenue of $1.29 billion and maintains a net profit margin of 4.69%, reflecting modest profitability. While the trailing P/E ratio stands at 43.87, the significantly lower forward P/E of 6.56 suggests market expectations for improved earnings efficiency in the near term. This divergence indicates that investors anticipate a substantial turnaround or cost optimization in upcoming quarters.

### Recent Developments

Upstart Holdings, Inc. recently filed its Annual Report on Form 10-K on February 10, 2026, and its Quarterly Report on Form 10-Q on August 4, 2026, both of which reiterate the high degree of risk inherent in investing in the company's common stock. These filings highlight that the company's business, financial condition, and prospects could be harmed by risks and uncertainties that are currently unknown or not deemed material. Investors should carefully consider these disclosed risks alongside other financial information before making investment decisions. The absence of specific recent news in the provided data suggests that current market attention is focused on these fundamental regulatory disclosures and the associated risk profile.

### SEC Filing Highlights
Upstart’s financial performance remains highly sensitive to macroeconomic conditions, with rising interest rates and unemployment potentially suppressing borrower demand while increasing funding costs and credit losses. The company faces significant execution risks tied to its AI model effectiveness and reliance on a concentrated base of lending partners and institutional investors for capital. Additionally, regulatory scrutiny and potential compliance failures pose ongoing threats to its operational stability and reputation. Consequently, quarterly results are subject to substantial volatility, reflecting the inherent challenges in balancing growth with profitability in a fluctuating credit environment.

### Risk Factors

*   **Macroeconomic Sensitivity and Credit Risk:** Adverse economic conditions, volatility, and negative trends can significantly reduce loan origination volumes, increase funding costs, and lead to higher delinquencies and defaults, particularly among borrowers with limited credit history.
*   **AI Model Dependency and Effectiveness:** The company’s growth and financial results rely heavily on the continuous improvement of its AI models to accurately reflect changing economic conditions and borrower credit risk; ineffective models could negatively impact approval rates and business prospects.
*   **Capital Funding and Partner Concentration:** The business depends on diverse and resilient loan funding from institutional investors and lending partners; an inability to secure economical financing or maintain key partnerships could decrease capital supply and force reliance on more costly alternatives.

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings, Inc. operates as an AI-driven lending platform that connects borrowers with lending partners, currently reporting annual revenue of $1.29 billion and maintaining a modest net profit margin of 4.69%. The stock is notable now due to the significant divergence between its trailing P/E of 43.87 and a forward P/E of 6.56, signaling strong market anticipation for near-term earnings efficiency and cost optimization. The single most important near-term variable shaping the outcome is the company's ability to execute this turnaround while navigating the heightened regulatory and macroeconomic risks disclosed in its recent filings.

### Outlook
The directional outlook for Upstart is cautiously constructive, driven by the market’s expectation of improved earnings efficiency as reflected in the low forward valuation multiple. However, this thesis remains highly contingent on the company’s ability to maintain AI model effectiveness and secure stable, economical funding from its partner network amidst a sensitive macroeconomic environment. Investors should closely monitor trends in loan origination volumes, the stability of the lending partner base, and any evolving regulatory scrutiny, as adverse shifts in these variables would significantly weaken the investment case by exacerbating credit losses or restricting capital access.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "annual revenue of $1.29 billion"
LABEL: SUPPORTED
REASON: Source data shows revenue of $1,285,890,048, which rounds to $1.29 billion; the pre-written Financial Health section also states "$1.29 billion."

---

CLAIM: "net profit margin of 4.69%"
LABEL: SUPPORTED
REASON: Source data shows profit_margin of 0.046919998, which equals approximately 4.69%; the pre-written Financial Health section also states "4.69%."

---

CLAIM: "trailing P/E of 43.87"
LABEL: SUPPORTED
REASON: Source data shows pe_ratio of 43.865387, which rounds to 43.87; the pre-written Financial Health section also states "43.87."

---

CLAIM: "forward P/E of 6.56"
LABEL: SUPPORTED
REASON: Source data shows forward_pe of 6.562216, which rounds to 6.56; the pre-written Financial Health section also states "6.56."

---

**OUTLOOK**

The Outlook section contains no specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers. All statements are qualitative and directional (e.g., "cautiously constructive," "low forward valuation multiple," "stable, economical funding"). There are therefore no additional quantitative or forward-looking claims to audit in this section.
