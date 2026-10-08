# CHGG — slm-full-gpu

## Metadata

ticker: CHGG
arm: slm-full-gpu
judge_prompt_version: v2
context_sha256: 293933abb5791358ce0ee76b0e8f491ac3801b21c02afabd58e5581a3de40dcb
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 680, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 12.003, "latency_s_total": 12.003, "parse_failure": 0, "prompt_tokens": 3017, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 433, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 9.591, "latency_s_total": 9.591, "parse_failure": 0, "prompt_tokens": 3042, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 126, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.596, "latency_s_total": 4.596, "parse_failure": 0, "prompt_tokens": 700, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 146, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.914, "latency_s_total": 4.914, "parse_failure": 0, "prompt_tokens": 694, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 166, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 5.108, "latency_s_total": 5.108, "parse_failure": 0, "prompt_tokens": 505, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 137, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 4.785, "latency_s_total": 4.785, "parse_failure": 0, "prompt_tokens": 760, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 923, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 10.139, "latency_s_total": 10.139, "parse_failure": 0, "prompt_tokens": 1528, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

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
[From Pinecone cache] Based on the provided text from Chegg’s (ticker: CHGG) Annual Report on Form 10-K, the key takeaways regarding risks and business strategy include:

**Strategic Transformation and Execution Risks**
Chegg is evolving its learning platform into a skilling-focused business-to-business organization, leveraging existing strengths in professional language learning, workplace readiness, and AI-related skills. This transformation carries significant risks, including organizational, operational, financial, and technological challenges. There is no assurance that the company can develop novel products, attract or retain customers, or hire the necessary talent in a competitive job market. Additionally, restructuring efforts may lead to a loss of continuity, accumulated knowledge, or efficiency, while diverting management time and resources from core operating activities.

**Revenue Dependency and Customer Retention**
The company’s revenue has declined, and its business relies heavily on its ability to attract new learners and retain existing ones. The Academic Services segment, which constitutes the majority of revenue, depends on small transactions from a widely dispersed student population with high turnover due to graduation. The Skilling business depends on attracting enterprise customers and engaging individual learners. Factors influencing customer base expansion and retention include competition from free content, piracy, the ability to localize content and pricing, and the effectiveness of sales and marketing efforts.

**Intense Competition and AI Disruption**
Chegg faces significant and increasing competition across all aspects of its business, particularly regarding AI. Competitors include:
*   **Language Learning:** GoFluent, Speexx, and Duolingo.
*   **Workforce Skilling:** 2U, Inc., Simplilearn, General Assembly, Galvanize, Inc., Flatiron School, Codecademy, DataCamp, and Lambda, Inc.
*   **Study Materials (Chegg Study):** Course Hero, Quizlet, Brainly, and Khan Academy.
*   **Writing Assistance (Chegg Writing):** Grammarly.
*   **Math Solutions (Chegg Math):** Photomath, Gauthmath, and Symbolab.

Broad AI providers not specifically focused on education, such as Google, OpenAI, Microsoft, Meta, and Anthropic, also pose a threat. Specifically, Google’s expansion of its Artificial Intelligence Overview (AIO) in August 2024 has created headwinds by displaying AI-generated educational content at the top of search results, keeping users on Google’s platform rather than directing them to Chegg. This shift from search origination to destination could materially adversely affect Chegg’s traffic, subscriptions, and financial condition.

**Legal Proceedings**
On February 24, 2025, Chegg filed a complaint in the U.S. District Court for the District of Columbia against Google LLC and Alphabet Inc. The suit asserts federal antitrust claims and common-law unjust enrichment claims related to Google’s expansion of the AIO search experience. The outcome is unpredictable, and the litigation could result in costly expenses, divert management attention, and require significant resources.

**Additional Competitive Threats**
Chegg has licensed content to other entities that may use it to train AI models competing with Chegg’s products. Furthermore, educational institutions like the University of Michigan are developing their own AI tools, and AI technologies may lower barriers to entry for new competitors in the industry.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Failure to Execute Business Strategy:** The company may fail to successfully execute its skilling-focused business-to-business strategy and realize the anticipated benefits of its business transformation and restructuring plan. This includes risks related to organizational, operational, financial, and technological challenges, such as an inability to develop novel products, attract or retain customers, or hire the right talent.
*   **Revenue Decline and Customer Retention:** Revenue has declined, and the business depends on attracting new learners and retaining existing ones. The Academic Services business faces high turnover due to graduation, while the Skilling business relies on attracting enterprise customers and individual learners. Customer base expansion and engagement may fluctuate due to factors like competing free content, piracy, localization challenges, and changes in customer spending habits.
*   **Technological Disruption and AI:** The company faces headwinds from new technologies, particularly AI and machine learning, which provide immediate responses and may disrupt traditional tools. Although the company has partnered with OpenAI and invested in AI initiatives, these efforts have not attracted as many new students as anticipated, adversely affecting the business. Failure to innovate or keep pace with technological developments could harm competitive position and business prospects.
*   **Competition:** The company faces competition in all aspects of its business, including AI, with numerous organizations, many of which have greater resources and offer lower prices. Competition is expected to increase as the industry evolves rapidly.
*   **Innovation and Investment Risks:** There is no guarantee that investments in new products, services, or initiatives will be successful. Developing new technologies requires significant expenses, and the company may face difficulties in obtaining necessary licenses or regulatory approvals. If competitors develop more cost-effective technologies, the company’s operating results and financial condition could be materially adversely affected.
*   **Operational and Restructuring Impacts:** Restructuring efforts may lead to a loss of continuity, accumulated knowledge, or efficiency. Reorganization can divert management and employee attention from operating activities and business growth. Additionally, new product offerings may increase liability risks and incur significant technical, legal, or other costs.

