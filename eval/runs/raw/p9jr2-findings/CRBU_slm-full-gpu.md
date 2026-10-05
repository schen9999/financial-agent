# CRBU — slm-full-gpu

## Metadata

ticker: CRBU
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 51b4b13184ffe88327cde67238211176c2883d885e3b7c8ada225702fc1b4e0d
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 775, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 13.769, "latency_s_total": 13.769, "parse_failure": 0, "prompt_tokens": 3103, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 539, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 11.436, "latency_s_total": 11.436, "parse_failure": 0, "prompt_tokens": 2342, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 143, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.091, "latency_s_total": 5.091, "parse_failure": 0, "prompt_tokens": 678, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 153, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.266, "latency_s_total": 5.266, "parse_failure": 0, "prompt_tokens": 672, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 186, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.631, "latency_s_total": 5.631, "parse_failure": 0, "prompt_tokens": 615, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 160, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.373, "latency_s_total": 5.373, "parse_failure": 0, "prompt_tokens": 859, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 958, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 10.621, "latency_s_total": 10.621, "parse_failure": 0, "prompt_tokens": 1670, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "CRBU",
  "company_name": "Caribou Biosciences, Inc.",
  "current_price": 1.22,
  "currency": "USD",
  "market_cap": 130793168.0,
  "forward_pe": -0.9657018,
  "week_52_high": 3.535,
  "week_52_low": 1.215,
  "revenue": 10035000.0,
  "net_income": -103403000.0,
  "profit_margin": 0.0,
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
    "filing_date": "2026-03-05",
    "summary": "Item 1A. Risk Factors. Investing in shares of our common stock involves a high degree of risk. You should carefully consider the following risks and uncertainties, together with all of the other information contained in this Annual Report on Form 10-K, including our financial statements and related notes, before making an investment decision. These disclosures reflect our beliefs and opinions as to factors that could materially and adversely affect our company and its securities in the future. References to past events are provided by way of example only and are not intended to be a complete listing or a representation as to whether or not such factors have occurred in the past or their likelihood of occurring in the future. Furthermore, the risks described below are not the only ones faci"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-13",
    "summary": "Item 1A. Risk Factors. There have been no material changes to the Risk Factors previously disclosed in Item 1A. to Part I of our Form 10-K. The risks described in our Form 10-K are not the only risks facing our company. Additional risks and uncertainties not currently known to us or that we currently deem to be immaterial also may materially adversely affect our business, financial condition, and/or operating results. Item 2. Unregistered Sales of Equity Securities, Use of Proceeds, and Issuer Purchases of Equity Securities. Unregistered Sales of Equity Securities during the Three Months Ended June 30, 2026 There were no unregistered sales of equity securities during the three months ended June 30, 2026. Item 5. Other Information. During the quarter ended June 30, 2026, none of our directo"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] Based on the provided text from the Annual Report on Form 10-K for ticker CRBU, here are the key takeaways regarding the company's financial position, risks, and operational status:

**Financial Position and Losses**
*   **Significant Operating Losses:** The company has incurred significant operating losses every year since its inception. For the years ended December 31, 2025, and 2024, net losses were $148.1 million and $149.1 million, respectively.
*   **Accumulated Deficit:** As of December 31, 2025, the company had an accumulated deficit of $596.5 million.
*   **No Revenue:** The company has not commercialized any products and has never generated revenue from product sales.
*   **Cash Position:** As of December 31, 2025, the company held $142.8 million in cash, cash equivalents, and marketable securities. This is expected to fund current operations for at least the next 12 months, though circumstances could cause these resources to be consumed faster than anticipated.

**Need for Additional Capital**
*   **Substantial Funding Requirements:** The company will need substantial additional financing to conduct its planned pivotal clinical trial for vispa-cel and to implement operating plans for its CB-011 product candidate.
*   **Current Insufficiency:** The company currently does not have sufficient funds to conduct the planned pivotal clinical trial for vispa-cel.
*   **Consequences of Funding Failure:** If additional financing is not obtained, the company may be unable to initiate the pivotal trial for vispa-cel, develop CB-011 beyond dose expansion, or complete the development and commercialization of these candidates. This could lead to delays, curtailment, or discontinuation of clinical trials.
*   **Sources of Future Capital:** The company expects to finance cash needs through equity offerings, debt financings, strategic collaborations, structured financings, or licensing arrangements. However, there is no certainty that funding will be available on acceptable terms or at all.

