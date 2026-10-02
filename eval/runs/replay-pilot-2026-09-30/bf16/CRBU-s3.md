# CRBU — replay s3 — bf16

## Metadata

ticker: CRBU
arm: bf16
sample: 3
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/CRBU_local-model.md
context_sha256: 471084e96f7accedb09a4d4e96977a78dd096d81837c1439ffc0b3621968b8e3
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:21:57Z
financial_health_prompt_sha256: eca2effb8594de62f1eeaaf96e89d6047c10fe40df7162d1189b17478eeab832
financial_health_seed: 30142
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 75
risk_factors_prompt_sha256: 3be5f033c1f0396bd628da9de43cc0da3e4b47305c7904226eaa552e32d53f1d
risk_factors_seed: 30143
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

Caribou Biosciences, Inc., trades under the ticker CRBU and is headquartered in [City Name], USA. It carries a current price of $1.29 per share in the healthcare sector. The company carries a market capitalization of $13.8 billion and a forward P/E ratio of -1.0x.

<!-- replay-section: Risk Factors -->
### Primary Risk Factors Disclosed

The company discloses several primary risk factors related to its financial position and business operations:

#### Financial and Capital Risks

- **Significant Operating Losses**: The company has incurred substantial net losses since inception ($148.1 million in 2025 and $149.1 million in 2024) with an accumulated deficit of $596.5 million, and anticipates continued losses for the foreseeable future.
- **No Revenue Generation**: The company has not commercialized any products and has never generated revenue from product sales.
- **Need for Additional Financing**: The company currently lacks sufficient funds to conduct its planned pivotal clinical trial for vispa-cel and will require substantial additional capital to complete development and commercialization of its product candidates.
- **Uncertainty of Profitability**: The company is unable to predict when or if it will become profitable, and even if profitable, may not be able to sustain profitability.
- **Potential Regulatory Challenges**: There can be no assurance that the FDA or other applicable authorities will grant the Company's requests for marketing approval or otherwise approve the Company's product candidates. If the Company fails to receive marketing approval for its product candidates, the Company would likely incur significant additional expenses and could experience material adverse effects on its business, results of operations, cash flows and financial condition.
- **Potential Intellectual Property Disputes**: The Company faces intellectual property disputes with third parties over patents and patent applications relating to the Company's technology platform and product candidates. These disputes may result in the loss of valuable rights or the imposition of costly injunctions or damages against the Company. In addition, these disputes may lead to litigation or arbitration proceedings involving the Company, which could have a material adverse effect on the Company's business, results of operations, cash flows and financial condition.
- **Potential Product Liability Claims**: The Company faces product liability claims arising out of the use of its product candidates. Any such claims could cause the Company to incur significant legal fees and expenses and could divert management's attention from the operation of the Company. Such claims could also subject the Company to negative publicity and adversely affect the reputation of the Company and its product candidates.
- **Potential Antitrust Issues**: The Company faces antitrust issues in connection with its research and development efforts and its commercialization plans. Failure to comply with antitrust laws and regulations could result in civil penalties, injunctive relief, exclusion from participation in government contracts, suspension of federal funding, damage awards, reputational harm, and
