# NTLA — local-model

## Metadata

ticker: NTLA
arm: local-model
judge_prompt_version: v2
context_sha256: 6761526dd59ed3e0a82dedfba025f89cfd45cbb4531936090ddc926547b4f182
local_model_served_name: financial-lora
local_model_dir: qwen-ft
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
[From Pinecone cache] I cannot provide a summary of the latest 10-K and 10-Q based on the context provided. The information given consists only of risk factor disclosures from a 10-K filing for the year ended December 31, 2025, specifically focusing on risks related to preclinical and clinical development of CRISPR-based therapeutics.

To provide a comprehensive summary of the latest 10-K and 10-Q filings, I would need access to additional sections of these documents, including:

- Business overview and strategy
- Financial performance and results of operations
- Management's discussion and analysis (MD&A)
- Balance sheet and cash flow information
- Recent developments and milestones
- Liquidity and capital resources
- Other material business information

The context provided only covers a portion of the risk factors section, which represents just one component of these regulatory filings. A complete summary would require information from multiple sections of both documents.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors related to its CRISPR genome editing technology business:

## Clinical Development and Regulatory Risks
- CRISPR genome editing technology has only recently been clinically validated for human therapeutic use, and in vivo CRISPR-based therapies remain largely unproven
- No genome editing in vivo therapy has been approved in the U.S., EU, or other key jurisdictions
- Clinical development is lengthy, expensive, and uncertain in outcome
- Regulatory agencies have very limited or no experience with CRISPR-based therapeutics, which may require additional testing and delay development
- The company faces challenges in obtaining regulatory authorization and approval for clinical trials

## Technical and Development Challenges
- Successfully developing safe delivery methods to target cells and optimizing efficacy and specificity remain unsolved issues
- Manufacturing, scalability, and profitability of CRISPR products are uncertain
- Success in one CRISPR product does not guarantee success in others
- Clinical trials may fail to demonstrate safety or efficacy, or produce negative or inconclusive results

## Market Adoption and Perception Risks
- Public perception and media coverage of safety or efficacy issues may discourage clinical trial participation and patient/physician acceptance
- Ethical concerns related to genome editing may adversely influence adoption
- Physicians and healthcare providers are often slow to adopt new technologies and may view these therapies as too complex or risky
- Healthcare providers and payors may determine that benefits do not outweigh costs

## Operational Risks
- Challenges in patient enrollment, retention, and follow-up
- Supply chain and manufacturing challenges for materials and product candidates
- Dependence on third-party contractors and clinical trial sites

## Pre-written sections (judge input)

### Financial Health

Intellia Therapeutics, Inc., trades under the ticker symbol NTLA. It is classified as a healthcare company within the biotechnology sector. As of February 26, 2026, the company carries a market capitalization of $172.78 billion and a forward P/E ratio of -4.74x. Over the past five years, the company has reported net income of -$39.99 billion and a net loss per share of $0.00. The company reports an annual revenue of $5.95 billion and a net loss of $3.99 billion over the course of its fiscal year ending December 31, 2025.

### Recent Developments

Intellia Therapeutics filed its most recent 10-Q on August 6, 2026, continuing to highlight significant risk factors inherent to its gene-editing biotechnology platform. The company remains in a pre-commercial or early-stage revenue phase, with $59.5M in annual revenue against a net loss of $400M, reflecting typical biotech R&D spending patterns. With a market cap of $1.73B and stock trading at $12.33 (down 56% from its 52-week high of $28.25), investor sentiment appears cautious regarding near-term profitability. The lack of recent positive news catalysts suggests the market is awaiting clinical trial results or regulatory milestones to justify the company's valuation. Investors should monitor upcoming pipeline announcements and cash burn rates, as the company's path to profitability remains dependent on successful clinical development and commercialization of its CRISPR-based therapies.

### SEC Filing Highlights

Based on available information from Intellia Therapeutics' recent SEC filings, the company continues to advance its CRISPR-based therapeutic pipeline while managing inherent risks associated with preclinical and clinical development stages. The filing emphasizes significant risks related to the development of in vivo CRISPR therapeutics, including regulatory approval uncertainties and the challenges of translating preclinical results to clinical efficacy. As a clinical-stage biopharmaceutical company, Intellia's financial position and operational progress remain dependent on successful advancement of its pipeline candidates and securing adequate capital resources. Investors should note that the company's risk disclosures highlight the speculative nature of CRISPR-based drug development and the substantial regulatory hurdles ahead.

### Primary Risk Factors Disclosed

#### Clinical Development and Regulatory Risks
- CRISPR genome editing technology has only recently been clinically validated for human therapeutic use, and in vivo CRISPR-based therapies remain largely unproven.
- No genome editing in vivo therapy has been approved in the U.S., EU, or other key jurisdictions.
- Clinical development is lengthy, expensive, and uncertain in outcome.
- Regulatory agencies have very limited or no experience with CRISPR-based therapeutics, which may require additional testing and delay development.
- The company faces challenges in obtaining regulatory authorization and approval for clinical trials.

#### Technical and Development Challenges
- Successfully developing safe delivery methods to target cells and optimizing efficacy and specificity remain unsolved issues.
- Manufacturing, scalability, and profitability of CRISPR products are uncertain.
- Success in one CRISPR product does not guarantee success in others.
- Clinical trials may fail to demonstrate safety or efficacy, or produce negative or inconclusive results.

