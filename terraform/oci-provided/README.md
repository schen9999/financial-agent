# terraform/oci-provided — the provided OKE cluster, codified by import

**Plan and import only. Never apply.** This cluster was provisioned for the
project, not by `terraform/oci`; the owner's 2026-10-07 exception
(CLAUDE.md) allows `terraform import` and `plan` here and nothing that
writes to the cloud. Every command goes through `scripts/tf_provided.sh`,
which refuses apply, destroy, state writes other than import, saved plans
and `-auto-approve`.

**Result (2026-10-07): zero diff.** 94 resources imported into the local
state; `plan -detailed-exitcode` exits 0 with "No changes. Your
infrastructure matches the configuration."

| Codified | Count |
|---|---|
| OKE cluster (`oci_containerengine_cluster`) | 1 |
| Node pools (`oci_containerengine_node_pool`: oke-system, oke-cpu) | 2 |
| VCN | 1 |
| Subnets (bastion, cp, operator, int_lb, pub_lb, workers, pods) | 7 |
| Network security groups | 7 |
| NSG security rules | 65 |
| Security lists | 3 |
| Route tables | 4 |
| DHCP options, internet gateway, NAT gateway, service gateway | 1 each |

Not codified: the bastion and operator compute instances, IAM policies and
dynamic groups, and anything outside the VCN's compartment.

**What is committed and what is not.** Committed: `providers.tf`,
`variables.tf`, and the scripts that rebuild the rest. Not committed (they
hold OCIDs; gitignored): `generated-imports.tf`, `generated-config.tf`
(1,850 lines) and the state. They live on the operator in
`~/financial-agent/terraform/oci-provided/`. Making the configuration
committable means replacing the OCIDs with variables and references — not
done (timebox).

**Reproduce** (operator, repo root; read-only in the cloud, instance
principal auth, Terraform 1.9.8 in `~/bin`):

```bash
python3 scripts/tf_provided_imports.py                       # 94 import blocks
bash scripts/tf_provided.sh init -input=false
bash scripts/tf_provided.sh plan -input=false -generate-config-out=generated-config.tf
python3 scripts/tf_provided_fixup.py                         # node pools: drop legacy placement fields
# import each block into local state (the loop in docs/deploy-runbook.md, "Terraform: the provided cluster")
bash scripts/tf_provided.sh plan -input=false -detailed-exitcode    # 0 = zero diff
```

Only fix-up needed: the generated node pools set the legacy
`quantity_per_subnet` and `subnet_ids` beside `node_config_details`, which
the provider rejects as conflicting.
