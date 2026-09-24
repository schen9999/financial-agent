# UPST — local-model

## Metadata

ticker: UPST
arm: local-model
judge_prompt_version: v2
context_sha256: 6cfb53121f3ea81856d108ee5fff0ab0c1d7208658f1afd96a0949099063e787
local_model_served_name: qwen2.5-7b-instruct
local_model_dir: qwen2.5-7b-instruct
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
  "pe_ratio": 49.89796,
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
[From Pinecone cache] I cannot provide a summary of the latest 10-K and 10-Q based on the information provided. The context materials only contain excerpts from the Risk Factors section of a 10-K filing for Upstart (UPST), specifically focusing on business and industry risks, funding and financing risks, and operational challenges.

To provide a comprehensive summary of the latest 10-K and 10-Q filings, I would need access to additional sections such as:

- Management's Discussion and Analysis (MD&A)
- Financial statements and results of operations
- Business overview and strategy
- Liquidity and capital resources
- Results for the specific periods covered

The excerpts provided only highlight risk factors and do not contain the financial performance data, operational results, or strategic updates that would constitute the key takeaways from a complete 10-K or 10-Q filing.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors affecting its business:

## Economic and Market Risks
- Adverse economic conditions, uncertainty, and volatility that impact borrower demand, approval rates, loan origination volume, and capital availability
- Macroeconomic factors affecting borrower ability and willingness to repay loans, particularly for borrowers with poor or limited credit history
- Concentration of operations in U.S. consumer credit markets

## Capital and Funding Risks
- Inability to maintain diverse and resilient loan funding from institutional investors
- Dependence on committed capital and co-investment arrangements that expose the company to credit risk compensation obligations
- Risks associated with asset-backed securitizations, warehouse credit facilities, and whole loan sale arrangements
- Potential need to repurchase loans or make payments if representations and warranties prove inaccurate
- Counterparty risk from derivative instruments and custodial arrangements

## Operational and Technology Risks
- Inability to improve or maintain effective artificial intelligence models for credit assessment
- Significant disruptions or failures in technology systems, including the AI lending platform
- Inability to approve sufficient borrowers for loans

## Business Model Risks
- Dependence on a limited number of lending partners for a significant portion of loan originations and revenue
- Reliance on strategic relationships with loan aggregators to attract applicants
- Historical dependence on a single loan product with vulnerability to product demand shifts
- Risks associated with introducing new loan products and service offerings

## Regulatory and Reputational Risks
- Compliance with evolving laws and regulations
- Security breaches and data protection failures
- Reputation and brand protection challenges
- Risks related to loan servicing and collections obligations

## Pre-written sections (judge input)

### Financial Health

As of the latest data, Upstart Holdings, Inc. (UPST) has a current stock price of $24.45 USD, with a market capitalization of approximately $237.93 million. The company's trailing P/E ratio stands at 49.9, while the forward P/E ratio is more favorable at 7.03. Revenue for the period was $1.285 billion, and the net income was $60.33 million, resulting in a profit margin of about 4.69%. These metrics suggest moderate valuation but strong profitability relative to revenue growth.

### Recent Developments

No significant recent news developments are currently available for Upstart Holdings. However, the company's most recent SEC filings—including a 10-K filed in February 2026 and a 10-Q filed in August 2026—emphasize substantial business risks that investors should carefully evaluate. The company continues to highlight uncertainties that could materially impact financial condition and operations. With a forward P/E ratio of 7.0 suggesting potential undervaluation against a current P/E of 49.9, investors should monitor upcoming earnings reports and regulatory developments in the credit services sector for catalysts that could drive stock performance.

### SEC Filing Highlights

Unable to provide SEC filing highlights at this time. The available source materials contain only risk factor disclosures from Upstart's 10-K filing and lack the necessary sections—including Management's Discussion and Analysis, financial statements, and operational results—required to identify key takeaways. A comprehensive review of the complete 10-K or 10-Q filing would be needed to accurately summarize financial performance, business developments, and material changes in the company's operations.

### Risk Factors

