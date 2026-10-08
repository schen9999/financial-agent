# EVGO — rerank3

## Metadata

ticker: EVGO
arm: rerank3
judge_prompt_version: v2
context_sha256: 3979db28ce73f7f6df17aad3b9ab7d3e4ecc0e37ae79c62922e3ef3e7b7dd218
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 336, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.012, "latency_s_total": 4.012, "parse_failure": 0, "prompt_tokens": 3406, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 368, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.956, "latency_s_total": 3.956, "parse_failure": 0, "prompt_tokens": 3391, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 136, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.823, "latency_s_total": 1.823, "parse_failure": 0, "prompt_tokens": 652, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 163, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.117, "latency_s_total": 2.117, "parse_failure": 0, "prompt_tokens": 645, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 218, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.313, "latency_s_total": 2.313, "parse_failure": 0, "prompt_tokens": 440, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 168, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.887, "latency_s_total": 1.887, "parse_failure": 0, "prompt_tokens": 416, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1146, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 16.195, "latency_s_total": 16.195, "parse_failure": 0, "prompt_tokens": 1772, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "EVGO",
  "company_name": "EVgo, Inc.",
  "current_price": 1.29,
  "currency": "USD",
  "market_cap": 405725248.0,
  "forward_pe": -2.931818,
  "week_52_high": 4.82,
  "week_52_low": 1.23,
  "financial_currency": "USD",
  "revenue": 402948000.0,
  "net_income": -54125000.0,
  "profit_margin_pct": -13.5,
  "dividend_yield": 0.0,
  "sector": "Consumer Cyclical",
  "industry": "Specialty Retail"
}

NEWS ARTICLES:
[]

