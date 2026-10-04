# UPST — baseline

## Metadata

ticker: UPST
arm: baseline
judge_prompt_version: v2
context_sha256: b520b079007ef79b88869d056f420e4a90dc705a4a62d40a9803ba6226000f8c
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 207, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.868, "latency_s_total": 2.868, "parse_failure": 0, "prompt_tokens": 3199, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 358, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.153, "latency_s_total": 4.153, "parse_failure": 0, "prompt_tokens": 2482, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 172, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.209, "latency_s_total": 2.209, "parse_failure": 0, "prompt_tokens": 658, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 156, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.989, "latency_s_total": 1.989, "parse_failure": 0, "prompt_tokens": 651, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 181, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.49, "latency_s_total": 2.49, "parse_failure": 0, "prompt_tokens": 432, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 112, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.575, "latency_s_total": 1.575, "parse_failure": 0, "prompt_tokens": 289, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1147, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 18.098, "latency_s_total": 18.098, "parse_failure": 0, "prompt_tokens": 1648, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "UPST",
  "company_name": "Upstart Holdings, Inc.",
  "current_price": 22.81,
  "currency": "USD",
  "market_cap": 2219710464.0,
  "pe_ratio": 43.865387,
  "forward_pe": 6.562216,
  "week_52_high": 55.22,
  "week_52_low": 22.555,
  "revenue": 1285890048.0,
  "net_income": 60334000.0,
  "profit_margin": 0.046919998,
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
[From Pinecone cache] I cannot provide a summary of the latest 10-K and 10-Q based on the information provided. The context materials only contain excerpts from the Risk Factors section of a 10-K filing for Upstart (UPST), specifically focusing on business and industry risks, funding and financing risks, and operational challenges.

To provide a comprehensive summary of the latest 10-K and 10-Q filings, I would need access to additional sections such as:

- Management's Discussion and Analysis (MD&A)
- Financial statements and results of operations
- Business overview and strategy
- Liquidity and capital resources
- Results for the specific periods covered

The excerpts provided only highlight potential risks and challenges the company faces, which represent just one component of a complete 10-K filing. A full summary would require reviewing the complete documents to capture the company's financial performance, operational results, strategic initiatives, and overall financial condition for the periods in question.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors affecting its business:

## Economic and Market Risks
- Adverse economic conditions, uncertainty, and volatility that impact borrower demand, approval rates, loan origination volume, and capital availability
- Macroeconomic factors affecting borrowers' ability and willingness to repay loans, particularly those with poor or limited credit history who are disproportionately affected by inflation, interest rates, and unemployment

## Capital and Funding Risks
- Inability to maintain diverse and resilient loan funding from institutional investors
- Dependence on committed capital and co-investment arrangements that expose the company to credit risk compensation obligations
- Risks associated with asset-backed securitizations, warehouse credit facilities, and whole loan sale arrangements, including representation and warranty obligations
- Counterparty risk from derivative instruments and custodial arrangements

## Operational and Technology Risks
- Inability to improve or maintain effective AI models for accurate credit risk assessment
- Significant disruption or failure in technology systems, including the AI lending platform
- Inability to approve sufficient borrowers for loans

## Business Model Risks
- Dependence on a limited number of lending partners for a significant portion of loan originations and revenue
- Concentration in U.S. consumer credit markets
- Reliance on strategic relationships with loan aggregators
- Historical net losses and inability to sustain profitability

## Regulatory and Reputational Risks
- Compliance with evolving laws and regulations
- Risks related to loan servicing and collections obligations
- Security breaches and data protection concerns
- Brand and reputation management

## Pre-written sections (judge input)

### Financial Health

Upstart Holdings trades at $22.81 with a market capitalization of $2.22 billion, currently near its 52-week low of $22.56. The company's trailing P/E ratio of 43.87 appears elevated relative to its modest 4.7% profit margin, though the forward P/E of 6.56 suggests significant earnings growth expectations. With $1.29 billion in annual revenue and $60.3 million in net income, Upstart demonstrates profitability but faces valuation concerns given its compressed margins and recent stock performance. The substantial gap between trailing and forward multiples indicates the market is pricing in substantial future earnings expansion, which carries execution risk. SEC filings highlight material business risks that warrant careful consideration before investment.

### Recent Developments

No recent news items are currently available for analysis. However, Upstart's latest SEC filings (10-K filed February 2026 and 10-Q filed August 2026) emphasize significant risk factors affecting the business, suggesting investors should carefully review regulatory disclosures. The company's stock has declined substantially from its 52-week high of $55.22 to $22.81, reflecting market concerns about the credit services sector and Upstart's operational challenges. With a forward P/E of 6.56 versus a trailing P/E of 43.87, the valuation suggests the market expects meaningful earnings growth, though this remains contingent on execution and market conditions.

### SEC Filing Highlights

