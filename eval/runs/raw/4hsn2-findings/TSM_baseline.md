# TSM — baseline

## Metadata

ticker: TSM
arm: baseline
judge_prompt_version: v2
context_sha256: 2c350e8c3b248648a0ed88a4069972bd8385698e0199ac469c8636d2df4b14a1
llm_calls: 5
llm_endpoints: anthropic
llm_by_site: {"section:financial_health": {"calls": 1, "completion_tokens": 180, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.497, "latency_s_total": 2.497, "parse_failure": 0, "prompt_tokens": 370, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 118, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.904, "latency_s_total": 1.904, "parse_failure": 0, "prompt_tokens": 363, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 191, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.818, "latency_s_total": 2.818, "parse_failure": 0, "prompt_tokens": 360, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 87, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.332, "latency_s_total": 1.332, "parse_failure": 0, "prompt_tokens": 368, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1037, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 15.395, "latency_s_total": 15.395, "parse_failure": 0, "prompt_tokens": 1614, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "TSM",
  "company_name": "Taiwan Semiconductor Manufacturing Company Limited",
  "current_price": 485.8,
  "currency": "USD",
  "market_cap": 2519588929536.0,
  "pe_ratio": 35.30523,
  "forward_pe": 22.157253,
  "week_52_high": 487.44,
  "week_52_low": 266.82,
  "financial_currency": "TWD",
  "revenue": 4440492343296.0,
  "net_income": 2216808415232.0,
  "profit_margin_pct": 49.92,
  "dividend_yield": 0.78,
  "sector": "Technology",
  "industry": "Semiconductors"
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
    "message": "No 10-K found"
  },
  "10-Q": {
    "message": "No 10-Q found"
  }
}

RAG — SEC HIGHLIGHTS:
(not available)

RAG — RISK FACTORS:
(not available)

## Pre-written sections (judge input)

### Financial Health

TSM trades at $485.80 USD with a market capitalization of $2.52 trillion USD, reflecting its position as a global semiconductor leader. The company generated revenue of 4.44 trillion TWD with exceptional profitability, posting a net income of 2.22 trillion TWD and a profit margin of 49.92%—demonstrating strong operational efficiency and pricing power. The current P/E ratio of 35.31x appears elevated relative to the forward P/E of 22.16x, suggesting market expectations for earnings growth moderation. With a modest dividend yield of 0.78%, TSM prioritizes reinvestment and capital allocation for growth. Overall, TSM exhibits robust financial health with industry-leading margins, though valuation multiples warrant monitoring given cyclical semiconductor dynamics.

### Recent Developments

No recent news or SEC filings are currently available for TSM. Investors should monitor upcoming earnings announcements and regulatory filings for updates on the company's advanced chip manufacturing capacity, geopolitical developments affecting Taiwan operations, and demand trends in AI and high-performance computing segments. TSM's strong financial position—with 4.44 trillion TWD in revenue and a 49.92% profit margin—provides a solid foundation, though the elevated forward P/E of 22.16x warrants attention to growth execution.

### SEC Filing Highlights

No recent SEC filings (10-K or 10-Q) are currently available for Taiwan Semiconductor Manufacturing Company Limited. As a Taiwan-listed company, TSM files with the Taiwan Stock Exchange rather than the U.S. Securities and Exchange Commission. Investors seeking detailed financial disclosures should refer to TSM's earnings reports and announcements filed with Taiwan regulatory authorities.

### Risk Factors

• **Geopolitical and Taiwan Exposure Risk** – As a Taiwan-based company, TSM faces significant geopolitical risks including potential cross-strait tensions, U.S.-China trade restrictions, and export controls that could disrupt operations, supply chains, and market access for key customers.

• **High Valuation and Cyclical Industry Dynamics** – Trading at a P/E ratio of 35.3x, TSM carries elevated valuation risk in a cyclical semiconductor industry prone to demand fluctuations, pricing pressures, and potential margin compression during downturns.

• **Concentrated Customer Base and Technology Competition** – Heavy reliance on a limited number of major customers (particularly in AI and smartphone sectors) combined with intense competition from Samsung, Intel, and others creates revenue concentration risk and pressure to maintain technological leadership through substantial capital expenditures.

## Audited (Exec Summary + Outlook)

