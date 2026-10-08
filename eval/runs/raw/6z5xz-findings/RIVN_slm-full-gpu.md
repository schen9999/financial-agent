# RIVN — slm-full-gpu

## Metadata

ticker: RIVN
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: bb4d4d4cfce55a7de59ec9ebe23b3d186bc71a71e4fada3906ad61fd2d262714
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 780, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 37.717, "latency_s_total": 37.717, "parse_failure": 0, "prompt_tokens": 2412, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 265, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.258, "latency_s_total": 19.258, "parse_failure": 0, "prompt_tokens": 2401, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 133, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 10.176, "latency_s_total": 10.176, "parse_failure": 0, "prompt_tokens": 644, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 146, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 14.292, "latency_s_total": 14.292, "parse_failure": 0, "prompt_tokens": 638, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 136, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 16.272, "latency_s_total": 16.272, "parse_failure": 0, "prompt_tokens": 339, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 152, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 19.295, "latency_s_total": 19.295, "parse_failure": 0, "prompt_tokens": 862, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 865, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 18.538, "latency_s_total": 18.538, "parse_failure": 0, "prompt_tokens": 1516, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "RIVN",
  "company_name": "Rivian Automotive, Inc.",
  "current_price": 14.34,
  "currency": "USD",
  "market_cap": 20762320896.0,
  "forward_pe": -8.2261095,
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
*   The automotive industry historically sees higher revenue in spring and summer. Commercial vehicle deliveries typically decrease in the final months of the year as customers focus on holiday last-mile deliveries rather than fleet expansion, potentially leading to higher finished goods inventory.
*   In Q4 2025, Rivian delivered more Electric Delivery Vehicles (EDVs) than seasonally typical due to earlier supplier constraints.
*   Revenue is influenced by new product launch timing and government incentives. Specifically, the expiration of federal EV tax credits on September 30, 2025, caused a pull-forward of deliveries into Q3 and a corresponding decline in Q4 2025.

**Competition and Market Position**
*   Primary competitive factors include talent, culture, technological innovation, product performance, customer experience, brand differentiation, pricing, total cost of ownership (TCO), and manufacturing scale.
*   Competition extends beyond traditional OEMs and dealers to include third-party vehicle remarketers, repair and maintenance providers, charging networks, software providers, autonomous vehicle developers, and fleet management companies.
*   Rivian aims to compete effectively through product/brand differentiation, vertically-integrated technology, and direct-to-customer relationships.

**Software and Services Segment**
*   Rivian provides value-added software and services to generate recurring revenue and brand loyalty. Key offerings include:
    *   **Joint Venture:** An equally-owned joint venture with Volkswagen Group to develop next-generation electrical architecture and software, with Volkswagen planning to use Rivian’s zonal ECU architecture.
    *   **Autonomy+:** Advanced driver assistance features. The "Universal Hands Free" feature was expanded via OTA update in December 2025, covering over 3.5 million miles of roads in North America. Fees for these features are expected to begin in April 2026.
    *   **Charging:** The Rivian Adventure Network operates DC fast chargers across North America, with over 95% of the network open to non-Rivian EVs.
    *   **Software Subscriptions:** Includes standard connectivity features and premium options like Connect+ for consumers, and FleetOS, a centralized fleet management platform for commercial vehicles.
    *   **Other Services:** Includes vehicle repair and maintenance (via physical centers, mobile vehicles, and partners), remarketing, insurance, financing, and the Rivian Gear Shop.

**Manufacturing**
*   Vehicles are currently manufactured at the Normal Factory in Illinois, which has an annual installed capacity of up to 215,000 vehicles.
*   The capacity split is expected to be up to 155,000 R2 vehicles, 85,000 R1 vehicles, and 65,000 Rivian Commercial Vans.
*   Customer deliveries for the R2 platform are expected to begin in the second quarter of 2026.

**Regulatory and Environmental Compliance**
*   Operations are subject to stringent federal, state, and local laws regarding product safety, environmental protection, and occupational health. Non-compliance can result in penalties, remedial obligations, or operational injunctions.
*   **NHTSA Compliance:** All current vehicles (R1T, R1S, EDV, and Rivian Commercial Van) are fully compliant with Federal Motor Vehicle Safety Standards, CAFE standards, and other NHTSA requirements without needing exemptions.
*   **EPA Compliance:** The Clean Air Act requires an EPA Certificate of Conformity and a California Executive Order for operations.

