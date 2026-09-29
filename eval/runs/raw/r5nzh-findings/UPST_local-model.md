# UPST — local-model

## Metadata

ticker: UPST
arm: local-model
judge_prompt_version: v2
context_sha256: 1ae41311fdd60d4d35310690743fb211c910392ec4a7b4bccd047cc12568e5e0
local_model_served_name: financial-lora-w4a16
local_model_dir: qwen-ft-w4a16
local_model_backend: openai
local_model_url: http://vllm.financial-agent.svc:8000
local_model_sampling: {"max_tokens": 512, "min_p": 0.0, "repetition_penalty": 1.1, "temperature": 0.1, "top_k": 20, "top_p": 0.8}

## Retrieved source context

STOCK DATA:
{
  "ticker": "UPST",
  "company_name": "Upstart Holdings, Inc.",
  "current_price": 23.03,
  "currency": "USD",
  "market_cap": 2241119488.0,
  "pe_ratio": 44.288464,
  "forward_pe": 6.625508,
  "week_52_high": 55.22,
  "week_52_low": 22.785,
  "revenue": 1285890048.0,
  "net_income": 60334000.0,
  "profit_margin": 0.046919998,
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
[From Pinecone cache] I cannot provide a summary of the latest 10-K and 10-Q based on the information provided. The context only includes excerpts from the Risk Factors section of a 10-K filing for Upstart (ticker: UPST), which focuses specifically on potential risks and uncertainties facing the business.

To provide a comprehensive summary of the latest 10-K and 10-Q filings, I would need access to additional sections such as:

- Management's Discussion and Analysis (MD&A)
- Financial statements and results of operations
- Business overview and strategy
- Liquidity and capital resources
- Critical accounting policies

The risk factors section alone does not represent the full scope of what these filings contain. If you'd like, I can summarize the specific risks outlined in the provided context, or you could provide additional sections from the filings for a more complete overview.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses numerous material risk factors affecting its business, which can be organized into several key categories:

## Economic and Market Risks
- Adverse economic conditions, uncertainty, and volatility that impact borrower demand, approval rates, and loan origination volume
- Reduced capital supply from lending partners and institutional investors during economic downturns
- Borrowers with limited credit history being disproportionately affected by inflation, higher interest rates, and unemployment
- Increased delinquencies, defaults, and charge-offs during economic downturns

## Capital and Funding Risks
- Inability to maintain diverse and resilient loan funding from institutional investors
- Dependence on committed capital and co-investment arrangements that expose the company to credit risk compensation obligations
- Risks associated with asset-backed securitizations, warehouse credit facilities, and whole loan sale arrangements
- Potential need to repurchase loans or make payments if representations and warranties prove inaccurate
- Counterparty risk from derivative instruments and custodial arrangements

## Operational and Technology Risks
- Inability to improve or maintain effective AI models for credit assessment
- Significant disruptions or failures in technology systems and the AI lending platform
- Dependence on strategic relationships with loan aggregators to attract applicants

## Business Model Risks
- Concentration in a limited number of lending partners for loan originations and revenue
- Historical dependence on a single loan product
- Inability to successfully introduce and manage new loan products
- Quarterly results fluctuations

## Regulatory and Reputational Risks
- Compliance with evolving laws and regulations
- Security breaches and data protection failures
- Brand and reputation management challenges
- Risks related to loan servicing and collections obligations

## Pre-written sections (judge input)

### Financial Health
Investing in our common stock involves a high degree of risk. The risks and uncertainties described below should be carefully considered, together with all of the other information in this Annual Report on Form 10-K, including the section titled Management's Discussion and Analysis of Financial Condition and Results of Operations and our condensed consolidated financial statements and related notes, before making a decision to invest in our common stock. Our business, financial condition, results of operations, or prospects could also be harmed by risks and uncertainties not currently known to us or that we currently do not believe are material. If any of the risks actually occur, our business, financial condition, results of operations, and prospects could be adversely affected.

### Recent Developments

Recent SEC filings highlight significant risk factors for Upstart Holdings, with the company emphasizing substantial uncertainties affecting its business outlook in both its 2026 10-K and 10-Q filings. The stock has experienced considerable volatility, trading near its 52-week low of $22.79 despite a forward P/E ratio of 6.63, suggesting the market has priced in meaningful headwinds. With a modest profit margin of 4.7% and elevated current valuation multiples relative to historical performance, investors should carefully weigh the company's disclosed risks against its AI-driven lending platform potential. The lack of recent positive news catalysts, combined with cautionary regulatory disclosures, indicates a period of uncertainty that warrants close monitoring of upcoming earnings and strategic developments.

### SEC Filing Highlights

Unable to provide a comprehensive summary at this time. The available data contains only risk factor disclosures from Upstart's 10-K filing, which do not represent the full scope of SEC filing contents. A complete analysis would require access to additional sections including Management's Discussion and Analysis (MD&A), financial statements, business overview, and results of operations. Please provide supplementary filing sections for a detailed investment brief.

# Primary Risk Factors Disclosed

The company discloses numerous material risk factors affecting its business, which can be organized into several key categories:

## Economic and Market Risks
- Adverse economic conditions, uncertainty, and volatility that impact borrower demand, approval rates, and loan origination volume
- Reduced capital supply from lending partners and institutional investors during economic downturns
- Borrowers with limited credit history being disproportionately affected by inflation, higher interest rates, and unemployment
- Increased delinquencies, defaults, and charge-offs during economic downturns

## Capital and Funding Risks
- Inability to maintain diverse and resilient loan funding from institutional investors
- Dependence on committed capital and co-investment arrangements that expose the company to credit risk compensation obligations
- Risks associated with asset-backed securitizations, warehouse credit facilities, and whole loan sale arrangements
- Potential need to repurchase loans or make payments if representations and warranties prove inaccurate
- Counterparty risk from derivative instruments and custodial arrangements

## Operational and Technology Risks
- Inability to improve or maintain effective AI models for credit assessment
- Significant disruptions or failures in technology systems and the AI lending platform
- Dependence on strategic relationships with loan aggregators to attract applicants

## Business Model Risks
- Concentration in a limited number of lending partners for loan originations and revenue
- Historical dependence on a single loan product
- Inability to successfully introduce and manage new loan products
- Quarterly results fluctuations

## Regulatory and Reputational Risks
- Compliance with evolving laws and regulations
- Security breaches and data protection failures
- Brand and reputation management challenges
- Risks related to loan servicing and collections obligations

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings operates an AI-driven lending platform that connects borrowers — many with limited traditional credit histories — with bank and credit union lending partners, positioning itself at the intersection of fintech innovation and consumer credit markets. The stock is notable today because it is trading near its 52-week low of $22.79, carries a forward P/E of 6.63, and posts a profit margin of only 4.7%, a combination that reflects a market pricing in substantial headwinds even as the underlying AI lending thesis remains intact. The single most important near-term variable is whether Upstart can sustain and broaden its base of lending partners and institutional capital providers, because without that funding supply, loan origination volume — and therefore revenue — cannot recover regardless of how well its AI models perform.

### Outlook
The directional outlook for Upstart is **cautious**, with the balance of near-term risks outweighing visible catalysts. On the headwind side, the macro environment remains the dominant force: elevated interest rates and persistent inflation disproportionately pressure the non-prime and thin-file borrowers that Upstart's platform is designed to serve, compressing both demand for loans and the willingness of institutional capital providers to fund them. Concentration risk among a limited number of lending partners amplifies this vulnerability — any pullback by key partners could have an outsized impact on origination volume and revenue. On the tailwind side, the company's AI-driven credit model represents a genuine structural differentiator if it can demonstrate superior loss performance through a full credit cycle, and a sustained decline in interest rates could meaningfully re-open both borrower demand and institutional appetite for consumer credit assets. Investors should monitor four key variables: (1) the trajectory of the federal funds rate and its effect on consumer credit demand; (2) trends in delinquency, default, and charge-off rates across Upstart's loan portfolio as a real-time test of AI model efficacy; (3) the breadth and stability of the lending partner and institutional investor base; and (4) progress in diversifying beyond the company's historically concentrated loan product mix into new product categories. A move toward a more constructive view would require visible improvement in funding partner diversification, stabilizing credit performance, and a macro environment that reduces pressure on the borrower segments Upstart serves — none of which appear imminent based on currently available information.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "trading near its 52-week low of $22.79"
LABEL: SUPPORTED
REASON: The source data lists the 52-week low as $22.785, which rounds to $22.79 (within $0.005); the current price of $23.03 confirms the stock is trading near that low.

---

CLAIM: "carries a forward P/E of 6.63"
LABEL: SUPPORTED
REASON: The source data lists forward_pe as 6.625508, which rounds to 6.63 (within 0.01).

---

CLAIM: "posts a profit margin of only 4.7%"
LABEL: SUPPORTED
REASON: The source data lists profit_margin as 0.046919998, which rounds to 4.7% (within 0.15 percentage points).

---

**OUTLOOK**

The Outlook section is largely qualitative and directional. I will identify every specific quantitative or forward-looking figure embedded within it.

---

CLAIM: (No explicit numerical figures appear in the Outlook section beyond those already audited above.)
LABEL: N/A
REASON: The Outlook section contains no additional specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers beyond what was already covered in the Executive Summary. All remaining content is qualitative directional language (e.g., "cautious," "dominant force," "outsized impact," "none of which appear imminent") that does not constitute a specific quantitative or forward-looking numerical claim subject to audit under the defined criteria.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | 52-week low of $22.79 | SUPPORTED |
| 2 | Forward P/E of 6.63 | SUPPORTED |
| 3 | Profit margin of only 4.7% | SUPPORTED |

All three auditable quantitative claims in the Executive Summary and Outlook are **SUPPORTED** by the raw source data. The Outlook section introduces no additional quantitative claims requiring verification.
