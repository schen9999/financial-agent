# EVGO — baseline

## Metadata

ticker: EVGO
arm: baseline
judge_prompt_version: v2
context_sha256: dce8cfe0379b43d5d7aed1a5b95cc873fbb0f5fadcbfd628dc6d68d1284ba66f

## Retrieved source context

STOCK DATA:
{
  "ticker": "EVGO",
  "company_name": "EVgo, Inc.",
  "current_price": 1.33,
  "currency": "USD",
  "market_cap": 418305920.0,
  "forward_pe": -3.0227275,
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

## Financial Position
- As of December 31, 2025, the company had $210.7 million in cash, cash equivalents, and restricted cash, with $161.2 million in working capital
- The company has a history of operating losses and negative operating cash flows
- Management expects to incur significant expenses and continuing losses in the near- and medium-term

## Business Model Dependencies
- Growth is highly correlated with EV adoption rates and OEMs' ability to supply electric vehicles to the market
- The company has experienced rapid growth recently but faces challenges in managing this expansion effectively
- Success depends heavily on relationships with automotive OEM and fleet partners

## Funding and Capital
- The company relies substantially on its ability to fully draw down a Department of Energy (DOE) Loan, which contains multiple conditions precedent
- The DOE Loan is secured by a substantial portion of consolidated assets
- Additional financing may be needed, though there is no assurance it will be available on favorable terms

## Market and Competitive Risks
- The company faces significant competition in the EV charging market
- Market growth estimates may prove inaccurate
- EV market development depends on numerous factors including consumer perception, government incentives, fuel prices, and EV model availability
- Automotive industry cyclicality may impact EV adoption, particularly among commercial fleet operators

## Operational Challenges
- Supply chain disruptions could materially affect operations
- Dependence on a limited number of vendors and customers creates vulnerability
- Construction risks, cost overruns, and installation delays are ongoing concerns

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
- Potential need for additional funding on potentially unfavorable terms

## DOE Loan-Related Risks
- Substantial dependence on the ability to fully draw on the DOE Loan, which has multiple conditions precedent
- Risk of default if unable to comply with DOE Loan covenants
- Significant assets pledged as collateral, limiting availability for additional secured debt
- Operational restrictions imposed on subsidiaries under the loan
- Restrictions on cash distributions from subsidiaries needed to fund operations

## EV Market Risks
- Changes to fuel economy standards or success of alternative fuels
- Slower-than-expected electrification of rideshare and commercial fleets
- Uncertainty regarding medium and heavy-duty vehicle segment development

## Other Risks
- Technology, intellectual property protection and enforcement challenges
- Lack of industry standards and transition to NACS charging standard
- Material weaknesses in internal controls over financial reporting
- Tax law changes and exposure to additional tax liabilities
- Inflationary pressures affecting equipment and operating costs

## Pre-written sections (judge input)

### Financial Health

EVgo is in a precarious financial position with a stock price of $1.33 and a market capitalization of $418.3 million, down significantly from its 52-week high of $5.18. The company is unprofitable with a negative profit margin of -13.5% and net losses of $54.1 million against revenue of $402.9 million, indicating substantial operational challenges. The negative forward P/E ratio reflects ongoing losses and investor concerns about the company's path to profitability. SEC filings highlight material risk factors that could further adversely affect the business and stock price. EVgo's financial metrics suggest elevated investment risk, particularly for conservative investors, though the company's position in the growing EV charging infrastructure sector presents potential upside if operational efficiency improves.

### Recent Developments

EVgo's latest SEC filings reveal persistent operational challenges, with the company reporting a negative profit margin of -13.5% and net losses of $54.1 million against $403 million in revenue. The stock has declined significantly from its 52-week high of $5.18 to $1.33, reflecting investor concerns about the company's path to profitability in the competitive EV charging market. Recent 10-Q and 10-K filings emphasize multiple risk factors that could materially adversely affect the business, with no material improvements noted in the risk profile between filings. For investors, EVgo's current valuation and negative earnings suggest the company remains in a critical growth phase where execution on profitability and market expansion will be essential to justify investment risk.

### SEC Filing Highlights

EVgo maintains a solid cash position of $210.7 million as of December 31, 2025, but continues to operate at a loss with negative operating cash flows, expecting significant near-term expenses. The company's growth trajectory is heavily dependent on EV adoption rates and OEM vehicle supply, creating exposure to automotive industry cyclicality and market development uncertainties. A critical funding dependency exists on the Department of Energy Loan, which is secured by substantial consolidated assets and contains multiple conditions precedent that must be satisfied. Operationally, EVgo faces supply chain vulnerabilities, vendor concentration risks, and construction-related delays that could materially impact expansion efforts. Success hinges on maintaining strong relationships with automotive OEM and fleet partners while navigating intense competitive pressures in the rapidly evolving EV charging market.

### Risk Factors

- **Dependence on DOE Loan and Continued Funding**: EVgo relies heavily on its ability to fully draw down a Department of Energy loan with multiple conditions precedent. Failure to meet covenants or draw conditions could force the company to seek additional funding on unfavorable terms, while significant pledged collateral limits flexibility for other financing needs.

- **EV Market Adoption Uncertainty**: The company's growth depends on sustained EV adoption rates and OEM supply capabilities. Slower-than-expected electrification of commercial fleets, changes to fuel economy standards, or shifts toward alternative fuels could materially reduce demand for charging infrastructure.

- **Path to Profitability and Operating Losses**: As an early-stage growth company with a history of operating losses, EVgo expects continued losses in the near to medium-term. The company faces intense competition in the EV charging market while managing rapid growth, construction risks, and supply chain disruptions—all of which could delay or prevent achieving profitability.

## Audited (Exec Summary + Outlook)

### Executive Summary
EVgo is a public EV fast-charging network operator competing in the rapidly evolving charging infrastructure sector, currently generating $402.9 million in revenue against a market capitalization of $418.3 million — a valuation that offers little premium over annual sales and reflects deep skepticism about the company's profitability trajectory. The stock is notable now precisely because of that skepticism: trading at $1.33, down sharply from its 52-week high of $5.18, EVgo sits at an inflection point where the gap between its infrastructure buildout ambitions and its financial reality is most acute. The single most important near-term variable is whether EVgo can satisfy the conditions precedent on its Department of Energy loan and convert that funding into network expansion without triggering covenant failures or requiring dilutive secondary financing.

### Outlook
The directional lean on EVgo is **cautious**, with the thesis hinging on a narrow set of variables that remain largely outside the company's direct control. On the tailwind side, secular growth in EV adoption, the strategic importance of fast-charging infrastructure, and EVgo's existing OEM and fleet partnerships provide a credible long-term demand backdrop. However, the headwinds are immediate and material: negative operating cash flows, an unresolved DOE loan draw process with meaningful conditions precedent, supply chain and construction execution risks, and a competitive market where better-capitalized rivals can absorb losses longer. Investors should watch the pace and success of DOE loan drawdowns as the clearest near-term signal of financial stability; any disruption there would likely force dilutive financing given the current cash runway. Beyond funding, the key variables to monitor are the trajectory of operating losses quarter-over-quarter, the rate of EV adoption among commercial fleets, and whether OEM partnerships translate into measurable throughput growth at existing stations. The cautious view would shift toward constructive if EVgo demonstrates consistent improvement in its loss profile, successfully draws on DOE funding without covenant stress, and shows that utilization rates across its network are trending meaningfully higher — none of which are yet in evidence from the current filings.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$402.9 million in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $402,948,000, which rounds to $402.9 million; the Financial Health and Recent Developments pre-written sections also state this figure.

---

CLAIM: "market capitalization of $418.3 million"
LABEL: SUPPORTED
REASON: Source data shows market_cap of $418,305,920, which rounds to $418.3 million; confirmed in the Financial Health pre-written section.

---

CLAIM: "trading at $1.33"
LABEL: SUPPORTED
REASON: Source data explicitly states current_price = 1.33 USD.

---

CLAIM: "down sharply from its 52-week high of $5.18"
LABEL: SUPPORTED
REASON: Source data explicitly states week_52_high = 5.18; the directional claim ("down sharply") is arithmetically verified: $1.33 is approximately 74% below $5.18.

---

CLAIM: "EVgo sits at an inflection point where the gap between its infrastructure buildout ambitions and its financial reality is most acute"
LABEL: INFERENCE
REASON: This is a qualitative characterization derived from the combination of the large stock price decline from 52-week high, ongoing net losses, and DOE loan dependency — all facts present in the source data — but the specific framing ("inflection point," "most acute") is an editorial inference rather than a directly stated fact.

---

CLAIM: "conditions precedent on its Department of Energy loan"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors sections explicitly state the DOE Loan "contains multiple conditions precedent."

---

**OUTLOOK**

---

CLAIM: "negative operating cash flows"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "the company has a history of operating losses and negative operating cash flows."

---

CLAIM: "unresolved DOE loan draw process with meaningful conditions precedent"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors sections explicitly state the company "relies substantially on its ability to fully draw down a Department of Energy (DOE) Loan, which contains multiple conditions precedent."

---

CLAIM: "current cash runway"
LABEL: INFERENCE
REASON: The source data states $210.7 million in cash as of December 31, 2025, and net losses of $54.1 million, from which a cash runway figure could be inferred directionally; however, no explicit "cash runway" figure or duration is stated in the source, making this a qualitative inference from present figures rather than an unsupported invented number.

---

CLAIM: "trajectory of operating losses quarter-over-quarter"
LABEL: SUPPORTED
REASON: The source data and SEC filing summaries confirm ongoing operating losses; monitoring their trajectory is a forward-looking watch item grounded in the confirmed existence of those losses — no specific figure is asserted.

---

CLAIM: "none of which are yet in evidence from the current filings"
LABEL: SUPPORTED
REASON: The SEC filing summaries and RAG sections confirm no material improvements in risk profile between filings, ongoing losses, and no evidence of successful DOE drawdowns or improved utilization rates in the provided source data.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | $402.9 million in revenue | SUPPORTED |
| 2 | Market capitalization of $418.3 million | SUPPORTED |
| 3 | Trading at $1.33 | SUPPORTED |
| 4 | Down sharply from 52-week high of $5.18 | SUPPORTED |
| 5 | Inflection point / gap most acute (qualitative) | INFERENCE |
| 6 | Conditions precedent on DOE loan | SUPPORTED |
| 7 | Negative operating cash flows | SUPPORTED |
| 8 | DOE loan draw process with meaningful conditions precedent | SUPPORTED |
| 9 | Current cash runway | INFERENCE |
| 10 | Trajectory of operating losses quarter-over-quarter | SUPPORTED |
| 11 | None of which are yet in evidence from current filings | SUPPORTED |

No quantitative claims in the Executive Summary or Outlook are UNSUPPORTED. All specific numeric figures ($402.9M revenue, $418.3M market cap, $1.33 price, $5.18 52-week high) are directly verified against the source data. The two INFERENCE labels apply to qualitative editorial characterizations that are derivable from but not explicitly stated in the source.
