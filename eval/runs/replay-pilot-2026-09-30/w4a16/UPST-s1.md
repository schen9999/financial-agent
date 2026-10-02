# UPST — replay s1 — w4a16

## Metadata

ticker: UPST
arm: w4a16
sample: 1
served_name: financial-lora-w4a16
source_findings: eval/runs/raw/v924f-findings/UPST_local-model.md
context_sha256: 82f2419f5757a2738079b1a202afd2ca89800e6b096575f15824974a67eee97e
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:24:25Z
financial_health_prompt_sha256: b1d8d0b500695b88aaa1fee4758ddf6ae5f7f80a9be40e7caed8decd1d965b65
financial_health_seed: 10392
financial_health_response_model: financial-lora-w4a16
financial_health_finish_reason: stop
financial_health_completion_tokens: 144
risk_factors_prompt_sha256: 335526a71b996515b374610ab4a47c80aaddf7b4398c94955a5f4813c4d3fc5b
risk_factors_seed: 10393
risk_factors_response_model: financial-lora-w4a16
risk_factors_finish_reason: stop
risk_factors_completion_tokens: 320

## Stock data

{
  "ticker": "UPST",
  "company_name": "Upstart Holdings, Inc.",
  "current_price": 24.45,
  "currency": "USD",
  "market_cap": 2379304192.0,
  "pe_ratio": 46.13208,
  "forward_pe": 7.034028,
  "week_52_high": 64.15,
  "week_52_low": 23.965,
  "revenue": 1285890048.0,
  "net_income": 60334000.0,
  "profit_margin": 0.046919998,
  "sector": "Financial Services",
  "industry": "Credit Services"
}

<!-- replay-section: Financial Health -->
### Financial Health
Investing in our common stock involves a high degree of risk. The risks and uncertainties described below should be carefully considered, together with all of the other information in this Annual Report on Form 10-K, including the section titled Management's Discussion and Analysis of Financial Condition and Results of Operations and our condensed consolidated financial statements and related notes, before making a decision to invest in our common stock. Our business, financial condition, results of operations, or prospects could also be harmed by risks and uncertainties not currently known to us or that we currently do not believe are material. If any of the risks actually occur, our business, financial condition, results of operations, and prospects could be adversely affected.

<!-- replay-section: Risk Factors -->
### Primary Risk Factors Disclosed

The company discloses numerous material risk factors affecting its business, which can be categorized into several key areas:

#### Economic and Market Risks
- Adverse economic conditions, uncertainty, and volatility that impact borrower demand, approval rates, and loan origination volume
- Reduced capital supply from lending partners and institutional investors during economic downturns
- Borrowers with limited credit history being disproportionately affected by inflation, higher interest rates, and unemployment

#### Funding and Capital Risks
- Inability to maintain diverse and resilient loan funding from institutional investors
- Dependence on committed capital and co-investment arrangements that expose the company to credit risk compensation obligations
- Risks associated with asset-backed securitizations, warehouse credit facilities, and whole loan sale arrangements
- Potential repurchase obligations if loan representations and warranties prove inaccurate

#### Operational and Technology Risks
- Failure to improve or maintain effective artificial intelligence models for credit assessment
- Significant disruptions or failures in technology systems, including the AI lending platform
- Inability to approve a sufficient number of borrowers for loans

#### Business Concentration Risks
- Heavy reliance on a limited number of lending partners for a significant portion of loan originations and revenue
- Dependence on a single loan product historically
- Concentration of operations in U.S. consumer credit markets

#### Additional Risks
- Inability to maintain relationships with loan aggregators
- Security breaches and data protection failures
- Regulatory compliance challenges across evolving laws and regulations
- Reputation and brand management issues
- Loan servicing and collections management risks
