# XOM — baseline

## Metadata

ticker: XOM
arm: baseline
judge_prompt_version: v2
context_sha256: b06c5e8d2806f8432e3f061ad4ad9e581762b66b236de3bec2b7643d9940bb61

## Retrieved source context

STOCK DATA:
{
  "ticker": "XOM",
  "company_name": "ExxonMobil Holdings Corporation",
  "current_price": 161.23,
  "currency": "USD",
  "market_cap": 662963552256.0,
  "pe_ratio": 20.72365,
  "forward_pe": 14.878227,
  "week_52_high": 176.41,
  "week_52_low": 110.39,
  "revenue": 361060007936.0,
  "net_income": 32757000192.0,
  "profit_margin": 0.09072,
  "dividend_yield": 2.6,
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
- **Upstream Earnings**: Total upstream earnings reached $7.9 billion in Q2 2026 (compared to $5.4 billion in Q2 2025) and $13.7 billion for the first half of 2026 (versus $12.2 billion in the same period of 2025)
- **Shareholder Returns**: The company distributed $8.6 billion in dividends and repurchased $10.0 billion of common stock

## Production & Operations
- **Oil-Equivalent Production**: Declined to 4,514 thousand barrels daily in Q2 2026 from 4,630 in Q2 2025, primarily due to Middle East disruptions, divestments, and entitlement changes
- **Production Mix**: Crude oil production remained relatively stable at 3,373 thousand barrels daily, while natural gas production decreased significantly from 8,219 to 6,849 million cubic feet daily

## Earnings Drivers
- **Positive Factors**: Higher crude oil realizations (+$4.65 billion) and advantaged volume growth from Guyana and Permian projects (+$1.14 billion in Q2)
- **Negative Factors**: Middle East volume disruptions (-$1.06 billion in Q2), higher depreciation expenses (-$690 million in Q2), and unfavorable derivatives mark-to-market impacts

## Market Conditions
- Crude oil prices remained within the 10-year historical range despite Middle East supply disruptions
- Natural gas prices stayed elevated above the 10-year average
- Global refining margins were significantly above historical ranges due to unprecedented capacity reductions

## Strategic Focus
- Advantaged assets (Permian, Guyana, and LNG) continue to drive growth
- 2030 greenhouse gas emission-reduction plans are incorporated into medium-term business planning

RAG — RISK FACTORS:
[From Pinecone cache] Based on the provided context, the document references risk factors that are detailed in Item 1A of ExxonMobil's 2025 Form 10-K filing. However, the specific primary risk factors are not enumerated in the excerpts provided.

The context does mention that forward-looking statements regarding environmental and sustainability efforts are not necessarily material to investors or required for SEC disclosure. It also notes that environmental and sustainability-related statements may be based on developing measurement standards, evolving internal controls and processes, and assumptions subject to change.

Additionally, the context indicates that actions to advance greenhouse gas emission-reduction plans are incorporated into medium-term business plans, and that current policy and technology trends are not yet on a pathway to achieve net-zero by 2050.

To obtain a comprehensive list of the primary risk factors disclosed by the company, you would need to review the complete Item 1A. Risk Factors section of the 2025 Form 10-K filing.

## Pre-written sections (judge input)

### Financial Health

ExxonMobil trades at $161.23 with a market capitalization of $663 billion, demonstrating substantial scale within the energy sector. The company generated $361 billion in revenue with a net profit margin of 9.1%, translating to $32.8 billion in net income, reflecting solid operational efficiency despite commodity price volatility. The current P/E ratio of 20.7x appears elevated relative to the forward P/E of 14.9x, suggesting market expectations for earnings growth or potential valuation compression. With a 2.6% dividend yield, XOM provides income alongside capital appreciation potential. Overall, the company exhibits strong financial fundamentals with healthy profitability, though investors should monitor energy sector cyclicality and the company's transition initiatives outlined in recent SEC filings.

### Recent Developments

ExxonMobil's most recent 10-Q filing (August 3, 2026) highlights the company's ongoing integration of greenhouse gas emission-reduction targets into its medium-term business plans, with specific actions outlined to meet 2030 goals. The company acknowledges that sustainability metrics and internal controls remain evolving, introducing some uncertainty around the measurability and achievement of these environmental commitments. With a forward P/E of 14.88 and a solid 2.6% dividend yield, XOM appears reasonably valued despite energy sector volatility, though investors should monitor execution risks on climate initiatives and commodity price exposure. The lack of recent material news developments suggests a period of operational stability, though the energy sector remains sensitive to geopolitical events and energy transition trends.

### SEC Filing Highlights

ExxonMobil reported strong upstream earnings of $7.9 billion in Q2 2026, up 46% year-over-year, driven by higher crude oil realizations and growth from advantaged projects in Guyana and the Permian. The company returned $18.6 billion to shareholders through $8.6 billion in dividends and $10.0 billion in share repurchases during the period. Production declined to 4,514 thousand barrels of oil equivalent daily due to Middle East disruptions and divestments, though crude oil output remained stable while natural gas production decreased. Higher depreciation expenses and unfavorable derivatives impacts partially offset earnings gains, though global refining margins remained significantly above historical averages. Management continues prioritizing advantaged asset development and integrating 2030 greenhouse gas emission-reduction targets into strategic planning.

### Risk Factors

• **Energy Transition and Climate Policy Risk** – Accelerating global climate regulations and the shift toward renewable energy could impact long-term demand for fossil fuels and require significant capital reallocation to meet net-zero commitments, which current technology pathways may not fully support.

• **Commodity Price Volatility** – Fluctuations in crude oil and natural gas prices directly affect revenues and profitability; geopolitical events and supply disruptions create unpredictable margin pressures.

• **Execution Risk on Sustainability Goals** – Environmental and sustainability targets rely on developing measurement standards and evolving internal controls; failure to achieve stated emission-reduction plans could expose the company to regulatory penalties and reputational damage.

## Audited (Exec Summary + Outlook)

### Executive Summary
ExxonMobil is one of the world's largest integrated energy companies, generating $361 billion in revenue and $32.8 billion in net income against a $663 billion market capitalization, underscoring its dominant scale across upstream production, refining, and chemicals. The stock is notable now because a meaningful gap between the current P/E of 20.7x and the forward P/E of 14.9x signals that the market is pricing in meaningful earnings improvement, while a 2.6% dividend yield and $18.6 billion returned to shareholders in the most recent period reflect a shareholder-return program that remains a core part of the investment case. The single most important near-term variable is crude oil price direction, which will determine whether the earnings growth implied by that forward valuation gap materializes or whether the current multiple proves difficult to justify.

### Outlook
The directional outlook for XOM is cautiously constructive, supported by a robust shareholder-return program, advantaged upstream growth in Guyana and the Permian, and refining margins that remain above historical averages — all of which provide meaningful near-term earnings support. The primary tailwinds to watch are sustained crude oil realizations and continued execution on high-return upstream projects; if those two variables hold, the earnings trajectory implied by the current forward valuation becomes more credible. On the headwind side, investors should monitor geopolitical developments affecting Middle East production, the pace and stringency of global climate policy, and whether the company's evolving sustainability measurement and internal controls mature quickly enough to reduce regulatory and reputational exposure. A deterioration in commodity prices, a production setback at key growth assets, or a regulatory tightening around emissions disclosures would each individually weaken the thesis; conversely, evidence of production volume recovery, stable-to-improving refining margins, and demonstrable progress toward 2030 greenhouse gas targets would strengthen conviction and support the case that the gap between current and forward valuation reflects genuine earnings growth rather than wishful market pricing.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

### EXECUTIVE SUMMARY

---

CLAIM: "generating $361 billion in revenue"
LABEL: SUPPORTED
REASON: Source data lists revenue as $361,060,007,936, which rounds to $361 billion; also confirmed in the Financial Health pre-written section.

---

CLAIM: "$32.8 billion in net income"
LABEL: SUPPORTED
REASON: Source data lists net_income as $32,757,000,192, which rounds to $32.8 billion; also confirmed in the Financial Health pre-written section.

---

CLAIM: "a $663 billion market capitalization"
LABEL: SUPPORTED
REASON: Source data lists market_cap as $662,963,552,256, which rounds to $663 billion; also confirmed in the Financial Health pre-written section.

---

CLAIM: "current P/E of 20.7x"
LABEL: SUPPORTED
REASON: Source data lists pe_ratio as 20.72365, which rounds to 20.7x.

---

CLAIM: "forward P/E of 14.9x"
LABEL: SUPPORTED
REASON: Source data lists forward_pe as 14.878227, which rounds to 14.9x.

---

CLAIM: "a 2.6% dividend yield"
LABEL: SUPPORTED
REASON: Source data explicitly lists dividend_yield as 2.6.

---

CLAIM: "$18.6 billion returned to shareholders in the most recent period"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states $8.6 billion in dividends plus $10.0 billion in share repurchases; $8.6B + $10.0B = $18.6B, confirmed by arithmetic and the SEC Filing Highlights pre-written section.

---

### OUTLOOK

---

CLAIM: "advantaged upstream growth in Guyana and the Permian"
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly names Guyana and Permian as advantaged assets driving growth, and the SEC Filing Highlights pre-written section repeats this.

---

CLAIM: "refining margins that remain above historical averages"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "Global refining margins were significantly above historical ranges due to unprecedented capacity reductions," which supports this claim directionally and factually.

---

CLAIM: "Middle East production" (as a geopolitical headwind to monitor)
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly identifies Middle East volume disruptions (-$1.06 billion in Q2) as a negative factor, confirming Middle East production is a relevant variable.

---

CLAIM: "2030 greenhouse gas targets"
LABEL: SUPPORTED
REASON: RAG SEC Highlights, the 10-Q filing summary, and the Risk Factors pre-written section all explicitly reference ExxonMobil's 2030 greenhouse gas emission-reduction plans.

---

CLAIM: "the gap between current and forward valuation" (implying the spread between 20.7x current P/E and 14.9x forward P/E)
LABEL: SUPPORTED
REASON: Both figures (current P/E 20.72x and forward P/E 14.88x) are present in the source data; the directional gap is arithmetically verifiable (20.72 − 14.88 = 5.84 points) and is not a new or fabricated figure.

---

**No additional quantitative figures, price targets, specific thresholds, named ratios, or forward-looking numbers appear in the Outlook section beyond those audited above.** All claims in the Executive Summary and Outlook are accounted for.
