# EVGO — baseline

## Metadata

ticker: EVGO
arm: baseline
judge_prompt_version: v2
context_sha256: 594c642beea6423c7745ad6a98da45ef148d5c2f5e995f5a1855dc48a21c487f
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 338, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.996, "latency_s_total": 3.996, "parse_failure": 0, "prompt_tokens": 3406, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 332, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.545, "latency_s_total": 3.545, "parse_failure": 0, "prompt_tokens": 3394, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 156, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.031, "latency_s_total": 2.031, "parse_failure": 0, "prompt_tokens": 652, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 157, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.226, "latency_s_total": 2.226, "parse_failure": 0, "prompt_tokens": 645, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 222, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.55, "latency_s_total": 2.55, "parse_failure": 0, "prompt_tokens": 404, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 154, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.857, "latency_s_total": 1.857, "parse_failure": 0, "prompt_tokens": 418, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1181, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.529, "latency_s_total": 17.529, "parse_failure": 0, "prompt_tokens": 1780, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
- OEMs' ability to supply EVs to the market
- Relationships with automotive OEM and fleet partners
- The ability to fully draw down on a Department of Energy (DOE) Loan, which is critical to business growth

## Competitive and Market Landscape
EVGO faces competition from multiple companies in the developing EV charging market. The company's market opportunity estimates and growth forecasts may prove inaccurate, and changes to fuel economy standards or alternative fuel success could negatively impact demand.

## Operational Challenges
Key operational risks include:
- Dependence on a limited number of vendors for charging equipment
- Reliance on a limited number of customers and OEM partners
- Construction risks, cost overruns, and installation delays
- Supply chain disruptions
- Political uncertainty at federal and state levels affecting the EV sector

## Financing and Debt Constraints
The DOE Loan, which secures a substantial portion of consolidated assets, imposes significant restrictions on operations and cash distributions from subsidiaries. The company may need to raise additional capital, which may not be available on favorable terms.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The primary risk factors fall into three main categories:

## Risks Related to Business Operations

- Operating as an early-stage growth company with a history of losses and expectations of continuing losses in the near and medium term
- Heavy dependence on EV adoption rates and OEM supply capabilities
- Challenges in managing rapid growth effectively
- Political and regulatory uncertainty at federal and state levels affecting the EV sector
- Potential inaccuracy in market opportunity estimates and growth forecasts
- Increasing competition in the EV charging market
- Reliance on a limited number of vendors for charging equipment and support services
- Dependence on a limited number of customers and OEM partners
- Construction risks, cost overruns, and installation delays
- Supply chain disruptions
- Need for additional funding that may not be available on favorable terms

## Risks Related to the DOE Loan

- Substantial dependence on the ability to fully draw down the DOE Loan, which has multiple conditions precedent
- Risk of default if loan covenants and terms are not maintained
- Significant assets pledged as collateral, limiting capacity for additional secured debt
- Operational restrictions imposed through the loan agreement
- Limitations on cash distributions from subsidiaries needed to fund operations

## Risks Related to the EV Market

- Potential negative impacts from changes to fuel economy standards or alternative fuel success
- Uncertainty regarding the pace of electrification in rideshare and commercial fleet sectors and their reliance on public fast charging networks

## Pre-written sections (judge input)

### Financial Health

EVgo is in a precarious financial position with a stock price of $1.29 and market capitalization of $406 million, down significantly from its 52-week high of $4.82. The company is unprofitable with a negative profit margin of -13.5% and net losses of $54 million against revenue of $403 million, indicating the business is not yet operationally sustainable. The negative forward P/E ratio reflects ongoing losses and investor concerns about the company's path to profitability. With no dividend yield and substantial operational challenges highlighted in recent SEC filings, EVgo presents a high-risk investment profile typical of early-stage infrastructure companies in the EV charging sector.

### Recent Developments

EVgo has not announced significant recent news developments. The company's most recent SEC filings—a 10-K (March 2026) and 10-Q (August 2026)—emphasize substantial operational risks without disclosing material changes to risk factors, suggesting ongoing business challenges. With a negative profit margin of -13.5%, net losses of $54.1 million, and a stock price down 73% from its 52-week high of $4.82, EVgo faces headwinds in the competitive EV charging market. Investors should monitor upcoming earnings reports and strategic announcements for signs of a path to profitability, as the company's current financial trajectory remains concerning.

### SEC Filing Highlights

EVGO is an early-stage growth company with a history of operating losses and expects to continue incurring significant expenses in the near term, though it has experienced rapid recent growth. The company's success is heavily dependent on continued EV adoption, OEM supply capabilities, and its ability to fully draw down a critical Department of Energy loan that is essential to funding expansion. EVGO faces competitive pressures in the developing EV charging market and operational risks including vendor concentration, limited customer diversification, construction delays, and supply chain disruptions. The DOE loan imposes significant restrictions on operations and cash distributions, and the company may need to raise additional capital on potentially unfavorable terms to support growth objectives.

### Risk Factors

- **Dependence on DOE Loan and Growth Capital**: EVgo relies heavily on drawing down its Department of Energy loan facility, which carries multiple conditions precedent and covenant requirements. The company has a history of losses with expectations of continued losses in the near to medium term, creating significant refinancing risk and potential constraints on operations and cash distributions.

