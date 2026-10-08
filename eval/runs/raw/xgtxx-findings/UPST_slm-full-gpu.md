# UPST — slm-full-gpu

## Metadata

ticker: UPST
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: f10dad83b78e3731b8da93afb68531b2ee4c87f659b231691972f0be56f6bed3
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 798, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 22.956, "latency_s_total": 22.956, "parse_failure": 0, "prompt_tokens": 3011, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 605, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 15.698, "latency_s_total": 15.698, "parse_failure": 0, "prompt_tokens": 2333, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 132, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 14.864, "latency_s_total": 14.864, "parse_failure": 0, "prompt_tokens": 688, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 188, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 21.201, "latency_s_total": 21.201, "parse_failure": 0, "prompt_tokens": 682, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 166, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 24.977, "latency_s_total": 24.977, "parse_failure": 0, "prompt_tokens": 678, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 105, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.365, "latency_s_total": 19.365, "parse_failure": 0, "prompt_tokens": 879, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 892, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 31.155, "latency_s_total": 31.155, "parse_failure": 0, "prompt_tokens": 1562, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
[From Pinecone cache] Based on the provided risk factors from the SEC EDGAR filings for Upstart (ticker: UPST), the key takeaways regarding the company's business, financial condition, and operational risks are as follows:

**1. Vulnerability to Economic Conditions**
The company’s business is heavily influenced by uncontrollable macroeconomic factors. Adverse economic conditions, such as inflation, higher interest rates, unemployment, or recession, can significantly reduce borrower demand, approval rates, and loan origination volumes. Because many borrowers on the platform have limited or poor credit histories, they are disproportionately affected by these conditions, leading to potential increases in delinquencies, defaults, and charge-offs.

**2. Dependence on Institutional Capital and Funding Risks**
Upstart relies on diverse and resilient sources of capital from institutional investors, including through whole loans, pass-through certificates, and asset-backed securities. Key risks include:
*   **Committed Capital and Co-Investment:** A significant portion of funding comes from arrangements that may require the company to compensate investors if loan credit performance deviates from expectations or if committed sale volumes are not met.
*   **Cost of Capital:** Capital arrangements made during high-interest-rate periods may become more costly if rates decline while terms remain fixed.
*   **Liquidity Constraints:** If institutional investors reduce capital availability, the company may be forced to rely more heavily on its balance sheet, incur higher funding costs, or accept less favorable terms.

**3. Securitization and Financing Complexities**
The company facilitates securitizations and uses warehouse credit facilities to finance loans. These activities expose the company to several risks:
*   **Risk Retention:** As a sole sponsor, the company must retain a portion of the credit risk (under Regulation RR). If these retained interests decline in value or cannot be refinanced on acceptable terms, liquidity and results of operations may suffer.
*   **Representations and Warranties:** If representations regarding transferred loans are inaccurate, the company may be required to repurchase loans or make indemnification payments, which could strain liquidity and harm its reputation.
*   **Regulatory Compliance:** Changes in laws such as the Dodd-Frank Act, the Investment Company Act of 1940, and the "Volcker Rule" may limit the structure of securitizations or restrict access to capital markets.

**4. Technology and AI Model Performance**
The company’s growth and financial health depend on the effectiveness of its artificial intelligence (AI) models. If these models fail to accurately or timely reflect changes in borrower credit risk due to economic shifts, or if there are significant disruptions or failures in the AI lending platform, the business could be adversely affected.

**5. Operational and Strategic Dependencies**
*   **Lending Partners:** The business depends on retaining existing lending partners and attracting new ones, with a limited number of partners accounting for a significant portion of originations and revenue.
*   **Loan Aggregators:** The company relies on strategic relationships with loan aggregators to attract applicants; failure to maintain these relationships could harm business growth.
*   **Product Mix:** A significant portion of historical business has depended on a single loan product, making the company vulnerable to shifts in product demand.
*   **Regulatory Compliance:** The business is subject to a wide range of evolving laws and regulations. Failure to comply, or even the perceived failure to comply, could harm the business.