**Operational Status and Risks**
*   **Clinical Stage:** The company is a clinical-stage biotechnology firm formed in 2011. It has no products approved for commercial sale and has limited experience in obtaining marketing approval, manufacturing at commercial scale, or conducting sales and marketing.
*   **Product Candidates:** The company is focusing on CAR-T cell therapy product candidates, specifically vispa-cel and CB-011. Costs increase substantially as product candidates advance through clinical phases with greater numbers of patients.
*   **Profitability Uncertainty:** The company is unable to predict when it will become profitable, if ever, and may not be able to sustain profitability even if it is achieved.
*   **Dilution and Restrictions:** Raising additional capital may cause dilution to existing stockholders, restrict operations through debt covenants, or require the company to relinquish rights to its technologies or product candidates on unfavorable terms.
*   **Management Distraction:** Fundraising efforts may divert management’s attention from day-to-day activities, potentially adversely affecting the development and commercialization of product candidates.

**General Risk Factors**
*   **Early-Stage Risks:** The company’s prospects must be considered in light of the uncertainties, risks, and difficulties frequently encountered by early-stage companies. Predictions about future success may be less accurate due to the limited operating history.
*   **External Factors:** Capital consumption may accelerate due to unforeseen events, regulatory delays, pandemics, or the need to expand programs, personnel, or facilities more rapidly than planned.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Financial Position and Need for Additional Capital:** The company has incurred significant operating losses since inception, with net losses of $148.1 million in 2025 and $149.1 million in 2024, resulting in an accumulated deficit of $596.5 million as of December 31, 2025. It has never generated revenue from product sales and anticipates continued losses. The company requires substantial additional financing to conduct planned pivotal clinical trials for vispa-cel and implement operating plans; failure to obtain this financing could prevent the completion of development and commercialization.
*   **Uncertainty of Profitability and Future Losses:** The company is unable to predict the extent of future losses or when it might become profitable, if at all. Even if profitable, it may not be able to sustain or increase profitability on a quarterly or annual basis.
*   **Early Stage of Operations and Development Risks:** The company is in the early stages of product development and has not yet demonstrated the ability to obtain marketing approval, manufacture at commercial scale, or conduct sales and marketing activities. There is no guarantee that the company will ever develop or commercialize a marketable cell therapy product.
*   **High Costs and Resource Consumption:** Costs for advancing product candidates through clinical phases increase substantially, particularly for large, multicenter trials. Expenses are expected to increase significantly due to clinical trial progress, hiring, intellectual property acquisition and maintenance, regulatory approval efforts, manufacturing expansion, and potential delays or safety issues.
*   **Insufficient Current Funds:** As of December 31, 2025, the company held $142.8 million in cash, cash equivalents, and marketable securities, which is expected to fund operations for at least the next 12 months. However, these assumptions may prove incorrect, and capital resources could be consumed faster than anticipated. The company currently lacks sufficient funds to initiate the planned pivotal clinical trial for vispa-cel or develop CB-011 beyond dose expansion without raising additional funds.
*   **Commercialization Challenges:** If marketing approval is obtained, the company expects to incur significant commercialization expenses related to sales, marketing, manufacturing, and distribution, unless commercialization partners are secured.
*   **Other Operational and External Risks:** Risks include potential delays in clinical trials due to unforeseen events, pandemics, or regulatory environments; difficulties in receiving regulatory clearances; costs associated with patent prosecution and litigation; effects of competing technologies; and the diversion of management attention during fundraising efforts.

## Pre-written sections (judge input)

### Financial Health

Caribou Biosciences, Inc. (CRBU) currently trades at $1.22 with a market capitalization of approximately $130.8 million. The company reported revenue of $10.04 million but incurred a net loss of $103.4 million, resulting in a negative profit margin and an ineffective forward P/E ratio. This significant net loss highlights the firm's ongoing reliance on capital raises to fund its pre-revenue or early-stage biotechnology operations. Consequently, the stock remains near its 52-week low of $1.215, reflecting the high financial risk associated with its current burn rate and lack of profitability.

### Recent Developments

Caribou Biosciences continues to face significant financial headwinds, evidenced by a net loss of $103.4 million and a market capitalization hovering near its 52-week low of $1.22. The company’s most recent 10-K filing in March 2026 reiterated substantial risk factors, highlighting the inherent volatility and uncertainty associated with its early-stage biotechnology operations. With no material changes reported in the subsequent 10-Q, investors are navigating a period of stagnation where operational milestones have not yet translated into profitability or sustained stock appreciation. Consequently, the stock remains highly speculative, trading well below its previous highs as the market awaits clearer signs of commercial viability or strategic partnerships.

### SEC Filing Highlights
Caribou Biosciences reported a net loss of $148.1 million for the year ended December 31, 2025, maintaining its status as a pre-revenue clinical-stage company with an accumulated deficit of $596.5 million. While the firm held $142.8 million in cash and marketable securities at year-end, management explicitly stated that these resources are insufficient to fund the planned pivotal clinical trial for vispa-cel. Consequently, the company faces a substantial need for additional capital through equity or debt offerings to continue development of vispa-cel and CB-011. Failure to secure this financing could result in the delay, curtailment, or discontinuation of key clinical programs.

