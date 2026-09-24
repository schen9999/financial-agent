# EVGO — baseline

## Metadata

ticker: EVGO
arm: baseline
judge_prompt_version: v2
context_sha256: a4f3cb808491d7edba4283d36c1a6e09429ed11df3ee5d8f859d80160f80ce9e

## Retrieved source context

STOCK DATA:
{
  "ticker": "EVGO",
  "company_name": "EVgo, Inc.",
  "current_price": 1.51,
  "currency": "USD",
  "market_cap": 474918720.0,
  "forward_pe": -3.4318182,
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

## Financial Position and Challenges
- The company has a history of operating losses and expects to continue incurring significant expenses and losses in the near to medium term
- As of December 31, 2025, the company had $210.7 million in cash, cash equivalents, and restricted cash, with $161.2 million in working capital
- Future profitability depends on continued EV adoption, regulatory support, and customer usage of their chargers

## Critical Dependencies
- **EV Market Growth**: The company's success is heavily dependent on continued EV adoption by consumers, businesses, and governments, which remains uncertain
- **DOE Loan**: Business growth is substantially dependent on the ability to fully draw down a Department of Energy loan, which has multiple conditions precedent
- **Limited Customer Base**: The company currently relies on a limited number of customers and OEM partners, creating concentration risk

## Operational Risks
- Supply chain disruptions could materially harm operations
- Rapid growth management challenges
- Construction delays and cost overruns associated with network expansion
- Dependence on a limited number of vendors for charging equipment

## Market Uncertainties
- EV market adoption rates remain uncertain and could develop more slowly than expected
- Macroeconomic factors and automotive industry cyclicality could impact EV demand
- Government policy changes at federal and state levels create sector uncertainty
- Competition from alternative fuel vehicles and charging methods

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several categories of primary risk factors:

## Business-Related Risks
- Operating as an early-stage growth company with a history of operating losses and expectations of continuing losses in the near and medium-term
- Heavy dependence on continuing EV adoption and demand, as well as OEMs' ability to supply EVs to the market
- Challenges in managing rapid growth effectively
- Uncertainty created by current and future federal and state administrations regarding the EV sector
- Potential inaccuracy of market opportunity estimates and growth forecasts
- Significant current and future competition in the EV charging market
- Reliance on a limited number of vendors for charging equipment and support services
- Dependence on a limited number of customers and OEM partners
- Construction risks, cost overruns, and installation delays
- Supply chain disruptions
- Potential need for additional funding that may not be available or may come on unfavorable terms

## DOE Loan-Related Risks
- Dependence on the ability to fully draw on the DOE Loan, which has multiple conditions precedent
- Risk of default if unable to comply with loan covenants
- Substantial assets pledged as collateral, limiting availability for additional secured debt
- Operational restrictions imposed on subsidiaries under the loan
- Restrictions on cash distributions from subsidiaries needed to fund operations

## EV Market Risks
- Changes to fuel economy standards or success of alternative fuels negatively impacting EV demand
- Slower-than-expected electrification of rideshare and commercial fleets
- Delayed development of medium and heavy-duty battery EV segments
- Reduction or elimination of government rebates, tax credits, and financial incentives

## Other Risks
- Technology, intellectual property protection, and infrastructure challenges
- Lack of industry standards and transition to NACS charging standard
- Material weaknesses in internal controls over financial reporting
- Tax law changes and additional tax liabilities
- Inflationary pressures affecting equipment and operating costs

## Pre-written sections (judge input)

### Financial Health

EVgo is in a precarious financial position with a market capitalization of $475 million and a stock price of $1.51, down significantly from its 52-week high of $5.18. The company generated $403 million in revenue but posted a net loss of $54 million, resulting in a negative 13.5% profit margin, indicating the company is not yet profitable. The forward P/E ratio of -3.43 reflects ongoing losses and investor concerns about the path to profitability. SEC filings highlight material business risks that could further impact financial performance and stock value. As an early-stage EV charging infrastructure player, EVgo requires continued capital investment and faces execution risks in a competitive market.

### Recent Developments

EVgo's latest SEC filings reveal no material changes to previously disclosed risk factors, suggesting operational stability in the near term. However, the company continues to face significant headwinds, with a negative profit margin of -13.5% and net losses of $54.1 million against $403 million in revenue, indicating the company remains unprofitable. The stock has declined substantially from its 52-week high of $5.18 to $1.51, reflecting investor concerns about the company's path to profitability in a competitive EV charging market. Investors should monitor upcoming quarterly results closely for signs of margin improvement and network utilization metrics that could validate the long-term investment thesis.

### SEC Filing Highlights

EVgo faces significant near-term profitability challenges, with a history of operating losses expected to continue as the company scales its charging network, though it maintains a solid cash position of $210.7 million as of December 31, 2025. The company's growth trajectory is heavily dependent on three critical factors: sustained EV market adoption, successful drawdown of its Department of Energy loan (subject to multiple conditions), and expansion of its limited customer base to reduce concentration risk. Operational execution risks include supply chain vulnerabilities, construction delays, and vendor dependencies that could materially impact network expansion. Market uncertainties around EV adoption rates, macroeconomic conditions, and potential shifts in government policy at federal and state levels present headwinds to the company's long-term strategy. Success ultimately hinges on EVgo's ability to capitalize on secular EV growth trends while managing capital efficiently and diversifying its customer base.

### Risk Factors

• **Continued Operating Losses and Funding Dependency** – EVgo operates as an early-stage growth company with a history of operating losses and expectations of continuing losses in the near and medium-term, with substantial dependence on the ability to fully draw on its DOE loan facility, which carries multiple conditions precedent and default risks if covenants are not met.

• **EV Market and Demand Uncertainty** – The company's success is heavily dependent on continued EV adoption and OEM supply, with material risks from potential reductions in government incentives, slower-than-expected fleet electrification, and policy uncertainty across different administrations.

• **Intense Competition and Vendor Concentration** – EVgo faces significant competition in the EV charging market while relying on a limited number of vendors for equipment and support services, and depends on a limited customer and OEM partner base, creating vulnerability to market consolidation and supply chain disruptions.

## Audited (Exec Summary + Outlook)

### Executive Summary
EVgo is an early-stage EV charging infrastructure company that generated $403 million in revenue while operating at a net loss of $54 million, positioning it as a growth-oriented but not yet profitable player in the rapidly evolving public fast-charging market. The stock is notable now precisely because of the tension between its long-term secular tailwind — rising EV adoption — and a share price that has fallen from a 52-week high of $5.18 to $1.51, reflecting deep investor skepticism about the timeline and conditions required to reach profitability. The single most important near-term variable is whether EVgo can successfully satisfy the conditions precedent to draw on its DOE loan facility, as that funding is central to the network expansion and capital efficiency that underpin the entire investment thesis.

### Outlook
The directional outlook for EVgo is **cautious**, with the balance of near-term risks outweighing the long-term secular opportunity until clearer evidence of operational progress emerges. On the tailwind side, secular EV adoption remains the foundational thesis, and EVgo's existing network and OEM relationships provide a platform that would be difficult to replicate quickly; a stable or improving policy environment at the federal and state level could meaningfully accelerate utilization and reduce funding uncertainty. On the headwind side, the path to profitability remains undefined, the DOE loan drawdown is subject to conditions that have not yet been fully satisfied, and the company's customer concentration leaves it exposed to demand shocks from a small number of partners. Investors should watch four key variables: the trajectory of network utilization and gross margin in successive quarterly results, the status and progress of DOE loan covenant compliance and drawdown milestones, any shifts in federal or state EV incentive policy that could alter demand curves, and whether the company demonstrates meaningful progress in broadening its customer and OEM partner base. The thesis would strengthen if quarterly results show consistent margin improvement alongside accelerating network utilization, and if the DOE loan advances toward full drawdown without covenant complications. Conversely, any covenant breach, a sustained deceleration in EV adoption, or a further deterioration in the competitive landscape would materially weaken the case for holding the stock at current levels.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "generated $403 million in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $402,948,000, which rounds to $403 million; the pre-written Financial Health and Recent Developments sections also state "$403 million in revenue."

---

CLAIM: "operating at a net loss of $54 million"
LABEL: SUPPORTED
REASON: Source data shows net_income of -$54,125,000, which rounds to -$54 million; confirmed in pre-written sections.

---

CLAIM: "share price that has fallen from a 52-week high of $5.18"
LABEL: SUPPORTED
REASON: Source data explicitly lists week_52_high as 5.18.

---

CLAIM: "to $1.51"
LABEL: SUPPORTED
REASON: Source data explicitly lists current_price as 1.51.

---

**OUTLOOK**

---

CLAIM: (no specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section)
LABEL: N/A
REASON: The Outlook section is entirely qualitative and directional — it references no specific numbers, percentages, ratios, price targets, or dated milestones. All claims are narrative characterizations (e.g., "cautious," "conditions precedent," "covenant compliance") that do not constitute quantitative or forward-looking numerical claims subject to audit under the defined criteria. No entries are required.