**6. Financial Performance and Reputation**
*   **Profitability:** The company has incurred net losses in the past and may not achieve or sustain profitability in the future.
*   **Volatility:** Quarterly results may fluctuate significantly, impacting the trading price of common stock.
*   **Brand and Data Security:** Security breaches, improper data access, or failure to maintain the brand’s reputation could lead to liability, harm results of operations, and damage credibility.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Economic Conditions:** The business is adversely affected by uncontrollable economic factors, including uncertainty, volatility, and negative trends that impact capital supply, borrower demand, and repayment ability. Adverse macroeconomic conditions can reduce loan origination volumes, increase funding costs, and lead to higher delinquencies and defaults, particularly affecting borrowers with poor or limited credit histories.
*   **Loan Funding and Capital Sources:** The company depends on diverse and resilient loan funding from institutional investors. Risks include the inability to maintain these sources, manage risks associated with committed capital and co-investment arrangements, and the potential for decreased capital availability or increased costs.
*   **AI Model Effectiveness:** The business relies on artificial intelligence models to approve borrowers. If these models are ineffective, fail to improve, or do not accurately reflect changes in economic conditions regarding credit risk, growth and financial results could be adversely affected.
*   **Lending Partners and Concentration:** A limited number of lending partners account for a significant portion of loan originations and revenue. The business depends on retaining existing partners and attracting new ones. Additionally, a significant portion of the business has historically depended on a single loan product.
*   **Profitability and Financial Performance:** The company has incurred net losses in the past and may not achieve profitability in the future. Quarterly results may fluctuate significantly, affecting the stock price.
*   **Balance Sheet and Servicing Risks:** Risks arise from managing loans on the balance sheet, loan servicing and collections obligations, and the Upstart Macro Index (UMI). Failure to manage these risks could harm the business.
*   **Reputation and Brand:** Failure to maintain, protect, and promote the brand may harm the business. High volumes of loan repurchases or payments could also harm the company's reputation as a loan seller and servicer.
*   **Technology and Security:** Significant disruptions or failures in technology systems, including the AI lending platform, could adversely affect operations. Security breaches, improper data access, or other security incidents may harm reputation and expose the company to liability.
*   **Strategic Relationships:** The company relies on strategic relationships with loan aggregators to attract applicants. Inability to maintain these relationships or replace their services could adversely affect the business.
*   **Legal and Regulatory Compliance:** The business is subject to a wide range of evolving laws and regulations. Failure or perceived failure to comply could harm the business.
*   **New Products:** Introducing and developing new loan products carries risks if these products are not successful or if related risks are not managed effectively.
*   **Counterparty and Repurchase Risks:** Inaccurate representations and warranties in securitization or financing arrangements may require loan repurchases or indemnification payments. Failure to satisfy these obligations could lead to default, liquidity constraints, and adverse effects on financial condition. Counterparty failures in derivative instruments or facilities could also result in losses.

## Pre-written sections (judge input)

### Financial Health

Upstart Holdings, Inc. (UPST) is currently trading at $24.02 with a market capitalization of approximately $2.34 billion. The company reports annual revenue of $1.29 billion and maintains a healthy net profit margin of 4.69%. While the trailing P/E ratio stands at 48.04, the significantly lower forward P/E of 6.91 suggests strong expected earnings growth in the near term. This valuation discrepancy indicates that the market anticipates a substantial improvement in profitability, positioning the stock as potentially undervalued relative to its future earnings potential.

### Recent Developments

Upstart Holdings, Inc. (UPST) is currently trading at $24.02, reflecting a significant decline from its 52-week high of $55.22, though it remains near its yearly low of $22.555. The company maintains a positive net income of $60.3 million with a profit margin of 4.69%, supported by revenues of $1.29 billion. Notably, the forward P/E ratio of approximately 6.91 suggests that market expectations for future earnings growth are substantially higher than current trailing metrics, which currently stand at a P/E of 48.04. Investors should monitor upcoming filings, including the 10-K due in February 2026 and the 10-Q in August 2026, for further clarity on risk factors and operational performance.

