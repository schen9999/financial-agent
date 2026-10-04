# CALM — baseline

## Metadata

ticker: CALM
arm: baseline
judge_prompt_version: v2
context_sha256: 647fb5e71bc5e06cf0a2ded87c6ca0f8bc507c73c05126a362311363328d15b5
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 431, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.372, "latency_s_total": 5.372, "parse_failure": 0, "prompt_tokens": 2912, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 390, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.34, "latency_s_total": 5.34, "parse_failure": 0, "prompt_tokens": 2911, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 176, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.316, "latency_s_total": 2.316, "parse_failure": 0, "prompt_tokens": 692, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 184, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.443, "latency_s_total": 2.443, "parse_failure": 0, "prompt_tokens": 685, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 181, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.408, "latency_s_total": 2.408, "parse_failure": 0, "prompt_tokens": 463, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 192, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.944, "latency_s_total": 1.944, "parse_failure": 0, "prompt_tokens": 512, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1206, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.02, "latency_s_total": 17.02, "parse_failure": 0, "prompt_tokens": 1870, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "CALM",
  "company_name": "Cal-Maine Foods, Inc.",
  "current_price": 66.67,
  "currency": "USD",
  "market_cap": 3114196480.0,
  "pe_ratio": 53.336,
  "forward_pe": 65.68473,
  "week_52_high": 95.57,
  "week_52_low": 63.5,
  "revenue": 2528636928.0,
  "net_income": 58727000.0,
  "profit_margin": 0.02322,
  "dividend_yield": 7.2,
  "sector": "Consumer Defensive",
  "industry": "Farm Products"
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
    "filing_date": "2026-07-22",
    "summary": "Item 1A. Risk Factors and elsewhere in this report as well as those included in other reports we file from time to time with the Securities and Exchange Commission (the \u201cSEC\u201d) (including our Quarterly Reports on Form 10-Q and Current Reports on Form 8-K), (ii) changes in wholesale shell egg market prices, (iii) changes in the demand for shell eggs and our prepared foods offerings, (iv) increases in feed costs for our shell egg operations as well as increases in input costs for prepared foods, (v) our ability to predict and meet demand for cage -free and other specialty eggs, (vi) the risks and hazards inherent in shell egg, egg products and prepared foods operations (including, as applicable, disease, pests, weather conditions, and potential for product recall), including but not limited t"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-09-30",
    "summary": "Item 1A Risk Factors of our 202 6 Annual Report, as well as those included in other reports we file from time to time with the Securities and Exchange Commission (the \u201cSEC\u201d) (including our Quarterly Reports on Form 10-Q and Current Reports on Form 8-K). The actual timing, number and value of shares repurchased under our share repurchase program will be determined by management in its discretion and will depend on a number of factors, including but not limited to, the market price of our Common Stock and general market and economic conditions. The share repurchase program may be suspended, modified or discontinued at any time without prior notice. Readers are cautioned not to place undue reliance on forward -looking statements because, while we believe the assumptions on which the forward -"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] # Key Takeaways from Cal-Maine Foods' Recent SEC Filings

## Company Overview
Cal-Maine Foods is the largest egg company in the United States and a leading player in the egg-based food industry. Founded in 1957 and headquartered in Ridgeland, Mississippi, the company operates a comprehensive portfolio spanning conventional to specialty eggs (cage-free, organic, pasture-raised, etc.) and prepared foods products.

