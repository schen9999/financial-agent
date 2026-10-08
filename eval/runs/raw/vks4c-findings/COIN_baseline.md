# COIN — baseline

## Metadata

ticker: COIN
arm: baseline
judge_prompt_version: v2
context_sha256: 1c90d67b4516282bace59f0bcb3c459f5b74f5f425a25c0d31a01475c7faf66c
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 341, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.957, "latency_s_total": 3.957, "parse_failure": 0, "prompt_tokens": 3094, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 340, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.967, "latency_s_total": 3.967, "parse_failure": 0, "prompt_tokens": 2632, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 156, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.79, "latency_s_total": 1.79, "parse_failure": 0, "prompt_tokens": 648, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 206, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.796, "latency_s_total": 2.796, "parse_failure": 0, "prompt_tokens": 641, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 199, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.309, "latency_s_total": 2.309, "parse_failure": 0, "prompt_tokens": 413, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 158, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.215, "latency_s_total": 2.215, "parse_failure": 0, "prompt_tokens": 422, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1223, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 18.246, "latency_s_total": 18.246, "parse_failure": 0, "prompt_tokens": 1842, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "COIN",
  "company_name": "Coinbase Global, Inc.",
  "current_price": 178.45,
  "currency": "USD",
  "market_cap": 47081697280.0,
  "forward_pe": 62.903835,
  "week_52_high": 402.16,
  "week_52_low": 139.11,
  "financial_currency": "USD",
  "revenue": 6043752960.0,
  "net_income": -987766016.0,
  "profit_margin_pct": -16.34,
  "dividend_yield": 0.0,
  "sector": "Financial Services",
  "industry": "Financial Data & Stock Exchanges"
}

NEWS ARTICLES:
[]