## Pre-written sections (judge input)

### Financial Health

Chegg, Inc. (CHGG) currently trades at $0.739 with a market capitalization of approximately $82.05 million. The company reported annual revenue of $265.51 million but is currently unprofitable, resulting in a negative net income of $52.99 million and a profit margin of -19.96%. Consequently, the forward P/E ratio is negative at -10.56, reflecting ongoing operational losses. This financial profile indicates significant near-term challenges in achieving sustained profitability despite generating substantial top-line revenue.

### Recent Developments

Chegg, Inc. continues to face significant financial headwinds, evidenced by a negative net income of approximately $53 million and a profit margin of -19.96%, resulting in a negative forward P/E ratio. The company's market capitalization has contracted to roughly $82 million, with the stock trading near its 52-week low, reflecting persistent investor concern over its path to profitability. While recent SEC filings indicate no material changes to risk factors or unregistered sales, the absence of positive catalysts and ongoing losses suggest continued volatility for shareholders. Investors should closely monitor upcoming quarterly results for any signs of operational turnaround or strategic shifts aimed at stabilizing revenue and reducing losses.

### SEC Filing Highlights
Chegg is executing a strategic pivot toward a B2B skilling-focused model, though this transformation carries significant operational and financial execution risks amid declining revenue. The company faces intense competitive pressure from both specialized ed-tech rivals and broad AI providers, with Google’s AI Overview specifically cited as a material headwind to user traffic and subscriptions. To counter these threats, Chegg has initiated antitrust litigation against Google, alleging unjust enrichment and seeking to address the shift in search origination away from its platform. Additionally, the business remains vulnerable to content licensing risks and the emergence of proprietary AI tools by educational institutions, which may lower barriers to entry for new competitors.

### Risk Factors

*   **Strategic Execution and Revenue Decline:** The company faces significant challenges in executing its skilling-focused B2B strategy, evidenced by recent revenue declines and difficulties in attracting and retaining customers amidst high turnover in the Academic Services segment and fluctuating engagement in the Skilling business.
*   **Technological Disruption and AI Integration:** Rapid advancements in AI and machine learning pose a threat to traditional educational tools; despite partnerships and investments, these initiatives have not yet generated anticipated student growth, and failure to innovate could severely harm the company’s competitive position.
*   **Intense Competition and Innovation Costs:** The market is highly competitive with numerous rivals possessing greater resources and offering lower prices, while the high cost of developing new technologies and securing regulatory approvals creates substantial financial and operational risks without guaranteed returns.

## Audited (Exec Summary + Outlook)

### Executive Summary
Chegg, Inc. operates in the educational technology sector with annual revenue of $265.51 million, though it currently faces significant profitability challenges with a negative net income of $52.99 million. The stock is notable for its depressed valuation near a market capitalization of approximately $82.05 million, reflecting persistent investor concern over its path to profitability amid a negative forward P/E ratio. The single most important near-term variable is the successful execution of its strategic pivot toward a B2B skilling-focused model, which will determine whether the company can stabilize revenue and mitigate the headwinds posed by AI disruption and intense competition.

### Outlook
The directional outlook for Chegg is cautiously neutral, characterized by a high-risk environment where the success of its B2B skilling pivot is paramount. Key variables to monitor include the traction of the new B2B strategy, the resolution or progress of the antitrust litigation against Google, and the company's ability to manage the technological disruption posed by AI tools. The thesis would strengthen if the B2B segment demonstrates consistent revenue growth and improved unit economics, thereby offsetting declines in the legacy Academic Services business. Conversely, the view would weaken if the company fails to retain customers in the skilling segment, if AI integration continues to erode user traffic without generating proportional revenue, or if competitive pressures from well-capitalized rivals force further margin compression. Investors should remain vigilant for signs of operational stabilization, as the current trajectory suggests continued volatility until a clear path to profitability emerges.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically identify every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections, then evaluate each.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "annual revenue of $265.51 million"
LABEL: SUPPORTED
REASON: The source data lists revenue as $265,512,000, which rounds to $265.51 million, matching the claim exactly.

---

CLAIM: "negative net income of $52.99 million"
LABEL: SUPPORTED
REASON: The source data lists net_income as -$52,997,000, which rounds to -$52.99 million, matching the claim exactly.

---

CLAIM: "market capitalization of approximately $82.05 million"
LABEL: SUPPORTED
REASON: The source data lists market_cap as $82,049,312, which rounds to approximately $82.05 million, matching the claim exactly.

---

CLAIM: "negative forward P/E ratio"
LABEL: SUPPORTED
REASON: The source data lists forward_pe as -10.557143, which is explicitly negative, confirming the directional claim.

---

**OUTLOOK**

The Outlook section contains no specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers. All statements are qualitative and directional (e.g., "cautiously neutral," "consistent revenue growth," "margin compression," "continued volatility"). There are no numerical claims to audit in this section.

---

**SUMMARY TABLE**

| # | Claim | Label |
|---|-------|-------|
| 1 | Annual revenue of $265.51 million | SUPPORTED |
| 2 | Negative net income of $52.99 million | SUPPORTED |
| 3 | Market capitalization of approximately $82.05 million | SUPPORTED |
| 4 | Negative forward P/E ratio | SUPPORTED |

All four auditable quantitative claims in the Executive Summary are supported by the raw source data. The Outlook section contains no quantitative claims requiring audit.
