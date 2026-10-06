# RIVN — slm-full-cpu

## Metadata

ticker: RIVN
arm: slm-full-cpu
judge_prompt_version: v2
context_sha256: 976eaaed47aab6196cf58f68c5189b25f487c04e83a291c51ee1b382317f7e28
slm_endpoint: slm-cpu
slm_url: http://llamacpp.financial-agent.svc:8080
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
llm_endpoints: slm-cpu
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 742, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 189.466, "latency_s_total": 189.466, "parse_failure": 0, "prompt_tokens": 2412, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 295, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 136.295, "latency_s_total": 136.295, "parse_failure": 0, "prompt_tokens": 2401, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 137, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 41.846, "latency_s_total": 41.846, "parse_failure": 0, "prompt_tokens": 644, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 143, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 54.644, "latency_s_total": 54.644, "parse_failure": 0, "prompt_tokens": 638, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 142, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 48.479, "latency_s_total": 48.479, "parse_failure": 0, "prompt_tokens": 369, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 170, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 68.387, "latency_s_total": 68.387, "parse_failure": 0, "prompt_tokens": 824, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 911, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 141.936, "latency_s_total": 141.936, "parse_failure": 0, "prompt_tokens": 1566, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "RIVN",
  "company_name": "Rivian Automotive, Inc.",
  "current_price": 14.485,
  "currency": "USD",
  "market_cap": 20972261376.0,
  "forward_pe": -8.309288,
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
*   The automotive industry historically sees higher revenue in spring and summer. Commercial vehicle deliveries typically decline in the final months of the year as customers focus on holiday last-mile deliveries rather than fleet expansion, potentially leading to higher finished goods inventory.
*   In the fourth quarter of 2025, Rivian delivered more Electric Delivery Vehicles (EDVs) than seasonally typical due to supplier constraints earlier in the year.
*   Revenue fluctuations were significantly impacted by the expiration of federal EV tax credits on September 30, 2025, which caused a pull-forward of deliveries into the third quarter and a corresponding decline in the fourth quarter.

**Competition and Market Position**
*   Primary competitive factors include talent, culture, technological innovation, product performance, customer experience, brand differentiation, pricing, total cost of ownership (TCO), and manufacturing scale.
*   Competition extends beyond traditional OEMs and dealers to include third-party vehicle remarketers, repair and maintenance providers, charging networks, software providers, and fleet management companies.
*   Rivian aims to compete effectively through product and brand differentiation, vertically-integrated technology, and direct-to-customer relationships.

**Software and Services Segment**
*   Rivian provides value-added software and services to generate recurring revenue and brand loyalty. Key offerings include:
    *   **Joint Venture:** An equally-owned joint venture with Volkswagen Group to develop next-generation electrical architecture and software technology.
    *   **Autonomy+:** Advanced driver assistance features, including a Universal Hands Free feature expanded to over 3.5 million miles of roads in North America via OTA update in December 2025. Fees for these features are expected to begin in April 2026.
    *   **Charging:** The Rivian Adventure Network, with over 95% of chargers open to non-Rivian EVs.
    *   **Subscriptions:** Includes Connect+ for consumer vehicles and FleetOS, a centralized fleet management platform for commercial vehicles.
    *   **Other Services:** Vehicle repair and maintenance (via physical centers and mobile vehicles), remarketing, insurance, financing, and the Rivian Gear Shop.

**Manufacturing and Production**
*   Vehicles are currently manufactured at the Normal Factory in Illinois, which has an annual installed capacity of up to 215,000 vehicles.
*   The capacity split is expected to be up to 155,000 R2 vehicles, 85,000 R1 vehicles, and 65,000 Rivian Commercial Vans.
*   Customer deliveries for the R2 platform are expected to begin in the second quarter of 2026.

**Regulatory Compliance**
*   **NHTSA:** All current models (R1T, R1S, EDV, and Rivian Commercial Van) are fully compliant with Federal Motor Vehicle Safety Standards, CAFE standards, and other NHTSA requirements without needing exemptions.
*   **EPA:** The company is subject to Clean Air Act requirements, including obtaining an EPA Certificate of Conformity and California Executive Order.
*   **General:** Operations are subject to stringent federal, state, and local laws regarding environmental protection, occupational health and safety, and product safety. Failure to comply can result in penalties, remedial obligations, or operational injunctions.

