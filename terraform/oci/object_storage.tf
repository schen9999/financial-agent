# Bucket for eval artifacts (Argo DAG outputs: eval JSON, grounding reports,
# cost-harness runs). Versioned so a re-run never silently overwrites the
# numbers of record.
data "oci_objectstorage_namespace" "ns" {
  compartment_id = var.tenancy_ocid
}

resource "oci_objectstorage_bucket" "eval_artifacts" {
  compartment_id = var.compartment_ocid
  namespace      = data.oci_objectstorage_namespace.ns.namespace
  name           = "${var.project}-eval-artifacts"
  access_type    = "NoPublicAccess"
  versioning     = "Enabled"
  auto_tiering   = "Disabled"
  freeform_tags  = local.tags
}
