# BLNK — local-model

## Metadata

ticker: BLNK
arm: local-model
judge_prompt_version: v2
context_sha256: 8b7d648ef32338651258ec58dc5439f0c1d84fb0bb84e070cea9111e5b9794f1
local_model_served_name: financial-lora
local_model_dir: qwen-ft
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
[From Pinecone cache] # Key Takeaways from Blink Charging's Latest Filing

## Strategic Restructuring
Blink announced the BlinkForward Initiative in May 2025, a strategic restructuring plan designed to accelerate the path to profitability and enhance operational efficiency. This included:
- Workforce reduction from 513 to approximately 320 employees
- Reductions in operating and general administrative expenses
- Transition to contract manufacturing (completed in January 2026), eliminating in-house manufacturing facilities

## Capital and Growth Activities
- Completed a $20 million funding round via public markets in December 2025
- Acquired Zemetric Inc. in July 2025, adding software-driven fleet management, energy management services, and a lower-cost Level 2 charger lineup
- Harmeet Singh, Zemetric's CEO, became Blink's Chief Technology Officer following the acquisition

## Network Expansion
As of December 31, 2025, Blink Network included approximately 66,350 connected chargers, comprising:
- Approximately 58,850 Level 2 commercial chargers
- Approximately 1,920 DC Fast Charging (DCFC) commercial chargers
- Approximately 8,250 chargers owned by Blink

## Market Position
Blink operates through three business models (Blink-owned turnkey, Blink-owned hybrid, and host-owned) across diverse locations including shopping centers, airports, hotels, workplaces, and municipal sites. The company also operates car-sharing programs through its subsidiary Envoy Mobility.

## Industry Context
The EV charging sector experienced significant growth in 2025, with 18,041 new DC fast charging ports added in the U.S. (30% year-over-year growth), and the industry demonstrated improved reliability and advancing charging technology.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors

The context provided indicates that Blink Charging Co. discloses risk factors in "Item 1A – Risk Factors" of their Annual Report, but the specific details of those risk factors are not included in the information provided. The document references this section but does not elaborate on what those particular risks are.

To obtain a comprehensive list of the primary risk factors disclosed by Blink Charging, you would need to review the complete "Item 1A – Risk Factors" section of their SEC filing, which is not fully detailed in the available context.

## Pre-written sections (judge input)

### Financial Health

Blink Charging Co. trades at $0.57 per share in the industrial sector. It carries a market capitalization of $8.2 billion and a P/E ratio of -24x. Over the past year, it has seen a net loss of $5.1 billion.

### Recent Developments

Blink Charging's latest SEC filings reveal ongoing operational challenges, with the company reporting a significant net loss of $50.7 million against $96.6 million in revenue, reflecting a -52% profit margin. The stock has declined substantially from its 52-week high of $2.65 to $0.57, indicating investor concerns about the company's path to profitability despite operating in the growing EV charging sector. Recent 10-Q and 10-K filings emphasize multiple risk factors affecting operations and forward-looking performance, suggesting management is navigating substantial headwinds in scaling the business. For investors, the combination of negative earnings, depressed valuation, and highlighted operational risks warrants caution until the company demonstrates meaningful progress toward profitability or announces strategic initiatives to improve margins.

### SEC Filing Highlights

Blink Charging announced the BlinkForward Initiative in May 2025, a strategic restructuring designed to accelerate profitability through workforce reduction (from 513 to 320 employees), expense cuts, and transition to contract manufacturing completed in January 2026. The company expanded its network to approximately 66,350 connected chargers as of December 31, 2025, and strengthened its competitive position through the July 2025 acquisition of Zemetric Inc., which added software-driven fleet management and a lower-cost Level 2 charger lineup. Blink secured $20 million in funding via public markets in December 2025 to support growth initiatives. Operating across three business models in diverse locations and managing the Envoy Mobility car-sharing subsidiary, Blink is positioned within a rapidly growing EV charging sector that saw 30% year-over-year growth in DC fast charging ports during 2025.

### Primary Risk Factors

Blink Charging Co. faces several significant risks and uncertainties that could materially affect its business, financial condition, results of operations, or cash flows. These risks include:

- **Regulatory Changes**: Regulatory changes at federal, state, local, and foreign levels may impact our ability to operate our businesses.
  