- **Market Adoption and Competition Risks**: EV charging demand depends on uncertain EV adoption rates, OEM supply capabilities, and the pace of electrification in commercial fleets and rideshare sectors. EVgo faces increasing competition in a nascent market while relying on a limited number of customers and OEM partners, creating revenue concentration risk.

- **Operational and Supply Chain Execution Risk**: As an early-stage growth company, EVgo faces construction delays, equipment cost overruns, vendor concentration risk, and supply chain disruptions. The company must manage rapid expansion while navigating political and regulatory uncertainty at federal and state levels that could impact the EV charging sector.

## Audited (Exec Summary + Outlook)

### Executive Summary
EVgo is an early-stage EV fast-charging infrastructure company operating in a competitive and rapidly evolving market, generating $403 million in revenue while sustaining net losses of $54 million and carrying a market capitalization of $406 million. The stock is notable now precisely because of its distressed profile — trading at $1.29, down 73% from its 52-week high of $4.82 — which reflects deep investor skepticism about the company's ability to reach profitability without additional dilutive capital raises or favorable policy support. The single most important near-term variable is EVgo's ability to satisfy the conditions required to fully draw down its Department of Energy loan, as that facility is essential to funding expansion and its loss could materially impair the company's growth trajectory.

### Outlook
The directional outlook for EVgo is **cautious**. On the tailwind side, the secular shift toward EV adoption and the electrification of commercial fleets and rideshare networks represent genuine long-term demand drivers, and EVgo's rapid recent growth suggests the underlying business model can scale if conditions align. However, the headwinds are substantial and near-term in nature: the company faces continued operating losses, a constrained capital structure, and meaningful political and regulatory uncertainty that could affect both federal loan support and broader EV policy. Investors should watch the status and drawdown progress of the DOE loan facility as the single most consequential variable, alongside trends in EV adoption rates, OEM delivery volumes, and the pace of commercial fleet electrification. On the competitive front, monitoring whether EVgo can diversify its customer and OEM partner base will be critical to assessing revenue concentration risk. The cautious lean would shift toward a more constructive view if EVgo demonstrates consistent progress drawing down the DOE facility, shows a credible narrowing of losses in successive earnings reports, and benefits from a stable or supportive federal policy environment for EV infrastructure — conversely, any disruption to the DOE loan, a slowdown in EV adoption, or the need to raise additional capital on unfavorable terms would deepen the bearish case materially.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "generating $403 million in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $402,948,000, which rounds to $403 million; the pre-written Financial Health section also states "revenue of $403 million."

---

CLAIM: "sustaining net losses of $54 million"
LABEL: SUPPORTED
REASON: Source data shows net_income of -$54,125,000, which rounds to -$54 million; consistent with the pre-written sections.

---

CLAIM: "market capitalization of $406 million"
LABEL: SUPPORTED
REASON: Source data shows market_cap of $405,725,248, which rounds to $406 million.

---

CLAIM: "trading at $1.29"
LABEL: SUPPORTED
REASON: Source data explicitly states current_price of $1.29.

---

CLAIM: "down 73% from its 52-week high of $4.82"
LABEL: SUPPORTED
REASON: The 52-week high of $4.82 is present in source data. Computed decline: (4.82 − 1.29) / 4.82 = 3.53 / 4.82 ≈ 73.2%, which is within 0.15 percentage points of 73%; the pre-written Recent Developments section also states "down 73% from its 52-week high of $4.82."

---

CLAIM: "52-week high of $4.82"
LABEL: SUPPORTED
REASON: Source data explicitly states week_52_high: 4.82.

---

CLAIM: "EVgo's ability to satisfy the conditions required to fully draw down its Department of Energy loan"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors sections explicitly state the DOE Loan has "multiple conditions precedent" and is "critical to business growth."

---

**OUTLOOK**

*(The Outlook section is largely qualitative/directional. I will identify every specific quantitative or forward-looking figure or named milestone.)*

---

CLAIM: "EVgo's rapid recent growth"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights section explicitly states "The company has experienced rapid growth recently," and this is echoed in the SEC Filing Highlights pre-written section.

---

CLAIM: "the status and drawdown progress of the DOE loan facility as the single most consequential variable"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors sections both identify the DOE Loan as critical/essential to business growth and expansion, supporting this characterization; no specific quantitative figure is embedded in this claim.

---

CLAIM: "shows a credible narrowing of losses in successive earnings reports"
LABEL: INFERENCE
REASON: No specific loss-narrowing figure or timeline is cited; this is a directional forward-looking condition derivable from the established fact of ongoing net losses (-$54 million), stated as a watch-item rather than a specific quantitative claim.

---

*(No price targets, specific ratio thresholds, named product milestones, or additional quantitative forward-looking numbers appear in the Outlook section beyond those already evaluated above.)*

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | $403 million in revenue | SUPPORTED |
| 2 | Net losses of $54 million | SUPPORTED |
| 3 | Market capitalization of $406 million | SUPPORTED |
| 4 | Trading at $1.29 | SUPPORTED |
| 5 | Down 73% from 52-week high | SUPPORTED |
| 6 | 52-week high of $4.82 | SUPPORTED |
| 7 | DOE loan conditions / full drawdown | SUPPORTED |
| 8 | Rapid recent growth | SUPPORTED |
| 9 | Credible narrowing of losses in successive earnings reports | INFERENCE |
