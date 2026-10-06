# NTLA — baseline

## Metadata

ticker: NTLA
arm: baseline
judge_prompt_version: v2
context_sha256: 22583f05be11819d52a7495e010031718a2f42375e8619bbdc13f5387d7ffbc8
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 215, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.725, "latency_s_total": 2.725, "parse_failure": 0, "prompt_tokens": 3360, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 356, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.4, "latency_s_total": 4.4, "parse_failure": 0, "prompt_tokens": 3237, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 172, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.905, "latency_s_total": 1.905, "parse_failure": 0, "prompt_tokens": 684, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 163, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.967, "latency_s_total": 1.967, "parse_failure": 0, "prompt_tokens": 677, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 208, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.449, "latency_s_total": 2.449, "parse_failure": 0, "prompt_tokens": 432, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 158, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.901, "latency_s_total": 1.901, "parse_failure": 0, "prompt_tokens": 299, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1214, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 18.026, "latency_s_total": 18.026, "parse_failure": 0, "prompt_tokens": 1812, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "NTLA",
  "company_name": "Intellia Therapeutics, Inc.",
  "current_price": 12.75,
  "currency": "USD",
  "market_cap": 1786615296.0,
  "forward_pe": -4.9056764,
  "week_52_high": 28.25,
  "week_52_low": 7.95,
  "financial_currency": "USD",
  "revenue": 59506000.0,
  "net_income": -399975008.0,
  "profit_margin_pct": 0.0,
  "dividend_yield": 0.0,
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
    "filing_date": "2026-02-26",
    "summary": "Item 1A. Risk Factors Investing in our common stock involves a high degree of risk. In evaluating us and our business, careful consideration should be given to the following risk factors, in addition to the other information set forth in this Annual Report on Form 10-K for the year ended December 31, 2025 and in other documents that we file with the Securities and Exchange Commission (\u201cSEC\u201d). If any of the following risks and uncertainties actually occurs, our business, prospects, financial condition and results of operations could be materially and adversely affected. The risks described below are not intended to be exhaustive and are not the only risks facing us. New risk factors can emerge from time to time, and we cannot predict the impact that any factor or combination of factors may "
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-06",
    "summary": "Item 1A. Risk Factors Investing in our common stock involves a high degree of risk. In evaluating us and our business, careful consideration should be given to the following risk factors, in addition to the other information set forth in this Quarterly Report on Form 10-Q, our Annual Report on Form 10-K for the year ended December 31, 2025, and in other documents that we file with the Securities and Exchange Commission (\u201cSEC\u201d). If any of the following risks and uncertainties actually occurs, our business, prospects, financial condition and results of operations could be materially and adversely affected. The risks described below are not intended to be exhaustive and are not the only risks facing us. New risk factors can emerge from time to time, and we cannot predict the impact that any f"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] I cannot provide a summary of the latest 10-K and 10-Q based on the information provided. The context materials only contain excerpts from the Risk Factors section (Item 1A) of a 10-K filing for the year ended December 31, 2025, specifically focusing on risks related to preclinical and clinical development of CRISPR-based therapeutics.

To provide a comprehensive summary of the latest 10-K and 10-Q filings, I would need access to additional sections such as:

- Management's Discussion and Analysis (MD&A)
- Financial statements and results of operations
- Business overview and strategy
- Liquidity and capital resources
- Recent developments and milestones
- Other material business information

The excerpts provided only address the company's risk factors related to CRISPR genome editing technology development, regulatory challenges, clinical trial uncertainties, and market adoption concerns—which represent just one portion of a complete 10-K filing.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors related to its CRISPR genome editing technology business:

## Technology and Development Risks
- CRISPR genome editing technology has only recently been clinically validated for human therapeutic use, and in vivo CRISPR-based technologies remain relatively new with largely unproven therapeutic utility
- The approaches being pursued are unproven and may never lead to marketable products
- Successful development requires solving numerous technical challenges, including safe delivery of therapeutic agents to target cells, optimizing efficacy and specificity, and demonstrating safety and effectiveness

## Regulatory and Approval Risks
- No genome editing in vivo therapy has been approved in the U.S., EU, or other key jurisdictions
- Obtaining regulatory approval for CRISPR product candidates remains uncertain
- Clinical trials are lengthy, expensive, and uncertain in outcome
- Regulatory requirements for later-phase clinical trials are more stringent than earlier phases
- The company faces potential delays or inability to complete clinical trials and obtain marketing approval

## Market Adoption Risks
- Public perception and media coverage of safety or efficacy issues may negatively influence clinical trial participation and physician/patient acceptance
- Physicians and healthcare providers are often slow to adopt new technologies and may view these therapies as too complex or risky
- Third-party payors may determine that benefits do not outweigh costs
- Ethical concerns related to genome editing may adversely affect commercialization

## Profitability Risk
- If the company cannot develop viable product candidates, achieve regulatory approval, or successfully market products, it may never achieve profitability

## Pre-written sections (judge input)

### Financial Health

Intellia Therapeutics trades at $12.75 with a market capitalization of $1.79 billion, down significantly from its 52-week high of $28.25. The company is unprofitable with a negative net income of $400 million against revenue of $59.5 million, reflecting typical early-stage biotech economics with a -4.91 forward P/E ratio. The substantial operating losses and lack of profitability indicate NTLA is in a pre-commercial or early commercialization phase, relying on R&D investments in gene-editing therapies rather than near-term earnings. Investors should view this as a high-risk, long-term development story dependent on pipeline success and future cash runway rather than current financial performance.

### Recent Developments

