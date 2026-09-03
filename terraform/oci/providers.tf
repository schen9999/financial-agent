terraform {
  required_version = ">= 1.5"

  required_providers {
    oci        = { source = "oracle/oci", version = "~> 7.0" }
    kubernetes = { source = "hashicorp/kubernetes", version = "~> 2.30" }
  }

  # Local state for now, matching infra/ (AWS). Upgrade to an OCI Object
  # Storage backend (S3-compatible API) once the bucket exists, if desired.
}

# Auth: tenancy/user/fingerprint/key vars are all optional — leave them unset
# (null) and the provider falls back to ~/.oci/config or OCI_* env vars.
# Phase 1 runs validate only, which needs no credentials at all.
provider "oci" {
  region           = var.region
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
}

# Kubernetes provider pointed at the OKE cluster this config creates, used only
# for the Block Volume StorageClass. OKE kubeconfigs authenticate via an exec
# plugin (the OCI CLI mints short-lived tokens), so `oci` must be on PATH at
# apply time. Known Terraform caveat: provider config derived from a resource
# in the same config means first apply may need
#   terraform apply -target=oci_containerengine_node_pool.app
# before a full apply. Irrelevant in Phase 1 (no apply until credentials land).
provider "kubernetes" {
  host                   = local.kubeconfig.clusters[0].cluster.server
  cluster_ca_certificate = base64decode(local.kubeconfig.clusters[0].cluster["certificate-authority-data"])

  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "oci"
    args = [
      "ce", "cluster", "generate-token",
      "--cluster-id", oci_containerengine_cluster.oke.id,
      "--region", var.region,
    ]
  }
}
