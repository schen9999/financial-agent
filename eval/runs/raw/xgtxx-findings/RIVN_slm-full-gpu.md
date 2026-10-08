# RIVN — slm-full-gpu

## Metadata

ticker: RIVN
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 9aac4cb2d7ab97f3d70ebd905474a424d5dd17e8e65da877d689a464a36893ba
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 788, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 23.381, "latency_s_total": 23.381, "parse_failure": 0, "prompt_tokens": 2412, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 297, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 10.469, "latency_s_total": 10.469, "parse_failure": 0, "prompt_tokens": 2401, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 133, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 16.494, "latency_s_total": 16.494, "parse_failure": 0, "prompt_tokens": 643, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 121, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 20.271, "latency_s_total": 20.271, "parse_failure": 0, "prompt_tokens": 637, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 156, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 15.204, "latency_s_total": 15.204, "parse_failure": 0, "prompt_tokens": 371, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 171, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 22.51, "latency_s_total": 22.51, "parse_failure": 0, "prompt_tokens": 870, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 880, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 28.753, "latency_s_total": 28.753, "parse_failure": 0, "prompt_tokens": 1544, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "RIVN",
  "company_name": "Rivian Automotive, Inc.",
  "current_price": 14.34,
  "currency": "USD",
  "market_cap": 20762320896.0,
  "forward_pe": -8.241758,
  "week_52_high": 22.69,
  "week_52_low": 12.39,
  "financial_currency": "USD",
  "revenue": 5882999808.0,
  "net_income": -3232999936.0,
  "profit_margin_pct": -54.95,
  "dividend_yield": 0.0,
  "sector": "Consumer Cyclical",
  "industry": "Auto Manufacturers"
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
    "filing_date": "2026-02-12",
    "summary": "Item 1A. Risk Factors. Software and Services Segment Complementing our vehicles, we provide a suite of value-added software and services which we expect to continue to generate long-term brand loyalty while also creating a recurring revenue stream across the vehicle lifecycle. These services include vehicle electrical architecture and software development services provided by the Joint Venture, Autonomy+, remarketing, vehicle repair and maintenance, charging, software subscriptions, vehicle accessories, financing, insurance, and more, as described below. \u2022 Joint Venture. Rivian and Volkswagen Group have formed an equally-owned joint venture as a separate legal entity to create next-generation electrical architecture and best-in-class software technology. The Joint Venture focuses on softwa"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-07-30",
    "summary": "Item 1A. Risk Factors Our business is subject to various risks and uncertainties, including those described below, that may cause actual results to differ materially from historical performance or projected future performance expressed in forward-looking statements made by us. We encourage you to consider carefully the risk factors described below in evaluating the information in this Form 10-Q as the outcome of one or more of these risks and uncertainties could have a material adverse effect on our financial condition, results of operations, and cash flows as well as on our reputation, business, growth, future prospects, and ability to accomplish our strategic objectives. Risks Related to Our Business We are a growth stage company with limited operating history and a history of losses. We"
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] Based on the provided context from Rivian Automotive, Inc.'s SEC filings, here are the key takeaways regarding operations, strategy, and regulatory compliance:

**Seasonality and Revenue Drivers**
*   The automotive industry typically sees higher revenue in spring and summer. Commercial vehicle deliveries often decline in the final months of the year as customers focus on holiday logistics rather than fleet expansion, potentially leading to higher finished goods inventory.
*   In Q4 2025, Rivian delivered more Electric Delivery Vehicles (EDVs) than seasonally typical due to supplier constraints earlier in the year.
*   Revenue is influenced by new product launch timing and government incentives. For instance, the expiration of federal EV tax credits on September 30, 2025, caused a pull-forward of deliveries into Q3 and a corresponding decline in Q4 2025.

**Competition and Market Position**
*   Primary competitive factors include talent, culture, technological innovation, product performance, customer experience, brand differentiation, pricing, total cost of ownership (TCO), and manufacturing scale.
*   Competition extends beyond traditional OEMs and dealers to include third parties involved in vehicle remarketing, repair, maintenance, charging, software, autonomous driving, and fleet management.
*   Rivian aims to compete effectively through product/brand differentiation, vertically-integrated technology, and direct-to-customer relationships.

