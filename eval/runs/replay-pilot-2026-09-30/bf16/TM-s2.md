# TM — replay s2 — bf16

## Metadata

ticker: TM
arm: bf16
sample: 2
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/TM_local-model.md
context_sha256: 54dcc3ff59319df8036d5400cfaeb954cf2cdd979008d1d9f1fb1698728acc2f
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:21:57Z
financial_health_prompt_sha256: 5256782785d900ac5df9b0dba279912684e78232c6b18a6c8918cb097c3e5a71
financial_health_seed: 20352
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 144
risk_factors_prompt_sha256: 6cbd67074edc2791639aaf572907dc4de57db62b53f125c4556df297905a30c0
risk_factors_seed: 20353
risk_factors_response_model: financial-lora
risk_factors_finish_reason: stop
risk_factors_completion_tokens: 169

## Stock data

{
  "ticker": "TM",
  "company_name": "Toyota Motor Corporation",
  "current_price": 190.36,
  "currency": "USD",
  "market_cap": 225421164544.0,
  "pe_ratio": 8.509611,
  "forward_pe": 12.063372,
  "week_52_high": 248.9,
  "week_52_low": 166.1,
  "revenue": 51957024686080.0,
  "net_income": 4483796959232.0,
  "profit_margin": 0.0863,
  "dividend_yield": 3.26,
  "sector": "Consumer Cyclical",
  "industry": "Auto Manufacturers"
}

<!-- replay-section: Financial Health -->
### Financial Health
Toyota Motor Corporation trades at $190.36 per share in the consumer cyclical sector. The company carries a market capitalization of $2.25 trillion and a P/E ratio of 8.5x (12.1x forward), a premium valuation. Over the past year, the stock has ranged between $166.10 and $248.90. The net income over the last fiscal year was $44.8 billion, representing a net profit margin of 8.6%. The dividend yield is currently 3.26%, which represents an annualized dividend payment of $0.326 per share.

<!-- replay-section: Risk Factors -->
### Risk Factors

- The global automotive industry is highly competitive and subject to rapid technological change.
- We may not achieve or maintain profitability in our business segments.
- Our ability to successfully implement our strategic initiatives will depend on our ability to effectively manage our growth.
- Our success depends upon our ability to attract and retain qualified personnel.
- Our future financial performance could be adversely affected if we fail to comply with applicable laws and regulations relating to environmental protection and safety.
- Our future financial performance could be adversely affected if we fail to comply with applicable laws and regulations relating to data privacy and security.
- Our future financial performance could be adversely affected if we fail to comply with applicable laws and regulations relating to labor and employment matters.
- Our future financial performance could be adversely affected if we fail to comply with applicable laws and regulations relating to tax matters.