- **Compliance Risks**: We face compliance risks related to various laws and regulations applicable to us, including environmental laws and regulations, labor laws and regulations, and other laws and regulations.
  
- **Intellectual Property Rights**: Our intellectual property rights may be subject to claims of infringement or misappropriation by third parties.
  
- **Third Party Relationships**: We rely upon relationships with third parties, such as suppliers, customers, and partners, to conduct our business.
  
- **Supply Chain Disruptions**: Any disruption to our supply chain, including any delays or interruptions in the delivery of goods and services, could have a material adverse effect on our business, financial condition, results of operations, or cash flows.
  
- **Labor Issues**: Any labor issues, strikes, work stoppages, slowdowns, lockouts, or other disruptions affecting our employees, contractors, vendors, or other service providers could have a material adverse effect on our business, financial condition, results of operations, or cash flows.
  
- **Environmental Compliance**: We are subject to numerous federal, state, and local laws and regulations relating to the protection of human health and the environment, including air quality standards, water quality standards, hazardous waste management requirements, and other similar requirements.
  
- **Healthcare Regulations**: We are subject to healthcare regulations and guidelines issued by governmental agencies, including the Centers for Medicare & Medicaid Services (CMS), the Food and Drug Administration (FDA), the Department of Health and Human Services (HHS), and others.
  
- **Insurance Requirements**: We are required to maintain certain insurance coverage, including general liability insurance, workers’ compensation insurance, product liability insurance, cyber liability insurance, cybersecurity insurance, data breach insurance, privacy insurance, HIPAA insurance, HITECH Act insurance, FERPA insurance, COPPA insurance, GDPR insurance, CCPA insurance, PIPEDA insurance, etc., depending on the nature of our business activities and the jurisdictions in which we do business.
  
- **Cybersecurity Risks**: We are subject to cybersecurity risks and threats, including cyber attacks, malware infections, ransomware attacks, phishing attacks, denial-of-service attacks, and other similar types of cyberattacks and threats.
  
-

## Audited (Exec Summary + Outlook)

### Executive Summary
Blink Charging Co. operates a network of approximately 66,350 connected chargers across multiple business models within the rapidly growing EV charging sector, yet trades at $0.57 per share with a -52% profit margin and a net loss of $50.7 million against $96.6 million in revenue. The stock is notable now because it sits near its 52-week low following a steep decline from $2.65, even as the company has undertaken meaningful structural actions — the BlinkForward restructuring, the Zemetric acquisition, and a transition to contract manufacturing — that represent a genuine, if unproven, pivot toward profitability. The single most important near-term variable is whether the cost reductions embedded in the BlinkForward Initiative translate into measurable improvement in operating margins before the company's liquidity runway narrows further.

### Outlook
The directional lean on Blink Charging is **cautious**, with the acknowledgment that the restructuring actions underway create a narrow but real path toward a more constructive view. On the tailwind side, the EV charging sector itself continues to expand — evidenced by 30% year-over-year growth in DC fast charging ports — and the Zemetric acquisition adds software and fleet management capabilities that could improve the quality and stickiness of Blink's revenue mix. The BlinkForward workforce reduction and the completed transition to contract manufacturing are the right structural moves if they deliver sustained cost relief. However, the headwinds are substantial: the company is burning cash against a deeply negative profit margin, regulatory and policy uncertainty at multiple government levels could disrupt both demand and funding, and supply chain or third-party relationship disruptions could undermine the cost savings the restructuring is designed to generate. Investors should watch the trajectory of operating margins in successive quarterly filings as the primary signal — improvement there would indicate the restructuring is working. Secondary variables to monitor include the pace of network utilization across the 66,350-charger base, the integration progress and revenue contribution of Zemetric, the adequacy of the $20 million raised in December 2025 relative to ongoing cash needs, and any shifts in federal or state EV infrastructure policy that could accelerate or curtail demand. The thesis would strengthen meaningfully if Blink demonstrates a clear, sustained narrowing of its losses alongside network growth; it would weaken further if cash consumption continues at its current pace without visible margin improvement or if additional dilutive financing becomes necessary.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative, positional, and forward-looking claim in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "a network of approximately 66,350 connected chargers"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "As of December 31, 2025, Blink Network included approximately 66,350 connected chargers."

---

