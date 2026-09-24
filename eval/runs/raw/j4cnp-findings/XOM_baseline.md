# XOM — baseline

## Metadata

ticker: XOM
arm: baseline
judge_prompt_version: v2
context_sha256: ea5c6a6916280bc5e4db6b367a249bb11073dccb7bd23f5374bd771e269dee3e

## Retrieved source context

STOCK DATA:
{
  "ticker": "XOM",
  "company_name": "ExxonMobil Holdings Corporation",
  "current_price": 159.47,
  "currency": "USD",
  "market_cap": 655726608384.0,
  "pe_ratio": 20.52381,
  "forward_pe": 14.787854,
  "week_52_high": 176.41,
  "week_52_low": 108.35,
  "revenue": 361060007936.0,
  "net_income": 32757000192.0,
  "profit_margin": 0.09072,
  "dividend_yield": 2.54,
  "sector": "Energy",
  "industry": "Oil & Gas Integrated"
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
    "message": "No 10-K found"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-03",
    "summary": "Item 1A. Risk Factors\" of ExxonMobil\u2019s 2025 Form 10-K. Forward-looking and other statements regarding environmental and other sustainability efforts and aspirations are not an indication that these statements are material to investors or require disclosure in our filing with the SEC or any other regulatory authority. In addition, historical, current, and forward-looking environmental and other sustainability-related statements may be based on standards for measuring progress that are still developing, internal controls and processes that continue to evolve, and assumptions that are subject to change in the future, including future rule-making. Actions needed to advance ExxonMobil\u2019s 2030 greenhouse gas emission-reductions plans are incorporated into its medium term business plans, which are"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] # Key Takeaways from ExxonMobil's Latest Filings

## Financial Performance
- **Upstream earnings** for the second quarter 2026 reached $7.9 billion, up from $5.4 billion in the same period of 2025
- Year-to-date upstream earnings totaled $13.7 billion compared to $12.2 billion in the prior year
- The company distributed $8.6 billion in dividends and repurchased $10.0 billion of common stock

## Production & Operations
- Oil-equivalent production decreased to 4,514 thousand barrels daily in Q2 2026 from 4,630 in Q2 2025
- Crude oil and liquids production reached 3,373 thousand barrels daily globally
- Natural gas production declined to 6,849 million cubic feet daily from 8,219 in the prior year quarter

## Earnings Drivers
- **Price impacts** added $4.65 billion in Q2 earnings from higher crude realizations, partially offset by lower gas prices
- **Advantaged volume growth** contributed $1.14 billion, primarily from Guyana and Permian expansion
- **Middle East disruptions** reduced earnings by $1.06 billion in the quarter
- **Structural cost savings** added $170 million
- **Expenses** decreased earnings by $690 million due to higher depreciation

## Strategic Outlook
- The company is incorporating greenhouse gas emission-reduction plans into medium-term business plans updated annually
- Future policy stringency and technology advancement will be incorporated into planning as they emerge
- Capital investment in lower-emission solutions is focused on returns and dependent on public policy support

RAG — RISK FACTORS:
[From Pinecone cache] Based on the provided context, the document references risk factors that are detailed in Item 1A of ExxonMobil's 2025 Form 10-K filing. However, the specific primary risk factors are not enumerated in the context information provided.

The context does mention that forward-looking statements regarding environmental and sustainability efforts are not necessarily indicative of material risks requiring SEC disclosure. It also notes that environmental and sustainability-related statements may be based on evolving standards, internal processes that continue to develop, and assumptions subject to change.

Additionally, the context indicates that actions to advance greenhouse gas emission-reduction plans are incorporated into medium-term business plans, and that current policy and technology trends are not yet on a pathway to achieve net-zero by 2050, which could represent a risk factor related to climate and energy transition.

To obtain a comprehensive list of the primary risk factors disclosed by the company, you would need to review the full Item 1A. Risk Factors section of the 2025 Form 10-K filing.

## Pre-written sections (judge input)

### Financial Health