SEC FILING SUMMARIES:
{
  "10-K": {
    "form_type": "10-K",
    "filing_date": "2026-03-09",
    "summary": "Item 1A. Risk Factors . In the course of conducting our business operations, we are exposed to a variety of risks, any of which have affected or could materially and adversely affect our business, financial condition and results of operations. Before you make a decision to buy our securities, in addition to the risks and uncertainties discussed above under \u201cCautionary Statement Regarding Forward-Looking Statements,\u201d you should carefully consider the specific risks set forth herein. If any of these risks actually occur, our business, financial condition, liquidity and results of operations may be harmed. As a result, the market price of our securities could decline, possibly significantly or permanently, and you could lose all or part of your investment. Additionally, the risks and uncertai"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-06",
    "summary": "Item 1A. Risk Factors In the course of conducting our business operations, we are exposed to a variety of risks, any of which have affected or could materially adversely affect our business, financial condition, and results of operations. The market price of our securities could decline, possibly significantly or permanently, if one or more of these risks and uncertainties occur. Before you make a decision to buy our securities, in addition to the risks and uncertainties discussed above under \u201cCautionary Statement Regarding Forward-Looking Statements,\u201d you should carefully consider the specific risk factors set forth in the \u201cRisk Factors\u201d section in the Annual Report. There have been no material changes to the risk factors disclosed in Part I, Item 1A of the Annual Report. See the \u201cItem 5 "
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] # Key Takeaways from EVGO's SEC Filings

## Business Stage and Financial Position
EVGO is an early-stage growth company with a history of operating losses and expects to continue incurring significant expenses and losses in the near and medium term. The company has experienced rapid growth recently, though this presents management challenges.

## Growth Dependencies
The company's success is heavily dependent on:
- Continued adoption and demand for electric vehicles
- Original equipment manufacturers' (OEMs) ability to supply EVs to the market
- Relationships with automotive OEM and fleet partners

## Financing and DOE Loan
A substantial portion of EVGO's growth strategy relies on its ability to draw down a Department of Energy (DOE) loan, which is secured by a significant portion of consolidated assets. The loan contains multiple conditions precedent for each draw and restrictive covenants that limit operational flexibility. The company may need to raise additional capital, which may not be available on favorable terms.

## Competitive and Market Risks
- Faces increasing competition in the EV charging market
- Dependent on a limited number of vendors for charging equipment
- Concentrated customer and OEM partner base creates vulnerability
- Market growth forecasts may prove inaccurate
- Political uncertainty at federal and state levels could impact the EV sector

## Operational Challenges
- Supply chain disruptions could materially impact operations
- Construction risks, cost overruns, and installation delays are present
- Rideshare and commercial fleet electrification may occur slower than expected

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The primary risk factors disclosed include:

## Business and Financial Risks
- History of operating losses and negative operating cash flows, with expectations of continuing losses in the near and medium term
- Dependence on cash distributions from subsidiaries to fund operations, with restrictions that could adversely affect business plans
- Substantial portion of consolidated assets secured by the DOE Loan, limiting availability for additional secured debt

## EV Market Risks
- Changes to fuel economy standards or success of alternative fuels could negatively impact EV market demand
- Rideshare and commercial fleets may not electrify as quickly as expected or may not rely on public fast charging networks
- Uncertainty regarding future demand and availability of battery EVs from medium and heavy-duty vehicle segments
- Dependence on regulatory credits revenue, which is subject to factors beyond the company's control
- Potential reduction, modification, or elimination of government rebates, tax credits, and other financial incentives for EVs and charging stations

## Technology and Infrastructure Risks
- Inability to maintain, protect, and enforce technology and intellectual property
- Lack of industry standards and transition to NACS charging standard creating uncertainty, competition, and unexpected costs

## Financial, Tax, and Accounting Risks
- Material weaknesses in internal control over financial reporting
- Changes to U.S. tax laws and regulations
- Inflationary pressures and changes in monetary or trade policy affecting equipment and operating costs

## Governance and Structural Risks
- Controlled company status limiting corporate governance protections
- EVgo Holdings' majority voting control creating potential conflicts with other stockholders
- Significant payments required under the Tax Receivable Agreement

## Pre-written sections (judge input)

### Financial Health

EVgo is in a precarious financial position with a stock price of $1.29 and market capitalization of approximately $406 million. The company is unprofitable, posting a net loss of $54.1 million against revenue of $403 million, resulting in a negative profit margin of -13.5%. The negative forward P/E ratio reflects ongoing losses and investor concerns about the company's path to profitability. With no dividend yield and a 52-week low near current trading levels, EVgo faces significant financial headwinds typical of early-stage EV charging infrastructure companies still scaling operations.

### Recent Developments

EVgo's latest SEC filings reveal no material changes to previously disclosed risk factors, suggesting the company continues to navigate significant operational challenges. The company reported a negative profit margin of -13.5% with a net loss of $54.1 million on $403 million in revenue, indicating ongoing profitability struggles in the competitive EV charging market. With the stock trading at $1.29—near its 52-week low of $1.23 and substantially below its $4.82 high—investor sentiment remains weak despite the broader EV infrastructure growth tailwinds. The absence of recent positive news developments and persistent losses underscore execution risks that investors should carefully weigh against the long-term potential of the EV charging sector.

### SEC Filing Highlights

EVGO is an early-stage growth company with a history of operating losses and expects to continue incurring significant expenses in the near term, though it has experienced rapid recent growth. The company's success is heavily dependent on continued EV adoption, OEM supply capabilities, and maintaining key automotive and fleet partnerships. A substantial portion of EVGO's growth strategy relies on drawing down a Department of Energy loan secured by consolidated assets, with multiple conditions and restrictive covenants that limit operational flexibility. The company faces increasing competitive pressure in the EV charging market, supply chain risks, and concentration risk from a limited vendor and customer base. Additional capital may be required and may not be available on favorable terms, while political uncertainty at federal and state levels presents ongoing sector headwinds.

### Risk Factors

- **Persistent Losses and Cash Flow Challenges**: EVgo has a history of operating losses and negative operating cash flows, with expectations of continuing losses in the near and medium term. The company depends on cash distributions from subsidiaries to fund operations, which are subject to restrictions that could adversely affect business plans.

- **EV Market Adoption Uncertainty**: Demand for public fast charging infrastructure depends on the pace of EV adoption, particularly among rideshare and commercial fleets. Changes to fuel economy standards, success of alternative fuels, or slower-than-expected electrification of medium and heavy-duty vehicles could significantly reduce demand for EVgo's services.

- **Regulatory and Incentive Dependency**: The company relies on government rebates, tax credits, and financial incentives to support EV adoption and charging infrastructure investment. Reduction, modification, or elimination of these incentives—combined with the transition to industry-standard NACS charging—could increase costs and create competitive pressures.

## Audited (Exec Summary + Outlook)

### Executive Summary
EVgo is an early-stage public fast-charging infrastructure company operating in the competitive EV charging market, generating $403 million in revenue while carrying a net loss of $54.1 million and a market capitalization of approximately $406 million. The stock is notable now precisely because it trades near its 52-week low of $1.23—a level that reflects deep investor skepticism about the path to profitability, heavy reliance on government incentives, and a DOE loan structure that constrains operational flexibility. The single most important near-term variable is whether the pace of EV adoption—particularly among rideshare and commercial fleet customers—accelerates sufficiently to drive utilization rates and move the company meaningfully toward breakeven before it requires additional capital on potentially unfavorable terms.

### Outlook
The directional lean on EVgo is **cautious**. The primary tailwind remains the long-term secular growth of EV adoption, which underpins demand for public fast-charging infrastructure and gives the company a structural reason to exist at scale. However, that tailwind is being offset by a convergence of meaningful headwinds: persistent operating losses, a DOE loan structure with restrictive covenants that limits strategic flexibility, concentration risk across both vendors and customers, and a politically uncertain incentive environment that could erode the subsidy support the business currently depends on. Investors should closely watch the trajectory of EV adoption rates—particularly among rideshare and commercial fleet operators, which represent EVgo's most critical demand drivers—as well as the company's ability to satisfy DOE loan conditions, its progress on the NACS transition, and any shifts in federal or state incentive policy. The cautious view would begin to soften if EVgo demonstrates a credible narrowing of operating losses alongside sustained network utilization growth and stable access to its DOE facility; it would deepen materially if EV adoption slows, key partnerships deteriorate, or the company is forced to raise additional capital under unfavorable conditions.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

### EXECUTIVE SUMMARY

---

CLAIM: "$403 million in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $402,948,000, which rounds to $403 million; the pre-written sections also confirm "$403 million in revenue."

---

CLAIM: "net loss of $54.1 million"
LABEL: SUPPORTED
REASON: Source data shows net_income of -$54,125,000, which rounds to -$54.1 million; confirmed in pre-written sections.

---

CLAIM: "market capitalization of approximately $406 million"
LABEL: SUPPORTED
REASON: Source data shows market_cap of $405,725,248, which rounds to approximately $406 million; confirmed in pre-written sections.

---

CLAIM: "trades near its 52-week low of $1.23"
LABEL: SUPPORTED
REASON: Source data explicitly lists week_52_low as $1.23 and current_price as $1.29, placing the stock near (within $0.06 of) its 52-week low.

---

### OUTLOOK

No explicit quantitative figures, price targets, thresholds, ratios, metrics, or percentages appear in the Outlook section. All content is qualitative and directional (e.g., "cautious," "long-term secular growth," "meaningful headwinds," "credible narrowing of operating losses"). There are no specific numbers, named milestones with attached figures, or forward-looking numerical claims to audit.

---

### SUMMARY TABLE

| # | Claim | Label |
|---|-------|-------|
| 1 | $403 million in revenue | SUPPORTED |
| 2 | net loss of $54.1 million | SUPPORTED |
| 3 | market capitalization of approximately $406 million | SUPPORTED |
| 4 | trades near its 52-week low of $1.23 | SUPPORTED |

All four auditable quantitative claims in the Executive Summary are supported by the raw source data. The Outlook section contains no quantitative or forward-looking numerical claims requiring audit entries.
