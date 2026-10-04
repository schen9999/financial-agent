# NTLA — baseline

## Metadata

ticker: NTLA
arm: baseline
judge_prompt_version: v2
context_sha256: f84f30a09f1e1fbfaac3eef1dbe992674373fb2bdff0cab01b4dbddcee78cf57
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 351, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.746, "latency_s_total": 4.746, "parse_failure": 0, "prompt_tokens": 3360, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 344, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.664, "latency_s_total": 4.664, "parse_failure": 0, "prompt_tokens": 3237, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 170, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.139, "latency_s_total": 2.139, "parse_failure": 0, "prompt_tokens": 663, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 182, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.174, "latency_s_total": 2.174, "parse_failure": 0, "prompt_tokens": 656, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 199, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.405, "latency_s_total": 2.405, "parse_failure": 0, "prompt_tokens": 420, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 189, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.184, "latency_s_total": 2.184, "parse_failure": 0, "prompt_tokens": 435, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1330, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.672, "latency_s_total": 19.672, "parse_failure": 0, "prompt_tokens": 1890, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "NTLA",
  "company_name": "Intellia Therapeutics, Inc.",
  "current_price": 12.26,
  "currency": "USD",
  "market_cap": 1717953280.0,
  "forward_pe": -4.7171445,
  "week_52_high": 28.25,
  "week_52_low": 7.95,
  "revenue": 59506000.0,
  "net_income": -399975008.0,
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
[From Pinecone cache] I can only provide information based on the context given, which contains excerpts from a 10-K filing for the year ended December 31, 2025. The context does not include a 10-Q filing, so I cannot summarize both documents.

Based on the 10-K excerpts provided, the key takeaways are:

**Business Focus and Technology:**
- The company is developing CRISPR genome editing-based therapeutics, including both in vivo and ex vivo therapies
- Current clinical-stage programs include nexiguran ziclumeran (NTLA-2001) and lonvoguran ziclumeran (NTLA-2002)

**Significant Risk Factors:**
- CRISPR in vivo therapies remain largely unproven with no approved in vivo genome editing therapies in the U.S., EU, or other major jurisdictions
- The company faces substantial challenges in solving critical issues including safe delivery of therapeutic agents, optimizing efficacy and specificity, and demonstrating safety and efficacy
- Clinical development faces regulatory hurdles, as agencies have limited experience with CRISPR-based therapeutics
- Physician and patient adoption of these novel therapies may be slow due to complexity, training requirements, and safety concerns
- Public perception and ethical concerns about genome editing could impact clinical trial enrollment and market acceptance

**Development Challenges:**
- Numerous potential delays and obstacles exist in preclinical studies and clinical trials
- Manufacturing, supply chain, and scaling challenges are anticipated
- There is no guarantee that success with one CRISPR product will translate to others

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors related to its business:

## Technology and Development Risks
- CRISPR genome editing technology has only recently been clinically validated for human therapeutic use, and in vivo CRISPR-based technologies remain relatively new with largely unproven therapeutic utility
- The approaches for developing CRISPR-based therapeutics are unproven and may never lead to marketable products
- No genome editing in vivo therapy has been approved in the U.S., EU, or other key jurisdictions, making regulatory approval uncertain
- Successful product development requires solving multiple technical challenges, including safe delivery of therapeutic agents to target cells and demonstrating safety, efficacy, potency, purity, and selectivity

## Clinical Development Risks
- All programs are still in discovery, preclinical, or clinical stages
- Clinical development is lengthy, expensive, and has uncertain outcomes
- Clinical trials can fail at any stage, and preclinical results may not predict clinical success
- The company faces a clinical hold on an IND for one of its trials (MAGNITUDE trial for NTLA-2001)

## Market Adoption and Perception Risks
- Public perception and media coverage of safety or efficacy issues may discourage clinical trial participation and physician/patient acceptance
- Physicians and healthcare providers are often slow to adopt new technologies and may view these therapies as too complex or risky
- Ethical concerns related to genome editing may adversely influence adoption
- Regulatory changes could limit development, commercialization, or approval of product candidates

