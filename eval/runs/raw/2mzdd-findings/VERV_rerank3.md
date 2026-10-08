# VERV — rerank3

## Metadata

ticker: VERV
arm: rerank3
judge_prompt_version: v2
context_sha256: 49440952e6a32f797bd84d79f00cbbc39293b3050e47432f35a148c51b433520
llm_calls: 7
llm_endpoints: anthropic
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 348, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.053, "latency_s_total": 4.053, "parse_failure": 0, "prompt_tokens": 2526, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 365, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.274, "latency_s_total": 4.274, "parse_failure": 0, "prompt_tokens": 2514, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 199, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.692, "latency_s_total": 2.692, "parse_failure": 0, "prompt_tokens": 592, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 176, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.403, "latency_s_total": 2.403, "parse_failure": 0, "prompt_tokens": 585, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 186, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 1.97, "latency_s_total": 1.97, "parse_failure": 0, "prompt_tokens": 435, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 171, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 2.067, "latency_s_total": 2.067, "parse_failure": 0, "prompt_tokens": 426, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1226, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 17.584, "latency_s_total": 17.584, "parse_failure": 0, "prompt_tokens": 1862, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "VERV",
  "company_name": "N/A",
  "currency": "USD"
}

NEWS ARTICLES:
[]

SEC FILING SUMMARIES:
{
  "10-K": {
    "form_type": "10-K",
    "filing_date": "2025-02-27",
    "summary": "Item 1A. Risk Factors. Our future operating results could differ materially from the results described in this Annual Report on Form 10-K due to the risks and uncertainties described below. You should consider carefully the following information about risks below in evaluating our business. If any of the following risks actually occur, our business, financial conditions, results of operations and future growth prospects would likely be materially and adversely affected. In these circumstances, the market price of our common stock would likely decline. In addition, we cannot assure investors that our assumptions and expectations will prove to be correct. Important factors could cause our actual results to differ materially from those indicated or implied by forward-looking statements. See p"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2025-05-14",
    "summary": "Item 1A. Risk Factors 26 Item 2. Unregistered Sales of Equity Securities and Use of Proceeds 91 Item 5. Other Information 91 Item 6. Exhibits 92 Signatures 93 Part I \u2500 Financi al Information Item 1. Financi al Statements Verve Therapeutics, Inc. Condensed consolidat ed balance sheets (in thousands, except share and per share amounts) (unaudited) March 31, 2025 December 31, 2024 Assets Current assets: Cash and cash equivalents $ 96,554 $ 172,560 Marketable securities 400,523 351,721 Collaboration receivable 1,399 3,255 Prepaid expenses and other current assets 13,174 15,215 Total current assets 511,650 542,751 Property and equipment, net 18,457 18,644 Restricted cash 4,774 4,774 Operating lease right-of-use assets 76,217 78,082 Other long term assets 3,065 3,141 Total assets $ 614,163 $ 647"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] # Key Takeaways from VERV's SEC Filings

Based on the available information, here are the primary points:

## Financial Position
- The company has accumulated significant losses since inception, with net losses of $198.7 million in 2024, $200.1 million in 2023, and $157.4 million in 2022
- As of December 31, 2024, the accumulated deficit reached $743.0 million
- No revenue has been generated from product sales to date

## Development Status
- The company has no approved products currently on the market
- Clinical development of the first product candidate began in 2022
- Multiple clinical trials are ongoing, including Heart-2 Phase 1b for VERVE-102 and Pulse-1 Phase 1b for VERVE-201
- Years of development remain before any product candidate may be ready for commercialization

## Funding and Capital Needs
- Operations have been financed through private placements, public stock offerings, and collaboration agreements (including a Research and Collaboration Agreement with Eli Lilly and Company effective July 2023)
- Substantial additional funding will be required to continue operations
- No credit facility or committed sources of capital currently exist
- The company may be forced to delay, reduce, or eliminate programs if unable to raise capital

## Future Outlook
- Significant operating losses are expected to continue for the foreseeable future
- Profitability is uncertain and may never be achieved
- Expenses are anticipated to increase substantially as clinical trials advance and development programs expand

RAG — RISK FACTORS:
[From Pinecone cache] # Primary Risk Factors Disclosed

The company discloses several significant risk factors, with the primary ones being:

## Financial Position and Capital Needs

- **Substantial accumulated losses**: The company has incurred net losses of $198.7 million, $200.1 million, and $157.4 million for 2024, 2023, and 2022 respectively, with an accumulated deficit of $743.0 million as of December 31, 2024.

- **No approved products or revenue**: The company has no products approved for sale and has never generated revenue from product sales, with no assurance of achieving profitability.

- **Ongoing losses expected**: Significant operating losses are anticipated for the foreseeable future, with operating expenses and net losses expected to fluctuate significantly.

## Funding Requirements

- **Need for substantial additional capital**: The company requires significant additional funding to continue operations, particularly for clinical trials, research and development, and potential commercialization efforts.

- **No committed funding sources**: The company currently lacks a credit facility or any committed sources of capital, creating uncertainty about its ability to fund operations.

- **Risk of program delays or termination**: If unable to raise capital on acceptable terms, the company may be forced to delay, reduce, or eliminate research and development programs or commercialization efforts.

## Product Development Challenges

- **Early-stage development**: The company has not yet completed a clinical trial of any product candidate, with many years potentially required before commercialization.

- **Uncertain commercialization success**: Success requires effectiveness in numerous challenging activities including completing trials, obtaining regulatory approvals, manufacturing, marketing, and achieving market acceptance.

## Pre-written sections (judge input)

### Financial Health

Verve Therapeutics (VERV) reported total assets of $614.2 million as of March 31, 2025, with a strong cash position of $96.6 million and marketable securities of $400.5 million, indicating solid liquidity. However, the company's cash reserves declined by $76 million sequentially from December 2024, suggesting ongoing operational burn typical of clinical-stage biopharmaceutical companies. As a pre-revenue or early-stage therapeutic firm, traditional valuation metrics like P/E ratio and profit margin are not applicable; the company's financial health is primarily assessed through cash runway and burn rate. The recent 10-Q filing emphasizes significant risk factors that could materially impact future operations and stock performance. Investors should monitor cash burn rates and milestone achievements closely, as the company's viability depends on successful clinical development and potential partnerships or financing.

### Recent Developments

Verve Therapeutics filed its Q1 2025 10-Q on May 14, 2025, revealing a cash position of $96.6 million as of March 31, 2025, down from $172.6 million at year-end 2024, indicating accelerated cash burn as the company advances its pipeline. The company maintains $400.5 million in marketable securities, providing a runway for ongoing operations and clinical development. The February 2025 10-K filing highlighted material risk factors that could adversely affect business operations and stock performance, suggesting investors should carefully evaluate execution risks. With cash declining significantly in the first quarter, investors should monitor upcoming milestones and partnership developments to assess the sustainability of the company's current burn rate and path to value creation.

### SEC Filing Highlights

Verve Therapeutics is a pre-revenue clinical-stage biotech company with accumulated losses of $743.0 million as of December 31, 2024, posting net losses of $198.7 million in 2024 alone. The company has no approved products and is advancing multiple clinical-stage candidates, including VERVE-102 and VERVE-201, with years of development remaining before potential commercialization. Operations are funded through equity offerings and strategic partnerships, including a research collaboration with Eli Lilly, though substantial additional capital will be required to continue development. Management expects significant operating losses to persist for the foreseeable future, with no clear path to profitability, and the company faces material risks if unable to secure future funding.

### Risk Factors

- **Severe financial burn with no revenue**: VERV has accumulated losses of $743.0 million as of December 31, 2024, with no approved products or product revenue. The company burned $198.7 million in 2024 alone and expects significant ongoing losses for the foreseeable future.

- **Critical funding dependency**: The company lacks committed capital sources and requires substantial additional funding to continue operations. Inability to raise capital on acceptable terms could force delays, reductions, or termination of R&D programs and commercialization efforts.

- **Early-stage development with uncertain path to commercialization**: VERV has not completed clinical trials for any product candidate, with many years potentially required before commercialization. Success depends on navigating numerous uncertain challenges including regulatory approval, manufacturing scale-up, and market acceptance.

## Audited (Exec Summary + Outlook)

### Executive Summary
Verve Therapeutics is a clinical-stage biopharmaceutical company advancing gene-editing therapies for cardiovascular disease, with no approved products but a meaningful asset base of $614.2 million in total assets and $400.5 million in marketable securities supporting its pipeline. The stock is notable now because accelerating cash burn — with cash declining from $172.6 million to $96.6 million in a single quarter — is sharpening investor focus on how long the company can sustain operations before requiring additional capital, even as its Eli Lilly partnership and dual pipeline candidates (VERVE-102 and VERVE-201) provide strategic credibility. The single most important near-term variable is clinical trial progress: meaningful data readouts from either lead candidate would either validate the platform and improve the company's financing position, or, if disappointing, materially increase the risk of dilutive capital raises or program curtailment.

### Outlook
The directional outlook for VERV is **cautious**, reflecting the structural realities of a pre-revenue, high-burn clinical-stage company with no approved products and an uncertain timeline to commercialization. The primary tailwind is the scientific and strategic credibility of the gene-editing platform, underscored by the Eli Lilly research collaboration, which provides both validation and a potential non-dilutive funding avenue. Headwinds are significant: the accelerating quarterly cash burn raises near-term financing risk, and the company's dependence on equity markets or partnership expansions to fund operations introduces meaningful dilution or execution risk. Investors should watch the pace and direction of clinical data from VERVE-102 and VERVE-201, the trajectory of quarterly cash consumption relative to the marketable securities buffer, any expansion or deepening of the Eli Lilly partnership, and the company's ability to access capital on favorable terms. The thesis would strengthen on positive clinical readouts, a broadened strategic partnership, or a moderation in burn rate; it would weaken on clinical setbacks, an inability to raise capital without severe dilution, or a deterioration in the broader biotech funding environment.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, and forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "a meaningful asset base of $614.2 million in total assets"
LABEL: SUPPORTED
REASON: The 10-Q summary states total assets of $614,163 thousand (≈$614.2 million) as of March 31, 2025, and the Financial Health pre-written section confirms "$614.2 million."

---

CLAIM: "$400.5 million in marketable securities"
LABEL: SUPPORTED
REASON: The 10-Q summary lists marketable securities of $400,523 thousand (≈$400.5 million) as of March 31, 2025, confirmed in both the Financial Health and Recent Developments sections.

---

CLAIM: "cash declining from $172.6 million to $96.6 million in a single quarter"
LABEL: SUPPORTED
REASON: The 10-Q source data shows cash and cash equivalents of $96,554 thousand at March 31, 2025, and $172,560 thousand at December 31, 2024; the decline is $76.0 million in Q1 2025, consistent with the claim of a single-quarter drop from $172.6M to $96.6M.

---

CLAIM: "its Eli Lilly partnership"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and SEC Filing Highlights pre-written section both explicitly reference a Research and Collaboration Agreement with Eli Lilly and Company.

---

CLAIM: "dual pipeline candidates (VERVE-102 and VERVE-201)"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly names "Heart-2 Phase 1b for VERVE-102 and Pulse-1 Phase 1b for VERVE-201," and the SEC Filing Highlights section confirms both candidates.

---

**OUTLOOK**

---

CLAIM: "pre-revenue, high-burn clinical-stage company with no approved products"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors sections both confirm no approved products, no product revenue, and net losses of $198.7 million in 2024 (high burn); the SEC Filing Highlights section also states "pre-revenue clinical-stage biotech."

---

CLAIM: "the Eli Lilly research collaboration, which provides both validation and a potential non-dilutive funding avenue"
LABEL: INFERENCE
REASON: The Eli Lilly collaboration is confirmed in the source data; characterizing it as a "non-dilutive funding avenue" is a reasonable inference from the nature of collaboration agreements (as opposed to equity raises), but the source data does not explicitly describe it as non-dilutive or as a funding avenue — it is derivable from the general structure of collaboration agreements without any additional absent facts, making it an inference rather than an unsupported claim.

---

CLAIM: "the accelerating quarterly cash burn"
LABEL: INFERENCE
REASON: The source data shows a $76 million cash decline in Q1 2025 alone; the Financial Health section notes "cash reserves declined by $76 million sequentially," and the Recent Developments section calls it "accelerated cash burn" — the directional characterization of acceleration is an inference from the single quarter's data point, as no prior quarterly burn figure is provided in the source to confirm the rate is accelerating versus prior quarters.

---

CLAIM: "the trajectory of quarterly cash consumption relative to the marketable securities buffer"
LABEL: SUPPORTED
REASON: Both the $400.5 million marketable securities figure and the quarterly cash burn dynamic are present in the source data; this is a qualitative watch-item referencing confirmed figures.

---

CLAIM: "any expansion or deepening of the Eli Lilly partnership"
LABEL: SUPPORTED
REASON: The Eli Lilly partnership is confirmed in the source data; this is a forward-looking watch-item referencing a confirmed existing relationship.

---

CLAIM: "clinical data from VERVE-102 and VERVE-201"
LABEL: SUPPORTED
REASON: Both VERVE-102 and VERVE-201 are explicitly named in the RAG SEC Highlights and SEC Filing Highlights sections as ongoing clinical-stage candidates.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | $614.2 million in total assets | SUPPORTED |
| 2 | $400.5 million in marketable securities | SUPPORTED |
| 3 | Cash declining from $172.6M to $96.6M in a single quarter | SUPPORTED |
| 4 | Eli Lilly partnership | SUPPORTED |
| 5 | Dual pipeline candidates VERVE-102 and VERVE-201 | SUPPORTED |
| 6 | Pre-revenue, no approved products, high-burn | SUPPORTED |
| 7 | Eli Lilly collaboration as non-dilutive funding avenue | INFERENCE |
| 8 | Accelerating quarterly cash burn | INFERENCE |
| 9 | Quarterly cash consumption vs. marketable securities buffer | SUPPORTED |
| 10 | Expansion/deepening of Eli Lilly partnership (watch-item) | SUPPORTED |
| 11 | Clinical data from VERVE-102 and VERVE-201 (watch-item) | SUPPORTED |
