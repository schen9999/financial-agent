# OMER — slm-full-gpu

## Metadata

ticker: OMER
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 36c1ab7c6ef9c43109074b29cc629f5896f3a51040091fe3f7398e72694cc18e
slm_endpoint: slm-gpu
slm_url: http://132.145.161.150:30880
slm_served_name: qwen3.6-35b-a3b-q4km
slm_artifact: ggml-org/Qwen3.6-35B-A3B-GGUF@baec3ebee244827cda0f4557eafa8b28f7545fa6:Qwen3.6-35B-A3B-Q4_K_M.gguf sha256:671e47e0ec53c665d048b98c3ecbfd5236b5ca9c3e02ed19fc8f81f7b85140c7
slm_build: b11347-5fc4f3c8c
slm_model_path: /models/Qwen3.6-35B-A3B-Q4_K_M.gguf
slm_model_ftype: Q4_K - Medium
slm_total_slots: 4
slm_n_ctx: 32768
slm_n_params: 34660610688
slm_model_size_bytes: 20408576512
slm_thinking: off
slm_sampling: {"planner": {"chat_template_kwargs": {"enable_thinking": false}, "dry_multiplier": 0.0, "frequency_penalty": 0.0, "max_tokens": 1024, "min_p": 0.0, "presence_penalty": 0.0, "repeat_penalty": 1.0, "temperature": 0.0, "top_k": 20, "top_n_sigma": -1.0, "top_p": 0.8, "typical_p": 1.0, "xtc_probability": 0.0}, "rag": {"chat_template_kwargs": {"enable_thinking": false}, "dry_multiplier": 0.0, "frequency_penalty": 0.0, "max_tokens": 2048, "min_p": 0.0, "presence_penalty": 0.0, "repeat_penalty": 1.0, "temperature": 0.1, "top_k": 20, "top_n_sigma": -1.0, "top_p": 0.8, "typical_p": 1.0, "xtc_probability": 0.0}, "react": {"chat_template_kwargs": {"enable_thinking": false}, "dry_multiplier": 0.0, "frequency_penalty": 0.0, "max_tokens": 1024, "min_p": 0.0, "presence_penalty": 0.0, "repeat_penalty": 1.0, "temperature": 0.0, "top_k": 20, "top_n_sigma": -1.0, "top_p": 0.8, "typical_p": 1.0, "xtc_probability": 0.0}, "section": {"chat_template_kwargs": {"enable_thinking": false}, "dry_multiplier": 0.0, "frequency_penalty": 0.0, "max_tokens": 768, "min_p": 0.0, "presence_penalty": 0.0, "repeat_penalty": 1.0, "temperature": 0.1, "top_k": 20, "top_n_sigma": -1.0, "top_p": 0.8, "typical_p": 1.0, "xtc_probability": 0.0}, "synthesis": {"chat_template_kwargs": {"enable_thinking": false}, "dry_multiplier": 0.0, "frequency_penalty": 0.0, "max_tokens": 4096, "min_p": 0.0, "presence_penalty": 0.0, "repeat_penalty": 1.0, "temperature": 0.2, "top_k": 20, "top_n_sigma": -1.0, "top_p": 0.8, "typical_p": 1.0, "xtc_probability": 0.0}}
llm_calls: 7
llm_endpoints: slm-gpu
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 689, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.167, "latency_s_total": 19.167, "parse_failure": 0, "prompt_tokens": 2632, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 389, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 11.92, "latency_s_total": 11.92, "parse_failure": 0, "prompt_tokens": 3034, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 142, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.253, "latency_s_total": 4.253, "parse_failure": 0, "prompt_tokens": 713, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 165, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.147, "latency_s_total": 5.147, "parse_failure": 0, "prompt_tokens": 707, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 191, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 8.825, "latency_s_total": 8.825, "parse_failure": 0, "prompt_tokens": 459, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 191, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 9.18, "latency_s_total": 9.18, "parse_failure": 0, "prompt_tokens": 767, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 1021, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 26.074, "latency_s_total": 26.074, "parse_failure": 0, "prompt_tokens": 1752, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "OMER",
  "company_name": "Omeros Corporation",
  "current_price": 18.75,
  "currency": "USD",
  "market_cap": 1357281024.0,
  "pe_ratio": 15.368852,
  "forward_pe": 15.243902,
  "week_52_high": 21.24,
  "week_52_low": 4.06,
  "financial_currency": "USD",
  "revenue": 38422000.0,
  "net_income": 116533000.0,
  "profit_margin_pct": 324.88,
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
    "filing_date": "2026-03-31",
    "summary": "ITEM 1A. RISK FACTORS The risks and uncertainties described below may have a material adverse effect on our business, prospects, financial condition or operating results. In addition, we may be adversely affected by risks that we currently deem immaterial or by other risks that are not currently known to us. You should carefully consider these risks before making an investment decision. The trading price of our common stock could decline due to any of these risks and you may lose all or part of your investment. In assessing the risks described below, you should also refer to the other information contained in this Annual Report on Form 10-K. Risks Related to Our Products, Product Candidates, Programs and Operations Our ability to achieve profitability is highly dependent on the commercial "
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-12",
    "summary": "ITEM 1A. RISK FACTORS We operate in an environment that involves a number of risks and uncertainties. Before making an investment decision you should carefully consider the risks described in Part I, Item 1A, \u201cRisk Factors\u201d of our Annual Report on Form 10-K for the year ended December 31, 2025, as filed with the SEC on March 31, 2026. In assessing the risk factors set forth in our Annual Report on Form 10-K for the year ended December 31, 2025, you should also refer to the other information included therein and in this Quarterly Report on Form 10-Q, including the supplemental risk factor below. In addition, we may be adversely affected by risks that we currently deem to be immaterial or by other risks that are not currently known to us. Due to these risks and uncertainties, known and unkno"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] Based on the provided text from the SEC EDGAR filings for ticker OMER, here are the key takeaways regarding the company's financial condition, risks, and operational outlook:

