# BLNK — baseline

## Metadata

ticker: BLNK
arm: baseline
judge_prompt_version: v2
context_sha256: f2f024e32d2b766f4ba98f68a1d0db33d26e342029486621fcf0c1344eeb4fda
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 415, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.79, "latency_s_total": 4.79, "parse_failure": 0, "prompt_tokens": 3389, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 127, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.639, "latency_s_total": 1.639, "parse_failure": 0, "prompt_tokens": 2926, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 151, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.049, "latency_s_total": 2.049, "parse_failure": 0, "prompt_tokens": 712, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 205, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.57, "latency_s_total": 2.57, "parse_failure": 0, "prompt_tokens": 705, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 154, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.991, "latency_s_total": 1.991, "parse_failure": 0, "prompt_tokens": 202, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 180, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.861, "latency_s_total": 1.861, "parse_failure": 0, "prompt_tokens": 498, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1177, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 16.931, "latency_s_total": 16.931, "parse_failure": 0, "prompt_tokens": 1788, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "BLNK",
  "company_name": "Blink Charging Co.",
  "current_price": 0.5607,
  "currency": "USD",
  "market_cap": 81267144.0,
  "forward_pe": -2.4272726,
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

## Business Overview
Blink Charging is a leading owner, operator, and provider of EV charging equipment and networked services across the U.S. and international markets. The company operates through three primary business models: Blink-owned turnkey, Blink-owned hybrid, and host-owned arrangements, each with different revenue-sharing structures and contract terms.

## Strategic Restructuring - BlinkForward Initiative
In May 2025, Blink announced the BlinkForward Initiative, a comprehensive restructuring plan focused on:
- Reducing global workforce from 513 to approximately 320 employees
- Cutting operating and general administrative expenses
- Transitioning to contract manufacturing (completed January 2026)
- Focusing on intellectual property and customer experience
- Expanding DC Fast Charging (DCFC) network deployment

## Financial and Growth Actions
- Completed a $20 million funding round via public markets in December 2025
- Acquired Zemetric Inc. in July 2025 to fill product gaps in fleet management, energy management services, and lower-cost Level 2 chargers

## Network Expansion
As of December 31, 2025, Blink Network included approximately 66,350 connected chargers, comprising:
- ~58,850 Level 2 commercial chargers
- ~1,920 DCFC commercial chargers
- ~8,250 chargers owned by Blink

## Industry Context
The EV charging sector experienced significant growth in 2025, with 18,041 new DC fast charging ports added in the U.S. (30% year-over-year growth), improved network reliability in the low 90% range, and stable pricing between $0.45-$0.53 per kilowatt-hour.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors

The context provided indicates that Blink Charging Co. discloses risk factors in "Item 1A – Risk Factors" of their Annual Report, but the specific details of those risk factors are not included in the information provided. The document references this section but does not elaborate on what those particular risk factors are.

To obtain a comprehensive list of the primary risk factors disclosed by Blink Charging, you would need to review the complete "Item 1A – Risk Factors" section of their SEC filing, which is not fully detailed in the available context.

## Pre-written sections (judge input)

### Financial Health

Blink Charging trades at $0.56 with a market capitalization of $81.3 million, reflecting significant financial distress. The company generated $96.6 million in revenue but posted a net loss of $50.7 million, resulting in a negative profit margin of -52.5%, indicating substantial operational losses. The negative forward P/E ratio further underscores unprofitability, while the stock's 52-week range ($0.45–$2.65) demonstrates extreme volatility. Despite revenue growth in the EV charging sector, Blink's inability to achieve profitability raises concerns about its path to sustainable operations and investor returns.

### Recent Developments

Blink Charging's most recent SEC filings (10-Q filed August 7, 2026, and 10-K filed March 31, 2026) highlight the company's positioning as a leading EV charging provider amid rapid market growth in the U.S. and international markets. However, the company continues to face significant profitability challenges, with a negative profit margin of -52.5% and net losses of $50.7 million against $96.6 million in revenue, indicating the company remains in a heavy investment phase. The stock has declined substantially from its 52-week high of $2.65 to $0.56, reflecting investor concerns about the path to profitability and competitive pressures in the EV charging sector. Investors should monitor upcoming quarterly results for signs of operational efficiency improvements and progress toward positive cash flow, as the company's survival depends on scaling operations while managing burn rate.

### SEC Filing Highlights

Blink Charging operates a network of approximately 66,350 connected chargers as of December 31, 2025, with strategic focus on expanding its DC Fast Charging (DCFC) infrastructure amid robust industry growth. The company implemented the BlinkForward Initiative in May 2025, reducing its workforce by approximately 37% and transitioning to contract manufacturing to improve operational efficiency and profitability. Blink secured $20 million in funding through public markets in December 2025 and acquired Zemetric Inc. in July 2025 to enhance its product portfolio with fleet management and energy management capabilities. The EV charging sector demonstrated strong momentum with 30% year-over-year growth in new DC fast charging ports, supporting Blink's expansion strategy in a favorable market environment.

### Risk Factors