- **Economic and Market Risks:** Adverse economic conditions, macroeconomic uncertainties, and market volatility can affect borrower demand, loan origination volumes, and capital availability.
- **Operational and Technology Risks:** The inability to effectively maintain or improve artificial intelligence models for credit assessment and potential disruptions in technology systems could negatively impact the company's operations.

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings, Inc. is an AI-driven credit services company that uses machine learning models to assess borrower creditworthiness, operating in a market where technology-enabled lending decisions represent a meaningful differentiation from traditional underwriting approaches; the company generated $1.285 billion in revenue with a net income of $60.33 million, reflecting a profit margin of approximately 4.69%. The stock is notable now because of a striking divergence between its trailing P/E of 49.9 and its forward P/E of 7.03, a gap that signals either a significant anticipated improvement in earnings power or meaningful uncertainty about the durability of that improvement. The single most important near-term variable is whether Upstart's AI models can sustain and expand loan origination volumes in the face of macroeconomic headwinds, as that outcome will determine whether the forward valuation compression reflects genuine earnings growth or proves overly optimistic.

### Outlook
The directional outlook for Upstart is **cautiously constructive, with meaningful conditions attached**. On the tailwind side, the sharp compression implied by the gap between the trailing and forward P/E ratios suggests the market is pricing in a material improvement in earnings quality, and Upstart's AI-driven model retains a structural differentiation argument in a credit market where more precise risk assessment can be a durable competitive advantage. However, the headwinds are substantial and should not be minimized: adverse macroeconomic conditions directly suppress borrower demand and loan origination volumes, which are the lifeblood of Upstart's revenue model, and tightening capital availability could constrain the funding partnerships the company depends on. Investors should watch the trajectory of loan origination volumes across earnings reports, the health of Upstart's lending partner relationships and capital markets access, the evolution of the broader interest rate and credit environment, and any regulatory developments affecting AI-based credit decisioning. The cautiously constructive lean would strengthen if origination volumes show consistent growth, profit margins expand, and the macroeconomic backdrop stabilizes; it would weaken if economic deterioration pressures borrower quality, if AI model performance degrades, or if regulatory scrutiny of automated credit assessment intensifies.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "the company generated $1.285 billion in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $1,285,890,048, which rounds to $1.285 billion; the pre-written Financial Health section also states "$1.285 billion."

---

CLAIM: "net income of $60.33 million"
LABEL: SUPPORTED
REASON: Source data shows net_income of $60,334,000, which rounds to $60.33 million; confirmed in the pre-written Financial Health section.

---

CLAIM: "profit margin of approximately 4.69%"
LABEL: SUPPORTED
REASON: Source data states profit_margin = 0.046919998, which equals approximately 4.69%; recomputed as $60,334,000 / $1,285,890,048 = 4.692%, within 0.15 pp of 4.69%.

---

CLAIM: "trailing P/E of 49.9"
LABEL: SUPPORTED
REASON: Source data shows pe_ratio = 49.89796, which rounds to 49.9; confirmed in the pre-written Financial Health section.

---

CLAIM: "forward P/E of 7.03"
LABEL: SUPPORTED
REASON: Source data shows forward_pe = 7.034028, which rounds to 7.03; confirmed in the pre-written Financial Health and Recent Developments sections.

---

**OUTLOOK**

---

CLAIM: "the sharp compression implied by the gap between the trailing and forward P/E ratios"
LABEL: SUPPORTED
REASON: Both ratios are present in the source data (trailing P/E 49.9, forward P/E 7.03); the directional characterization of a large gap between them is arithmetically verifiable (a difference of ~42.9 points), making the "sharp compression" label a supported inference from those two figures.

---

*(No additional specific quantitative figures, price targets, thresholds, ratios, percentages, named product milestones, or forward-looking numbers appear in the Outlook section. All remaining content in the Outlook consists of qualitative directional statements, risk characterizations, and watch-item descriptions drawn from the Risk Factors pre-written section, none of which contain auditable quantitative claims.)*

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | $1.285 billion in revenue | SUPPORTED |
| 2 | Net income of $60.33 million | SUPPORTED |
| 3 | Profit margin of approximately 4.69% | SUPPORTED |
| 4 | Trailing P/E of 49.9 | SUPPORTED |
| 5 | Forward P/E of 7.03 | SUPPORTED |
| 6 | "Sharp compression" gap between trailing and forward P/E | SUPPORTED |

**No unsupported or inference-only quantitative claims were identified.** The Executive Summary and Outlook are tightly constrained to figures present in the source data, with no invented price targets, undocumented thresholds, or unverifiable forward-looking numbers introduced.