**Software and Services Segment**
*   Rivian provides value-added software and services to generate recurring revenue and brand loyalty. Key offerings include:
    *   **Joint Venture:** An equally-owned entity with Volkswagen Group focused on next-generation electrical architecture and software technology.
    *   **Autonomy+:** Advanced driver assistance features. The Universal Hands Free feature was expanded to over 3.5 million miles of roads in North America via an OTA update in December 2025. Fees for these features are expected to begin in April 2026.
    *   **Charging:** The Rivian Adventure Network offers DC fast chargers, with over 95% of the network open to non-Rivian EVs.
    *   **Software Subscriptions:** Includes Connect+ for consumers and FleetOS, a centralized fleet management platform for commercial vehicles.
    *   **Other Services:** Includes vehicle repair and maintenance (via physical centers, mobile vehicles, and partners), remarketing, insurance, financing, and the Rivian Gear Shop.

**Manufacturing and Production**
*   Vehicles are currently manufactured at the Normal Factory in Illinois, which has an annual installed capacity of up to 215,000 vehicles.
*   The capacity split is expected to be up to 155,000 R2 vehicles, 85,000 R1 vehicles, and 65,000 Rivian Commercial Vans.
*   Customer deliveries for the R2 platform are expected to begin in the second quarter of 2026.

**Regulatory and Environmental Compliance**
*   Operations are subject to stringent federal, state, and local laws regarding product safety, environmental protection, and occupational health. Non-compliance can result in penalties, remedial obligations, or operational injunctions.
*   **NHTSA Compliance:** All current vehicles (R1T, R1S, EDV, and Rivian Commercial Van) are fully compliant with Federal Motor Vehicle Safety Standards, CAFE standards, and other NHTSA requirements without needing exemptions.
*   **EPA Compliance:** The Clean Air Act requires an EPA Certificate of Conformity and a California Executive Order for operations.
*   **Disclosure:** The Automobile Information and Disclosure Act requires disclosure of MSRP, optional equipment, and pricing, along with optional fuel economy and crash test ratings.

RAG — RISK FACTORS:
[From Pinecone cache] Based on the provided context, the primary risk factors disclosed include:

*   **Raw Material Access:** There are specific risks related to the company's access to raw materials, which are detailed in Part I, Item 1A.
*   **Regulatory Compliance:** Operations, properties, products, and services are subject to stringent federal, state, and local laws regarding product safety, environmental protection, occupational health and safety, and emissions. Failure to comply with these regulations can result in administrative, civil, and criminal penalties, investigatory and remedial obligations, and orders enjoining operations. This includes compliance with National Highway Traffic Safety Administration (NHTSA) Safety Standards, Federal Corporate Average Fuel Economy (CAFE) standards, and Clean Air Act requirements.
*   **Seasonality and Demand Fluctuations:** The automotive industry experiences higher revenue in spring and summer, with commercial vehicle deliveries typically lower in the final months of the year. Additionally, revenues are influenced by the timing of new product launches and changes in government incentives, such as the expiration of federal EV tax credits, which can cause significant fluctuations in consumer demand.
*   **Competition:** The company faces competition from millions of traditional internal combustion engine (ICE) vehicles and electric vehicles (EVs) in both consumer and commercial markets. Competition also extends to downstream entities such as vehicle remarketers, repair and maintenance providers, charging and software providers, autonomous vehicle software developers, and traditional fleet management companies.

## Pre-written sections (judge input)

### Financial Health

Rivian Automotive, Inc. (RIVN) currently trades at $14.34 with a market capitalization of approximately $20.76 billion. The company has generated $5.88 billion in revenue but remains unprofitable, reporting a net loss of $3.23 billion and a negative profit margin of -54.95%. Consequently, the forward P/E ratio is negative, reflecting the firm's ongoing challenges in achieving earnings stability. While the company is expanding its recurring revenue streams through software and services, it continues to operate as a growth-stage entity with a history of losses.

### Recent Developments

Rivian filed its 2026 10-K on February 12, highlighting a strategic joint venture with Volkswagen Group to develop next-generation electrical architecture and software, aiming to create recurring revenue streams and enhance long-term brand loyalty. The company continues to report significant net losses, with a profit margin of -54.95%, underscoring the challenges inherent in its growth-stage status and limited operating history. Investors should monitor the execution of this software-centric partnership as a critical factor in improving margins and achieving sustainable profitability amidst current financial headwinds.

### SEC Filing Highlights
Rivian’s Q4 2025 revenue was significantly impacted by the expiration of federal EV tax credits, which triggered a delivery pull-forward into Q3 and a subsequent seasonal decline. The company is preparing for the R2 platform launch, with customer deliveries scheduled for Q2 2026, while its Normal Factory maintains an annual capacity of up to 215,000 vehicles. To drive recurring revenue, Rivian is expanding its software and services segment, including the upcoming monetization of its Autonomy+ features in April 2026 and a strategic joint venture with Volkswagen on next-generation electrical architecture. Additionally, the Rivian Adventure Network continues to broaden access, with over 95% of its DC fast chargers now open to non-Rivian EVs.

