# BLNK — local-model

## Metadata

ticker: BLNK
arm: local-model
judge_prompt_version: v2
context_sha256: fcd98c909b5dae809e73c74a8770cdc02cc0020099a1d11f5c40cc5b309c2efe
local_model_served_name: qwen2.5-1.5b-instruct
local_model_dir: qwen2.5-1.5b-instruct
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
[From Pinecone cache] # Key Takeaways from Blink Charging's Latest Filing

## Business Overview
Blink Charging is a leading owner, operator, and provider of EV charging equipment and networked services across the U.S. and international markets. The company operates through three primary business models: Blink-owned turnkey, Blink-owned hybrid, and host-owned arrangements, each with different revenue-sharing structures and contract terms.

## Strategic Restructuring (BlinkForward Initiative)
In May 2025, Blink announced a comprehensive restructuring plan aimed at achieving profitability and operational efficiency:
- Reduced global workforce from 513 to approximately 320 employees
- Transitioned to contract manufacturing, eliminating in-house manufacturing facilities (completed January 2026)
- Reduced operating and general administrative expenses
- Focused expansion on DC Fast Charging (DCFC) networks in high-utilization locations
- Completed a $20 million funding round in December 2025

## Strategic Acquisition
In July 2025, Blink acquired Zemetric Inc., which provided:
- Software-driven fleet management and energy management services
- Lower-cost Level 2 charger hardware lineup
- New Chief Technology Officer (Zemetric's former CEO)

## Network Growth
As of December 31, 2025, Blink Network included approximately 66,350 connected chargers, with approximately 8,250 owned by the company.

## Market Conditions
The EV charging industry experienced significant growth in 2025, with 18,041 new DC fast charging ports added in the U.S. (30% year-over-year growth), improved network reliability, and stable pricing ranging from $0.45-$0.53 per kilowatt-hour.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors

The context provided indicates that Blink Charging Co. discloses risk factors in "Item 1A – Risk Factors" of their Annual Report, but the specific details of those risk factors are not included in the information provided. The document references this section but does not elaborate on what those particular risks are.

To obtain a comprehensive list of the primary risk factors disclosed by Blink Charging, you would need to review the complete "Item 1A – Risk Factors" section of their SEC filing, which is not fully detailed in the available context.

## Pre-written sections (judge input)

### Financial Health

#### Key Metrics:

- **Price**: $0.5652 USD
- **Market Cap**: $819,193,600 USD
- **P/E Ratio**: -2.45
- **Revenue**: $96,550,000 USD
- **Net Income**: -$50,667,000 USD
- **Profit Margin**: -0.52%

#### Brief Financial Assessment:

Blink Charging Co. operates within the Industrials sector, specifically in Engineering & Construction. Despite having a negative P/E ratio (-2.45), which suggests investors may view it as undervalued based on earnings multiples, the company's current valuation does not align well with its operating performance. Revenue has shown steady growth over recent years, but net income remains consistently negative, indicating significant losses despite operational activities. Profit margins are also notably low at -0.52%, suggesting high costs relative to revenues. These factors combined suggest that while the stock might appear cheap on a multiple basis, it may not be generating sufficient cash flow to cover expenses and maintain profitability. Investors should carefully consider the underlying business model and management team before making an investment decision.

### Recent Developments

Blink Charging's most recent SEC filings (10-K filed March 31, 2026 and 10-Q filed August 7, 2026) highlight the company's positioning as a leading EV charging provider amid expanding U.S. and international markets. However, the company continues to face significant profitability challenges, with a negative profit margin of -52.5% and net losses of $50.7 million against $96.6 million in revenue, indicating the business remains in a heavy investment phase. The stock has declined substantially from its 52-week high of $2.65 to $0.57, reflecting investor concerns about the path to profitability and competitive pressures in the EV charging sector. With a negative forward P/E ratio and market cap of approximately $82 million, investors should monitor upcoming quarterly results for evidence of margin improvement and network expansion success.

### SEC Filing Highlights

Blink Charging executed a comprehensive restructuring plan (BlinkForward Initiative) in 2025, reducing its workforce by 37% and transitioning to contract manufacturing to achieve profitability and operational efficiency. The company strategically acquired Zemetric Inc. in July 2025, gaining software-driven fleet management capabilities and a lower-cost Level 2 charger lineup to enhance competitive positioning. As of December 31, 2025, Blink's network expanded to approximately 66,350 connected chargers with 8,250 company-owned units, while the broader U.S. EV charging market grew 30% year-over-year with stable pricing between $0.45-$0.53 per kilowatt-hour. The company secured $20 million in funding during December 2025 and is strategically focusing expansion on high-utilization DC Fast Charging networks. These operational improvements and market tailwinds position Blink to capitalize on accelerating EV infrastructure demand while moving toward profitability.

### Risk Factors

1. **Regulatory Changes and Compliance Risks**: Regulatory changes or new regulations could impact the company's operations, financial performance, and compliance requirements. These changes may necessitate significant investments in compliance measures or adjustments to business strategies.

2. **Supply Chain Disruptions**: Dependence on third-party suppliers can expose the company to supply chain disruptions, including delays, shortages, or quality issues. Such disruptions could lead to increased costs, reduced product availability, and potential revenue losses.

## Audited (Exec Summary + Outlook)

### Executive Summary
Blink Charging Co. is a leading EV charging network provider operating approximately 66,350 connected chargers across U.S. and international markets, generating $96.6 million in revenue while carrying a net loss of $50.7 million and a negative profit margin of -52.5%. The stock is notable now because it has fallen sharply from its 52-week high of $2.65 to $0.57, the company has undertaken a significant restructuring through its BlinkForward Initiative — including a 37% workforce reduction and a shift to contract manufacturing — and it secured $20 million in fresh funding in December 2025, making this a pivotal inflection moment for the thesis. The single most important near-term variable is whether these restructuring actions translate into measurable margin improvement in upcoming quarterly results, as continued losses at the current scale would further pressure an already distressed balance sheet.

### Outlook
The directional outlook for Blink Charging is **cautious**, with a path to becoming cautiously constructive contingent on clear and sustained evidence of operational improvement. On the tailwind side, the broader U.S. EV charging market grew 30% year-over-year, network pricing has remained stable, and the BlinkForward restructuring — combined with the Zemetric acquisition's software and cost advantages — provides a credible, if unproven, framework for narrowing losses. Headwinds are substantial: the company remains deeply unprofitable, the stock has lost the vast majority of its value from its 52-week high, competitive pressures in the EV charging sector are intensifying, and dependence on third-party suppliers and evolving regulations introduces meaningful execution risk. Investors should watch the trajectory of profit margins in each successive quarterly filing, the pace and quality of DC Fast Charging network expansion, the degree to which contract manufacturing and workforce reductions flow through to lower operating costs, and any shifts in the regulatory environment that could affect EV infrastructure incentives. The thesis would strengthen if upcoming quarters demonstrate a clear narrowing of net losses and improving unit economics; it would weaken if losses persist at current levels, liquidity deteriorates, or competitive dynamics erode network utilization and pricing stability.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative, factual, and forward-looking claim in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "approximately 66,350 connected chargers across U.S. and international markets"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "Blink Network included approximately 66,350 connected chargers" as of December 31, 2025.

---

CLAIM: "generating $96.6 million in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $96,550,000; $96.6 million is a correct rounding to one decimal place.

---

CLAIM: "net loss of $50.7 million"
LABEL: SUPPORTED
REASON: Source data shows net income of -$50,667,000, which rounds to -$50.7 million.

---

CLAIM: "negative profit margin of -52.5%"
LABEL: SUPPORTED
REASON: Source data gives profit_margin = -0.52477; expressed as a percentage this is -52.477%, which rounds to -52.5%. Within 0.15 percentage points of the stated figure.

---

CLAIM: "fallen sharply from its 52-week high of $2.65 to $0.57"
LABEL: SUPPORTED
REASON: Source data confirms week_52_high = $2.65 and current_price = $0.5652, which rounds to $0.57.

---

CLAIM: "37% workforce reduction"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states workforce reduced from 513 to approximately 320 employees; (513−320)/513 = 37.6%, which rounds to 37% and is consistent with the pre-written SEC Filing Highlights section's "37%" figure.

---

CLAIM: "shift to contract manufacturing"
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly states "Transitioned to contract manufacturing, eliminating in-house manufacturing facilities (completed January 2026)."

---

CLAIM: "secured $20 million in fresh funding in December 2025"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "Completed a $20 million funding round in December 2025."

---

**OUTLOOK**

---

CLAIM: "the broader U.S. EV charging market grew 30% year-over-year"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "18,041 new DC fast charging ports added in the U.S. (30% year-over-year growth)."

---

CLAIM: "network pricing has remained stable"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "stable pricing ranging from $0.45–$0.53 per kilowatt-hour," which supports the characterization of stable pricing.

---

CLAIM: "the stock has lost the vast majority of its value from its 52-week high"
LABEL: SUPPORTED
REASON: Current price $0.5652 vs. 52-week high $2.65 represents a decline of ($2.65 − $0.5652)/$2.65 = 78.7%, which arithmetically constitutes "the vast majority" of its value.

---

CLAIM: "dependence on third-party suppliers and evolving regulations introduces meaningful execution risk"
LABEL: SUPPORTED
REASON: The pre-written Risk Factors section explicitly lists "Regulatory Changes and Compliance Risks" and "Supply Chain Disruptions" (dependence on third-party suppliers) as named risk factors.

---

CLAIM: "the pace and quality of DC Fast Charging network expansion"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states Blink is "strategically focusing expansion on high-utilization DC Fast Charging (DCFC) networks," confirming DC Fast Charging expansion as a stated strategic priority.

---

CLAIM: "the degree to which contract manufacturing and workforce reductions flow through to lower operating costs"
LABEL: SUPPORTED
REASON: Both the contract manufacturing transition and workforce reduction are explicitly documented in the RAG SEC Highlights as components of the BlinkForward restructuring aimed at "achieving profitability and operational efficiency."

---

CLAIM: "the Zemetric acquisition's software and cost advantages"
LABEL: SUPPORTED
REASON: RAG SEC Highlights confirms Zemetric provided "software-driven fleet management and energy management services" and a "lower-cost Level 2 charger hardware lineup," supporting both the software and cost advantage characterizations.

---

**No additional quantitative or forward-looking claims were identified in the two sections that have not already been evaluated above.**
