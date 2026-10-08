# UPST — rerank3

## Metadata

ticker: UPST
arm: rerank3
judge_prompt_version: v2
context_sha256: e900d57bb54a25b7ee7291644ad1d0d9ea797526deae9a8497111945daadfec7
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 216, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 3.119, "latency_s_total": 3.119, "parse_failure": 0, "prompt_tokens": 3199, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 364, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.344, "latency_s_total": 4.344, "parse_failure": 0, "prompt_tokens": 2482, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 160, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.968, "latency_s_total": 1.968, "parse_failure": 0, "prompt_tokens": 676, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 158, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.064, "latency_s_total": 2.064, "parse_failure": 0, "prompt_tokens": 669, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 203, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.542, "latency_s_total": 2.542, "parse_failure": 0, "prompt_tokens": 438, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 115, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.657, "latency_s_total": 1.657, "parse_failure": 0, "prompt_tokens": 298, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1167, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 18.17, "latency_s_total": 18.17, "parse_failure": 0, "prompt_tokens": 1678, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "UPST",
  "company_name": "Upstart Holdings, Inc.",
  "current_price": 24.02,
  "currency": "USD",
  "market_cap": 2337459456.0,
  "pe_ratio": 48.04,
  "forward_pe": 6.910321,
  "week_52_high": 55.22,
  "week_52_low": 22.555,
  "financial_currency": "USD",
  "revenue": 1285890048.0,
  "net_income": 60334000.0,
  "profit_margin_pct": 4.69,
  "dividend_yield": 0.0,
  "sector": "Financial Services",
  "industry": "Credit Services"
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
    "filing_date": "2026-02-10",
    "summary": "ITEM 1A. RISK FACTORS RISK FACTORS Investing in our common stock involves a high degree of risk. The risks and uncertainties described below should be carefully considered, together with all of the other information in this Annual Report on Form 10-K, including the section titled \u201cManagement\u2019s Discussion and Analysis of Financial Condition and Results of Operations\u201d and our consolidated financial statements and related notes, before making a decision to invest in our common stock. Our business, financial condition, results of operations, or prospects could also be harmed by risks and uncertainties not currently known to us or that we currently do not believe are material. If any of the risks actually occur, our business, financial condition, results of operations, and prospects could be ad"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-04",
    "summary": "ITEM 1A. RISK FACTORS RISK FACTORS Investing in our common stock involves a high degree of risk. The risks and uncertainties described below should be carefully considered, together with all of the other information in this Quarterly Report on Form 10-Q, including the section titled \u201cManagement\u2019s Discussion and Analysis of Financial Condition and Results of Operations\u201d and our condensed consolidated financial statements and related notes, before making a decision to invest in our common stock. Our business, financial condition, results of operations, or prospects could also be harmed by risks and uncertainties not currently known to us or that we currently do not believe are material. If any of the risks actually occur, our business, financial condition, results of operations, and prospect"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] I cannot provide a summary of the latest 10-K and 10-Q based on the information provided. The context materials only contain excerpts from the Risk Factors section of a 10-K filing for Upstart (ticker: UPST), specifically focusing on business and industry risks, funding and capital arrangement risks, and securitization-related risks.

To provide a comprehensive summary of the latest 10-K and 10-Q filings, I would need access to additional sections such as:

- Management's Discussion and Analysis (MD&A)
- Financial statements and results of operations
- Business overview and strategy
- Liquidity and capital resources
- Results from the 10-Q (quarterly report)

The excerpts provided only highlight the company's identified risk factors, which represent just one component of these regulatory filings. A complete summary would require reviewing the full documents to capture the company's financial performance, operational results, strategic initiatives, and other material information beyond the risk disclosures.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors affecting its business:

## Economic and Market Risks
- Adverse economic conditions, uncertainty, and volatility that reduce borrower demand, approval rates, and loan origination volume
- Impact on capital supply from lending partners and institutional investors
- Effects on borrowers with poor, limited, or no credit history who are disproportionately affected by inflation, higher interest rates, and unemployment

