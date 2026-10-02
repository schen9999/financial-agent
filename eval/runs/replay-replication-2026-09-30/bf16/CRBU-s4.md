# CRBU — replay s4 — bf16

## Metadata

ticker: CRBU
arm: bf16
sample: 4
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/CRBU_local-model.md
context_sha256: 471084e96f7accedb09a4d4e96977a78dd096d81837c1439ffc0b3621968b8e3
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:48:58Z
financial_health_prompt_sha256: eca2effb8594de62f1eeaaf96e89d6047c10fe40df7162d1189b17478eeab832
financial_health_seed: 1040100
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 142
risk_factors_prompt_sha256: 3be5f033c1f0396bd628da9de43cc0da3e4b47305c7904226eaa552e32d53f1d
risk_factors_seed: 1040101
risk_factors_response_model: financial-lora
risk_factors_finish_reason: length
risk_factors_completion_tokens: 512

## Stock data

{
  "ticker": "CRBU",
  "company_name": "Caribou Biosciences, Inc.",
  "current_price": 1.29,
  "currency": "USD",
  "market_cap": 138297680.0,
  "forward_pe": -1.0211109,
  "week_52_high": 3.535,
  "week_52_low": 1.25,
  "revenue": 10035000.0,
  "net_income": -103403000.0,
  "profit_margin": 0.0,
  "sector": "Healthcare",
  "industry": "Biotechnology"
}

<!-- replay-section: Financial Health -->
### Financial Health

Caribou Biosciences, Inc., trades under the ticker CRBU and is headquartered in [Location]. It carries a current market price of $1.29 per share in the United States.

The company reports net income of -$10.3 billion over the last fiscal year. This represents a net loss of $10.3 billion compared to $10.3 billion in the prior year.

In terms of revenue, the company reported $10.0 million in net revenue over the last fiscal year. This compares to $10.0 million in net revenue in the prior year.

The company's sector is Healthcare and its industry is Biotechnology.

<!-- replay-section: Risk Factors -->
### Primary Risk Factors Disclosed

The company discloses several primary risk factors related to its financial position and business operations:

#### Financial and Capital Risks

- **Significant Operating Losses**: The company has incurred substantial net losses since inception ($148.1 million in 2025 and $149.1 million in 2024) with an accumulated deficit of $596.5 million, and anticipates continued losses for the foreseeable future.
- **No Revenue Generation**: The company has not commercialized any products and has never generated revenue from product sales.
- **Need for Additional Financing**: The company currently lacks sufficient funds to conduct its planned pivotal clinical trial for vispa-cel and will require substantial additional capital to complete development and commercialization of its product candidates.
- **Uncertainty of Profitability**: The company is unable to predict when or if it will become profitable, and even if profitable, may not be able to sustain profitability.
- **Potential Dilution of Equity Interests**: The company's stock price could decline significantly due to various factors including but not limited to changes in market conditions, competition, industry trends, economic conditions, political events, natural disasters, pandemics, health crises, public health emergencies, government regulations, compliance issues, litigation matters, intellectual property disputes, data breaches, cyber attacks, information security incidents, privacy violations, data protection breaches, and other similar developments that affect the Company's business, results of operations, cash flows, financial condition, liquidity, and prospects.
- **Potential Impact of Changes in Accounting Standards**: The adoption of new accounting standards, such as those issued by the Financial Accounting Standards Board ("FASB") or another standard-setting body), may impact the Company's reported financial results and disclosures. These impacts may include, among others: (i) changes in the valuation of assets; (ii) changes in the measurement of liabilities; (iii) changes in the recognition and measurement of income taxes; (iv) changes in the recognition and measurement of deferred tax assets and liabilities; (v) changes in the recognition and measurement of equity instruments; (vi) changes in the recognition and measurement of derivative instruments; (vii) changes in the recognition and measurement of non-controlling interests; (viii) changes in the recognition and measurement of discontinued operations; (ix) changes in the recognition and measurement of extraordinary items; (x) changes in the recognition and measurement of comprehensive income; (xi) changes in the recognition and measurement of net income attributable