## Pre-written sections (judge input)

### Financial Health

Intellia Therapeutics trades at $12.26 with a market capitalization of $1.72 billion, down significantly from its 52-week high of $28.25. The company is unprofitable with a net loss of $400 million against revenue of $59.5 million, resulting in a negative profit margin and forward P/E ratio of -4.72, indicating substantial cash burn typical of early-stage biotech firms. As a clinical-stage gene-editing company, NTLA's financial viability depends heavily on successful clinical trial outcomes and future commercialization of its CRISPR-based therapeutics rather than current operational profitability. The company faces considerable execution risk and will likely require additional capital raises to fund ongoing development programs.

### Recent Developments

Intellia Therapeutics filed its most recent 10-Q on August 6, 2026, continuing to highlight significant risk factors inherent to its gene-editing biotechnology platform. The company remains in a pre-commercial or early-stage revenue phase, with $59.5 million in annual revenue against a net loss of $400 million, reflecting the substantial R&D investments typical of clinical-stage biotech firms. With a stock price of $12.26 (down from a 52-week high of $28.25), investors should monitor upcoming clinical trial results and regulatory milestones, as these will be critical catalysts for valuation recovery. The negative forward P/E ratio underscores the company's current unprofitability, making execution on its pipeline programs essential for long-term investor returns.

### SEC Filing Highlights

Intellia Therapeutics is advancing CRISPR genome editing-based therapeutics with clinical-stage programs including nexiguran ziclumeran (NTLA-2001) and lonvoguran ziclumeran (NTLA-2002), targeting both in vivo and ex vivo applications. The company faces significant regulatory and technical risks, as no in vivo genome editing therapies have been approved in major jurisdictions, and the company must overcome critical challenges in safe delivery, efficacy optimization, and safety demonstration. Additional headwinds include manufacturing and supply chain complexities, limited physician and patient familiarity with CRISPR therapeutics, and potential public perception concerns regarding genome editing that could impact trial enrollment and market adoption. Success with one CRISPR program does not guarantee transferability to other candidates, adding execution risk to the pipeline.

### Risk Factors

- **Unproven Technology and Regulatory Uncertainty**: CRISPR-based in vivo therapies remain largely unvalidated with no approved genome editing treatments in major jurisdictions. The company faces significant technical hurdles in safe delivery and demonstrating safety/efficacy, with uncertain regulatory pathways and a current clinical hold on its MAGNITUDE trial for NTLA-2001.

- **Clinical Development Challenges**: All programs are in early-stage development with lengthy, expensive clinical trials that can fail at any stage. Preclinical results may not translate to clinical success, creating substantial execution risk and capital requirements before any potential commercialization.

- **Market Adoption and Perception Risks**: Physician and patient adoption may be hindered by concerns about complexity, safety perception, and ethical issues surrounding genome editing. Negative media coverage or regulatory changes could significantly impede clinical trial enrollment and commercial viability.

## Audited (Exec Summary + Outlook)

### Executive Summary
Intellia Therapeutics is a clinical-stage biotechnology company advancing CRISPR genome editing-based therapeutics, including lead programs nexiguran ziclumeran (NTLA-2001) and lonvoguran ziclumeran (NTLA-2002), operating in a field where no in vivo genome editing therapy has yet received regulatory approval in any major jurisdiction. Trading at $12.26 — less than half its 52-week high of $28.25 — with a $1.72 billion market capitalization, a net loss of $400 million against $59.5 million in revenue, and a forward P/E of -4.72, the stock reflects deep investor skepticism and the high-risk, pre-commercial nature of the platform. The single most important near-term variable shaping the investment outcome is resolution of the clinical hold on the MAGNITUDE trial for NTLA-2001, as regulatory clearance and subsequent clinical data would represent the most direct catalyst for restoring confidence in the pipeline.