## Capital and Funding Risks
- Inability to maintain diverse and resilient loan funding from institutional investors
- Risks associated with committed capital and co-investment arrangements where the company may need to compensate investors if loan performance deviates from expectations
- Dependence on securitizations, warehouse facilities, and risk retention financing arrangements
- Counterparty risk from derivative instruments and custodial arrangements

## Operational and Technology Risks
- Ineffectiveness of artificial intelligence models in accurately reflecting changes in economic conditions and borrower credit risk
- Significant disruptions or failures in technology systems, including the AI lending platform
- Inability to approve a significant number of borrowers for loans

## Business Model Risks
- Concentration of business with a limited number of lending partners
- Dependence on a single loan product historically
- Reliance on strategic relationships with loan aggregators
- Inability to manage risks associated with loan servicing and collections obligations

## Regulatory and Reputational Risks
- Compliance with a wide range of evolving laws and regulations
- Security breaches and improper access to data
- Reputation and brand protection challenges
- Representation and warranty obligations related to securitizations and loan sales

## Pre-written sections (judge input)

### Financial Health

Upstart Holdings trades at $24.02 with a market capitalization of $2.34 billion, currently trading near its 52-week low of $22.56. The company generated $1.29 billion in revenue with a modest 4.69% profit margin and net income of $60.3 million, indicating operational profitability but thin margins typical of credit services. The elevated trailing P/E ratio of 48.04 contrasts sharply with a forward P/E of 6.91, suggesting market expectations for significant earnings growth ahead. The stock offers no dividend yield, with capital appreciation as the primary return mechanism. Recent SEC filings highlight substantial business risks that warrant careful consideration before investment.

### Recent Developments

Limited recent news is available for analysis at this time. However, Upstart's most recent SEC filings (10-Q filed August 4, 2026 and 10-K filed February 10, 2026) emphasize significant risk factors affecting the business, suggesting investors should carefully review operational challenges and market uncertainties. The company's valuation metrics show a stark contrast—trading at a 48x trailing P/E while maintaining a forward P/E of just 6.9x—indicating market expectations for substantial earnings growth or potential near-term headwinds. With a modest 4.69% profit margin and no dividend, investors are betting on future profitability rather than current income generation.

### SEC Filing Highlights

Based on available information, Upstart's recent SEC filings emphasize significant risk factors across its business operations, including dependence on AI model performance, regulatory uncertainties in lending, and exposure to securitization market volatility. The company faces material risks related to funding availability, capital arrangement constraints, and potential disruptions in its ability to monetize loans through secondary market sales. Without access to complete MD&A sections and financial statements, a comprehensive assessment of recent operational performance and strategic initiatives cannot be provided at this time.

### Risk Factors

• **Economic Sensitivity and Credit Risk**: Adverse economic conditions, rising interest rates, and unemployment disproportionately impact Upstart's borrower base, particularly those with limited credit history. Economic downturns reduce loan origination volume, approval rates, and institutional investor capital supply, directly affecting revenue and profitability.

• **AI Model Effectiveness and Technology Dependence**: The company's core lending platform relies on artificial intelligence models that may fail to accurately predict borrower credit risk amid changing economic conditions. Significant technology disruptions or system failures could impair loan approvals and damage the business model.

• **Funding and Capital Structure Risk**: Upstart depends on diverse institutional investors and securitization markets to fund loan originations. Inability to maintain stable funding relationships, combined with co-investment obligations and representation/warranty liabilities on sold loans, creates exposure to capital constraints and potential financial losses if loan performance deteriorates.

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings is an AI-driven lending marketplace that connects borrowers — particularly those with limited traditional credit history — to institutional capital partners, generating $1.29 billion in revenue and $60.3 million in net income while operating at thin 4.69% profit margins characteristic of the credit services sector. The stock is notable now because it trades near its 52-week low of $22.56 at a price of $24.02, yet the dramatic compression between a trailing P/E of 48.04 and a forward P/E of 6.91 signals that the market is pricing in a substantial earnings inflection — making this a high-conviction bet on future profitability rather than a reward for current performance. The single most important near-term variable is whether Upstart's AI credit models can sustain or improve predictive accuracy in a shifting macroeconomic environment, as model effectiveness directly determines loan approval rates, institutional investor confidence, and the company's ability to grow origination volume.