### Executive Summary
Taiwan Semiconductor Manufacturing Company Limited is the world's leading dedicated semiconductor foundry, commanding a $2.52 trillion USD market capitalization and delivering industry-leading profitability with a net income of 2.22 trillion TWD on revenue of 4.44 trillion TWD and a profit margin of 49.92%. The stock is notable now because its current P/E of 35.31x sits meaningfully above its forward P/E of 22.16x, creating a valuation setup where the market is pricing in significant earnings growth even as cyclical and geopolitical risks remain elevated. The single most important near-term variable is whether demand from AI and high-performance computing customers proves durable enough to justify that growth expectation and sustain TSM's exceptional margins through the next earnings cycle.

### Outlook
The directional outlook for TSM is **cautiously constructive**, supported by powerful structural tailwinds in AI and high-performance computing demand, TSM's unmatched position at the leading edge of semiconductor manufacturing, and a financial profile that demonstrates exceptional pricing power and operational discipline. However, that constructive lean is tempered by meaningful headwinds: the gap between the current and forward P/E ratios places the burden squarely on earnings execution, leaving little room for demand disappointment or margin erosion. Investors should monitor the trajectory of AI-related chip orders and whether that demand proves broad and sustained or concentrated and episodic; the evolution of U.S.-China trade policy and export controls, which represent the most acute near-term risk to both customer access and supply chain continuity; and cross-strait geopolitical developments, which carry the potential to reprice the stock sharply regardless of underlying fundamentals. Progress on geographic diversification of manufacturing capacity could gradually reduce the geopolitical risk premium embedded in the valuation, strengthening the thesis, while any signs of customer concentration risk materializing, margin compression, or an escalation in Taiwan-related tensions would warrant a more cautious stance.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$2.52 trillion USD market capitalization"
LABEL: SUPPORTED
REASON: Source data shows market_cap = 2,519,588,929,536.0 USD, which rounds to $2.52 trillion USD; the pre-written Financial Health section also states "$2.52 trillion USD."

---

CLAIM: "net income of 2.22 trillion TWD"
LABEL: SUPPORTED
REASON: Source data shows net_income = 2,216,808,415,232.0 TWD, which rounds to 2.22 trillion TWD; confirmed in the Financial Health section.

---

CLAIM: "revenue of 4.44 trillion TWD"
LABEL: SUPPORTED
REASON: Source data shows revenue = 4,440,492,343,296.0 TWD, which rounds to 4.44 trillion TWD; confirmed in the Financial Health section.

---

CLAIM: "profit margin of 49.92%"
LABEL: SUPPORTED
REASON: Source data explicitly states profit_margin_pct = 49.92; also confirmed in the Financial Health section.

---

CLAIM: "current P/E of 35.31x"
LABEL: SUPPORTED
REASON: Source data shows pe_ratio = 35.30523, which rounds to 35.31x; confirmed in the Financial Health section.

---

CLAIM: "forward P/E of 22.16x"
LABEL: SUPPORTED
REASON: Source data shows forward_pe = 22.157253, which rounds to 22.16x; confirmed in the Financial Health section.

---

**OUTLOOK**

---

CLAIM: "the gap between the current and forward P/E ratios"
LABEL: SUPPORTED
REASON: Both figures are present in the source data (35.31x current P/E vs. 22.16x forward P/E); the gap of approximately 13.15 points is arithmetically verifiable from those two figures.

---

*(No additional specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section beyond the P/E gap reference already audited above. All other statements in the Outlook are qualitative directional or risk characterizations — e.g., "cautiously constructive," "meaningful headwinds," "most acute near-term risk" — and contain no specific quantitative claims subject to audit under the defined criteria.)*

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | $2.52 trillion USD market cap | SUPPORTED |
| 2 | Net income of 2.22 trillion TWD | SUPPORTED |
| 3 | Revenue of 4.44 trillion TWD | SUPPORTED |
| 4 | Profit margin of 49.92% | SUPPORTED |
| 5 | Current P/E of 35.31x | SUPPORTED |
| 6 | Forward P/E of 22.16x | SUPPORTED |
| 7 | Gap between current and forward P/E | SUPPORTED |

All audited quantitative claims in the Executive Summary and Outlook are **SUPPORTED** by the raw source data. No unsupported or inference-only quantitative claims were identified.
