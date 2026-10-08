# NTLA — baseline

## Metadata

ticker: NTLA
arm: baseline
judge_prompt_version: v2
context_sha256: 33b4d5934acb4efb7f29c9906f39b1032efb91ff490ddc98253db09179bbe0f0
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 359, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.538, "latency_s_total": 4.538, "parse_failure": 0, "prompt_tokens": 3360, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 358, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.549, "latency_s_total": 4.549, "parse_failure": 0, "prompt_tokens": 3237, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 175, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.104, "latency_s_total": 2.104, "parse_failure": 0, "prompt_tokens": 661, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 178, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.172, "latency_s_total": 2.172, "parse_failure": 0, "prompt_tokens": 654, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 206, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.274, "latency_s_total": 2.274, "parse_failure": 0, "prompt_tokens": 434, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 198, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.13, "latency_s_total": 2.13, "parse_failure": 0, "prompt_tokens": 443, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1356, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.552, "latency_s_total": 19.552, "parse_failure": 0, "prompt_tokens": 1924, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "NTLA",
  "company_name": "Intellia Therapeutics, Inc.",
  "current_price": 11.71,
  "currency": "USD",
  "market_cap": 1640883584.0,
  "forward_pe": -4.5617986,
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
[]

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
[From Pinecone cache] I can only provide information based on the context given, which contains excerpts from the Risk Factors section of a 10-K filing for the year ended December 31, 2025. The context does not include a 10-Q filing or comprehensive information about the company's financial performance, operations, or other key business developments.

Based on the available risk factors disclosure, the key takeaways are:

**Technology and Development Stage:**
- The company is developing CRISPR genome editing therapeutics, including both in vivo and ex vivo therapies
- In vivo CRISPR-based therapies remain largely unproven, with no in vivo genome editing therapy approved in the U.S., EU, or other major jurisdictions to date
- The company has two CRISPR-based therapies in clinical development: nexiguran ziclumeran (NTLA-2001) and lonvoguran ziclumeran (NTLA-2002)

**Significant Risks:**
- Unproven therapeutic approaches that may never lead to marketable products
- Regulatory uncertainty, as FDA and other agencies have limited experience with CRISPR-based therapeutics
- Clinical trial challenges including enrollment, safety concerns, and potential regulatory holds
- Physician and patient adoption risks due to the novel nature of the therapies
- Manufacturing, delivery, and scalability challenges

**Regulatory Status:**
- A clinical hold is pending resolution for the MAGNITUDE trial related to NTLA-2001

To obtain a complete summary of the latest 10-K and 10-Q filings, you would need to review the full documents.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors related to its CRISPR genome editing technology business:

## Technology and Development Risks
- CRISPR genome editing technology has only recently been clinically validated for human therapeutic use, and in vivo CRISPR-based technologies remain relatively new with largely unproven therapeutic utility
- The approaches for developing CRISPR-based therapeutics are unproven and may never lead to marketable products
- Successful development requires solving numerous technical challenges, including safe delivery of therapeutic agents to target cells, optimizing efficacy and specificity, and demonstrating safety and efficacy

## Regulatory and Approval Risks
- No genome editing in vivo therapy has been approved in the U.S., EU, or other key jurisdictions
- Clinical trials are lengthy, expensive, and uncertain in outcome
- Regulatory requirements for later-phase clinical trials are more stringent than earlier phases
- The company faces potential delays or inability to complete clinical trials and obtain regulatory approval

## Market Adoption Risks
- Public perception and media coverage of safety or efficacy issues may discourage clinical trial participation and physician/patient acceptance
- Physicians and healthcare providers are often slow to adopt new technologies and may view these therapies as too complex or risky
- Certain patients may not be candidates for the therapies due to health conditions or genetic profiles

## Regulatory and Legislative Risks
- Government responses to negative public perception or ethical concerns could result in new legislation or regulations that limit development, commercialization, or approval of product candidates
- Healthcare providers and payors may determine that benefits do not outweigh costs

## Pre-written sections (judge input)

### Financial Health

Intellia Therapeutics trades at $11.71 with a market capitalization of $1.64 billion, down significantly from its 52-week high of $28.25. The company is unprofitable with a net loss of $400 million against minimal revenue of $59.5 million, resulting in a negative profit margin typical of early-stage biotech firms. The forward P/E ratio is not meaningful given the negative earnings, reflecting the company's pre-commercial or early-revenue stage. As a clinical-stage gene-editing company, NTLA's financial viability depends on successful pipeline advancement and future commercialization rather than current profitability. Investors should view this as a high-risk, high-reward opportunity requiring patience for clinical and regulatory milestones.

### Recent Developments