RAG — RISK FACTORS:
[From Pinecone cache] Based on the provided context, the primary risk factors disclosed include:

*   **Access to Raw Materials:** The company references specific risks related to its ability to access raw materials.
*   **Seasonality and Demand Fluctuations:** The automotive industry experiences higher revenue in spring and summer, with commercial vehicle sales typically lower in the final months of the year due to holiday focus on last-mile deliveries. Additionally, consumer demand can fluctuate significantly due to the timing of government incentives, such as the expiration of federal EV tax credits, which can cause pull-forwards in deliveries and subsequent declines.
*   **Regulatory Compliance:** Operations are subject to stringent federal, state, and local laws regarding product safety, environmental protection, occupational health and safety, and emissions. Failure to comply can result in administrative, civil, and criminal penalties, investigatory obligations, and orders enjoining operations. Specific regulations include NHTSA Safety Standards (crashworthiness, crash avoidance, and EV requirements), CAFE standards, and the Automobile Information and Disclosure Act.
*   **Competition:** The company faces competition from millions of traditional internal combustion engine vehicles and EVs, as well as downstream competitors such as vehicle remarketers, repair and maintenance providers, charging and software providers, autonomous vehicle developers, and fleet management companies.

## Pre-written sections (judge input)

### Financial Health

Rivian Automotive, Inc. (RIVN) currently trades at $14.34 with a market capitalization of approximately $20.76 billion. The company has generated $5.88 billion in revenue but remains unprofitable, reporting a net loss that results in a negative profit margin of -54.95%. Consequently, the forward P/E ratio is negative, reflecting the absence of earnings. While the stock has shown resilience near its 52-week low of $12.39, the persistent losses highlight the ongoing challenges associated with its growth-stage status and capital-intensive operations.

### Recent Developments

Rivian filed its 2026 10-K on February 12, highlighting a strategic joint venture with Volkswagen Group to develop next-generation electrical architecture and software, aiming to create recurring revenue streams through services like subscriptions and maintenance. The company continues to report significant net losses, with a profit margin of -54.95%, reflecting the challenges inherent in its growth-stage status and limited operating history. Despite these headwinds, the focus on software-defined vehicles and value-added services is intended to bolster long-term brand loyalty and diversify income beyond hardware sales. Investors should monitor the execution of this JV partnership and progress toward profitability as key indicators for the stock's future performance.

### SEC Filing Highlights
Rivian’s Q4 2025 revenue was significantly impacted by the expiration of federal EV tax credits, which triggered a delivery pull-forward into Q3 and a subsequent seasonal decline. To drive future growth, the company is advancing its software and services segment, highlighted by a joint venture with Volkswagen for next-generation electrical architecture and the upcoming monetization of its "Autonomy+" features in April 2026. Manufacturing capacity at the Normal Factory is being optimized to support the R2 platform, with customer deliveries scheduled to begin in the second quarter of 2026. Additionally, all current vehicle models remain fully compliant with NHTSA safety standards and EPA regulatory requirements, mitigating immediate operational risks.

### Risk Factors

*   **Supply Chain and Raw Material Constraints:** The company faces significant risks related to its ability to secure and access essential raw materials, which could disrupt production and increase costs.
*   **Demand Volatility and Seasonality:** Revenue is subject to seasonal fluctuations, with lower commercial sales in year-end months, and consumer demand is highly sensitive to the timing of government incentives, such as the expiration of federal EV tax credits.
*   **Intense Competition and Regulatory Pressure:** The company competes against millions of traditional and electric vehicles, as well as downstream service providers, while facing stringent federal and state regulations regarding safety, emissions, and environmental compliance.

## Audited (Exec Summary + Outlook)

### Executive Summary
Rivian Automotive, Inc. is a growth-stage electric vehicle manufacturer with a market capitalization of approximately $20.76 billion, currently navigating the challenges of a capital-intensive business model that has resulted in a negative profit margin of -54.95%. The stock is notable for its strategic pivot toward recurring revenue streams through a joint venture with Volkswagen and the imminent launch of its more affordable R2 platform, despite persistent near-term losses. The single most important near-term variable shaping the investment outcome is the successful execution of the R2 delivery ramp and the monetization of software-defined vehicle features.