• **Dependence on EV Market Growth and Adoption** – Blink's revenue is heavily tied to electric vehicle adoption rates and charging infrastructure demand, which remain subject to regulatory changes, fuel price fluctuations, and consumer preference shifts.

• **Capital Intensity and Funding Requirements** – Expanding the charging network requires significant ongoing capital investment; inability to secure adequate financing or achieve profitability could constrain growth and dilute shareholder value.

• **Competitive Landscape and Pricing Pressure** – Intensifying competition from larger players (Tesla, ChargePoint) and new market entrants may compress margins and limit market share gains in an increasingly crowded EV charging sector.

## Audited (Exec Summary + Outlook)

### Executive Summary
Blink Charging is a leading EV charging network operator with approximately 66,350 connected chargers and $96.6 million in revenue, competing in a sector experiencing 30% year-over-year growth in new DC fast charging ports. The stock is notable now precisely because of the tension between that industry tailwind and the company's severe financial distress — trading at $0.56 with an $81.3 million market cap, a net loss of $50.7 million, and a -52.5% profit margin that raises legitimate questions about long-term viability. The single most important near-term variable is whether the BlinkForward Initiative — which cut the workforce by approximately 37% and shifted to contract manufacturing — translates into measurable improvement in operational efficiency and a credible trajectory toward positive cash flow.

### Outlook
The directional lean on Blink Charging is **cautious**, with the acknowledgment that a narrow but real path to improvement exists. On the tailwind side, the broader EV charging sector continues to grow rapidly, the BlinkForward restructuring represents a meaningful structural cost reduction, and the Zemetric acquisition adds fleet and energy management capabilities that could differentiate Blink's offering over time. Against that, the headwinds are substantial: the company is burning cash at a significant rate, operates in an increasingly competitive market dominated by better-capitalized rivals, and remains dependent on continued access to external capital — a precarious position for a stock already trading near its 52-week low. The key variables an investor should monitor are the pace of improvement in operating margins across successive quarterly results, the rate at which the BlinkForward cost reductions flow through to reduced net losses, the company's ability to secure additional financing without excessive dilution, and any shifts in the regulatory or policy environment affecting EV infrastructure investment. The thesis would strengthen if upcoming quarters show a clear and sustained narrowing of losses alongside continued network expansion; it would weaken further if cash burn remains elevated, financing becomes more difficult to access, or competitive pressure begins to erode revenue growth in the DCFC segment.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "approximately 66,350 connected chargers"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "Blink Network included approximately 66,350 connected chargers as of December 31, 2025," and the pre-written SEC Filing Highlights section repeats this figure.

---

CLAIM: "$96.6 million in revenue"
LABEL: SUPPORTED
REASON: The raw source data lists revenue as $96,550,000, which rounds to $96.6 million; the Financial Health pre-written section also states "$96.6 million in revenue."

---

CLAIM: "30% year-over-year growth in new DC fast charging ports"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights states "18,041 new DC fast charging ports added in the U.S. (30% year-over-year growth)," and the pre-written SEC Filing Highlights section repeats this figure.

---

CLAIM: "trading at $0.56"
LABEL: SUPPORTED
REASON: The raw source data lists current_price as $0.5607, which rounds to $0.56; the pre-written Financial Health section also states "$0.56."

---

CLAIM: "$81.3 million market cap"
LABEL: SUPPORTED
REASON: The raw source data lists market_cap as $81,267,144, which rounds to $81.3 million; the pre-written Financial Health section also states "$81.3 million."

---

CLAIM: "a net loss of $50.7 million"
LABEL: SUPPORTED
REASON: The raw source data lists net_income as -$50,667,000, which rounds to -$50.7 million; the pre-written Financial Health section also states "net loss of $50.7 million."

---

CLAIM: "-52.5% profit margin"
LABEL: SUPPORTED
REASON: The raw source data lists profit_margin as -0.52477, which equals -52.477%, rounding to -52.5%; this is within 0.15 percentage points of the stated -52.5%.

---

CLAIM: "cut the workforce by approximately 37%"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights states the workforce was reduced "from 513 to approximately 320 employees"; (513 − 320) / 513 = 193 / 513 ≈ 37.6%, which rounds to approximately 37%, consistent with the claim and within acceptable rounding; the pre-written SEC Filing Highlights also states "approximately 37%."

---

**OUTLOOK**

---

CLAIM: "trading near its 52-week low"
LABEL: SUPPORTED
REASON: The raw source data lists current_price as $0.5607, 52-week low as $0.45, and 52-week high as $2.65; the current price of $0.5607 is $0.1107 above the 52-week low and $2.0893 below the 52-week high, placing it at (0.5607 − 0.45) / (2.65 − 0.45) = 0.1107 / 2.20 ≈ 5.0% of the way up the 52-week range — arithmetically confirming the stock is trading near its 52-week low.

---

*No additional quantitative figures, price targets, thresholds, ratios, named product milestones, or forward-looking numbers appear in the Outlook section beyond those already audited above. All qualitative directional statements (e.g., "cautious," "narrow but real path," "meaningful structural cost reduction") contain no specific quantitative claims requiring verification.*
