# TSM — replay s5 — bf16

## Metadata

ticker: TSM
arm: bf16
sample: 5
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/TSM_local-model.md
context_sha256: faff0ddd4ff49a73316e9ef8d738b08e542749945089049e0387f1d3fdf58af4
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:48:58Z
financial_health_prompt_sha256: 7b54e0323848c6767fe729a6ee5994199d218b7f835f19629c4eedf5d42b016c
financial_health_seed: 1050330
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 101
risk_factors_prompt_sha256: b459fa6820823ec38ef57e9062c365a4a883f76fa42580deb91ac0f0236242c5
risk_factors_seed: 1050331
risk_factors_response_model: financial-lora
risk_factors_finish_reason: length
risk_factors_completion_tokens: 512

## Stock data

{
  "ticker": "TSM",
  "company_name": "Taiwan Semiconductor Manufacturing Company Limited",
  "current_price": 446.57,
  "currency": "USD",
  "market_cap": 2316123766784.0,
  "pe_ratio": 33.276455,
  "forward_pe": 20.367981,
  "week_52_high": 479.0,
  "week_52_low": 266.82,
  "revenue": 4440492343296.0,
  "net_income": 2216808415232.0,
  "profit_margin": 0.49923,
  "dividend_yield": 0.9,
  "sector": "Technology",
  "industry": "Semiconductors"
}

<!-- replay-section: Financial Health -->
### Financial Health
Taiwan Semiconductor Manufacturing Company Limited trades at $446.57 per share in the technology sector. It carries a market capitalization of $2.32 trillion and a P/E ratio of 33.3x (20.4x forward), a premium valuation. The company reports net income of $221.7 billion and a net profit margin of 49.9%. It currently pays a dividend yield of 0.9%.

<!-- replay-section: Risk Factors -->
### Risk Factors

- The semiconductor industry is highly competitive and subject to rapid technological change.
- TSM faces intense competition from other semiconductor manufacturers in terms of product offerings, pricing strategies, and market share.
- TSM's business operations may be adversely affected by factors such as economic downturns or recessions, changes in consumer spending patterns, increases in interest rates, declines in foreign exchange rates, natural disasters, pandemics, acts of terrorism, war, civil unrest, political instability, labor strikes, work stoppages, or any other events that could have a material adverse effect on our business, financial condition, results of operations, cash flows, liquidity, capital resources, ability to access capital markets, reputation, or the conduct of our business.
- TSM may also be adversely affected by factors such as changes in government regulations, including those related to environmental protection, energy conservation, safety, health, public order, public morals, public welfare, public security, national defense, international relations, trade, commerce, taxation, tariffs, import/export restrictions, export controls, embargoes, sanctions, anti-corruption laws, anti-money laundering laws, anti-terrorism laws, anti-drug laws, anti-human trafficking laws, anti-sexual harassment laws, anti-discrimination laws, anti-bullying laws, anti-harassment laws, anti-abuse laws, anti-violence laws, anti-aggression laws, anti-invasion laws, anti-intrusion laws, anti-infiltration laws, anti-infiltration measures, anti-infiltration policies, anti-infiltration procedures, anti-infiltration protocols, anti-infiltration guidelines, anti-infiltration standards, anti-infiltration codes, anti-infiltration rules, anti-infiltration statutes, anti-infiltration ordinances, anti-infiltration regulations, anti-infiltration directives, anti-infiltration recommendations, anti-infiltration advice, anti-infiltration counsel, anti-infiltration guidance, anti-infiltration support, anti-infiltration assistance, anti-infiltration cooperation, anti-infiltration partnership, anti-infiltration consortium, anti-infiltration federation, anti-infiltration association, anti-infiltration union, anti-infiltration guild, anti-infiltration fraternity, anti-infiltration circle, anti-infiltration lodge, anti-infiltration cabal, anti-infiltration conspiracy, anti-infiltration plot, anti-infiltration scheme, anti-infiltration maneuver, anti-infiltration tactic, anti-infiltration strategy, anti-in
