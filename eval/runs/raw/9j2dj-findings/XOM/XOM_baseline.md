# XOM — baseline

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
- **Upstream Earnings**: Total upstream earnings reached $13.7 billion for the first half of 2026, compared to $12.2 billion in the same period of 2025
- **Shareholder Returns**: The company distributed $8.6 billion in dividends and repurchased $10.0 billion of common stock

## Production and Operations
- **Oil-Equivalent Production**: Decreased to 4,514 thousand barrels daily in Q2 2026 from 4,630 in Q2 2025, primarily due to Middle East disruptions, divestments, and other factors
- **Natural Gas Production**: Worldwide natural gas production declined from 8,219 to 6,849 million cubic feet daily year-over-year

## Earnings Drivers (Q2 2026)
- **Positive Impacts**: Higher crude oil realizations (+$4.7 billion), advantaged volume growth from Guyana and Permian (+$1.1 billion), and structural cost savings (+$170 million)
- **Negative Impacts**: Middle East disruptions (-$1.1 billion), higher depreciation expenses (-$690 million), and unfavorable derivatives timing effects (-$180 million)

## Market Conditions
- Crude oil prices remained within the 10-year historical range despite supply disruptions in the Middle East
- Natural gas prices remained elevated above the 10-year average
- Global refining margins were significantly above historical ranges due to unprecedented capacity reductions

## Strategic Focus
- Advantaged assets (Permian, Guyana, and LNG) continue to drive growth
- 2030 greenhouse gas emission-reduction plans are incorporated into medium-term business planning
- Future investments in lower-emission solutions remain dependent on policy support and returns

RAG — RISK FACTORS:
[From Pinecone cache] Based on the provided context, the document references risk factors that are detailed in Item 1A of ExxonMobil's 2025 Form 10-K filing. However, the specific risk factors themselves are not included in the context information provided.

The context only mentions that risk factors exist and directs readers to that section of the 2025 Form 10-K for details, but does not enumerate or describe what those primary risk factors actually are.

To obtain information about the primary risk factors disclosed by ExxonMobil, you would need to review the complete Item 1A. Risk Factors section from the company's 2025 Form 10-K filing.

## Audited (Exec Summary + Outlook)

### Executive Summary
ExxonMobil is one of the world's largest integrated oil and gas majors, operating across upstream, downstream, and chemical segments, with a market capitalization of $655.7 billion and annual revenue of $361.1 billion that underscore its dominant position in the global energy landscape. The stock is notable now because upstream earnings grew 12% to $13.7 billion in H1 2026 and the forward P/E of 14.8x represents a meaningful compression from the trailing multiple of 20.5x, suggesting the market may be pricing in improved earnings power even as energy transition pressures and geopolitical disruptions weigh on sentiment. The single most important near-term variable is crude oil price realization: sustained favorable pricing would validate the earnings re-rating implied by the forward multiple, while a meaningful decline would pressure cash flows, shareholder return capacity, and the credibility of the company's low-emission investment commitments.

### Outlook
The directional outlook for ExxonMobil is **cautiously constructive**, supported by the company's advantaged upstream positions in Guyana and the Permian, a demonstrated commitment to shareholder returns, and a forward earnings multiple that implies improving profitability relative to current levels. Key tailwinds to watch include the trajectory of crude oil price realizations, the pace of volume recovery from Middle East disruptions, and the durability of refining margin strength driven by global capacity reductions. On the headwind side, investors should monitor natural gas production trends, the geopolitical environment affecting operational continuity, and the evolving regulatory landscape around carbon pricing and climate disclosure — all of which could raise costs or constrain capital allocation flexibility. The thesis would strengthen if Guyana and Permian volumes ramp as planned, commodity prices remain supportive, and the policy environment provides clearer frameworks for low-emission investments; it would weaken if crude prices deteriorate materially, production disruptions persist, or regulatory burdens accelerate faster than the company can adapt its medium-term plans.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of $655.7 billion"
LABEL: SUPPORTED
REASON: Source data shows market_cap = $655,726,608,384, which rounds to $655.7 billion; also explicitly stated in the Financial Health pre-written section.

---

CLAIM: "annual revenue of $361.1 billion"
LABEL: SUPPORTED
REASON: Source data shows revenue = $361,060,007,936, which rounds to $361.1 billion; also explicitly stated in the Financial Health pre-written section.

---

CLAIM: "upstream earnings grew 12% to $13.7 billion in H1 2026"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states upstream earnings reached $13.7 billion for H1 2026 vs. $12.2 billion in H1 2025; ($13.7B − $12.2B) / $12.2B = 12.3%, within 0.15 pp of 12%, and the SEC Filing Highlights pre-written section states "grew 12% to $13.7 billion in H1 2026."

---

CLAIM: "forward P/E of 14.8x"
LABEL: SUPPORTED
REASON: Source data shows forward_pe = 14.787854, which rounds to 14.8x; also stated in the Financial Health section.

---

CLAIM: "trailing multiple of 20.5x"
LABEL: SUPPORTED
REASON: Source data shows pe_ratio = 20.52381, which rounds to 20.5x; also stated in the Financial Health section.

---

**OUTLOOK**

---

CLAIM: "advantaged upstream positions in Guyana and the Permian"
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly names "Guyana and Permian" as advantaged assets driving growth, and the SEC Filing Highlights pre-written section confirms "Strategic focus remains on advantaged assets in Permian and Guyana."

---

CLAIM: "forward earnings multiple that implies improving profitability relative to current levels"
LABEL: INFERENCE
REASON: The forward P/E of 14.8x is lower than the trailing P/E of 20.5x, both present in the source data; a lower forward P/E directly implies higher expected future earnings relative to current price, making this a direct comparison of two present figures.

---

CLAIM: "volume recovery from Middle East disruptions"
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly identifies "Middle East disruptions" as a cause of production decline (−$1.1 billion impact and reduced barrels daily), supporting the characterization of disruptions affecting volumes.

---

CLAIM: "durability of refining margin strength driven by global capacity reductions"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "Global refining margins were significantly above historical ranges due to unprecedented capacity reductions," directly supporting this claim.

---

CLAIM: "natural gas production trends" (as a headwind to monitor)
LABEL: SUPPORTED
REASON: RAG SEC Highlights confirms natural gas production declined from 8,219 to 6,849 million cubic feet daily year-over-year, providing a factual basis for flagging this as a concern.

---

CLAIM: "Guyana and Permian volumes ramp as planned"
LABEL: SUPPORTED
REASON: RAG SEC Highlights identifies "advantaged volume growth from Guyana and Permian" as a positive earnings driver and names these as strategic focus assets, supporting the reference to planned volume ramp.

---

*No additional quantitative figures, price targets, specific thresholds, ratios, or named product milestones appear in the Outlook section beyond those evaluated above.*