### Risk Factors

*   **Substantial Capital Requirements and Liquidity Risk:** The company has incurred significant operating losses and holds an accumulated deficit of $596.5 million. Current cash reserves are insufficient to fund planned pivotal clinical trials for vispa-cel or further development of CB-011, necessitating additional financing that may not be available on favorable terms or at all.
*   **Early-Stage Development and Commercialization Uncertainty:** As a pre-revenue company in the early stages of product development, there is no guarantee of obtaining regulatory approval, manufacturing at commercial scale, or successfully commercializing any cell therapy products.
*   **Unpredictable Profitability and Rising Costs:** The company is unable to predict the extent of future losses or when it might become profitable. Expenses are expected to increase substantially due to clinical trial progress, hiring, regulatory efforts, and potential delays or safety issues.

## Audited (Exec Summary + Outlook)

### Executive Summary
Caribou Biosciences is a pre-revenue clinical-stage biotechnology company specializing in CRISPR-based cell therapies, currently navigating a precarious financial position marked by an accumulated deficit of $596.5 million and a market capitalization near its 52-week low of $1.22. The stock is notable now because management has explicitly stated that existing cash reserves are insufficient to fund pivotal trials for vispa-cel, forcing the company to seek urgent external capital to avoid program discontinuation. The single most important near-term variable is the company’s ability to successfully execute a financing round on favorable terms to sustain its pipeline development.

### Outlook
The directional outlook for Caribou Biosciences is cautiously constructive but heavily contingent on execution risk surrounding capital formation and clinical progression. While the underlying CRISPR technology offers significant long-term potential, immediate headwinds from substantial liquidity constraints and the binary nature of clinical trial outcomes dominate the current narrative. Investors should closely monitor the company’s ability to secure necessary financing without excessive dilution and watch for updates on the pivotal trial for vispa-cel, as successful trial initiation and data readouts would serve as critical catalysts to strengthen the investment thesis. Conversely, any delays in funding or adverse safety signals would significantly weaken the outlook, potentially leading to program curtailment or further equity raises at depressed valuations.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

## EXECUTIVE SUMMARY

---

CLAIM: "accumulated deficit of $596.5 million"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights, RAG Risk Factors, and SEC Filing Highlights pre-written section all explicitly state the accumulated deficit as of December 31, 2025 was $596.5 million.

---

CLAIM: "market capitalization near its 52-week low of $1.22"
LABEL: UNSUPPORTED
REASON: The 52-week low is $1.215 per the source data, not $1.22; $1.22 is the current price, not the 52-week low — the claim conflates two distinct figures, making it factually incorrect as stated.

---

CLAIM: "existing cash reserves are insufficient to fund pivotal trials for vispa-cel"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states "The company currently does not have sufficient funds to conduct the planned pivotal clinical trial for vispa-cel," and this is corroborated by the SEC Filing Highlights pre-written section.

---

## OUTLOOK

No explicit quantitative figures, price targets, thresholds, ratios, metrics, or percentages appear in the Outlook section. The section contains only qualitative and directional statements (e.g., "cautiously constructive," "significant long-term potential," "excessive dilution," "depressed valuations") and named product/program references (vispa-cel). I evaluate the named product milestone references below.

---

CLAIM: "watch for updates on the pivotal trial for vispa-cel"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and Risk Factors both explicitly identify the planned pivotal clinical trial for vispa-cel as a key forward-looking milestone requiring additional financing.

---

CLAIM: "successful trial initiation and data readouts would serve as critical catalysts"
LABEL: INFERENCE
REASON: The source data confirms vispa-cel's pivotal trial is the central pending milestone and that funding is required to initiate it; the characterization of initiation and data readouts as "critical catalysts" is a direct logical derivation from those facts, requiring no additional external information.

---

CLAIM: "any delays in funding or adverse safety signals would significantly weaken the outlook, potentially leading to program curtailment"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly states that failure to obtain financing "could lead to delays, curtailment, or discontinuation of clinical trials," directly grounding this forward-looking risk statement.

---

### Summary Table

| Claim | Label |
|---|---|
| Accumulated deficit of $596.5 million | SUPPORTED |
| Market capitalization near its 52-week low of $1.22 | UNSUPPORTED |
| Cash reserves insufficient to fund pivotal trials for vispa-cel | SUPPORTED |
| Watch for updates on the pivotal trial for vispa-cel | SUPPORTED |
| Successful trial initiation and data readouts as critical catalysts | INFERENCE |
| Delays in funding or adverse safety signals could lead to program curtailment | SUPPORTED |
