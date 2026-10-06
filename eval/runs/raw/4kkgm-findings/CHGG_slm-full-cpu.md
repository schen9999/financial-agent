# CHGG — slm-full-cpu

## Metadata

ticker: CHGG
arm: slm-full-cpu
judge_prompt_version: v2
context_sha256: b85bd137cdfa339d3b9f246255a9572164e94ab1a1451798b5bc5c5ad8b06974
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 671, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 191.921, "latency_s_total": 191.921, "parse_failure": 0, "prompt_tokens": 3017, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 421, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 164.284, "latency_s_total": 164.284, "parse_failure": 0, "prompt_tokens": 3042, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 129, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 35.945, "latency_s_total": 35.945, "parse_failure": 0, "prompt_tokens": 701, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 149, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 45.851, "latency_s_total": 45.851, "parse_failure": 0, "prompt_tokens": 695, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 157, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 46.761, "latency_s_total": 46.761, "parse_failure": 0, "prompt_tokens": 493, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 151, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 60.587, "latency_s_total": 60.587, "parse_failure": 0, "prompt_tokens": 751, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 883, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 148.96, "latency_s_total": 148.96, "parse_failure": 0, "prompt_tokens": 1550, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "CHGG",
  "company_name": "Chegg, Inc.",
  "current_price": 0.7137,
  "currency": "USD",
  "market_cap": 79240312.0,
  "forward_pe": -10.195714,
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
Chegg is evolving its learning platform into a skilling-focused business-to-business organization, leveraging existing strengths in professional language learning, workplace readiness, and AI-related skills. This transformation carries significant risks, including organizational, operational, financial, and technological challenges. The company faces the risk of failing to develop novel products, attract or retain customers, or hire the necessary talent in a competitive job market. Additionally, restructuring efforts may lead to a loss of continuity, accumulated knowledge, or efficiency, while diverting management attention from core operations.

**Intense Competition and AI Disruption**
Competition is intensifying across all aspects of Chegg’s business, particularly regarding AI technologies. The company faces rivals in specific verticals, including:
*   **Language Learning:** GoFluent, Speexx, and Duolingo.
*   **Workforce Skilling:** 2U, Inc., Simplilearn, General Assembly, Galvanize, Inc., Flatiron School, Codecademy, DataCamp, and Lambda, Inc.
*   **Study Materials (Chegg Study):** Course Hero, Quizlet, Brainly, and Khan Academy.
*   **Writing Assistance (Chegg Writing):** Grammarly.
*   **Math Solutions (Chegg Math):** Photomath, Gauthmath, and Symbolab.

Furthermore, broad AI providers not specifically focused on education—such as Google, OpenAI, Microsoft, Meta, and Anthropic—pose significant competitive threats. AI technologies may also lower barriers to entry for new competitors.

**Impact of Google’s AI Overview (AIO)**
Google’s expansion of its Artificial Intelligence Overview (AIO) search experience, which began significantly in August 2024, has created headwinds for Chegg. By displaying AI-generated educational content and solutions at the top of search results, Google keeps users on its platform rather than directing them to Chegg’s site. This shift from search origination to destination is expected to reduce website traffic and subscriber growth, potentially materially adversely affecting Chegg’s operating results and financial condition.

**Legal Proceedings**
On February 24, 2025, Chegg filed a complaint in the U.S. District Court for the District of Columbia against Google LLC and Alphabet Inc. The suit asserts federal antitrust claims and common-law unjust enrichment claims related to Google’s expansion of the AIO search experience. The outcome is unpredictable, and the litigation could result in costly expenses, divert management time, and require significant resources.

**Revenue Dependency and Customer Retention**
Chegg’s revenue has declined, and its business relies heavily on attracting new learners and retaining existing ones. The Academic Services business, which constitutes the majority of revenue, depends on small transactions from a widely dispersed student population with high turnover due to graduation. The Skilling business depends on attracting enterprise customers and engaging individual learners. Factors influencing customer base expansion and retention include the availability of free competing content, piracy, localization efforts, changes in customer spending habits, and the effectiveness of sales and marketing strategies.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Failure to Execute Business Strategy:** The company may fail to successfully execute its skilling-focused business-to-business strategy and realize the anticipated benefits of its business transformation and restructuring plan. This includes risks related to organizational, operational, financial, and technological challenges, such as inability to develop novel products, attract or retain customers, or hire the right talent.
*   **Revenue Decline and Customer Retention:** Revenue has declined, and the business depends on attracting new learners and retaining existing ones. The Academic Services business faces high turnover due to student graduation, while the Skilling business depends on attracting enterprise customers and engaging individual learners. Customer base expansion and engagement may fluctuate due to factors like competing free content, piracy, localization challenges, and changes in customer spending habits.
*   **Technological Disruption and AI:** The company faces headwinds from new technologies, particularly AI and machine learning, which provide immediate responses and may disrupt traditional tools. Although the company has partnered with OpenAI and invested in AI initiatives, these efforts have not attracted as many new students as anticipated, adversely affecting the business. Failure to innovate or keep pace with technological developments could harm competitive position and business prospects.
*   **Competition:** The company faces competition in all aspects of its business, including AI, with numerous organizations, many of which have greater resources and offer products at lower prices. Competition is expected to increase as the industry evolves.
*   **Innovation and Investment Risks:** There is no guarantee that investments in new products, services, or initiatives will be successful. Developing new technologies requires significant expenses, and the company may face difficulties in obtaining necessary licenses or regulatory approvals. If competitors develop more cost-effective technologies, the company’s operating results and financial condition could be materially adversely affected.
*   **Restructuring Impacts:** Restructuring efforts may lead to a loss of continuity, accumulated knowledge, or efficiency during transitional periods. These efforts also require significant management and employee time, potentially diverting attention from operating activities and business growth.