SEC FILING SUMMARIES:
{
  "10-K": {
    "form_type": "10-K",
    "filing_date": "2026-02-12",
    "summary": "ITEM 1A. RISK FACTORS Investing in our Class A common stock involves a high degree of risk. You should carefully consider the risks and uncertainties described below, together with all of the other information in this Annual Report on Form 10-K, including the section titled \u201cManagement\u2019s Discussion and Analysis of Financial Condition and Results of Operations\u201d and the Consolidated Financial Statements and related notes. The risks and uncertainties described below are not the only ones we face. Additional risks and uncertainties that we are unaware of or that we deem immaterial may also become important factors that adversely affect our business. If any of the following risks occur, our business, operating results, financial condition, and future prospects could be materially and adversely "
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-07-30",
    "summary": "Item 1A Risk Factors in the Annual Report for additional details about these regulations. 41 Table of Contents We are required to hold corporate liquid assets at our subsidiaries to meet capital requirements established by our regulators based on the value of crypto assets and payment stablecoins held in custody. Our money-transmitting subsidiary, CB Inc., and our custodian subsidiary, Coinbase Custody Trust Company, LLC (\u201cCCTC\u201d), which is a fiduciary under New York State Law and a qualified custodian under the Investment Advisers Act of 1940, are required to maintain minimum net capital requirements under agreements with the New York State Department of Financial Services. These subsidiaries and other subsidiaries are also subject to maintenance capital requirements by other regulators bo"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] # Key Takeaways from Coinbase's Risk Disclosures

Based on the SEC filings provided, here are the primary risk factors and business considerations:

## Revenue Volatility and Crypto Dependence
Coinbase's operating results significantly fluctuate due to the highly volatile nature of cryptocurrency prices and trading volumes. The company's revenue is substantially dependent on crypto asset prices and transaction volumes on its platform, making it difficult to forecast growth accurately.

## Revenue Concentration Risk
A meaningful portion of revenue is concentrated in a limited number of areas:
- **Transaction revenue**: Approximately 45-46% of trading volume comes from Bitcoin and Ethereum transactions
- **Subscription and services revenue**: Heavily dependent on stablecoin revenue from payment stablecoins

If revenue from these concentrated areas declines without replacement from new demand, the business could be adversely affected.

## Multiple Risk Factors Affecting Operations
Operating results are influenced by numerous unpredictable factors including:
- Regulatory changes and government actions
- Ability to attract and retain customers and developers
- System failures and security breaches
- Competition from other platforms
- Macroeconomic conditions
- Market sentiment toward crypto assets

## Specific Bitcoin and Ethereum Risks
The company faces particular risks related to these major assets, including blockchain network challenges, environmental concerns, potential forks, scaling issues, and regulatory restrictions on mining or staking activities.

## Stock Price Volatility
The combination of these factors creates significant uncertainty, which could cause the Class A common stock price to fluctuate substantially.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company identifies several primary risk factors affecting its business:

## Operating Results Volatility
Operating results fluctuate significantly due to the highly volatile nature of crypto asset prices and market sentiment. This volatility makes it difficult to forecast growth trends accurately, and period-to-period comparisons may not be meaningful indicators of future performance.

## Revenue Dependency on Crypto Markets
Total revenue is substantially dependent on:
- Prices of crypto assets
- Volume of transactions conducted on the platform
- Declines in either could adversely affect business, operating results, and financial condition

## Revenue Concentration
Revenue is concentrated in limited areas, particularly:
- Bitcoin and Ethereum transactions (within transaction revenue)
- Payment stablecoin revenue (within subscription and services revenue)

If revenue from these concentrated areas declines without replacement from new demand, the business could be adversely affected.

## Crypto Asset Price and Volume Volatility
Crypto asset prices and transaction volumes are subject to significant uncertainty and volatility, influenced by numerous unpredictable factors including:
- Market conditions and sentiment toward crypto
- Trading activities on other platforms
- Regulatory and legislative changes
- Technological viability and security concerns
- Global economic and political conditions
- Banking system stability

## Operational and Competitive Factors
Additional risks include:
- Ability to attract and retain customers and talent
- Competition from other platforms and payment services
- System failures and security breaches
- Regulatory enforcement actions and legal proceedings
- Macroeconomic conditions affecting the broader economy

## Pre-written sections (judge input)

### Financial Health

Coinbase is trading at $178.45 with a market capitalization of $47.1 billion, reflecting significant volatility from its 52-week range of $139.11–$402.16. The company generated $6.0 billion in revenue but reported a net loss of $987.8 million, resulting in a negative profit margin of -16.34%, indicating operational challenges despite strong top-line growth. The forward P/E ratio of 62.9x suggests elevated valuation expectations relative to near-term earnings recovery. With no dividend yield and ongoing regulatory capital requirements, Coinbase's financial health remains dependent on achieving profitability and navigating the volatile cryptocurrency market environment.

### Recent Developments

Coinbase's latest SEC filings reveal heightened regulatory capital requirements for its custody and money-transmitting subsidiaries, reflecting intensified oversight of crypto asset holdings and stablecoin operations. The company's most recent 10-Q filing (July 2026) emphasizes compliance obligations with New York State regulators and other jurisdictions, which could impact operational flexibility and profitability. With a negative profit margin of -16.34% and net losses of approximately $988 million against $6.04 billion in revenue, Coinbase faces pressure to achieve profitability while managing these regulatory capital constraints. The elevated forward P/E ratio of 62.9x suggests investors are pricing in significant future growth expectations, making regulatory developments and path to profitability critical watch points. Investors should monitor how capital requirements affect margins and whether the company can leverage its $47 billion market cap position to scale profitably in the evolving regulatory environment.

### SEC Filing Highlights

Coinbase's revenue is highly volatile and concentrated, with approximately 45-46% of trading volume derived from Bitcoin and Ethereum transactions, creating significant dependency on a limited number of crypto assets. The company faces substantial operational risks including regulatory uncertainty, competitive pressures, and potential system failures, all of which could materially impact financial performance. Transaction revenue fluctuations are directly tied to cryptocurrency price movements and trading volumes, making earnings forecasting inherently unpredictable. Additionally, Coinbase's subscription and services revenue relies heavily on stablecoin adoption, introducing another concentration risk to the business model. These interconnected factors contribute to significant stock price volatility and warrant careful monitoring of regulatory developments and market sentiment toward digital assets.

### Risk Factors

• **Crypto Market Volatility and Revenue Dependency** – Operating results and total revenue are highly dependent on cryptocurrency asset prices and transaction volumes, which are subject to significant unpredictable fluctuations driven by market sentiment, regulatory changes, and global economic conditions. Declines in either metric could materially adversely affect business performance and financial results.

• **Revenue Concentration Risk** – Revenue is concentrated in a limited number of areas, particularly Bitcoin and Ethereum transactions and payment stablecoin revenue. Loss of demand in these concentrated segments without offsetting growth from new revenue sources could significantly impact overall financial performance.

• **Regulatory and Competitive Pressures** – The company faces ongoing regulatory enforcement actions, evolving legislative frameworks, and intense competition from other cryptocurrency platforms and traditional payment services. Changes in regulatory treatment of crypto assets or increased competitive pressure could adversely affect customer acquisition, retention, and profitability.

## Audited (Exec Summary + Outlook)

### Executive Summary
Coinbase is a leading cryptocurrency exchange and financial infrastructure platform, generating $6.0 billion in revenue while carrying a market capitalization of $47.1 billion — yet the company remains unprofitable, reporting a net loss of $987.8 million and a negative profit margin of -16.34%. The stock is notable now because it trades at a forward P/E of 62.9x, embedding substantial growth expectations into a valuation that must be reconciled with ongoing net losses, heightened regulatory capital requirements, and a 52-week price range of $139.11–$402.16 that reflects deep uncertainty about the company's trajectory. The single most important near-term variable is whether Coinbase can demonstrate a credible path to profitability while absorbing the operational and financial costs of intensifying regulatory compliance obligations.

### Outlook
The directional outlook for Coinbase is **cautious**, with the potential to turn more constructive if specific conditions materialize. On the tailwind side, broader institutional adoption of digital assets, favorable evolution of the legislative and regulatory framework, and growing stablecoin utilization could collectively expand Coinbase's addressable market and support the subscription and services revenue that is less dependent on trading volume swings. However, the headwinds are substantial and immediate: the company must close a wide profitability gap while simultaneously absorbing rising regulatory capital requirements across its custody and money-transmitting subsidiaries, and its revenue base remains heavily concentrated in Bitcoin and Ethereum transaction activity — segments that are inherently tied to unpredictable market sentiment. Investors should watch the trajectory of the profit margin as the clearest signal of operational progress, the pace and scope of regulatory capital demands from New York State and other jurisdictions as a constraint on financial flexibility, the trend in stablecoin adoption as a gauge of services-revenue durability, and any shifts in competitive intensity from rival platforms or traditional payment providers. The thesis would strengthen meaningfully if Coinbase demonstrates sustained margin improvement and achieves regulatory clarity that reduces compliance drag; it would weaken if crypto market conditions deteriorate, regulatory burdens escalate further, or revenue concentration in Bitcoin and Ethereum deepens without diversification into new growth areas.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

## EXECUTIVE SUMMARY

---

CLAIM: "$6.0 billion in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $6,043,752,960, which rounds to $6.0 billion; the pre-written Financial Health section also states "$6.0 billion in revenue."

---

CLAIM: "market capitalization of $47.1 billion"
LABEL: SUPPORTED
REASON: Source data shows market_cap of $47,081,697,280, which rounds to $47.1 billion; confirmed in the pre-written sections.

---

CLAIM: "net loss of $987.8 million"
LABEL: SUPPORTED
REASON: Source data shows net_income of -$987,766,016, which rounds to -$987.8 million; confirmed in the pre-written sections.

---

CLAIM: "negative profit margin of -16.34%"
LABEL: SUPPORTED
REASON: Source data explicitly states profit_margin_pct of -16.34%; arithmetic check: -987,766,016 / 6,043,752,960 = -16.34%. Confirmed.

---

CLAIM: "forward P/E of 62.9x"
LABEL: SUPPORTED
REASON: Source data explicitly states forward_pe of 62.903835, which rounds to 62.9x; confirmed in pre-written sections.

---

CLAIM: "52-week price range of $139.11–$402.16"
LABEL: SUPPORTED
REASON: Source data explicitly states week_52_low of $139.11 and week_52_high of $402.16; confirmed in pre-written Financial Health section.

---

## OUTLOOK

---

CLAIM: "approximately 45-46% of trading volume derived from Bitcoin and Ethereum transactions" (implied by "revenue base remains heavily concentrated in Bitcoin and Ethereum transaction activity")
LABEL: N/A — The Outlook section does not quote the 45–46% figure explicitly; it only makes a qualitative directional claim about concentration. No specific quantitative figure to audit here.

*(No quantitative figures are stated in the Outlook section beyond qualitative directional language referencing entities and conditions already audited above. The Outlook contains no new standalone numerical claims — no price targets, no specific thresholds, no ratios, no percentages, no named product milestones, and no forward-looking numbers beyond those already captured in the Executive Summary.)*

---

## SUMMARY TABLE

| Claim | Label |
|---|---|
| $6.0 billion in revenue | SUPPORTED |
| $47.1 billion market cap | SUPPORTED |
| Net loss of $987.8 million | SUPPORTED |
| Profit margin of -16.34% | SUPPORTED |
| Forward P/E of 62.9x | SUPPORTED |
| 52-week range $139.11–$402.16 | SUPPORTED |

**All auditable quantitative claims in the Executive Summary and Outlook are SUPPORTED by the source data. No unsupported or inference-only figures were identified.**
