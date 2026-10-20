# Documentation index

Start here. Each question points to the document that answers it. Documents
are marked **reference** (describes the system as it is now; kept current) or
**dated log** (a record of what was measured or done on a given date; read
the dates, and use it as evidence rather than as current instructions).

## Start here

| Reader | Start with |
|---|---|
| Deciding what to adopt | [report.md](report.md): the evaluation and the recommendation |
| Deploying or operating it on OCI | [deploy-oci.md](deploy-oci.md), then [operations.md](operations.md) |
| Checking a figure | [numbers-of-record.md](numbers-of-record.md): every quotable number, its run ID and the command that produced it |
| Comparing with Harness Engineering on OCI CPU | [harness-mapping.md](harness-mapping.md) |

## Reader questions

| Question | Where to look | Type |
|---|---|---|
| What was found, and what is recommended? | [report.md](report.md): the evaluation report and recommendation (2026-10-19) | reference |
| How do I deploy it on OCI from scratch? | [deploy-oci.md](deploy-oci.md): resources, the OKE app plane and eval harness, the CPU and GPU model endpoints, verification, teardown | reference |
| What is this, and what does it do? | [README](../README.md): "What it does" and "Conclusions" | reference |
| How is it deployed on OCI? | [architecture.md](architecture.md), "Deployed topology (October 2026)"; [README](../README.md): "Deployed on OCI"; the current procedure in [operations.md](operations.md); OKE steps in [deploy-runbook.md](deploy-runbook.md#oke-provided-cluster), "OKE (provided cluster)" (the never-applied Terraform path is "OKE (OCI) — Phase 2") | reference |
| How do I configure it? | [configuration.md](configuration.md): every environment variable, its default, and where it is set | reference |
| What does the API look like? | [api.md](api.md): all routes with request/response shapes and examples | reference |
| Something broke. What do I check? | [operations.md](operations.md), "Troubleshooting" (incidents that actually happened) | reference |
| What does the OKE Terraform create? | [terraform/oci/README.md](../terraform/oci/README.md) (written and validated, never applied) | reference |
| Is the provided cluster in Terraform? | [terraform/oci-provided/README.md](../terraform/oci-provided/README.md): codified via terraform import on the operator host, never applied; the configuration is committed with every OCID a reference or a variable, and the plan has zero diff (2026-10-15) | reference |
| How do I run it locally? | [README](../README.md): "Running Locally"; [k8s/README.md](../k8s/README.md) for the kind cluster | reference |
| What is the architecture? | [architecture.md](architecture.md), including the pipeline and Kubernetes diagrams and the Celery vs Argo split (moved from the README, 2026-10-08) | reference |
| What are the results, and which numbers can I quote? | [numbers-of-record.md](numbers-of-record.md): [current](numbers-of-record.md#current), [dated run records](numbers-of-record.md#dated-run-records), [retired](numbers-of-record.md#retired); summary table in the [README](../README.md) "Key results" | reference |
| How is grounding measured, and how reliable is the judge? | [eval-methodology.md](eval-methodology.md): "What is measured", "Rigor rules", the judge-validation sections; a guided version as of September 2026 in [system-tour.md](system-tour.md), section 5 | dated log |
| Can a self-served open-weight model write the whole brief, and at what cost? | [eval-methodology.md](eval-methodology.md): "GPU SLM extended run `p9jr2`" (the same-image three-way, cost per brief, numeric check); the full experiment records in [experiments.md](experiments.md); summary in the [README](../README.md) | dated log |
| How was a real error traced, end to end? | [debugging-story.md](debugging-story.md): a currency error the judge accepted and the numeric check caught, traced to the stock data; three shorter cases | dated log |
| What has run on the A10, how fast, at what cost? | [gpu-inference.md](gpu-inference.md): vLLM on the fine-tune (BF16 vs W4A16), why llama.cpp for Qwen3.6, CPU vs A10 | reference |
| What happens when a component fails, and how are eval runs kept honest? | [reliability.md](reliability.md): app-plane failure behaviour (tested or not), eval-plane safeguards | reference |
| What is the demo plan? | [demo.md](demo.md): conclusions, the numbers, the live run | reference |
| How does this map to the post Harness Engineering using OCI CPU & OKE? | [harness-mapping.md](harness-mapping.md): the post's terms beside this system's, the measurements the post does not report, what is built and not built | reference |
| Which model should write the sections: hosted, or open-weight on the A10? | [model-recommendation.md](model-recommendation.md): recommendation, four-arm results, and the A10 cost per brief (2026-09-28) | dated log |
| Why does the fine-tuned model ship disabled? | [eval-methodology.md](eval-methodology.md): the 40-ticker A/B (2026-09-05/06) and the four-arm comparison (2026-09-23) | dated log |
| How do I run the tests? | [README](../README.md): "Testing"; [verification.md](verification.md) for the manifest-equivalence proof | reference |
| What are the known limitations? | [eval-methodology.md](eval-methodology.md): [known limitations](eval-methodology.md#known-limitations-from-the-cold-read-review-2026-10-09) and the numbered limitations before it; the README's "Next steps"; the September view in [system-tour.md](system-tour.md#known-limitations-and-next-steps) | reference |
| What does it cost? | Infrastructure list prices (OCI A10, AWS): [cost.md](cost.md); per-brief API cost: [numbers-of-record.md](numbers-of-record.md#current) | reference |
| How do I tear it down? | [operations.md](operations.md), "Teardown": kind, a k3s node, the A10 VMs (tenancy owner, OCI console), ECS, OKE | reference |
| How is the AWS deployment built? | [aws.md](aws.md) (moved from the README, 2026-10-08); [infra/README.md](../infra/README.md) | reference |
| How were the vLLM nodes brought up, and what broke? | [deploy-runbook.md](deploy-runbook.md): the dated notes in "Single-VM path (k3s)", including "Rebuild on fresh nodes, 2026-09-23" | dated log |
| What did the codebase look like before the Kubernetes work? | [PHASE0_AUDIT.md](PHASE0_AUDIT.md) (2026-08-24) | dated log |
| How were the older benchmarks run? | [benchmarks.md](../benchmarks.md) (Aug 2026, pre-retrieval-fix) | dated log |
| How do I use the MCP server? | [mcp.md](mcp.md) (moved from the README, 2026-10-08) | reference |
| What were the experiments, in full? | [experiments.md](experiments.md): the grounding eval, the self-served comparison, reranking (June), the QLoRA fine-tune, the multi-agent supervisor, the old benchmark summary (moved verbatim from the README, 2026-10-08) | dated log |

## All documents

### Core documents

| Document | What it is | Type |
|---|---|---|
| [report.md](report.md) | The evaluation report and recommendation: results, method, limitations, next steps | reference |
| [README.md](../README.md) | Overview, conclusions, OCI deployment, key results, decisions, how to run and test | reference |
| [deploy-oci.md](deploy-oci.md) | How to deploy on OCI as it runs today: resources, steps, verification, teardown | reference |
| [harness-mapping.md](harness-mapping.md) | This system mapped against the post Harness Engineering using OCI CPU & OKE | reference |

### Deploy and operate

| Document | What it is | Type |
|---|---|---|
| [operations.md](operations.md) | Current procedure for an OCI A10 node, teardown for every target, troubleshooting | reference |
| [architecture.md](architecture.md) | Topology diagram, the deployed topology (October 2026) and deploy targets | reference |
| [configuration.md](configuration.md) | Every environment variable: default, purpose, where it is set | reference |
| [api.md](api.md) | All API routes with request/response shapes and examples | reference |
| [reliability.md](reliability.md) | App-plane request flow and failure behaviour; eval-plane traffic proof, attempts, gates, stop rules | reference |
| [cost.md](cost.md) | Infrastructure list prices from the official OCI and AWS price APIs, with retrieval dates | reference |
| [verification.md](verification.md) | Proof that the kustomize overlays did not change the kind render | reference |
| [terraform/oci-provided/README.md](../terraform/oci-provided/README.md) | The provided OKE cluster, codified via terraform import (zero-diff plan, never applied); configuration committed without OCIDs | reference |
| [terraform/oci/README.md](../terraform/oci/README.md) | OCI Terraform: what it creates and how to apply it | reference |
| [k8s/README.md](../k8s/README.md) | Kubernetes manifest layout and the kind workflow | reference |
| [mcp.md](mcp.md) | The MCP server: tools, running it, Claude Desktop | reference |
| [aws.md](aws.md) | The AWS ECS deployment (secondary) | reference |
| [infra/README.md](../infra/README.md) | AWS Terraform: apply, secrets, teardown | reference |

### Evidence and results

| Document | What it is | Type |
|---|---|---|
| [numbers-of-record.md](numbers-of-record.md) | Every quotable number, its source harness, and the retired ones | reference |
| [eval-methodology.md](eval-methodology.md) | How the eval works, and every dated experiment and validation | dated log |
| [gpu-inference.md](gpu-inference.md) | A10 serving: what ran, serving speed, CPU vs GPU for Qwen3.6, what has not run | reference |
| [experiments.md](experiments.md) | The experiment records moved from the README (2026-10-08) | dated log |
| [debugging-story.md](debugging-story.md) | One error traced end to end (Toyota's currency), the limits of each eval layer, three shorter cases | dated log |
| [harness-benchmark-plan.md](harness-benchmark-plan.md) | Pre-registered plan and results (2026-10-20) of the harness benchmark on OCI CPU | reference |
| [model-recommendation.md](model-recommendation.md) | Hosted Haiku vs open-weight models for the section-writing role: recommendation, results and A10 cost, from the 2026-09-23 four-arm comparison | dated log |

### The November demo

| Document | What it is | Type |
|---|---|---|
| [demo.md](demo.md) | The November demo: conclusions, the numbers, the live run | reference |

### Dated logs

| Document | What it is | Type |
|---|---|---|
| [deploy-runbook.md](deploy-runbook.md) | How each deploy step was first executed and what broke (dated), plus the OKE steps; the current procedure is operations.md | dated log |
| [system-tour.md](system-tour.md) | Guided tour of the system, results, and limitations, as of September 2026 | dated log |
| [PHASE0_AUDIT.md](PHASE0_AUDIT.md) | Repository audit before the Kubernetes work (2026-08-24) | dated log |
| [benchmarks.md](../benchmarks.md) | Earlier benchmark runs and their caveats | dated log |

`CLAUDE.md` at the repository root is the working-constraints file for the AI coding assistant used to build the project. It is not part of the documentation.
