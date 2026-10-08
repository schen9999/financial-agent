# AWS deployment (secondary)

Moved verbatim from the README on 2026-10-08.


The primary deployment is on OCI ([above](../README.md#deployed-on-oci)). AWS ECS is a secondary, single-container deployment of the API only.

The FastAPI backend is containerized and runs on **AWS ECS Fargate**, with a real
**RDS PostgreSQL** database, secrets in **AWS Secrets Manager**, and a
**GitHub Actions** deploy workflow that runs **on manual dispatch only**
(since 2026-09-28; a merge to `main` no longer deploys). Run it from `main`
(Actions → Deploy → Run workflow) after CI has passed on that commit; it builds
and deploys the dispatched commit. The whole
footprint is defined in **Terraform** (`infra/`). The Streamlit frontend stays on
Streamlit Cloud; Redis/Celery are stubbed in this environment (the cache no-ops
and the async endpoint is disabled).

```
CI green on main, then manual "Run workflow" (Deploy)
     │
     ▼
GitHub Actions ──OIDC (no long-lived AWS keys)──► assume scoped IAM role
  1. checkout the dispatched commit (CI is the separate pytest gate)
  2. docker build → push image (latest + commit SHA) → Amazon ECR
  3. register new task-def revision → update ECS service (wait for stable)
     │
     ▼
ECS Fargate task  (public subnet, public IP, security group locked to my IP)
  FastAPI container (uvicorn, single worker; bge-small model baked into image)
     │                                   │
     ▼                                   ▼
RDS PostgreSQL (t3.micro)        Secrets Manager
  research_briefs table            ANTHROPIC / NEWS / PINECONE / LANGSMITH keys,
  (private, SG-locked to           DATABASE_URL, REDIS_URL — injected as task
   the task's SG)                  env vars by the execution role
```

**Current state.** The service normally runs at 0 tasks. The image last
verified running was `c602e99` (task definition revision 8), on 2026-09-24,
by scaling to 1: `/health` returned 200 and an AAPL brief returned 200 with
all six sections, then the service was parked at 0 again. The automatic
deploys that followed each merge that day (the last at `7e17b4b`) ran at 0
tasks and were not verified the same way. Two caveats: the task
definition has no container health check (Fargate ignores the image's
Dockerfile `HEALTHCHECK`), so ECS reports health as UNKNOWN; and at 0 tasks a
deploy's "wait for stable" passes without starting a container, so a deploy
alone doesn't prove the new image runs.

**Design choices**

- **Terraform, end to end** — ECR, RDS, Secrets Manager, IAM roles, security
  groups, the ECS cluster/task-def/service, and the GitHub OIDC provider are all
  in `infra/`. Local state; `terraform.tfvars` (with my IP) is gitignored.
- **No static cloud credentials** — GitHub Actions authenticates via **OIDC**,
  assuming a repo-scoped IAM role with just enough permission to push to ECR and
  deploy the service. Nothing long-lived is stored in the repo.
- **Secrets never in the image or git** — they live in Secrets Manager and are
  injected into the task as environment variables at runtime via the execution
  role.
- **Cost-aware** — RDS `t3.micro` on the free tier; Fargate runs in a **public
  subnet with a public IP (no NAT gateway)** to avoid NAT cost; the task's
  security group is locked to a single IP, so the unauthenticated API isn't open
  to the world.
- **Image** — `python:3.13-slim` with the embedding model baked in so cold start
  doesn't hit the HuggingFace Hub; built in CI (no local Docker needed).

### Pausing to save cost

Fargate bills while a task runs, so the service is parked at 0 tasks and scaled
up only when it's needed:

```bash
infra/ecs-scale.sh 0   # pause  — stop the task (no Fargate compute cost; RDS stays free-tier)
infra/ecs-scale.sh 1   # resume — launch a fresh task (~1-2 min to start)
infra/ecs-ip.sh        # print the running task's public IP + base URL
```

Or the raw one-liner:

```bash
aws ecs update-service --cluster financial-agent-cluster --service financial-agent-api \
  --desired-count 1 --region us-east-1     # 0 to pause
```

There's no load balancer, so the task gets a **new public IP** on each resume
(`infra/ecs-ip.sh` fetches it). The service ignores `desired_count` in Terraform,
so scaling this way doesn't fight `terraform apply`.

See [`infra/README.md`](../infra/README.md) for the apply steps.
