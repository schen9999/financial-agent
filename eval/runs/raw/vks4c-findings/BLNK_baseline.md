# BLNK — baseline

## Metadata

ticker: BLNK
arm: baseline
judge_prompt_version: v2
context_sha256: cb6f52fc6473be29a38ddb9683b1f40f568de628e68f228ad6e923f29f3d6fa6
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 481, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.67, "latency_s_total": 5.67, "parse_failure": 0, "prompt_tokens": 3389, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 126, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.632, "latency_s_total": 1.632, "parse_failure": 0, "prompt_tokens": 2926, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 182, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.228, "latency_s_total": 2.228, "parse_failure": 0, "prompt_tokens": 709, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 210, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.627, "latency_s_total": 2.627, "parse_failure": 0, "prompt_tokens": 702, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 148, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.918, "latency_s_total": 1.918, "parse_failure": 0, "prompt_tokens": 201, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 213, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.614, "latency_s_total": 2.614, "parse_failure": 0, "prompt_tokens": 564, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1286, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.01, "latency_s_total": 19.01, "parse_failure": 0, "prompt_tokens": 1914, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "BLNK",
  "company_name": "Blink Charging Co.",
  "current_price": 0.5104,
  "currency": "USD",
  "market_cap": 73976720.0,
  "forward_pe": -2.2095237,
  "week_52_high": 2.63,
  "week_52_low": 0.45,
  "financial_currency": "USD",
  "revenue": 96550000.0,
  "net_income": -50667000.0,
  "profit_margin_pct": -52.48,
  "dividend_yield": 0.0,
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
As of December 31, 2025, Blink Network included approximately 66,350 connected chargers, comprising:
- ~58,850 Level 2 commercial chargers
- ~1,920 DCFC commercial chargers
- ~8,250 chargers owned by Blink

## Industry Trends
The EV charging sector demonstrated strong growth in 2025:
- 25% of new vehicles sold globally were electric
- 18,041 new DC fast charging ports added in the U.S. (30% year-over-year growth)
- Network reliability improved to low 90% range across most states
- Shift toward higher-power equipment (51% of new deployments at 250kW+)
- Stable pricing averaging $0.45-$0.53 per kilowatt-hour

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors

The context provided indicates that Blink Charging Co. discloses risk factors in "Item 1A – Risk Factors" of their Annual Report, but the specific details of those risk factors are not included in the information provided. The document references this section but does not elaborate on what those particular risks are.

To obtain a comprehensive list of the primary risk factors disclosed by Blink Charging, you would need to review the complete "Item 1A – Risk Factors" section of their SEC filing, which is not fully detailed in the available context.

## Pre-written sections (judge input)

### Financial Health

Blink Charging trades at $0.51 with a market capitalization of $74.0 million, reflecting significant financial distress. The company generated $96.6 million in revenue but posted a net loss of $50.7 million, resulting in a negative profit margin of -52.5%, indicating substantial operational losses. The forward P/E ratio of -2.21 is not meaningful given the company's unprofitability. With the stock trading near its 52-week low of $0.45 (down from $2.63), Blink faces considerable financial headwinds and requires near-term profitability improvements to stabilize shareholder value. The company's ability to achieve positive cash flow and margins will be critical to its long-term viability in the competitive EV charging market.

### Recent Developments

Blink Charging's most recent SEC filings (10-K filed March 31, 2026 and 10-Q filed August 7, 2026) emphasize the company's positioning as a leading EV charging provider amid expanding U.S. and international markets. However, the company continues to face significant operational challenges, with a negative net income of -$50.7 million against $96.6 million in revenue, reflecting a -52.48% profit margin that signals substantial losses despite growing top-line revenue. The stock has declined sharply from its 52-week high of $2.63 to $0.51, indicating investor concerns about the company's path to profitability and competitive pressures in the EV charging infrastructure space. With a negative forward P/E ratio and no dividend, investors should monitor upcoming quarterly results closely to assess whether Blink can achieve operational efficiency and margin improvement in an increasingly competitive market.

### SEC Filing Highlights

Blink Charging's latest filings reveal a company undergoing significant operational restructuring through its "BlinkForward Initiative," which reduced headcount by 37% and eliminated in-house manufacturing to improve profitability. The company's network grew to approximately 66,350 connected chargers as of December 31, 2025, with strategic focus shifting toward higher-margin DC Fast Charging deployments in high-utilization locations. The July 2025 acquisition of Zemetric Inc. strengthened Blink's software capabilities and provided a lower-cost Level 2 charger lineup, while a $20 million funding round in December 2025 supported operational needs. Industry tailwinds remain favorable, with 25% of global new vehicle sales being electric and U.S. DC fast charging ports growing 30% year-over-year, though Blink faces execution risks as it transitions to a leaner, contract-manufacturing model.

### Risk Factors

• **Dependence on EV Market Growth and Adoption** – Blink's revenue is heavily tied to electric vehicle adoption rates and charging infrastructure demand, which remain subject to regulatory changes, fuel price fluctuations, and consumer preference shifts.

• **Capital Intensity and Funding Requirements** – Expanding the charging network requires significant ongoing capital investment; inability to secure adequate financing or achieve profitability could constrain growth and dilute shareholder value.

• **Competitive Landscape and Market Saturation** – Blink faces intense competition from larger, better-capitalized competitors and established automotive manufacturers entering the charging space, which could pressure margins and market share.

## Audited (Exec Summary + Outlook)

