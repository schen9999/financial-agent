# CALM — rerank3

## Metadata

ticker: CALM
arm: rerank3
judge_prompt_version: v2
context_sha256: b4b9dd1d0fc41d09edf763043a92fa7eaaf54d42b7d7b96ecf385c7e82e1683b
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 450, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.825, "latency_s_total": 4.825, "parse_failure": 0, "prompt_tokens": 2912, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 417, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.124, "latency_s_total": 5.124, "parse_failure": 0, "prompt_tokens": 2900, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 187, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.238, "latency_s_total": 2.238, "parse_failure": 0, "prompt_tokens": 680, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 152, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.127, "latency_s_total": 2.127, "parse_failure": 0, "prompt_tokens": 673, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 218, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.725, "latency_s_total": 2.725, "parse_failure": 0, "prompt_tokens": 490, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 206, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.397, "latency_s_total": 2.397, "parse_failure": 0, "prompt_tokens": 531, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1277, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 18.234, "latency_s_total": 18.234, "parse_failure": 0, "prompt_tokens": 1930, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "CALM",
  "company_name": "Cal-Maine Foods, Inc.",
  "current_price": 62.7,
  "currency": "USD",
  "market_cap": 2928755456.0,
  "pe_ratio": 51.39344,
  "forward_pe": 61.7734,
  "week_52_high": 95.57,
  "week_52_low": 61.88,
  "financial_currency": "USD",
  "revenue": 2528636928.0,
  "net_income": 58727000.0,
  "profit_margin_pct": 2.32,
  "dividend_yield": 3.86,
  "sector": "Consumer Defensive",
  "industry": "Farm Products"
}

NEWS ARTICLES:
[]

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

**Prepared Foods Expansion:**
- Multiple capacity expansion projects underway expected to grow prepared foods production by more than 30% from mid-2027 through 2028
- Echo Lake Foods facilities projects include 17 million pounds of additional scrambled egg production and a high-speed pancake line adding 12 million pounds
- Crepini Foods joint venture investing in equipment to add 18 million pounds of capacity over 12-18 months

**Acquisitions:**
- Acquired Echo Lake Foods (June 2025) for $289.5 million, expanding prepared foods capabilities
- Acquired ISE America assets (Q1 FY2025) adding 4.7 million laying hens capacity across Northeast and Mid-Atlantic
- Acquired Creighton Brothers (March 2026) for $129.3 million, adding 3.2 million layers and egg products capacity
- Acquired Van's Foods assets (May 2026) for $24.8 million to support prepared foods retail strategy

## Risk Factors
- HPAI (Highly Pathogenic Avian Influenza) outbreak impacting operations in Q3-Q4 FY2024 and March 2026
- Volatility in wholesale egg prices and feed costs
- Integration challenges from recent acquisitions
- Market competition and regulatory pressures

## Business Strategy
The company aims to leverage its market position, vertical integration, and strong balance sheet to pursue sustainable growth, expand margins, and diversify revenue streams through specialty eggs, prepared foods expansion, and strategic acquisitions.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses the following primary risk factors:

1. **Market Price Volatility** - Changes in wholesale shell egg market prices and demand for shell eggs and prepared foods offerings

2. **Input Cost Increases** - Rising feed costs for shell egg operations and increased input costs for prepared foods

3. **Specialty Product Demand** - Ability to predict and meet demand for cage-free and other specialty eggs

4. **Operational Hazards** - Risks inherent in shell egg, egg products, and prepared foods operations including disease, pests, weather conditions, and product recall potential. Notably, this includes the current outbreak of Highly Pathogenic Avian Influenza (HPAI) affecting poultry in the U.S., Canada and other countries, which impacted the company's flocks in fiscal 2024 and again in March 2026

5. **Acquisition Integration** - Risks related to acquiring new flocks or businesses and the ability to successfully integrate and manage recently acquired businesses while realizing expected benefits such as synergies, cost savings, and margin expansion

6. **Operational Efficiency** - Ability to produce, supply, and distribute products efficiently and reliably

7. **Competition** - Ability to compete effectively with existing competitors and new market entrants, retain customers, and acquire new customers

8. **Regulatory and Market Reactions** - Government, customer, and consumer reactions to high market prices for eggs, including potential new regulations