ExxonMobil demonstrates solid financial fundamentals with a market capitalization of $655.7 billion and annual revenue of $361.1 billion, supported by a healthy 9.1% profit margin and net income of $32.8 billion. The current stock price of $159.47 USD reflects a trailing P/E ratio of 20.5x, though the forward P/E of 14.8x suggests more attractive valuation on an earnings basis. The company's 2.54% dividend yield provides income appeal for investors. While the stock trades near its 52-week high of $176.41, the valuation appears reasonable given the company's scale and profitability in the cyclical energy sector.

### Recent Developments

ExxonMobil's most recent 10-Q filing (August 3, 2026) highlights the company's ongoing integration of greenhouse gas emission-reduction targets into its medium-term business plans, with specific actions outlined to meet 2030 goals. The company acknowledges evolving sustainability measurement standards and internal processes, indicating a proactive approach to environmental compliance and investor expectations around ESG metrics. With a forward P/E of 14.79 and a solid 2.54% dividend yield, XOM appears reasonably valued relative to its earnings potential, though investors should monitor how capital allocation toward emissions reduction initiatives impacts future profitability and cash flow generation.

### SEC Filing Highlights

ExxonMobil reported strong upstream earnings of $7.9 billion in Q2 2026, up 46% year-over-year, driven primarily by higher crude oil realizations that added $4.65 billion in earnings despite production headwinds. The company returned $18.6 billion to shareholders through dividends and buybacks while maintaining disciplined capital allocation focused on advantaged projects like Guyana and Permian expansion, which contributed $1.14 billion in earnings growth. Production volumes declined modestly to 4,514 thousand barrels of oil-equivalent daily, with natural gas output particularly affected, though this was offset by strong pricing dynamics and structural cost improvements of $170 million. Middle East geopolitical disruptions reduced quarterly earnings by $1.06 billion, highlighting exposure to regional volatility. The company continues integrating greenhouse gas emission-reduction initiatives into its medium-term planning while emphasizing that lower-emission investments remain contingent on supportive public policy frameworks.

### Risk Factors

• **Energy Transition and Climate Policy Risk** – Regulatory pressures and global shifts toward renewable energy could impact long-term demand for fossil fuels and require significant capital reallocation to maintain competitiveness in a decarbonizing economy.

• **Commodity Price Volatility** – Fluctuations in crude oil and natural gas prices directly affect revenues and profitability, exposing the company to market cyclicality and geopolitical supply disruptions.

• **Regulatory and Environmental Compliance Risk** – Increasingly stringent environmental regulations, carbon pricing mechanisms, and sustainability mandates could increase operational costs and limit project development opportunities.

## Audited (Exec Summary + Outlook)

### Executive Summary
ExxonMobil is one of the world's largest integrated energy companies, generating $361.1 billion in annual revenue and $32.8 billion in net income, underpinned by a $655.7 billion market capitalization that reflects its dominant scale across upstream, downstream, and chemical operations. The stock is notable now because Q2 2026 upstream earnings surged 46% year-over-year, shareholder returns reached $18.6 billion in a single quarter, and the forward P/E of 14.8x offers a more attractive entry point than the trailing multiple suggests — all while the stock trades below its 52-week high of $176.41. The single most important near-term variable is crude oil price realization: as demonstrated in the most recent quarter, pricing dynamics were the primary driver of earnings strength, meaning any sustained reversal in crude prices would disproportionately pressure results given the modest production volume trends already in evidence.

### Outlook
The directional outlook for XOM is **cautiously constructive**, supported by several meaningful tailwinds: the company's advantaged growth projects in Guyana and the Permian continue to contribute incremental earnings, structural cost discipline is evident, and the forward valuation is more compelling than the trailing multiple implies. The 2.54% dividend yield and demonstrated commitment to shareholder returns further anchor the investment case for income-oriented investors. That said, the thesis carries real headwinds that warrant close monitoring. Crude oil price realization is the dominant swing factor — the Q2 2026 results illustrate how heavily earnings depend on pricing rather than volume growth, and any deterioration in the commodity environment would meaningfully pressure the bull case. Investors should also watch the trajectory of Middle East geopolitical risk, which has already demonstrated a material earnings impact, as well as the pace and cost of emissions-reduction capital allocation as ExxonMobil works toward its 2030 goals — particularly whether supportive public policy frameworks materialize to underwrite lower-emission investments. What would strengthen the thesis: sustained or improving crude realizations, volume recovery in natural gas, and policy clarity that makes lower-emission projects accretive rather than dilutive to returns. What would weaken it: a prolonged commodity downturn, escalating regional conflict disrupting operations, or an accelerating regulatory burden that compresses margins faster than cost efficiencies can offset.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