### Outlook
The directional outlook for Intellia Therapeutics is **cautious**, reflecting the convergence of meaningful platform potential and substantial near-term execution risk. The primary tailwind is the transformative, first-mover nature of CRISPR-based in vivo gene editing — if the technology can be validated clinically, the addressable opportunity is significant and the competitive moat could be durable. However, headwinds are considerable and immediate: the clinical hold on the MAGNITUDE trial for NTLA-2001 is the most pressing overhang, and its resolution — and the direction of any regulatory feedback — will be the clearest signal of whether the thesis can recover. Investors should closely monitor the status of that clinical hold, safety and efficacy data readouts across both NTLA-2001 and NTLA-2002, and any updates to the regulatory pathway for in vivo genome editing more broadly. The company's cash runway and the pace of capital consumption are also critical variables to watch, given the likelihood of future dilutive financing. The view would become more constructive if the clinical hold is lifted with a clear path forward, if clinical data demonstrate a compelling safety and efficacy profile, and if regulatory agencies signal greater clarity on approval standards for this modality. Conversely, the thesis would weaken further on adverse clinical data, additional regulatory setbacks, or signs that the CRISPR platform's challenges are not transferable across programs — reinforcing the risk that pipeline diversification does not provide the protection investors might expect.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "Trading at $12.26"
LABEL: SUPPORTED
REASON: The source data explicitly lists `"current_price": 12.26`.

---

CLAIM: "less than half its 52-week high of $28.25"
LABEL: SUPPORTED
REASON: $12.26 / $28.25 = 0.4340, which is less than 0.50 (i.e., less than half); the 52-week high of $28.25 is explicitly in the source data (`"week_52_high": 28.25`), and the arithmetic confirms the positional claim.

---

CLAIM: "$1.72 billion market capitalization"
LABEL: SUPPORTED
REASON: Source data shows `"market_cap": 1717953280.0`, which rounds to $1.72 billion.

---

CLAIM: "a net loss of $400 million"
LABEL: SUPPORTED
REASON: Source data shows `"net_income": -399975008.0`, which rounds to -$400 million; the pre-written Financial Health section also states "net loss of $400 million."

---

CLAIM: "$59.5 million in revenue"
LABEL: SUPPORTED
REASON: Source data shows `"revenue": 59506000.0`, which rounds to $59.5 million.

---

CLAIM: "a forward P/E of -4.72"
LABEL: SUPPORTED
REASON: Source data explicitly lists `"forward_pe": -4.7171445`, which rounds to -4.72.

---

CLAIM: "nexiguran ziclumeran (NTLA-2001) and lonvoguran ziclumeran (NTLA-2002)"
LABEL: SUPPORTED
REASON: Both named programs are explicitly identified in the RAG — SEC Highlights section and the pre-written SEC Filing Highlights section.

---

CLAIM: "no in vivo genome editing therapy has yet received regulatory approval in any major jurisdiction"
LABEL: SUPPORTED
REASON: Explicitly stated in the RAG — SEC Highlights: "No genome editing in vivo therapy has been approved in the U.S., EU, or other key jurisdictions."

---

CLAIM: "clinical hold on the MAGNITUDE trial for NTLA-2001"
LABEL: SUPPORTED
REASON: Explicitly stated in the RAG — Risk Factors: "The company faces a clinical hold on an IND for one of its trials (MAGNITUDE trial for NTLA-2001)."

---

**OUTLOOK**

---

CLAIM: "clinical hold on the MAGNITUDE trial for NTLA-2001" (repeated in Outlook)
LABEL: SUPPORTED
REASON: Same as above; explicitly present in the RAG — Risk Factors section.

---

CLAIM: "safety and efficacy data readouts across both NTLA-2001 and NTLA-2002"
LABEL: SUPPORTED
REASON: Both programs (NTLA-2001 and NTLA-2002) are named in the source data (RAG — SEC Highlights and pre-written sections); the reference to safety and efficacy data is consistent with the clinical-stage characterization in the source.

---

CLAIM: "the likelihood of future dilutive financing"
LABEL: INFERENCE
REASON: The pre-written Financial Health section states the company "will likely require additional capital raises," and the net loss of ~$400M against $59.5M revenue makes this a directly derivable forward-looking inference from the source data; no specific financing amount or timeline is asserted.

---

*No other specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section beyond those already evaluated above.*