Unable to provide SEC filing highlights at this time. The available source materials contain only risk factor disclosures from Upstart's 10-K filing and lack critical sections necessary for a comprehensive summary, including Management's Discussion and Analysis (MD&A), financial statements, results of operations, and business performance metrics. To generate accurate takeaways on financial performance, revenue trends, profitability, and strategic initiatives, access to complete 10-K and 10-Q filings would be required.

### Risk Factors

• **Economic Sensitivity and Credit Risk** – Adverse macroeconomic conditions, rising interest rates, and unemployment disproportionately impact borrowers' ability to repay, particularly Upstart's target demographic with limited credit history. Loan origination volume and approval rates are highly vulnerable to economic downturns.

• **Funding and Capital Dependence** – The company relies on institutional investors and co-investment arrangements to fund loans. Inability to maintain diverse funding sources or disruptions in capital availability could severely constrain loan originations and revenue growth.

• **AI Model Performance and Technology Risk** – Upstart's competitive advantage depends on its AI credit assessment models. Degradation in model accuracy, technology system failures, or inability to improve model performance could undermine loan approval rates and investor confidence in the platform.

## Audited (Exec Summary + Outlook)

### Executive Summary
Upstart Holdings is an AI-driven lending marketplace generating $1.29 billion in annual revenue by using machine learning models to assess credit risk for borrowers who are underserved by traditional scoring methods, positioning it at the intersection of fintech and consumer credit. The stock is notable now because it trades near its 52-week low of $22.56 — down sharply from a 52-week high of $55.22 — while simultaneously carrying a forward P/E of 6.56 that implies the market expects a dramatic acceleration in earnings relative to the trailing P/E of 43.87, creating a high-stakes divergence between current distress and embedded recovery expectations. The single most important near-term variable is whether Upstart's AI credit models can sustain loan performance well enough to retain and expand institutional funding relationships, as that funding access is the operational lifeline that determines whether the earnings recovery the market is pricing actually materializes.

### Outlook
The directional outlook for Upstart is **cautious, with a conditional path to constructive**. On the tailwind side, the wide gap between trailing and forward valuation multiples suggests the market has already discounted a great deal of bad news, and any stabilization in the interest rate environment or improvement in consumer credit conditions could meaningfully re-accelerate loan origination volumes and margin expansion. On the headwind side, the company's compressed profit margin, heavy dependence on institutional capital partners, and sensitivity to macroeconomic deterioration leave little room for operational missteps. Investors should monitor three key variables: the trajectory of the broader interest rate environment and its effect on borrower demand and loan performance; the stability and diversification of Upstart's institutional funding relationships, which are the direct lever on origination capacity; and the demonstrated accuracy of its AI credit models over time, since any erosion in model performance would simultaneously damage lender confidence and competitive differentiation. The thesis would strengthen if Upstart shows consistent improvement in net income and profit margins alongside growing origination volumes, and if funding partners deepen their commitments — signaling confidence in model reliability. The thesis would weaken if macroeconomic conditions deteriorate, funding sources contract, or regulatory scrutiny of AI-based lending practices intensifies in ways that constrain the platform's operating model.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$1.29 billion in annual revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue of $1,285,890,048, which rounds to $1.29 billion; the pre-written Financial Health section also states "$1.29 billion in annual revenue."

---

CLAIM: "52-week low of $22.56"
LABEL: SUPPORTED
REASON: Source data lists week_52_low as $22.555, which rounds to $22.56; the pre-written sections also state this figure.

---

CLAIM: "52-week high of $55.22"
LABEL: SUPPORTED
REASON: Source data explicitly lists week_52_high as $55.22; confirmed in pre-written Recent Developments section.

---

CLAIM: "forward P/E of 6.56"
LABEL: SUPPORTED
REASON: Source data lists forward_pe as 6.562216, which rounds to 6.56; confirmed in pre-written sections.

---

CLAIM: "trailing P/E of 43.87"
LABEL: SUPPORTED
REASON: Source data lists pe_ratio as 43.865387, which rounds to 43.87; confirmed in pre-written Financial Health section.

---

**OUTLOOK**

---

CLAIM: (No specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section.)
LABEL: N/A
REASON: The Outlook section is entirely qualitative and directional — it references the "wide gap between trailing and forward valuation multiples" and "compressed profit margin" without restating any specific numbers, so there are no additional quantitative claims to audit beyond those already covered in the Executive Summary.

---

**SUMMARY TABLE**

| Claim | Label |
|---|---|
| $1.29 billion in annual revenue | SUPPORTED |
| 52-week low of $22.56 | SUPPORTED |
| 52-week high of $55.22 | SUPPORTED |
| Forward P/E of 6.56 | SUPPORTED |
| Trailing P/E of 43.87 | SUPPORTED |

All five quantitative claims in the audited sections are supported by the raw source data. No unsupported or inference-labeled claims were identified. Notably, the brief does not introduce any figures (e.g., specific profit margin percentages, market cap figures, net income figures, or price targets) in the Executive Summary or Outlook that would require additional checks — those figures appear only in the pre-written Financial Health section, which is outside the audit scope.
