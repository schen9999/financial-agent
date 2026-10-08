# EVGO — baseline

## Metadata

ticker: EVGO
arm: baseline
judge_prompt_version: v2
context_sha256: 67e68e3269cc53d1eb49c08292922b6bc39048e337bfc9ae00d2f5b52848e1e5
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 354, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.891, "latency_s_total": 3.891, "parse_failure": 0, "prompt_tokens": 2553, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 504, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.945, "latency_s_total": 5.945, "parse_failure": 0, "prompt_tokens": 3348, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 165, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.748, "latency_s_total": 1.748, "parse_failure": 0, "prompt_tokens": 675, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 169, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.14, "latency_s_total": 2.14, "parse_failure": 0, "prompt_tokens": 668, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 231, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.718, "latency_s_total": 2.718, "parse_failure": 0, "prompt_tokens": 576, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 172, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.188, "latency_s_total": 2.188, "parse_failure": 0, "prompt_tokens": 434, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1232, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.012, "latency_s_total": 19.012, "parse_failure": 0, "prompt_tokens": 1876, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "EVGO",
  "company_name": "EVgo, Inc.",
  "current_price": 1.35,
  "currency": "USD",
  "market_cap": 424596224.0,
  "forward_pe": -3.068182,
  "week_52_high": 5.15,
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

Based on the risk factors disclosed, here are the primary takeaways:

## Financial Position and Challenges
- The company has a history of operating losses and expects to continue incurring significant expenses and losses in the near to medium term
- As of December 31, 2025, the company had $210.7 million in cash, cash equivalents, and restricted cash, with $161.2 million in working capital
- Future profitability depends on continued EV adoption, regulatory support, and customer use of their chargers

## Critical Dependencies
- **EV Market Growth**: The company's success is heavily dependent on continued EV adoption by consumers, fleet operators, and governments, as well as OEMs' ability to supply EVs
- **DOE Loan**: Business growth is substantially dependent on the ability to fully draw down a Department of Energy loan, which has multiple conditions precedent
- **Limited Customer Base**: The company currently depends on a limited number of customers and OEM partners, making it vulnerable to losing significant relationships

## Operational Risks
- Rapid growth management challenges
- Supply chain disruptions
- Construction delays and cost overruns
- Competition from other charging networks and alternative fuel technologies
- Reliance on a limited number of vendors for charging equipment

## Market Uncertainties
- EV market adoption rates may be slower than anticipated
- Macroeconomic factors and automotive industry cyclicality could impact EV demand
- Government policy changes at federal and state levels create uncertainty
- Fleet electrification may not occur as quickly as expected

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several categories of primary risk factors:

## Business-Related Risks
- Operating as an early-stage growth company with a history of operating losses and expectations of continuing losses in the near and medium-term
- Heavy dependence on continuing EV adoption and demand, as well as OEMs' ability to supply EVs to the market
- Challenges in managing rapid growth effectively
- Uncertainty created by current and future federal and state administrations regarding the EV sector
- Potential inaccuracy of market opportunity estimates and growth forecasts
- Significant competition in the EV charging market
- Reliance on a limited number of vendors for charging equipment and support services
- Dependence on a limited number of customers and OEM partners
- Construction risks, cost overruns, and installation delays
- Supply chain disruptions
- Potential need for additional funding on potentially unfavorable terms

## DOE Loan-Related Risks
- Substantial dependence on the ability to fully draw on the DOE Loan, which has multiple conditions precedent
- Risk of default if unable to comply with DOE Loan covenants
- Significant assets pledged as collateral, limiting availability for additional secured debt
- Operational restrictions imposed on subsidiaries under the loan
- Limitations on cash distributions from subsidiaries needed to fund operations

## EV Market Risks
- Changes to fuel economy standards or success of alternative fuels
- Slower-than-expected electrification of rideshare and commercial fleets
- Uncertain demand for medium and heavy-duty vehicle battery EVs
- Dependence on regulatory credits revenue
- Reduction or elimination of government rebates, tax credits, and financial incentives

## Technology and Infrastructure Risks
- Inability to maintain, protect, and enforce technology and intellectual property
- Uncertainty from lack of industry standards and transition to NACS charging standard

## Financial and Governance Risks
- Material weaknesses in internal controls over financial reporting
- Changes to U.S. tax laws and regulations
- Inflationary pressures affecting equipment and operating costs
- Controlled company status limiting certain corporate governance protections
- Provisions that may discourage lawsuits against directors and officers
- Anti-takeover provisions that could limit stock price appreciation

## Pre-written sections (judge input)

### Financial Health

EVgo is in a precarious financial position with a market capitalization of $424.6 million and a stock price of $1.35, down significantly from its 52-week high of $5.15. The company generated $402.9 million in revenue but posted a net loss of $54.1 million, resulting in a negative profit margin of -13.5%, indicating ongoing operational challenges. The negative forward P/E ratio reflects unprofitability, and with no dividend yield, the company is reinvesting losses rather than returning value to shareholders. SEC filings emphasize substantial business risks that could materially harm financial condition and liquidity, suggesting investors should exercise caution given the company's current trajectory toward profitability remains uncertain.

### Recent Developments

