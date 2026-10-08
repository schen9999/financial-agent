# CHGG — slm-full-gpu

## Metadata

ticker: CHGG
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: b83dc72376af829a5df154b38da8182f80df269310527f4949558e01b09d2127
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 717, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 12.175, "latency_s_total": 12.175, "parse_failure": 0, "prompt_tokens": 3017, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 493, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 9.962, "latency_s_total": 9.962, "parse_failure": 0, "prompt_tokens": 3042, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 142, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.883, "latency_s_total": 4.883, "parse_failure": 0, "prompt_tokens": 700, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 168, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.21, "latency_s_total": 5.21, "parse_failure": 0, "prompt_tokens": 694, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 142, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.881, "latency_s_total": 4.881, "parse_failure": 0, "prompt_tokens": 565, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 156, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.085, "latency_s_total": 5.085, "parse_failure": 0, "prompt_tokens": 797, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 931, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 10.277, "latency_s_total": 10.277, "parse_failure": 0, "prompt_tokens": 1594, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "CHGG",
  "company_name": "Chegg, Inc.",
  "current_price": 0.739,
  "currency": "USD",
  "market_cap": 82049312.0,
  "forward_pe": -10.557143,
  "week_52_high": 1.56,
  "week_52_low": 0.45,
  "financial_currency": "USD",
  "revenue": 265512000.0,
  "net_income": -52997000.0,
  "profit_margin_pct": -19.96,
  "dividend_yield": 0.0,
  "sector": "Consumer Defensive",
  "industry": "Education & Training Services"
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
    "filing_date": "2026-03-09",
    "summary": "ITEM 1A. RISK FACTORS The risks and uncertainties set forth below, as well as other risks and uncertainties described elsewhere in this Annual Report on Form 10-K including on our consolidated financial statements and related notes and the section titled \u201cManagement\u2019s Discussion and Analysis of Financial Condition and Results of Operations\u201d or in other filings by Chegg with the SEC, could adversely affect our business, financial condition, results of operations, and the trading price of our common stock. Additional risks and uncertainties that are not currently known to us or that are not currently believed by us to be material may also harm our business operations and financial results. Because of the following risks and uncertainties, as well as other factors affecting our financial cond"
  },
  "10-Q": {
    "form_type": "10-Q",
    "filing_date": "2026-08-06",
    "summary": "ITEM 1A. RISK FACTORS Our operations and financial results are subject to various risks and uncertainties, including those described in Part I, Item 1A, \u201cRisk Factors\u201d in our Annual Report on Form 10-K for the fiscal year ended December 31, 2025, which could adversely affect our business, financial condition, results of operations, cash flows, and the trading price of our common stock. There have been no material changes in our risk factors from our Annual Report on Form 10-K. ITEM 2. UNREGISTERED SALES OF EQUITY SECURITIES AND USE OF PROCEEDS Unregistered Sales of Securities We had no unregistered sales of our securities during the three months ended June 30, 2026. Purchases of Securities by the Registrant and Affiliated Purchasers The following table presents the common stock repurchase "
  }
}

RAG — SEC HIGHLIGHTS:
[From Pinecone cache] Based on the provided context from Chegg’s (ticker: CHGG) filings, the key takeaways regarding risks and business strategy include:

**Strategic Transformation and Execution Risks**
Chegg is evolving its learning platform into a skilling-focused business-to-business organization, leveraging existing strengths in professional language learning, workplace readiness, and AI-related skills. This transformation carries significant risks, including organizational, operational, financial, and technological challenges. There is no assurance that the company can develop novel products, attract or retain customers, or hire the necessary talent in a competitive job market. Additionally, restructuring efforts may lead to a loss of continuity, accumulated knowledge, or efficiency, while diverting management attention from core operations.

**Intense Competition and AI Disruption**
Competition is increasing across all aspects of Chegg’s business, particularly regarding AI. The company faces rivals in specific verticals, including:
*   **Language Learning:** GoFluent, Speexx, and Duolingo.
*   **Workforce Skilling:** 2U, Inc., Simplilearn, General Assembly, Galvanize, Inc., Flatiron School, Codecademy, DataCamp, and Lambda, Inc.
*   **Study Materials (Chegg Study):** Course Hero, Quizlet, Brainly, and Khan Academy.
*   **Writing Assistance (Chegg Writing):** Grammarly.
*   **Math Solutions (Chegg Math):** Photomath, Gauthmath, and Symbolab.

Furthermore, broad AI providers not specifically focused on education—such as Google, OpenAI, Microsoft, Meta, and Anthropic—pose significant competitive threats.

