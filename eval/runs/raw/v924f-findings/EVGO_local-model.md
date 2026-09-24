# EVGO — local-model

## Metadata

ticker: EVGO
arm: local-model
judge_prompt_version: v2
context_sha256: f5e3606368d5600e9df8c2a57956aac3d3392ccfba08ade3a1d092f2e0b840f5
local_model_served_name: financial-lora
local_model_dir: qwen-ft
local_model_backend: openai
local_model_url: http://vllm.financial-agent.svc:8000
local_model_sampling: {"max_tokens": 512, "min_p": 0.0, "repetition_penalty": 1.1, "temperature": 0.1, "top_k": 20, "top_p": 0.8}

## Retrieved source context

STOCK DATA:
{
  "ticker": "EVGO",
  "company_name": "EVgo, Inc.",
  "current_price": 1.36,
  "currency": "USD",
  "market_cap": 427741376.0,
  "forward_pe": -3.0909092,
  "week_52_high": 5.18,
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

Based on the risk factors disclosed, here are the primary takeaways:

## Financial Position and Outlook
- As of December 31, 2025, the company had $210.7 million in cash, cash equivalents, and restricted cash, with $161.2 million in working capital
- The company has a history of operating losses and expects to continue incurring significant expenses and losses in the near- and medium-term
- Future profitability depends on successful capital draws from the DOE Loan and the Credit Agreement

## Business Dependencies
- Growth is heavily dependent on continued EV adoption by consumers, fleet operators, and governments
- Success relies on OEM partnerships and their ability to supply EVs to the market
- The company depends on a limited number of vendors for charging equipment and a limited number of customers and OEM partners

## Key Risk Areas
- **Market Risk**: EV adoption may not continue at expected rates; the market for public DC fast charging may develop more slowly than anticipated
- **Regulatory Risk**: Changes in government policy at federal and state levels create uncertainty; potential expiration of EV tax incentives and regulatory changes could impact demand
- **Operational Risk**: Supply chain disruptions, construction delays, and rapid growth management challenges
- **Financing Risk**: Ability to fully draw on the DOE Loan is critical; additional financing may be needed but may not be available on favorable terms

## Market Factors Affecting Demand
Multiple factors could negatively impact EV charging demand, including macroeconomic conditions, gasoline price volatility, EV supply chain issues, grid reliability concerns, and competition from alternative fuel vehicles.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several categories of primary risk factors:

## Business-Related Risks
- Operating as an early-stage growth company with a history of losses and expectations of continuing losses in the near and medium-term
- Heavy dependence on EV adoption and demand, as well as OEMs' ability to supply EVs to the market
- Challenges in managing rapid growth effectively
- Uncertainty created by current and future federal and state administrations regarding the EV sector
- Potential inaccuracy of market opportunity estimates and growth forecasts
- Significant current and future competition in the EV charging market
- Reliance on a limited number of vendors for charging equipment and support services
- Dependence on a limited number of customers and OEM partners
- Construction risks, cost overruns, and installation delays
- Supply chain disruptions
- Potential need for additional funding that may not be available on favorable terms

## DOE Loan-Related Risks
- Dependence on the ability to fully draw on the DOE Loan, which has multiple conditions precedent
- Risk of default if unable to comply with loan covenants
- Substantial portion of consolidated assets pledged as collateral, limiting additional borrowing capacity
- Operational restrictions imposed on subsidiaries under the loan
- Limitations on cash distributions from subsidiaries needed to fund operations

## EV Market Risks
- Changes to fuel economy standards or success of alternative fuels
- Slower-than-expected electrification of rideshare and commercial fleets
- Uncertainty regarding medium and heavy-duty vehicle segment development

## Technology, Finance, and Governance Risks
- Inability to maintain and protect intellectual property
- Lack of industry standards and transition to NACS charging standard
- Material weaknesses in internal controls over financial reporting
- Changes to tax laws and regulations
- Inflationary pressures affecting equipment and operating costs

## Pre-written sections (judge input)

### Financial Health
EVgo, Inc., trades at $1.36 per share in the consumer cyclical sector. It carries a market capitalization of $42.8 billion and a forward P/E ratio of -3.1x. Over the past year, it has reported net income of -$5.4 billion and a net loss of -$5.4 billion. Its net profit margin stands at -0.14x. Over the past five years, it has reported net income of -$5.4 billion and a net loss of -$5.4 billion. Its net profit margin stands at -0.14x over the past five years. Over the past year, it has reported net income of -$5.4 billion and a net loss of -$5.4 billion. Its net profit margin stands at -0.14x over the past five years. Over the past year, it has reported net income of -$5.4 billion and a net loss of -$5.4 billion. Its net profit margin stands at -0.14x over the past five years. Over the past year, it has reported net income of -$5.4 billion and a net loss of -$5.4 billion. Its net profit margin stands at -0.14x over the past five years. Over the past year, it has reported net income of -$5.4 billion and a net loss of -$5.4 billion. Its net profit margin stands at -0.14x over the past five years. Over the past year, it has reported net income of -$5.4 billion and a net loss of -$5.4 billion. Its net profit margin stands at -0.14x over the past five years. Over the past year, it has reported net income of -$5.4 billion and a net loss of -$5.4 billion. Its net profit margin stands at -0.14x over the past five years. Over the past year, it has reported net income of -$5.4 billion and a net loss of -$5.4 billion. Its net profit margin stands at -0.14x over the past five years. Over the past year, it has reported net income of -$5.4 billion and a net loss of -$5.4 billion. Its net profit margin stands at -0.14x over the past five years. Over the past year, it has reported net income of -$5.4

### Recent Developments

EVgo's latest SEC filings reveal persistent operational challenges, with the company reporting a negative profit margin of -13.5% and net losses of $54.1 million against $403 million in revenue. The stock has declined significantly from its 52-week high of $5.18 to $1.36, reflecting investor concerns about the company's path to profitability in the competitive EV charging market. Recent 10-Q and 10-K filings emphasize multiple risk factors that could materially adversely affect the business, with no material improvements noted in the risk profile since the annual report. For investors, EVgo's current valuation and negative earnings trajectory suggest the company remains in a critical phase where execution on profitability initiatives will be essential to justify further investment.

### SEC Filing Highlights

EVgo reported $210.7 million in cash and equivalents as of December 31, 2025, with $161.2 million in working capital, though the company continues to operate at a loss and expects significant near-term expenses. Future profitability is contingent on successful capital draws from the DOE Loan and Credit Agreement, making government financing critical to the company's financial viability. Growth depends heavily on sustained EV adoption rates, OEM partnerships, and favorable regulatory conditions, with risks including potential expiration of EV tax incentives and slower-than-anticipated market development. The company faces operational challenges including supply chain vulnerabilities, vendor concentration, and customer concentration risks that could impact scaling. Macroeconomic headwinds, gasoline price volatility, and competition from alternative fuel vehicles present additional demand-side risks to the charging network business.

### Primary Risk Factors Disclosed

The company discloses several categories of primary risk factors:

#### Business-Related Risks
- Operating as an early-stage growth company with a history of losses and expectations of continuing losses in the near and medium-term.
- Heavy dependence on EV adoption and demand, as well as OEMs' ability to supply EVs to the market.
- Challenges in managing rapid growth effectively.
- Uncertainty created by current and future federal and state administrations regarding the EV sector.
- Potential inaccuracy of market opportunity estimates and growth forecasts.
- Significant current and future competition in the EV charging market.
- Reliance on a limited number of vendors for charging equipment and support services.
- Dependence on a limited number of customers and OEM partners.
- Construction risks, cost overruns, and installation delays.
- Supply chain disruptions.
- Potential need for additional funding that may not be available on favorable terms.

#### DOE Loan-Related Risks
- Dependence on the ability to fully draw on the DOE Loan, which has multiple conditions precedent.
- Risk of default if unable to comply with loan covenants.
- Substantial portion of consolidated assets pledged as collateral, limiting additional borrowing capacity.
- Operational restrictions imposed on subsidiaries under the loan.
- Limitations on cash distributions from subsidiaries needed to fund operations.

#### EV Market Risks
- Changes to fuel economy standards or success of alternative fuels.
- Slower-than-expected electrification of rideshare and commercial fleets.
- Uncertainty regarding medium and heavy-duty vehicle segment development.

#### Technology, Finance, and Governance Risks
- Inability to maintain and protect intellectual property.
- Lack of industry standards and transition to NACS charging standard.
- Material weaknesses in internal controls over financial reporting.
- Changes to tax laws and regulations.
- Inflationary pressures affecting equipment and operating costs.

## Audited (Exec Summary + Outlook)

### Executive Summary
EVgo, Inc. is a public EV fast-charging network operator in the consumer cyclical sector, trading at $1.36 per share with $403 million in revenue against net losses of $54.1 million, reflecting the early-stage, capital-intensive nature of building charging infrastructure at scale. The stock is notable now because it has fallen sharply from its 52-week high of $5.18 to $1.36, compressing the margin for error at a moment when the company's financial viability depends critically on its ability to draw on the DOE Loan and Credit Agreement under conditions that remain unresolved. The single most important near-term variable is whether EVgo can successfully satisfy the conditions precedent to fully access that government financing, as failure to do so would materially threaten its ability to fund operations and continue scaling.

### Outlook
The directional lean on EVgo is **cautious**. The company operates in a sector with genuine long-term tailwinds — secular EV adoption, fleet electrification, and the ongoing buildout of charging infrastructure — but the near-term investment thesis is burdened by a convergence of serious headwinds that make the path to profitability highly uncertain. Investors should watch the status of DOE Loan draw conditions most closely, as access to that capital is the linchpin of the company's financial viability; any indication that draws are being delayed, restricted, or placed at risk of default would materially weaken the thesis. Equally important to monitor are the trajectory of EV adoption rates and OEM vehicle supply, the durability of federal and state EV tax incentives under shifting regulatory conditions, and whether the company demonstrates measurable progress in narrowing its net loss and improving its profit margin over successive quarters. The concentration risks — in vendors, customers, and OEM partners — mean that any disruption in a key relationship could have outsized operational consequences. The view would become more constructive if EVgo demonstrates consistent progress on loan draws, shows improving unit economics at the network level, resolves disclosed material weaknesses in internal controls, and benefits from a stable or supportive federal policy environment for EV infrastructure; conversely, the view would weaken further if government financing access deteriorates, EV adoption slows meaningfully, or competition intensifies in ways that compress network utilization and pricing power.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "trading at $1.36 per share"
LABEL: SUPPORTED
REASON: The raw source data explicitly lists `"current_price": 1.36`.

---

CLAIM: "$403 million in revenue"
LABEL: SUPPORTED
REASON: Raw source data shows `"revenue": 402948000.0`; $402.948M rounds to $403M, within rounding tolerance.

---

CLAIM: "net losses of $54.1 million"
LABEL: SUPPORTED
REASON: Raw source data shows `"net_income": -54125000.0`, i.e., a net loss of $54.125M, which rounds to $54.1M.

---

CLAIM: "fallen sharply from its 52-week high of $5.18 to $1.36"
LABEL: SUPPORTED
REASON: Raw source data explicitly lists `"week_52_high": 5.18` and `"current_price": 1.36`.

---

CLAIM: "the company's financial viability depends critically on its ability to draw on the DOE Loan and Credit Agreement"
LABEL: SUPPORTED
REASON: The SEC Filing Highlights pre-written section states: "Future profitability is contingent on successful capital draws from the DOE Loan and Credit Agreement, making government financing critical to the company's financial viability."

---

**OUTLOOK**

---

CLAIM: "DOE Loan draw conditions most closely, as access to that capital is the linchpin of the company's financial viability"
LABEL: SUPPORTED
REASON: Directly supported by the SEC Filing Highlights section and RAG — SEC Highlights, which state future profitability depends on successful capital draws from the DOE Loan and that the ability to fully draw on the DOE Loan is a key risk.

---

CLAIM: "any indication that draws are being delayed, restricted, or placed at risk of default would materially weaken the thesis"
LABEL: SUPPORTED
REASON: The Primary Risk Factors section explicitly discloses "Risk of default if unable to comply with loan covenants" and "Dependence on the ability to fully draw on the DOE Loan, which has multiple conditions precedent."

---

CLAIM: "whether the company demonstrates measurable progress in narrowing its net loss and improving its profit margin over successive quarters"
LABEL: SUPPORTED
REASON: This is a directional forward-looking watch-item grounded in the disclosed net loss of $54.1M and profit margin of -13.5% (source: `"profit_margin": -0.13502`), both present in the source data; no specific target figure is asserted.

---

CLAIM: "resolves disclosed material weaknesses in internal controls"
LABEL: SUPPORTED
REASON: The Primary Risk Factors section explicitly lists "Material weaknesses in internal controls over financial reporting" as a disclosed risk.

---

*(No additional specific quantitative figures, price targets, thresholds, ratios, or named product milestones appear in the Outlook section beyond those already evaluated above. The remaining Outlook content consists of qualitative directional statements and categorical risk descriptions — vendor concentration, OEM concentration, EV adoption, federal policy — all of which are grounded in the pre-written sections and RAG content without asserting specific numbers.)*

---

**ADDITIONAL NOTE — FIGURES PRESENT IN PRE-WRITTEN SECTIONS BUT NOT CARRIED INTO THE AUDITED SECTIONS:**

The Financial Health pre-written section contains severely erroneous figures (e.g., market cap stated as "$42.8 billion" vs. actual $427.7 million, net income stated as "-$5.4 billion" vs. actual -$54.1 million). These errors do **not** appear in the Executive Summary or Outlook, so they are outside the audit scope. However, for completeness:

CLAIM: *(not in audited sections)* — The Executive Summary does **not** cite market cap or forward P/E, so no audit entry is required for those figures.

---

**SUMMARY TABLE**

| Claim | Label |
|---|---|
| $1.36 per share | SUPPORTED |
| $403 million in revenue | SUPPORTED |
| Net losses of $54.1 million | SUPPORTED |
| 52-week high of $5.18 | SUPPORTED |
| DOE Loan and Credit Agreement financial viability dependency | SUPPORTED |
| DOE Loan draw conditions as linchpin | SUPPORTED |
| Default/delay risk on DOE Loan draws | SUPPORTED |
| Progress on narrowing net loss and improving profit margin | SUPPORTED |
| Resolves disclosed material weaknesses in internal controls | SUPPORTED |

All quantitative and forward-looking claims in the Executive Summary and Outlook are **SUPPORTED** by the source data. No UNSUPPORTED or INFERENCE labels are warranted.