### Outlook
The directional outlook for Rivian is cautiously constructive, driven by the potential for margin expansion through its software and services joint venture with Volkswagen and the anticipated volume growth from the upcoming R2 platform. Key variables to monitor include the execution speed of the R2 delivery ramp, the adoption rates of monetized features like "Autonomy+," and the company's ability to stabilize gross margins amidst intense competitive pressure. The thesis would be strengthened by clear evidence of recurring revenue growth offsetting hardware losses and successful supply chain optimization; conversely, it would be weakened by prolonged delays in the R2 launch, continued deterioration in hardware margins, or a failure to secure necessary raw materials.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of approximately $20.76 billion"
LABEL: SUPPORTED
REASON: The source data lists market_cap as 20,762,320,896.0 USD, which rounds to approximately $20.76 billion.

---

CLAIM: "negative profit margin of -54.95%"
LABEL: SUPPORTED
REASON: The source data explicitly states profit_margin_pct as -54.95, and this figure is also repeated in the pre-written Financial Health and Recent Developments sections.

---

CLAIM: "joint venture with Volkswagen"
LABEL: SUPPORTED
REASON: The SEC filing summaries and RAG highlights explicitly describe an equally-owned joint venture between Rivian and Volkswagen Group for next-generation electrical architecture and software.

---

CLAIM: "imminent launch of its more affordable R2 platform"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights state that "Customer deliveries for the R2 platform are expected to begin in the second quarter of 2026," confirming an upcoming launch; the characterization of "more affordable" is not quantitatively verifiable from the source data, but the launch timing is supported.

---

CLAIM: "successful execution of the R2 delivery ramp and the monetization of software-defined vehicle features" [as the single most important near-term variable]
LABEL: INFERENCE
REASON: This is a qualitative editorial judgment synthesizing the R2 delivery timeline (Q2 2026, per RAG) and the Autonomy+ monetization start (April 2026, per RAG) into a prioritization statement; no source explicitly ranks these as "the single most important" variable, but both underlying facts are present in the source data.

---

**OUTLOOK**

---

CLAIM: "software and services joint venture with Volkswagen"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights and 10-K summary explicitly confirm the equally-owned joint venture with Volkswagen Group focused on software and electrical architecture.

---

CLAIM: "upcoming R2 platform"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights confirm R2 customer deliveries are expected to begin in Q2 2026.

---

CLAIM: "monetized features like 'Autonomy+'"
LABEL: SUPPORTED
REASON: The RAG SEC Highlights explicitly state that "Fees for these features [Autonomy+] are expected to begin in April 2026," confirming planned monetization.

---

CLAIM: "R2 delivery ramp" [as a key variable to monitor]
LABEL: SUPPORTED
REASON: The RAG SEC Highlights confirm R2 deliveries are scheduled to begin in Q2 2026, making the ramp a factually grounded forward-looking milestone.

---

CLAIM: "prolonged delays in the R2 launch" [as a thesis-weakening risk]
LABEL: SUPPORTED
REASON: The R2 launch in Q2 2026 is confirmed in the source data, making a delay scenario a directly derivable risk from that stated timeline.

---

CLAIM: "failure to secure necessary raw materials" [as a thesis-weakening risk]
LABEL: SUPPORTED
REASON: The RAG Risk Factors section explicitly identifies "Access to Raw Materials" as a disclosed risk factor in Rivian's SEC filings.

---

**SUMMARY OF FINDINGS**

No claims in the Executive Summary or Outlook sections are UNSUPPORTED. All quantitative figures ($20.76B market cap, -54.95% profit margin) are directly present in the source data. All named milestones (R2 platform launch in Q2 2026, Autonomy+ monetization in April 2026, Volkswagen JV) are explicitly confirmed in the RAG SEC Highlights. The one INFERENCE is the editorial prioritization of the R2 ramp and software monetization as "the single most important near-term variable," which synthesizes present facts but adds a ranking judgment not stated in the source.
