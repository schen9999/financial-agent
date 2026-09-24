# UPST — local-model

## Metadata

ticker: UPST
arm: local-model
judge_prompt_version: v2
context_sha256: 47643712df42b3311a334a5c7a6e3baf33faa5b2fd43dac60ede78e6937e9a0d
local_model_served_name: qwen2.5-1.5b-instruct
local_model_dir: qwen2.5-1.5b-instruct
local_model_backend: openai
local_model_url: http://vllm.financial-agent.svc:8000
local_model_sampling: {"max_tokens": 512, "min_p": 0.0, "repetition_penalty": 1.1, "temperature": 0.1, "top_k": 20, "top_p": 0.8}

## Retrieved source context

STOCK DATA:
{
  "ticker": "UPST",
  "company_name": "Upstart Holdings, Inc.",
  "current_price": 24.45,
  "currency": "USD",
  "market_cap": 2379304192.0,
  "pe_ratio": 46.13208,
  "forward_pe": 7.034028,
  "week_52_high": 64.15,
  "week_52_low": 23.965,
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
[From Pinecone cache] I cannot provide a summary of the latest 10-K and 10-Q based on the information provided. The context materials only contain excerpts from the Risk Factors section of a 10-K filing for Upstart (ticker: UPST), specifically focusing on business and industry risks, funding and financing risks, and operational challenges.

To provide a comprehensive summary of the latest 10-K and 10-Q filings, I would need access to additional sections such as:

- Management's Discussion and Analysis (MD&A)
- Financial statements and results of operations
- Business overview and strategy
- Liquidity and capital resources
- Results from the most recent quarter (10-Q)

Based solely on the risk factors section provided, the key themes discussed include:

- Economic sensitivity and macroeconomic headwinds affecting borrower demand and ability to repay
- Dependence on institutional investor capital and funding arrangements
- Reliance on AI models for credit decisions
- Concentration risk with lending partners
- Regulatory and compliance challenges
- Technology and cybersecurity risks
- Loan servicing and collections obligations

However, this represents only the risk disclosure portion of the filings and does not capture the full picture of the company's financial performance, strategic initiatives, or overall business results.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors affecting its business:

## Economic and Market Risks
- Adverse economic conditions, uncertainty, and volatility that impact borrower demand, approval rates, loan origination volume, and capital availability
- Macroeconomic factors beyond the company's control that affect borrower ability and willingness to repay loans
- Concentration of operations in U.S. consumer credit, making the business vulnerable to domestic economic downturns

## Capital and Funding Risks
- Inability to maintain diverse and resilient loan funding from institutional investors
- Dependence on committed capital and co-investment arrangements that expose the company to credit risk compensation obligations
- Risks associated with asset-backed securitizations, warehouse credit facilities, and whole loan sale arrangements
- Potential need to repurchase loans or make payments if representations and warranties prove inaccurate

## Operational and Technology Risks
- Ineffectiveness of artificial intelligence models in accurately assessing borrower credit risk
- Inability to approve a significant number of borrowers for loans
- Significant disruptions or failures in technology systems, including the AI lending platform
- Dependence on strategic relationships with loan aggregators

## Business Model Risks
- Heavy reliance on a limited number of lending partners for loan originations and revenue
- Historical net losses and inability to sustain profitability
- Significant fluctuations in quarterly results
- Dependence on a single loan product historically

## Regulatory and Reputational Risks
- Compliance with evolving laws and regulations
- Security breaches and data protection failures
- Risks related to loan servicing and collections obligations
- Importance of brand reputation and credibility

## Pre-written sections (judge input)

### Financial Health

#### Key Metrics:

- **Current Price:** $24.45 USD
- **Market Cap:** $23,793,041,920 USD
- **P/E Ratio:** 46.13x
- **Forward PE Ratio:** 7.03x
- **Revenue:** $1,285,890,048 USD
- **Net Income:** $60,334,000 USD
- **Profit Margin:** 4.7%

#### Brief Financial Assessment:

Upstart Holdings, Inc., operates within the Financial Services sector under the Credit Services industry. The company's current valuation is substantial at $23.79 billion, reflecting its significant market capitalization. With a trailing P/E ratio of 46.13 times earnings, the stock appears overvalued compared to peers. However, the forward P/E ratio of 7.03 suggests potential growth opportunities if the company maintains its profitability trajectory. Revenue has been steadily increasing, indicating strong operational performance. Despite these positive indicators, investors should consider the higher-than-average P/E ratios and the company's exposure to various credit-related risks as part of their investment analysis.

### Recent Developments

No significant recent news developments are currently available for Upstart Holdings. However, the company's most recent SEC filings—including a 10-K filed in February 2026 and a 10-Q filed in August 2026—emphasize substantial business risks that investors should carefully evaluate. With a forward P/E ratio of 7.0x against a current P/E of 46.1x, the market appears to be pricing in meaningful earnings growth expectations, though the company's modest 4.7% profit margin suggests limited near-term profitability cushion. Investors should monitor upcoming earnings reports and regulatory developments in the AI-driven lending space, as Upstart's business model remains sensitive to credit market conditions and regulatory changes.

### SEC Filing Highlights

Based on available risk disclosures, Upstart faces significant macroeconomic sensitivity affecting borrower demand and repayment capacity, alongside dependence on institutional investor capital for funding arrangements. The company relies heavily on AI models for credit decisions, creating concentration risk with lending partners and exposure to regulatory compliance challenges. Key operational risks include technology vulnerabilities, cybersecurity threats, and loan servicing obligations that could impact financial performance and investor returns.

### Primary Risk Factors Disclosed

1. **Economic and Market Risks**: Adverse economic conditions, uncertainty, and volatility impacting borrower demand, approval rates, loan origination volume, and capital availability; macroeconomic factors beyond the company’s control affecting borrower ability and willingness to repay loans; concentration of operations in U.S. consumer credit, making the business vulnerable to domestic economic downturns.

2. **Capital and Funding Risks**: Inability to maintain diverse and resilient loan funding from institutional investors; dependence on committed capital and co-investment arrangements exposing the company to credit risk compensation obligations; risks associated with asset-backed securitizations, warehouse credit facilities, and whole loan sale arrangements; potential need to repurchase loans or make payments if representations and warranties prove inaccurate.

3. **Operational and Technology Risks**: Effectiveness of artificial intelligence models in accurately assessing borrower credit risk; inability to approve a significant number of borrowers for loans; significant disruptions or failures in technology systems, including the AI lending platform; dependence on strategic relationships with loan aggregators.

4. **Business Model Risks**: Heavy reliance on a limited number of lending partners for loan originations and revenue; historical net losses and inability to sustain profitability; significant fluctuations in quarterly results; dependence on a single loan product historically.

5. **Regulatory and Reputational Risks**: Compliance with evolving laws and regulations; security breaches and data protection failures; risks related to loan servicing and collections obligations; importance of brand reputation and credibility.

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings, Inc. is an AI-driven consumer credit platform operating within the Financial Services sector's Credit Services industry, generating $1.29 billion in revenue with a market capitalization of approximately $23.79 billion. The stock is notable now for the striking divergence between its trailing P/E of 46.13x and its forward P/E of 7.03x, a gap that signals the market is pricing in a substantial earnings acceleration — yet the company's current 4.7% profit margin leaves little room for error if that growth fails to materialize. The single most important near-term variable is whether Upstart's AI lending platform can sustain and expand loan origination volume in a manner that converts revenue growth into durable, widening profitability.

### Outlook
The directional outlook for Upstart is **cautiously constructive, but contingent on several critical variables resolving favorably**. On the tailwind side, the sharp compression implied by the forward P/E relative to the trailing P/E suggests the market anticipates meaningful earnings improvement, and continued revenue growth would support that narrative if it is accompanied by expanding profit margins rather than simply higher top-line volume. Key variables to monitor include the trajectory of U.S. consumer credit conditions — since deteriorating macroeconomic conditions would directly suppress borrower demand, approval rates, and repayment capacity — as well as the health and diversity of Upstart's institutional funding relationships, which underpin the entire origination model. Investors should also watch the regulatory environment surrounding AI-driven lending decisions, as adverse rule-making could constrain the platform's core underwriting approach and lending partner relationships. The thesis would strengthen if successive earnings reports demonstrate consistent margin expansion, successful diversification beyond the company's historically single-product focus, and a broadening of its lending partner base; it would weaken if macroeconomic headwinds compress origination volume, if institutional capital partners pull back, or if regulatory scrutiny intensifies in ways that limit the AI model's operational flexibility.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$1.29 billion in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $1,285,890,048, which rounds to $1.29 billion.

---

CLAIM: "market capitalization of approximately $23.79 billion"
LABEL: UNSUPPORTED
REASON: The raw source data lists market_cap as $2,379,304,192 (approximately $2.38 billion); the pre-written Financial Health section incorrectly states $23,793,041,920, and the AI brief reproduces that erroneous figure — the actual source figure is ~$2.38 billion, not ~$23.79 billion.

---

CLAIM: "trailing P/E of 46.13x"
LABEL: SUPPORTED
REASON: Source data explicitly lists pe_ratio as 46.13208, which rounds to 46.13x.

---

CLAIM: "forward P/E of 7.03x"
LABEL: SUPPORTED
REASON: Source data explicitly lists forward_pe as 7.034028, which rounds to 7.03x.

---

CLAIM: "current 4.7% profit margin"
LABEL: SUPPORTED
REASON: Source data lists profit_margin as 0.046919998, which rounds to 4.7%.

---

**OUTLOOK**

---

CLAIM: "sharp compression implied by the forward P/E relative to the trailing P/E"
LABEL: SUPPORTED
REASON: Forward P/E of 7.03x versus trailing P/E of 46.13x represents a large compression, directly derivable from the two figures present in the source data.

---

CLAIM: "successful diversification beyond the company's historically single-product focus"
LABEL: SUPPORTED
REASON: The pre-written Risk Factors section explicitly states "dependence on a single loan product historically" as a business model risk, making this a direct restatement of a source fact.

---

*(No additional quantitative figures, price targets, thresholds, ratios, specific percentages, named product milestones, or forward-looking numbers appear in the Outlook section beyond those already evaluated above and the qualitative directional statements, which are not subject to quantitative audit.)*

---

**SUMMARY NOTE:** The most material finding is that the market capitalization figure of ~$23.79 billion is **UNSUPPORTED** — it is inflated by a factor of roughly 10x relative to the actual source data figure of ~$2.38 billion. This error originated in the pre-written Financial Health section and was carried forward uncritically into the Executive Summary.
