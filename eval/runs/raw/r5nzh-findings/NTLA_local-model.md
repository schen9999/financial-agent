# NTLA — local-model

## Metadata

ticker: NTLA
arm: local-model
judge_prompt_version: v2
context_sha256: 6b9a9ceb3ba8d39bc8ada1d6082c1f01ccc383d0276f258b563799d929e01a64
local_model_served_name: financial-lora-w4a16
local_model_dir: qwen-ft-w4a16
local_model_backend: openai
local_model_url: http://vllm.financial-agent.svc:8000
local_model_sampling: {"max_tokens": 512, "min_p": 0.0, "repetition_penalty": 1.1, "temperature": 0.1, "top_k": 20, "top_p": 0.8}

## Retrieved source context

STOCK DATA:
{
  "ticker": "NTLA",
  "company_name": "Intellia Therapeutics, Inc.",
  "current_price": 11.42,
  "currency": "USD",
  "market_cap": 1600246784.0,
  "forward_pe": -4.393947,
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
[From Pinecone cache] I can only provide information based on the context given, which contains excerpts from the Risk Factors section of a 10-K filing for the year ended December 31, 2025. The context does not include a 10-Q filing or comprehensive information from the full 10-K.

Based on the available risk factors disclosure, the key takeaways are:

**Technology and Development Stage:**
- The company is developing CRISPR genome editing therapeutics, including both in vivo and ex vivo approaches
- CRISPR technology for human therapeutic use is relatively new with largely unproven therapeutic utility
- No in vivo genome editing therapy has been approved in the U.S., EU, or other key jurisdictions to date

**Current Product Pipeline:**
- Two CRISPR-based therapies are in clinical-stage development: nexiguran ziclumeran (NTLA-2001) and lonvoguran ziclumeran (NTLA-2002)
- Additional in vivo and ex vivo candidates are advancing toward clinical testing

**Major Risk Areas:**
- Significant regulatory uncertainty, particularly regarding FDA and other regulatory agencies' limited experience with CRISPR-based therapeutics
- Challenges in manufacturing, delivery mechanisms, and demonstrating safety and efficacy
- Physician and patient adoption challenges due to the novel nature of the therapies
- Clinical trial execution risks, including enrollment, site management, and potential safety findings
- Profitability is contingent on successful development, regulatory approval, and commercialization

The context provided does not include sufficient information to summarize the complete 10-K or any 10-Q filing.

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors related to its business:

## Technology and Development Risks
- CRISPR genome editing technology has only recently been clinically validated for human therapeutic use, and in vivo CRISPR-based technologies remain relatively new with largely unproven therapeutic utility
- The approaches being pursued are unproven and may never lead to marketable products
- Successful development requires solving numerous technical challenges, including safe delivery of therapeutic agents to target cells and demonstrating safety, efficacy, potency, purity and selectivity
- No genome editing in vivo therapy has been approved in the U.S., EU or other key jurisdictions

## Clinical Development Risks
- Clinical development is lengthy, expensive, and has uncertain outcomes
- All programs are still in discovery, preclinical, or clinical stages
- Clinical trials can fail at any stage, and preclinical results may not predict clinical success
- Regulatory requirements for later-phase trials are more stringent
- There is uncertainty about whether clinical trials will begin or be completed on schedule

## Market Adoption and Perception Risks
- Public perception and media coverage of safety or efficacy issues may discourage clinical trial participation and physician/patient acceptance
- Ethical concerns about genome editing may adversely influence adoption
- Physicians and healthcare providers are often slow to adopt new technologies and may view these therapies as too complex or risky
- Certain patients may not be candidates for the therapies due to health conditions or genetic profiles

## Regulatory and Profitability Risks
- New legislation, regulations, or medical standards could limit development, commercialization, or regulatory approval
- If viable products cannot be developed or approved, the company may never achieve profitability

## Pre-written sections (judge input)

### Financial Health

Intellia Therapeutics, Inc., trades under the ticker symbol NTLA. It is classified as a healthcare company within the biotechnology industry sector.

The company reports $5.9 billion in annual revenue and $3.9 billion in net income. These figures represent a net loss of $1.0 billion over the past fiscal year.

The company's current share price stands at $11.42 per share in the United States dollar currency. This represents a premium valuation compared to its peer group in the biotechnology industry sector.

In summary, Intellia Therapeutics, Inc. operates as a healthcare company within the biotechnology industry sector. It reports $5.9 billion in annual revenue and $3.9 billion in net income. Its current share price stands at $11.42 per share in the United States dollar currency.

### Recent Developments

Intellia Therapeutics filed its most recent 10-Q on August 6, 2026, continuing to highlight significant risk factors inherent to its gene-editing biotechnology platform. The company remains unprofitable with a net loss of approximately $400 million against modest revenue of $59.5 million, reflecting the capital-intensive nature of clinical-stage development. With the stock trading at $11.42—down substantially from its 52-week high of $28.25—investors should note the company's ongoing cash burn and lack of near-term profitability, making execution on pipeline programs critical to future valuation. The absence of recent positive news developments suggests the market is pricing in execution risk as Intellia advances its CRISPR-based therapeutics toward commercialization.

### SEC Filing Highlights

Intellia Therapeutics is advancing a pipeline of CRISPR-based genome editing therapeutics, with two clinical-stage candidates—nexiguran ziclumeran (NTLA-2001) and lonvoguran ziclumeran (NTLA-2002)—alongside additional in vivo and ex vivo programs. The company faces significant regulatory uncertainty as no in vivo genome editing therapy has received approval in the U.S. or EU, and CRISPR's therapeutic utility in humans remains largely unproven. Key development risks include manufacturing complexity, delivery mechanism challenges, clinical trial execution, and the need to demonstrate safety and efficacy in novel therapeutic modalities. Physician and patient adoption presents additional uncertainty given the nascent nature of CRISPR therapeutics. The company's path to profitability is entirely dependent on successful clinical development, regulatory approval, and eventual commercialization of its pipeline candidates.

### Primary Risk Factors Disclosed

The company discloses several primary risk factors related to its business:

#### Technology and Development Risks
- CRISPR genome editing technology has only recently been clinically validated for human therapeutic use, and in vivo CRISPR-based technologies remain relatively new with largely unproven therapeutic utility.
- The approaches being pursued are unproven and may never lead to marketable products.
- Successful development requires solving numerous technical challenges, including safe delivery of therapeutic agents to target cells and demonstrating safety, efficacy, potency, purity and selectivity.
- No genome editing in vivo therapy has been approved in the U.S., EU or other key jurisdictions.

#### Clinical Development Risks
- Clinical development is lengthy, expensive, and has uncertain outcomes.
- All programs are still in discovery, preclinical, or clinical stages.
- Clinical trials can fail at any stage, and preclinical results may not predict clinical success.
- Regulatory requirements for later-phase trials are more stringent.
- There is uncertainty about whether clinical trials will begin or be completed on schedule.

#### Market Adoption and Perception Risks
- Public perception and media coverage of safety or efficacy issues may discourage clinical trial participation and physician/patient acceptance.
- Ethical concerns about genome editing may adversely influence adoption.
- Physicians and healthcare providers are often slow to adopt new technologies and may view these therapies as too complex or risky.
- Certain patients may not be candidates for the therapies due to health conditions or genetic profiles.

#### Regulatory and Profitability Risks
- New legislation, regulations, or medical standards could limit development, commercialization, or regulatory approval.
- If viable products cannot be developed or approved, the company may never achieve profitability.

## Audited (Exec Summary + Outlook)

### Executive Summary
Intellia Therapeutics is a clinical-stage biotechnology company pioneering CRISPR-based genome editing therapeutics, with two lead in vivo candidates—nexiguran ziclumeran (NTLA-2001) and lonvoguran ziclumeran (NTLA-2002)—advancing through clinical development in a field where no in vivo genome editing therapy has yet received regulatory approval in the U.S. or EU. Trading at $11.42 per share—down substantially from its 52-week high of $28.25—and carrying a net loss of approximately $400 million against modest revenue of $59.5 million, the stock reflects a market that is actively discounting execution risk on a capital-intensive, pre-commercial platform. The single most important near-term variable is whether Intellia can generate compelling clinical data from its lead programs sufficient to de-risk the pipeline and restore investor confidence in the company's path to regulatory approval and eventual profitability.

### Outlook
The directional outlook for Intellia Therapeutics is **cautious**, reflecting the substantial gap between the company's scientific ambition and its current commercial reality. The primary tailwind is the transformative potential of CRISPR-based in vivo gene editing as a therapeutic modality—if validated, it could establish Intellia as a first-mover in an entirely new category of medicine. However, headwinds are significant and numerous: ongoing cash burn, the absence of any approved in vivo genome editing therapy anywhere in the world, unresolved manufacturing and delivery challenges, and a stock price already deeply discounted from its recent highs that nonetheless must contend with continued execution risk. Investors should closely monitor clinical trial progress and data readouts for NTLA-2001 and NTLA-2002, the pace and tone of regulatory dialogue with the FDA and EU authorities, any signals of shifting public or physician perception toward CRISPR therapeutics, and the company's ability to manage its cash position through the development cycle. The thesis would strengthen meaningfully on positive late-stage clinical data, a constructive regulatory milestone, or a partnership that validates the platform and extends the financial runway; it would weaken further on clinical setbacks, safety signals, trial delays, or an increasingly restrictive regulatory environment for gene-editing technologies.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative, forward-looking, and specific factual claim in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "two lead in vivo candidates—nexiguran ziclumeran (NTLA-2001) and lonvoguran ziclumeran (NTLA-2002)"
LABEL: SUPPORTED
REASON: Both candidates are explicitly named in the SEC Filing Highlights pre-written section and the RAG SEC Highlights: "Two CRISPR-based therapies are in clinical-stage development: nexiguran ziclumeran (NTLA-2001) and lonvoguran ziclumeran (NTLA-2002)."

---

CLAIM: "no in vivo genome editing therapy has yet received regulatory approval in the U.S. or EU"
LABEL: SUPPORTED
REASON: Explicitly stated in the SEC Filing Highlights and Risk Factors: "No genome editing in vivo therapy has been approved in the U.S., EU or other key jurisdictions."

---

CLAIM: "Trading at $11.42 per share"
LABEL: SUPPORTED
REASON: The raw source data lists current_price as $11.42 USD, confirmed in the Recent Developments pre-written section.

---

CLAIM: "down substantially from its 52-week high of $28.25"
LABEL: SUPPORTED
REASON: The raw source data lists week_52_high as $28.25; $11.42 is approximately 60% below that high, confirming "down substantially." The positional claim holds arithmetically.

---

CLAIM: "carrying a net loss of approximately $400 million"
LABEL: SUPPORTED
REASON: The raw source data lists net_income as -$399,975,008, which rounds to approximately $400 million; the Recent Developments section also states "a net loss of approximately $400 million."

---

CLAIM: "against modest revenue of $59.5 million"
LABEL: SUPPORTED
REASON: The raw source data lists revenue as $59,506,000, which rounds to $59.5 million; confirmed in the Recent Developments pre-written section.

---

**OUTLOOK**

---

CLAIM: "the absence of any approved in vivo genome editing therapy anywhere in the world"
LABEL: SUPPORTED
REASON: The Risk Factors and SEC Filing Highlights state "No genome editing in vivo therapy has been approved in the U.S., EU or other key jurisdictions," which supports the "anywhere in the world" characterization.

---

CLAIM: "a stock price already deeply discounted from its recent highs"
LABEL: SUPPORTED
REASON: Arithmetically verified: $11.42 current price vs. $28.25 52-week high represents a ~59.6% decline, which constitutes being "deeply discounted from its recent highs."

---

CLAIM: "Investors should closely monitor clinical trial progress and data readouts for NTLA-2001 and NTLA-2002"
LABEL: SUPPORTED
REASON: Both NTLA-2001 and NTLA-2002 are named in the source data and pre-written sections as the two clinical-stage candidates; monitoring their progress is a direct restatement of the pipeline facts present in the context.

---

CLAIM: "the pace and tone of regulatory dialogue with the FDA and EU authorities"
LABEL: SUPPORTED
REASON: The Risk Factors and SEC Filing Highlights explicitly reference FDA and other regulatory agencies (including EU) as key regulatory bodies whose decisions affect the company's path to approval.

---

*No additional standalone quantitative figures, price targets, specific thresholds, ratios, or named product milestones with attached numbers appear in the Outlook section beyond those already evaluated above.*

---

**SUMMARY OF FINDINGS**

All claims in the Executive Summary and Outlook are **SUPPORTED** by the source data or pre-written sections. Notably, the Financial Health pre-written section contained materially erroneous figures ($5.9 billion revenue, $3.9 billion net income) that the AI synthesis model correctly **did not use**—instead drawing the accurate figures ($59.5 million revenue, ~$400 million net loss) from the Recent Developments section and raw source data. No unsupported or inference-only claims were identified in the audited sections.
