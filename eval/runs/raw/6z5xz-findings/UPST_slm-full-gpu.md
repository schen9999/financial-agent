# UPST — slm-full-gpu

## Metadata

ticker: UPST
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 593c1a40ee5d3c169051e5bfb2c5f46757d92c3d4e05a6190b7a83b17569e00c
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 908, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 30.096, "latency_s_total": 30.096, "parse_failure": 0, "prompt_tokens": 3011, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 631, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 22.541, "latency_s_total": 22.541, "parse_failure": 0, "prompt_tokens": 2333, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 122, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.726, "latency_s_total": 5.726, "parse_failure": 0, "prompt_tokens": 688, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 179, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 11.073, "latency_s_total": 11.073, "parse_failure": 0, "prompt_tokens": 682, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 175, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 13.203, "latency_s_total": 13.203, "parse_failure": 0, "prompt_tokens": 704, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 103, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 8.079, "latency_s_total": 8.079, "parse_failure": 0, "prompt_tokens": 989, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 869, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 28.905, "latency_s_total": 28.905, "parse_failure": 0, "prompt_tokens": 1538, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "UPST",
  "company_name": "Upstart Holdings, Inc.",
  "current_price": 24.02,
  "currency": "USD",
  "market_cap": 2337459456.0,
  "pe_ratio": 48.04,
  "forward_pe": 6.910321,
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
The company’s business is heavily influenced by uncontrollable macroeconomic factors. Adverse economic conditions, such as inflation, higher interest rates, unemployment, or recession, can reduce borrower demand, lower approval and acceptance rates, and increase delinquencies and defaults. Because the company’s operations are concentrated in U.S. consumer credit, it is disproportionately affected by downturns in the U.S. economy or consumer credit markets.

**2. Dependence on Institutional Capital and Funding Risks**
Upstart relies on diverse and resilient sources of capital from institutional investors, including through whole loans, pass-through certificates, and asset-backed securities. Key risks include:
*   **Committed Capital and Co-Investment:** A significant portion of funding comes from arrangements that may require the company to compensate investors if loan credit performance deviates from expectations or if committed loan sale volumes are not achieved.
*   **Cost of Capital:** Capital arrangements made during high-interest-rate periods may become more costly if rates decline while terms remain fixed.
*   **Liquidity Constraints:** If institutional capital becomes less available or more expensive, the company may need to rely more heavily on its balance sheet, incurring higher funding costs or accepting less favorable terms.

**3. Securitization and Financing Complexities**
The company facilitates securitizations and uses warehouse credit facilities to finance loans. Risks in this area include:
*   **Risk Retention:** As a sole sponsor, the company must retain a portion of credit risk under Regulation RR. If these retained interests decline in value or cannot be refinanced on acceptable terms, liquidity and results of operations could suffer.
*   **Regulatory Compliance:** Securitizations are subject to regulations like the Dodd-Frank Act, the Investment Company Act of 1940, and the "Volcker Rule." Failure to comply could restrict access to securitization markets.
*   **Repurchase Obligations:** If representations and warranties regarding transferred loans are inaccurate, the company may be forced to repurchase loans or make indemnification payments, which could strain liquidity and harm its reputation.

**4. Technology and Artificial Intelligence (AI) Reliance**
The company’s growth and operational success depend on the effectiveness of its AI lending platform. Risks include:
*   **Model Effectiveness:** If AI models fail to accurately or timely reflect changes in economic conditions regarding borrower credit risk, or if they fail to approve a significant number of borrowers, growth prospects could be adversely affected.
*   **System Disruptions:** Any significant disruption or failure in technology systems, including the AI platform, could harm business operations and financial results.
*   **Data Security:** Security breaches or improper access to borrower data could damage reputation, result in liability, and adversely affect operations.

**5. Regulatory and Compliance Exposure**
The business is subject to a wide range of evolving laws and regulations. Failure to comply, or even the perceived failure to comply, with these laws could harm the business. This includes state licensing requirements and federal regulations affecting lending, securitization, and data privacy.

**6. Operational and Strategic Risks**
*   **Lending Partners:** The business depends on retaining existing lending partners and attracting new ones, as a limited number of partners account for a significant portion of loan originations and revenue.
*   **Loan Aggregators:** The company relies on strategic relationships with loan aggregators to attract applicants; losing these relationships could negatively impact business.
*   **Product Concentration:** A significant portion of historical business has depended on a single loan product, making the company vulnerable to shifts in product demand.
*   **Profitability:** The company has incurred net losses in the past and faces uncertainty regarding its ability to sustain or achieve profitability in the future.
*   **Brand Reputation:** Failure to maintain, protect, and promote its brand may harm the business.

