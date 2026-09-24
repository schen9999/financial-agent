# EVGO — local-model

## Metadata

ticker: EVGO
arm: local-model
judge_prompt_version: v2
context_sha256: a3a0c595cef2055e36382f120bfd02af0b1999473febfd8a4be320b9a0f84e2a
local_model_served_name: qwen2.5-7b-instruct
local_model_dir: qwen2.5-7b-instruct
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

## Financial Position and Challenges
- As of December 31, 2025, the company had $210.7 million in cash, cash equivalents, and restricted cash, with $161.2 million in working capital
- The company has a history of operating losses and negative operating cash flows, with expectations to continue incurring significant losses in the near and medium term
- Additional financing may be needed to fund ongoing operations

## Business Dependencies
- Growth is heavily dependent on continued EV adoption by consumers, businesses, and governments
- Success relies on OEMs' ability to supply EVs to the market and customers' willingness to use the company's charging network
- The company depends on a limited number of vendors for charging equipment and a limited number of customers and OEM partners

## Market and Operational Risks
- The EV market remains rapidly evolving with uncertain demand trajectories
- Competition is expected to intensify as the EV charging market develops
- Supply chain disruptions could materially impact operations
- Construction delays, cost overruns, and installation contingencies pose operational risks
- Rapid growth management presents challenges

## Critical Financing Risk
- The company's growth is substantially dependent on its ability to fully draw on a Department of Energy (DOE) Loan, which contains multiple conditions precedent
- The DOE Loan is secured by substantial consolidated assets, limiting flexibility for additional secured debt

## Regulatory and Market Uncertainties
- Federal and state policy changes regarding EVs create sector uncertainty
- Macroeconomic factors, automotive industry cyclicality, and fuel price volatility could impact EV demand
- Changes to fuel economy standards or alternative fuel success could negatively affect the market

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several categories of primary risk factors:

## Business-Related Risks
- Operating as an early-stage growth company with a history of losses and expectations of continuing losses in the near and medium-term
- Heavy dependence on EV adoption and demand, as well as OEMs' ability to supply EVs to the market
- Challenges in managing rapid growth effectively
- Uncertainty created by current and future federal and state administrations regarding the EV sector
- Potential inaccuracy of market opportunity estimates and growth forecasts
- Significant competition in the EV charging market
- Reliance on a limited number of vendors for charging equipment and support services
- Dependence on a limited number of customers and OEM partners
- Construction risks, cost overruns, and installation delays
- Supply chain disruptions
- Potential need to raise additional capital on potentially unfavorable terms

## DOE Loan-Related Risks
- Substantial dependence on the ability to fully draw on the DOE Loan, which has multiple conditions precedent
- Risk of default if covenants or terms are not complied with
- Substantial assets pledged as collateral, limiting availability for additional secured debt
- Operational restrictions imposed on subsidiaries
- Limitations on cash distributions from subsidiaries needed to fund operations

## EV Market Risks
- Changes to fuel economy standards or success of alternative fuels
- Slower-than-expected electrification of rideshare and commercial fleets
- Reduced reliance on public fast charging infrastructure

## Technology, Finance, and Governance Risks
- Inability to maintain and protect intellectual property
- Lack of industry standards and transition to NACS charging standard
- Material weaknesses in internal controls over financial reporting
- Tax law changes and inflationary pressures
- Controlled company structure and governance limitations

## Pre-written sections (judge input)

### Financial Health

EVgo, Inc. (EVGO) currently trades at $1.36 per share, with a market capitalization of approximately $427.74 million. The company has a forward P/E ratio of -3.09, indicating either significant losses or an unusual valuation metric. Revenue stands at $402,948,000, but with a net income loss of $54,125,000 and a negative profit margin of -13.5%, the financial health remains precarious. Investors should approach this stock with caution given its current financial performance and the numerous risks highlighted in recent filings.

### Recent Developments

EVgo's most recent SEC filings (10-K filed March 2026 and 10-Q filed August 2026) emphasize significant operational risks without material changes to previously disclosed risk factors, suggesting ongoing business challenges. The company continues to operate at a loss with a negative profit margin of -13.5% and net income of -$54.1 million, indicating the EV charging network operator has not yet achieved profitability despite $403 million in revenue. With the stock trading at $1.36—down 74% from its 52-week high of $5.18—investors should carefully evaluate whether EVgo can execute its growth strategy and reach positive cash flow before capital constraints become critical.

### SEC Filing Highlights

EVgo reported $210.7 million in cash and equivalents as of December 31, 2025, but continues to face significant operational challenges with a history of operating losses and negative cash flows, with expectations for continued losses in the near to medium term. The company's growth trajectory is heavily dependent on a Department of Energy loan with multiple conditions precedent, which is secured by substantial consolidated assets and limits additional financing flexibility. Key risks include dependence on a limited vendor base for charging equipment, reliance on OEM partners and consumer EV adoption rates, and exposure to supply chain disruptions and construction delays that could impact network expansion. The rapidly evolving EV market presents both opportunity and uncertainty, with intensifying competition and regulatory changes creating headwinds to demand forecasts. Management has flagged the need for additional financing to sustain operations and fund growth initiatives.

### Risk Factors