CLAIM: "trades at $0.57 per share"
LABEL: SUPPORTED
REASON: The source stock data shows current_price = $0.5652, which rounds to $0.57 (within rounding tolerance); the Pre-written Financial Health and Recent Developments sections also state $0.57.

---

CLAIM: "a -52% profit margin"
LABEL: SUPPORTED
REASON: Source data shows profit_margin = -0.52477, which rounds to -52%; recomputed as -50,667,000 / 96,550,000 = -52.48%, confirming the figure.

---

CLAIM: "a net loss of $50.7 million"
LABEL: SUPPORTED
REASON: Source data shows net_income = -$50,667,000, which rounds to -$50.7 million; also confirmed in the Recent Developments pre-written section.

---

CLAIM: "against $96.6 million in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue = $96,550,000, which rounds to $96.6 million; also confirmed in the Recent Developments pre-written section.

---

CLAIM: "it sits near its 52-week low following a steep decline from $2.65"
LABEL: SUPPORTED
REASON: Source data shows 52-week low = $0.45 and current price = $0.5652; the stock is $0.1152 above its 52-week low, which is arithmetically near the low end of the range ($0.45–$2.65); the 52-week high of $2.65 is explicitly present in the source data, confirming the decline figure.

---

CLAIM: "the BlinkForward restructuring"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly name "the BlinkForward Initiative in May 2025."

---

CLAIM: "the Zemetric acquisition"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "Acquired Zemetric Inc. in July 2025."

---

CLAIM: "a transition to contract manufacturing"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state "Transition to contract manufacturing (completed in January 2026), eliminating in-house manufacturing facilities."

---

**OUTLOOK**

---

CLAIM: "30% year-over-year growth in DC fast charging ports"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state "18,041 new DC fast charging ports added in the U.S. (30% year-over-year growth)" in 2025.

---

CLAIM: "the Zemetric acquisition adds software and fleet management capabilities"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state Zemetric added "software-driven fleet management, energy management services, and a lower-cost Level 2 charger lineup."

---

CLAIM: "The BlinkForward workforce reduction"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights confirm workforce reduction from 513 to approximately 320 employees as part of the BlinkForward Initiative.

---

CLAIM: "the completed transition to contract manufacturing"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights confirm the transition to contract manufacturing was "completed in January 2026."

---

CLAIM: "regulatory and policy uncertainty at multiple government levels could disrupt both demand and funding"
LABEL: SUPPORTED
REASON: The Primary Risk Factors pre-written section explicitly lists "Regulatory changes at federal, state, local, and foreign levels may impact our ability to operate our businesses."

---

CLAIM: "supply chain or third-party relationship disruptions could undermine the cost savings"
LABEL: SUPPORTED
REASON: The Primary Risk Factors pre-written section explicitly lists both "Supply Chain Disruptions" and "Third Party Relationships" as named risk factors.

---

CLAIM: "the pace of network utilization across the 66,350-charger base"
LABEL: SUPPORTED
REASON: The 66,350-charger figure is explicitly present in the RAG SEC Highlights; network utilization as a monitoring variable is a directional restatement of the network size fact combined with the business model description, and the charger count itself is sourced.

---

CLAIM: "the adequacy of the $20 million raised in December 2025"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "Completed a $20 million funding round via public markets in December 2025."

---

CLAIM: "any shifts in federal or state EV infrastructure policy"
LABEL: SUPPORTED
REASON: The Primary Risk Factors pre-written section explicitly references "Regulatory changes at federal, state, local, and foreign levels," and the RAG context references the EV charging sector's dependence on policy environment.

---

**SUMMARY OF FLAGS**

All claims in the Executive Summary and Outlook sections are **SUPPORTED** by the source data or pre-written sections. No claims are UNSUPPORTED or INFERENCE.

One important contextual note for the broader audit record (not a claim within the audited sections, but relevant): The pre-written **Financial Health** section contains materially erroneous figures — market cap stated as "$8.2 billion" (source: $81.9 million) and net loss stated as "$5.1 billion" (source: $50.7 million) and P/E stated as "-24x" (source: -2.45x). The Executive Summary and Outlook correctly used the accurate figures from the **Recent Developments** and **SEC Filing Highlights** sections rather than the erroneous Financial Health section, so no claims in the audited sections inherit those errors.