### Executive Summary
Blink Charging is a leading EV charging network operator with approximately 66,350 connected chargers and $96.6 million in revenue, competing in a rapidly expanding but intensely competitive infrastructure market. The stock is notable now precisely because it trades near its 52-week low of $0.51 — a steep decline from $2.63 — while the company simultaneously executes a significant restructuring through its BlinkForward Initiative, creating a high-risk, high-uncertainty inflection point for investors. The single most important near-term variable is whether that restructuring — headcount reduction, elimination of in-house manufacturing, and a shift toward higher-margin DC Fast Charging — translates into measurable improvement in operating margins and a credible path to positive cash flow.

### Outlook
The directional outlook for Blink Charging is **cautious**, with a narrow but real path to improvement contingent on flawless execution of its restructuring strategy. On the tailwind side, broad industry dynamics remain supportive — global EV adoption continues to expand and U.S. DC fast charging infrastructure is growing rapidly — and Blink's BlinkForward Initiative, if successful, could meaningfully reduce its cost structure while the Zemetric acquisition adds software depth that may support higher-margin service revenue over time. However, the headwinds are substantial and immediate: the company is deeply unprofitable, its stock is trading near multi-year lows, and it operates in a capital-intensive business against larger, better-funded competitors. Investors should watch the trajectory of gross and operating margins in upcoming quarterly results as the primary signal of whether restructuring savings are materializing; the pace of DC Fast Charging deployment and utilization rates at those sites as an indicator of revenue quality; the company's ability to fund operations without excessive dilution; and any shifts in the regulatory or policy environment that could accelerate or dampen EV adoption. The cautious stance would shift toward more constructive if Blink demonstrates sequential margin improvement, sustains or grows its connected charger network without proportional cost increases, and secures financing on terms that do not significantly dilute existing shareholders. Conversely, continued margin deterioration, further equity raises at distressed valuations, or loss of competitive positioning to better-capitalized rivals would deepen the negative thesis.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

## EXECUTIVE SUMMARY

---

CLAIM: "approximately 66,350 connected chargers"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "Blink Network included approximately 66,350 connected chargers as of December 31, 2025," and the SEC Filing Highlights pre-written section repeats this figure.

---

CLAIM: "$96.6 million in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $96,550,000; the pre-written Financial Health section rounds this to $96.6 million, which matches within rounding.

---

CLAIM: "trades near its 52-week low of $0.51"
LABEL: UNSUPPORTED
REASON: The 52-week low in the source data is $0.45, not $0.51; $0.51 is the current price, not the 52-week low, so the claim conflates two distinct figures.

---

CLAIM: "a steep decline from $2.63"
LABEL: SUPPORTED
REASON: The source data explicitly lists the 52-week high as $2.63, and the current price of $0.5104 confirms a steep decline from that level.

---

CLAIM: "headcount reduction" [as part of BlinkForward]
LABEL: SUPPORTED
REASON: The RAG SEC Highlights confirms the BlinkForward Initiative reduced the global workforce from 513 to approximately 320 employees.

---

CLAIM: "elimination of in-house manufacturing" [as part of BlinkForward]
LABEL: SUPPORTED
REASON: The RAG SEC Highlights states Blink "Transitioned to contract manufacturing, eliminating in-house manufacturing facilities (completed January 2026)."

---

CLAIM: "a shift toward higher-margin DC Fast Charging" [as part of BlinkForward]
LABEL: SUPPORTED
REASON: The RAG SEC Highlights states BlinkForward included "Focused expansion on DC Fast Charging (DCFC) networks in high-utilization locations."

---

## OUTLOOK

---

CLAIM: "U.S. DC fast charging infrastructure is growing rapidly"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights states 18,041 new DC fast charging ports were added in the U.S. with 30% year-over-year growth, supporting this directional claim.

---

CLAIM: "Zemetric acquisition adds software depth"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights confirms the July 2025 acquisition of Zemetric Inc. provided "Software-driven fleet management and energy management services."

---

*(No additional specific quantitative figures, price targets, thresholds, ratios, named metrics, percentages, or forward-looking numbers appear in the Outlook section beyond those already evaluated above or directional/qualitative statements not subject to numerical audit.)*

---

## SUMMARY TABLE

| # | Claim | Label |
|---|-------|-------|
| 1 | ~66,350 connected chargers | SUPPORTED |
| 2 | $96.6 million in revenue | SUPPORTED |
| 3 | 52-week low of $0.51 | UNSUPPORTED |
| 4 | Steep decline from $2.63 | SUPPORTED |
| 5 | Headcount reduction (BlinkForward) | SUPPORTED |
| 6 | Elimination of in-house manufacturing (BlinkForward) | SUPPORTED |
| 7 | Shift toward higher-margin DC Fast Charging (BlinkForward) | SUPPORTED |
| 8 | U.S. DC fast charging infrastructure growing rapidly | SUPPORTED |
| 9 | Zemetric acquisition adds software depth | SUPPORTED |

---

**Critical Finding:** The most significant error is in the Executive Summary, where the 52-week low of **$0.45** (from source data) is misidentified as **$0.51** (the current stock price). The claim "trades near its 52-week low of $0.51" is factually incorrect on the stated low figure, even though the directional observation that the stock is near its 52-week low is arithmetically defensible ($0.5104 vs. $0.45 low). The specific dollar figure attributed to the 52-week low is wrong and therefore **UNSUPPORTED**.
