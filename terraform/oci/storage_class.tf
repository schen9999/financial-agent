# Block Volume StorageClass for the Postgres PVC (and any future stateful
# service). OKE installs a default `oci-bv` class with the CSI driver; this
# dedicated class exists so the k8s oke overlay pins performance and expansion
# behavior explicitly instead of riding cluster defaults. OCI block volumes
# have a 50 GB minimum — PVC requests in the oke overlay must ask for >= 50Gi.
resource "kubernetes_storage_class_v1" "block_volume" {
  metadata {
    name = var.storage_class_name
  }

  storage_provisioner    = "blockvolume.csi.oraclecloud.com"
  reclaim_policy         = "Delete"
  volume_binding_mode    = "WaitForFirstConsumer" # bind in the pod's AD, not before
  allow_volume_expansion = true

  parameters = {
    attachment-type = "paravirtualized"
    vpusPerGB       = "10" # balanced tier; 20 = higher performance if Postgres needs it
  }

  depends_on = [
    oci_containerengine_node_pool.app, # CSI driver needs schedulable nodes
  ]
}