## Pre-written sections (judge input)

### Financial Health

Chegg, Inc. (CHGG) currently trades at $0.7137 with a market capitalization of approximately $79.2 million. The company reported annual revenue of $265.5 million but faces significant profitability challenges, evidenced by a net loss of $53.0 million and a negative profit margin of -19.96%. Consequently, the forward P/E ratio is negative at -10.20, reflecting ongoing operational losses. This financial profile indicates substantial near-term risk, as the company continues to struggle with maintaining positive earnings despite its established market presence.

### Recent Developments

Chegg, Inc. continues to face significant financial headwinds, evidenced by a negative net income of approximately $53 million and a profit margin of -19.96%, resulting in a negative forward P/E ratio. The company’s market capitalization has contracted to roughly $79.2 million, with the stock trading near its 52-week low of $0.45, reflecting persistent investor concern over profitability. While recent SEC filings indicate no material changes to risk factors or unregistered equity sales, the absence of dividend yields and ongoing losses suggest limited near-term upside for conservative investors. Consequently, the stock remains a high-risk asset heavily dependent on successful turnaround strategies to restore investor confidence.

### SEC Filing Highlights
Chegg is executing a strategic transformation toward a B2B skilling-focused model, though this shift introduces significant operational and talent acquisition risks amid intense competition from both specialized edtech rivals and broad AI providers. The company faces substantial headwinds from Google’s AI Overview, which redirects user traffic away from Chegg’s platform and threatens to materially impact subscriber growth and operating results. In response, Chegg filed an antitrust lawsuit against Google in February 2025, alleging unjust enrichment and anticompetitive practices related to the AI search feature. Additionally, the company continues to navigate revenue declines driven by high customer turnover in its Academic Services segment and the need to effectively retain enterprise clients in its Skilling business.

### Risk Factors

*   **Strategic Execution and Revenue Volatility:** The company faces significant risks in executing its B2B skilling strategy, including organizational challenges and the potential for continued revenue decline due to high customer turnover in Academic Services and difficulties in retaining enterprise clients.
*   **Technological Disruption and AI Integration:** Rapid advancements in AI and machine learning pose a threat to traditional educational tools; despite investments, these initiatives have not yet attracted anticipated student volumes, and failure to innovate could severely harm the company’s competitive position.
*   **Intense Competition and Innovation Costs:** The market is highly competitive with numerous rivals offering lower-priced alternatives and greater resources, while the high cost of developing new technologies and securing regulatory approvals creates uncertainty regarding the success of future investments.

## Audited (Exec Summary + Outlook)

### Executive Summary
Chegg, Inc. operates in the educational technology sector with a market capitalization of approximately $79.2 million, though it currently faces significant profitability challenges evidenced by a net loss of $53.0 million and a negative profit margin of -19.96%. The stock is notable now as a high-risk turnaround candidate trading near its 52-week low, heavily dependent on successful strategic shifts to restore investor confidence. The single most important near-term variable is the company’s ability to successfully execute its transformation toward a B2B skilling-focused model while mitigating the traffic diversion caused by Google’s AI Overview.

### Outlook
The directional outlook for Chegg is cautiously constructive but heavily contingent on successful strategic pivots and legal outcomes. Key variables to monitor include the traction of the B2B skilling model, the effectiveness of enterprise client retention, and the resolution of the antitrust lawsuit against Google, which directly impacts user traffic and subscriber growth. The thesis would be strengthened by evidence of stabilized Academic Services revenue and successful integration of AI capabilities that drive engagement rather than displacement; conversely, continued revenue declines or adverse rulings in the Google litigation would significantly weaken the investment case. Investors should watch for signs of operational leverage and improved unit economics as primary indicators of a sustainable turnaround.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of approximately $79.2 million"
LABEL: SUPPORTED
REASON: Source data lists market_cap as 79,240,312.0 USD, which rounds to approximately $79.2 million; also confirmed in the Financial Health and Recent Developments pre-written sections.

---

CLAIM: "net loss of $53.0 million"
LABEL: SUPPORTED
REASON: Source data lists net_income as -52,997,000, which rounds to -$53.0 million; confirmed in the Financial Health pre-written section.

---

CLAIM: "negative profit margin of -19.96%"
LABEL: SUPPORTED
REASON: Source data explicitly states profit_margin_pct as -19.96; also confirmed in the Financial Health pre-written section. Cross-check: -52,997,000 / 265,512,000 = -19.96%, within 0.15 pp.

---

CLAIM: "trading near its 52-week low"
LABEL: SUPPORTED
REASON: Current price is $0.7137 and the 52-week low is $0.45; the 52-week high is $1.56. The current price of $0.7137 is closer to the low ($0.45) than to the high ($1.56) — distance to low is $0.2637, distance to high is $0.8463 — so the positional claim holds arithmetically.

---

**OUTLOOK**

---

CLAIM: (no explicit quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers are present in the Outlook section)
LABEL: N/A
REASON: The Outlook section contains only qualitative and directional statements (e.g., "cautiously constructive," "key variables to monitor," "thesis would be strengthened") with no specific quantitative claims, figures, ratios, percentages, price targets, or named numerical milestones to audit.

---

**SUMMARY NOTE:** The Executive Summary contains four auditable quantitative or positional claims, all of which are SUPPORTED. The Outlook section contains no quantitative or forward-looking numerical claims subject to audit under the defined criteria.
