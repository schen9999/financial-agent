# VERV — replay s1 — bf16

## Metadata

ticker: VERV
arm: bf16
sample: 1
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/VERV_local-model.md
context_sha256: a6cff528aacd4fc17eefdfe642c93058b746cad093e890e8074b49c9c0d0a0ef
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:48:58Z
financial_health_prompt_sha256: b95d74ec0b76a9217d4409da81081054c8780fe9165b4f6d2c8385b089337bd6
financial_health_seed: 1010360
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 242
risk_factors_prompt_sha256: 80c1d0e24c67124ec7ad66f754dbbaf5cdde2540457cc6d0fa33d7230da3b591
risk_factors_seed: 1010361
risk_factors_response_model: financial-lora
risk_factors_finish_reason: stop
risk_factors_completion_tokens: 282

## Stock data

{
  "ticker": "VERV",
  "company_name": "N/A",
  "currency": "USD"
}

<!-- replay-section: Financial Health -->
### Financial Health

**Balance Sheet Summary:**
As of March 31, 2025, Verve Therapeutics reported total assets of $614,163. This represents an increase of $33,584 over its December 31, 2024, balance sheet figure of $580,579.

In terms of liabilities, as of March 31, 2025, Verve Therapeutics had total liabilities of $114,699. This is a decrease of $10,410 over its December 31, 2024, balance sheet figure of $125,119.

The company's equity stands at $499,464 as of March 31, 2025. This represents a decrease of $10,410 over its December 31, 2024, balance sheet figure of $509,874.

This comprehensive overview highlights Verve Therapeutics' robust financial health as of March 31, 2025.

<!-- replay-section: Risk Factors -->
### Primary Risk Factors Disclosed

The company discloses several significant risk factors related to its financial position and operations:

#### Financial Losses and Lack of Revenue
- The company has incurred substantial losses since inception with no approved products for sale.
- Net losses were $198.7 million, $200.1 million, and $157.4 million for 2024, 2023, and 2022 respectively.
- Accumulated deficit reached $743.0 million as of December 31, 2024.
- No revenue has been generated from product sales to date.

#### Need for Additional Capital
- The company currently lacks a credit facility or committed sources of capital.
- Substantial additional funding is required to continue operations, particularly for:
  - Ongoing and planned clinical trials
  - Research, development, and preclinical testing
  - Potential commercialization expenses if marketing approval is obtained
  - Operating costs as a public company

#### Product Development Uncertainties
- The company has not yet completed a clinical trial of any product candidate.
- Development timelines are uncertain and may take many years before commercialization.
- Success requires completing preclinical testing, clinical trials, obtaining regulatory approvals, and achieving market acceptance.
- There is no assurance of profitability even if products are successfully developed and approved.