## EXECUTIVE SUMMARY

---

CLAIM: "$361.1 billion in annual revenue"
LABEL: SUPPORTED
REASON: Source data lists revenue as $361,060,007,936, which rounds to $361.1 billion; also confirmed in the Financial Health pre-written section.

---

CLAIM: "$32.8 billion in net income"
LABEL: SUPPORTED
REASON: Source data lists net_income as $32,757,000,192, which rounds to $32.8 billion; also confirmed in the Financial Health pre-written section.

---

CLAIM: "$655.7 billion market capitalization"
LABEL: SUPPORTED
REASON: Source data lists market_cap as $655,726,608,384, which rounds to $655.7 billion; confirmed in the Financial Health pre-written section.

---

CLAIM: "Q2 2026 upstream earnings surged 46% year-over-year"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states upstream earnings were $7.9 billion in Q2 2026 vs. $5.4 billion in Q2 2025; ($7.9B − $5.4B) / $5.4B = 46.3%, which rounds to 46% — within 0.15 pp of the stated figure; also confirmed in the SEC Filing Highlights pre-written section.

---

CLAIM: "shareholder returns reached $18.6 billion in a single quarter"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states the company distributed $8.6 billion in dividends and repurchased $10.0 billion of common stock; $8.6B + $10.0B = $18.6 billion, confirmed in the SEC Filing Highlights pre-written section.

---

CLAIM: "the forward P/E of 14.8x"
LABEL: SUPPORTED
REASON: Source data lists forward_pe as 14.787854, which rounds to 14.8x; confirmed in the Financial Health pre-written section.

---

CLAIM: "the stock trades below its 52-week high of $176.41"
LABEL: SUPPORTED
REASON: Source data lists current_price as $159.47 and week_52_high as $176.41; $159.47 < $176.41 confirms the stock trades below its 52-week high, and the $176.41 figure is exact.

---

## OUTLOOK

---

CLAIM: "The 2.54% dividend yield"
LABEL: SUPPORTED
REASON: Source data explicitly lists dividend_yield as 2.54; confirmed in the Financial Health and Recent Developments pre-written sections.

---

CLAIM: "Middle East geopolitical risk, which has already demonstrated a material earnings impact"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "Middle East disruptions reduced earnings by $1.06 billion in the quarter," confirming a material earnings impact; the SEC Filing Highlights pre-written section also cites this figure explicitly.

---

CLAIM: "ExxonMobil works toward its 2030 goals"
LABEL: SUPPORTED
REASON: RAG SEC Highlights and the 10-Q filing summary both explicitly reference "ExxonMobil's 2030 greenhouse gas emission-reductions plans," confirming the 2030 goal milestone.

---

CLAIM: "advantaged growth projects in Guyana and the Permian continue to contribute incremental earnings"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "Advantaged volume growth contributed $1.14 billion, primarily from Guyana and Permian expansion," confirmed in the SEC Filing Highlights pre-written section.

---

CLAIM: "structural cost discipline is evident" (implicitly referencing structural cost savings)
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly states "Structural cost savings added $170 million," confirming the existence of structural cost discipline; the SEC Filing Highlights pre-written section also references "structural cost improvements of $170 million."

---

CLAIM: "the forward valuation is more compelling than the trailing multiple implies"
LABEL: INFERENCE
REASON: Source data provides trailing P/E of 20.52x and forward P/E of 14.79x; the forward P/E being lower than the trailing P/E directly supports this directional claim by simple comparison of the two present figures.

---

*No additional quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers were identified in the Executive Summary and Outlook sections beyond those audited above.*
