# CRBU — baseline

## Metadata

ticker: CRBU
arm: baseline
judge_prompt_version: v2
context_sha256: 994508322affe79716d8972125c20f3731a23fdd061766c3d47465165e226898
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 349, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.82, "latency_s_total": 3.82, "parse_failure": 0, "prompt_tokens": 3244, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 341, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.776, "latency_s_total": 3.776, "parse_failure": 0, "prompt_tokens": 2432, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 169, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.234, "latency_s_total": 2.234, "parse_failure": 0, "prompt_tokens": 668, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 169, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.043, "latency_s_total": 2.043, "parse_failure": 0, "prompt_tokens": 661, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 201, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.553, "latency_s_total": 2.553, "parse_failure": 0, "prompt_tokens": 418, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 186, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.916, "latency_s_total": 1.916, "parse_failure": 0, "prompt_tokens": 434, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1284, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.041, "latency_s_total": 19.041, "parse_failure": 0, "prompt_tokens": 1862, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "CRBU",
  "company_name": "Caribou Biosciences, Inc.",
  "current_price": 1.22,
  "currency": "USD",
  "market_cap": 130793168.0,
  "forward_pe": -0.9657018,
  "week_52_high": 3.535,
  "week_52_low": 1.215,
  "revenue": 10035000.0,
  "net_income": -103403000.0,
  "profit_margin": 0.0,
  "sector": "Healthcare",
  "industry": "Biotechnology"
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
    "filing_date": "2026-03-05",
    "summary": "Item 1A. Risk Factors. Investing in shares of our common stock involves a high degree of risk. You should carefully consider the following risks and uncertainties, together with all of the other information contained in this Annual Report on Form 10-K, including our financial statements and related notes, before making an investment decision. These disclosures reflect our beliefs and opinions as to factors that could materially and adversely affect our company and its securities in the future. References to past events are provided by way of example only and are not intended to be a complete listing or a representation as to whether or not such factors have occurred in the past or their likelihood of occurring in the future. Furthermore, the risks described below are not the only ones faci"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-13",
    "summary": "Item 1A. Risk Factors. There have been no material changes to the Risk Factors previously disclosed in Item 1A. to Part I of our Form 10-K. The risks described in our Form 10-K are not the only risks facing our company. Additional risks and uncertainties not currently known to us or that we currently deem to be immaterial also may materially adversely affect our business, financial condition, and/or operating results. Item 2. Unregistered Sales of Equity Securities, Use of Proceeds, and Issuer Purchases of Equity Securities. Unregistered Sales of Equity Securities during the Three Months Ended June 30, 2026 There were no unregistered sales of equity securities during the three months ended June 30, 2026. Item 5. Other Information. During the quarter ended June 30, 2026, none of our directo"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] # Key Takeaways from the Latest SEC Filings

## Financial Position and Losses

The company has incurred substantial operating losses since inception, with net losses of $148.1 million in 2025 and $149.1 million in 2024. An accumulated deficit of $596.5 million has been recorded as of December 31, 2025. No products have been commercialized, and the company has never generated revenue from product sales.

## Capital Requirements and Funding Needs

The company currently has $142.8 million in cash, cash equivalents, and marketable securities, which is expected to fund operations for at least the next 12 months. However, substantial additional financing will be required to:
- Conduct the planned pivotal clinical trial for vispa-cel
- Advance CB-011 beyond dose expansion
- Support ongoing research and development activities

Without additional capital, the company will be unable to complete development and commercialization of its product candidates.

## Development Stage and Operational Challenges

As a clinical-stage biotechnology company formed in 2011, the company has limited operating history with no approved products. Operations have focused on technology development and Phase 1 clinical trials. The company has not yet demonstrated the ability to obtain marketing approval, manufacture at commercial scale, or conduct commercial sales and marketing activities.

## Future Expense Expectations

Significant expenses are anticipated as the company progresses clinical trials, expands manufacturing capabilities, seeks regulatory approvals, and potentially establishes commercialization infrastructure. Capital consumption may accelerate due to unforeseen circumstances beyond management's control.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors related to its financial position and business operations:

## Financial and Capital Risks