### Risk Factors

*   **Regulatory Compliance and Safety:** Operations are subject to stringent federal, state, and local laws regarding product safety, emissions, and environmental protection; non-compliance with standards such as NHTSA Safety Standards and CAFE regulations can result in significant penalties and operational restrictions.
*   **Demand Volatility and Seasonality:** Revenue is heavily influenced by seasonal trends, the timing of new product launches, and changes in government incentives, such as the expiration of federal EV tax credits, leading to potential fluctuations in consumer demand.
*   **Intense Market Competition:** The company faces fierce competition from millions of traditional internal combustion engine vehicles and other EVs, as well as downstream entities including charging infrastructure providers, software developers, and fleet management companies.

## Audited (Exec Summary + Outlook)

### Executive Summary
Rivian Automotive, Inc. operates as a growth-stage electric vehicle manufacturer with a market capitalization of approximately $20.76 billion, though it currently faces significant profitability challenges with a net loss of $3.23 billion. The stock is notable now as the company navigates the transition from its initial launch phase toward scalable production and recurring revenue generation through strategic partnerships and software monetization. The single most important near-term variable shaping the investment outcome is the successful execution of the upcoming R2 platform launch and the integration of the Volkswagen joint venture to drive long-term margin expansion.

### Outlook
The directional outlook for Rivian is cautiously constructive, anchored by the potential for structural margin improvement through its software-centric strategy and the Volkswagen joint venture, which aims to reduce costs and enhance recurring revenue. Key variables to monitor include the execution timeline for the R2 platform launch, the uptake of monetized software features like Autonomy+, and the broader impact of seasonal demand shifts and regulatory changes on delivery volumes. The thesis would be strengthened if the company demonstrates consistent progress toward gross margin expansion via the new electrical architecture and successful scaling of the Adventure Network; conversely, persistent net losses, delays in the R2 rollout, or intensified price competition in the mid-market EV segment would weaken the investment case.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of approximately $20.76 billion"
LABEL: SUPPORTED
REASON: The source data lists market_cap as $20,762,320,896.0, which rounds to approximately $20.76 billion.

---

CLAIM: "net loss of $3.23 billion"
LABEL: SUPPORTED
REASON: The source data lists net_income as -$3,232,999,936.0, which rounds to a net loss of $3.23 billion.

---

CLAIM: "R2 platform launch"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and the SEC Filing Highlights pre-written section both explicitly reference the R2 platform launch with customer deliveries scheduled for Q2 2026.

---

CLAIM: "Volkswagen joint venture"
LABEL: SUPPORTED
REASON: The 10-K summary, RAG SEC Highlights, and pre-written sections all explicitly describe an equally-owned joint venture between Rivian and Volkswagen Group focused on next-generation electrical architecture and software technology.

---

**OUTLOOK**

---

CLAIM: "Volkswagen joint venture, which aims to reduce costs and enhance recurring revenue"
LABEL: INFERENCE
REASON: The source data explicitly states the JV aims to create "next-generation electrical architecture and best-in-class software technology" and generate "recurring revenue streams," and cost reduction is a reasonable inference from architectural standardization, but "reduce costs" is not explicitly stated in the source — however, the recurring revenue aim is directly supported, making this a partial inference on the cost-reduction element.

---

CLAIM: "R2 platform launch" (execution timeline)
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and pre-written SEC Filing Highlights section both confirm the R2 platform launch with customer deliveries expected to begin in Q2 2026.

---

CLAIM: "monetized software features like Autonomy+"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state that "Fees for these [Autonomy+] features are expected to begin in April 2026," confirming Autonomy+ as a named monetized software feature.

---

CLAIM: "Adventure Network" (scaling of the Adventure Network)
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and pre-written SEC Filing Highlights section both reference the Rivian Adventure Network, noting over 95% of its DC fast chargers are open to non-Rivian EVs, confirming it as a named, sourced entity.

---

CLAIM: "mid-market EV segment" (intensified price competition in the mid-market EV segment)
LABEL: UNSUPPORTED
REASON: Neither the raw source data, the SEC filings, the RAG highlights, nor any pre-written section references the "mid-market EV segment" as a specific category or competitive arena for Rivian; this qualifier is absent from all context provided.
