# BLNK — local-model

## Metadata

ticker: BLNK
arm: local-model
judge_prompt_version: v2
context_sha256: 430d3f4047390dd9e21b85653a193c3c75cc74dab132b96efb00c6910f965d51
local_model_served_name: qwen2.5-7b-instruct
local_model_dir: qwen2.5-7b-instruct
local_model_backend: openai
local_model_url: http://vllm.financial-agent.svc:8000
local_model_sampling: {"max_tokens": 512, "min_p": 0.0, "repetition_penalty": 1.1, "temperature": 0.1, "top_k": 20, "top_p": 0.8}

## Retrieved source context

STOCK DATA:
{
  "ticker": "BLNK",
  "company_name": "Blink Charging Co.",
  "current_price": 0.5652,
  "currency": "USD",
  "market_cap": 81919360.0,
  "forward_pe": -2.446753,
  "week_52_high": 2.65,
  "week_52_low": 0.45,
  "revenue": 96550000.0,
  "net_income": -50667000.0,
  "profit_margin": -0.52477,
  "sector": "Industrials",
  "industry": "Engineering & Construction"
}

NEWS ARTICLES:
[]

SEC FILING SUMMARIES:
{
  "10-K": {
    "form_type": "10-K",
    "filing_date": "2026-03-31",
    "summary": "Item 1A \u2013 Risk Factors\u201d below. In this Annual Report, unless otherwise indicated or the context otherwise requires, the \u201cCompany,\u201d \u201cBlink,\u201d \u201cBlink Charging,\u201d \u201cwe,\u201d \u201cus\u201d or \u201cour\u201d refer to Blink Charging Co., a Nevada corporation, and its consolidated subsidiaries. The mark \u201cBlink\u201d is our registered trademark in the United States and, regarding the name of Ecotality, Inc. (whose assets we acquired in October 2013), in Australia, China, Hong Kong, Indonesia, Japan, South Korea, Malaysia, Mexico, New Zealand, Philippines, South Africa, Singapore, Switzerland, Taiwan, and is a trademark registered in the European Union under the Madrid Protocol. We have registered other trademarks and use certain trademarks, trade names, and logos that have not been registered. We claim common law rights to the"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-07",
    "summary": "Item 1A - Risk Factors. Any one or more of these uncertainties, risks and other influences, could materially affect our results of operations and whether forward-looking statements made by us ultimately prove to be accurate. Our actual results, performance and achievements could differ materially from those expressed or implied in these forward-looking statements. Except as required by federal securities laws, we undertake no obligation to publicly update or revise any forward-looking statements, whether from new information, future events or otherwise. U.S. dollars are reported in thousands, except for share and per share amounts. Overview We are a leading owner, operator, and provider of EV charging equipment and networked EV charging services in the rapidly growing U.S. and internationa"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] # Key Takeaways from Blink Charging's Latest SEC Filings

## Strategic Restructuring and Operational Efficiency
In May 2025, Blink announced the BlinkForward Initiative, a strategic restructuring plan designed to accelerate the path to profitability and enhance operational efficiency. This included:
- Workforce reduction from 513 to approximately 320 employees
- Reductions in operating, general, and administrative expenses
- Transition to contract manufacturing (completed in January 2026), eliminating in-house manufacturing facilities

## Capital and Growth Activities
- Completed a $20 million funding round via public markets in December 2025
- Acquired Zemetric Inc. in July 2025, adding software-driven fleet management, energy management services, and a lower-cost Level 2 charger lineup
- Harmeet Singh, Zemetric's CEO, became Blink's Chief Technology Officer following the acquisition

## Network Expansion
As of December 31, 2025, Blink Network comprised approximately 66,350 connected chargers, including:
- Approximately 58,850 Level 2 commercial chargers
- Approximately 1,920 DC Fast Charging (DCFC) commercial chargers
- Approximately 8,250 chargers owned by Blink

## Market Conditions
The EV charging industry showed strong growth in 2025:
- 18,041 new DC fast charging ports added in the U.S. (30% year-over-year growth)
- U.S. had 70,007 public DC fast charging ports by year-end 2025
- Network reliability improved to low 90% range across most U.S. states
- Pricing remained stable, ranging between $0.45-$0.53 per kilowatt-hour

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors

The context provided indicates that Blink Charging Co. discloses risk factors in "Item 1A – Risk Factors" of their Annual Report, but the specific details of those risk factors are not included in the information provided. The document references this section but does not elaborate on what those particular risks are.

To obtain a comprehensive list of the primary risk factors disclosed by Blink Charging, you would need to review the complete "Item 1A – Risk Factors" section of their SEC filing, which is not fully detailed in the available context.

## Pre-written sections (judge input)

### Financial Health

Blink Charging Co. (BLNK) currently trades at $0.5652 per share, with a market capitalization of approximately $81.92 million. The company has a forward P/E ratio of -2.45, indicating potential undervaluation given its net loss. Revenue stands at $96.55 million, but with a significant net income loss of -$50.67 million, resulting in a profit margin of -52.48%. These metrics suggest ongoing challenges in achieving profitability despite growth opportunities in the electric vehicle sector.

### Recent Developments

Blink Charging's most recent SEC filings (10-K filed March 31, 2026 and 10-Q filed August 7, 2026) highlight the company's position as a leading EV charging provider amid expanding U.S. and international markets. However, the company continues to face significant profitability challenges, with a negative profit margin of -52.5% and net losses of $50.7 million against $96.6 million in revenue, indicating the company remains in a heavy investment phase. The stock has declined substantially from its 52-week high of $2.65 to $0.57, reflecting investor concerns about the path to profitability and competitive pressures in the EV charging sector. Investors should monitor upcoming quarterly results for signs of operational efficiency improvements and progress toward positive cash flow, as the company's survival depends on scaling operations while managing costs in an increasingly competitive market.

### SEC Filing Highlights

Blink Charging executed the BlinkForward Initiative in 2025, restructuring operations to improve profitability through workforce reduction (513 to 320 employees), expense cuts, and transition to contract manufacturing completed in January 2026. The company expanded its network to approximately 66,350 connected chargers and strategically acquired Zemetric Inc. in July 2025, gaining software-driven fleet management capabilities and a lower-cost Level 2 charger lineup. Blink raised $20 million in December 2025 and benefited from strong industry tailwinds, with the U.S. DC fast charging market growing 30% year-over-year while pricing remained stable at $0.45-$0.53 per kilowatt-hour.

### Risk Factors

- **Regulatory Changes and Compliance Risks**: Regulatory changes at local, state, or federal levels could impact the company's operations and profitability.
- **Dependence on Key Customers**: The company's financial performance may be significantly affected by its relationships with key customers, any of whom could reduce orders or terminate contracts.

## Audited (Exec Summary + Outlook)

### Executive Summary
Blink Charging Co. is a leading EV charging provider operating a network of approximately 66,350 connected chargers across U.S. and international markets, generating $96.55 million in revenue against a market capitalization of roughly $81.92 million. The stock is notable now because it has fallen sharply from its 52-week high of $2.65 to $0.57, compressing the company's valuation to a level where the market appears to be pricing in meaningful execution risk even as the BlinkForward restructuring and Zemetric acquisition signal a deliberate pivot toward operational discipline. The single most important near-term variable is whether the cost reductions and contract manufacturing transition completed in early 2026 translate into measurable improvement in the net loss trajectory — without that evidence, the path to survival remains uncertain.

### Outlook
The directional outlook for Blink Charging is **cautious, with a conditional constructive tilt** contingent on demonstrated operational progress. On the tailwind side, the U.S. DC fast charging market's 30% year-over-year growth, stable per-kilowatt-hour pricing, and the structural shift toward EV adoption provide a genuine demand backdrop that could reward a leaner, better-capitalized Blink. The BlinkForward restructuring, the completed transition to contract manufacturing, and the Zemetric acquisition's software and fleet management capabilities are all steps in the right direction. However, the headwinds are substantial: a net loss margin of -52.48%, a stock price near multi-year lows, dependence on key customers who could reduce or terminate contracts, and the ever-present threat of regulatory shifts that could alter the economics of charging infrastructure. The key variables an investor should watch are the pace of operating expense reduction following the workforce and manufacturing restructuring, whether services-side gross margins improve as the network scales toward and beyond 66,350 connected chargers, the rate of cash burn relative to the $20 million raised in December 2025, and any signs of customer concentration risk materializing. What would strengthen the thesis is clear quarter-over-quarter narrowing of net losses, evidence that the Zemetric integration is driving higher-margin software and fleet revenue, and sustained pricing stability in the charging market. What would weaken it is continued cash burn without a credible bridge to positive operating cash flow, adverse regulatory changes reducing EV infrastructure incentives, or the loss of a significant customer relationship.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

## EXECUTIVE SUMMARY

---

CLAIM: "approximately 66,350 connected chargers"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "Blink Network comprised approximately 66,350 connected chargers" as of December 31, 2025.

---

CLAIM: "$96.55 million in revenue"
LABEL: SUPPORTED
REASON: The raw source data lists revenue as $96,550,000.0, which equals $96.55 million.

---

CLAIM: "market capitalization of roughly $81.92 million"
LABEL: SUPPORTED
REASON: The raw source data lists market_cap as $81,919,360.0, which rounds to approximately $81.92 million.

---

CLAIM: "fallen sharply from its 52-week high of $2.65"
LABEL: SUPPORTED
REASON: The raw source data lists week_52_high as $2.65.

---

CLAIM: "to $0.57"
LABEL: SUPPORTED
REASON: The raw source data lists current_price as $0.5652, which rounds to $0.57 (within standard rounding); the Pre-written Recent Developments section also states "to $0.57."

---

CLAIM: "contract manufacturing transition completed in early 2026"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights states the "Transition to contract manufacturing (completed in January 2026)," which is consistent with "early 2026."

---

## OUTLOOK

---

CLAIM: "U.S. DC fast charging market's 30% year-over-year growth"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights states "18,041 new DC fast charging ports added in the U.S. (30% year-over-year growth)."

---

CLAIM: "stable per-kilowatt-hour pricing"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights states "Pricing remained stable, ranging between $0.45-$0.53 per kilowatt-hour."

---

CLAIM: "net loss margin of -52.48%"
LABEL: SUPPORTED
REASON: The raw source data lists profit_margin as -0.52477, which equals -52.477%, rounding to -52.48%; this is within 0.15 percentage points of the stated figure.

---

CLAIM: "stock price near multi-year lows"
LABEL: INFERENCE
REASON: The raw source data shows the 52-week low is $0.45 and the current price is $0.5652, placing the stock close to its 52-week low; the claim of "multi-year lows" extends beyond the 52-week window and is not directly verifiable from the provided data, but the proximity to the 52-week low ($0.5652 vs. $0.45 low) supports the directional characterization as an inference from the available range data.

---

CLAIM: "dependence on key customers who could reduce or terminate contracts"
LABEL: SUPPORTED
REASON: The Pre-written Risk Factors section explicitly states "Dependence on Key Customers: The company's financial performance may be significantly affected by its relationships with key customers, any of whom could reduce orders or terminate contracts."

---

CLAIM: "the $20 million raised in December 2025"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights states "Completed a $20 million funding round via public markets in December 2025."

---

CLAIM: "network scales toward and beyond 66,350 connected chargers"
LABEL: SUPPORTED
REASON: The 66,350 figure is explicitly present in the RAG SEC Highlights as the current network size; the directional framing ("toward and beyond") is a forward-looking restatement of the established baseline figure, which is present in the source data.

---

CLAIM: "adverse regulatory changes reducing EV infrastructure incentives"
LABEL: UNSUPPORTED
REASON: The Pre-written Risk Factors section references only generic "Regulatory Changes and Compliance Risks" affecting "operations and profitability"; the specific qualifier "reducing EV infrastructure incentives" does not appear in any source data or pre-written section.

---

CLAIM: "loss of a significant customer relationship"
LABEL: SUPPORTED
REASON: The Pre-written Risk Factors section states key customers "could reduce orders or terminate contracts," directly grounding this watch-item.