9. **Macroeconomic Factors** - Changes in inflation, interest rates, and trade and tariff policies

10. **Intellectual Property** - Loss or expiration of registered trademarks or other intellectual property

11. **Legal Matters** - Adverse results in pending litigation

12. **Geopolitical Risks** - Global instability from geopolitical conflicts and other uncertainties

## Pre-written sections (judge input)

### Financial Health

Cal-Maine Foods trades at $62.70 with a market capitalization of $2.93 billion and generates $2.53 billion in annual revenue. The company's valuation appears stretched with a P/E ratio of 51.4x and forward P/E of 61.8x, significantly above industry averages, while profitability remains thin at a 2.32% net profit margin with only $58.7 million in net income. The elevated valuation multiples relative to modest earnings suggest the market is pricing in future growth or recovery in egg prices, though the company's exposure to commodity price volatility and operational risks (disease, feed costs, weather) presents downside risk. A 3.86% dividend yield provides some income support, but investors should monitor margin trends closely given the cyclical nature of the egg industry.

### Recent Developments

Cal-Maine Foods' most recent filings reveal ongoing operational challenges typical of the egg production industry, with the company facing volatility in wholesale shell egg prices, feed cost pressures, and demand fluctuations for specialty products like cage-free eggs. The company maintains an active share repurchase program, suggesting management confidence despite a challenging operating environment. However, the stock's elevated forward P/E ratio of 61.77x and thin profit margin of 2.32% indicate that current valuations may not fully reflect commodity price risks inherent in the business. Investors should monitor upcoming quarterly results for trends in feed costs and cage-free egg adoption rates, which will be critical to earnings sustainability.

### SEC Filing Highlights

Cal-Maine Foods, the nation's largest egg producer, is executing an aggressive growth strategy centered on prepared foods expansion and strategic acquisitions. The company acquired Echo Lake Foods ($289.5M), Creighton Brothers ($129.3M), and Van's Foods ($24.8M) to bolster its prepared foods portfolio, with capacity expected to grow over 30% through 2028. However, the company faces significant headwinds from Highly Pathogenic Avian Influenza (HPAI) outbreaks that impacted operations in late FY2024 and March 2026, creating operational disruptions and margin pressure. Recent acquisitions including ISE America have added approximately 8 million layers of capacity across multiple regions, supporting both conventional and specialty egg production. The company's vertical integration and strong balance sheet position it to weather commodity price volatility while pursuing its diversification into higher-margin prepared foods segments.

### Risk Factors

• **Avian Influenza and Operational Hazards** – Highly Pathogenic Avian Influenza (HPAI) outbreaks pose significant threats to flock health and production capacity, with the company experiencing impacts in fiscal 2024 and March 2026. Additional operational risks include disease, pests, weather events, and product recall potential across shell egg and prepared foods operations.

• **Commodity Price Volatility and Input Costs** – Wholesale shell egg prices and demand fluctuate significantly based on market conditions, while rising feed costs and other input expenses directly pressure margins. The company has limited ability to pass through cost increases to customers in a timely manner.

• **Specialty Product Demand and Competition** – Increasing consumer and retailer demand for cage-free and specialty eggs requires capital investment and operational changes. Intense competition from existing and new market entrants, combined with difficulty predicting specialty product demand, creates margin pressure and customer retention risks.

## Audited (Exec Summary + Outlook)

### Executive Summary
Cal-Maine Foods is the nation's largest egg producer, generating $2.53 billion in annual revenue, and is actively diversifying into prepared foods through acquisitions totaling over $440 million, with production capacity expected to grow over 30% through 2028. The stock is notable now because its valuation — a P/E of 51.4x and forward P/E of 61.8x — appears stretched relative to a thin 2.32% net profit margin, suggesting the market is pricing in a meaningful earnings recovery or successful execution of the prepared foods strategy that has yet to materialize in current results. The single most important near-term variable is the trajectory of HPAI outbreaks: further flock disruptions, as seen in fiscal 2024 and March 2026, would directly compress production capacity and margins at precisely the moment the company is integrating multiple large acquisitions.