RAG — RISK FACTORS:
[From Pinecone cache] Based on the provided context, the primary risk factors disclosed include:

*   **Raw Material Access:** There are specific risks related to the company's access to raw materials, which are detailed in Part I, Item 1A.
*   **Regulatory Compliance:** Operations, properties, products, and services are subject to stringent federal, state, and local laws regarding product safety, environmental protection, occupational health and safety, and emissions. Failure to comply can result in administrative, civil, and criminal penalties, investigatory and remedial obligations, and orders enjoining operations. This includes compliance with National Highway Traffic Safety Administration (NHTSA) Safety Standards, Federal Corporate Average Fuel Economy (CAFE) standards, and Clean Air Act requirements.
*   **Seasonality and Demand Fluctuations:** The automotive industry experiences higher revenue in spring and summer, with commercial vehicle deliveries potentially decreasing in the final months of the year. Additionally, revenues are influenced by the timing of new product launches and changes in government incentives, such as the expiration of federal EV tax credits, which can cause significant fluctuations in consumer demand.
*   **Competition:** The company faces competition from millions of traditional internal combustion engine (ICE) vehicles and electric vehicles (EVs) in both consumer and commercial markets. Competition also extends to downstream third parties, including vehicle remarketers, repair and maintenance providers, charging and software providers, autonomous vehicle software developers, and traditional fleet management companies.

## Pre-written sections (judge input)

### Financial Health

Rivian Automotive, Inc. (RIVN) currently trades at $14.49 with a market capitalization of approximately $21.0 billion. The company has generated $5.88 billion in revenue but remains unprofitable, reporting a net loss of $3.23 billion and a negative profit margin of -54.95%. Consequently, the forward P/E ratio is negative, reflecting the firm's ongoing challenges in achieving earnings stability. While the business model aims to generate recurring revenue through software and services, current financials indicate a high-risk profile typical of early-stage growth companies in the auto manufacturing sector.

### Recent Developments

Rivian Automotive filed its 10-K on February 12, 2026, highlighting a strategic joint venture with Volkswagen Group to develop next-generation electrical architecture and software, aiming to create recurring revenue streams through services like subscriptions and maintenance. Despite this strategic pivot toward software and services, the company continues to report significant net losses, with a profit margin of -54.95% and negative forward P/E, underscoring the challenges of its growth-stage status. Investors should monitor the execution of the JV and the company's path to profitability, as these factors remain critical given the current stock price of $14.49 and substantial operating losses.

### SEC Filing Highlights
Rivian’s fourth-quarter 2025 revenue was significantly impacted by the expiration of federal EV tax credits, which triggered a delivery pull-forward into Q3 and a subsequent seasonal decline in Q4. The company is preparing for the R2 platform launch, with deliveries expected in Q2 2026, while its Normal Factory maintains an annual capacity of up to 215,000 vehicles. To drive recurring revenue, Rivian is expanding its software and services segment, including a joint venture with Volkswagen for next-generation architecture and the upcoming monetization of its Autonomy+ features in April 2026. All current models remain fully compliant with NHTSA and EPA regulations, mitigating immediate regulatory risks as the company scales production and competes on total cost of ownership.

### Risk Factors

*   **Supply Chain and Raw Material Constraints:** The company faces specific risks regarding its access to essential raw materials, which could disrupt production and increase costs.
*   **Regulatory and Compliance Exposure:** Operations are subject to stringent federal, state, and local laws, including NHTSA safety standards, CAFE regulations, and environmental protections; non-compliance may result in significant penalties, remedial obligations, or operational injunctions.
*   **Market Volatility and Competitive Pressure:** Revenue is susceptible to seasonal demand fluctuations, changes in government incentives (such as EV tax credits), and intense competition from both traditional ICE vehicles and other EV manufacturers, as well as downstream service providers.

## Audited (Exec Summary + Outlook)

