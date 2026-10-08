# TSM — baseline

## Metadata

ticker: TSM
arm: baseline
judge_prompt_version: v2
context_sha256: be5de35bfd82b12c955adbcaac9422afd39f310284dfca4daabca78d2d17dc39
llm_calls: 5
llm_endpoints: anthropic
llm_by_site: {"section:financial_health": {"calls": 1, "completion_tokens": 165, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.056, "latency_s_total": 2.056, "parse_failure": 0, "prompt_tokens": 300, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 113, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.55, "latency_s_total": 1.55, "parse_failure": 0, "prompt_tokens": 293, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 196, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.765, "latency_s_total": 2.765, "parse_failure": 0, "prompt_tokens": 290, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 133, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.593, "latency_s_total": 1.593, "parse_failure": 0, "prompt_tokens": 298, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1088, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 16.94, "latency_s_total": 16.94, "parse_failure": 0, "prompt_tokens": 1616, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "TSM",
  "company_name": "Taiwan Semiconductor Manufacturing Company Limited",
  "current_price": 472.78,
  "currency": "USD",
  "market_cap": 2452061159424.0,
  "pe_ratio": 35.334827,
  "forward_pe": 21.563414,
  "week_52_high": 479.0,
  "week_52_low": 266.82,
  "revenue": 4440492343296.0,
  "net_income": 2216808415232.0,
  "profit_margin": 0.49923,
  "dividend_yield": 0.86,
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

TSM trades at $472.78 with a market capitalization of $2.45 trillion, reflecting its position as a global semiconductor leader. The company demonstrates exceptional profitability with a 49.9% net profit margin and annual revenue of $4.44 trillion, generating $2.22 trillion in net income. While the current P/E ratio of 35.3x appears elevated, the forward P/E of 21.6x suggests more reasonable valuation expectations as earnings growth materializes. The stock's 0.86% dividend yield provides modest income alongside capital appreciation potential, supported by strong fundamentals and consistent cash generation. Overall, TSM exhibits robust financial health with premium valuation justified by industry dominance and superior margins.

### Recent Developments

No recent news data is currently available for TSM. Investors should monitor upcoming earnings reports and regulatory filings, as TSM's strong financial position—with a 49.9% profit margin and $2.45 trillion market capitalization—makes company announcements particularly impactful for the semiconductor sector. The stock's current valuation at a forward P/E of 21.6x reflects market expectations for continued growth, though the absence of recent developments warrants caution until new information emerges.

### SEC Filing Highlights

SEC filings are currently unavailable for TSM. However, based on the latest financial metrics, the company demonstrates exceptional profitability with a 49.9% net profit margin and strong revenue of $4.44 trillion USD. TSM's market capitalization of $2.45 trillion reflects its dominant position in the semiconductor industry, though the elevated forward P/E ratio of 21.6x suggests investors are pricing in significant future growth expectations. The modest 0.86% dividend yield indicates the company prioritizes reinvestment in capital-intensive manufacturing operations rather than shareholder distributions.

### Risk Factors

• **Geopolitical and Regulatory Risk**: As Taiwan's largest company and a critical global semiconductor supplier, TSM faces significant exposure to U.S.-China trade tensions, potential Taiwan strait instability, and evolving export restrictions on advanced chip technology that could disrupt operations and market access.

• **Valuation and Cyclicality Risk**: Trading at a forward P/E of 21.6x with a 49.9% profit margin, TSM's premium valuation leaves limited margin for error. The cyclical semiconductor industry is vulnerable to demand downturns, inventory corrections, and pricing pressure that could compress margins and justify lower multiples.

• **Competitive and Technology Risk**: Intense competition from Samsung, Intel, and emerging players, combined with the capital-intensive nature of maintaining technological leadership in advanced node manufacturing, requires continuous heavy investment to sustain competitive advantages and market share.

## Audited (Exec Summary + Outlook)

### Executive Summary
Taiwan Semiconductor Manufacturing Company is the world's dominant pure-play contract chipmaker, commanding a $2.45 trillion market capitalization and delivering a 49.9% net profit margin that reflects unmatched scale and technological leadership in advanced node manufacturing. The stock is notable today because its current P/E of 35.3x appears stretched on the surface, yet the forward P/E of 21.6x implies the market is pricing in meaningful earnings growth ahead — creating a valuation story that hinges entirely on whether that growth materializes as expected. The single most important near-term variable is the trajectory of geopolitical risk surrounding the Taiwan Strait and U.S.-China trade policy, as an escalation in either could simultaneously disrupt operations, restrict market access, and compress the premium multiple the market currently awards TSM's exceptional fundamentals.

### Outlook
The directional outlook for TSM is **cautiously constructive**, supported by powerful structural tailwinds — including secular demand for advanced semiconductors across artificial intelligence, high-performance computing, and next-generation mobile — that play directly to TSM's manufacturing leadership. The key variables an investor should monitor are: the evolution of U.S.-China trade and export-control policy, which could either expand or sharply curtail TSM's addressable market; the pace at which the gap between the current P/E of 35.3x and the forward P/E of 21.6x closes through earnings delivery rather than multiple compression; the sustainability of the 49.9% net profit margin as capital reinvestment demands and competitive intensity from Samsung and Intel intensify; and any concrete developments regarding Taiwan Strait stability, which remains the single largest binary risk to the entire thesis. The constructive lean would strengthen if geopolitical conditions stabilize, earnings growth validates the forward multiple, and profit margins prove durable through the next semiconductor cycle. Conversely, the view would turn cautious if export restrictions broaden materially, a cyclical demand correction pressures margins, or geopolitical tensions escalate in a way that calls TSM's operational continuity into question.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number appearing in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$2.45 trillion market capitalization"
LABEL: SUPPORTED
REASON: Source data shows market_cap = 2,452,061,159,424, which rounds to $2.45 trillion; the pre-written sections also state "$2.45 trillion."

---

CLAIM: "49.9% net profit margin"
LABEL: SUPPORTED
REASON: Source data shows profit_margin = 0.49923, which rounds to 49.9%; confirmed in all pre-written sections.

---

CLAIM: "current P/E of 35.3x"
LABEL: SUPPORTED
REASON: Source data shows pe_ratio = 35.334827, which rounds to 35.3x; consistent with the pre-written Financial Health section.

---

CLAIM: "forward P/E of 21.6x"
LABEL: SUPPORTED
REASON: Source data shows forward_pe = 21.563414, which rounds to 21.6x; confirmed in all pre-written sections.

---

**OUTLOOK**

---

CLAIM: "current P/E of 35.3x"
LABEL: SUPPORTED
REASON: Source data shows pe_ratio = 35.334827, which rounds to 35.3x.

---

CLAIM: "forward P/E of 21.6x"
LABEL: SUPPORTED
REASON: Source data shows forward_pe = 21.563414, which rounds to 21.6x.

---

CLAIM: "49.9% net profit margin"
LABEL: SUPPORTED
REASON: Source data shows profit_margin = 0.49923, which rounds to 49.9%.

---

CLAIM: "competitive intensity from Samsung and Intel"
LABEL: SUPPORTED
REASON: Samsung and Intel are explicitly named as competitors in the pre-written Risk Factors section.

---

**No additional quantitative figures, price targets, thresholds, ratios, named product milestones, or forward-looking numbers appear in the Executive Summary or Outlook sections beyond those audited above.** All qualitative directional language (e.g., "cautiously constructive," "meaningful earnings growth," "secular demand") contains no specific quantitative claims requiring verification.