### SEC Filing Highlights
Upstart’s business remains highly sensitive to macroeconomic headwinds, as rising interest rates and potential recessions threaten to suppress borrower demand and increase default rates among its credit-limited user base. The company faces significant funding risks due to its reliance on institutional capital, where fixed-cost arrangements from high-rate periods may become burdensome if market conditions shift. Additionally, operational resilience is challenged by the necessity to maintain key lending partnerships and ensure the continuous accuracy of its AI models amidst evolving regulatory landscapes.

### Risk Factors

*   **Macroeconomic Sensitivity and Credit Risk:** Adverse economic conditions, volatility, and negative trends can significantly reduce loan origination volumes, increase funding costs, and lead to higher delinquencies and defaults, particularly among borrowers with limited credit histories.
*   **Reliance on AI Models and Capital Sources:** The business is heavily dependent on the continued effectiveness of its AI lending models to accurately assess credit risk, as well as its ability to secure diverse and resilient funding from institutional investors without facing increased costs or capital constraints.
*   **Concentration and Profitability Challenges:** A significant portion of revenue and loan originations depends on a limited number of lending partners and specific loan products, while the company has a history of net losses and faces uncertainty regarding its ability to achieve sustained future profitability.

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings, Inc. leverages artificial intelligence to facilitate consumer lending, currently generating $1.29 billion in annual revenue with a net profit margin of 4.69%. The stock is notable for its significant valuation gap, where a forward P/E of 6.91 contrasts sharply with a trailing P/E of 48.04, signaling strong market expectations for near-term earnings recovery. The single most important near-term variable shaping this outcome is the company’s ability to sustain loan origination volumes amidst shifting macroeconomic conditions and interest rate environments.

### Outlook
The directional outlook for Upstart is cautiously constructive, driven by the market’s anticipation of robust earnings growth as reflected in the low forward valuation multiple. However, this thesis is heavily contingent on the stability of the macroeconomic environment; specifically, investors must monitor trends in interest rates and consumer credit health, as rising rates or economic contraction could suppress origination volumes and increase default rates among the company’s credit-limited user base. The view would weaken significantly if the company faces renewed funding constraints from institutional partners or if regulatory pressures impair the deployment of its AI models. Conversely, the outlook would strengthen if Upstart demonstrates consistent execution in maintaining key lending partnerships and proves its ability to navigate fixed-cost funding arrangements during periods of market volatility.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$1.29 billion in annual revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $1,285,890,048, which rounds to $1.29 billion; the pre-written sections also state "$1.29 billion."

---

CLAIM: "net profit margin of 4.69%"
LABEL: SUPPORTED
REASON: Source data explicitly lists `profit_margin_pct: 4.69`, confirmed in the pre-written Financial Health and Recent Developments sections.

---

CLAIM: "forward P/E of 6.91"
LABEL: SUPPORTED
REASON: Source data lists `forward_pe: 6.910321`, which rounds to 6.91; present in pre-written sections as well.

---

CLAIM: "trailing P/E of 48.04"
LABEL: SUPPORTED
REASON: Source data explicitly lists `pe_ratio: 48.04`; confirmed in pre-written sections.

---

**OUTLOOK**

---

CLAIM: "low forward valuation multiple"
LABEL: SUPPORTED
REASON: The forward P/E of 6.91 is explicitly present in the source data and is directionally low relative to the trailing P/E of 48.04; this is a qualitative restatement of two present figures.

---

*(No additional specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section beyond the qualitative directional statements, which contain no auditable numeric claims.)*

---

**SUMMARY TABLE**

| Claim | Label |
|---|---|
| $1.29 billion in annual revenue | SUPPORTED |
| Net profit margin of 4.69% | SUPPORTED |
| Forward P/E of 6.91 | SUPPORTED |
| Trailing P/E of 48.04 | SUPPORTED |
| "Low forward valuation multiple" (directional) | SUPPORTED |

All quantitative claims in the Executive Summary and Outlook are grounded in the source data. No figures were found to be unsupported or requiring inference beyond direct rounding or restatement.