### Outlook
The directional lean on Upstart is **cautiously constructive, with meaningful conditions attached**. The primary tailwind is the implied earnings inflection embedded in the forward valuation, which suggests that if Upstart's AI models continue to perform and macroeconomic conditions stabilize or improve, the company could see a significant expansion in origination volume, institutional funding appetite, and ultimately profit margins. Key variables to monitor include the trajectory of interest rates and their effect on borrower demand and securitization market health, the stability and breadth of Upstart's institutional funding relationships, and any regulatory developments affecting AI-driven lending practices. The thesis would strengthen if the company demonstrates consistent improvement in loan performance data, successfully broadens its capital partner base, and shows operating leverage translating into meaningfully higher margins. Conversely, the view would turn more cautious if macroeconomic deterioration — particularly rising unemployment — pressures borrower credit quality, if AI model accuracy is called into question by rising default rates, or if securitization market access tightens and constrains the company's ability to move loans off its balance sheet. Given the thin current margins and the stock's proximity to its 52-week low, the risk/reward is asymmetric but the outcome is highly sensitive to variables largely outside management's direct control.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative, positional, and forward-looking claim in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "generating $1.29 billion in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $1,285,890,048, which rounds to $1.29 billion as stated in the pre-written Financial Health section.

---

CLAIM: "$60.3 million in net income"
LABEL: SUPPORTED
REASON: Source data shows net income of $60,334,000, which rounds to $60.3 million, consistent with the pre-written Financial Health section.

---

CLAIM: "thin 4.69% profit margins"
LABEL: SUPPORTED
REASON: Source data explicitly lists profit_margin_pct as 4.69, matching the claim exactly.

---

CLAIM: "trades near its 52-week low of $22.56"
LABEL: SUPPORTED
REASON: Source data shows week_52_low of $22.555, which rounds to $22.56; current price is $24.02, which is approximately 6.5% above the 52-week low — arithmetically "near" the low is supported. The $22.56 figure is accurate.

---

CLAIM: "at a price of $24.02"
LABEL: SUPPORTED
REASON: Source data explicitly lists current_price as 24.02.

---

CLAIM: "trailing P/E of 48.04"
LABEL: SUPPORTED
REASON: Source data explicitly lists pe_ratio as 48.04.

---

CLAIM: "forward P/E of 6.91"
LABEL: SUPPORTED
REASON: Source data lists forward_pe as 6.910321, which rounds to 6.91.

---

CLAIM: "the market is pricing in a substantial earnings inflection"
LABEL: INFERENCE
REASON: This is a directional interpretation derived directly from the contrast between the trailing P/E of 48.04 and the forward P/E of 6.91, both present in the source data — the compression implies market expectation of significantly higher future earnings.

---

**OUTLOOK**

---

CLAIM: "the implied earnings inflection embedded in the forward valuation"
LABEL: INFERENCE
REASON: Derived from the contrast between the trailing P/E of 48.04 and forward P/E of 6.91, both present in the source data, making this a direct restatement of the same inference as above.

---

CLAIM: "the stock's proximity to its 52-week low"
LABEL: SUPPORTED
REASON: Current price of $24.02 versus 52-week low of $22.555 represents a gap of approximately $1.47 (roughly 6.5% above the low), and the 52-week high is $55.22; arithmetically the stock is far closer to its low than its high, confirming the positional claim.

---

CLAIM: "thin current margins"
LABEL: SUPPORTED
REASON: Source data confirms profit_margin_pct of 4.69%, which is explicitly described as thin in the pre-written sections and is objectively a low margin figure for the sector.

---

*No additional specific quantitative figures, named price targets, thresholds, ratios, percentages, named product milestones, or other forward-looking numbers appear in the Outlook section beyond those already audited above. All remaining Outlook language is qualitative and directional (e.g., "cautiously constructive," "key variables to monitor," "thesis would strengthen/turn more cautious") and does not constitute auditable quantitative claims.*
