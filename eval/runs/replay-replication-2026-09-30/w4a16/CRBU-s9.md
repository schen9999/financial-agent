# CRBU — replay s9 — w4a16

## Metadata

ticker: CRBU
arm: w4a16
sample: 9
served_name: financial-lora-w4a16
source_findings: eval/runs/raw/v924f-findings/CRBU_local-model.md
context_sha256: 471084e96f7accedb09a4d4e96977a78dd096d81837c1439ffc0b3621968b8e3
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:53:35Z
financial_health_prompt_sha256: eca2effb8594de62f1eeaaf96e89d6047c10fe40df7162d1189b17478eeab832
financial_health_seed: 1090100
financial_health_response_model: financial-lora-w4a16
financial_health_finish_reason: stop
financial_health_completion_tokens: 159
risk_factors_prompt_sha256: 3be5f033c1f0396bd628da9de43cc0da3e4b47305c7904226eaa552e32d53f1d
risk_factors_seed: 1090101
risk_factors_response_model: financial-lora-w4a16
risk_factors_finish_reason: stop
risk_factors_completion_tokens: 284

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

Caribou Biosciences, Inc., trades under the ticker CRBU and is headquartered in [City]. It operates within the healthcare sector and falls under the biotechnology industry.

The company reports $1.29 per share in current trading. This represents a net income of -$1.03 billion over the last fiscal year. The company carries a market capitalization of $13.83 billion and a forward P/E ratio of -1.02x.

In terms of revenue, Caribou Biosciences, Inc. reported $1.00 billion in annual revenue over the last fiscal year. Net income has been consistently negative since the company's inception.

The company operates in the healthcare sector and specifically within the biotechnology industry.

<!-- replay-section: Risk Factors -->
### Primary Risk Factors Disclosed

The company discloses several primary risk factors related to its financial position and business operations:

#### Financial and Capital Risks
- **Significant Operating Losses**: The company has incurred substantial net losses since inception ($148.1 million in 2025 and $149.1 million in 2024) with an accumulated deficit of $596.5 million, and anticipates continued losses for the foreseeable future.
- **No Revenue Generation**: The company has not commercialized any products and has never generated revenue from product sales.
- **Need for Additional Financing**: The company currently lacks sufficient funds to conduct its planned pivotal clinical trial for vispa-cel and will require substantial additional capital to complete development and commercialization of its product candidates.
- **Uncertainty of Profitability**: The company is unable to predict when or if it will become profitable, and even if profitable, may not be able to sustain profitability.
- **Operational and Development Risks**
- **Extensive Development Requirements**: The allogeneic cell therapy product candidates are based on new technologies requiring extensive development with significant costs, particularly as they advance through clinical phases with greater numbers of patients.
- **Regulatory and Clinical Uncertainties**: Risks include potential delays in clinical trials, difficulties in receiving regulatory approvals, and failure of clinical trials to meet endpoints.