### Executive Summary
Rivian Automotive operates as a premium electric vehicle manufacturer with a $21.0 billion market capitalization, currently navigating the challenges of early-stage growth with $5.88 billion in revenue and a net loss of $3.23 billion. The stock is notable now due to its strategic pivot toward recurring software revenue via a Volkswagen joint venture and the imminent launch of the R2 platform, despite a negative profit margin of -54.95% and negative forward P/E. The single most important near-term variable is the successful execution of the R2 delivery ramp in Q2 2026 and the monetization of Autonomy+ features, which will determine if the company can transition from high-burn growth to sustainable unit economics.

### Outlook
The directional outlook for Rivian is cautiously constructive, driven by the potential for margin expansion through its strategic pivot to software and services, particularly the Volkswagen joint venture and Autonomy+ monetization. Key variables to monitor include the execution speed of the R2 platform launch, the stability of the services-margin trend, and the company's ability to navigate seasonal demand fluctuations without relying heavily on federal tax credits. The thesis would be strengthened by clear evidence of recurring revenue growth offsetting manufacturing losses, while it would be weakened by continued deterioration in gross margins or delays in the R2 delivery ramp that exacerbate current cash burn challenges.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$21.0 billion market capitalization"
LABEL: SUPPORTED
REASON: Source data shows market_cap = $20,972,261,376, which rounds to $21.0 billion; the Pre-written Financial Health section also states "approximately $21.0 billion."

---

CLAIM: "$5.88 billion in revenue"
LABEL: SUPPORTED
REASON: Source data shows revenue = $5,882,999,808, which rounds to $5.88 billion; confirmed in the Financial Health pre-written section.

---

CLAIM: "net loss of $3.23 billion"
LABEL: SUPPORTED
REASON: Source data shows net_income = -$3,232,999,936, which rounds to -$3.23 billion; confirmed in the Financial Health pre-written section.

---

CLAIM: "negative profit margin of -54.95%"
LABEL: SUPPORTED
REASON: Source data explicitly states profit_margin_pct = -54.95; arithmetic check: -3,232,999,936 / 5,882,999,808 = -54.96%, within 0.15 pp of the stated figure.

---

CLAIM: "negative forward P/E"
LABEL: SUPPORTED
REASON: Source data shows forward_pe = -8.309288, which is negative; confirmed in the Financial Health pre-written section.

---

CLAIM: "R2 delivery ramp in Q2 2026"
LABEL: SUPPORTED
REASON: RAG SEC Highlights and SEC Filing Highlights pre-written section both explicitly state "Customer deliveries for the R2 platform are expected to begin in the second quarter of 2026."

---

CLAIM: "monetization of Autonomy+ features"
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly states "Fees for these features [Autonomy+] are expected to begin in April 2026," and the SEC Filing Highlights pre-written section references "the upcoming monetization of its Autonomy+ features in April 2026."

---

**OUTLOOK**

---

CLAIM: "Volkswagen joint venture"
LABEL: SUPPORTED
REASON: Source data (10-K summary, RAG SEC Highlights, and multiple pre-written sections) explicitly describes an equally-owned joint venture between Rivian and Volkswagen Group.

---

CLAIM: "Autonomy+ monetization"
LABEL: SUPPORTED
REASON: RAG SEC Highlights explicitly states fees for Autonomy+ features are expected to begin in April 2026; confirmed in the SEC Filing Highlights pre-written section.

---

CLAIM: "R2 platform launch" / "R2 delivery ramp"
LABEL: SUPPORTED
REASON: RAG SEC Highlights and SEC Filing Highlights pre-written section both explicitly state R2 platform deliveries are expected to begin in Q2 2026.

---

CLAIM: "seasonal demand fluctuations without relying heavily on federal tax credits"
LABEL: SUPPORTED
REASON: RAG SEC Highlights and Risk Factors both explicitly discuss seasonality and the impact of the expiration of federal EV tax credits on Q3/Q4 2025 deliveries; the directional characterization is grounded in these source facts.

---

**Summary:** No quantitative or forward-looking claims in the Executive Summary or Outlook are unsupported or require inference beyond what is directly present in the source data. All figures check out arithmetically and all named milestones, products, and partnerships are explicitly present in the source material.