**Financial Position and Liquidity**
*   **Cash Reserves:** As of December 31, 2025, the company held $171.8 million in cash, cash equivalents, and short-term investments.
*   **Operating Losses:** The company has incurred cumulative operating losses since inception. For the year ended December 31, 2025, cash used in operations was $116.1 million, and the net loss was $3.4 million.
*   **Indebtedness:** The company had $70.8 million in outstanding principal on its 2029 Notes and approximately $1.2 million in finance lease obligations. The $17.1 million in 2026 Notes matured and were repaid in full as of the reporting date.
*   **Capital Needs:** The company expects to continue spending substantial amounts on clinical trials, manufacturing, commercialization of YARTEMLEA, and R&D. It may need to raise additional capital through debt, equity, or partnerships, though there is no assurance that such capital will be available on acceptable terms.

**Product Commercialization and Revenue Dependence**
*   **YARTEMLEA:** This is the company’s only commercialized product, approved by the FDA in December 2025. The company’s ability to achieve profitability is highly dependent on the commercial success of YARTEMLEA.
*   **Commercialization Risks:** Success depends on physician and patient acceptance, reimbursement policies, and the company’s limited experience in marketing, selling, and managing third-party manufacturing. Failure to commercialize YARTEMLEA successfully could materially adversely affect the business and stock price.
*   **Reimbursement Challenges:** Revenue prospects are heavily tied to coverage and reimbursement from government and private payers. There are risks regarding pricing pressures, discounts, and the time required to secure adequate reimbursement rates.

**Strategic Partnerships and Future Programs**
*   **Novo Nordisk Collaboration:** The company has a transaction with Novo Nordisk involving zaltenibart. Future payments are contingent on the successful development, regulatory approval, and commercialization of zaltenibart. If these milestones are not met or are less successful than anticipated, the company may receive little to no additional milestone or royalty payments.
*   **Preclinical Programs:** The company may have insufficient funds to advance preclinical programs to revenue-generating stages. Failure to do so could limit revenue generation through partnerships or collaborations.

