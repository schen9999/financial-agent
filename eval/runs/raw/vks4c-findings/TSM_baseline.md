# TSM — baseline

## Metadata

ticker: TSM
arm: baseline
judge_prompt_version: v2
context_sha256: 005e3b79586d06677f0c25f10ecab44cb2954aa64ab0680f04959e109c0bbad8
llm_calls: 5
llm_endpoints: anthropic
llm_by_site: {"section:financial_health": {"calls": 1, "completion_tokens": 185, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.277, "latency_s_total": 2.277, "parse_failure": 0, "prompt_tokens": 347, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 127, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.891, "latency_s_total": 1.891, "parse_failure": 0, "prompt_tokens": 340, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 200, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.632, "latency_s_total": 2.632, "parse_failure": 0, "prompt_tokens": 337, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 88, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.341, "latency_s_total": 1.341, "parse_failure": 0, "prompt_tokens": 345, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1101, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 16.946, "latency_s_total": 16.946, "parse_failure": 0, "prompt_tokens": 1662, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "TSM",
  "company_name": "Taiwan Semiconductor Manufacturing Company Limited",
  "current_price": 472.2,
  "currency": "USD",
  "market_cap": 2449053057024.0,
  "pe_ratio": 35.05568,
  "forward_pe": 21.53696,
  "week_52_high": 487.47,
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
[]

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

TSM trades at $472.20 USD with a market capitalization of $2.45 trillion USD, reflecting its position as a global semiconductor leader. The current P/E ratio of 35.06x appears elevated relative to the forward P/E of 21.54x, suggesting market expectations for earnings growth. The company demonstrates exceptional profitability with revenue of 4.44 trillion TWD and net income of 2.22 trillion TWD, translating to an impressive 49.92% profit margin that underscores operational excellence and pricing power. The modest 0.78% dividend yield indicates TSM prioritizes reinvestment and capital allocation for growth rather than shareholder distributions. Overall, TSM exhibits robust financial health with strong earnings generation, though current valuation multiples warrant monitoring relative to semiconductor industry cyclicality.

### Recent Developments

No recent news or SEC filings are currently available for TSM. Investors should monitor upcoming quarterly earnings reports and regulatory filings for updates on the company's advanced chip manufacturing capacity, geopolitical developments affecting Taiwan operations, and demand trends in AI and high-performance computing segments. TSM's strong financial position—with 4.44 trillion TWD in revenue and a 49.92% profit margin—provides a solid foundation, though the elevated forward P/E ratio of 21.54x suggests current valuations reflect high growth expectations that warrant close attention to execution.

### SEC Filing Highlights

No recent 10-K or 10-Q filings were available for review. As a Taiwan-listed company, TSM files with the Taiwan Stock Exchange rather than the SEC, so traditional U.S. securities filings are not applicable. Investors should refer to TSM's financial reports and disclosures filed with Taiwan regulatory authorities for the most current operational and financial information.

### Risk Factors

• **Geopolitical and Taiwan Exposure Risk** – As a Taiwan-based foundry serving global customers, TSM faces significant geopolitical risks including potential cross-strait tensions, U.S.-China trade restrictions, and export controls that could disrupt operations, supply chains, and customer access.

• **High Valuation and Cyclical Demand** – Trading at a forward P/E of 21.5x with a 49.9% profit margin, TSM's premium valuation leaves limited margin for error. Semiconductor demand is cyclical, and any downturn in customer orders or end-market weakness could pressure earnings and stock performance.

• **Intense Competition and Technology Obsolescence** – TSM faces relentless competition from Samsung and Intel in advanced chip manufacturing, requiring continuous capital investment in R&D and cutting-edge fabrication facilities to maintain technological leadership and market share.

## Audited (Exec Summary + Outlook)

### Executive Summary
Taiwan Semiconductor Manufacturing Company Limited is the world's dominant pure-play contract chip foundry, generating 4.44 trillion TWD in revenue and 2.22 trillion TWD in net income at a 49.92% profit margin — a level of profitability that reflects both its unrivaled manufacturing scale and the pricing power that comes with being the essential supplier to the global semiconductor industry. Trading at $472.20 USD with a $2.45 trillion USD market capitalization, TSM commands investor attention today because its gap between the current P/E of 35.06x and the forward P/E of 21.54x signals that the market is pricing in substantial earnings growth, making execution against that expectation the central investment question. The single most important near-term variable is whether demand from AI and high-performance computing customers remains strong enough to sustain the earnings trajectory the current valuation implies.

### Outlook
The directional outlook for TSM is **cautiously constructive**, supported by powerful secular tailwinds — most notably the sustained buildout of AI infrastructure and high-performance computing — that continue to drive demand for advanced semiconductor manufacturing capacity where TSM has no peer. The company's exceptional profit margin and dominant foundry position provide meaningful resilience, and its ongoing geographic diversification efforts represent a long-term structural positive for supply-chain risk management. That said, the constructive view is tempered by several headwinds that investors should monitor closely: the trajectory of cross-strait geopolitical tensions remains the single largest exogenous risk and could rapidly reprice the stock regardless of operational performance; the pace and durability of AI-driven chip demand will determine whether earnings growth justifies the gap between current and forward valuation multiples; and the competitive posture of Samsung and Intel in advanced nodes warrants ongoing scrutiny, as any meaningful erosion of TSM's technology lead would pressure both margins and market share. What would strengthen the thesis is consistent evidence of robust order flow from AI and hyperscaler customers, stable geopolitical conditions, and continued margin discipline; what would weaken it is any sign of demand softening, escalating export controls, or a deterioration in the cross-strait security environment.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "generating 4.44 trillion TWD in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of 4,440,492,343,296 TWD, which rounds to 4.44 trillion TWD; the pre-written Financial Health section also states "4.44 trillion TWD" in revenue.

---

CLAIM: "2.22 trillion TWD in net income"
LABEL: SUPPORTED
REASON: Source data shows net income of 2,216,808,415,232 TWD, which rounds to 2.22 trillion TWD; the pre-written Financial Health section also states "2.22 trillion TWD" in net income.

---

CLAIM: "49.92% profit margin"
LABEL: SUPPORTED
REASON: Source data explicitly lists profit_margin_pct as 49.92; the pre-written sections also state 49.92%.

---

CLAIM: "Trading at $472.20 USD"
LABEL: SUPPORTED
REASON: Source data lists current_price as 472.2 USD, matching the stated figure exactly.

---

CLAIM: "$2.45 trillion USD market capitalization"
LABEL: SUPPORTED
REASON: Source data lists market_cap as 2,449,053,057,024 USD, which rounds to $2.45 trillion; the pre-written Financial Health section also states "$2.45 trillion USD."

---

CLAIM: "current P/E of 35.06x"
LABEL: SUPPORTED
REASON: Source data lists pe_ratio as 35.05568, which rounds to 35.06x; the pre-written Financial Health section also states "35.06x."

---

CLAIM: "forward P/E of 21.54x"
LABEL: SUPPORTED
REASON: Source data lists forward_pe as 21.53696, which rounds to 21.54x; the pre-written Financial Health section also states "21.54x."

---

**OUTLOOK**

The Outlook section is largely qualitative and directional. I will identify every specific quantitative or named-metric claim within it.

---

CLAIM: (implicit reference to) "the gap between current and forward valuation multiples" (referencing the P/E gap between 35.06x and 21.54x)
LABEL: SUPPORTED
REASON: Both the current P/E of 35.06x and forward P/E of 21.54x are present in the source data and pre-written sections; the directional claim that a gap exists is arithmetically verified (35.06 − 21.54 = 13.52 points).

---

**No other specific quantitative figures, price targets, thresholds, ratios, percentages, named product milestones, or forward-looking numbers appear in the Outlook section.** All remaining claims in the Outlook are qualitative, directional, or conditional statements (e.g., "cautiously constructive," "no peer," "meaningful resilience," "largest exogenous risk," "ongoing geographic diversification efforts") that do not constitute auditable quantitative or specific factual claims under the defined scope.
