# OMER — replay s3 — bf16

## Metadata

ticker: OMER
arm: bf16
sample: 3
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/OMER_local-model.md
context_sha256: 6a470474e224225606c5a4a7c693788f9eaad3a8a9a65bc1f3ca1cc48ba85fc4
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:21:57Z
financial_health_prompt_sha256: 56a830cbcb0ab25f7b9d8ae6224fd808c188acf0677a30f8f502f364aa89d780
financial_health_seed: 30262
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 97
risk_factors_prompt_sha256: dc82012faadabcdf617ca62af3b57a72404c38413c0a709d254ab90fbcf0ddb4
risk_factors_seed: 30263
risk_factors_response_model: financial-lora
risk_factors_finish_reason: stop
risk_factors_completion_tokens: 191

## Stock data

{
  "ticker": "OMER",
  "company_name": "Omeros Corporation",
  "current_price": 20.74,
  "currency": "USD",
  "market_cap": 1501333760.0,
  "pe_ratio": 12.569697,
  "forward_pe": 16.861788,
  "week_52_high": 21.24,
  "week_52_low": 4.06,
  "revenue": 38422000.0,
  "net_income": 116533000.0,
  "profit_margin": 3.2488198,
  "sector": "Healthcare",
  "industry": "Biotechnology"
}

<!-- replay-section: Financial Health -->
### Financial Health

Omeros Corporation trades under the ticker OMER and carries a current price of $20.74 per share in the healthcare sector. It carries a market capitalization of $150.13 billion and a P/E ratio of 12.57x (forward). Over the past five years, it has reported net income of $116.53 million and a net profit margin of 3.25%.

<!-- replay-section: Risk Factors -->
### Primary Risk Factors Disclosed

#### Product Commercialization Risks
- **YARTEMLEA dependency**: The company's profitability is highly dependent on the commercial success of YARTEMLEA, its only commercialized product (FDA-approved in December 2025). Failure to successfully commercialize it could materially adversely affect the business and stock price.
- **Commercialization challenges**: Potential obstacles include lack of physician and patient acceptance, limited marketing and sales experience, reliance on third-party manufacturers and suppliers, and unknown safety risks.

#### Reimbursement and Pricing Risks
- **Inadequate coverage or reimbursement from government and private payers**: This could severely impact revenue prospects.
- **Government and private payers increasingly demand predetermined discounts from list prices**: This could lead to unfavorable terms.
- **Pricing may be subject to government price controls, particularly in foreign jurisdictions like the EU**: This could limit the company's pricing flexibility.