Intellia Therapeutics filed its 2025 10-K in February 2026 and most recent 10-Q in August 2026, with both filings emphasizing significant risk factors inherent to the company's gene-editing business. The company continues to face substantial operational challenges, evidenced by a net loss of $400 million against minimal revenue of $59.5 million, indicating the pre-commercial or early-stage nature of its CRISPR-based therapeutics pipeline. With the stock trading at $11.71—down 59% from its 52-week high of $28.25—investors should monitor clinical trial progress and regulatory milestones closely, as the company's path to profitability remains uncertain and dependent on successful advancement of its gene-editing programs.

### SEC Filing Highlights

Intellia Therapeutics is advancing two CRISPR-based therapies in clinical development—nexiguran ziclumeran (NTLA-2001) and lonvoguran ziclumeran (NTLA-2002)—representing both in vivo and ex vivo genome editing approaches. However, the company faces significant regulatory uncertainty as no in vivo CRISPR genome editing therapy has been approved in the U.S., EU, or other major jurisdictions to date, and a clinical hold is pending resolution for the MAGNITUDE trial related to NTLA-2001. Key risks include unproven therapeutic approaches, manufacturing and delivery scalability challenges, and potential physician and patient adoption barriers given the novel nature of CRISPR-based treatments. The company's success depends on navigating regulatory pathways with limited FDA precedent and overcoming clinical trial enrollment and safety concerns.

### Risk Factors

• **Unproven Technology and Clinical Validation** – CRISPR in vivo genome editing remains relatively new with largely unproven therapeutic utility in humans. The company must overcome significant technical challenges including safe delivery to target cells, efficacy optimization, and safety demonstration, with no guarantee of successful product development.

• **Regulatory Approval Uncertainty** – No in vivo genome editing therapy has been approved in the U.S., EU, or other major jurisdictions. Clinical trials are lengthy, expensive, and uncertain; regulatory requirements become more stringent in later phases, creating risk of delays or failure to obtain approval.

• **Market Adoption and Public Perception Risks** – Negative media coverage of safety or efficacy issues could discourage trial participation and physician/patient acceptance. Healthcare providers may view the therapies as too complex or risky, and payors may determine benefits do not justify costs, limiting commercial viability even if approved.

## Audited (Exec Summary + Outlook)

### Executive Summary
Intellia Therapeutics is a clinical-stage gene-editing company developing CRISPR-based therapeutics, including two programs in active clinical development—nexiguran ziclumeran (NTLA-2001) and lonvoguran ziclumeran (NTLA-2002)—with a market capitalization of $1.64 billion supported by minimal revenue of $59.5 million against a net loss of $400 million. The stock is notable now precisely because of its dislocation—trading at $11.71, down 59% from its 52-week high of $28.25—reflecting deep investor skepticism about the company's ability to navigate an unprecedented regulatory landscape with no approved in vivo CRISPR therapy anywhere in the world as a comparable benchmark. The single most important near-term variable is the resolution of the clinical hold on the MAGNITUDE trial related to NTLA-2001, as the outcome will either restore confidence in the lead program or further compress the timeline to any potential commercialization.

### Outlook
The directional outlook for Intellia Therapeutics is **cautious**, with the balance of near-term risks outweighing near-term catalysts. The primary headwind is the unresolved clinical hold on the MAGNITUDE trial, which clouds visibility into the lead program and signals potential safety or procedural concerns that regulators must address before the company can advance. Compounding this, the absence of any approved in vivo CRISPR therapy globally means Intellia is navigating regulatory pathways without established precedent, making timelines inherently difficult to predict. On the tailwind side, the company's dual-modality pipeline—spanning both in vivo and ex vivo approaches—provides some diversification of clinical risk, and growing scientific and institutional interest in CRISPR-based medicine represents a longer-term structural tailwind for the field. Investors should monitor the following key variables: resolution and terms of the MAGNITUDE clinical hold, clinical data readouts from both NTLA-2001 and NTLA-2002, any FDA guidance or precedent-setting regulatory interactions that clarify the approval pathway for in vivo gene editing, and the company's cash runway given its substantial ongoing net losses. The cautious stance would shift toward constructive if the clinical hold is lifted cleanly, if clinical data demonstrate compelling efficacy and an acceptable safety profile, or if a regulatory agency provides meaningful pathway clarity; it would deepen further if the hold results in program termination, if safety signals emerge across the pipeline, or if the company faces financing pressure before reaching meaningful milestones.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative, forward-looking, and specific factual claim in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "two programs in active clinical development—nexiguran ziclumeran (NTLA-2001) and lonvoguran ziclumeran (NTLA-2002)"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "The company has two CRISPR-based therapies in clinical development: nexiguran ziclumeran (NTLA-2001) and lonvoguran ziclumeran (NTLA-2002)."

---

CLAIM: "a market capitalization of $1.64 billion"
LABEL: SUPPORTED
REASON: Source data shows market_cap = 1,640,883,584.0, which rounds to $1.64 billion.

---

CLAIM: "minimal revenue of $59.5 million"
LABEL: SUPPORTED
REASON: Source data shows revenue = 59,506,000.0, which rounds to $59.5 million.

