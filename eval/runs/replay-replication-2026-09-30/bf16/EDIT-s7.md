# EDIT — replay s7 — bf16

## Metadata

ticker: EDIT
arm: bf16
sample: 7
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/EDIT_local-model.md
context_sha256: 35fd11f194201b563e370554975b823c3e44bf58552a16df1b8ce296004ac7c4
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:48:58Z
financial_health_prompt_sha256: 6e28dd79a4b0a230673259741e3f59019f7eed8327bd6bfa00ee7fe0c57b72ae
financial_health_seed: 1070110
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 200
risk_factors_prompt_sha256: 8dbe13748e4cb686acbaf3ffd63e2a8667242e81c33546957fbfc75c59880f21
risk_factors_seed: 1070111
risk_factors_response_model: financial-lora
risk_factors_finish_reason: stop
risk_factors_completion_tokens: 313

## Stock data

{
  "ticker": "EDIT",
  "company_name": "Editas Medicine, Inc.",
  "current_price": 2.69,
  "currency": "USD",
  "market_cap": 413130304.0,
  "forward_pe": -3.5717604,
  "week_52_high": 4.537,
  "week_52_low": 1.66,
  "revenue": 47005000.0,
  "net_income": -73949000.0,
  "profit_margin": -1.57322,
  "sector": "Healthcare",
  "industry": "Biotechnology"
}

<!-- replay-section: Financial Health -->
### Financial Health

Editas Medicine, Inc., trades under the ticker EDIT. It's headquartered in Cambridge, Massachusetts. As of March 9, 2026, it carries a current stock price of $2.69 per share in the United States dollars (USD). 

The company reports a market capitalization of $41.3 billion (US$41.313 billion) as of March 9, 2026. This figure represents the total value of all outstanding shares of the company.

As of March 9, 2026, Editas Medicine reports a net income of -$7.4 billion (US$7.394 billion) as of March 9, 2026. This negative net income indicates a loss position for the company.

In terms of its industry sector, Editas Medicine falls under the Healthcare sector. Within the healthcare industry, it operates within the Biotechnology sub-sector.

<!-- replay-section: Risk Factors -->
### Risk Factors Disclosed

The company faces several significant financial position and capital needs risks, as well as challenges related to development and commercialization:

#### Financial Position and Capital Needs
- **Substantial accumulated losses**: The company has incurred net losses of $160.1 million, $237.1 million, and $153.2 million for 2025, 2024, and 2023 respectively, with an accumulated deficit of $1.6 billion as of December 31, 2025.
- **Expectation of continued losses**: The company expects to incur losses for the foreseeable future and may never achieve profitability.
- **Significant funding requirements**: Substantial additional capital will be needed to continue operations, with existing cash expected to fund operations only into the third quarter of 2027.
- **Limited external funding sources**: The company has limited committed potential external sources of funds beyond contingent payments from collaboration agreements.

#### Development and Commercialization Challenges
- **Early-stage development**: The company is currently only in preclinical testing stages for its most advanced research programs.
- **Time and expense intensive process**: Identifying product candidates and conducting preclinical testing and clinical trials is time-consuming, expensive, and uncertain, taking years to complete.
- **No guarantee of success**: The company may never generate necessary data or results required to obtain marketing approval and achieve product sales.
- **Years to commercialization**: Commercial revenues are not expected for years, if at all.
