# EVGO — baseline

## Metadata

ticker: EVGO
arm: baseline
judge_prompt_version: v2
context_sha256: 46f4a1edb03bd40e5ab8b542164bbb4258aa5aa6170c1bda731d99ff86da6965

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
- Future profitability depends on successful execution of growth plans and continued EV adoption

## Critical Dependencies
- **EV Market Growth**: The company's success is heavily dependent on continued EV adoption by consumers, fleet operators, and governments, as well as OEMs' ability to supply EVs
- **DOE Loan**: Business growth is substantially dependent on the ability to fully draw down on a Department of Energy loan, which has multiple conditions precedent
- **Limited Customer Base**: The company currently relies on a limited number of customers and OEM partners, creating concentration risk

## Key Business Challenges
- Rapid growth management and execution risks
- Supply chain disruptions and vendor dependencies
- Intense competition in the EV charging market
- Uncertainty from changing federal and state policies affecting the EV sector
- Market adoption risks, including potential slower-than-expected EV growth and shifts in charging preferences

## Market Uncertainties
- EV market development remains uncertain and subject to macroeconomic factors, regulatory changes, and consumer preferences
- Automotive industry cyclicality may impact EV adoption rates, particularly among commercial fleet operators

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several categories of primary risk factors:

## Business-Related Risks
- Operating as an early-stage growth company with a history of operating losses and expectations of continuing losses in the near and medium-term
- Heavy dependence on continuing EV adoption and demand, as well as OEMs' ability to supply EVs to the market
- Challenges in managing rapid growth effectively
- Uncertainty created by current and future federal and state administrations regarding the EV sector
- Potential inaccuracy of market opportunity estimates and growth forecasts
- Significant competition in the EV charging market
- Reliance on a limited number of vendors for charging equipment and support services
- Dependence on a limited number of customers and OEM partners
- Construction risks, cost overruns, and installation delays
- Supply chain disruptions
- Potential need for additional funding that may not be available on favorable terms

## DOE Loan-Related Risks
- Substantial dependence on the ability to fully draw on the DOE Loan, which has multiple conditions precedent
- Risk of default if unable to comply with DOE Loan covenants
- Substantial assets pledged as collateral, limiting availability for additional secured debt
- Operational restrictions imposed on subsidiaries under the loan
- Restrictions on cash distributions from subsidiaries needed to fund operations

## EV Market Risks
- Changes to fuel economy standards or success of alternative fuels negatively impacting EV demand
- Slower-than-expected electrification of rideshare and commercial fleets
- Reduction or elimination of government rebates, tax credits, and financial incentives

## Other Risks
- Technology, intellectual property, and infrastructure protection challenges
- Lack of industry standards and transition to NACS charging standard
- Material weaknesses in internal controls over financial reporting
- Tax law changes and inflationary pressures affecting costs
- Governance structure risks related to the company's "Up-C" structure

## Pre-written sections (judge input)

### Financial Health

EVgo is in a precarious financial position with a stock price of $1.36 and market capitalization of $428 million, down significantly from its 52-week high of $5.18. The company is unprofitable with a negative profit margin of -13.5% and net losses of $54.1 million against revenue of $403 million, indicating substantial operational challenges. The negative forward P/E ratio reflects ongoing losses and investor concerns about the company's path to profitability. SEC filings highlight material risk factors that could further adversely affect the business and stock price. This early-stage EV charging infrastructure company requires significant capital deployment and operational improvements before achieving sustainable profitability.

### Recent Developments

EVgo's latest SEC filings reveal ongoing operational challenges, with the company continuing to face significant risk factors that could materially impact its business and financial performance. The most recent 10-Q filing (August 2026) indicates no material changes to previously disclosed risks, suggesting persistent headwinds in the EV charging market. With a negative profit margin of -13.5% and net losses of $54.1 million against $403 million in revenue, EVgo remains unprofitable despite operating in the growing EV infrastructure sector. The stock's 74% decline from its 52-week high of $5.18 to the current $1.36 reflects investor concerns about the company's path to profitability and competitive positioning in the rapidly evolving charging network landscape.

### SEC Filing Highlights

EVgo reported $210.7 million in cash and cash equivalents as of December 31, 2025, with $161.2 million in working capital, though the company continues to operate at a loss and expects significant near-term expenses. The company's growth trajectory is heavily dependent on three critical factors: sustained EV market adoption, successful drawdown of its Department of Energy loan (subject to multiple conditions), and execution of its expansion strategy. EVgo faces material risks including customer concentration, intense competitive pressures in the EV charging market, supply chain vulnerabilities, and sensitivity to regulatory and macroeconomic shifts affecting EV adoption rates. The company acknowledges that future profitability remains contingent on scaling operations while managing rapid growth execution risks in an uncertain EV market environment.

### Risk Factors

