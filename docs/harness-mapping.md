# How this system maps to harness engineering on OCI CPU

Sanjay Basu's
[Harness Engineering using OCI CPU & OKE](https://blogs.oracle.com/cloud-infrastructure/harness-engineering-using-oci-cpu-oke)
(OCI blog, 2026-09-28) defines a harness as one agent loop with tools, and
harness orchestration as composing harnesses into larger programs. It
argues that a harness spends its time waiting on inference served
somewhere else. Its limits are CPU, memory bandwidth and
latency, not accelerators. So the harness belongs on CPU nodes in OKE,
inference is sized separately, and GPUs should not sit idle behind the
harness. The post sketches a layout: an E6 control plane; reasoners fanned
out on A2 Arm and scaled by KEDA on queue depth; a "meter" that checks
finished traces as a separate batch job; OCI Queue or Streaming triggers
behind an approval gate; egress limited to model endpoints; and API keys
in OCI Vault. It reports no benchmark of a harness on any shape.

| The post's term | Ours | Where |
|---|---|---|
| Harness: an agent loop with tools | The ReAct `/ask` agent, a LangGraph loop over four tools (stock data, news, SEC filings, filing retrieval). The brief pipeline, which is what the eval measures, has no loop: it fetches the data, writes four sections in parallel, then the synthesis | [agent/react_agent.py](../agent/react_agent.py), `/ask` in [api.py](../api.py); [agent/core.py](../agent/core.py) `run_research_checked` |
| Hand-wired DAG: fixed and auditable | The Argo eval workflow: one pod per ticker, two at a time, then the aggregate and the gate. The brief pipeline is hand-wired in the same sense | [argo/base/eval-workflow.yaml](../argo/base/eval-workflow.yaml) |
| Goal-plus-judge loop | The multi-agent supervisor graph: draft, have the shared LLM judge check the Executive Summary and Outlook, revise while above 5% unsupported, at most two revisions. It shipped default-off because evals showed no grounding gain at higher cost and latency. The eval's 5% gate uses the same judge, but it scores a finished run and does not loop | [agent/graph.py](../agent/graph.py), [agent/grounding.py](../agent/grounding.py); `MULTI_AGENT_ENABLED`, `CRITIC_MAX_UNSUPPORTED_PCT`, `MAX_REVISIONS` in [k8s/base/10-configmap.yaml](../k8s/base/10-configmap.yaml); `max-unsupported-pct` in the eval workflow |
| Meter: self-checks on finished traces, as a separate batch job | The Argo eval harness, a batch run apart from the app that judges finished briefs against their sources and gates the run. The traffic proof, which after the run matches every request in the model server's log to a harness call. The numeric check rerun over a finished run's briefs. The numeric check also runs inline on every brief, in warn mode | the eval workflow; [scripts/traffic_proof_tasks.py](../scripts/traffic_proof_tasks.py); [agent/numeric_check.py](../agent/numeric_check.py), [scripts/numeric_backtest.py](../scripts/numeric_backtest.py) |
| Restricted egress | Only the other direction, inbound to the model: the A10 endpoint requires a key, and its port admits only the OKE cluster's egress IP. The harness's own egress is not restricted (next steps, below) | [k8s/llamacpp/overlays/k3s-gpu](../k8s/llamacpp/overlays/k3s-gpu/kustomization.yaml); [deploy-runbook.md, "Demo live run"](deploy-runbook.md#demo-live-run-november-2026-gpu-smoke-from-the-oke-harness) |

**What our measurements add.** The post reports no benchmark, so these
are ours. All are model-side measurements of one system, and each has its
own caveats:

- **A GPU behind this harness sits partly idle.** On the A10 run of record
  `nstp9` (image `f3043751`, two briefs in flight, the run's setting) the
  A10 averaged about 36% utilization (35.7%; median sample 0%). Each eval
  pod also spends time outside the model: fetching data, retrieving
  filings, waiting on the judge. That is the likely reason, not a measured
  breakdown. At four briefs in flight (`xgtxx`) it averaged 45%. Nothing
  faster has been run.
- **In-cluster CPU inference is cheapest per brief, and slow.** On the
  previous image `1f51dad` (`8vpq6`, traffic proof EXACT): $0.0107 a brief,
  model cost only, at 355 s per ticker against hosted's 26 s (13.7×). The
  endpoint was saturating its 8 vCPU. It suits batch work, not
  interactive work. The CPU's citable numbers are on that image only.
- **On the E5 node, more cores stop helping at 8 vCPU** (llama-bench on the
  OKE E5 node, 2026-10-08, a dated measurement with no judge). Prompt
  processing speeds up 1.8× from 4 to 8 vCPU, then not at all. Generation
  stays at about 13 tok/s at every level. Memory bandwidth is the usual
  limit on generation, but that is an inference: this run does not
  measure it. More replicas on separate nodes might add throughput, which
  is also an inference and not measured.
- **The same model file on three OCI shapes** (llama-bench, 2026-10-16,
  a dated measurement with no judge;
  [gpu-inference.md](gpu-inference.md#same-model-file-on-an-intel-cpu-an-amd-cpu-and-an-nvidia-gpu-2026-10-16-llama-bench-no-judge)).
  On node 2's Intel Xeon (VM.GPU.A10.1), generation rises with threads,
  10.8 to 22.1 tok/s from 4 to 28, where the AMD E5 stayed about 13;
  Xeon prompt processing flattens past 15 threads, plausibly the VM's 15
  physical cores, which was not measured. The A10 is about 5× the best
  CPU on generation and about 19× on prompt processing. This compares
  OCI shapes, not chips: core layouts, memory, an OKE node against a k3s
  VM all differ, and memory bandwidth was not measured.
- **The instruction set decides whether an engine runs at all.** vLLM's
  prebuilt CPU image needs AVX-512. It crashed with SIGILL on the AVX2-only
  dev laptop ([benchmarks.md](../benchmarks.md)), and its CPU backend ran on
  node 2's AVX-512 Xeon (2026-09-28, dated). This bears on the post's note
  about X12 and AVX-512. llama.cpp is the engine that ran on the OKE E5
  nodes.

One difference: in the post the harness calls inference off-box, but ours
also serves a model in-cluster on CPU. Our measurements say in-cluster CPU
inference suits batch work. That is consistent with sizing inference
separately from the harness, but it does not prove it.

**Built since (2026-10-16):**

- **KEDA scaling of the Celery worker on Redis queue depth.** KEDA 2.21.0
  on the provided OKE cluster scales the worker from 1 to 4 replicas,
  one replica per 2 waiting tasks. What was verified, and only this: a
  backlog of 8 tasks of Celery's builtin `celery.accumulate` (no model
  call, no Anthropic credit). KEDA's metric read 8, the HPA set 4
  replicas, a new pod ran all 8 with no errors, and the worker was back
  at 1 replica 375 s after the backlog cleared. API discovery was
  healthy before, during and after. The same test passed on kind (1 to
  2 to 1), and so did the uninstall. Not measured: request-time load,
  i.e. real briefs. The metric counts only tasks no worker has taken
  yet, while each worker holds up to 4. On scale-down, a running brief is
  finished before the pod exits if it finishes within the worker's 120 s
  grace period, which was tested on kind with a probe task. A longer
  brief, which means the CPU SLM route or a hung call, is lost. The grace
  period has been applied on OKE since 2026-10-16 (runbook "KEDA",
  step 5).
  [Runbook, "KEDA"](deploy-runbook.md#keda-worker-scaling-on-queue-depth).

**Not built, as next steps:**

- **API keys from OCI Vault instead of Kubernetes Secrets.** Today the
  operator creates the Secrets by hand from a temp file that is shredded
  afterwards. Vault would remove that step and add rotation and audit.
- **Separate node pools: E6 for the control plane, A2 for the reasoners.**
  We used the four E5 nodes provided with the cluster, which is not ours
  to reshape. Arm nodes would also need multi-arch images, and the app
  image is built for `linux/amd64` only.
- **Pod egress restricted to model endpoints.** Today no overlay defines a
  NetworkPolicy, so app and eval pods can reach anything. The Terraform
  path's worker security list allows all egress, for image pulls and OCI
  services. The provided cluster's VCN rules belong to the tenancy and are
  not in the repo. The allowlist would also have to admit the data
  sources (Yahoo, SEC, news), and the cluster's CNI would have to enforce
  NetworkPolicy, which has not been checked.
- **Blast-radius metering, an approval gate, Queue or Streaming
  triggers.** These suit harnesses that generate their graphs just in time.
  Ours deliberately stays at the hand-wired, auditable end, where the graph
  is fixed in reviewed code.

Related: [demo.md](demo.md) for the conclusions and the numbers, [numbers-of-record.md](numbers-of-record.md) for what may be quoted.