### Outlook
The directional outlook for Cal-Maine Foods is **cautious**, with the investment thesis hinging on the successful convergence of several variables that remain difficult to predict. On the tailwind side, the company's vertical integration, strong balance sheet, and expanding prepared foods portfolio represent a credible long-term diversification away from pure commodity egg exposure, and the 3.86% dividend yield offers a degree of return while investors wait for that thesis to develop. However, the headwinds are meaningful and immediate: HPAI outbreak risk remains the most acute threat to watch, as further flock disruptions would simultaneously reduce production capacity and strain the integration of recently acquired operations. Investors should also monitor feed cost trends and wholesale shell egg price movements quarter to quarter, as the company's limited ability to pass through input cost increases means margin can deteriorate quickly. The pace of cage-free egg adoption — both consumer demand and the capital requirements to meet retailer mandates — will be a critical longer-term variable shaping whether the specialty segment becomes a margin driver or a drag. The view would become more constructive if HPAI pressures stabilize, feed costs moderate, and early prepared foods acquisitions demonstrate improving margin contribution; it would turn more negative if disease outbreaks recur at scale, egg prices weaken, or acquisition integration proves more costly than anticipated.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "generating $2.53 billion in annual revenue"
LABEL: SUPPORTED
REASON: Source data lists revenue as $2,528,636,928, which rounds to $2.53 billion; the pre-written Financial Health section also states "$2.53 billion in annual revenue."

---

CLAIM: "acquisitions totaling over $440 million"
LABEL: SUPPORTED
REASON: The three named acquisitions sum to $289.5M (Echo Lake) + $129.3M (Creighton Brothers) + $24.8M (Van's Foods) = $443.6M, which exceeds $440M; this arithmetic is fully derivable from the RAG SEC Highlights figures.

---

CLAIM: "production capacity expected to grow over 30% through 2028"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "Multiple capacity expansion projects underway expected to grow prepared foods production by more than 30% from mid-2027 through 2028."

---

CLAIM: "a P/E of 51.4x"
LABEL: SUPPORTED
REASON: Source data lists pe_ratio as 51.39344, which rounds to 51.4x; the pre-written Financial Health section also states "P/E ratio of 51.4x."

---

CLAIM: "forward P/E of 61.8x"
LABEL: SUPPORTED
REASON: Source data lists forward_pe as 61.7734, which rounds to 61.8x; the pre-written Financial Health section also states "forward P/E of 61.8x."

---

CLAIM: "a thin 2.32% net profit margin"
LABEL: SUPPORTED
REASON: Source data explicitly lists profit_margin_pct as 2.32; the pre-written Financial Health section also states "2.32% net profit margin."

---

CLAIM: "HPAI outbreaks: further flock disruptions, as seen in fiscal 2024 and March 2026"
LABEL: SUPPORTED
REASON: The RAG Risk Factors section explicitly states HPAI "impacted the company's flocks in fiscal 2024 and again in March 2026," and the RAG SEC Highlights corroborates "HPAI (Highly Pathogenic Avian Influenza) outbreak impacting operations in Q3-Q4 FY2024 and March 2026."

---

**OUTLOOK**

---

CLAIM: "the 3.86% dividend yield offers a degree of return"
LABEL: SUPPORTED
REASON: Source data explicitly lists dividend_yield as 3.86; the pre-written Financial Health section also states "A 3.86% dividend yield."

---

CLAIM: "HPAI outbreak risk remains the most acute threat to watch, as further flock disruptions would simultaneously reduce production capacity"
LABEL: SUPPORTED
REASON: This is a qualitative directional restatement of the explicitly disclosed HPAI risk factor present in both the RAG Risk Factors and RAG SEC Highlights sections; no unverifiable quantitative claim is embedded.

---

CLAIM: "feed cost trends and wholesale shell egg price movements quarter to quarter"
LABEL: SUPPORTED
REASON: Both feed cost pressures and wholesale shell egg price volatility are explicitly named as primary risk factors in the RAG Risk Factors and pre-written Risk Factors sections; this is a qualitative restatement of disclosed risks with no unverifiable quantitative claim embedded.

---

CLAIM: "the company's limited ability to pass through input cost increases"
LABEL: SUPPORTED
REASON: The pre-written Risk Factors section explicitly states "The company has limited ability to pass through cost increases to customers in a timely manner," which is drawn from the disclosed risk factors.

---

*No additional quantitative figures, price targets, thresholds, ratios, named product milestones, or forward-looking numbers appear in the Outlook section beyond those already evaluated above.*