EVgo's latest SEC filings reveal persistent operational challenges, with the company reporting a -13.5% profit margin and net losses of $54.1 million against $403 million in revenue. The stock has declined significantly from its 52-week high of $5.15 to $1.35, reflecting investor concerns about the company's path to profitability in the competitive EV charging market. Recent 10-Q and 10-K filings emphasize multiple risk factors that could materially adversely affect the business, with no material improvements noted in the risk profile. For investors, EVgo's negative valuation metrics and substantial operating losses suggest the company remains in a critical phase where execution on growth and cost management will be essential to justify current valuations.

### SEC Filing Highlights

EVgo faces significant near-term profitability challenges, with a history of operating losses expected to continue as the company scales its network, though it maintains a solid cash position of $210.7 million as of December 31, 2025. The company's growth trajectory is heavily dependent on three critical factors: sustained EV adoption rates, successful drawdown of its Department of Energy loan (subject to multiple conditions), and retention of a limited customer base concentrated among key OEM and fleet partners. Operational risks including supply chain disruptions, construction delays, and competitive pressures from alternative charging networks pose material execution challenges. Market uncertainties around EV adoption rates, macroeconomic headwinds, and potential shifts in government policy create additional headwinds to the company's growth projections.

### Risk Factors

- **Continued Operating Losses and Funding Dependency**: EVgo operates as an early-stage growth company with a history of operating losses and expectations of continuing losses in the near and medium-term. The company is substantially dependent on its ability to fully draw on a DOE loan with multiple conditions precedent, and may require additional funding on potentially unfavorable terms.

- **EV Market and Demand Uncertainty**: EVgo's success depends heavily on continued EV adoption, OEM supply capabilities, and government incentives. Risks include slower-than-expected electrification of commercial fleets, potential reduction or elimination of government rebates and tax credits, and changes to fuel economy standards that could favor alternative fuels.

- **Intense Competition and Vendor Concentration**: The EV charging market faces significant competition while EVgo relies on a limited number of vendors for equipment and support services, as well as a limited number of customers and OEM partners. Construction delays, supply chain disruptions, and cost overruns further constrain operational flexibility and profitability.

## Audited (Exec Summary + Outlook)

### Executive Summary
EVgo is a public fast-charging network operator competing in the rapidly evolving EV infrastructure market, generating $402.9 million in revenue while carrying a market capitalization of $424.6 million — a valuation that offers little premium above a single year of top-line sales and reflects deep skepticism about the company's path to profitability. The stock's steep decline from its 52-week high of $5.15 to $1.35 makes EVgo notable now as a high-risk, high-uncertainty situation where the market is actively questioning whether the business model can scale to sustainable economics before liquidity becomes a constraint. The single most important near-term variable is whether EVgo can successfully satisfy the conditions precedent to draw down its Department of Energy loan, as that funding is central to the company's ability to expand its network without resorting to dilutive or unfavorable financing.

### Outlook
The directional lean on EVgo is **cautious**. On the tailwind side, secular growth in EV adoption, the potential unlocking of DOE loan proceeds, and EVgo's existing OEM and fleet relationships provide a credible long-term demand runway if execution holds. However, the headwinds are immediate and material: operating losses are expected to continue, the DOE loan drawdown remains conditional and uncertain, government policy support for EV incentives faces meaningful political risk, and competition from alternative charging networks shows no sign of easing. Investors should watch four key variables closely — the status and progress of DOE loan conditions, the trajectory of operating losses and cash burn relative to the $210.7 million cash position, the pace of broad EV adoption and any shifts in OEM production commitments, and any changes to federal or state policy affecting EV incentives and charging infrastructure funding. A more constructive view would require demonstrated progress toward satisfying DOE loan conditions, visible improvement in the loss margin trend, and sustained or accelerating EV adoption data; conversely, failure to access the DOE facility, a deterioration in the cash position, or a meaningful pullback in EV demand or government support would further weaken an already fragile investment thesis.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "generating $402.9 million in revenue"
LABEL: SUPPORTED
REASON: The raw source data lists revenue as $402,948,000, which rounds to $402.9 million, and the pre-written Financial Health section states "$402.9 million in revenue."

---

CLAIM: "market capitalization of $424.6 million"
LABEL: SUPPORTED
REASON: The raw source data lists market_cap as $424,596,224, which rounds to $424.6 million, consistent with the pre-written sections.

---

CLAIM: "a valuation that offers little premium above a single year of top-line sales"
LABEL: INFERENCE
REASON: This is directly derivable by comparing market cap ($424.6M) to revenue ($402.9M), showing the price-to-sales ratio is approximately 1.05x — a straightforward arithmetic comparison of two figures present in the source data.

---

CLAIM: "The stock's steep decline from its 52-week high of $5.15 to $1.35"
LABEL: SUPPORTED
REASON: The raw source data explicitly lists week_52_high as $5.15 and current_price as $1.35.

---

**OUTLOOK**

---

CLAIM: "$210.7 million cash position"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights section explicitly states "the company had $210.7 million in cash, cash equivalents, and restricted cash, as of December 31, 2025," and this figure is repeated in the pre-written SEC Filing Highlights section.

---

No other specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Executive Summary or Outlook sections beyond those evaluated above. All remaining claims in those sections are qualitative or directional in nature (e.g., "cautious," "credible long-term demand runway," "no sign of easing") and do not constitute quantitative or forward-looking numerical claims subject to this audit.
