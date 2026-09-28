# XOM — baseline

## Metadata

ticker: XOM
arm: baseline
judge_prompt_version: v2
context_sha256: 73254cb301fde64c96e7a2a0a9e6677d5d88ea96dd241b40317b5b12b5169488

## Retrieved source context

STOCK DATA:
{
  "ticker": "XOM",
  "company_name": "ExxonMobil Holdings Corporation",
  "current_price": 162.03,
  "currency": "USD",
  "market_cap": 666253066240.0,
  "pe_ratio": 20.853281,
  "forward_pe": 14.952051,
  "week_52_high": 176.41,
  "week_52_low": 110.39,
  "revenue": 361060007936.0,
  "net_income": 32757000192.0,
  "profit_margin": 0.09072,
  "dividend_yield": 2.56,
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
- **Upstream Earnings**: Total upstream earnings reached $7.9 billion in Q2 2026 (compared to $5.4 billion in Q2 2025) and $13.7 billion for the first half of 2026 (versus $12.2 billion in the prior year period)
- **Shareholder Returns**: The company distributed $8.6 billion in dividends and repurchased $10.0 billion of common stock

## Production & Operations
- **Oil-Equivalent Production**: Declined to 4,514 thousand barrels daily in Q2 2026 from 4,630 in Q2 2025, primarily due to divestments and Middle East disruptions
- **Production Mix**: Crude oil and liquids production totaled 3,373 thousand barrels daily globally, while natural gas production was 6,849 million cubic feet daily

## Earnings Drivers
- **Positive Factors**: Higher crude oil realizations added $4.7 billion in Q2 earnings; advantaged volume growth (Guyana and Permian) contributed $1.1 billion
- **Negative Factors**: Middle East disruptions reduced earnings by $1.1 billion; higher depreciation expenses decreased earnings by $690 million; unfavorable derivatives mark-to-market impacts reduced earnings by $180 million

## Market Conditions & Strategy
- Crude oil prices remained within the 10-year historical range despite supply disruptions in the Middle East
- Natural gas prices remained elevated above the 10-year average
- The company is focused on advantaged assets including Permian, Guyana, and LNG projects
- Environmental and sustainability efforts are being incorporated into medium-term business plans with annual updates

RAG — RISK FACTORS:
[From Pinecone cache] Based on the provided context, the document references risk factors but does not provide a comprehensive list of the primary risk factors themselves. The context only includes a brief mention that directs readers to "Item 1A. Risk Factors" of ExxonMobil's 2025 Form 10-K for detailed information about risk factors.

The only specific risk factor area that receives some discussion in the provided context relates to environmental and sustainability efforts. The document notes that forward-looking statements regarding environmental and sustainability initiatives are not necessarily material to investors and may be based on:

- Standards for measuring progress that are still developing
- Internal controls and processes that continue to evolve
- Assumptions subject to change in the future, including future rule-making

Additionally, the context mentions that current trends for policy stringency and development of lower-emission solutions are not yet on a pathway to achieve net-zero by 2050, which could be considered a risk factor related to climate and regulatory policy.

However, to obtain a complete understanding of the primary risk factors disclosed by the company, you would need to review the full "Item 1A. Risk Factors" section of the 2025 Form 10-K filing.

## Pre-written sections (judge input)

### Financial Health

ExxonMobil trades at $162.03 with a market capitalization of $666.3 billion, supported by strong operational fundamentals including $361.1 billion in annual revenue and a healthy 9.1% profit margin generating $32.8 billion in net income. The stock's P/E ratio of 20.9x appears reasonable relative to its forward P/E of 15.0x, suggesting potential valuation compression as earnings are expected to grow. With a 2.56% dividend yield and solid profitability metrics, the company demonstrates financial stability typical of integrated energy majors, though investors should monitor commodity price exposure and energy transition risks inherent to the sector.

### Recent Developments

ExxonMobil's most recent 10-Q filing (August 3, 2026) highlights the company's ongoing integration of greenhouse gas emission-reduction targets into its medium-term business plans, with specific actions outlined to meet 2030 goals. The company continues to navigate evolving environmental standards and regulatory frameworks, noting that sustainability metrics and internal controls remain subject to refinement. With a solid 9.1% profit margin and $32.8 billion in net income on $361 billion in revenue, XOM maintains financial strength to fund both energy transition initiatives and its 2.56% dividend yield. The forward P/E of 14.95x suggests reasonable valuation relative to earnings expectations, though investors should monitor how capital allocation between traditional oil & gas operations and low-carbon investments impacts long-term returns.

### SEC Filing Highlights

ExxonMobil reported strong upstream earnings of $7.9 billion in Q2 2026, up 46% year-over-year, driven primarily by higher crude oil realizations that added $4.7 billion in earnings. The company returned $18.6 billion to shareholders through $8.6 billion in dividends and $10.0 billion in share repurchases during the period. Production declined modestly to 4,514 thousand barrels of oil-equivalent daily due to divestments and Middle East disruptions, though advantaged projects in Guyana and the Permian contributed $1.1 billion in incremental earnings. ExxonMobil continues to prioritize high-return, low-cost assets while navigating elevated natural gas prices and incorporating sustainability initiatives into its medium-term strategy.

### Risk Factors

• **Energy Transition and Climate Policy Risk** – Regulatory pressure to reduce emissions and transition to lower-carbon energy sources may impact demand for traditional oil and gas products, while the company's net-zero commitments depend on developing technologies and market conditions that remain uncertain.

• **Commodity Price Volatility** – Fluctuations in crude oil and natural gas prices directly affect revenues and profitability; sustained low prices could impair asset values and reduce capital investment capacity.

• **Regulatory and Environmental Compliance Risk** – Evolving environmental standards, sustainability measurement frameworks, and climate-related regulations create operational and financial uncertainties, with internal processes and controls still developing to address these emerging requirements.

## Audited (Exec Summary + Outlook)

### Executive Summary
ExxonMobil is one of the world's largest integrated energy majors, generating $361.1 billion in annual revenue and $32.8 billion in net income across its upstream, downstream, and chemical operations, underpinned by a $666.3 billion market capitalization. The stock is notable now because Q2 2026 upstream earnings surged 46% year-over-year to $7.9 billion while the gap between the current P/E of 20.9x and forward P/E of 15.0x implies meaningful earnings growth is anticipated, even as the company simultaneously executes a $10.0 billion share repurchase program and sustains a 2.56% dividend yield. The single most important near-term variable is crude oil price realization — the same driver that added $4.7 billion in earnings in Q2 2026 — as its direction will determine whether the forward earnings expansion embedded in current valuations materializes or reverses.

### Outlook
The directional outlook for ExxonMobil is cautiously constructive, supported by the momentum of a 46% year-over-year surge in upstream earnings, robust shareholder returns, and the incremental contribution of advantaged growth assets in Guyana and the Permian — but tempered by meaningful headwinds that investors should monitor closely. On the tailwind side, elevated natural gas prices, continued production ramp at low-cost projects, and a disciplined capital return program all reinforce the investment thesis. The key variables to watch are crude oil price realizations, which proved to be the dominant earnings driver in Q2 2026; the pace and stability of production recovery from Middle East disruptions; and how management allocates capital between traditional upstream operations and the low-carbon investments tied to its 2030 emission-reduction commitments. The thesis would strengthen if crude realizations remain supportive, Guyana and Permian volumes continue to scale, and the company demonstrates that energy transition spending does not materially erode returns on traditional assets. Conversely, the view would weaken under a sustained decline in commodity prices, an acceleration of climate-related regulatory burdens that raise compliance costs, or evidence that capital allocation is shifting away from high-return projects toward lower-return transition investments before those initiatives achieve commercial scale.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative, forward-looking, and specific factual claim in the Executive Summary and Outlook sections.

---

## EXECUTIVE SUMMARY

---

CLAIM: "$361.1 billion in annual revenue"
LABEL: SUPPORTED
REASON: Source data lists revenue as $361,060,007,936, which rounds to $361.1 billion; also confirmed in the Financial Health pre-written section.

---

CLAIM: "$32.8 billion in net income"
LABEL: SUPPORTED
REASON: Source data lists net_income as $32,757,000,192, which rounds to $32.8 billion; confirmed in multiple pre-written sections.

---

CLAIM: "$666.3 billion market capitalization"
LABEL: SUPPORTED
REASON: Source data lists market_cap as $666,253,066,240, which rounds to $666.3 billion.

---

CLAIM: "Q2 2026 upstream earnings surged 46% year-over-year to $7.9 billion"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states upstream earnings were $7.9 billion in Q2 2026 vs. $5.4 billion in Q2 2025; ($7.9B − $5.4B) / $5.4B = 46.3%, which rounds to 46% — within 0.15 pp tolerance; the pre-written SEC Filing Highlights section also states "up 46% year-over-year."

---

CLAIM: "current P/E of 20.9x"
LABEL: SUPPORTED
REASON: Source data lists pe_ratio as 20.853281, which rounds to 20.9x.

---

CLAIM: "forward P/E of 15.0x"
LABEL: SUPPORTED
REASON: Source data lists forward_pe as 14.952051, which rounds to 15.0x.

---

CLAIM: "the gap between the current P/E of 20.9x and forward P/E of 15.0x implies meaningful earnings growth is anticipated"
LABEL: INFERENCE
REASON: Both P/E figures are present in the source data; the directional inference that a lower forward P/E implies anticipated earnings growth is a standard, directly derivable financial interpretation requiring no additional facts.

---

CLAIM: "$10.0 billion share repurchase program"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states the company "repurchased $10.0 billion of common stock," confirmed in the SEC Filing Highlights pre-written section.

---

CLAIM: "2.56% dividend yield"
LABEL: SUPPORTED
REASON: Source data lists dividend_yield as 2.56.

---

CLAIM: "crude oil price realization … added $4.7 billion in earnings in Q2 2026"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "Higher crude oil realizations added $4.7 billion in Q2 earnings," confirmed in the SEC Filing Highlights pre-written section.

---

## OUTLOOK

---

CLAIM: "46% year-over-year surge in upstream earnings"
LABEL: SUPPORTED
REASON: Same arithmetic as above — ($7.9B − $5.4B) / $5.4B ≈ 46.3%, within tolerance; sourced from RAG SEC Highlights and pre-written section.

---

CLAIM: "incremental contribution of advantaged growth assets in Guyana and the Permian"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "advantaged volume growth (Guyana and Permian) contributed $1.1 billion," and the pre-written SEC Filing Highlights section confirms this.

---

CLAIM: "elevated natural gas prices"
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly states "Natural gas prices remained elevated above the 10-year average."

---

CLAIM: "crude oil price realizations … proved to be the dominant earnings driver in Q2 2026"
LABEL: SUPPORTED
REASON: RAG SEC Highlights identifies higher crude oil realizations as adding $4.7 billion in Q2 earnings, the largest single factor listed among earnings drivers, supporting the characterization as dominant.

---

CLAIM: "production recovery from Middle East disruptions"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "Middle East disruptions reduced earnings by $1.1 billion" and caused production to decline, confirming the disruption exists; the outlook's reference to "recovery" is a forward-looking directional watch-item, but the underlying disruption fact is present in the source.

---

CLAIM: "2030 emission-reduction commitments"
LABEL: SUPPORTED
REASON: The 10-Q summary and RAG SEC Highlights both reference "ExxonMobil's 2030 greenhouse gas emission-reductions plans" explicitly.

---

CLAIM: "Guyana and Permian volumes continue to scale"
LABEL: SUPPORTED
REASON: RAG SEC Highlights identifies Guyana and Permian as advantaged growth assets contributing $1.1 billion in incremental earnings, supporting the characterization of ongoing scaling; the forward-looking framing is a watch-item consistent with source data.

---

*No additional quantitative figures, price targets, thresholds, ratios, or named product milestones appear in the Outlook section beyond those already audited above.*