**Impact of Google’s AI Overview (AIO)**
Google’s expansion of its Artificial Intelligence Overview (AIO) search experience, which began significantly in August 2024, has created headwinds for Chegg. By displaying AI-generated educational content and solutions at the top of search results, Google keeps users on its platform rather than directing them to Chegg’s site. This shift from search origination to destination is expected to reduce website traffic and subscriber growth, potentially materially adversely affecting Chegg’s financial condition.

**Legal Action Against Google**
On February 24, 2025, Chegg filed a complaint in the U.S. District Court for the District of Columbia against Google LLC and Alphabet Inc. The suit asserts federal antitrust and common-law unjust enrichment claims related to Google’s expansion of AIO. The outcome is unpredictable, and the litigation could result in costly expenses, divert management time, and require significant resources.

**Revenue Dependency and Customer Retention**
Chegg’s revenue has declined, and its business relies heavily on attracting new learners and retaining existing ones. The Academic Services segment, which represents the majority of revenue, depends on small transactions from a dispersed student population with high turnover due to graduation. The Skilling business depends on engaging enterprise customers and individual learners. Factors influencing customer base expansion and retention include the availability of free competing content, piracy, localization efforts, changes in customer spending habits, and the effectiveness of sales and marketing strategies.

**Content Licensing and New Entrants**
Chegg has licensed content to other entities that may use it to train AI models competing with Chegg’s products. Additionally, educational institutions like the University of Michigan are developing their own AI tools. AI technologies are also lowering barriers to entry, facilitating the arrival of new competitors who may develop superior or more cost-effective technologies.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Failure to Execute Business Strategy:** The company may fail to successfully execute its skilling-focused business-to-business strategy and business transformation plan. This could result from organizational, operational, financial, or technological challenges, such as an inability to develop novel products, attract or retain customers, or hire the right talent. Additionally, restructuring efforts may cause a loss of continuity, accumulated knowledge, or efficiency, and divert management attention from operating activities.
*   **Revenue Decline and Customer Retention:** Revenue has declined, and the business relies heavily on attracting new learners and retaining existing ones. The Academic Services business faces high turnover due to student graduation, while the Skilling business depends on attracting enterprise customers and individual learners. Customer base expansion and engagement may fluctuate due to factors such as competing free content, piracy, localization challenges, changes in customer spending habits, and the effectiveness of sales and marketing efforts.
*   **Technological Disruption and AI Competition:** The company faces headwinds from new technologies, particularly AI and machine learning, which provide immediate responses and are expected to improve in accuracy and complexity. Although the company has partnered with OpenAI and invested in AI initiatives, these efforts have not attracted as many new students as anticipated. Failure to innovate, keep pace with technological developments, or offer competitive AI-powered products could harm the company’s competitive position and business prospects.
*   **Intense Competition:** The company competes with numerous organizations, many of which have greater resources and offer products at lower prices. Competition is expected to increase across all aspects of the business, including AI. If competitors develop more cost-effective technologies or product offerings, the company’s operating results, growth, and financial condition could be materially adversely affected.
*   **Product Development and Liability Risks:** New product and service offerings may increase the risk of liability and incur significant technical, legal, or other costs. There is no guarantee that investments in new products, services, or initiatives will be successful, as these markets may be unproven, and the company may lack prior experience with the required technologies or business models. Additionally, the company may be unable to obtain necessary third-party licenses or regulatory approvals.
*   **Pricing and Unauthorized Use:** The company may be unable to maintain its customer base if it cannot offer competitive prices, adequately prevent unauthorized account sharing, or stop the piracy and illegal reproduction of its content.

## Pre-written sections (judge input)

### Financial Health

Chegg, Inc. (CHGG) currently trades at $0.739 with a market capitalization of approximately $82.05 million. The company reported annual revenue of $265.51 million but faces significant profitability challenges, evidenced by a net loss and a negative profit margin of -19.96%. This financial strain is further reflected in a negative forward P/E ratio of -10.56, indicating that the company is not currently generating earnings to support valuation multiples. Consequently, the stock remains well below its 52-week high of $1.56, highlighting ongoing investor concern regarding its near-term financial stability.

### Recent Developments

Chegg, Inc. (CHGG) continues to face significant financial headwinds, evidenced by a negative net income of approximately $53 million and a profit margin of -19.96%, resulting in a negative forward P/E ratio. The company's market capitalization has contracted to roughly $82 million, with the stock trading near its 52-week low of $0.45, reflecting persistent investor concern over profitability and cash flow. Recent SEC filings, including the 10-K and 10-Q reports, highlight ongoing risk factors without indicating material changes in operational strategy or unregistered equity sales. For investors, these developments underscore the high-risk nature of the position, characterized by sustained losses and a depressed valuation that may struggle to recover without a clear path to profitability.

