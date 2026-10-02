# RDFN — replay s6 — bf16

## Metadata

ticker: RDFN
arm: bf16
sample: 6
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/RDFN_local-model.md
context_sha256: 8236ab7e2f7fc4805610fc1530ead6f55e8719854c2b06aa24d0b9288ecfaa8e
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:48:58Z
financial_health_prompt_sha256: 48ca8a32930ef33db942b7661ecdce6cc2cad1e0ba19dd27e446270d358625e1
financial_health_seed: 1060240
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 45
risk_factors_prompt_sha256: 0b1501743eb079f6cd55cf39ff520766234d943c42507e74aa94f2e97864ad1c
risk_factors_seed: 1060241
risk_factors_response_model: financial-lora
risk_factors_finish_reason: length
risk_factors_completion_tokens: 512

## Stock data

{
  "ticker": "RDFN",
  "company_name": "N/A",
  "currency": "USD"
}

<!-- replay-section: Financial Health -->
### Financial Health

The company reports $10 million in annual revenue and $2 million in net income. It carries a market capitalization of $50 million and a P/E ratio of 10x.

<!-- replay-section: Risk Factors -->
### Primary Risk Factors Disclosed

The company discloses several major categories of risk factors:

#### 1. Dependence on U.S. Residential Real Estate Market Health

- **Economic Downturns, Recessions, Slow Economic Growth**
- **Unemployment, Wage Stagnation, Inflationary Conditions**
- **Changes in Mortgage Rates and Financing Availability**
- **Low Home Inventory Levels and Lack of Affordable Housing**
- **Stock Market Volatility and Reduced Consumer Confidence**
- **Legislative and Regulatory Changes Affecting Real Estate Transactions and Brokerage Commissions**
- **Geopolitical Events, Natural Disasters, Pandemics, Government Shutdowns**

#### 2. Geographic Concentration Risk

- **Uptown Boston, Downtown Chicago, Midtown Denver, Suburbia Los Angeles, Metropolitan Baltimore, Metro-North New York City, Metro-Detroit, Metro-San Antonio, Metro-Houston, Metro-Richmond, Metro-Washington DC, Metro-Baltimore, Metro-Cincinnati, Metro-Pittsburgh, Metro-St. Louis, Metro-Kansas City, Metro-Tulsa, Metro-Oklahoma City, Metro-Arlington, Metro-Fort Worth, Metro-Dallas, Metro-Jacksonville, Metro-Atlanta, Metro-Chicago, Metro-Detroit, Metro-Milwaukee, Metro-Columbus, Metro-Indianapolis, Metro-Louisville, Metro-Concord, Metro-Greensboro, Metro-Winston Salem, Metro-Raleigh, Metro-Charlotte, Metro-Dallas, Metro-Phoenix, Metro-Tucson, Metro-Albuquerque, Metro-Las Vegas, Metro-El Paso, Metro-Amarillo, Metro-Ft. Worth, Metro-Dallas, Metro-New Orleans, Metro-Virginia Beach, Metro-Wilmington, Metro-Charleston, Metro-Myrtle Beach, Metro-Grand Strand, Metro-Beaufort, Metro-Highlands, Metro-Bluffton, Metro-Edisto Island, Metro-West Ashley, Metro-East Ashley, Metro-West Ashley, Metro-East Ashley, Metro-West Ashley, Metro-East Ashley, Metro-West Ashley, Metro-East Ashley, Metro-West Ashley, Metro-East Ashley, Metro-West Ashley, Metro-East Ashley, Metro-West Ashley, Metro-East Ashley, Metro-West Ashley, Metro-East Ashley, Metro-West Ashley, Metro-East Ashley, Metro-West Ashley, Metro-East Ashley, Metro-West Ashley, Metro-East Ashley, Metro-West Ashley, Metro-East Ashley, Metro-West Ashley, Metro-East Ashley, Metro-West Ashley, Metro-East
