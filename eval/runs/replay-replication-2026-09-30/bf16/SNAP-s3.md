# SNAP — replay s3 — bf16

## Metadata

ticker: SNAP
arm: bf16
sample: 3
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/SNAP_local-model.md
context_sha256: 50eb8df0f9b4c781ffcd5abe298b4cc1c3fe2051a9fe1f26847932d63f939808
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:48:58Z
financial_health_prompt_sha256: daf8b085148ad64347dc1897eb08103c7ee4b7df66155e7c6be16c4deaea72d8
financial_health_seed: 1030300
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 123
risk_factors_prompt_sha256: cb1b21aceff3bcde977c5167092d8d44f85b40112d55e3d8d36ab1235b77dc61
risk_factors_seed: 1030301
risk_factors_response_model: financial-lora
risk_factors_finish_reason: stop
risk_factors_completion_tokens: 274

## Stock data

{
  "ticker": "SNAP",
  "company_name": "Snap Inc.",
  "current_price": 5.29,
  "currency": "USD",
  "market_cap": 8946436096.0,
  "forward_pe": 6.8217573,
  "week_52_high": 9.13,
  "week_52_low": 3.81,
  "revenue": 6351084032.0,
  "net_income": -311243008.0,
  "profit_margin": -0.04901,
  "sector": "Communication Services",
  "industry": "Internet Content & Information"
}

<!-- replay-section: Financial Health -->
### Financial Health
Snap Inc., a company listed under the ticker SNAP, trades at $5.29 per share in the communication services sector. It carries a market capitalization of $894.6 billion and a forward P/E ratio of 6.8x. Over the past year, it has seen its stock price rise to $9.13 from $3.81. In terms of net income, Snap reported a net loss of $31.1 billion over the last fiscal year. This represents a net loss of $0.049 per share.

<!-- replay-section: Risk Factors -->
### Primary Risk Factors Disclosed

The company discloses several significant risk factors affecting its business:

#### User Engagement and Retention Risks
- Declining or stagnant daily active user (DAU) growth rates, with the company having 474 million DAUs in the quarter ended December 31, 2025.
- Low barriers to entry and switching costs that make it easy for users to migrate to competing platforms.
- The majority of users being 18-34 years old, a demographic that may be less brand loyal and more trend-driven.
- Difficulty penetrating other demographic groups.
- Competition from other companies for user attention and engagement.
- Various factors that could negatively affect user retention, including poor product performance, inadequate user experience, security concerns, and regulatory changes.

#### Advertising Revenue Concentration
- Heavy dependence on advertising revenue, which accounted for approximately 87% of total revenue in 2025, 91% in 2024, and 96% in 2023.
- Most advertisers lack long-term commitments and could reduce spending or leave.
- Some customers with meaningful budgets contribute significantly to revenue, creating concentration risk.
- Advertisers may view certain advertising solutions as experimental or unproven.
- Economic or political instability could negatively impact advertiser budgets and spending.
