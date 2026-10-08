# The PROVIDED OKE cluster, codified by import: plan only, NEVER apply
# (CLAUDE.md, the 2026-10-07 exception). Run every command through
# scripts/tf_provided.sh, which refuses apply, destroy, CLI import, state
# writes and saved plans. Import blocks and generated configuration hold
# OCIDs and stay local (gitignored): scripts/tf_provided_imports.py writes
# generated-imports.tf, `plan -generate-config-out=generated-config.tf`
# writes the configuration. State is local and gitignored.
terraform {
  required_version = ">= 1.5.0" # import blocks and -generate-config-out

  required_providers {
    oci = { source = "oracle/oci", version = "~> 7.0" }
  }
}

# The operator host authenticates as itself (instance principal), the same
# way its oci CLI does; no key file exists for this tree.
provider "oci" {
  auth   = "InstancePrincipal"
  region = var.region
}
