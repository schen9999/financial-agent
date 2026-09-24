# EVGO — local-model

## Metadata

ticker: EVGO
arm: local-model
judge_prompt_version: v2
context_sha256: e18aed21db8f3a009c35702ddd2814c73aa0efc9757a423533fef00b0a459121
local_model_served_name: qwen2.5-1.5b-instruct
local_model_dir: qwen2.5-1.5b-instruct
local_model_backend: openai
local_model_url: http://vllm.financial-agent.svc:8000
local_model_sampling: {"max_tokens": 512, "min_p": 0.0, "repetition_penalty": 1.1, "temperature": 0.1, "top_k": 20, "top_p": 0.8}

## Retrieved source context

STOCK DATA:
{
  "ticker": "EVGO",
  "company_name": "EVgo, Inc.",
  "current_price": 1.36,
  "currency": "USD",
  "market_cap": 427741376.0,
  "forward_pe": -3.0909092,
  "week_52_high": 5.18,
  "week_52_low": 1.23,
  "revenue": 402948000.0,
  "net_income": -54125000.0,
  "profit_margin": -0.13502,
  "sector": "Consumer Cyclical",
  "industry": "Specialty Retail"
}

NEWS ARTICLES:
[]

SEC FILING SUMMARIES:
{
  "10-K": {
    "form_type": "10-K",
    "filing_date": "2026-03-09",
    "summary": "Item 1A. Risk Factors . In the course of conducting our business operations, we are exposed to a variety of risks, any of which have affected or could materially and adversely affect our business, financial condition and results of operations. Before you make a decision to buy our securities, in addition to the risks and uncertainties discussed above under \u201cCautionary Statement Regarding Forward-Looking Statements,\u201d you should carefully consider the specific risks set forth herein. If any of these risks actually occur, our business, financial condition, liquidity and results of operations may be harmed. As a result, the market price of our securities could decline, possibly significantly or permanently, and you could lose all or part of your investment. Additionally, the risks and uncertai"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-06",
    "summary": "Item 1A. Risk Factors In the course of conducting our business operations, we are exposed to a variety of risks, any of which have affected or could materially adversely affect our business, financial condition, and results of operations. The market price of our securities could decline, possibly significantly or permanently, if one or more of these risks and uncertainties occur. Before you make a decision to buy our securities, in addition to the risks and uncertainties discussed above under \u201cCautionary Statement Regarding Forward-Looking Statements,\u201d you should carefully consider the specific risk factors set forth in the \u201cRisk Factors\u201d section in the Annual Report. There have been no material changes to the risk factors disclosed in Part I, Item 1A of the Annual Report. See the \u201cItem 5 "
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] # Key Takeaways from EVGO's SEC Filings

Based on the risk factors disclosed, here are the primary takeaways:

## Financial Position and Outlook
- As of December 31, 2025, the company had $210.7 million in cash, cash equivalents, and restricted cash, with $161.2 million in working capital
- The company has a history of operating losses and expects to continue incurring significant expenses and losses in the near- and medium-term
- Future profitability depends on successful capital draws from the DOE Loan and the Credit Agreement

## Business Dependencies
- Growth is heavily dependent on continued EV adoption by consumers, fleet operators, and governments
- Success relies on OEM partnerships and their ability to supply EVs to the market
- The company depends on a limited number of vendors for charging equipment and a limited number of customers and OEM partners

## Key Risk Areas
- **Market Risk**: EV adoption may not continue at expected rates; the market for public DC fast charging may develop more slowly than anticipated
- **Regulatory Risk**: Changes in government policy at federal and state levels create uncertainty; potential expiration of EV tax incentives and regulatory changes could impact demand
- **Operational Risk**: Supply chain disruptions, construction delays, and rapid growth management challenges
- **Financing Risk**: The DOE Loan contains conditions precedent to draws and imposes operational restrictions; additional financing may be needed on unfavorable terms

## Market Challenges
- EV pricing remains higher than traditional vehicles, affecting consumer demand
- Automotive industry cyclicality may be more pronounced for commercial fleet purchasers
- Competition from alternative fuel vehicles and other charging methods

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several categories of primary risk factors:

## Business-Related Risks
- Operating as an early-stage growth company with a history of losses and expectations of continuing losses in the near and medium term
- Heavy dependence on EV adoption and demand, as well as OEMs' ability to supply EVs to the market
- Challenges in managing rapid growth effectively
- Uncertainty created by current and future federal and state administrations regarding the EV sector
- Potential inaccuracy of market opportunity estimates and growth forecasts
- Significant competition in the EV charging market
- Reliance on a limited number of vendors for charging equipment and support services
- Dependence on a limited number of customers and OEM partners
- Supply chain disruptions
- Need for additional funding that may not be available on favorable terms

## DOE Loan-Related Risks
- Substantial dependence on the ability to fully draw on the DOE Loan, which has multiple conditions precedent
- Risk of default if unable to comply with loan covenants
- Substantial assets pledged as collateral, limiting availability for additional secured debt
- Operational restrictions imposed on subsidiaries under the loan terms
- Limitations on cash distributions from subsidiaries needed to fund operations

## EV Market Risks
- Changes to fuel economy standards or success of alternative fuels negatively impacting EV demand
- Slower-than-expected electrification of rideshare and commercial fleets
- Reduction or elimination of government rebates, tax credits, and financial incentives

## Other Risks
- Technology, intellectual property, and infrastructure protection challenges
- Transition to NACS charging standards creating uncertainty and costs
- Material weaknesses in internal controls over financial reporting
- Inflationary pressures affecting equipment and operating costs
- Tax law changes and liabilities

## Pre-written sections (judge input)

### Financial Health

**Price:** $1.36 per share as of [insert date]

**Market Cap:** $4,277,413,760

**P/E Ratio:** -3.09x

**Revenue:** $4,029,480,000

**Net Income:** -$54,125,000

**Profit Margin:** -13.50%

The company's stock is trading at a significant discount compared to its historical high of $5.18, indicating that investors perceive it as undervalued. Despite facing losses in net income, the negative profit margin suggests that the company is not generating sufficient profits to cover its expenses. The low P/E ratio (-3.09x) indicates that the market expects future earnings growth to be very modest, suggesting caution among investors. However, the current valuation might be driven by short-term trends rather than long-term fundamentals. Investors should closely monitor the company's performance and profitability moving forward to assess whether this valuation remains justified.

### Recent Developments

EVgo's most recent SEC filings (10-K filed March 2026 and 10-Q filed August 2026) emphasize significant operational risks without material changes to previously disclosed risk factors, suggesting ongoing business challenges. The company continues to operate at a loss with a negative profit margin of -13.5% and net income of -$54.1 million, indicating the EV charging network operator has not yet achieved profitability despite $403 million in revenue. With the stock trading at $1.36—down 74% from its 52-week high of $5.18—investors should carefully evaluate whether EVgo can execute its growth strategy and reach cash flow positivity before capital constraints become critical.

### SEC Filing Highlights

EVgo reported $210.7 million in cash and equivalents as of December 31, 2025, with $161.2 million in working capital, though the company continues to operate at a loss and expects significant near-term expenses. The company's growth trajectory is heavily dependent on continued EV adoption, OEM partnerships, and successful capital draws from its DOE Loan and Credit Agreement facilities. Key risks include potential slowdown in EV market adoption, regulatory changes affecting EV incentives, supply chain disruptions, and reliance on a limited number of vendors and customers. EVgo faces competitive pressures from alternative fuel vehicles and other charging infrastructure providers, while EV pricing premiums continue to impact consumer demand. Future profitability hinges on scaling operations efficiently while managing the operational restrictions imposed by its DOE financing arrangements.

### Risk Factors

1. **Business-Related Risks**
   - Operating as an early-stage growth company with a history of losses and expectations of continuing losses in the near and medium term.
   - Heavy dependence on EV adoption and demand, as well as OEMs' ability to supply EVs to the market.
   - Challenges in managing rapid growth effectively.
   - Uncertainty created by current and future federal and state administrations regarding the EV sector.
   - Potential inaccuracy of market opportunity estimates and growth forecasts.
   - Significant competition in the EV charging market.
   - Reliance on a limited number of vendors for charging equipment and support services.
   - Dependence on a limited number of customers and OEM partners.
   - Supply chain disruptions.
   - Need for additional funding that may not be available on favorable terms.

2. **DOE Loan-Related Risks**
   - Substantial dependence on the ability to fully draw on the DOE Loan, which has multiple conditions precedent.
   - Risk of default if unable to comply with loan covenants.
   - Substantial assets pledged as collateral, limiting availability for additional secured debt.
   - Operational restrictions imposed on subsidiaries under the loan terms.
   - Limitations on cash distributions from subsidiaries needed to fund operations.

3. **EV Market Risks**
   - Changes to fuel economy standards or success of alternative fuels negatively impacting EV demand.
   - Slower-than-expected electrification of rideshare and commercial fleets.
   - Reduction or elimination of government rebates, tax credits, and financial incentives.

## Audited (Exec Summary + Outlook)

### Executive Summary
EVgo operates a public fast-charging network for electric vehicles and, despite generating $403 million in revenue, has yet to achieve profitability, carrying a net loss of -$54.1 million and a negative profit margin of -13.5%. The stock is notable now because it trades at $1.36—down 74% from its 52-week high of $5.18—placing it at a critical juncture where the gap between its current valuation and its growth ambitions is unusually wide, and where the company's $210.7 million in cash and equivalents provides only a finite runway to prove its model. The single most important near-term variable is whether EVgo can successfully draw on its DOE Loan facilities under the required conditions, as failure to do so would materially compress its ability to scale and accelerate the path to cash flow positivity.

### Outlook
The directional outlook for EVgo is **cautious**, with the investment thesis hinging on a narrow set of variables that could swing materially in either direction. On the tailwind side, continued broad EV adoption, stable or expanding federal and state incentive programs, and the successful electrification of rideshare and commercial fleets would all strengthen network utilization and improve the path toward profitability. On the headwind side, the risks are substantial and immediate: the DOE Loan draw conditions represent a structural dependency that, if unmet, could constrain capital precisely when the company needs it most; any rollback of government EV incentives under shifting federal or state administrations would suppress consumer demand; and intensifying competition from both established charging networks and alternative fuel technologies could erode EVgo's market position before it achieves scale. Investors should watch the pace and conditions of DOE Loan draws, the trajectory of the company's loss reduction relative to its cash position, the health of its OEM partnerships, and any regulatory signals affecting EV incentives. The cautious lean would shift toward constructive if EVgo demonstrates consistent progress in narrowing losses, successfully accesses its DOE financing without covenant stress, and EV adoption trends remain durable — but deterioration in any one of these areas, particularly the financing access or the regulatory environment, would deepen the concern.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "generating $403 million in revenue"
LABEL: SUPPORTED
REASON: The source data shows revenue of $402,948,000, which rounds to $403 million; the pre-written sections also state "$403 million in revenue."

---

CLAIM: "net loss of -$54.1 million"
LABEL: SUPPORTED
REASON: The source data shows net_income of -$54,125,000, which rounds to -$54.1 million; confirmed in pre-written sections.

---

CLAIM: "negative profit margin of -13.5%"
LABEL: SUPPORTED
REASON: The source data shows profit_margin of -0.13502, which is -13.502%, rounding to -13.5%; confirmed in pre-written sections.

---

CLAIM: "trades at $1.36"
LABEL: SUPPORTED
REASON: The source data explicitly states current_price of 1.36 USD.

---

CLAIM: "down 74% from its 52-week high of $5.18"
LABEL: SUPPORTED
REASON: The 52-week high of $5.18 is present in source data. Computed decline: (5.18 − 1.36) / 5.18 = 3.82 / 5.18 = 73.75%, which rounds to 74%; arithmetic check passes within 0.15 percentage points.

---

CLAIM: "52-week high of $5.18"
LABEL: SUPPORTED
REASON: The source data explicitly states week_52_high: 5.18.

---

CLAIM: "$210.7 million in cash and equivalents"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "the company had $210.7 million in cash, cash equivalents, and restricted cash" as of December 31, 2025; also confirmed in the pre-written SEC Filing Highlights section.

---

**OUTLOOK**

The Outlook section is largely qualitative and directional. I will identify every specific quantitative or named-milestone claim embedded within it.

---

CLAIM: (No specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section.)
LABEL: N/A
REASON: The Outlook section contains only qualitative directional statements, named risk categories (DOE Loan draw conditions, government EV incentives, OEM partnerships, regulatory signals), and conditional language — none of which constitute specific quantitative or measurable claims requiring arithmetic verification. All named risk categories (DOE Loan conditions, EV incentive rollback, OEM partnerships, competition, rideshare/commercial fleet electrification) are grounded in the RAG Risk Factors and SEC Filing Highlights sections and do not assert specific figures.

---

**SUMMARY TABLE**

| Claim | Label |
|---|---|
| $403 million in revenue | SUPPORTED |
| Net loss of -$54.1 million | SUPPORTED |
| Negative profit margin of -13.5% | SUPPORTED |
| Trades at $1.36 | SUPPORTED |
| Down 74% from 52-week high | SUPPORTED |
| 52-week high of $5.18 | SUPPORTED |
| $210.7 million in cash and equivalents | SUPPORTED |

All auditable quantitative claims in the Executive Summary are supported. The Outlook section contains no specific quantitative claims requiring verification.
