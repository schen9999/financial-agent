# NTLA — local-model

## Metadata

ticker: NTLA
arm: local-model
judge_prompt_version: v2
context_sha256: e7c8864107a2f2ea02b9229f95582536a8b4fc07fccf13631b3d14e9ae136aff
local_model_served_name: qwen2.5-7b-instruct
local_model_dir: qwen2.5-7b-instruct
local_model_backend: openai
local_model_url: http://vllm.financial-agent.svc:8000
local_model_sampling: {"max_tokens": 512, "min_p": 0.0, "repetition_penalty": 1.1, "temperature": 0.1, "top_k": 20, "top_p": 0.8}

## Retrieved source context

STOCK DATA:
{
  "ticker": "NTLA",
  "company_name": "Intellia Therapeutics, Inc.",
  "current_price": 12.33,
  "currency": "USD",
  "market_cap": 1727762048.0,
  "forward_pe": -4.7440777,
  "week_52_high": 28.25,
  "week_52_low": 7.95,
  "revenue": 59506000.0,
  "net_income": -399975008.0,
  "profit_margin": 0.0,
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
[From Pinecone cache] I cannot provide a summary of the latest 10-K and 10-Q based on the context provided. The information given consists only of risk factor disclosures from a 10-K filing for the year ended December 31, 2025, specifically focusing on risks related to preclinical and clinical development of CRISPR-based therapeutics.

To provide a comprehensive summary of the latest 10-K and 10-Q filings, I would need access to additional sections of these documents, including:

- Business overview and strategy
- Financial performance and results of operations
- Management's discussion and analysis (MD&A)
- Balance sheet and cash flow information
- Liquidity and capital resources
- Recent developments and milestones
- Competitive landscape
- Other material business information

The context provided only covers one portion of the risk factors section, which represents just one component of a complete 10-K filing. A meaningful summary would require information from multiple sections of both the annual and quarterly reports.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors related to its business:

## Clinical Development and Technology Risks
- CRISPR genome editing technology has only recently been clinically validated for human therapeutic use, and in vivo CRISPR-based therapies remain largely unproven
- No genome editing in vivo therapy has been approved in the U.S., EU, or other key jurisdictions
- The company's approaches to developing CRISPR-based therapeutics are unproven and may never lead to marketable products
- Significant technical challenges must be solved, including safe delivery of therapeutic agents to target cells and optimization of efficacy and specificity

## Regulatory and Approval Challenges
- Clinical development is lengthy, expensive, and uncertain in outcome
- Regulatory authorities have very limited or no experience with clinical development of CRISPR-based therapeutics, particularly in vivo therapeutics
- The FDA and other regulatory agencies may require additional testing, data, or impose other requirements that could delay development
- Regulatory requirements for later-phase clinical trials are more stringent than earlier phases

## Market Adoption and Public Perception Risks
- Public perception and media coverage of potential safety or efficacy issues may adversely influence participation in clinical trials and physician/patient acceptance
- Ethical concerns related to genome editing and CRISPR-based therapies may impact adoption
- Physicians, healthcare providers, and payors are often slow to adopt new products and may view these therapies as too complex or risky
- New legislation or regulations could limit the company's ability to develop or commercialize product candidates

## Clinical Trial Execution Risks
- Challenges in obtaining regulatory authorization to conduct clinical trials
- Difficulty enrolling sufficient subjects or maintaining enrollment rates
- Potential for clinical trials to fail at any stage
- Undesirable side effects or unexpected characteristics of product candidates

## Pre-written sections (judge input)

### Financial Health

Intellia Therapeutics, Inc. (NTLA) currently trades at $12.33 per share, with a market capitalization of approximately $1.73B. The company has a forward P/E ratio of -4.74, indicating either significant losses or an unusual valuation metric. Revenue stands at $59.5M, but the net income is a substantial loss of -$399.98M, resulting in a profit margin of 0%. These metrics suggest ongoing financial challenges and high-risk investing conditions.

### Recent Developments

Intellia Therapeutics filed its most recent 10-Q on August 6, 2026, continuing to highlight significant risk factors inherent to its gene-editing biotechnology business. The company remains in a pre-commercial or early-stage revenue phase, with $59.5 million in annual revenue against a net loss of $400 million, reflecting the substantial R&D investments typical of clinical-stage biotech firms. With a stock price of $12.33 (down 56% from its 52-week high of $28.25), investors should monitor upcoming clinical trial results and regulatory milestones, as these will be critical catalysts for valuation recovery. The negative forward P/E ratio underscores the company's current unprofitability, making execution on its pipeline programs essential for long-term investor returns.

### SEC Filing Highlights

Based on available information, Intellia Therapeutics' recent SEC filings emphasize the significant risks inherent in developing CRISPR-based therapeutics, including preclinical and clinical development challenges. The company's disclosures indicate a focus on its pipeline of gene-editing therapies, though comprehensive financial performance metrics and operational results would require access to complete 10-K and 10-Q sections beyond risk factor disclosures. Investors should note that detailed information regarding liquidity, cash position, clinical trial progress, and near-term milestones would be essential for a complete investment assessment and should be reviewed directly in the full SEC filings.

### Risk Factors

- **Clinical Development and Technology Risks:** CRISPR-based therapies are unproven and face significant technical challenges, including safe delivery and optimization of efficacy and specificity.
- **Regulatory and Approval Challenges:** Regulatory authorities lack experience with CRISPR-based therapeutics, leading to potential delays and stringent requirements that could impede development.

## Audited (Exec Summary + Outlook)

### Executive Summary
Intellia Therapeutics is a clinical-stage biotechnology company developing CRISPR-based gene-editing therapies, operating with $59.5M in revenue and a market capitalization of approximately $1.73B as it works to translate a pioneering technology platform into approved medicines. The stock is notable now precisely because of its vulnerability — trading at $12.33, down 56% from its 52-week high of $28.25, against a backdrop of a $400M net loss — placing the company at a high-stakes inflection point where investor confidence hinges entirely on pipeline execution rather than commercial fundamentals. The single most important near-term variable is the outcome of upcoming clinical trial readouts, which will either validate the CRISPR platform's therapeutic potential and catalyze a rerating, or deepen concerns about the company's ability to justify its ongoing R&D burn.

### Outlook
The directional outlook for Intellia is **cautious**, though not without a path to improvement. The primary tailwind is the transformative potential of CRISPR gene editing as a therapeutic modality — if the platform delivers durable, safe clinical results, the technology could command significant long-term value and attract partnership or licensing interest that meaningfully changes the company's financial trajectory. Against that, the headwinds are substantial: a large and ongoing net loss, a stock already deeply discounted from its recent highs, regulatory inexperience with CRISPR-based medicines, and the binary nature of clinical-stage biotech investing, where a single trial failure can be disproportionately damaging. Investors should watch clinical trial data readouts as the foremost catalyst, alongside any signals from regulatory agencies regarding their evolving framework for gene-editing therapies, the company's liquidity and cash runway as disclosed in full SEC filings, and whether Intellia secures partnerships or collaborations that could validate the pipeline and reduce financial pressure. What would shift the view toward constructive is a combination of positive clinical efficacy and safety data, meaningful regulatory progress, and evidence of a sustainable funding path; what would deepen the cautious stance is trial setbacks, regulatory delays, or deterioration in the company's cash position without a clear path to additional capital.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$59.5M in revenue"
LABEL: SUPPORTED
REASON: The source data lists revenue as $59,506,000, which rounds to $59.5M; this figure also appears explicitly in the pre-written Financial Health and Recent Developments sections.

---

CLAIM: "market capitalization of approximately $1.73B"
LABEL: SUPPORTED
REASON: The source data lists market_cap as $1,727,762,048, which rounds to approximately $1.73B, consistent with the pre-written Financial Health section.

---

CLAIM: "trading at $12.33"
LABEL: SUPPORTED
REASON: The source data explicitly lists current_price as $12.33.

---

CLAIM: "down 56% from its 52-week high of $28.25"
LABEL: SUPPORTED
REASON: The 52-week high of $28.25 is present in the source data; the percentage decline computes as (28.25 − 12.33) / 28.25 = 15.92 / 28.25 ≈ 56.35%, which rounds to 56% — within 0.15 percentage points of the stated figure; the pre-written Recent Developments section also states "down 56% from its 52-week high of $28.25."

---

CLAIM: "52-week high of $28.25"
LABEL: SUPPORTED
REASON: The source data explicitly lists week_52_high as $28.25.

---

CLAIM: "a $400M net loss"
LABEL: SUPPORTED
REASON: The source data lists net_income as −$399,975,008, which rounds to −$400M; this figure also appears in the pre-written Recent Developments section as "a net loss of $400 million."

---

**OUTLOOK**

No additional specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section. The Outlook is composed entirely of qualitative directional statements, conditional language, and general characterizations (e.g., "large and ongoing net loss," "deeply discounted from its recent highs," "binary nature of clinical-stage biotech investing") without introducing any new specific quantitative claims beyond those already evaluated above.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | $59.5M in revenue | SUPPORTED |
| 2 | Market cap ~$1.73B | SUPPORTED |
| 3 | Trading at $12.33 | SUPPORTED |
| 4 | Down 56% from 52-week high | SUPPORTED |
| 5 | 52-week high of $28.25 | SUPPORTED |
| 6 | $400M net loss | SUPPORTED |

All six quantitative claims in the Executive Summary are supported by the source data. The Outlook section contains no additional quantitative or forward-looking numerical claims requiring evaluation.
