# UPST — local-model

## Metadata

ticker: UPST
arm: local-model
judge_prompt_version: v2
context_sha256: 82f2419f5757a2738079b1a202afd2ca89800e6b096575f15824974a67eee97e
local_model_served_name: financial-lora
local_model_dir: qwen-ft
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
[From Pinecone cache] I cannot provide a summary of the latest 10-K and 10-Q based on the information provided. The context materials only contain excerpts from the Risk Factors section of a 10-K filing for Upstart (ticker: UPST), specifically focusing on business and industry risks, funding and financing risks, and operational challenges.

To provide a comprehensive summary of the latest 10-K and 10-Q filings, I would need access to additional sections such as:

- Management's Discussion and Analysis (MD&A)
- Financial statements and results of operations
- Business overview and strategy
- Liquidity and capital resources
- Results from the most recent quarter (10-Q)

Based solely on the risk factors section provided, the key themes include concerns about economic conditions affecting borrower demand and repayment ability, dependence on institutional investor capital, reliance on AI models for credit decisions, concentration in U.S. consumer credit, and regulatory compliance challenges. However, this represents only the risk disclosure portion of the filings and does not constitute a complete summary of the company's financial performance, operations, or outlook.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses numerous material risk factors affecting its business, which can be categorized into several key areas:

## Economic and Market Risks
- Adverse economic conditions, uncertainty, and volatility that impact borrower demand, approval rates, and loan origination volume
- Reduced capital supply from lending partners and institutional investors during economic downturns
- Borrowers with limited credit history being disproportionately affected by inflation, higher interest rates, and unemployment

## Funding and Capital Risks
- Inability to maintain diverse and resilient loan funding from institutional investors
- Dependence on committed capital and co-investment arrangements that expose the company to credit risk compensation obligations
- Risks associated with asset-backed securitizations, warehouse credit facilities, and whole loan sale arrangements
- Potential repurchase obligations if loan representations and warranties prove inaccurate

## Operational and Technology Risks
- Failure to improve or maintain effective artificial intelligence models for credit assessment
- Significant disruptions or failures in technology systems, including the AI lending platform
- Inability to approve a sufficient number of borrowers for loans

## Business Concentration Risks
- Heavy reliance on a limited number of lending partners for a significant portion of loan originations and revenue
- Dependence on a single loan product historically
- Concentration of operations in U.S. consumer credit markets

## Additional Risks
- Inability to maintain relationships with loan aggregators
- Security breaches and data protection failures
- Regulatory compliance challenges across evolving laws and regulations
- Reputation and brand management issues
- Loan servicing and collections management risks

## Pre-written sections (judge input)

### Financial Health
Upstart Holdings, Inc., trades under the ticker symbol UPST. It is listed on the Nasdaq Capital Market. As of February 10, 2026, the company carries a market capitalization of $237.9 billion and a P/E ratio of 46.1x (7.0x forward). The company reports net income of $6.0 billion and a net profit margin of 4.69%. The company operates within the sector of Financial Services and the industry of Credit Services.

### Recent Developments

Recent SEC filings highlight significant risk factors for Upstart Holdings, with both the 2026 10-K and 10-Q emphasizing material uncertainties affecting the business and financial condition. The company's stock has experienced considerable volatility, trading near its 52-week low of $23.97 despite a forward P/E ratio of 7.03, suggesting the market has priced in substantial headwinds. With a modest profit margin of 4.7% and elevated current valuation multiples relative to earnings, investors should carefully review the detailed risk disclosures in recent filings before making investment decisions. The lack of recent positive news developments, combined with regulatory scrutiny typical in the credit services sector, indicates a cautious near-term outlook for the stock.

### SEC Filing Highlights

Based on available information, Upstart's recent filings emphasize significant business risks including dependence on institutional investor capital for funding, reliance on AI models for credit underwriting decisions, and exposure to economic cycles affecting borrower demand and repayment ability. The company faces concentration risk in the U.S. consumer credit market and ongoing regulatory compliance challenges. A comprehensive analysis of financial performance, operational results, and management guidance would require access to the full MD&A and financial statements sections of the most recent 10-K and 10-Q filings.

### Primary Risk Factors Disclosed

The company discloses numerous material risk factors affecting its business, which can be categorized into several key areas:

#### Economic and Market Risks
- Adverse economic conditions, uncertainty, and volatility that impact borrower demand, approval rates, and loan origination volume.
- Reduced capital supply from lending partners and institutional investors during economic downturns.
- Borrowers with limited credit history being disproportionately affected by inflation, higher interest rates, and unemployment.

#### Funding and Capital Risks
- Inability to maintain diverse and resilient loan funding from institutional investors.
- Dependence on committed capital and co-investment arrangements that expose the company to credit risk compensation obligations.
- Risks associated with asset-backed securitizations, warehouse credit facilities, and whole loan sale arrangements.
- Potential repurchase obligations if loan representations and warranties prove inaccurate.

#### Operational and Technology Risks
- Failure to improve or maintain effective artificial intelligence models for credit assessment.
- Significant disruptions or failures in technology systems, including the AI lending platform.
- Inability to approve a sufficient number of borrowers for loans.

#### Business Concentration Risks
- Heavy reliance on a limited number of lending partners for a significant portion of loan originations and revenue.
- Dependence on a single loan product historically.
- Concentration of operations in U.S. consumer credit markets.