- **Dependence on DOE Loan and Continued Funding**: EVgo relies heavily on drawing the full amount of its Department of Energy loan, which carries multiple conditions precedent and strict covenants. Failure to comply could trigger default, and the company may require additional capital on unfavorable terms to fund operations and growth.

- **EV Market and Policy Uncertainty**: Demand for EV charging depends on sustained EV adoption, government incentives, and favorable regulatory policies. Reductions in tax credits, changes in fuel economy standards, or shifts in administration priorities could significantly impact market growth and the company's revenue trajectory.

- **Operational Losses and Path to Profitability**: EVgo is an early-stage growth company with a history of operating losses and expectations of continuing losses in the near to medium-term, creating uncertainty about the company's ability to achieve sustainable profitability.

## Audited (Exec Summary + Outlook)

### Executive Summary
EVgo is an early-stage EV charging infrastructure company generating $403 million in revenue, yet trading at $1.36 per share with a market capitalization of $428 million — a level that reflects the market's deep skepticism about its path to profitability given net losses of $54.1 million and a negative profit margin of -13.5%. The stock's 74% decline from its 52-week high of $5.18 has brought it to a level where the risk-reward calculus is dominated less by growth potential and more by survival and funding questions, making this a high-risk, speculative situation rather than a conventional growth investment. The single most important near-term variable is whether EVgo can successfully satisfy the conditions required to draw down its Department of Energy loan, as failure to do so would materially impair the company's ability to fund operations and execute its expansion strategy.

### Outlook
The directional lean on EVgo is **cautious**. The structural tailwind of long-term EV adoption remains intact, and the company does operate at meaningful scale, but the near-term investment thesis is burdened by compounding headwinds that are difficult to dismiss. Investors should monitor the DOE loan drawdown process closely — successful, uninterrupted access to that facility would meaningfully reduce near-term liquidity risk, while any covenant breach or delay would likely accelerate concerns about the company's ability to self-fund operations. Beyond funding, the key variables to watch are the trajectory of EV adoption rates and the durability of federal and state policy support, including tax credits and fuel economy standards, as any rollback would directly compress the addressable market and weaken EVgo's revenue outlook. Competitive dynamics in the charging network landscape also warrant attention, particularly whether EVgo can defend or grow its network utilization against well-capitalized rivals. The path to a more constructive view would require visible progress toward narrowing operating losses, clean execution of the expansion strategy, and a stable or improving policy environment for EVs — none of which appear sufficiently certain at this stage to offset the material risks the company has itself disclosed.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "generating $403 million in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $402,948,000, which rounds to $403 million; the pre-written sections also state "$403 million in revenue."

---

CLAIM: "trading at $1.36 per share"
LABEL: SUPPORTED
REASON: Source data explicitly lists current_price as 1.36 USD.

---

CLAIM: "market capitalization of $428 million"
LABEL: SUPPORTED
REASON: Source data shows market_cap of $427,741,376, which rounds to $428 million; the pre-written Financial Health section also states "$428 million."

---

CLAIM: "net losses of $54.1 million"
LABEL: SUPPORTED
REASON: Source data shows net_income of -$54,125,000, which rounds to -$54.1 million; confirmed in pre-written sections.

---

CLAIM: "negative profit margin of -13.5%"
LABEL: SUPPORTED
REASON: Source data lists profit_margin as -0.13502, which equals -13.502%, rounding to -13.5%; recomputed: -54,125,000 / 402,948,000 = -13.43%, within 0.15 pp of -13.5% (difference is ~0.07 pp). SUPPORTED.

---

CLAIM: "74% decline from its 52-week high of $5.18"
LABEL: SUPPORTED
REASON: 52-week high of $5.18 is in source data; decline = (5.18 − 1.36) / 5.18 = 3.82 / 5.18 = 73.75%, which rounds to 74%; pre-written Recent Developments section also states "74% decline." SUPPORTED.

---

CLAIM: "52-week high of $5.18"
LABEL: SUPPORTED
REASON: Source data explicitly lists week_52_high as 5.18.

---

**OUTLOOK**

---

CLAIM: (no specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section)
LABEL: N/A
REASON: The Outlook section is entirely qualitative and directional — it references the DOE loan, EV adoption, tax credits, fuel economy standards, competitive dynamics, and operating losses, but does not assert any specific numerical figures, percentages, price targets, or measurable thresholds that require verification against source data. No auditable quantitative claims are present.

---

**SUMMARY TABLE**

| Claim | Label |
|---|---|
| $403 million in revenue | SUPPORTED |
| $1.36 per share | SUPPORTED |
| Market cap of $428 million | SUPPORTED |
| Net losses of $54.1 million | SUPPORTED |
| Profit margin of -13.5% | SUPPORTED |
| 74% decline from 52-week high | SUPPORTED |
| 52-week high of $5.18 | SUPPORTED |

All quantitative claims in the Executive Summary are supported by the source data. The Outlook section contains no auditable quantitative claims.
