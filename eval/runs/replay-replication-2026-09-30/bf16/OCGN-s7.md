# OCGN — replay s7 — bf16

## Metadata

ticker: OCGN
arm: bf16
sample: 7
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/OCGN_local-model.md
context_sha256: a85efe94f652dfb10dbf101a19790b98de76413068dfd1e6bb1d8ab7578a6ef9
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:48:58Z
financial_health_prompt_sha256: 3eee140210bae743edc425ee11073b94901ca28bd56ef96aa941b07763528ba3
financial_health_seed: 1070210
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 215
risk_factors_prompt_sha256: ab30e2574e664ed4b5ee8ccd35e12c65d96d0b4b79915b27030e815c1f2b473e
risk_factors_seed: 1070211
risk_factors_response_model: financial-lora
risk_factors_finish_reason: length
risk_factors_completion_tokens: 512

## Stock data

{
  "ticker": "OCGN",
  "company_name": "Ocugen, Inc.",
  "current_price": 1.0,
  "currency": "USD",
  "market_cap": 339110400.0,
  "forward_pe": -3.7499533,
  "week_52_high": 2.725,
  "week_52_low": 0.97,
  "revenue": 4581000.0,
  "net_income": -81811000.0,
  "profit_margin": 0.0,
  "sector": "Healthcare",
  "industry": "Biotechnology"
}

<!-- replay-section: Financial Health -->
### Financial Health

Ocugen, Inc., trades under the ticker symbol OCGN. It is listed on the Nasdaq Capital Market. 

The company carries a market capitalization of $33.9 billion and a forward P/E ratio of -3.7x. 

In terms of net income, Ocugen reports a net loss of -$8.1 billion over the past year. This represents a net loss per share of -$0.82. 

The company's net cash position stands at $1.0 billion as of December 31, 2025. This represents a net increase of $1.0 billion from the prior quarter. 

As of March 31, 2026, the company has $1.0 billion in cash and cash equivalents. This represents a net decrease of $1.0 billion from the prior quarter. 

Overall, Ocugen, Inc. carries a significant market capitalization and net cash position. However, it reports a substantial net loss over the past year.

<!-- replay-section: Risk Factors -->
### Primary Risk Factors Disclosed

The company discloses several primary risk factors across financial, operational, and competitive dimensions:

#### Financial and Capital Risks
- The company has significant accumulated losses and negative cash flows since its inception. It also faces substantial doubt about the ability to continue as a going concern without additional funding.
- The company requires substantial additional capital to develop product candidates. This may result in potential dilution to stockholders and restrictions on operations.
- The company is subject to debt covenants that limit operating and financial flexibility.

#### Product Development and Regulatory Risks
- The company heavily depends on the success of product candidates. There is no guarantee of successful development, regulatory approval, or commercialization of any such product candidate.
- The company's novel technology platform faces an uncertain regulatory environment. As a result, there can be no assurance regarding the timing or outcome of any regulatory review process.
- The company may face delays or difficulties in patient enrollment for clinical trials due to various reasons such as lack of awareness among patients, inadequate healthcare infrastructure, and other logistical challenges.

#### Operational and Competitive Risks
- The company has no prior experience in marketing, sales, and distribution of biotechnology products. Therefore, there can be no assurance that the company will be able to successfully market, sell, and distribute its product candidates.
- The company faces significant competition from pharmaceutical and biotechnology companies, academic institutions, and research organizations. Additionally, the company relies on third parties for clinical trials, manufacturing, and supply agreements. If these third parties fail to comply with applicable regulations, the company could suffer material adverse effects on its business, results of operations, and financial condition.
- The company may face intellectual property risks, including patent protection uncertainties and reliance on licensed patents from other entities. These risks could have a material adverse effect on the company's business, results of operations, and financial condition.

#### Commercialization Risks
- The company depends on third-party payors for reimbursement at profitable levels. Any failure by the company to obtain adequate reimbursement rates from third-party payors would adversely affect the company's business, results of operations, and financial condition.
- The company faces challenges in establishing and maintaining collaborative relationships with third parties. Failure to establish and maintain effective collaborative relationships with third parties could have a material adverse effect on the company's business, results of operations, and financial condition.
- The company relies on third parties for manufacturing and supply agreements. If these third parties fail to comply with applicable regulations, the company could suffer material adverse effects on its business,