---

CLAIM: "a net loss of $400 million"
LABEL: SUPPORTED
REASON: Source data shows net_income = -399,975,008.0, which rounds to -$400 million.

---

CLAIM: "trading at $11.71"
LABEL: SUPPORTED
REASON: Source data shows current_price = 11.71.

---

CLAIM: "down 59% from its 52-week high of $28.25"
LABEL: SUPPORTED
REASON: The 52-week high of $28.25 is present in source data. The decline is (28.25 − 11.71) / 28.25 = 16.54 / 28.25 ≈ 58.55%, which rounds to 59%; within 0.15 percentage points of the stated 59% (rounding 58.55% to 59% is standard). The pre-written Recent Developments section also states "down 59% from its 52-week high of $28.25," confirming the figure.

---

CLAIM: "no approved in vivo CRISPR therapy anywhere in the world as a comparable benchmark"
LABEL: SUPPORTED
REASON: RAG SEC Highlights states "no in vivo genome editing therapy approved in the U.S., EU, or other major jurisdictions to date," and the SEC Filing Highlights pre-written section corroborates this.

---

CLAIM: "The single most important near-term variable is the resolution of the clinical hold on the MAGNITUDE trial related to NTLA-2001"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "A clinical hold is pending resolution for the MAGNITUDE trial related to NTLA-2001," and the SEC Filing Highlights pre-written section repeats this fact.

---

**OUTLOOK**

---

CLAIM: "The primary headwind is the unresolved clinical hold on the MAGNITUDE trial"
LABEL: SUPPORTED
REASON: The clinical hold on the MAGNITUDE trial related to NTLA-2001 is explicitly documented in the RAG SEC Highlights and the SEC Filing Highlights pre-written section.

---

CLAIM: "the absence of any approved in vivo CRISPR therapy globally"
LABEL: SUPPORTED
REASON: RAG SEC Highlights and Risk Factors both confirm no in vivo genome editing therapy has been approved in the U.S., EU, or other major jurisdictions.

---

CLAIM: "the company's dual-modality pipeline—spanning both in vivo and ex vivo approaches"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights states the company is "developing CRISPR genome editing therapeutics, including both in vivo and ex vivo therapies," and the SEC Filing Highlights pre-written section references "both in vivo and ex vivo genome editing approaches."

---

CLAIM: "the company's cash runway given its substantial ongoing net losses"
LABEL: INFERENCE
REASON: The net loss of ~$400 million is present in the source data, supporting the characterization of "substantial ongoing net losses"; the reference to "cash runway" as a watch item is a standard inference from a large net loss at a pre-commercial company, though no specific cash balance or runway figure is cited or claimed.

---

CLAIM: "[cautious stance would shift] if the clinical hold is lifted cleanly, if clinical data demonstrate compelling efficacy and an acceptable safety profile, or if a regulatory agency provides meaningful pathway clarity"
LABEL: INFERENCE
REASON: These are forward-looking conditional scenarios derived directly from the documented clinical hold, unproven regulatory pathway, and clinical trial risks present in the source data; no specific thresholds or figures are asserted, making this a directional inference rather than an unsupported quantitative claim.

---

CLAIM: "[cautious stance would deepen] if the hold results in program termination, if safety signals emerge across the pipeline, or if the company faces financing pressure before reaching meaningful milestones"
LABEL: INFERENCE
REASON: These downside scenarios are logical extensions of the documented risks (clinical hold, unproven technology, pre-commercial losses) present in the source data; again, no specific figures or thresholds are asserted that could be checked against the data.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | Two named programs in active clinical development | SUPPORTED |
| 2 | Market cap $1.64 billion | SUPPORTED |
| 3 | Revenue $59.5 million | SUPPORTED |
| 4 | Net loss $400 million | SUPPORTED |
| 5 | Stock at $11.71 | SUPPORTED |
| 6 | Down 59% from 52-week high of $28.25 | SUPPORTED |
| 7 | No approved in vivo CRISPR therapy anywhere in the world | SUPPORTED |
| 8 | Clinical hold on MAGNITUDE trial (NTLA-2001) as key near-term variable | SUPPORTED |
| 9 | Unresolved clinical hold on MAGNITUDE trial as primary headwind | SUPPORTED |
| 10 | No approved in vivo CRISPR therapy globally | SUPPORTED |
| 11 | Dual-modality pipeline (in vivo and ex vivo) | SUPPORTED |
| 12 | Cash runway concern given substantial net losses | INFERENCE |
| 13 | Constructive shift conditions (hold lifted, data, regulatory clarity) | INFERENCE |
| 14 | Deepening caution conditions (termination, safety signals, financing pressure) | INFERENCE |

**No UNSUPPORTED claims were identified.** All quantitative figures checked arithmetically against source data. No period mismatches, absent entities, or failed ratio checks were found.
