# NTLA — local-model

## Metadata

ticker: NTLA
arm: local-model
judge_prompt_version: v2
context_sha256: 3bea8b5997475b8c4cb09c79cbd67457af8fa1beab2b2f9d3f5455d88913d789
local_model_served_name: qwen2.5-1.5b-instruct
local_model_dir: qwen2.5-1.5b-instruct
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
[From Pinecone cache] # Key Takeaways from the Risk Factors Disclosure

Based on the available information from the 10-K filing, here are the primary risk factors disclosed:

## Clinical Development Challenges
- CRISPR genome editing technology is relatively new with largely unproven therapeutic utility in humans
- No in vivo genome editing therapy has been approved in the U.S., EU, or other key jurisdictions
- The company faces significant challenges in developing safe delivery methods, optimizing efficacy and specificity, and demonstrating safety and potency of CRISPR-based products

## Regulatory and Development Uncertainties
- Regulatory agencies have very limited experience with CRISPR-based therapeutics, particularly in vivo therapies, which may require additional testing and data
- Clinical trials may fail to demonstrate safety or efficacy, requiring additional studies or program termination
- Regulatory requirements may be revised, potentially delaying or preventing approval of product candidates

## Market Adoption Risks
- Public perception and media coverage of safety or efficacy issues could discourage clinical trial participation and physician/patient acceptance
- Healthcare providers and payors are often slow to adopt new technologies, particularly those requiring additional training and upfront costs
- Certain patients may not be candidates for these therapies due to health conditions or genetic profiles

## Operational and Financial Risks
- All programs remain in discovery, preclinical, or clinical stages with uncertain timelines and outcomes
- Preclinical and clinical testing is expensive, time-consuming, and difficult to design and implement
- The company may face challenges in manufacturing, supply chain management, and establishing sales and marketing capabilities

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several primary risk factors related to its business:

## Clinical Development and Technology Risks
- CRISPR genome editing technology has only recently been clinically validated for human therapeutic use, and in vivo CRISPR-based therapies remain largely unproven
- No genome editing in vivo therapy has been approved in the U.S., EU, or other key jurisdictions
- The approaches for developing CRISPR-based therapeutics are unproven and may never lead to marketable products
- Success requires solving multiple technical challenges, including safe delivery of therapeutic agents to target cells and optimizing efficacy and specificity

## Regulatory and Approval Challenges
- Clinical development is lengthy, expensive, and uncertain in outcome
- Regulatory agencies have very limited or no experience with CRISPR-based therapeutics, particularly in vivo therapies, which may require additional testing and delay development
- Regulatory authorities may impose stricter requirements for CRISPR products compared to traditional therapies
- There is no guarantee that clinical trials will begin or be completed on schedule

## Market Adoption and Public Perception Risks
- Public perception and media coverage of safety or efficacy issues may discourage clinical trial participation and patient/physician acceptance
- Ethical concerns related to genome editing and CRISPR may adversely influence adoption
- Physicians and healthcare providers are often slow to adopt new technologies and may view these therapies as too complex or risky
- Certain patients may not be candidates for the therapies due to health conditions or genetic profiles

## Operational and Manufacturing Risks
- Challenges in obtaining sufficient commercial manufacturing capacity
- Supply or quality issues with product candidates and necessary materials
- Difficulties in sourcing preclinical, clinical, and commercial supplies across different jurisdictions

## Pre-written sections (judge input)

### Financial Health

**Price:** $12.33 per share as of [insert date]

**Market Cap:** $17,277,620,480

**P/E Ratio:** -4.74 (Forward)

**Revenue:** $59,506,000

**Net Income:** -$3,999,750,080

**Profit Margin:** 0%

The company's current valuation is relatively low compared to its historical performance, indicated by the negative forward PE ratio (-4.74), suggesting potential value appreciation opportunities. Despite significant losses, the company has maintained a strong focus on research and development, which is crucial for advancing its pipeline of biologics therapies. However, investors should remain cautious due to the substantial net income loss, indicating ongoing operational challenges.

### Recent Developments

Intellia Therapeutics has not announced major clinical or commercial milestones in recent news flow, though the company filed its 2025 10-K in February 2026 and most recent 10-Q in August 2026, both emphasizing significant risk factors inherent to its gene-editing pipeline. The company continues to operate as a pre-commercial biotech with negative net income of approximately $400 million annually and minimal revenue of $59.5 million, indicating it remains in the development phase with substantial cash burn. With the stock trading at $12.33—down significantly from its 52-week high of $28.25—investors should monitor upcoming clinical trial data and regulatory decisions on its NTLA-2002 and other CRISPR-based programs, as these will be critical catalysts for valuation. The lack of recent positive news combined with the company's pre-profitability status suggests investors should expect continued volatility until meaningful clinical or regulatory progress is demonstrated.

### SEC Filing Highlights

Intellia Therapeutics faces significant clinical and regulatory uncertainties as a CRISPR-based therapeutic company with no approved in vivo genome editing therapies to date. The company's pipeline remains in discovery through clinical stages, with all programs dependent on demonstrating safety and efficacy in human trials—a challenge complicated by limited regulatory precedent for CRISPR therapeutics. Key operational risks include manufacturing scalability, high development costs, and potential delays from evolving regulatory requirements. Market adoption risks are substantial, given healthcare providers' cautious approach to novel gene-editing technologies and public perception concerns around CRISPR safety. Despite these headwinds, the company continues advancing its lead programs while navigating the inherent uncertainties of pioneering a new therapeutic modality.

### Risk Factors

