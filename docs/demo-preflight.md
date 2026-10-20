# Demo preflight checklist

Run it in full on the rehearsal day (rehearsal and freeze 2026-10-24,
spare day 2026-10-25), ending with the rehearsal and the freeze tag, and
again 30 minutes before the demo (checks 1–11 only). In
order; **stop at the first check whose output differs from the expected
line** and take its branch in
[deploy-runbook.md, "Failure branches"](deploy-runbook.md#failure-branches).

Shells: **laptop** is WSL in the repo; **operator** is `ssh oke-operator`
(ProxyJump `oke-bastion`), in `~/financial-agent`; **node 2** is `ssh oci2`.
Each of the three has `~/financial-agent/.addresses.env` (gitignored,
from `addresses.env.example`): check 9 reads node 2's address from it,
and `scripts/redact.py` uses it to write placeholders, not addresses,
into every capture. No address is typed into a command or committed.
Nothing here sends a completion to either model endpoint before the
rehearsal's own run.

## Checks

- [ ] **1. Repo at the commit to be frozen** (laptop and operator)
  ```bash
  git fetch && git checkout main && git pull --ff-only && git status -sb && git log -1 --oneline
  ```
  Expected: `## main...origin/main`, no changes, the same commit on both.

- [ ] **2. Tests** (laptop; rehearsal day only)
  ```bash
  python -m pytest tests/ -q
  ```
  Expected: `... passed, 1 skipped` (the credit-gated judge test), no
  failures.

- [ ] **3. Anthropic credit** (laptop; no API call)
  ```bash
  make anthropic-estimate RUNS="argo/eval-run-slm-gpu-smoke.yaml argo/eval-run-slm-gpu-smoke.yaml argo/eval-run-slm-gpu-smoke.yaml"
  ```
  Expected: `ESTIMATE : $2.71` and `BUDGET : $4.06` (rehearsal, demo, one
  spare smoke; each smoke $0.90, from `m7qvv` on this image). The console's
  billing page shows at least the BUDGET line. 30 minutes before: the demo
  smoke and the spare, `BUDGET : $2.71`. A low balance fails the run
  mid-run (`eval/runtime_guards.py`).

- [ ] **4. OKE nodes and pods** (operator)
  ```bash
  kubectl get nodes
  kubectl -n financial-agent get pods
  kubectl -n argo get pods
  kubectl -n financial-agent get scaledobject worker
  make keda-check
  ```
  Expected: 4 nodes `Ready`; `api`, `worker`, `streamlit`, `mcp`, `redis`,
  `postgres`, `llamacpp` all `Running` with ready containers, and exactly
  one `worker` pod (KEDA's minimum; more means queued async work, so wait
  for it to drain); `workflow-controller` and `argo-server` `Running`.
  The ScaledObject shows `MIN 1`, `MAX 4`, `READY True`. `make
  keda-check` ends with `DISCOVERY CHECK (installed): PASS`, and every
  line above it is `OK`:
  ```
    OK    api-resources complete (exit 0, no discovery error on stderr)
    OK    all 27 APIServices Available
    OK    served by keda/keda-operator-metrics-apiserver
    OK    GET /apis/external.metrics.k8s.io/v1beta1 answers
    OK    deploy/keda-operator available (1)
    OK    deploy/keda-operator-metrics-apiserver available (1)
    OK    deploy/keda-admission-webhooks available (1)
  ```
  (27 is the count on 2026-10-16. A different count with every line `OK`
  is not a failure; note it.) **If any line is `FAIL`**, in particular
  "unable to retrieve the complete list of server APIs", **do not debug
  it**: uninstall KEDA per the runbook (`make keda-uninstall
  KEDA_OVERLAY=oke-provided`, ending `DISCOVERY CHECK (uninstalled):
  PASS`) and re-run checks 1–4. Failure branch: "`make keda-check`
  fails".

- [ ] **5. Nightly CronWorkflow suspended, nothing running** (operator)
  ```bash
  kubectl -n financial-agent get cronworkflow grounding-eval-nightly -o jsonpath='{.spec.suspend}{"\n"}'
  kubectl -n financial-agent get workflows | grep -w Running
  ```
  Expected: `true`, then no output.

- [ ] **6. Image pin `f3043751`** (operator)
  ```bash
  python3 scripts/pin_oke_image.py --overlay oke-provided --check
  kubectl -n financial-agent get deploy api -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
  kubectl -n financial-agent get workflowtemplate grounding-eval -o jsonpath='{.spec.templates[*].container.image}{"\n"}'
  ```
  Expected: the check passes with tag `f3043751…`; the api image and every
  template image end in `:f3043751eb51083b8c674d23ad4ff1da91cbdeac`.

- [ ] **7. The app does not call a model endpoint** (operator)
  ```bash
  kubectl -n financial-agent get configmap app-config -o jsonpath='{.data.SLM_FULL}{"\n"}'
  ```
  Expected: `false` (the public UI uses hosted models, so it cannot put
  traffic in the proof's window).

- [ ] **8. Node 2: endpoint, key, GPU, vLLM at 0** (node 2)
  ```bash
  curl -s localhost:30880/health; echo
  curl -s -o /dev/null -w '%{http_code}\n' localhost:30880/v1/models
  nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv
  kubectl -n financial-agent get deploy vllm llamacpp
  ```
  Expected: `{"status":"ok"}`; `401`; `llama-server` near `20488 MiB`;
  vllm `0/0`, llamacpp `1/1`. If vLLM serves on 30880: `make vm-llamacpp`
  at once and tell the tenancy owner (runbook, "Demo live run").

- [ ] **9. 30880 from OKE, and the harness's own path** (laptop, then operator)
  ```bash
  scp scripts/gpu_exposure_check.sh oke-operator:/tmp/ && \
    ssh -T -n oke-operator 'bash -ic "bash /tmp/gpu_exposure_check.sh"'
  # operator:
  kubectl -n financial-agent exec deploy/api -- env SLM_FULL=true SLM_ENDPOINT=gpu python -c \
    "import json; from agent.tools.slm import server_facts; print(json.dumps(server_facts(), indent=1))"
  ```
  Expected: `HTTP 401` without the key, `HTTP 200` with it, alias
  `qwen3.6-35b-a3b-q4km` (no `-hybrid`), as in
  `eval/runs/gpu-exposure-check-2026-10-05.txt`; `server_facts` prints the
  same alias and no error.

- [ ] **10. Yahoo from the cluster** (operator; one request)
  ```bash
  kubectl -n financial-agent exec deploy/api -- python -c \
    "import yfinance as yf; print(yf.Ticker('AAPL').fast_info['lastPrice'])"
  ```
  Expected: a price. A 429 or an error: no run today shows stock figures;
  fallback for the numbers.

- [ ] **11. Screens and tunnels** (operator, then laptop)
  ```bash
  # operator
  nohup kubectl -n argo port-forward svc/argo-server 2746:2746 >/tmp/pf-argo.log 2>&1 &
  nohup kubectl -n financial-agent port-forward svc/streamlit 8501:8501 >/tmp/pf-streamlit.log 2>&1 &
  # laptop
  ssh -N -L 32746:localhost:2746 -L 32501:localhost:8501 oke-operator
  ```
  Expected: `https://localhost:32746` lists the workflows;
  `http://localhost:32501` loads. The shared terminals (operator, node 2,
  laptop) are open with scrollback cleared (`clear && printf '\e[3J'`).
  Never on a shared screen: `kubectl get secret … -o yaml|json`,
  `kubectl exec … env`, `env`/`printenv`, `/proc/<pid>/environ`,
  `cat .env`. The exposure script, `server_facts` and the run's output
  print no key.

## The rehearsal (rehearsal day only)

- [ ] **12. Launch** (operator, at a recorded time), **with the screen
  recorded**. Start the recording before the launch and stop it after
  check 14's last line. It becomes the first fallback on the day
  (the fallback list in the local presenter notes, not in the repo).
  Capture, in this order on screen:
  - the operator pane running the command below, from submit to the last line;
  - the Argo UI graph (`https://localhost:32746`, check 11): ten eval
    pods, two at a time, then the aggregate;
  - the node 2 pane with `watch -n 2 nvidia-smi`, the A10 moving with the
    calls;
  - the second operator pane with the live CPU ask (check 13), from the
    command to its `LIVE CPU ASK:` line;
  - at the end of the run: the aggregate table, the gate line,
    `stock block empty`, the call table and the attempts block;
  - the laptop pane for check 14, ending on
    `TRAFFIC PROOF (per-request): TASK-EXACT`.

  Keys and secrets stay off screen, as in check 11: no
  `kubectl get secret … -o yaml|json`, no `kubectl exec … env`, no
  `env`/`printenv`, no `/proc/<pid>/environ`, no `cat .env`, and no
  Streamlit basic-auth prompt with the password typed in view. Scrollback
  cleared in every recorded pane first. Watch the recording through once
  before storing it. The file stays out of the repo (size): store it
  where the presenter notes' fallback list points, not under the working tree.
  ```bash
  make slm-eval-run ENDPOINT=gpu EVAL_RUN_FILE=argo/eval-run-slm-gpu-smoke.yaml 2>&1 | tee ~/rehearsal-$(date -u +%F).log
  ```
  Expected, in about 10 minutes (`m7qvv` 9 min 56 s): 11/11 nodes
  Succeeded; `stock block empty : 0/10`; Trunc, Loop, Parse, Fmt, Err all
  0; the attempts block shows 0 retries; a gate line (a smoke may fail it
  on qualitative watch-items, as `m7qvv` did: recorded, not re-run). The
  last line `TRAFFIC PROOF: …` is the `/metrics` counter, **reported, not
  deciding**: it has drifted by a few tokens on both endpoints. Note the
  workflow name `WF` it prints.

- [ ] **13. The live CPU ask, while the smoke runs** (operator, a second
  pane, started a minute or two after check 12, as at step 3 of the
  running order; no Anthropic spend). First, before check 12, the two
  things it needs from outside the cluster's model:
  ```bash
  # the embedding model loads from the image with the HF hub switched off
  kubectl -n financial-agent exec deploy/api -c api -- env HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python -c \
    "from llama_index.embeddings.huggingface import HuggingFaceEmbedding as E; print(len(E(model_name='BAAI/bge-small-en-v1.5').get_text_embedding('ok')))"
  # EDGAR answers from the cluster (one request, SEC's ticker map)
  kubectl -n financial-agent exec deploy/api -c api -- python -c \
    "from agent.tools.sec_common import lookup_cik; print(lookup_cik('V'))"
  ```
  Expected: `384` (bge-small's dimension). An error about the hub or a
  missing file means the model is not in the image's cache: use `ALT=2`,
  which needs no embedding, and say so. Then `0001403161`; `None` means
  EDGAR did not answer: use the recorded pane, no live ask. Then, after
  check 12:
  ```bash
  make live-cpu-ask 2>&1 | tee ~/rehearsal-cpu-ask-$(date -u +%F).log
  ```
  Expected: `endpoint  slm-cpu  served alias qwen3.6-35b-a3b-q4km  build
  b11347-…`; the question; `tool call   get_sec_filings(…)` then
  `tool call   query_sec_filing(…)`, each followed by its `tool result`;
  an answer about the risks of Walmart's omnichannel and eCommerce
  investments (read it: one topic, no unrelated lists); `10-K check  get_sec_filings: 2026-03-13; indexed
  filing: 2026-03-13 -> same filing`; three or more model
  calls, every one `slm-cpu` with alias `qwen3.6-35b-a3b-q4km` and no
  `ERROR`; last line `LIVE CPU ASK: OK — wall <n> s, … hosted calls
  attempted 0. A demonstration, not a citable run.` Wall time: **expect
  about 70 s cold.** Dated trials of 2026-10-16 (not citable runs): the
  narrowed Walmart question 33.8 s, but warm (its retrieval answer took
  4.5 s, very likely the prompt cache from a run 20 minutes earlier); the
  first Walmart wording 72.5 s cold (retrieval answer 35.2 s); the Apple
  alternate 95.8 s; the old Visa question 93.3 s. Record whether the
  retrieval answer took about 35 s (cold) or a few seconds (warm). A
  mention of "Walmart+" in the answer is the model's own addition, not in
  the sources (demo.md). A `MISMATCH` on the 10-K line
  means a newer Walmart 10-K than the indexed one: drop the step (demo.md,
  failure table). A `refusing:` line means the exec's environment is wrong
  (nothing was sent). `NOT OK` with `hosted Anthropic call attempted`
  means the guard stopped a hosted call: record it, do not re-run, and drop
  the step from the demo until it is understood. Check 14's proof must
  still come out TASK-EXACT: the ask has no address or key for node 2.

- [ ] **14. The deciding proof: per-request match** (operator, then laptop)
  ```bash
  # operator: the window's start
  kubectl -n financial-agent get workflow $WF -o jsonpath='{.metadata.creationTimestamp}{"\n"}'
  # laptop, right after the run (T0 = the timestamp above, ID = the last part of WF)
  mkdir -p eval/runs/slm-proof-$ID
  ssh oci2 "kubectl -n financial-agent logs deploy/llamacpp -c llama-server --since-time=$T0" \
    | python3 scripts/redact.py > eval/runs/slm-proof-$ID/llamacpp-server-window.log
  scp "oke-operator:~/slm-proof/$WF*" eval/runs/slm-proof-$ID/
  python3 scripts/traffic_proof_tasks.py --endpoint slm-gpu \
    --server-log eval/runs/slm-proof-$ID/llamacpp-server-window.log \
    --log eval/runs/slm-proof-$ID/$WF.log \
    --before eval/runs/slm-proof-$ID/$WF-before.json --after eval/runs/slm-proof-$ID/$WF-after.json \
    --json-out eval/runs/slm-proof-$ID/proof-tasks.json
  ```
  Expected: `unmatched: server 0, harness 0`, `0 incomplete`, and
  `TRAFFIC PROOF (per-request): TASK-EXACT` (70 calls on a smoke).
  Anything else: the run is not citable; say so on the day and use the
  fallback.

- [ ] **15. Record the timings** for the running order: the smoke's wall
  time, the live CPU ask's wall time (check 13), and how long checks 4–11
  took.

- [ ] **16. Freeze** — only after 12, 13 and 14 pass: [Freeze](#freeze), below.

## Freeze

The tag `demo-freeze-2026-10` goes on the final commit of `main` after the
rehearsal (CLAUDE.md, constraint 6). If the rehearsal's capture is
committed, it goes in through a PR like any change; the tag goes on `main`
once that PR is merged. Laptop:

```bash
git fetch origin && git checkout main && git pull --ff-only
git status -sb                                   # ## main...origin/main, clean
git log -1 --oneline                             # the commit to freeze: the rehearsal's capture merge, or the commit it ran from
python -m pytest tests/ -q                       # passes on exactly this commit
git tag -l demo-freeze-2026-10                   # no output: the tag does not exist yet
git tag -a demo-freeze-2026-10 -m "Demo freeze after the rehearsal on <date>: image f3043751, rehearsal <wf>"
git push origin demo-freeze-2026-10
git ls-remote --tags origin demo-freeze-2026-10  # one line, the tag object's sha
git rev-parse demo-freeze-2026-10^{}             # the frozen commit, equal to git rev-parse main
```

Post-demo work branches from the tag: `git checkout -b <branch> demo-freeze-2026-10`.

## GitHub Release (after the tag exists)

Only once `git ls-remote --tags origin demo-freeze-2026-10` prints the tag
(Freeze, above). The notes are drafted in
`notes/release-demo-freeze-2026-10.md` (gitignored); fill its rehearsal
date and workflow name first. In the browser:

1. The repo on GitHub → **Releases** → **Draft a new release**.
2. **Choose a tag**: pick the existing `demo-freeze-2026-10`. Do not type a
   new name: GitHub would create a new tag on the default branch's head.
3. **Release title**: the `Title:` line of the notes file.
4. **Description**: everything below the `---` line of the notes file.
5. Leave "Set as a pre-release" off, then **Publish release**.

Expected: the release page shows tag `demo-freeze-2026-10` and the short
sha of `git rev-parse demo-freeze-2026-10^{}`; its three links open the
README, demo.md and numbers-of-record.md at the tag.