**7. Financial Volatility**
Quarterly results may fluctuate significantly due to the factors mentioned above, which could adversely affect the trading price of the common stock. Additionally, the company manages the Upstart Macro Index (UMI), and failure to manage risks associated with it could harm credibility and reputation.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Economic Conditions:** The business is adversely affected by uncontrollable economic factors, including uncertainty, volatility, and negative trends that impact capital supply, borrower demand, and repayment ability. Adverse macroeconomic conditions can reduce loan origination volumes, increase funding costs, and lead to higher delinquencies and defaults.
*   **Loan Funding and Capital Sources:** The company depends on diverse and resilient loan funding from institutional investors. Risks include the inability to maintain these sources, manage risks associated with committed capital and co-investment arrangements, and the potential for decreased capital availability or increased costs.
*   **Financing Arrangements:** Loan funding through lending partners, securitization programs, and warehouse credit facilities exposes the company to risks. Failure to manage these could decrease capital supply or force the company to seek more costly capital. Additionally, inaccurate representations and warranties on transferred loans may require repurchases or indemnification payments.
*   **AI Model Effectiveness:** The business relies on artificial intelligence models to approve borrowers. If these models are ineffective, fail to improve, or do not accurately reflect changes in economic conditions on credit risk, growth and financial results could be adversely affected.
*   **Borrower Approval Rates:** An inability to approve a significant number of borrowers for loans through the marketplace would negatively impact growth and financial condition.
*   **Lending Partner Concentration:** A limited number of lending partners account for a significant portion of loan originations and revenue. Dependence on retaining these partners and attracting new ones poses a risk.
*   **Profitability:** The company has incurred net losses in the past and may not achieve or sustain profitability in the future.
*   **Balance Sheet Risks:** Inability to manage risks associated with loans held on the balance sheet could harm business and financial results.
*   **Quarterly Result Fluctuations:** Significant fluctuations in quarterly results could adversely affect the business and stock trading price.
*   **Upstart Macro Index (UMI):** Failure to manage risks associated with the UMI could adversely affect credibility, reputation, and financial condition.
*   **Reputation and Brand:** Failure to maintain, protect, and promote the brand may harm the business.
*   **Loan Servicing and Collections:** Inability to manage risks related to servicing and collection obligations could negatively impact the business.
*   **Product Dependence and Innovation:** A significant portion of business has historically depended on a single loan product. Shifts in demand or the failure of new product introductions could adversely affect the business.
*   **Security and Technology:** Security breaches, improper data access, or significant disruptions/failures in technology systems, including the AI lending platform, could harm reputation and operations.
*   **Loan Aggregators:** Reliance on strategic relationships with loan aggregators to attract applicants creates risk if these relationships cannot be maintained or replaced.
*   **Regulatory Compliance:** The business is subject to a wide range of evolving laws and regulations. Failure or perceived failure to comply could harm the business.

## Pre-written sections (judge input)

### Financial Health

Upstart Holdings, Inc. (UPST) is currently trading at $24.02 with a market capitalization of approximately $2.34 billion. The company reports annual revenue of $1.29 billion and maintains a healthy net profit margin of 4.69%. While the trailing P/E ratio stands at 48.04, the significantly lower forward P/E of 6.91 suggests strong expected earnings growth in the near term. This valuation discrepancy indicates that the market anticipates a substantial improvement in profitability relative to current price levels.

### Recent Developments

Upstart Holdings, Inc. (UPST) is currently trading at $24.02, reflecting a significant recovery from its 52-week low of $22.56 but remaining well below its recent high of $55.22. The company reported a net income of $60.3 million, translating to a profit margin of 4.69% on revenues of $1.29 billion. Notably, the forward P/E ratio stands at a compelling 6.91, suggesting market expectations for substantial earnings growth despite the current trailing P/E of 48.04. Investors should monitor upcoming filings, including the 10-K due in February 2026 and the 10-Q in August 2026, for further insights into risk management and operational stability.

