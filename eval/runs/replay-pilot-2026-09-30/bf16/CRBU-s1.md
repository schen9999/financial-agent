# CRBU — replay s1 — bf16

## Metadata

ticker: CRBU
arm: bf16
sample: 1
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/CRBU_local-model.md
context_sha256: 471084e96f7accedb09a4d4e96977a78dd096d81837c1439ffc0b3621968b8e3
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:21:57Z
financial_health_prompt_sha256: eca2effb8594de62f1eeaaf96e89d6047c10fe40df7162d1189b17478eeab832
financial_health_seed: 10142
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 148
risk_factors_prompt_sha256: 3be5f033c1f0396bd628da9de43cc0da3e4b47305c7904226eaa552e32d53f1d
risk_factors_seed: 10143
risk_factors_response_model: financial-lora
risk_factors_finish_reason: length
risk_factors_completion_tokens: 512

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

Caribou Biosciences, Inc., trades under the ticker CRBU. It is classified under the healthcare sector within the biotechnology sub-industry.

The company carries a current market capitalization of $13.8 billion and a forward P/E ratio of -1.0x (-1.0211109x).

In terms of net income, the company reports a net loss of -$10.3 billion over the last fiscal year.

The company's net income per share stands at -$0.0 per share over the same period.

As of the most recent data available, the company has reported a net loss of -$10.3 billion over the last fiscal year.

<!-- replay-section: Risk Factors -->
### Primary Risk Factors Disclosed

The company discloses several primary risk factors related to its financial position and business operations:

#### Financial and Capital Risks

- **Significant Operating Losses**: The company has incurred substantial net losses since inception ($148.1 million in 2025 and $149.1 million in 2024) with an accumulated deficit of $596.5 million, and anticipates continued losses for the foreseeable future.
- **No Revenue Generation**: The company has not commercialized any products and has never generated revenue from product sales.
- **Need for Additional Financing**: The company currently lacks sufficient funds to conduct its planned pivotal clinical trial for vispa-cel and will require substantial additional capital to complete development and commercialization of its product candidates.
- **Uncertainty of Profitability**: The company is unable to predict when or if it will become profitable, and even if profitable, may not be able to sustain profitability.
- **Risk of Regulatory Approval**: There can be no assurance that the FDA will approve the Company's investigational drug candidate vispa-cel for the treatment of certain cancers. If the FDA does not approve vispa-cel within the specified timeframe, the Company would need to seek alternative regulatory pathways or abandon the development program for vispa-cel.
- **Risk of Failure in Clinical Trials**: There can be no assurance that the Company will successfully complete all preclinical studies and clinical trials required for regulatory approval of vispa-cel. In addition, there can be no assurance that the results obtained from these preclinical studies and clinical trials will be predictive of the results obtained from subsequent preclinical studies and clinical trials. If the Company fails to successfully complete all preclinical studies and clinical trials required for regulatory approval of vispa-cel, the Company would need to seek alternative regulatory pathways or abandon the development program for vispa-cel.
- **Risk of Noncompliance with Regulatory Requirements**: There can be no assurance that the Company will comply with applicable laws and regulations relating to the research, development, testing, manufacturing, storage, packaging, distribution, promotion, advertising, sale, use, disposal, return, exchange, recall, environmental protection, safety, health, quality control, compliance, and other matters. Any non-compliance could result in fines, penalties, civil actions, criminal prosecutions, injunctions, recalls, seizures, suspension of production or services, withdrawal of regulatory clearances or approvals, or similar adverse consequences.
- **Risk of Intellectual Property Infr
