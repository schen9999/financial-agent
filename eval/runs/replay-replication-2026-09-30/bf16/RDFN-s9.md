# RDFN — replay s9 — bf16

## Metadata

ticker: RDFN
arm: bf16
sample: 9
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/RDFN_local-model.md
context_sha256: 8236ab7e2f7fc4805610fc1530ead6f55e8719854c2b06aa24d0b9288ecfaa8e
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:48:58Z
financial_health_prompt_sha256: 48ca8a32930ef33db942b7661ecdce6cc2cad1e0ba19dd27e446270d358625e1
financial_health_seed: 1090240
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 42
risk_factors_prompt_sha256: 0b1501743eb079f6cd55cf39ff520766234d943c42507e74aa94f2e97864ad1c
risk_factors_seed: 1090241
risk_factors_response_model: financial-lora
risk_factors_finish_reason: stop
risk_factors_completion_tokens: 314

## Stock data

{
  "ticker": "RDFN",
  "company_name": "N/A",
  "currency": "USD"
}

<!-- replay-section: Financial Health -->
### Financial Health

The company reports $10 million in annual revenue and $2 million in net income. Over the past three years, the company has reported consistent growth in both revenue and net income.

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
- **Downturn in Ten Major Metropolitan Markets (Boston, Chicago, Denver, Los Angeles, Maryland, Northern Virginia, Portland, San Diego, San Francisco, and Seattle))**
- **Higher Revenue and Margins in These Markets Compared to Smaller Markets**

#### 3. Technology and Competitive Risks
- **Inability to Maintain Competitive Technology Offerings or Develop New Ones That Meet Customer Expectations**
- **Undetected Errors or Vulnerabilities in Technology Platforms**
- **Challenges in Obtaining and Providing Comprehensive, Accurate Real Estate Listings Data**
- **Intense Competition from Well-Resourced Competitors with Stronger Brand Recognition and Established Relationships**
- **Potential Violations of Fair Lending Laws and Regulations**
- **Difficulty Attracting Specialized Talent and Complying with Evolving AI Regulations**
