# Documentation index

Start here. Each question points to the document that answers it. Documents
are marked **reference** (describes the system as it is now; kept current) or
**dated log** (a record of what was measured or done on a given date; read
the dates, and use it as evidence rather than as current instructions).

## Reader questions

| Question | Where to look | Type |
|---|---|---|
| What is this, and what does it do? | [README](../README.md): "Summary" and "What It Does" | reference |
| How is it deployed on OCI? | [README](../README.md): "Deployed on OCI"; the current procedure in [operations.md](operations.md); OKE steps in [deploy-runbook.md](deploy-runbook.md), "OKE (OCI)" | reference |
| How do I configure it? | [configuration.md](configuration.md): every environment variable, its default, and where it is set | reference |
| What does the API look like? | [api.md](api.md): all routes with request/response shapes and examples | reference |
| Something broke. What do I check? | [operations.md](operations.md), "Troubleshooting" (incidents that actually happened) | reference |
| What does the OKE Terraform create? | [terraform/oci/README.md](../terraform/oci/README.md) (written and validated, never applied) | reference |
| How do I run it locally? | [README](../README.md): "Running Locally"; [k8s/README.md](../k8s/README.md) for the kind cluster | reference |
| What is the architecture? | [architecture.md](architecture.md); diagrams in the [README](../README.md) "Architecture" section | reference |
| What are the results, and which numbers can I quote? | [numbers-of-record.md](numbers-of-record.md): [current](numbers-of-record.md#current), [dated run records](numbers-of-record.md#dated-run-records), [retired](numbers-of-record.md#retired); summary table in the [README](../README.md) "Key results" | reference |
| How is grounding measured, and how reliable is the judge? | [eval-methodology.md](eval-methodology.md): "What is measured", "Rigor rules", the judge-validation sections; a guided version in [system-tour.md](system-tour.md), section 5 | dated log |
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
| [architecture.md](architecture.md) | Topology diagram and deploy targets | reference |
| [operations.md](operations.md) | Current procedure for an OCI A10 node, teardown for every target, troubleshooting | reference |
| [configuration.md](configuration.md) | Every environment variable: default, purpose, where it is set | reference |
| [api.md](api.md) | All API routes with request/response shapes and examples | reference |
| [cost.md](cost.md) | Infrastructure list prices from the official OCI and AWS price APIs, with retrieval dates | reference |
| [deploy-runbook.md](deploy-runbook.md) | How each deploy step was first executed and what broke (dated), plus the OKE steps; the current procedure is operations.md | dated log |
| [numbers-of-record.md](numbers-of-record.md) | Every quotable number, its source harness, and the retired ones | reference |
| [system-tour.md](system-tour.md) | Guided tour of the system, results, and limitations | reference |
| [verification.md](verification.md) | Proof that the kustomize overlays did not change the kind render | reference |
| [eval-methodology.md](eval-methodology.md) | How the eval works, and every dated experiment and validation | dated log |
| [PHASE0_AUDIT.md](PHASE0_AUDIT.md) | Repository audit before the Kubernetes work (2026-08-24) | dated log |
| [benchmarks.md](../benchmarks.md) | Earlier benchmark runs and their caveats | dated log |
| [k8s/README.md](../k8s/README.md) | Kubernetes manifest layout and the kind workflow | reference |
| [infra/README.md](../infra/README.md) | AWS Terraform: apply, secrets, teardown | reference |
| [terraform/oci/README.md](../terraform/oci/README.md) | OCI Terraform: what it creates and how to apply it | reference |
| [CLAUDE.md](../CLAUDE.md) | Working constraints and documentation rules used while building the project | reference |