- **Heavy Dependence on EV Adoption**: Success is highly dependent on the continued growth and widespread adoption of electric vehicles.
- **Rapid Growth Management**: Managing rapid expansion while maintaining operational efficiency poses significant challenges.

## Audited (Exec Summary + Outlook)

### Executive Summary
EVgo, Inc. is a public fast-charging network operator for electric vehicles that has generated $402,948,000 in revenue while carrying a net loss of $54,125,000 and a negative profit margin of -13.5%, reflecting a business still in the investment phase of building out its charging infrastructure. The stock is notable now precisely because of the tension between its scale of revenue and its persistent unprofitability, with shares trading at $1.36 — down 74% from their 52-week high of $5.18 — signaling that the market has grown deeply skeptical of the path to profitability. The single most important near-term variable is whether EVgo can satisfy the conditions precedent on its Department of Energy loan and secure the additional financing management has flagged as necessary, as the answer to that question will determine whether the company has sufficient runway to reach positive cash flow.

### Outlook
The directional lean on EVgo is **cautious**. The primary tailwind remains the long-term secular shift toward electric vehicle adoption, which underpins demand for public fast-charging infrastructure and gives the business a credible reason to exist at scale. However, the headwinds are substantial and immediate: the company has explicitly guided for continued losses in the near to medium term, management has acknowledged the need for additional financing, and the Department of Energy loan — the central pillar of the growth plan — remains contingent on satisfying multiple unresolved conditions precedent. Investors should monitor the following variables closely: progress toward fulfilling the DOE loan conditions and any changes to that facility's terms; the pace and cost of network expansion relative to cash burn against the $210.7 million cash position reported at year-end 2025; the trajectory of the profit margin, watching for any narrowing of the -13.5% loss rate as a signal that unit economics are improving; the rate of broader EV adoption and any regulatory shifts that could accelerate or dampen consumer demand; and the competitive intensity of the fast-charging market, particularly from well-capitalized rivals. The cautious view would begin to shift toward neutral or constructive if EVgo successfully closes its DOE financing, demonstrates meaningful improvement in operating margins, and shows that network expansion is translating into improved utilization without proportional increases in losses. Conversely, the thesis would weaken materially if financing conditions deteriorate, cash reserves erode faster than anticipated, or EV adoption trends disappoint in ways that reduce throughput across the charging network.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$402,948,000 in revenue"
LABEL: SUPPORTED
REASON: The raw source data lists `"revenue": 402948000.0`, and the pre-written Financial Health and Recent Developments sections both confirm this figure.

---

CLAIM: "net loss of $54,125,000"
LABEL: SUPPORTED
REASON: The raw source data lists `"net_income": -54125000.0`, confirmed in the pre-written sections as "net income loss of -$54.1 million."

---

CLAIM: "negative profit margin of -13.5%"
LABEL: SUPPORTED
REASON: The raw source data lists `"profit_margin": -0.13502`; -54,125,000 / 402,948,000 = -0.13432, which rounds to -13.4%, but the source data explicitly states -0.13502 (≈ -13.5%), and the pre-written sections use -13.5%, so the claim matches the provided source figure within 0.15 pp.

---

CLAIM: "shares trading at $1.36"
LABEL: SUPPORTED
REASON: The raw source data lists `"current_price": 1.36`.

---

CLAIM: "down 74% from their 52-week high of $5.18"
LABEL: SUPPORTED
REASON: The 52-week high of $5.18 is present in the source data. The percentage decline: (5.18 − 1.36) / 5.18 = 3.82 / 5.18 = 73.75%, which rounds to 74%. Both the figure and the arithmetic check out; the pre-written Recent Developments section also states "down 74% from its 52-week high of $5.18."

---

**OUTLOOK**

---

CLAIM: "continued losses in the near to medium term"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state "expectations to continue incurring significant losses in the near and medium term," and the pre-written SEC Filing Highlights section repeats this language.

---

CLAIM: "management has acknowledged the need for additional financing"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state "Additional financing may be needed to fund ongoing operations," and the pre-written SEC Filing Highlights section states "Management has flagged the need for additional financing to sustain operations and fund growth initiatives."

---

CLAIM: "the Department of Energy loan — the central pillar of the growth plan — remains contingent on satisfying multiple unresolved conditions precedent"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors both state the company's growth is "substantially dependent on its ability to fully draw on a Department of Energy (DOE) Loan, which contains multiple conditions precedent"; the pre-written SEC Filing Highlights section confirms this language.

---

CLAIM: "$210.7 million cash position reported at year-end 2025"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state "As of December 31, 2025, the company had $210.7 million in cash, cash equivalents, and restricted cash," and the pre-written SEC Filing Highlights section repeats this figure and date.

---

CLAIM: "the -13.5% loss rate" (in the Outlook, as a watch-item threshold)
LABEL: SUPPORTED
REASON: This is a direct restatement of the profit margin figure already confirmed above (-0.13502 per source data, expressed as -13.5% in the pre-written sections and source data).

---

**Summary of findings:** All quantitative and forward-looking claims in the Executive Summary and Outlook are SUPPORTED by the source data or pre-written sections, and all derived figures (the 74% decline, the -13.5% margin) pass arithmetic verification within the specified tolerances. No claims were found to be UNSUPPORTED or INFERENCE.
