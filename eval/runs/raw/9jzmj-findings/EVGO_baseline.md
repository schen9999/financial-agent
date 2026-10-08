# EVGO — baseline

## Metadata

ticker: EVGO
arm: baseline
judge_prompt_version: v2
context_sha256: 08c5d362f2776fdee17ce3ea7a306caad2a55675786fcedb83449ae4addcf6f6
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 360, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.306, "latency_s_total": 4.306, "parse_failure": 0, "prompt_tokens": 2553, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 419, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.186, "latency_s_total": 5.186, "parse_failure": 0, "prompt_tokens": 3348, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 150, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.646, "latency_s_total": 1.646, "parse_failure": 0, "prompt_tokens": 656, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 151, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.952, "latency_s_total": 1.952, "parse_failure": 0, "prompt_tokens": 649, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 226, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.838, "latency_s_total": 2.838, "parse_failure": 0, "prompt_tokens": 491, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 177, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.266, "latency_s_total": 2.266, "parse_failure": 0, "prompt_tokens": 440, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1226, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 18.982, "latency_s_total": 18.982, "parse_failure": 0, "prompt_tokens": 1810, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "EVGO",
  "company_name": "EVgo, Inc.",
  "current_price": 1.38,
  "currency": "USD",
  "market_cap": 434031680.0,
  "forward_pe": -3.1363637,
  "week_52_high": 5.15,
  "week_52_low": 1.23,
  "revenue": 402948000.0,
  "net_income": -54125000.0,
  "profit_margin": -0.13502,
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

## Financial Position
- As of December 31, 2025, the company had $210.7 million in cash, cash equivalents, and restricted cash, with $161.2 million in working capital
- The company has a history of operating losses and negative operating cash flows
- Management expects to continue incurring significant expenses and losses in the near- and medium-term

## Business Model Dependencies
- Growth is heavily dependent on continued EV adoption by consumers, businesses, and governments
- Success relies on OEMs' ability to supply EVs to the market and customers' willingness to use the company's charging network
- The company depends on a limited number of vendors for charging equipment and a limited number of customers and OEM partners

## Funding and Capital
- The company has a Department of Energy (DOE) Loan that is critical to business growth, with multiple conditions precedent to drawing funds
- The DOE Loan is secured by a substantial portion of consolidated assets, limiting flexibility for additional secured debt
- Additional financing may be needed, with no assurance it will be available on favorable terms

## Market and Competitive Risks
- The EV market is still rapidly evolving with uncertain demand trajectories
- The company faces competition from multiple sources and expects significant future competition
- Market growth depends on factors beyond the company's control, including government policy, fuel prices, EV pricing, and consumer preferences

## Operational Challenges
- Supply chain disruptions could materially impact operations
- Construction risks, cost overruns, and installation delays are present
- Rapid growth management presents operational challenges

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several categories of primary risk factors:

## Business-Related Risks
- Operating as an early-stage growth company with a history of losses and expectations of continuing losses in the near and medium-term
- Heavy dependence on EV adoption and demand, as well as OEMs' ability to supply EVs to the market
- Challenges in managing rapid growth effectively
- Uncertainty created by current and future federal and state administrations regarding the EV sector
- Potential inaccuracy of market opportunity estimates and growth forecasts
- Significant competition in the EV charging market
- Reliance on a limited number of vendors for charging equipment and support services
- Dependence on a limited number of customers and OEM partners
- Construction risks, cost overruns, and installation delays
- Supply chain disruptions
- Potential need for additional funding that may not be available on favorable terms

## DOE Loan-Related Risks
- Substantial dependence on the ability to fully draw on the DOE Loan, which has multiple conditions precedent
- Risk of default if unable to comply with loan covenants
- Substantial assets pledged as collateral, limiting availability for additional secured debt
- Operational restrictions imposed on subsidiaries under the loan terms
- Limitations on cash distributions from subsidiaries needed to fund operations

## EV Market Risks
- Changes to fuel economy standards or success of alternative fuels
- Slower-than-expected electrification of rideshare and commercial fleets
- Uncertainty regarding medium and heavy-duty vehicle segment development

## Technology, Finance, and Governance Risks
- Intellectual property protection challenges
- Industry standard transition uncertainties
- Material weaknesses in internal controls over financial reporting
- Tax law changes and liabilities
- Inflationary pressures affecting equipment and operating costs
- Controlled company status limiting certain corporate governance protections

## Pre-written sections (judge input)

### Financial Health

EVgo is in a precarious financial position with a market capitalization of $434 million and a stock price of $1.38, down significantly from its 52-week high of $5.15. The company generated $403 million in revenue but posted a net loss of $54 million, resulting in a negative 13.5% profit margin, indicating the company is not yet profitable. The forward P/E ratio of -3.14 reflects ongoing losses and investor concerns about the path to profitability. With substantial operational losses and elevated business risks noted in recent SEC filings, EVgo faces significant financial headwinds as it scales its EV charging network infrastructure.

### Recent Developments

EVgo's latest SEC filings reveal no material changes to previously disclosed risk factors, suggesting operational stability despite ongoing challenges. The company continues to face significant headwinds, with a negative profit margin of -13.5% and net losses of $54.1 million against $403 million in revenue, indicating the business remains unprofitable. The stock has declined substantially from its 52-week high of $5.15 to $1.38, reflecting investor concerns about the company's path to profitability in the competitive EV charging market. With limited positive news catalysts and persistent operational losses, investors should carefully monitor upcoming quarterly results for signs of margin improvement or network expansion success.

### SEC Filing Highlights

