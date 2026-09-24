# Infrastructure cost

Unit prices for what this project provisions, taken from the providers'
official price-list APIs, with the date each was retrieved. They are list
prices only: no discounts, credits, free-tier allowances, or taxes are
applied, and the tenancy's or account's own billing console is the
authority on what is actually charged. Per-brief **API** cost (Anthropic
tokens) is separate: $0.0366/brief, the cost of record in
[numbers-of-record.md](numbers-of-record.md).

## OCI: the A10 nodes

Source: Oracle's public price-list API used by the OCI cost estimator,
`https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/?currencyCode=USD`,
retrieved 2026-09-24T07:14Z (the API reported `lastUpdated`
2026-09-23T13:10:59Z). Oracle's HTML price-list pages
(`oracle.com/cloud/price-list/`, `oracle.com/cloud/compute/pricing/`) could
not be retrieved programmatically (HTTP 403), so the API is the source here.

| Part | Product | Metric | Pay-as-you-go (USD) |
|---|---|---|---|
| B95909 | Compute - GPU - A10 | GPU per hour | 2.00 |
| B91961 | Storage - Block Volume - Storage | GB of storage capacity per month | 0.0255 |
| B91962 | Storage - Block Volume - Performance Units | performance units per GB per month | 0.0017 |
| B91445 | Storage - Block Volume - Free 200GB | GB of storage capacity per month | 0 |

What this means for the two nodes, with no assumptions added:

- Each node is a **VM.GPU.A10.1**, which has one A10 GPU (`nvidia-smi` on
  both nodes lists one NVIDIA A10). The list price is **USD 2.00 per GPU
  per hour** (part B95909, from the source above). The source does not
  state whether that rate also covers the shape's 15 OCPUs and memory; the
  tenancy's cost analysis shows how the instances are actually billed.
- Each node has a **1 TiB boot volume** (`lsblk` on both nodes), billed at
  the Block Volume rates above. The boot-volume total depends on the
  volume's performance setting (performance units per GB), which is not
  visible from inside the VM, so no total is given here.
- Whether a stopped instance keeps accruing charges, and for which
  components, is set by OCI's billing rules for the shape. The nodes are
  stopped or terminated by the tenancy owner in the OCI console
  ([operations.md](operations.md), "Teardown").

The OKE Terraform in [`terraform/oci/`](../terraform/oci/) has never been
applied, so it costs nothing today.

## AWS: the ECS deployment

Source: the AWS Price List API (`aws pricing get-products`, us-east-1
region), retrieved 2026-09-24T07:15Z. Resource sizes are read from the live
account (read-only) on the same date.

| Resource (as provisioned) | SKU | Price (USD, on demand) |
|---|---|---|
| RDS `db.t3.micro`, PostgreSQL, Single-AZ | TGN7QDJF2AGFU9XA | 0.018 per instance-hour |
| RDS gp2 storage, PostgreSQL, 20 GB provisioned | G2TQUMAQNSQ7H65X | 0.115 per GB-month |
| Secrets Manager, 6 secrets (`financial-agent/*`) | BJ3PQ9BYGU6P632F | 0.40 per secret per month (plus 0.05 per 10,000 API calls) |
| Fargate vCPU, Linux/x86 | 8CESGAFWKAJ98PME | 0.04048 per vCPU-hour |
| Fargate memory, Linux/x86 | PBZNQUSEXZUC34C9 | 0.004445 per GB-hour |

- **ECS runs at 0 tasks normally**, so Fargate charges nothing while it is
  parked. When scaled to 1, the task definition (1 vCPU, 3 GB) costs
  0.04048 + 3 × 0.004445 = **USD 0.0538 per running hour** at list price.
  Scale with `infra/ecs-scale.sh 0|1`.
- **RDS runs continuously** (`available`), so it accrues its instance-hour
  and storage rates whether or not ECS is scaled up. The README describes
  it as free tier; free-tier eligibility depends on the AWS account, so
  check the account's billing console.
- ECR image storage and CloudWatch Logs also accrue small charges; they
  are not priced here.
