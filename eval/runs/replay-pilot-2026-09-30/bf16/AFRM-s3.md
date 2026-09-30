# AFRM — replay s3 — bf16

## Metadata

ticker: AFRM
arm: bf16
sample: 3
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/AFRM_local-model.md
context_sha256: 5f1c0ef5993c907aaa7ef4df23dc1e315f145515cdae951dcc8f9bb84fd26035
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:21:57Z
financial_health_prompt_sha256: 893e4c490ef862d8e3356084a2cc10182220026d5a7907105f5139cea1d8d51c
financial_health_seed: 30052
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 55
risk_factors_prompt_sha256: a33285d4dda1f5eeb86d1b04e842241674a68c169afca5e895a1a9056b539c7d
risk_factors_seed: 30053
risk_factors_response_model: financial-lora
risk_factors_finish_reason: length
risk_factors_completion_tokens: 512

## Stock data

{
  "ticker": "AFRM",
  "company_name": "Affirm Holdings, Inc.",
  "current_price": 68.09,
  "currency": "USD",
  "market_cap": 22975010816.0,
  "pe_ratio": 12.312838,
  "forward_pe": 14.103469,
  "week_52_high": 90.44,
  "week_52_low": 42.095,
  "revenue": 4261082112.0,
  "net_income": 1929793024.0,
  "profit_margin": 0.45289,
  "sector": "Financial Services",
  "industry": "Credit Services"
}

<!-- replay-section: Financial Health -->
### Financial Health
Affirm Holdings, Inc., trades as AFRM. It carries a current market price of $68.09 per share in the financial services sector. The company reports net income of $19.3 billion over the past fiscal year.

<!-- replay-section: Risk Factors -->
### Primary Risk Factors Disclosed

The company faces several material risk factors across its business operations:

#### Commercial Partner and Consumer Risks
- **Concentration Risk:** The reliance on a small number of commercial partners creates concentration risk.
- **Competitive Landscape:** The highly competitive industry with low barriers to entry presents significant challenges.
- **Consumer Creditworthiness:** The impact of general economic conditions and consumer creditworthiness on revenue is substantial.

#### Operational and Financial Risks
- **Revenue Growth:** The dependence on specific originating bank partners (Celtic Bank and Lead Bank) for loan origination exposes the company to operational and financial risks.
- **Loan Performance Issues:** The inability to sustain revenue and GMV growth rates significantly impacts the company's ability to generate profits.
- **Funding Sources:** The reliance on various funding sources that may not be renewed or available on acceptable terms introduces operational and financial risks.
- **Potential Loan Performance Issues:** The potential loan performance issues could result in financial losses.
- **International Expansion Challenges:** The challenges with international expansion further exacerbate these risks.

#### Competitive and Market Risks
- **Competition:** The competition from legacy payment methods, mobile wallets, and other pay-over-time solutions intensifies market dynamics.
- **General Economic Conditions and Consumer Creditworthiness:** The impact of general economic conditions and consumer creditworthiness on revenue is substantial.
- **Interest Rate Increases:** An increase in interest rates could negatively impact the company’s net income and overall financial health.

#### Regulatory, Legal, and Operational Risks
- **Extensive Regulatory Oversight and Potential Changes in Laws and Regulations:** The extensive regulatory oversight and potential changes in laws and regulations pose significant operational and financial risks.
- **Litigation, Regulatory Actions, and Compliance Issues:** The possibility of litigation, regulatory actions, and compliance issues can lead to significant operational and financial risks.
- **Cyber-Attacks and Data Security Threats:** The threat of cyber-attacks and data security threats can have severe operational and financial consequences.
- **Service Disruptions on the Platform:** The possibility of service disruptions on the platform can cause significant operational and financial risks.
- **Loss of Key Personnel, Including the Founder and CEO:** The loss of key personnel, including the founder and CEO, can have severe operational and financial implications.
- **Challenges with International Expansion:** The challenges with international expansion can introduce additional operational and financial risks.
- **Significant Quarterly Result Fluctuations:** The possibility of significant quarterly result fluctuations can have severe operational and financial consequences.
-
