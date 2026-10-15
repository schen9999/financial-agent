# The PROVIDED OKE cluster, codified via terraform import: plan only, NEVER
# apply (CLAUDE.md, the 2026-10-07 exception); every command through
# scripts/tf_provided.sh. Written by scripts/tf_provided_codify.py from the
# generated configuration: OCIDs are references or variables (values in the
# gitignored terraform.tfvars), tags and null attributes dropped.

resource "oci_containerengine_cluster" "cluster_oke_test_tbhcuw" {
  compartment_id     = var.compartment_ocid
  kubernetes_version = "v1.34.1"
  name               = "oke-test-tbhcuw"
  type               = "ENHANCED_CLUSTER"
  vcn_id             = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
  cluster_pod_network_options {
    cni_type = "OCI_VCN_IP_NATIVE"
  }
  endpoint_config {
    is_public_ip_enabled = true
    nsg_ids              = [oci_core_network_security_group.nsg_cp_tbhcuw.id]
    subnet_id            = oci_core_subnet.subnet_cp_tbhcuw.id
  }
  image_policy_config {
    is_policy_enabled = false
  }
  options {
    ip_families           = ["IPv4"]
    service_lb_subnet_ids = [oci_core_subnet.subnet_pub_lb_tbhcuw.id]
    add_ons {
      is_kubernetes_dashboard_enabled = false
      is_tiller_enabled               = false
    }
    admission_controller_options {
      is_pod_security_policy_enabled = false
    }
    kubernetes_network_config {
      pods_cidr     = "10.240.0.0/12"
      services_cidr = "10.96.0.0/16"
    }
    persistent_volume_config {
    }
    service_lb_config {
      backend_nsg_ids = []
    }
  }
}
