# OCIR repository for the single app image (api, worker, streamlit, mcp, and
# the Argo eval templates all run financial-agent-app). OCIR would auto-create
# repos on first push, but an explicit resource pins the compartment and keeps
# the repo in state. vLLM uses an upstream public image — no repo needed.
#
# Push target (also in outputs): <region-key>.ocir.io/<namespace>/financial-agent/app
resource "oci_artifacts_container_repository" "app" {
  compartment_id = var.compartment_ocid
  display_name   = "${var.project}/app"
  is_public      = false
  is_immutable   = false
  freeform_tags  = local.tags
}

# Region key (e.g. us-ashburn-1 -> iad) for the OCIR hostname.
data "oci_identity_regions" "all" {}

locals {
  region_key = lower(one([
    for r in data.oci_identity_regions.all.regions : r.key if r.name == var.region
  ]))
  ocir_host = "${local.region_key}.ocir.io"
}
