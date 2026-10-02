# CRBU — replay s10 — bf16

## Metadata

ticker: CRBU
arm: bf16
sample: 10
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/CRBU_local-model.md
context_sha256: 471084e96f7accedb09a4d4e96977a78dd096d81837c1439ffc0b3621968b8e3
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:48:58Z
financial_health_prompt_sha256: eca2effb8594de62f1eeaaf96e89d6047c10fe40df7162d1189b17478eeab832
financial_health_seed: 1100100
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 236
risk_factors_prompt_sha256: 3be5f033c1f0396bd628da9de43cc0da3e4b47305c7904226eaa552e32d53f1d
risk_factors_seed: 1100101
risk_factors_response_model: financial-lora
risk_factors_finish_reason: stop
risk_factors_completion_tokens: 138

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

Caribou Biosciences, Inc., trades under the ticker CRBU and is headquartered in [City Name], USA. It carries a current price of $1.29 per share in the healthcare sector within the biotechnology industry.

The company reports a market capitalization of $138.3 billion and a forward P/E ratio of -1.0x. This negative P/E ratio indicates that the stock is undervalued relative to its earnings potential.

In terms of net income, Caribou Biosciences, Inc. reports a net loss of -$10.3 billion over the last fiscal year. This significant net loss underscores the substantial losses incurred by the company over the course of the fiscal year.

In summary, Caribou Biosciences, Inc. trades at $1.29 per share in the healthcare sector within the biotechnology industry. It carries a market capitalization of $138.3 billion and a forward P/E ratio of -1.0x, which is considered undervalued. Over the last fiscal year, it reported a net loss of -$10.3 billion.

<!-- replay-section: Risk Factors -->
### Primary Risk Factors Disclosed

#### Financial and Capital Risks
- The company has incurred substantial net losses since inception ($148.1 million in 2025 and $149.1 million in 2024) with an accumulated deficit of $596.5 million, and anticipates continued losses for the foreseeable future.
- The company has not commercialized any products and has never generated revenue from product sales.
- The company needs substantial additional capital to complete development and commercialization of its product candidates.
- The company cannot predict when or if it will become profitable, and even if profitable, may not be able to sustain profitability.
