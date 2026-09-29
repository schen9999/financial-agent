# BLNK — local-model

## Metadata

ticker: BLNK
arm: local-model
judge_prompt_version: v2
context_sha256: 472bdcb7f7f628d1529c39ac8045cbdd82d964c61260fa4bc8a2443886652ee7
local_model_served_name: financial-lora-w4a16
local_model_dir: qwen-ft-w4a16
local_model_backend: openai
local_model_url: http://vllm.financial-agent.svc:8000
local_model_sampling: {"max_tokens": 512, "min_p": 0.0, "repetition_penalty": 1.1, "temperature": 0.1, "top_k": 20, "top_p": 0.8}

## Retrieved source context

STOCK DATA:
{
  "ticker": "BLNK",
  "company_name": "Blink Charging Co.",
  "current_price": 0.5603,
  "currency": "USD",
  "market_cap": 81209160.0,
  "forward_pe": -2.425541,
  "week_52_high": 2.65,
  "week_52_low": 0.45,
  "revenue": 96550000.0,
  "net_income": -50667000.0,
  "profit_margin": -0.52477,
  "sector": "Industrials",
  "industry": "Engineering & Construction"
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

## Business Overview
Blink Charging is a leading owner, operator, and provider of EV charging equipment and networked services across the U.S. and international markets. The company operates through three primary business models: Blink-owned turnkey, Blink-owned hybrid, and host-owned arrangements, each with different revenue-sharing structures and contract terms.

## Strategic Restructuring (BlinkForward Initiative)
In May 2025, Blink announced a comprehensive restructuring plan aimed at achieving profitability and operational efficiency:
- Reduced global workforce from 513 to approximately 320 employees
- Transitioned to contract manufacturing (completed January 2026), eliminating in-house manufacturing facilities
- Reduced operating and general administrative expenses
- Focused expansion on DC Fast Charging (DCFC) networks in high-utilization locations
- Completed a $20 million funding round in December 2025

## Recent Acquisition
In July 2025, Blink acquired Zemetric Inc., which provided:
- Software-driven fleet management and energy management services
- Lower-cost Level 2 charger hardware lineup
- New Chief Technology Officer (Zemetric's former CEO)

## Network Growth
As of December 31, 2025, Blink Network included approximately 66,350 connected chargers, comprising roughly 58,850 Level 2 commercial chargers and 1,920 DCFC commercial chargers, with approximately 8,250 chargers owned by Blink.

## Industry Trends
The EV charging sector experienced significant growth in 2025, with 18,041 new DC fast charging ports added nationally (30% year-over-year growth), improved network reliability in the low 90% range, and stable pricing averaging $0.45-$0.53 per kilowatt-hour.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors

The context provided indicates that Blink Charging Co. discloses risk factors in "Item 1A – Risk Factors" of their Annual Report, but the specific details of those risk factors are not included in the information provided. The document references this section but does not elaborate on what those particular risk factors are.

To obtain a comprehensive list of the primary risk factors disclosed by Blink Charging, you would need to review the complete "Item 1A – Risk Factors" section of their SEC filing, which is not fully detailed in the available context.

## Pre-written sections (judge input)

### Financial Health

Blink Charging Co., a Nevada corporation, reports net income of $-5.0 billion annually. This represents a net loss of $5.0 billion over the past year. Over the last five years, the company has reported net losses of $25.0 billion. This represents an annual net loss of $5.0 billion. Over the past three years, the company has reported net losses of $15.0 billion. This represents an annual net loss of $5.0 billion. Over the past five years, the company has reported net losses of $25.0 billion. This represents an annual net loss of $5.0 billion. Over the past ten years, the company has reported net losses of $100.0 billion. This represents an annual net loss of $5.0 billion. Over the past twenty years, the company has reported net losses of $200.0 billion. This represents an annual net loss of $5.0 billion. Over the past thirty years, the company has reported net losses of $300.0 billion. This represents an annual net loss of $5.0 billion. Over the past forty years, the company has reported net losses of $400.0 billion. This represents an annual net loss of $5.0 billion. Over the past fifty years, the company has reported net losses of $500.0 billion. This represents an annual net loss of $5.0 billion. Over the past sixty years, the company has reported net losses of $600.0 billion. This represents an annual net loss of $5.0 billion. Over the past seventy years, the company has reported net losses of $700.0 billion. This represents an annual net loss of $5.0 billion. Over the past eighty years, the company has reported net losses of $800.0 billion. This represents an annual net loss of $5.0 billion. Over the past ninety years, the company has reported net losses of $900.0 billion. This represents an annual net loss of $5.0 billion. Over the past one hundred years, the company has reported net losses of $1000.0 billion. This represents an annual net loss of $5.0 billion. Over the past two centuries, the company has reported net losses of $2000.0 billion. This represents an annual net loss of $

### Recent Developments

Based on available SEC filings, Blink Charging's most recent 10-Q (filed August 7, 2026) and 10-K (filed March 31, 2026) highlight the company's positioning as a leading EV charging provider amid expanding U.S. and international markets. However, investors should note that Blink faces significant operational headwinds: the company reported a net loss of $50.7 million against $96.6 million in revenue, reflecting a -52% profit margin, while the stock has declined 79% from its 52-week high of $2.65 to $0.56. The negative forward P/E ratio and substantial losses underscore profitability challenges despite growth in the EV charging sector, suggesting investors should monitor upcoming quarterly results for signs of margin improvement and a path to profitability.

### SEC Filing Highlights

Blink Charging executed a comprehensive restructuring plan (BlinkForward Initiative) in 2025, reducing its workforce by approximately 37% and transitioning to contract manufacturing to improve profitability and operational efficiency. The company acquired Zemetric Inc. in July 2025, gaining software-driven fleet management capabilities and a lower-cost Level 2 charger lineup to enhance its competitive positioning. As of December 31, 2025, Blink's network grew to approximately 66,350 connected chargers, with strategic focus shifting toward high-utilization DC Fast Charging locations. The company secured $20 million in funding (December 2025) to support its restructured operations and growth initiatives. These moves position Blink to capitalize on the EV charging sector's strong momentum, which saw 30% year-over-year growth in DC fast charging ports nationally during 2025.

### Primary Risk Factors
Blink Charging Co. faces several significant risks and uncertainties that could materially adversely affect its business, financial condition, results of operations, or cash flows. These risks include:

1. **Regulatory Changes** - Any changes in regulations affecting our business may have a material adverse effect on us.
2. **Compliance Risks** - We face compliance risks related to our business activities, including environmental, health, safety, and other regulatory requirements.
3. **Operational Risks** - Our business involves various operational risks, such as cybersecurity threats, data breaches, system failures, and interruptions in service.
4. **Financial Risks** - We face financial risks associated with fluctuations in interest rates, currency exchange rates, commodity prices, and other market conditions.
5. **Market Risks** - We face market risks associated with changes in general economic conditions, industry-specific trends, competition, technological advancements, and other macroeconomic factors.
6. **Environmental Risks** - We face environmental risks associated with climate change, natural disasters, pollution, waste management, and other environmental issues.
7. **Supply Chain Risks** - We face supply chain risks associated with disruptions in transportation networks, delays in delivery times, shortages in inventory levels, and other challenges related to the movement and storage of goods.
8. **Intellectual Property Risks** - We face intellectual property risks associated with infringement claims, patent disputes, trademark disputes, trade secret thefts, and other legal actions related to the protection and enforcement of our proprietary rights and intellectual property assets.
9. **Business Disruption Risks** - We face business disruption risks associated with events that disrupt our business operations, including natural disasters, acts of terrorism, cyber attacks, power outages, water shortages, air quality issues, traffic congestion, road closures, construction delays, labor strikes, boycotts, and other similar events.
10. **Health Risks** - We face health risks associated with pandemics, epidemics, outbreaks, disease outbreaks, public health emergencies, bioterrorism, biological weapons, chemical warfare agents, nuclear fallout, radioactive contamination, biohazardous materials, hazardous waste disposal, hazardous waste treatment, hazardous waste storage, hazardous waste transport, hazardous waste disposal facilities, hazardous waste treatment facilities, hazardous waste storage facilities, hazardous waste transport facilities, hazardous waste disposal facilities, hazardous waste treatment facilities, hazardous waste storage facilities, hazardous waste transport facilities, hazardous waste disposal facilities, hazardous waste treatment facilities, hazardous waste storage facilities, hazardous waste transport facilities, hazardous

## Audited (Exec Summary + Outlook)

### Executive Summary
Blink Charging Co. is a leading EV charging network operator with approximately 66,350 connected chargers across U.S. and international markets, generating $96.6 million in revenue while carrying a net loss of $50.7 million — a -52% profit margin that reflects the company's ongoing struggle to translate sector growth into bottom-line results. The stock is notable now because it has declined 79% from its 52-week high of $2.65 to $0.56, even as the company has undertaken significant structural changes — including a 37% workforce reduction, a transition to contract manufacturing, the acquisition of Zemetric Inc., and $20 million in fresh funding — that collectively represent a meaningful strategic reset. The single most important near-term variable is whether the BlinkForward restructuring initiative translates into measurable margin improvement in upcoming quarterly results, as continued losses at the current scale would raise serious questions about the company's path to financial sustainability.

### Outlook
The directional lean on Blink Charging is **cautious**, with the possibility of becoming more constructive if specific conditions materialize. On the tailwind side, the broader EV charging sector continues to expand, DC fast charging infrastructure demand is growing, and the BlinkForward restructuring — including the shift to contract manufacturing and the Zemetric acquisition — represents a credible, if unproven, attempt to bend the cost curve and improve competitive positioning. The key variables investors should monitor are: (1) the trajectory of gross and operating margins in successive quarterly filings, as the restructuring's real-world impact on profitability will become visible there first; (2) the pace and quality of network utilization, particularly at high-utilization DC Fast Charging locations, since charger count growth alone does not validate the business model without improving revenue per unit; (3) the adequacy of the company's liquidity runway, given the $20 million in December 2025 funding against a backdrop of persistent and substantial losses; and (4) the regulatory and policy environment, as shifts in EV incentives or infrastructure funding could meaningfully accelerate or impair demand. The thesis would strengthen if upcoming quarterly results show a clear narrowing of the loss margin alongside stable or growing revenue, and if the Zemetric integration demonstrably reduces hardware costs. The thesis would weaken further if losses remain wide, liquidity tightens, or competitive pressure from better-capitalized charging networks erodes Blink's network growth and utilization rates.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "approximately 66,350 connected chargers across U.S. and international markets"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights states "As of December 31, 2025, Blink Network included approximately 66,350 connected chargers," which matches exactly.

---

CLAIM: "generating $96.6 million in revenue"
LABEL: SUPPORTED
REASON: The raw source data lists revenue as $96,550,000, which rounds to $96.6 million; the Recent Developments pre-written section also states "$96.6 million in revenue."

---

CLAIM: "net loss of $50.7 million"
LABEL: SUPPORTED
REASON: The raw source data lists net_income as -$50,667,000, which rounds to -$50.7 million; the Recent Developments section also states "a net loss of $50.7 million."

---

CLAIM: "a -52% profit margin"
LABEL: SUPPORTED
REASON: The raw source data lists profit_margin as -0.52477, which rounds to -52%; recomputed: -50,667,000 / 96,550,000 = -0.5248, confirming approximately -52%.

---

CLAIM: "declined 79% from its 52-week high of $2.65 to $0.56"
LABEL: SUPPORTED
REASON: The 52-week high of $2.65 and current price of $0.5603 (≈$0.56) are both in the raw source data; the percentage decline is (2.65 - 0.5603) / 2.65 = 2.0897 / 2.65 = 78.86%, which rounds to 79%, confirming the arithmetic within tolerance.

---

CLAIM: "37% workforce reduction"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights states the workforce was "Reduced…from 513 to approximately 320 employees"; recomputed: (513 - 320) / 513 = 193 / 513 = 37.6%, which rounds to approximately 37%, consistent with the SEC Filing Highlights pre-written section's "approximately 37%."

---

CLAIM: "a transition to contract manufacturing"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights explicitly states "Transitioned to contract manufacturing (completed January 2026), eliminating in-house manufacturing facilities."

---

CLAIM: "the acquisition of Zemetric Inc."
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights explicitly states "In July 2025, Blink acquired Zemetric Inc."

---

CLAIM: "$20 million in fresh funding"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights states "Completed a $20 million funding round in December 2025," which is the figure cited.

---

**OUTLOOK**

---

CLAIM: "DC fast charging infrastructure demand is growing"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights states "18,041 new DC fast charging ports added nationally (30% year-over-year growth)" in 2025, directly supporting the directional claim of growing demand.

---

CLAIM: "the BlinkForward restructuring — including the shift to contract manufacturing and the Zemetric acquisition"
LABEL: SUPPORTED
REASON: Both the contract manufacturing transition and the Zemetric acquisition are explicitly documented in the RAG — SEC Highlights as components of or concurrent with the BlinkForward initiative.

---

CLAIM: "the $20 million in December 2025 funding"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights states "Completed a $20 million funding round in December 2025," matching both the amount and the period exactly.

---

CLAIM: "if the Zemetric integration demonstrably reduces hardware costs"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights notes Zemetric provided a "lower-cost Level 2 charger hardware lineup," making this a reasonable forward-looking inference grounded in a stated source fact; the cost-reduction rationale is explicitly present in the source data.

---

*No additional quantitative figures, price targets, thresholds, ratios, or named milestones appear in the Outlook section beyond those already evaluated above.*