## Strategic Growth Initiatives
The company is pursuing several key growth strategies:
- Increasing the proportion of specialty shell eggs in its sales mix
- Expanding prepared foods and egg products businesses
- Strengthening its portfolio of branded offerings (including Eggland's Best®, Land O'Lakes®, and Van's®)
- Pursuing strategic acquisitions and organic investments

## Recent Acquisitions
Cal-Maine has been actively acquiring complementary businesses, including:
- **Echo Lake Foods** (June 2025) for $289.5 million - expanding prepared foods capabilities
- **Creighton Brothers** (March 2026) for $129.3 million - adding shell egg production and egg products capacity
- **Van's Foods assets** (May 2026) for $24.8 million - supporting prepared foods diversification
- **Clean Egg** (October 2025) for $23.7 million - adding cage-free and free-range production
- **ISE America** (Q1 fiscal 2025) - expanding Northeast and Mid-Atlantic market presence

## Prepared Foods Expansion
Multiple capacity expansion projects are underway expected to grow prepared foods production by more than 30% from mid-2027 through 2028, including scrambled egg production, pancake lines, and equipment installations through joint ventures.

## Risk Factors
Key risks include HPAI outbreaks, feed cost volatility, market price fluctuations, integration challenges from acquisitions, and competitive pressures.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors affecting its business:

**Market and Operational Risks:**
- Fluctuations in wholesale shell egg market prices
- Changes in demand for shell eggs and prepared foods offerings
- Increases in feed costs and input costs for prepared foods
- Ability to predict and meet demand for cage-free and specialty eggs

**Disease and Environmental Hazards:**
- Risks inherent in shell egg, egg products, and prepared foods operations including disease, pests, weather conditions, and product recall potential
- Current outbreak of Highly Pathogenic Avian Influenza (HPAI) affecting poultry in the U.S., Canada, and other countries, which impacted operations in fiscal 2024 and March 2026

**Acquisition and Integration Risks:**
- Risks and obligations from recent or future acquisitions, such as the Echo Lake Foods acquisition completed in June 2025
- Risks that conditions for completing pending acquisitions may not be met
- Ability to successfully integrate recently acquired businesses and realize expected benefits including synergies, cost savings, and margin expansion

**Competitive and Operational Challenges:**
- Ability to produce, supply, and distribute products efficiently and reliably
- Competition with existing competitors and new market entrants
- Ability to retain existing customers and acquire new customers

**Regulatory and Economic Risks:**
- Government, customer, and consumer reactions to high egg market prices
- Potential new or expanded government regulations
- Changes in inflation, interest rates, and trade and tariff policies
- Global instability from geopolitical conflicts

**Other Risks:**
- Loss or expiration of registered trademarks or intellectual property
- Adverse results in pending litigation and legal matters

## Pre-written sections (judge input)

### Financial Health

Cal-Maine Foods trades at $66.67 with a market capitalization of $3.1 billion, generating $2.5 billion in annual revenue. The company's valuation appears stretched, with a P/E ratio of 53.3x and forward P/E of 65.7x, significantly above industry averages and reflecting elevated market expectations. However, profitability remains challenged, with a thin net profit margin of just 2.3%, indicating limited earnings relative to sales. The elevated dividend yield of 7.2% suggests the company prioritizes shareholder returns despite modest earnings, which may not be sustainable long-term. Overall, CALM presents a high-valuation, low-margin profile typical of commodity-exposed agricultural producers facing input cost pressures and market volatility.

### Recent Developments

Cal-Maine Foods faces significant operational and market headwinds as outlined in its latest SEC filings. The company's most recent 10-Q (September 30, 2026) and 10-K (July 22, 2026) highlight persistent risk factors including volatile wholesale shell egg prices, fluctuating feed costs, and demand uncertainty for specialty egg products like cage-free offerings. With a notably high forward P/E ratio of 65.68x and a compressed profit margin of 2.32%, the stock appears to price in elevated earnings expectations that may be difficult to achieve given commodity price pressures and operational risks such as disease and weather-related disruptions. The company's active share repurchase program suggests management confidence, though investors should monitor quarterly results closely for trends in pricing power and cost management amid an uncertain commodity environment.

### SEC Filing Highlights

Cal-Maine Foods, the largest U.S. egg producer, is executing an aggressive diversification strategy through multiple acquisitions including Echo Lake Foods ($289.5M), Creighton Brothers ($129.3M), and Van's Foods assets ($24.8M) to expand its prepared foods and specialty egg portfolios. The company is investing heavily in capacity expansion, with prepared foods production expected to grow over 30% from mid-2027 through 2028 through new scrambled egg and pancake production lines. Cal-Maine continues to shift its sales mix toward higher-margin specialty eggs (cage-free, organic, pasture-raised) while strengthening branded offerings including Eggland's Best® and Land O'Lakes®. Key risks remain elevated, including avian influenza exposure, feed cost volatility, and integration execution challenges from recent acquisitions.

### Risk Factors

- **Avian Influenza and Disease Exposure**: Highly Pathogenic Avian Influenza (HPAI) outbreaks significantly impacted operations in fiscal 2024 and March 2026, with ongoing risks to U.S. and Canadian poultry operations that could disrupt production and supply chains.

- **Commodity Price Volatility**: Fluctuations in wholesale shell egg market prices and feed costs directly impact margins; the company has limited ability to predict demand for cage-free and specialty eggs, creating earnings uncertainty.

- **Integration and Acquisition Execution Risk**: Recent acquisitions (Echo Lake Foods in June 2025) and pending deals carry risks that expected synergies, cost savings, and margin expansion may not materialize, alongside integration challenges that could strain operations.

## Audited (Exec Summary + Outlook)

### Executive Summary
Cal-Maine Foods is the largest U.S. egg producer, generating $2.5 billion in annual revenue and pursuing an aggressive expansion into prepared foods and specialty eggs through acquisitions totaling over $440 million across Echo Lake Foods, Creighton Brothers, and Van's Foods assets. The stock is notable now because it trades at a stretched valuation — a 53.3x trailing P/E and 65.7x forward P/E — against a net profit margin of just 2.3%, creating a precarious gap between market expectations and the company's demonstrated earnings power. The single most important near-term variable is whether Cal-Maine can successfully integrate its recent acquisitions while managing avian influenza exposure and commodity price volatility well enough to justify those elevated multiples.

### Outlook
The directional lean on CALM is **cautious**. The bull case rests on the company's strategic pivot toward higher-margin specialty eggs and prepared foods, a capacity expansion that could meaningfully broaden the revenue mix, and the strength of established brands like Eggland's Best® and Land O'Lakes® as demand for premium egg products grows. However, those tailwinds are offset by a valuation that leaves little room for error, a dividend yield that may prove difficult to sustain against thin margins, and a risk profile dominated by variables largely outside management's control — namely HPAI outbreaks, wholesale shell egg price swings, and feed cost inflation. Investors should watch the trajectory of specialty egg demand and pricing power, the pace and cost of acquisition integration (particularly Echo Lake Foods), any new HPAI developments affecting flock size or supply chains, and whether quarterly results show margin improvement or further compression. The thesis would strengthen if integration synergies materialize ahead of schedule, specialty egg volumes grow at a sustained rate, and the commodity environment stabilizes; it would weaken if another significant HPAI outbreak disrupts operations, acquisition costs strain the balance sheet, or earnings continue to fall short of the elevated expectations already embedded in the stock's valuation.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "the largest U.S. egg producer"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "Cal-Maine Foods is the largest egg company in the United States."

---

CLAIM: "generating $2.5 billion in annual revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $2,528,636,928, which rounds to $2.5 billion; the Financial Health section also states "$2.5 billion in annual revenue."

---

CLAIM: "acquisitions totaling over $440 million across Echo Lake Foods, Creighton Brothers, and Van's Foods assets"
LABEL: SUPPORTED
REASON: Echo Lake Foods ($289.5M) + Creighton Brothers ($129.3M) + Van's Foods ($24.8M) = $443.6M, which is over $440 million; all three figures are present in the RAG SEC Highlights.

---

CLAIM: "a 53.3x trailing P/E"
LABEL: SUPPORTED
REASON: Source data lists pe_ratio as 53.336, which rounds to 53.3x; confirmed in the Financial Health section.

---

CLAIM: "65.7x forward P/E"
LABEL: SUPPORTED
REASON: Source data lists forward_pe as 65.68473, which rounds to 65.7x; confirmed in the Financial Health and Recent Developments sections.

---

CLAIM: "a net profit margin of just 2.3%"
LABEL: SUPPORTED
REASON: Source data lists profit_margin as 0.02322 (2.322%), which rounds to 2.3%; confirmed in the Financial Health section.

---

**OUTLOOK**

---

CLAIM: "a dividend yield that may prove difficult to sustain against thin margins"
LABEL: SUPPORTED
REASON: The dividend yield of 7.2% is present in the source data, and the Financial Health section explicitly states the elevated yield "may not be sustainable long-term" given modest earnings — the directional claim is grounded in source material.

---

CLAIM: "the pace and cost of acquisition integration (particularly Echo Lake Foods)"
LABEL: SUPPORTED
REASON: Echo Lake Foods is explicitly named in the Risk Factors section as a specific integration risk example ("Recent acquisitions (Echo Lake Foods in June 2025)…carry risks that expected synergies, cost savings, and margin expansion may not materialize").

---

CLAIM: "a capacity expansion that could meaningfully broaden the revenue mix"
LABEL: INFERENCE
REASON: The RAG SEC Highlights state prepared foods production is expected to grow over 30% from mid-2027 through 2028; the claim that this "could meaningfully broaden the revenue mix" is a direct qualitative inference from that stated expansion figure, requiring no additional facts.

---

CLAIM: "prepared foods production expected to grow over 30% from mid-2027 through 2028" *(implicit in the bull case reference to "capacity expansion")*
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "prepared foods production by more than 30% from mid-2027 through 2028," and this figure is reproduced in the SEC Filing Highlights pre-written section.

---

*(Note: The Outlook does not explicitly quote the 30% figure — it references "capacity expansion" generically — so no separate entry is needed for a figure not directly quoted. All other quantitative or forward-looking claims in the Outlook are qualitative directional statements rather than specific figures, except those already evaluated above.)*

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | Largest U.S. egg producer | SUPPORTED |
| 2 | $2.5 billion in annual revenue | SUPPORTED |
| 3 | Acquisitions totaling over $440 million (Echo Lake, Creighton, Van's) | SUPPORTED |
| 4 | 53.3x trailing P/E | SUPPORTED |
| 5 | 65.7x forward P/E | SUPPORTED |
| 6 | Net profit margin of 2.3% | SUPPORTED |
| 7 | Dividend yield difficult to sustain against thin margins | SUPPORTED |
| 8 | Integration risk particularly Echo Lake Foods | SUPPORTED |
| 9 | Capacity expansion could meaningfully broaden revenue mix | INFERENCE |
