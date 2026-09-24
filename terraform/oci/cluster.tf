locals {
  tags = {
    Project   = var.project
    ManagedBy = "terraform"
  }
}

# OKE basic cluster (per CLAUDE.md — no enhanced-cluster features needed, and
# basic clusters carry no per-cluster charge). Flannel overlay CNI keeps the
# subnet/seclist surface small; the eval workloads have no need for VCN-native
# pod networking.
resource "oci_containerengine_cluster" "oke" {
  compartment_id     = var.compartment_ocid
  name               = "${var.project}-oke"
  type               = "BASIC_CLUSTER"
  kubernetes_version = var.kubernetes_version
  vcn_id             = oci_core_vcn.main.id
  freeform_tags      = local.tags

  cluster_pod_network_options {
    cni_type = "FLANNEL_OVERLAY"
  }

  endpoint_config {
    is_public_ip_enabled = true
    subnet_id            = oci_core_subnet.api.id
  }

  options {
    service_lb_subnet_ids = [oci_core_subnet.lb.id]

    kubernetes_network_config {
      pods_cidr     = "10.244.0.0/16"
      services_cidr = "10.96.0.0/16"
    }
  }
}

# Kubeconfig for the kubernetes provider (StorageClass in storage_class.tf).
data "oci_containerengine_cluster_kube_config" "oke" {
  cluster_id = oci_containerengine_cluster.oke.id
}

locals {
  kubeconfig = yamldecode(data.oci_containerengine_cluster_kube_config.oke.content)
}