1. **Clinical Development and Technology Risks**
   - CRISPR genome editing technology has only recently been clinically validated for human therapeutic use, and in vivo CRISPR-based therapies remain largely unproven.
   - No genome editing in vivo therapy has been approved in the U.S., EU, or other key jurisdictions.
   - The approaches for developing CRISPR-based therapeutics are unproven and may never lead to marketable products.
   - Success requires solving multiple technical challenges, including safe delivery of therapeutic agents to target cells and optimizing efficacy and specificity.

2. **Regulatory and Approval Challenges**
   - Clinical development is lengthy, expensive, and uncertain in outcome.
   - Regulatory agencies have very limited or no experience with CRISPR-based therapeutics, particularly in vivo therapies, which may require additional testing and delay development.
   - Regulatory authorities may impose stricter requirements for CRISPR products compared to traditional therapies.
   - There is no guarantee that clinical trials will begin or be completed on schedule.

3. **Market Adoption and Public Perception Risks**
   - Public perception and media coverage of safety or efficacy issues may discourage clinical trial participation and patient/physician acceptance.
   - Ethical concerns related to genome editing and CRISPR may adversely influence adoption.
   - Physicians and healthcare providers are often slow to adopt new technologies and may view these therapies as too complex or risky.
   - Certain patients may not be candidates for the therapies due to health conditions or genetic profiles.

## Audited (Exec Summary + Outlook)

### Executive Summary
Intellia Therapeutics is a clinical-stage biotechnology company pioneering in vivo CRISPR-based genome editing therapies, operating in a field where no such therapy has yet received regulatory approval in the U.S., EU, or other major jurisdictions, and generating $59,506,000 in revenue against a backdrop of substantial ongoing losses. The stock is notable now because it trades at $12.33 per share—well below its 52-week high of $28.25—reflecting a combination of pre-commercial status, significant cash burn, and an absence of recent positive clinical or regulatory catalysts. The single most important near-term variable shaping the investment outcome is the clinical trial data and regulatory trajectory for NTLA-2002 and the company's other lead CRISPR programs, as meaningful progress there represents the clearest path to a revaluation of the stock.

### Outlook
The directional lean on Intellia Therapeutics is **cautious**, with the potential to become constructive if specific clinical and regulatory conditions are met. The primary tailwind is the transformative long-term potential of in vivo CRISPR gene editing as a therapeutic modality—if validated, it could address diseases with limited or no existing treatment options, and Intellia is among the earliest movers in this space. However, the headwinds are substantial and immediate: the company is pre-commercial, carries significant ongoing cash burn, operates in a regulatory environment with limited precedent for its technology, and has seen its stock decline sharply from its 52-week high without a clear near-term catalyst to reverse that trend. Investors should watch the clinical readout cadence and data quality for NTLA-2002 and other pipeline programs most closely, as positive safety and efficacy signals would be the most direct catalyst for a shift in sentiment; conversely, trial setbacks, safety signals, or regulatory delays would likely deepen the current bearish pressure. Beyond clinical data, key variables to monitor include the pace at which regulatory agencies develop clearer frameworks for in vivo CRISPR therapies, the company's ability to manage cash burn and extend its operational runway, and broader shifts in public and physician perception of gene-editing technologies. The thesis strengthens meaningfully if clinical data demonstrate compelling proof-of-concept and regulators signal a constructive path forward; it weakens further if the pipeline stalls, manufacturing challenges emerge, or the regulatory environment becomes more restrictive.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically identify every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections, then evaluate each one.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "generating $59,506,000 in revenue"
LABEL: SUPPORTED
REASON: The raw source data lists revenue as $59,506,000, and the pre-written Financial Health section confirms "$59,506,000" in revenue.

---

CLAIM: "trades at $12.33 per share"
LABEL: SUPPORTED
REASON: The raw source data lists current_price as $12.33, confirmed in the pre-written Financial Health section ("$12.33 per share").

---

CLAIM: "well below its 52-week high of $28.25"
LABEL: SUPPORTED
REASON: The raw source data lists week_52_high as $28.25, and $12.33 is arithmetically well below $28.25 (approximately 56% below), so both the figure and the positional claim are verified.

---

CLAIM: "NTLA-2002 and the company's other lead CRISPR programs" (as a named product milestone/forward-looking variable)
LABEL: SUPPORTED
REASON: NTLA-2002 is explicitly named in the pre-written Recent Developments section as a critical catalyst program ("its NTLA-2002 and other CRISPR-based programs").

---

**OUTLOOK**

---

CLAIM: "NTLA-2002 and other pipeline programs" (as named watch-items for clinical readout)
LABEL: SUPPORTED
REASON: NTLA-2002 is explicitly named in the pre-written Recent Developments section as a key program to monitor for clinical trial data and regulatory decisions.

---

*(No additional specific quantitative figures, price targets, thresholds, ratios, percentages, or forward-looking numbers appear in the Outlook section beyond those already evaluated above. All other claims in the Outlook are qualitative directional statements — e.g., "cautious," "transformative long-term potential," "earliest movers," "sharply from its 52-week high" — that do not constitute specific quantitative or named-milestone claims requiring audit under the defined scope. The 52-week high directional reference in the Outlook ("seen its stock decline sharply from its 52-week high") does not introduce a new figure and is covered by the check above.)*

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | Revenue of $59,506,000 | SUPPORTED |
| 2 | Stock price of $12.33 per share | SUPPORTED |
| 3 | 52-week high of $28.25 | SUPPORTED |
| 4 | $12.33 is "well below" the 52-week high of $28.25 | SUPPORTED |
| 5 | NTLA-2002 named as lead program / near-term variable | SUPPORTED |
| 6 | NTLA-2002 named as clinical readout watch-item in Outlook | SUPPORTED |