#### Additional Risks
- Inability to maintain relationships with loan aggregators.
- Security breaches and data protection failures.
- Regulatory compliance challenges across evolving laws and regulations.
- Reputation and brand management issues.
- Loan servicing and collections management risks.

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings, Inc. is an AI-driven credit services company operating within the Financial Services sector, carrying a market capitalization of $237.9 billion and reporting net income of $6.0 billion at a net profit margin of 4.69%. The stock is notable now because it trades near its 52-week low of $23.97 while carrying a trailing P/E of 46.1x alongside a sharply lower forward P/E of 7.0x — a divergence that signals the market is pricing in meaningful near-term earnings improvement expectations even as material uncertainties disclosed in recent SEC filings weigh on sentiment. The single most important near-term variable is Upstart's ability to sustain and diversify institutional funding capital, as the company's entire origination engine depends on continued investor appetite for its AI-underwritten loans — an appetite that can contract rapidly in adverse economic or credit conditions.

### Outlook
The directional outlook for Upstart is **cautious**, with the balance of near-term evidence tilting toward headwinds outweighing tailwinds. On the headwind side, the stock's proximity to its 52-week low, the modest profit margin, and the breadth of material risk factors disclosed in recent filings — spanning funding concentration, AI model reliability, regulatory pressure, and macroeconomic sensitivity — collectively argue for restraint. The company's borrower base, which skews toward individuals with limited credit history, remains particularly vulnerable to any deterioration in employment conditions, inflation, or interest rate levels. On the tailwind side, the wide gap between the trailing and forward P/E ratios suggests the market may already be discounting a meaningful earnings recovery, and Upstart's AI-driven underwriting model retains a differentiated positioning within the credit services industry if macro conditions stabilize. Investors should monitor the following key variables: the depth and diversity of institutional funding commitments and capital market appetite for Upstart-originated loans; the trajectory of interest rates and their effect on borrower demand and approval rates; demonstrated improvement in AI model performance and loan repayment outcomes; progress in expanding beyond concentration in a single loan product and a limited lending partner base; and the evolving regulatory environment governing AI-based credit decisions. A sustained improvement in funding partner breadth, combined with stabilizing credit performance and a more constructive macro backdrop, would be the conditions most likely to shift this view in a more constructive direction.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of $237.9 billion"
LABEL: UNSUPPORTED
REASON: The raw source data shows market_cap = $2,379,304,192 (~$2.38 billion); the pre-written Financial Health section erroneously states "$237.9 billion," and the AI reproduced that error — the actual figure is approximately $2.38 billion, not $237.9 billion.

---

CLAIM: "net income of $6.0 billion"
LABEL: UNSUPPORTED
REASON: The raw source data shows net_income = $60,334,000 (~$60.3 million); the pre-written Financial Health section erroneously states "$6.0 billion," and the AI reproduced that error — the actual figure is approximately $60.3 million, not $6.0 billion.

---

CLAIM: "net profit margin of 4.69%"
LABEL: SUPPORTED
REASON: The raw source data explicitly states profit_margin = 0.046919998, which equals 4.69% (rounded to two decimal places); also confirmed by recomputation: $60,334,000 / $1,285,890,048 ≈ 4.69%.

---

CLAIM: "trades near its 52-week low of $23.97"
LABEL: SUPPORTED
REASON: The raw source data states week_52_low = 23.965, which rounds to $23.97 (or $23.965 as stated in the Recent Developments pre-written section as $23.97); the current price of $24.45 is indeed near this low, and the figure $23.97 matches the source rounded to two decimal places.

---

CLAIM: "trailing P/E of 46.1x"
LABEL: SUPPORTED
REASON: The raw source data explicitly states pe_ratio = 46.13208, which rounds to 46.1x.

---

CLAIM: "forward P/E of 7.0x"
LABEL: SUPPORTED
REASON: The raw source data explicitly states forward_pe = 7.034028, which rounds to 7.0x.

---

**OUTLOOK**

---

CLAIM: "the stock's proximity to its 52-week low"
LABEL: SUPPORTED
REASON: Current price = $24.45 vs. 52-week low = $23.965; the stock is approximately $0.49 (about 2%) above its 52-week low, confirming proximity arithmetically.

---

CLAIM: "the modest profit margin"
LABEL: SUPPORTED
REASON: The raw source data confirms profit_margin = 4.69%, which is a modest margin; this is a directional/qualitative restatement of a figure present in the source data.

---

CLAIM: "the wide gap between the trailing and forward P/E ratios"
LABEL: SUPPORTED
REASON: Trailing P/E = 46.13x and forward P/E = 7.03x are both present in the source data; the gap of ~39 points is arithmetically verifiable and constitutes a wide divergence.

---

*No additional specific quantitative figures, price targets, thresholds, ratios, named product milestones, or forward-looking numbers appear in the Outlook section beyond those already audited above. All qualitative risk-factor references (funding concentration, AI model reliability, regulatory pressure, macroeconomic sensitivity, borrower base characteristics, single loan product concentration, limited lending partner base, AI-based credit decisions) are drawn from the pre-written Risk Factors and SEC Filing Highlights sections and contain no additional quantitative claims requiring arithmetic verification.*

---

**SUMMARY OF KEY FINDINGS:**

The two most material errors are the market capitalization ($237.9 billion vs. the correct ~$2.38 billion) and net income ($6.0 billion vs. the correct ~$60.3 million) — both off by a factor of 100. These errors originated in the pre-written Financial Health section and were uncritically reproduced by the AI in the Executive Summary.
