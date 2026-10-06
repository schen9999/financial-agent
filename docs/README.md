# Documentation index

Start here. Each question points to the document that answers it. Documents
are marked **reference** (describes the system as it is now; kept current) or
**dated log** (a record of what was measured or done on a given date; read
the dates, and use it as evidence rather than as current instructions).

## Reader questions

| Question | Where to look | Type |
|---|---|---|
| What is this, and what does it do? | [README](../README.md): "Summary" and "What It Does" | reference |
| How is it deployed on OCI? | [architecture.md](architecture.md), "Deployed topology (October 2026)"; [README](../README.md): "Deployed on OCI"; the current procedure in [operations.md](operations.md); OKE steps in [deploy-runbook.md](deploy-runbook.md), "OKE (OCI)" | reference |
| How do I configure it? | [configuration.md](configuration.md): every environment variable, its default, and where it is set | reference |
| What does the API look like? | [api.md](api.md): all routes with request/response shapes and examples | reference |
| Something broke. What do I check? | [operations.md](operations.md), "Troubleshooting" (incidents that actually happened) | reference |
| What does the OKE Terraform create? | [terraform/oci/README.md](../terraform/oci/README.md) (written and validated, never applied) | reference |
| How do I run it locally? | [README](../README.md): "Running Locally"; [k8s/README.md](../k8s/README.md) for the kind cluster | reference |
| What is the architecture? | [architecture.md](architecture.md); diagrams in the [README](../README.md) "Architecture" section | reference |
| What are the results, and which numbers can I quote? | [numbers-of-record.md](numbers-of-record.md): [current](numbers-of-record.md#current), [dated run records](numbers-of-record.md#dated-run-records), [retired](numbers-of-record.md#retired); summary table in the [README](../README.md) "Key results" | reference |
| How is grounding measured, and how reliable is the judge? | [eval-methodology.md](eval-methodology.md): "What is measured", "Rigor rules", the judge-validation sections; a guided version in [system-tour.md](system-tour.md), section 5 | dated log |
| Can a self-served open-weight model write the whole brief, and at what cost? | [eval-methodology.md](eval-methodology.md): "GPU SLM extended run `p9jr2`" (the same-image three-way, cost per brief, numeric check); summary in the [README](../README.md) | dated log |
| How was a real error traced, end to end? | [debugging-story.md](debugging-story.md): a currency error the judge accepted and the numeric check caught, traced to the stock data; three shorter cases | dated log |
| What has run on the A10, how fast, at what cost? | [gpu-inference.md](gpu-inference.md): vLLM on the fine-tune (BF16 vs W4A16), why llama.cpp for Qwen3.6, CPU vs A10 | reference |
| What is the demo plan? | [demo.md](demo.md): conclusions, running order, the live run, prepared answers | reference |
| Which model should write the sections: hosted, or open-weight on the A10? | [model-recommendation.md](model-recommendation.md): recommendation, four-arm results, and the A10 cost per brief (2026-09-28) | dated log |
| Why does the fine-tuned model ship disabled? | [eval-methodology.md](eval-methodology.md): the 40-ticker A/B (2026-09-05/06) and the four-arm comparison (2026-09-23) | dated log |
| How do I run the tests? | [README](../README.md): "Testing"; [verification.md](verification.md) for the manifest-equivalence proof | reference |
| What are the known limitations? | [system-tour.md](system-tour.md): [known limitations and next steps](system-tour.md#known-limitations-and-next-steps) | reference |
| What does it cost? | Infrastructure list prices (OCI A10, AWS): [cost.md](cost.md); per-brief API cost: [numbers-of-record.md](numbers-of-record.md#current) | reference |
| How do I tear it down? | [operations.md](operations.md), "Teardown": kind, a k3s node, the A10 VMs (tenancy owner, OCI console), ECS, OKE | reference |
| How is the AWS deployment built? | [README](../README.md): "AWS Deployment (secondary)"; [infra/README.md](../infra/README.md) | reference |
| How were the vLLM nodes brought up, and what broke? | [deploy-runbook.md](deploy-runbook.md): the dated notes in "Single-VM path (k3s)", including "Rebuild on fresh nodes, 2026-09-23" | dated log |
| What did the codebase look like before the Kubernetes work? | [PHASE0_AUDIT.md](PHASE0_AUDIT.md) (2026-08-24) | dated log |
| How were the older benchmarks run? | [benchmarks.md](../benchmarks.md) (Aug 2026, pre-retrieval-fix) | dated log |
| How do I use the MCP server? | [README](../README.md): "MCP Server" | reference |

## All documents

| Document | What it is | Type |
|---|---|---|
| [README.md](../README.md) | Overview, OCI deployment, key results, how to run and test | reference |
| [architecture.md](architecture.md) | Topology diagram, the deployed topology (October 2026) and deploy targets | reference |
| [debugging-story.md](debugging-story.md) | One error traced end to end (Toyota's currency), the limits of each eval layer, three shorter cases | dated log |
| [gpu-inference.md](gpu-inference.md) | A10 serving: what ran, serving speed, CPU vs GPU for Qwen3.6, what has not run | reference |
| [demo.md](demo.md) | The November demo: conclusions, running order, live run, prepared answers | reference |
| [operations.md](operations.md) | Current procedure for an OCI A10 node, teardown for every target, troubleshooting | reference |
| [configuration.md](configuration.md) | Every environment variable: default, purpose, where it is set | reference |
| [api.md](api.md) | All API routes with request/response shapes and examples | reference |
| [cost.md](cost.md) | Infrastructure list prices from the official OCI and AWS price APIs, with retrieval dates | reference |
| [deploy-runbook.md](deploy-runbook.md) | How each deploy step was first executed and what broke (dated), plus the OKE steps; the current procedure is operations.md | dated log |
| [numbers-of-record.md](numbers-of-record.md) | Every quotable number, its source harness, and the retired ones | reference |
| [system-tour.md](system-tour.md) | Guided tour of the system, results, and limitations | reference |
| [verification.md](verification.md) | Proof that the kustomize overlays did not change the kind render | reference |
| [model-recommendation.md](model-recommendation.md) | Hosted Haiku vs open-weight models for the section-writing role: recommendation, results and A10 cost, from the 2026-09-23 four-arm comparison | dated log |
| [eval-methodology.md](eval-methodology.md) | How the eval works, and every dated experiment and validation | dated log |
| [PHASE0_AUDIT.md](PHASE0_AUDIT.md) | Repository audit before the Kubernetes work (2026-08-24) | dated log |
| [benchmarks.md](../benchmarks.md) | Earlier benchmark runs and their caveats | dated log |
| [k8s/README.md](../k8s/README.md) | Kubernetes manifest layout and the kind workflow | reference |
| [infra/README.md](../infra/README.md) | AWS Terraform: apply, secrets, teardown | reference |
| [terraform/oci/README.md](../terraform/oci/README.md) | OCI Terraform: what it creates and how to apply it | reference |
| [CLAUDE.md](../CLAUDE.md) | Working constraints and documentation rules used while building the project | reference |
