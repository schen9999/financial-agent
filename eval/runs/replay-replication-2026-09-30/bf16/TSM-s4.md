# TSM — replay s4 — bf16

## Metadata

ticker: TSM
arm: bf16
sample: 4
served_name: financial-lora
source_findings: eval/runs/raw/v924f-findings/TSM_local-model.md
context_sha256: faff0ddd4ff49a73316e9ef8d738b08e542749945089049e0387f1d3fdf58af4
agent_core_sha256: f45e278f9722d5c331843a77692b154904f72edd059e6a3da48976a7945db44e
sampling: {"temperature": 0.1, "max_tokens": 512, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.1, "min_p": 0.0}
endpoint: http://localhost:30880
generated_utc: 2026-09-30T04:48:58Z
financial_health_prompt_sha256: 7b54e0323848c6767fe729a6ee5994199d218b7f835f19629c4eedf5d42b016c
financial_health_seed: 1040330
financial_health_response_model: financial-lora
financial_health_finish_reason: stop
financial_health_completion_tokens: 101
risk_factors_prompt_sha256: b459fa6820823ec38ef57e9062c365a4a883f76fa42580deb91ac0f0236242c5
risk_factors_seed: 1040331
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
Taiwan Semiconductor Manufacturing Company Limited trades at $446.57 per share in the technology sector. The company carries a market capitalization of $2.32 trillion and a P/E ratio of 33.3x (20.4x forward), a premium valuation. It reports net income of $22.2 billion and a net profit margin of 49.9%. The company currently pays a dividend yield of 0.9%.

<!-- replay-section: Risk Factors -->
### Risk Factors

- The semiconductor industry is highly competitive and subject to rapid technological change.
- TSM faces intense competition from other semiconductor manufacturers in terms of product offerings, pricing strategies, and market share.
- TSM may also face competition from foreign companies that have established manufacturing facilities in China or elsewhere in Asia.
- In addition to direct competitors, TSM may also face indirect competition from other industries that use semiconductors, such as telecommunications, automotive, and consumer electronics.
- TSM's business operations could be adversely affected if it experiences significant disruptions in its supply chain, including delays or shortages in raw materials, components, or finished products; difficulties in obtaining adequate transportation services; or any other factors that could result in material interruptions to our business operations.
- TSM may also experience adverse effects on its business operations if it encounters significant disruptions in its information technology systems, including failures in data centers, network infrastructure, or application software; security breaches or cyber attacks that compromise the confidentiality, integrity, or availability of sensitive information or critical assets; or any other factors that could result in material interruptions to our business operations.
- TSM may also experience adverse effects on its business operations if it encounters significant disruptions in its human resources management system, including failures in recruitment processes, employee performance evaluations, or personnel training programs; difficulties in attracting and retaining qualified employees; or any other factors that could result in material interruptions to our business operations.
- TSM may also experience adverse effects on its business operations if it encounters significant disruptions in its corporate governance structure, including failures in board meetings, executive sessions, or committee deliberations; difficulties in implementing effective risk management practices; or any other factors that could result in material interruptions to our business operations.
- TSM may also experience adverse effects on its business operations if it encounters significant disruptions in its compliance and regulatory affairs function, including failures in internal audits, external inspections, or legal proceedings; difficulties in ensuring adherence to applicable laws, regulations, standards, codes, guidelines, policies, procedures, protocols, best practices, lessons learned, knowledge sharing, innovation, creativity, imagination, intuition, foresight, insight, perception, judgment, evaluation, analysis, synthesis, abstraction, generalization, specialization, differentiation, homogenization, regularization, denoising, compression, expansion, contraction, dilation, magnification, reduction, enlargement, scaling, rescaling, normalization, standardization, skewing, kurtosis, variance, standard deviation, coefficient of variation, z-score, t-statistic, F-statistic, chi-square