- **Significant Operating Losses**: The company has incurred substantial net losses since inception ($148.1 million in 2025 and $149.1 million in 2024) with an accumulated deficit of $596.5 million, and anticipates continued losses for the foreseeable future.

- **No Revenue Generation**: The company has not commercialized any products and has never generated revenue from product sales.

- **Need for Additional Financing**: The company currently lacks sufficient funds to conduct its planned pivotal clinical trial for vispa-cel and requires substantial additional capital to implement its operating plans and develop its product candidates.

- **Uncertainty of Profitability**: There is no assurance the company will ever achieve profitability, and even if it does, it may not be able to sustain profitability on a quarterly or annual basis.

## Development and Commercialization Risks

- **Early Stage Operations**: The company has not yet demonstrated an ability to obtain marketing approval, manufacture at commercial scale, or conduct sales and marketing activities for its product candidates.

- **Extensive Development Requirements**: The allogeneic cell therapy product candidates are based on new technologies requiring extensive and costly development, particularly as they advance through clinical phases with greater numbers of patients.

- **Regulatory and Commercial Uncertainties**: The company faces uncertainties regarding regulatory clearances, manufacturing capabilities, and the ability to establish commercialization infrastructure.

## Pre-written sections (judge input)

### Financial Health

Caribou Biosciences trades at $1.22 per share with a market capitalization of $130.8 million, down significantly from its 52-week high of $3.54. The company generated $10.0 million in revenue but reported a net loss of $103.4 million, reflecting a negative profit margin typical of early-stage biotechnology firms in development phases. With a negative forward P/E ratio, traditional valuation metrics are not meaningful, indicating the company is not yet profitable. The substantial cash burn relative to revenue suggests Caribou is heavily dependent on capital raises and milestone achievements to fund operations. Investors should view this as a high-risk, pre-commercial stage biotech investment requiring careful monitoring of clinical progress and cash runway.

### Recent Developments

Caribou Biosciences' most recent SEC filings reveal no material changes to previously disclosed risk factors, suggesting a stable operational environment in the near term. The company's latest 10-Q filing (August 2026) indicates no significant corporate actions such as unregistered equity sales or director changes during Q2 2026. However, with a market capitalization of $131 million, negative net income of $103 million, and minimal revenue of $10 million, the company remains in a pre-commercial or early-stage revenue phase typical of biotechnology firms. Investors should note the substantial cash burn rate and lack of profitability, which underscores the high-risk nature of this investment pending successful clinical development and commercialization of pipeline assets.

### SEC Filing Highlights

Caribou Biosciences remains a pre-revenue clinical-stage company with substantial operating losses of $148.1 million in 2025 and an accumulated deficit of $596.5 million, with no approved products or product sales to date. The company's cash position of $142.8 million is expected to fund operations for at least 12 months, but significant additional financing will be required to advance its lead candidate vispa-cel through pivotal trials and develop CB-011. As a company with limited operating history since 2011, Caribou has not yet demonstrated the ability to obtain regulatory approval, achieve commercial-scale manufacturing, or execute commercialization activities. The company anticipates substantial near-term expense increases as it progresses clinical development and manufacturing capabilities, with capital consumption potentially accelerating due to unforeseen circumstances.

### Risk Factors

- **Significant Cash Burn and Funding Dependency**: Caribou has accumulated losses of $596.5 million with no revenue generation to date. The company requires substantial additional capital to fund its pivotal clinical trial for vispa-cel and has no assurance of achieving profitability, creating material risk of dilution or financing challenges.

- **Early-Stage Cell Therapy Technology**: Vispa-cel and other allogeneic cell therapy candidates are based on novel technologies that have not yet demonstrated commercial viability. The company has not obtained marketing approval, achieved commercial-scale manufacturing, or established sales infrastructure, leaving significant regulatory and execution risk.

- **Clinical and Regulatory Uncertainty**: Success depends on completing pivotal trials, obtaining regulatory clearance, and demonstrating clinical efficacy and safety in larger patient populations—outcomes that remain unproven and subject to FDA requirements that could delay or prevent commercialization.

## Audited (Exec Summary + Outlook)

