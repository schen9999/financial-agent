# terraform/oci-provided — the provided OKE cluster, codified via terraform import

**Plan and import only. Never apply.** This cluster was provisioned for the
project, not by `terraform/oci`; the owner's 2026-10-07 exception
(CLAUDE.md) allows `terraform import` and `plan` here and nothing that
writes to the cloud. Every command goes through `scripts/tf_provided.sh`,
which refuses apply, destroy, state writes other than import, saved plans
and `-auto-approve`.

**Result: zero diff, configuration committed (2026-10-15).** The 94
resources imported on 2026-10-07 are codified in reviewable files here,
with no OCID in any of them; `plan -detailed-exitcode` exits 0 with "No
changes. Your infrastructure matches the configuration." (operator host,
2026-10-15).

| File | What it holds |
|---|---|
| `network.tf` | VCN, 7 subnets (bastion, cp, operator, int_lb, pub_lb, workers, pods), 7 NSGs and their 65 rules, 3 security lists, 4 route tables, DHCP options, internet, NAT and service gateways |
| `cluster.tf` | the OKE cluster (`oci_containerengine_cluster`) |
| `nodepool.tf` | the node pools `oke-system` and `oke-cpu` |
| `variables.tf` | `region`, plus the values that are not codified resources: the compartment, node image, NAT public IP and Oracle services IDs and similar (6 in all) |
| `terraform.tfvars.example` | placeholders for those variables; the real `terraform.tfvars` is gitignored and lives on the operator |
| `providers.tf`, `.terraform.lock.hcl` | the OCI provider (instance-principal auth) and its pinned version |

An OCID that is a codified resource's own ID is written as a reference
(`oci_core_subnet.subnet_workers_tbhcuw.id`), and every other OCID is a
variable. `defined_tags` and `freeform_tags` are left out: they are
optional and computed, so leaving them out changes nothing in the plan,
and the Oracle tags record who created each resource. Null attributes are
dropped.

**Two security lists ignore their rules.** The OKE cloud controller owns
the rules it adds for the public Streamlit LoadBalancer
(security-list management mode, `k8s/overlays/oke-provided-public-ui`):
health-check and NodePort rules between the public LB subnet and the
workers, and the allowlisted ingress on 443. Those rules change whenever
the LoadBalancer Service changes, so they are not copied into HCL.
`sl_default_security_list_for_oke_test_vcn_tbhcuw` and `sl_pub_lb_tbhcuw`
carry `lifecycle { ignore_changes = [ingress_security_rules,
egress_security_rules] }` with a comment saying Kubernetes owns them.
Both lists held no rules at import (2026-10-07), so the HCL writes none
for them. The trade-off: a rule change on
those two lists from any other source does not show in the plan either.
Every other attribute of those lists, and every other resource, is
compared.

**Provenance, from the tags (read 2026-10-15).** The cluster carries the
freeform tags `role=cluster` and `state_id=tbhcuw`, and the node pools
`role=worker`, `pool=<name>`, `state_id=tbhcuw` and
`cluster_autoscaler=disabled`; the cluster is named `oke-test-tbhcuw`.
Those are the tags `oracle-terraform-modules/terraform-oci-oke` sets, so
the cluster was most likely built with that module. The tags match; they
do not prove it, and that module's state is not ours.

**Not codified:** the bastion and operator compute instances; the
public Streamlit LoadBalancer and the rules the cloud controller manages
(above); IAM policies and dynamic groups; anything outside the VCN's
compartment.

**Known limitations: network exposure, recorded as provisioned.** The
HCL records these rules as the cluster has them and does not change them.
The demo depends on the current configuration, so tightening them is
deferred until after the demo:

- **The Kubernetes API endpoint has a public IP.** The cluster's
  `endpoint_config` sets `is_public_ip_enabled = true`, in the `cp`
  subnet, which allows public IPs and routes to the internet gateway. The
  control-plane NSG admits TCP 6443 from 0.0.0.0/0
  (`nsg_cp_tbhcuw_rule_04`, "Allow TCP ingress to kube-apiserver from
  0.0.0.0/0"). Kubernetes authentication still applies. The operator
  host reaches the API on the private endpoint, 10.140.0.3.
- **SSH to the bastion is open to 0.0.0.0/0** (`nsg_bastion_tbhcuw_rule_03`,
  TCP 22).
- **The `pub_lb` NSG admits TCP 443 and 80 from 0.0.0.0/0**
  (`nsg_pub_lb_tbhcuw_rule_00`, `nsg_pub_lb_tbhcuw_rule_03`). The HCL
  does not show whether the Streamlit LoadBalancer uses that NSG. Its
  allowlist is enforced in the `pub_lb` security list and again in an
  nginx sidecar (deploy-runbook, "Public Streamlit UI").
- ICMP type 3 code 4 from 0.0.0.0/0 to the pods and workers is path-MTU
  discovery, and is expected.

**Reproduce** (operator, repo root; read-only in the cloud, instance
principal auth, Terraform 1.9.8 in `~/bin`). With the state already
imported, the committed files and the real `terraform.tfvars` are enough:

```bash
bash scripts/tf_provided.sh init -input=false
bash scripts/tf_provided.sh plan -input=false -detailed-exitcode    # 0 = zero diff
```

From nothing (a fresh state), regenerate and codify:

```bash
python3 scripts/tf_provided_imports.py                       # 94 import blocks (gitignored)
bash scripts/tf_provided.sh init -input=false
bash scripts/tf_provided.sh plan -input=false -generate-config-out=generated-config.tf
python3 scripts/tf_provided_fixup.py                         # node pools: drop legacy placement fields
# import each block into local state (the loop in docs/deploy-runbook.md, "Terraform: the provided cluster")
python3 scripts/tf_provided_codify.py \
  --controller-managed sl_default_security_list_for_oke_test_vcn_tbhcuw,sl_pub_lb_tbhcuw
bash scripts/tf_provided.sh fmt
bash scripts/tf_provided.sh plan -input=false -detailed-exitcode    # 0 = zero diff
```

`tf_provided_fixup.py`: the generated node pools set the legacy
`quantity_per_subnet` and `subnet_ids` beside `node_config_details`, which
the provider rejects as conflicting. `tf_provided_codify.py` writes the
committable files and the gitignored `terraform.tfvars`, and refuses to
write anything if an OCID, an email address, an availability-domain name
or a public address would reach a committable file.
