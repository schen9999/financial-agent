# TSM — rerank3

## Metadata

ticker: TSM
arm: rerank3
judge_prompt_version: v2
context_sha256: 005e3b79586d06677f0c25f10ecab44cb2954aa64ab0680f04959e109c0bbad8
llm_calls: 5
llm_endpoints: anthropic
llm_by_site: {"section:financial_health": {"calls": 1, "completion_tokens": 181, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.201, "latency_s_total": 2.201, "parse_failure": 0, "prompt_tokens": 347, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 127, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.915, "latency_s_total": 1.915, "parse_failure": 0, "prompt_tokens": 340, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 210, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.021, "latency_s_total": 3.021, "parse_failure": 0, "prompt_tokens": 337, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 88, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.379, "latency_s_total": 1.379, "parse_failure": 0, "prompt_tokens": 345, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1140, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.597, "latency_s_total": 17.597, "parse_failure": 0, "prompt_tokens": 1674, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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

TSM trades at $472.20 USD with a market capitalization of $2.45 trillion USD, reflecting its position as a global semiconductor leader. The current P/E ratio of 35.06x appears elevated relative to the forward P/E of 21.54x, suggesting market expectations for earnings growth. The company demonstrates exceptional profitability with revenue of 4.44 trillion TWD and net income of 2.22 trillion TWD, translating to an impressive 49.92% profit margin that underscores operational excellence and pricing power. With a modest dividend yield of 0.78%, TSM prioritizes reinvestment in capital-intensive manufacturing capabilities. Overall, TSM exhibits robust financial health supported by strong earnings generation, though valuation multiples warrant monitoring amid cyclical semiconductor industry dynamics.

### Recent Developments

No recent news or SEC filings are currently available for TSM. Investors should monitor upcoming quarterly earnings reports and regulatory filings for updates on the company's advanced chip manufacturing capacity, geopolitical developments affecting Taiwan operations, and demand trends in AI and high-performance computing segments. TSM's strong financial position—with 4.44 trillion TWD in revenue and a 49.92% profit margin—provides a solid foundation, though the elevated forward P/E ratio of 21.54x suggests current valuations reflect high growth expectations that warrant close attention to execution.

### SEC Filing Highlights

No recent 10-K or 10-Q filings were available for review. As a Taiwan-listed company, TSM files with the Taiwan Stock Exchange rather than the SEC, so traditional U.S. securities filings are not applicable. Investors should refer to TSM's financial reports and disclosures filed with Taiwan regulatory authorities for the most current operational and financial information.

### Risk Factors

• **Geopolitical and Taiwan Exposure Risk** – As a Taiwan-based foundry serving global customers, TSM faces significant exposure to U.S.-China tensions, potential Taiwan strait instability, and evolving semiconductor export restrictions that could disrupt operations, limit market access, or trigger supply chain relocations.

• **High Valuation and Cyclical Demand** – Trading at a forward P/E of 21.5x with a 49.9% profit margin, TSM's premium valuation leaves limited margin for error. Semiconductor demand is cyclical, and any downturn in customer capex or end-market weakness could pressure earnings and multiples significantly.

• **Concentrated Customer Base and Technology Competition** – TSM's revenue is heavily dependent on a small number of large customers (particularly in AI/data center), and it faces intense competition from Samsung and Intel in advanced node manufacturing, risking market share loss and pricing pressure.

## Audited (Exec Summary + Outlook)

### Executive Summary
Taiwan Semiconductor Manufacturing Company is the world's dominant pure-play foundry, manufacturing advanced chips for the majority of the global semiconductor industry, and its scale is reflected in a market capitalization of $2.45 trillion USD, revenue of 4.44 trillion TWD, and a 49.92% profit margin that is exceptional for a capital-intensive manufacturer. The stock is notable today because its premium valuation — with a trailing P/E of 35.06x compressing toward a forward P/E of 21.54x — implies the market is pricing in substantial earnings growth, making execution on that growth trajectory the central investment question. The single most important near-term variable is the trajectory of AI and high-performance computing demand from TSM's largest customers, as sustained strength there would validate current valuation multiples, while any softening would expose the stock to meaningful multiple compression.

### Outlook
The directional outlook for TSM is **cautiously constructive**, supported by powerful structural tailwinds — most notably the accelerating global demand for AI inference and training chips, which flows directly through TSM's advanced node manufacturing capacity — but tempered by a risk profile that is unusually wide for a company of this quality. On the positive side, TSM's technological leadership in advanced node fabrication and its entrenched position across the global fabless ecosystem create durable competitive advantages that are difficult for Samsung or Intel to displace quickly. The key variables an investor should monitor include: the pace and durability of AI-driven customer orders, the trajectory of U.S.-China geopolitical tensions and any escalation in semiconductor export restrictions, TSM's progress in geographic diversification of its manufacturing footprint, and whether the gap between the trailing and forward P/E ratios closes through earnings growth rather than price decline. The thesis would strengthen if AI and high-performance computing demand proves more durable and broad-based than currently anticipated, if geopolitical risks stabilize, and if TSM demonstrates continued pricing power alongside its 49.92% profit margin. Conversely, the thesis would weaken materially if semiconductor end-market demand turns cyclically lower, if a key customer meaningfully reduces orders or pursues in-house fabrication, or if geopolitical developments around Taiwan escalate in ways that threaten operational continuity or trigger customer supply chain diversification away from TSM.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

## EXECUTIVE SUMMARY

---

CLAIM: "market capitalization of $2.45 trillion USD"
LABEL: SUPPORTED
REASON: Source data shows market_cap = 2,449,053,057,024.0 USD ≈ $2.45 trillion; the pre-written Financial Health section also states "$2.45 trillion USD."

---

CLAIM: "revenue of 4.44 trillion TWD"
LABEL: SUPPORTED
REASON: Source data shows revenue = 4,440,492,343,296.0 TWD ≈ 4.44 trillion TWD, confirmed in the pre-written sections.

---

CLAIM: "49.92% profit margin"
LABEL: SUPPORTED
REASON: Source data explicitly states profit_margin_pct = 49.92; confirmed in pre-written sections.

---

CLAIM: "trailing P/E of 35.06x"
LABEL: SUPPORTED
REASON: Source data shows pe_ratio = 35.05568, which rounds to 35.06x; confirmed in the pre-written Financial Health section.

---

CLAIM: "forward P/E of 21.54x"
LABEL: SUPPORTED
REASON: Source data shows forward_pe = 21.53696, which rounds to 21.54x; confirmed in the pre-written sections.

---

## OUTLOOK

---

CLAIM: "Samsung or Intel" (named as competitors in advanced node manufacturing)
LABEL: SUPPORTED
REASON: The pre-written Risk Factors section explicitly names "Samsung and Intel in advanced node manufacturing" as competitors.

---

CLAIM: "49.92% profit margin" (second mention, in Outlook)
LABEL: SUPPORTED
REASON: Source data explicitly states profit_margin_pct = 49.92; confirmed in pre-written sections.

---

*No additional standalone quantitative figures, price targets, thresholds, ratios, specific percentages, named product milestones, or forward-looking numbers appear in the Outlook section beyond those already audited above. All qualitative directional statements (e.g., "cautiously constructive," "durable competitive advantages," "meaningful multiple compression") contain no specific quantitative claims requiring verification.*

---

### Summary Table

| Claim | Label |
|---|---|
| Market cap $2.45 trillion USD | SUPPORTED |
| Revenue 4.44 trillion TWD | SUPPORTED |
| Profit margin 49.92% | SUPPORTED |
| Trailing P/E 35.06x | SUPPORTED |
| Forward P/E 21.54x | SUPPORTED |
| Samsung and Intel as competitors | SUPPORTED |
| Profit margin 49.92% (Outlook repeat) | SUPPORTED |

**All auditable quantitative and named-entity claims in the Executive Summary and Outlook are SUPPORTED by the source data or pre-written sections.**
