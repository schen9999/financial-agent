# CHGG — slm-full-cpu

## Metadata

ticker: CHGG
arm: slm-full-cpu
judge_prompt_version: v2
context_sha256: 9b3d491bee752d3932039342db898bd01aa8a7a3a49d03c62a53772b47bca0e1
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
llm_by_site: {"rag:highlights": {"calls": 1, "completion_tokens": 770, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 204.855, "latency_s_total": 204.855, "parse_failure": 0, "prompt_tokens": 3023, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "rag:risks": {"calls": 1, "completion_tokens": 565, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 182.694, "latency_s_total": 182.694, "parse_failure": 0, "prompt_tokens": 3012, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:financial_health": {"calls": 1, "completion_tokens": 143, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 38.836, "latency_s_total": 38.836, "parse_failure": 0, "prompt_tokens": 663, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:recent_developments": {"calls": 1, "completion_tokens": 176, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 51.588, "latency_s_total": 51.588, "parse_failure": 0, "prompt_tokens": 657, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:risk_factors": {"calls": 1, "completion_tokens": 201, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 62.522, "latency_s_total": 62.522, "parse_failure": 0, "prompt_tokens": 637, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "section:sec_filing_highlights": {"calls": 1, "completion_tokens": 143, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 80.817, "latency_s_total": 80.817, "parse_failure": 0, "prompt_tokens": 850, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}, "synthesis": {"calls": 1, "completion_tokens": 957, "completion_tokens_unrecorded": 0, "errors": 0, "format_failure": 0, "latency_s_max": 143.207, "latency_s_total": 143.207, "parse_failure": 0, "prompt_tokens": 1704, "prompt_tokens_unrecorded": 0, "repeat_run": 0, "retry": 0, "truncated": 0}}

## Retrieved source context

STOCK DATA:
{
  "ticker": "CHGG",
  "company_name": "Chegg, Inc.",
  "current_price": 0.738,
  "currency": "USD",
  "market_cap": 81938280.0,
  "forward_pe": -10.542857,
  "week_52_high": 1.57,
  "week_52_low": 0.45,
  "revenue": 265512000.0,
  "net_income": -52997000.0,
  "profit_margin": -0.1996,
  "sector": "Consumer Defensive",
  "industry": "Education & Training Services"
}

NEWS ARTICLES:
[]

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
[From Pinecone cache] Based on the provided SEC EDGAR filings for Chegg (ticker: CHGG), the key takeaways regarding the company's business risks, competitive landscape, and strategic challenges are as follows:

**Strategic Transformation and Financial Performance**
*   **Business Pivot:** Chegg is evolving into a skilling-focused business-to-business organization, leveraging existing assets in professional language learning, workplace readiness, and AI-related skills. This transformation involves significant organizational, operational, and financial risks.
*   **Revenue Decline:** The company’s revenue has declined, driven by high turnover in its Academic Services business (due to student graduation) and challenges in attracting and retaining enterprise customers in its Skilling business.
*   **Execution Risks:** There is a risk that the company may fail to realize anticipated benefits from its restructuring plan, potentially leading to a loss of continuity, accumulated knowledge, or efficiency.

**Impact of Artificial Intelligence and Technology**
*   **Google’s AI Overview (AIO):** Google’s expansion of its AI-generated search results (AIO) has created significant headwinds by keeping users on Google’s platform rather than directing them to Chegg. This has led to reductions in website traffic and subscriber growth.
*   **Litigation:** On February 24, 2025, Chegg filed a lawsuit against Google LLC and Alphabet Inc. in the U.S. District Court for the District of Columbia. The suit asserts federal antitrust and common-law unjust enrichment claims regarding Google’s AIO expansion. The outcome is uncertain, and the litigation could be costly and divert management resources.
*   **AI Investment Challenges:** Although Chegg partnered with OpenAI in April 2023 to integrate GPT-4 and began rolling out an AI-powered user experience in September 2023, these initiatives have not attracted as many new students as anticipated. The company acknowledges that new AI technologies provide immediate responses to students, creating ongoing disruption.
*   **Content Licensing Risks:** Chegg has licensed content to other entities that may use it to train AI models competing with Chegg’s own products. Additionally, educational institutions like the University of Michigan are developing their own AI tools.

**Competitive Landscape**
*   **Intense Competition:** Chegg faces competition in all aspects of its business, including AI. Competitors include:
    *   **Language Learning:** GoFluent, Speexx, and Duolingo.
    *   **Workforce Skilling:** 2U, Inc., Simplilearn, General Assembly, Galvanize, Inc., Flatiron School, Codecademy, DataCamp, and Lambda, Inc.
    *   **Study Materials:** Course Hero, Quizlet, Brainly, and Khan Academy.
    *   **Writing Tools:** Grammarly.
    *   **Math Solvers:** Photomath, Gauthmath, and Symbolab.
    *   **General AI:** Google, OpenAI, Microsoft, Meta, and Anthropic, whose broad AI offerings impact education.
*   **Market Entry:** AI technologies may lower barriers to entry, facilitating the arrival of new competitors.

**Customer Acquisition and Retention**
*   **Customer Sensitivity:** The student demographic is characterized by rapidly changing tastes, price sensitivity, and low brand loyalty. Business customers’ willingness to invest is subject to broader economic factors.
*   **Piracy and Sharing:** Unauthorized account sharing and piracy of content pose ongoing risks to maintaining the user base.
*   **Go-to-Market Strategy:** The company must continuously adjust its go-to-market approach to changing customer preferences and ensure its pricing covers costs while remaining competitive. Failure to innovate or price effectively could further harm financial conditions.

RAG — RISK FACTORS:
[From Pinecone cache] The primary risk factors disclosed include:

*   **Strategic Transformation Challenges:** Failure to successfully execute the skilling-focused business-to-business strategy and realize the benefits of business transformation and restructuring. This includes risks related to organizational, operational, financial, and technological challenges, such as developing novel products, attracting customers, hiring talent, and managing the loss of continuity or efficiency during transitions.
*   **Revenue Decline and Customer Retention:** The business depends on attracting new learners and retaining existing ones, particularly given the high turnover rate in the Academic Services sector due to graduation. Revenue is at risk if the company fails to attract new customers, retain existing ones, or increase engagement levels.
*   **Technological Disruption and AI:** The need to innovate and offer new products in response to rapidly evolving technologies, particularly AI. The company faces headwinds from new AI tools that provide immediate responses and may disrupt the business. Although the company has invested in AI initiatives (including a partnership with OpenAI), these efforts have not attracted as many new students as anticipated.
*   **Intense Competition:** The company faces significant competition in all aspects of its business, including from education-focused companies (such as GoFluent, Duolingo, Course Hero, Quizlet, Grammarly, Photomath, and others) and non-education companies with broad AI offerings (such as Google, OpenAI, Microsoft, Meta, and Anthropic).
*   **Impact of Google’s AI Overview (AIO):** Google’s expansion of its AI Overview search experience, which displays AI-generated content at the top of search results, has created headwinds by reducing traffic to the company’s website and keeping users on Google rather than leading them to the company’s services. The company has filed an antitrust and unjust enrichment lawsuit against Google regarding this issue.
*   **Content Piracy and Unauthorized Use:** Risks associated with piracy, unauthorized account sharing of subscription services, and the unauthorized use of content. Additionally, licensed content may be used by other entities to train AI models that compete with the company’s products.
*   **Innovation and Investment Risks:** The uncertainty of new product markets, the significant expenses required to develop new technologies, and the risk that new products or services may not be successful or may not generate sufficient revenue to justify the investments.
*   **Legal and Regulatory Risks:** The potential for costly litigation, including the ongoing lawsuit against Google, which could divert management time and resources. There are also risks related to obtaining necessary licenses and regulatory approvals for new products.
*   **Market and Economic Factors:** The willingness of business customers to invest in worker training is subject to economic factors, while the student demographic is characterized by rapidly changing tastes, preferences, and price sensitivity.

## Pre-written sections (judge input)

### Financial Health

Chegg, Inc. (CHGG) currently trades at $0.738 with a market capitalization of approximately $81.9 million, reflecting significant downward pressure from its 52-week high of $1.57. The company reported annual revenue of $265.5 million but is currently unprofitable, evidenced by a net income of -$52.9 million and a negative profit margin of -19.96%. Consequently, the forward P/E ratio is negative at -10.54, indicating that earnings expectations remain depressed. This financial profile highlights substantial near-term challenges in achieving sustainable profitability despite maintaining a baseline revenue stream.

### Recent Developments

Chegg, Inc. filed its Annual Report on Form 10-K on March 9, 2026, and its Quarterly Report on Form 10-Q on August 6, 2026, with both filings highlighting persistent risks that could adversely affect the company's financial condition and stock price. The most recent 10-Q filing confirmed no material changes to the risk factors previously disclosed in the annual report, indicating a stable but challenging operational environment. Additionally, the company reported no unregistered sales of equity securities during the quarter ended June 30, 2026, while detailing stock repurchase activities. Investors should remain cautious as the company continues to navigate significant financial headwinds, evidenced by a negative profit margin of nearly 20% and a market capitalization under $82 million.

### SEC Filing Highlights
Chegg is executing a strategic pivot toward a B2B skilling model, though this transition has contributed to recent revenue declines driven by high student turnover and challenges in enterprise customer retention. The company faces significant headwinds from Google’s AI Overview, which has reduced web traffic and subscriber growth, prompting Chegg to file an antitrust lawsuit against Google in February 2025. Despite partnerships with OpenAI and internal AI initiatives, Chegg acknowledges that rapid advancements in generative AI continue to disrupt its core academic services and complicate customer acquisition. Additionally, the firm contends with intense competition across all business segments and risks associated with content licensing potentially fueling rival AI models.

### Risk Factors

*   **Technological Disruption and Competitive Pressure:** The company faces significant headwinds from rapidly evolving AI technologies and intense competition from both specialized ed-tech firms and major tech giants (e.g., Google, OpenAI). Specifically, Google’s AI Overview has reduced organic traffic, while new AI tools threaten to disrupt traditional learning models, despite Chegg’s own AI investments.
*   **Strategic Transformation and Execution Risks:** Success depends on the effective execution of a strategic shift toward a B2B skilling-focused model. Failure to manage organizational, operational, and technological challenges during this transition—such as attracting enterprise customers and retaining talent—could hinder growth and profitability.
*   **Customer Retention and Revenue Volatility:** Revenue is highly sensitive to customer acquisition and retention, particularly given the high churn rate inherent in the student demographic due to graduation. Additionally, economic factors may reduce business willingness to invest in worker training, while price sensitivity among students limits pricing power.

## Audited (Exec Summary + Outlook)

### Executive Summary
Chegg, Inc. operates in the ed-tech sector with a market capitalization of approximately $81.9 million, currently navigating a challenging financial landscape marked by a negative profit margin of -19.96% and a net income of -$52.9 million. The stock is notable now as it attempts to pivot toward a B2B skilling model while simultaneously litigating against Google’s AI Overview, which has significantly impacted its organic traffic and subscriber growth. The single most important near-term variable is the successful execution of this strategic transition and the ability to retain enterprise customers amidst intense competitive pressure from major tech giants.

### Outlook
The directional outlook for Chegg is cautiously neutral, heavily dependent on the successful execution of its strategic pivot to a B2B skilling model. Key variables to monitor include the rate of enterprise customer acquisition, the stability of the new revenue mix, and the legal and competitive dynamics surrounding Google’s AI Overview. The thesis would strengthen if the company demonstrates consistent progress in reducing reliance on high-churn student subscriptions and shows tangible traction in the B2B sector; conversely, the view would weaken if the transition fails to offset revenue declines or if competitive pressures from AI-driven alternatives continue to erode market share without corresponding margin improvements.

---
*This brief is for informational purposes only and does not constitute financial advice.*

## Judge findings

I will now systematically evaluate every specific quantitative figure, price target, threshold, ratio, metric, percentage, named product milestone, or forward-looking number in the **Executive Summary** and **Outlook** sections.

---

**EXECUTIVE SUMMARY**

---

CLAIM: "market capitalization of approximately $81.9 million"
LABEL: SUPPORTED
REASON: The raw source data lists `market_cap: 81938280.0`, which rounds to $81.9 million, and the Financial Health section explicitly states "approximately $81.9 million."

---

CLAIM: "negative profit margin of -19.96%"
LABEL: SUPPORTED
REASON: The raw source data lists `profit_margin: -0.1996`, which equals -19.96%, confirmed in both the Financial Health and Recent Developments pre-written sections.

---

CLAIM: "net income of -$52.9 million"
LABEL: SUPPORTED
REASON: The raw source data lists `net_income: -52997000.0`, which rounds to -$53.0 million; however, the Financial Health pre-written section (a direct input to the model) states "-$52.9 million," and -52,997,000 rounds to -$53.0 million at one decimal place. Checking: $52,997,000 = $53.0 million to one decimal, not $52.9 million. The claim of -$52.9 million does not match the source figure of -$52,997,000 (which rounds to -$53.0 million).
LABEL: UNSUPPORTED
REASON: The source data shows net income of -$52,997,000, which rounds to -$53.0 million, not -$52.9 million as claimed; the $0.1 million discrepancy exceeds the 0.15 percentage point tolerance for derived figures and represents a factual rounding error.

*(Correcting my entry above — reissuing as a single clean entry:)*

CLAIM: "net income of -$52.9 million"
LABEL: UNSUPPORTED
REASON: The raw source data shows `net_income: -52997000.0`, which rounds to -$53.0 million, not -$52.9 million; the pre-written Financial Health section also states -$52.9 million, but that figure itself misrounds the source data, and no source figure of -$52.9 million exists.

---

CLAIM: "pivot toward a B2B skilling model"
LABEL: SUPPORTED
REASON: The SEC Filing Highlights and RAG sections explicitly describe Chegg "evolving into a skilling-focused business-to-business organization" and "executing a strategic pivot toward a B2B skilling model."

---

CLAIM: "litigating against Google's AI Overview"
LABEL: SUPPORTED
REASON: The RAG — SEC Highlights section confirms Chegg filed a lawsuit against Google LLC and Alphabet Inc. on February 24, 2025, asserting antitrust and unjust enrichment claims regarding Google's AI Overview expansion.

---

**OUTLOOK**

---

*(The Outlook section contains no specific quantitative figures, price targets, thresholds, ratios, metrics, percentages, named product milestones, or forward-looking numbers. All statements are qualitative and directional in nature — e.g., "cautiously neutral," "rate of enterprise customer acquisition," "stability of the new revenue mix," "consistent progress," "tangible traction." None of these constitute quantitative or specifically measurable claims subject to the audit criteria.)*

No auditable quantitative or forward-looking numerical claims are present in the Outlook section.

---

**SUMMARY TABLE**

| Claim | Label |
|---|---|
| Market cap ~$81.9 million | SUPPORTED |
| Profit margin -19.96% | SUPPORTED |
| Net income -$52.9 million | UNSUPPORTED |
| B2B skilling pivot | SUPPORTED |
| Litigating against Google's AI Overview | SUPPORTED |