### SEC Filing Highlights
Chegg is executing a strategic transformation toward a B2B skilling-focused model, though this shift introduces significant operational and talent acquisition risks amidst intense competition from both specialized edtech rivals and broad AI providers. The company faces substantial headwinds from Google’s AI Overview, which diverts search traffic away from Chegg’s platforms, prompting a federal antitrust lawsuit filed in February 2025 to address these alleged unfair practices. Revenue performance remains pressured by high customer turnover in the Academic Services segment and the growing availability of free, AI-generated educational content that threatens subscriber retention. Additionally, the firm contends with the risk that licensed content may be used by third parties to train competing AI models, further lowering barriers to entry for new market competitors.

### Risk Factors

*   **Strategic Execution and Revenue Volatility:** The company faces risks in executing its B2B skilling strategy and managing restructuring efforts, compounded by historical revenue declines and high customer turnover in its Academic Services segment.
*   **Technological Disruption and AI Competition:** Rapid advancements in AI and machine learning pose significant competitive threats; failure to innovate or effectively integrate AI-powered solutions may erode the company’s market position and growth prospects.
*   **Intense Market Competition and Piracy:** Chegg competes against well-resourced rivals offering lower-priced alternatives, while also struggling to mitigate revenue loss from unauthorized account sharing, piracy, and the availability of free competing content.

## Audited (Exec Summary + Outlook)

### Executive Summary
Chegg, Inc. operates in the educational technology sector, currently navigating a challenging financial landscape marked by a $265.51 million annual revenue and a negative profit margin of -19.96%. The stock is notable for its depressed valuation, trading near its 52-week low of $0.45 with a market capitalization of roughly $82 million, reflecting deep investor skepticism regarding its path to profitability. The single most important near-term variable shaping the outcome is the successful execution of its strategic pivot to a B2B skilling-focused model amidst intense AI-driven competition.

### Outlook
The directional outlook for Chegg remains cautiously neutral, heavily weighted by the uncertainty surrounding its strategic pivot from a B2C academic model to a B2B skilling focus. While the antitrust lawsuit against Google and the potential for B2B partnerships offer theoretical tailwinds, these are currently overshadowed by significant headwinds, including the erosion of search traffic via AI overviews and the threat of free, AI-generated content. Investors should closely monitor the success of the B2B transition, specifically regarding talent acquisition and the stabilization of customer retention rates in the Academic Services segment. The thesis would strengthen if the company demonstrates clear progress in reducing customer churn and securing meaningful B2B contracts, whereas continued revenue volatility or failure to differentiate its AI capabilities from broad providers would further weaken the investment case.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically audit every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the Executive Summary and Outlook sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "$265.51 million annual revenue"
LABEL: SUPPORTED
REASON: The raw source data lists revenue of $265,512,000, which rounds to $265.51 million, and the same figure appears in the Financial Health pre-written section.

---

CLAIM: "negative profit margin of -19.96%"
LABEL: SUPPORTED
REASON: The raw source data explicitly states `"profit_margin_pct": -19.96`, and the same figure appears in the Financial Health and Recent Developments pre-written sections.

---

CLAIM: "trading near its 52-week low of $0.45"
LABEL: SUPPORTED
REASON: The raw source data lists `"week_52_low": 0.45`, and the current price of $0.739 is arithmetically closer to the 52-week low of $0.45 than to the 52-week high of $1.56, making the "near its 52-week low" positional claim arithmetically valid; the $0.45 figure is explicitly present in the source data.

---

CLAIM: "market capitalization of roughly $82 million"
LABEL: SUPPORTED
REASON: The raw source data lists `"market_cap": 82,049,312`, which rounds to approximately $82 million, consistent with the pre-written sections.

---

**OUTLOOK**

No explicit quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers appear in the Outlook section. All claims in the Outlook are qualitative or directional in nature (e.g., "cautiously neutral," "theoretical tailwinds," "significant headwinds," "clear progress," "meaningful B2B contracts"). There are no numerical claims to audit in this section.

---

**SUMMARY TABLE**

| Claim | Label |
|---|---|
| $265.51 million annual revenue | SUPPORTED |
| Negative profit margin of -19.96% | SUPPORTED |
| Trading near its 52-week low of $0.45 | SUPPORTED |
| Market capitalization of roughly $82 million | SUPPORTED |

All four quantitative claims in the audited sections are supported by the raw source data. No unsupported or inference-labeled claims were identified. The Outlook section contains no quantitative claims requiring audit.