**Risks Related to Indebtedness**
*   **Restrictions and Covenants:** Indebtedness limits cash flow available for operations and may restrict the ability to obtain additional financing, plan for business changes, or react to competitive disadvantages.
*   **Dilution and Default:** Conversion of notes could dilute existing stockholders. Failure to comply with financial covenants or make scheduled payments could result in default, making all indebtedness immediately payable.
*   **Refinancing Risk:** The ability to pay principal and interest depends on future performance, which is subject to factors beyond the company’s control.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Dependence on YARTEMLEA:** The company’s ability to achieve profitability is highly dependent on the commercial success of YARTEMLEA, its only commercialized product. Failure to successfully commercialize this product could materially adversely affect the business, financial condition, and stock price.
*   **Commercialization Challenges:** There are risks associated with limited experience in marketing, selling, and distributing YARTEMLEA, reliance on a limited number of manufacturers and suppliers, and potential lack of acceptance by physicians, patients, and payers.
*   **Reimbursement and Pricing Risks:** Success depends heavily on obtaining adequate coverage and reimbursement from government and private payers. Risks include delays in reimbursement, limited coverage for approved uses, reimbursement rates that do not cover costs, and pressure from payers for discounts. Additionally, pricing may be adversely affected by government programs like the Inflation Reduction Act and foreign price controls.
*   **Dependence on Novo Nordisk for Zaltenibart:** The company’s ability to realize value from zaltenibart depends entirely on Novo Nordisk’s development, regulatory approval, and commercialization efforts. Novo Nordisk controls key decisions, and the company may receive little to no milestone or royalty payments if Novo Nordisk fails to advance or commercialize the product successfully.
*   **Operating Losses and Capital Needs:** The company has incurred cumulative operating losses since inception and expects to continue incurring losses until generating significant revenue. There is a risk that the company may be unable to raise additional capital on acceptable terms when needed, which could force it to delay, scale back, or discontinue development or commercialization programs.
*   **Indebtedness:** The company has significant liabilities, including convertible senior notes and finance lease obligations, which limit cash flow available for operations and expose the company to financial risks.

## Pre-written sections (judge input)

### Financial Health

Omeros Corporation (OMER) trades at $18.75 with a market capitalization of approximately $1.36 billion, reflecting a P/E ratio of 15.37. The company reported revenue of $38.42 million and a net income of $116.53 million, resulting in an exceptional profit margin of 324.88%. This unusually high margin suggests significant non-operating income or one-time gains rather than core operational profitability from its biotechnology products. While the valuation metrics appear reasonable relative to earnings, investors should scrutinize the sustainability of these profits given the company's early-stage commercialization status.

### Recent Developments

Omeros Corporation (OMER) recently filed its Annual Report on Form 10-K on March 31, 2026, and its Quarterly Report on Form 10-Q on August 12, 2026, both of which highlight ongoing risks related to achieving sustained profitability and commercializing its product candidates. The company reported a net income of $116.53 million with a notable profit margin of 324.88%, indicating strong recent financial performance despite the inherent uncertainties in the biotechnology sector. Investors should closely monitor these filings for updates on commercial execution and risk mitigation strategies, as the stock currently trades near its 52-week high of $21.24, reflecting market confidence in its near-term prospects.

### SEC Filing Highlights
Omeros reported $171.8 million in cash and short-term investments as of December 31, 2025, while incurring a net loss of $3.4 million and using $116.1 million in operating cash. The company’s sole commercialized product, YARTEMLEA, received FDA approval in December 2025, making future profitability highly dependent on its successful commercialization and reimbursement. Outstanding debt includes $70.8 million in 2029 Notes, with the 2026 Notes having been fully repaid during the reporting period. Management anticipates substantial ongoing expenditures for clinical trials and commercialization, potentially necessitating additional capital raises through debt, equity, or partnerships. Strategic progress remains contingent on the development of zaltenibart under the Novo Nordisk collaboration, with future payments tied to specific regulatory and commercial milestones.

### Risk Factors

*   **Product Concentration and Commercialization Risk:** Profitability is heavily dependent on the commercial success of YARTEMLEA, the company’s sole commercialized product. Limited experience in marketing and distribution, alongside potential lack of acceptance by physicians, patients, and payers, poses significant execution risks.
*   **Reimbursement and Pricing Pressures:** Revenue is contingent on securing adequate coverage from government and private payers. Risks include reimbursement delays, rates that fail to cover costs, and adverse impacts from government initiatives like the Inflation Reduction Act and foreign price controls.
*   **Pipeline Dependency and Financial Sustainability:** The value of the zaltenibart pipeline relies entirely on Novo Nordisk’s development and commercialization efforts, with no guarantee of milestone or royalty payments. Concurrently, the company faces cumulative operating losses, significant indebtedness, and the risk of being unable to raise necessary capital on acceptable terms.

