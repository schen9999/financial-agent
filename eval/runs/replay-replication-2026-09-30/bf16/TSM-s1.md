# TSM — replay s1 — bf16

## Metadata

ticker: TSM
arm: bf16
sample: 1
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/TSM_local-model.md
context_sha256: faff0ddd4ff49a73316e9ef8d738b08e542749945089049e0387f1d3fdf58af4
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:48:58Z
financial_health_prompt_sha256: 7b54e0323848c6767fe729a6ee5994199d218b7f835f19629c4eedf5d42b016c
financial_health_seed: 1010330
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 101
risk_factors_prompt_sha256: b459fa6820823ec38ef57e9062c365a4a883f76fa42580deb91ac0f0236242c5
risk_factors_seed: 1010331
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
- TSM's business operations may be adversely affected by factors such as economic conditions, political instability, natural disasters, or pandemics that could disrupt supply chains, manufacturing processes, or customer demand.
- TSM's business operations may also be adversely affected by factors such as labor shortages, worker strikes, or industrial disputes that could disrupt production schedules, workforce availability, or employee morale.
- TSM's business operations may also be adversely affected by factors such as cybersecurity threats, data breaches, or cyber attacks that could compromise sensitive information, intellectual property, trade secrets, or proprietary technologies used in its business operations.
- TSM's business operations may also be adversely affected by factors such as environmental regulations, compliance requirements, or legal proceedings that could impose additional costs, liabilities, or restrictions on its business operations.
- TSM's business operations may also be adversely affected by factors such as geopolitical tensions, international relations, or diplomatic conflicts that could impact global markets, currency values, exchange rates, interest rates, inflation rates, or any other macroeconomic indicators that could affect its business operations.
- TSM's business operations may also be adversely affected by factors such as regulatory changes, policy adjustments, or legislative reforms that could alter existing laws, regulations, policies, procedures, guidelines, standards, codes, protocols, or any other governmental or regulatory requirements applicable to its business operations.
- TSM's business operations may also be adversely affected by factors such as natural disasters, catastrophic events, or extraordinary circumstances that could cause significant disruptions to its business operations, including but not limited to earthquakes, tsunamis, hurricanes, cyclones, typhoons, tornadoes, blizzards, snowstorms, hail storms, lightning storms, thunderstorms, droughts, floods, landslides, avalanches, mudslides, sinkholes, subsidence, erosion, pollution, contamination, radioactive fallout, chemical spills, biological agents, nuclear weapons, chemical weapons, biological weapons, radiological weapons, explosive devices, improvised explosive devices, IEDs, landmines, booby traps, ambushes, snipers, mortar rounds, artillery shells, rockets, missiles, drones, unmanned aerial vehicles, UAVs, autonomous vehicles, self-driving cars, electric vehicles, hybrid electric vehicles, plug-in hybrid electric vehicles, PHEVs, battery-electric vehicles, BEVs,