### SEC Filing Highlights
Upstart’s operations remain highly sensitive to macroeconomic headwinds, with rising interest rates and potential recessions threatening to reduce borrower demand and increase credit losses. The company faces significant funding risks due to its reliance on institutional capital, where deviations in loan performance or shifting interest rate environments could elevate costs or constrain liquidity. Additionally, Upstart’s growth is contingent on the continued effectiveness of its AI lending models and its ability to navigate complex regulatory requirements surrounding securitizations and data privacy.

### Risk Factors

*   **Macroeconomic Sensitivity and Credit Risk:** Adverse economic conditions, including volatility and negative trends, can significantly reduce loan origination volumes, increase funding costs, and lead to higher delinquencies and defaults, directly impacting financial results.
*   **Reliance on AI Models and Borrower Approval:** The business is heavily dependent on the effectiveness of its AI models to accurately assess credit risk; if these models fail to improve or adapt to changing economic conditions, or if borrower approval rates decline, growth and profitability will be adversely affected.
*   **Funding Dependency and Partner Concentration:** The company relies on diverse but potentially unstable capital sources, including institutional investors and a limited number of lending partners; any disruption in these funding arrangements or the loss of key partners could force the company to seek more costly capital or reduce loan supply.

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings, Inc. leverages artificial intelligence to facilitate consumer lending, currently generating $1.29 billion in annual revenue with a net profit margin of 4.69%. The stock is notable for its significant valuation compression, trading near its 52-week low of $22.56 despite a forward P/E ratio of 6.91 that implies substantial expected earnings growth. The single most important near-term variable shaping the investment outcome is the stability of the macroeconomic environment, specifically regarding interest rates and recession risks that directly impact borrower demand and credit losses.

### Outlook
The directional outlook for Upstart is cautiously constructive, driven by the market’s expectation of robust earnings growth as evidenced by the low forward P/E, yet tempered by the company’s acute sensitivity to macroeconomic volatility. Investors should closely monitor the trend in loan origination volumes and the stability of institutional funding costs, as these are the primary levers for profitability. A strengthening economic environment with stable interest rates would likely validate the current valuation gap and support a re-rating toward the recent high of $55.22, whereas signs of rising delinquencies or funding constraints would weaken the thesis and keep the stock anchored near its 52-week low.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$1.29 billion in annual revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $1,285,890,048, which rounds to $1.29 billion; the pre-written sections also state "$1.29 billion."

---

CLAIM: "net profit margin of 4.69%"
LABEL: SUPPORTED
REASON: Source data explicitly lists profit_margin_pct as 4.69%, confirmed in both the pre-written sections and raw data.

---

CLAIM: "trading near its 52-week low of $22.56"
LABEL: SUPPORTED
REASON: Source data lists week_52_low as $22.555, which rounds to $22.56 (as also stated in the pre-written Recent Developments section); the current price of $24.02 is indeed near that low.

---

CLAIM: "forward P/E ratio of 6.91"
LABEL: SUPPORTED
REASON: Source data lists forward_pe as 6.910321, which rounds to 6.91; confirmed in pre-written sections.

---

CLAIM: "implies substantial expected earnings growth"
LABEL: INFERENCE
REASON: The forward P/E of 6.91 versus the trailing P/E of 48.04 (both present in source data) directly implies a large expected increase in earnings; this is a standard directional interpretation of the ratio gap.

---

**OUTLOOK**

---

CLAIM: "low forward P/E"
LABEL: SUPPORTED
REASON: Forward P/E of 6.91 is explicitly present in the source data and is objectively low relative to the trailing P/E of 48.04.

---

CLAIM: "re-rating toward the recent high of $55.22"
LABEL: SUPPORTED
REASON: Source data explicitly lists week_52_high as $55.22, and the pre-written Recent Developments section references this same figure.

---

CLAIM: "keep the stock anchored near its 52-week low"
LABEL: SUPPORTED
REASON: The 52-week low of $22.555 is present in the source data; the directional claim that downside risks would keep the stock near that level is a positional inference from the two present figures (current price $24.02 vs. low $22.555), which arithmetically confirms the stock is already near its 52-week low ($24.02 is approximately 6.5% above $22.555).

---

**SUMMARY OF FINDINGS**

No claims in the Executive Summary or Outlook sections are UNSUPPORTED. All specific quantitative figures ($1.29B revenue, 4.69% margin, $22.56 52-week low, 6.91 forward P/E, $55.22 52-week high) are directly traceable to the raw source data. The two forward-looking directional statements are appropriately labeled as INFERENCE, being fully derivable from figures present in the source data without requiring any external facts.