### Executive Summary
Caribou Biosciences is a clinical-stage biotechnology company developing allogeneic cell therapies, most notably its lead candidate vispa-cel, trading at $1.22 per share with a market capitalization of $130.8 million and an accumulated deficit of $596.5 million that reflects the long, capital-intensive path typical of novel cell therapy development. The stock has declined sharply from its 52-week high of $3.54, drawing attention as a speculative opportunity for investors willing to accept substantial binary risk in exchange for exposure to a differentiated CRISPR-based cell therapy platform. The single most important near-term variable is the clinical and regulatory progress of vispa-cel through its pivotal trial, as a meaningful readout — positive or negative — will disproportionately determine whether the company can attract the additional financing it requires to survive and scale.

### Outlook
The directional lean on Caribou Biosciences is **cautious**, with the possibility of turning more constructive contingent on specific, demonstrable clinical and operational milestones. The primary tailwind is the company's differentiated CRISPR-based allogeneic cell therapy platform, which — if validated clinically — could position vispa-cel competitively in a cell therapy landscape where off-the-shelf approaches remain largely unproven at scale. The cash position of $142.8 million provides a near-term operational runway of at least 12 months, offering a window for meaningful data generation without immediate financing distress. However, the headwinds are substantial: the company faces accelerating expense growth as pivotal trials advance, an accumulated deficit of $596.5 million with no approved products, and an inevitable need for additional capital that introduces meaningful dilution risk. Investors should watch the following key variables closely — the pace and quality of clinical data from the vispa-cel pivotal trial, any FDA interactions or regulatory guidance that could clarify or complicate the approval pathway, the company's ability to demonstrate progress on commercial-scale manufacturing, and the terms and timing of any future capital raises. The thesis would strengthen materially on compelling efficacy and safety data from vispa-cel, a clear regulatory pathway, or a strategic partnership that validates the platform and reduces financing dependency; it would weaken on clinical setbacks, trial delays, unfavorable FDA feedback, or a dilutive capital raise executed from a position of weakness.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "trading at $1.22 per share"
LABEL: SUPPORTED
REASON: The raw source data explicitly lists `"current_price": 1.22`.

---

CLAIM: "market capitalization of $130.8 million"
LABEL: SUPPORTED
REASON: Source data shows `"market_cap": 130793168.0`; rounding to one decimal place gives $130.8 million.

---

CLAIM: "accumulated deficit of $596.5 million"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors sections both explicitly state "An accumulated deficit of $596.5 million has been recorded as of December 31, 2025."

---

CLAIM: "52-week high of $3.54"
LABEL: SUPPORTED
REASON: Source data shows `"week_52_high": 3.535`; rounding to two decimal places gives $3.54, consistent with the pre-written Financial Health section's "$3.54."

---

CLAIM: "The stock has declined sharply from its 52-week high of $3.54"
LABEL: SUPPORTED
REASON: Current price is $1.22 and 52-week high is $3.535; $1.22 < $3.535 confirms a sharp decline arithmetically (approximately 65% below the high).

---

**OUTLOOK**

---

CLAIM: "cash position of $142.8 million"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "The company currently has $142.8 million in cash, cash equivalents, and marketable securities."

---

CLAIM: "near-term operational runway of at least 12 months"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states the $142.8 million "is expected to fund operations for at least the next 12 months."

---

CLAIM: "accumulated deficit of $596.5 million with no approved products"
LABEL: SUPPORTED
REASON: Both the RAG SEC Highlights and Risk Factors sections explicitly state the $596.5 million accumulated deficit and confirm "No products have been commercialized."

---

CLAIM: "accelerating expense growth as pivotal trials advance"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "Significant expenses are anticipated as the company progresses clinical trials" and "Capital consumption may accelerate due to unforeseen circumstances beyond management's control."

---

CLAIM: "vispa-cel pivotal trial" (as a named product milestone)
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors both explicitly name "vispa-cel" and its "planned pivotal clinical trial" as a key development milestone.

---

CLAIM: "CB-011" (as a named pipeline asset referenced implicitly via "develop CB-011")
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly names "CB-011" as a pipeline candidate requiring additional capital to advance beyond dose expansion; the Outlook references the broader platform context consistent with this.

---

*No additional quantitative figures, price targets, thresholds, ratios, percentages, or forward-looking numbers appear in the Executive Summary or Outlook sections beyond those audited above.*