## Audited (Exec Summary + Outlook)

### Executive Summary
Omeros Corporation is a biotechnology company focused on developing and commercializing therapies for inflammatory diseases, currently trading with a market capitalization of approximately $1.36 billion. The stock is notable for its recent surge near the 52-week high of $21.24, driven by the December 2025 FDA approval of its sole commercialized product, YARTEMLEA, and reported net income of $116.53 million. The single most important near-term variable shaping the investment outcome is the successful commercial execution and reimbursement uptake of YARTEMLEA, which will determine whether the company can sustain its cash position of $171.8 million while funding ongoing clinical trials and debt obligations.

### Outlook
The directional outlook for Omeros is cautiously constructive, anchored by the recent regulatory milestone of YARTEMLEA’s approval and a robust liquidity position, yet tempered by the inherent execution risks of early-stage commercialization. Investors should monitor the trend of commercial adoption rates and reimbursement negotiations, as sustained uptake would validate the business model and support the current valuation, whereas slow penetration or payer resistance would weaken the thesis by increasing the likelihood of dilutive capital raises. Additionally, progress on the zaltenibart collaboration with Novo Nordisk serves as a critical secondary variable; positive regulatory or commercial milestones from this partnership would provide significant upside potential, while stagnation would highlight the company’s reliance on external partners for long-term value creation.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of approximately $1.36 billion"
LABEL: SUPPORTED
REASON: Source data lists market_cap = 1,357,281,024.0 USD, which rounds to approximately $1.36 billion.

---

CLAIM: "52-week high of $21.24"
LABEL: SUPPORTED
REASON: Source data explicitly states week_52_high = 21.24.

---

CLAIM: "recent surge near the 52-week high of $21.24"
LABEL: UNSUPPORTED
REASON: The current price is $18.75 versus the 52-week high of $21.24, a gap of approximately 11.7%; this does not arithmetically constitute trading "near" the high, and no news or filing data confirms a recent surge toward that level.

---

CLAIM: "December 2025 FDA approval of its sole commercialized product, YARTEMLEA"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state "YARTEMLEA, approved by the FDA in December 2025" and confirm it is "the company's only commercialized product."

---

CLAIM: "reported net income of $116.53 million"
LABEL: SUPPORTED
REASON: Source data lists net_income = 116,533,000.0 USD, which equals $116.53 million; this figure also appears in the pre-written Financial Health and Recent Developments sections.

---

CLAIM: "cash position of $171.8 million"
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly state "As of December 31, 2025, the company held $171.8 million in cash, cash equivalents, and short-term investments," and this figure is repeated in the SEC Filing Highlights pre-written section.

---

**OUTLOOK**

---

CLAIM: "YARTEMLEA's approval" (as a recent regulatory milestone)
LABEL: SUPPORTED
REASON: RAG SEC Highlights confirm FDA approval of YARTEMLEA in December 2025.

---

CLAIM: "zaltenibart collaboration with Novo Nordisk"
LABEL: SUPPORTED
REASON: RAG SEC Highlights and Risk Factors both explicitly name the Novo Nordisk collaboration involving zaltenibart.

---

CLAIM: "positive regulatory or commercial milestones from this partnership would provide significant upside potential"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state future payments are contingent on successful development, regulatory approval, and commercialization of zaltenibart, directly grounding this forward-looking characterization in the source data.

---

**Summary of findings:** The only claim that fails a check is the characterization of the stock as trading "near" its 52-week high. At $18.75 versus a high of $21.24, the stock is approximately 11.7% below its 52-week high — a gap that does not arithmetically support the word "near," and no source data confirms a recent directional surge toward that level. All quantitative figures cited (market cap, 52-week high, net income, cash position, YARTEMLEA approval timing, Novo Nordisk/zaltenibart partnership) are directly supported by the source data.