EVgo reported $210.7 million in cash and cash equivalents as of December 31, 2025, with $161.2 million in working capital, though the company continues to operate at a loss with negative operating cash flows. The company's growth strategy is heavily dependent on a critical Department of Energy loan with multiple conditions precedent, which is secured by a substantial portion of consolidated assets and limits additional financing flexibility. EVgo faces significant operational and market risks, including dependence on a limited number of vendors and OEM partners, evolving EV market demand, and supply chain disruptions that could impact expansion timelines and costs. Management expects to continue incurring substantial expenses and losses in the near- and medium-term as the company scales its charging network amid competitive pressures and uncertain market trajectories.

### Risk Factors

• **Dependence on DOE Loan and Covenant Compliance** — EVgo relies heavily on drawing down its Department of Energy loan to fund operations and growth, with substantial assets pledged as collateral. Failure to meet loan covenants or satisfy conditions precedent could trigger default, while operational restrictions on subsidiaries limit financial flexibility and cash distribution capabilities.

• **EV Market Adoption and Demand Uncertainty** — The company's success is contingent on accelerating EV adoption rates, OEM supply capacity, and fleet electrification timelines. Slower-than-expected market growth, policy changes across administrations, or shifts toward alternative fuel technologies could materially reduce charging demand and revenue.

• **Ongoing Losses and Path to Profitability** — As an early-stage growth company with a history of losses and expectations of continuing losses in the near to medium-term, EVgo faces uncertainty regarding when (or if) it will achieve profitability, requiring additional capital that may not be available on favorable terms.

## Audited (Exec Summary + Outlook)

### Executive Summary
EVgo operates a national fast-charging network for electric vehicles, generating $403 million in revenue while carrying a market capitalization of $434 million and a net loss of $54 million — the profile of an early-stage infrastructure company still in the costly build-out phase. The stock is notable now precisely because of the tension between its depressed price of $1.38 (well off its 52-week high of $5.15) and the scale of capital being deployed, making it a high-risk, binary-outcome situation rather than a conventional growth investment. The single most important near-term variable is whether EVgo can satisfy the conditions precedent on its Department of Energy loan, as access to that financing is the linchpin of its entire expansion strategy and its ability to continue operating without dilutive capital raises.

### Outlook
The directional lean on EVgo is **cautious**, with the investment thesis resting on a narrow set of conditions that must materialize in sequence rather than in parallel. On the tailwind side, secular growth in EV adoption, fleet electrification, and the structural need for public fast-charging infrastructure provide a credible long-term demand backdrop. However, the headwinds are immediate and concrete: persistent operating losses, negative operating cash flows, a stock price that has lost the majority of its value from its 52-week high, and a financing structure that concentrates existential risk in a single government loan facility. Investors should watch three variables above all others — first, progress on satisfying the DOE loan's conditions precedent and any covenant developments, as this is the most direct near-term solvency signal; second, the trajectory of operating margins quarter over quarter, which would indicate whether network scale is beginning to translate into improved unit economics; and third, the broader policy and regulatory environment for EV infrastructure, where shifts across administrations could either accelerate or undermine both demand and government financing support. The thesis would strengthen meaningfully if EVgo demonstrates clear progress toward unlocking DOE loan drawdowns, shows sequential margin improvement, and reports network expansion without supply chain disruption. It would weaken further if loan conditions remain unsatisfied, losses widen, or EV adoption trends soften — any of which could force dilutive capital raises at an already depressed valuation.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "generating $403 million in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $402,948,000, which rounds to $403 million; the pre-written sections also state "$403 million in revenue."

---

CLAIM: "market capitalization of $434 million"
LABEL: SUPPORTED
REASON: Source data shows market_cap of $434,031,680, which rounds to $434 million.

---

CLAIM: "net loss of $54 million"
LABEL: SUPPORTED
REASON: Source data shows net_income of -$54,125,000, which rounds to -$54 million.

---

CLAIM: "depressed price of $1.38"
LABEL: SUPPORTED
REASON: Source data explicitly lists current_price as $1.38.

---

CLAIM: "well off its 52-week high of $5.15"
LABEL: SUPPORTED
REASON: Source data explicitly lists week_52_high as $5.15, and $1.38 is arithmetically well below $5.15.

---

**OUTLOOK**

---

CLAIM: "a stock price that has lost the majority of its value from its 52-week high"
LABEL: SUPPORTED
REASON: $1.38 vs. $5.15 represents a decline of approximately 73.2% ((5.15 − 1.38) / 5.15), which is arithmetically a majority (>50%) of its value lost from the 52-week high.

---

CLAIM: "negative operating cash flows"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights section explicitly states "The company has a history of operating losses and negative operating cash flows."

---

CLAIM: "a financing structure that concentrates existential risk in a single government loan facility"
LABEL: INFERENCE
REASON: This is a qualitative characterization directly derivable from the SEC highlights and risk factors, which state the DOE Loan is "critical to business growth," secured by "a substantial portion of consolidated assets," and that the company is "heavily dependent" on drawing it down — no new external fact is required.

---

CLAIM: "persistent operating losses"
LABEL: SUPPORTED
REASON: Source data shows net_income of -$54,125,000 and the RAG sections explicitly confirm "a history of operating losses" with management expecting to "continue incurring significant expenses and losses in the near- and medium-term."

---

*No additional standalone quantitative figures, price targets, specific thresholds, ratios, named product milestones, or forward-looking numbers appear in the Outlook section beyond those already evaluated above. All other claims in the Outlook are qualitative directional statements (e.g., "cautious," "tailwind," "headwinds") that do not constitute quantitative or forward-looking numerical claims subject to this audit.*