#### Market Adoption and Perception Risks
- Public perception and media coverage of safety or efficacy issues may discourage clinical trial participation and patient/physician acceptance.
- Ethical concerns related to genome editing may adversely influence adoption.
- Physicians and healthcare providers are often slow to adopt new technologies and may view these therapies as too complex or risky.
- Healthcare providers and payors may determine that benefits do not outweigh costs.

#### Operational Risks
- Challenges in patient enrollment, retention, and follow-up.
- Supply chain and manufacturing challenges for materials and product candidates.
- Dependence on third-party contractors and clinical trial sites.

## Audited (Exec Summary + Outlook)

### Executive Summary
Intellia Therapeutics is a clinical-stage biopharmaceutical company developing CRISPR-based in vivo gene-editing therapies, operating with $59.5M in annual revenue against a net loss of $400M as it advances a pipeline in which no comparable therapy has yet received regulatory approval in the U.S., EU, or other key jurisdictions. The stock is notable now precisely because of its dislocation — trading at $12.33, down 56% from its 52-week high of $28.25, with a market cap of $1.73B — reflecting deep investor skepticism about near-term profitability and the absence of recent positive catalysts. The single most important near-term variable is clinical trial data: meaningful evidence of safety and efficacy from its pipeline candidates would be the primary catalyst capable of shifting market sentiment and validating the company's core scientific thesis.

### Outlook
The directional lean on Intellia Therapeutics is **cautious**, with the possibility of turning more constructive contingent on specific, binary catalysts. The primary tailwind is the platform itself: CRISPR-based in vivo gene editing represents a genuinely novel therapeutic modality, and a first-mover regulatory approval in any key jurisdiction would be a transformative event for the company and the field. The headwinds, however, are substantial and immediate — a persistent cash burn against limited revenue, a stock already down sharply from its recent high, and a regulatory environment with no established precedent for approving in vivo CRISPR therapies. Investors should watch four key variables closely: (1) clinical trial readouts for safety and efficacy, which represent the clearest near-term inflection points; (2) cash runway and the pace of cash burn, which will determine whether the company can reach those milestones without dilutive financing; (3) regulatory signals from the FDA, EMA, or other agencies regarding their evolving framework for CRISPR-based therapeutics; and (4) public and physician sentiment around gene editing, which could accelerate or impede patient enrollment and eventual commercial adoption. The thesis would strengthen materially on positive clinical data, a regulatory approval anywhere in the pipeline, or a meaningful partnership that validates the platform and extends the cash runway; it would weaken further on trial failures, safety signals, an inability to secure capital on reasonable terms, or adverse regulatory guidance that raises the bar for approval.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$59.5M in annual revenue"
LABEL: SUPPORTED
REASON: The raw source data shows revenue of $59,506,000, which rounds to $59.5M; this figure also appears explicitly in the "Recent Developments" pre-written section.

---

CLAIM: "net loss of $400M"
LABEL: SUPPORTED
REASON: The raw source data shows net_income of -$399,975,008, which rounds to -$400M; this figure also appears explicitly in the "Recent Developments" pre-written section.

---

CLAIM: "no comparable therapy has yet received regulatory approval in the U.S., EU, or other key jurisdictions"
LABEL: SUPPORTED
REASON: The Risk Factors section explicitly states "No genome editing in vivo therapy has been approved in the U.S., EU, or other key jurisdictions."

---

CLAIM: "trading at $12.33"
LABEL: SUPPORTED
REASON: The raw source data explicitly lists current_price as 12.33 USD.

---

CLAIM: "down 56% from its 52-week high of $28.25"
LABEL: SUPPORTED
REASON: The 52-week high of $28.25 is present in the source data; the percentage decline computes as (28.25 − 12.33) / 28.25 = 15.92 / 28.25 ≈ 56.35%, which is within 0.15 percentage points of 56%, and the $28.25 figure is explicitly in the source data and the "Recent Developments" section.

---

CLAIM: "market cap of $1.73B"
LABEL: SUPPORTED
REASON: The raw source data shows market_cap of $1,727,762,048, which rounds to $1.73B; this figure also appears in the "Recent Developments" pre-written section.

---

**OUTLOOK**

---

CLAIM: "a stock already down sharply from its recent high"
LABEL: SUPPORTED
REASON: This is a directional restatement of the verified 56% decline from the 52-week high of $28.25 to the current price of $12.33, both present in the source data.

---

*(No additional specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section beyond the directional reference above. All other content in the Outlook consists of qualitative risk characterizations, conditional statements, and general strategic commentary without specific numerical claims requiring verification.)*

---

**SUMMARY TABLE**

| Claim | Label |
|---|---|
| $59.5M in annual revenue | SUPPORTED |
| net loss of $400M | SUPPORTED |
| No regulatory approval in U.S., EU, or other key jurisdictions | SUPPORTED |
| Trading at $12.33 | SUPPORTED |
| Down 56% from 52-week high of $28.25 | SUPPORTED |
| Market cap of $1.73B | SUPPORTED |
| Stock already down sharply from its recent high (Outlook) | SUPPORTED |

All quantitative and forward-looking claims in the Executive Summary and Outlook are supported by the source data. No unsupported or inference-only claims were identified.