Intellia Therapeutics filed its most recent 10-Q on August 6, 2026, continuing to highlight significant risk factors inherent to its gene-editing biotechnology platform. The company remains in a pre-commercial or early-stage revenue phase, with $59.5 million in annual revenue against a net loss of $400 million, reflecting the substantial R&D investments typical of clinical-stage biotech firms. With a stock price of $12.75 (down 55% from its 52-week high of $28.25), investors should monitor upcoming clinical trial results and regulatory milestones that could validate Intellia's CRISPR-based therapeutic candidates and justify the company's current valuation.

### SEC Filing Highlights

Based on available information, Intellia Therapeutics' recent 10-K filing emphasizes significant risks inherent to its CRISPR-based therapeutic development pipeline, including preclinical and clinical development uncertainties, regulatory approval challenges, and potential market adoption obstacles. The company's disclosures highlight the inherent unpredictability of advancing novel genome editing therapies through clinical trials and the substantial capital requirements to support ongoing R&D efforts. Key risk factors underscore the competitive landscape in CRISPR therapeutics and the dependency on successful clinical validation of its pipeline candidates. A comprehensive analysis of financial performance, liquidity position, and operational milestones would require access to additional filing sections beyond the risk factors disclosed.

### Risk Factors

- **Unproven Technology & Development Challenges**: In vivo CRISPR-based therapies remain largely unproven with uncertain therapeutic utility. The company must overcome significant technical hurdles including safe delivery to target cells, optimizing efficacy/specificity, and demonstrating safety—with no guarantee of success.

- **Regulatory Uncertainty & No Approved Precedent**: No genome editing in vivo therapy has been approved in the U.S. or EU. Obtaining regulatory approval is uncertain and requires lengthy, expensive clinical trials with increasingly stringent requirements in later phases, creating risk of delays or failure to achieve approval.

- **Market Adoption & Reimbursement Risk**: Physician adoption of complex new genome editing therapies may be slow, public perception concerns could impact trial enrollment, and third-party payors may determine costs outweigh benefits. Ethical concerns around genome editing could further hinder commercialization and revenue generation.

## Audited (Exec Summary + Outlook)

### Executive Summary
Intellia Therapeutics is a clinical-stage biotechnology company developing CRISPR-based in vivo gene-editing therapies, operating with $59.5 million in revenue and a market capitalization of $1.79 billion as it pursues a potentially transformative but largely unproven therapeutic modality. The stock is notable now precisely because of its sharp decline — trading at $12.75, down 55% from its 52-week high of $28.25 — reflecting the market's growing impatience with the long and capital-intensive path from clinical-stage science to commercial reality. The single most important near-term variable is the outcome of upcoming clinical trial readouts, which will either validate Intellia's CRISPR platform and restore investor confidence or further pressure a company already absorbing a net loss of $400 million annually.

### Outlook
The directional outlook for Intellia Therapeutics is **cautious**, with the investment thesis hinging almost entirely on binary clinical and regulatory events rather than near-term financial improvement. The primary tailwind is the transformative potential of in vivo CRISPR gene editing as a therapeutic modality — if validated, it could open large and durable markets with limited existing competition. However, headwinds are substantial and structural: the company carries a heavy annual net loss, operates in a regulatory environment with no approved in vivo genome editing precedent in the U.S. or EU, and faces meaningful risks around physician adoption, public perception, and payor reimbursement. Investors should closely watch clinical trial data readouts for signs of efficacy and safety, regulatory interactions that signal the FDA's or EMA's evolving posture toward CRISPR-based therapies, the company's cash runway and any financing activity that could signal dilution risk, and the competitive landscape as other CRISPR-focused firms advance their own pipelines. The thesis would strengthen meaningfully on positive late-stage clinical data, a regulatory breakthrough designation, or a partnership that validates the platform and reduces cash burn. Conversely, clinical setbacks, safety signals, or an adverse regulatory signal would likely weaken the thesis further and raise serious questions about the company's path to commercialization.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$59.5 million in revenue"
LABEL: SUPPORTED
REASON: The raw source data lists revenue of $59,506,000, which rounds to $59.5 million, and the same figure appears in the pre-written sections.

---

CLAIM: "market capitalization of $1.79 billion"
LABEL: SUPPORTED
REASON: The raw source data lists market_cap of $1,786,615,296, which rounds to $1.79 billion, consistent with the pre-written Financial Health section.

---

CLAIM: "trading at $12.75"
LABEL: SUPPORTED
REASON: The raw source data explicitly lists current_price as $12.75.

---

CLAIM: "down 55% from its 52-week high of $28.25"
LABEL: SUPPORTED
REASON: The 52-week high of $28.25 is present in the source data; the percentage decline computes as (28.25 − 12.75) / 28.25 = 15.50 / 28.25 ≈ 54.87%, which rounds to 55% — within 0.15 percentage points of the stated figure.

---

CLAIM: "net loss of $400 million annually"
LABEL: SUPPORTED
REASON: The raw source data lists net_income of −$399,975,008, which rounds to −$400 million, and the pre-written sections confirm this figure.

---

**OUTLOOK**

---

CLAIM: "no approved in vivo genome editing precedent in the U.S. or EU"
LABEL: SUPPORTED
REASON: The RAG Risk Factors section explicitly states "No genome editing in vivo therapy has been approved in the U.S., EU, or other key jurisdictions," and this is echoed in the pre-written SEC Filing Highlights and Risk Factors sections.

---

*No additional specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section beyond the qualitative directional statements and the one factual regulatory claim evaluated above.*
