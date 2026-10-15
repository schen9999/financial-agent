# The PROVIDED OKE cluster, codified via terraform import: plan only, NEVER
# apply (CLAUDE.md, the 2026-10-07 exception); every command through
# scripts/tf_provided.sh. Written by scripts/tf_provided_codify.py from the
# generated configuration: OCIDs are references or variables (values in the
# gitignored terraform.tfvars), tags and null attributes dropped.

resource "oci_containerengine_node_pool" "pool_oke_cpu" {
  cluster_id         = oci_containerengine_cluster.cluster_oke_test_tbhcuw.id
  compartment_id     = var.compartment_ocid
  kubernetes_version = "v1.34.1"
  name               = "oke-cpu"
  node_metadata = {
    apiserver_host           = "10.140.0.3"
    oke-kubeproxy-proxy-mode = "iptables"
    user_data                = var.pool_oke_cpu_user_data
  }
  node_shape     = "VM.Standard.E5.Flex"
  ssh_public_key = var.pool_oke_cpu_ssh_public_key
  initial_node_labels {
    key   = "oci.oraclecloud.com/vcn-native-ip-cni"
    value = jsonencode(true)
  }
  initial_node_labels {
    key   = "oke.oraclecloud.com/cluster_autoscaler"
    value = "disabled"
  }
  initial_node_labels {
    key   = "oke.oraclecloud.com/pool.mode"
    value = "node-pool"
  }
  initial_node_labels {
    key   = "oke.oraclecloud.com/pool.name"
    value = "oke-cpu"
  }
  initial_node_labels {
    key   = "oke.oraclecloud.com/tf.module"
    value = "terraform-oci-oke"
  }
  initial_node_labels {
    key   = "oke.oraclecloud.com/tf.state_id"
    value = "tbhcuw"
  }
  node_config_details {
    is_pv_encryption_in_transit_enabled = false
    nsg_ids                             = [oci_core_network_security_group.nsg_workers_tbhcuw.id]
    size                                = 2
    node_pool_pod_network_option_details {
      cni_type          = "OCI_VCN_IP_NATIVE"
      max_pods_per_node = 110
      pod_nsg_ids       = [oci_core_network_security_group.nsg_pods_tbhcuw.id]
      pod_subnet_ids    = [oci_core_subnet.subnet_pods_tbhcuw.id]
    }
    placement_configs {
      availability_domain = var.availability_domain_1
      fault_domains       = []
      subnet_id           = oci_core_subnet.subnet_workers_tbhcuw.id
    }
  }
  node_eviction_node_pool_settings {
    eviction_grace_duration              = "PT5M"
    is_force_action_after_grace_duration = false
    is_force_delete_after_grace_duration = true
  }
  node_pool_cycling_details {
    cycle_modes             = ["INSTANCE_REPLACE"]
    is_node_cycling_enabled = false
    maximum_surge           = jsonencode(1)
    maximum_unavailable     = jsonencode(0)
  }
  node_shape_config {
    memory_in_gbs = 64
    ocpus         = 8
  }
  node_source_details {
    boot_volume_size_in_gbs = jsonencode(256)
    image_id                = var.pool_oke_cpu_image_id
    source_type             = "IMAGE"
  }
}

resource "oci_containerengine_node_pool" "pool_oke_system" {
  cluster_id         = oci_containerengine_cluster.cluster_oke_test_tbhcuw.id
  compartment_id     = var.compartment_ocid
  kubernetes_version = "v1.34.1"
  name               = "oke-system"
  node_metadata = {
    apiserver_host           = "10.140.0.3"
    oke-kubeproxy-proxy-mode = "iptables"
    user_data                = var.pool_oke_cpu_user_data
  }
  node_shape     = "VM.Standard.E5.Flex"
  ssh_public_key = var.pool_oke_cpu_ssh_public_key
  initial_node_labels {
    key   = "oci.oraclecloud.com/vcn-native-ip-cni"
    value = jsonencode(true)
  }
  initial_node_labels {
    key   = "oke.oraclecloud.com/cluster_autoscaler"
    value = "disabled"
  }
  initial_node_labels {
    key   = "oke.oraclecloud.com/pool.mode"
    value = "node-pool"
  }
  initial_node_labels {
    key   = "oke.oraclecloud.com/pool.name"
    value = "oke-system"
  }
  initial_node_labels {
    key   = "oke.oraclecloud.com/tf.module"
    value = "terraform-oci-oke"
  }
  initial_node_labels {
    key   = "oke.oraclecloud.com/tf.state_id"
    value = "tbhcuw"
  }
  node_config_details {
    is_pv_encryption_in_transit_enabled = false
    nsg_ids                             = [oci_core_network_security_group.nsg_workers_tbhcuw.id]
    size                                = 2
    node_pool_pod_network_option_details {
      cni_type          = "OCI_VCN_IP_NATIVE"
      max_pods_per_node = 110
      pod_nsg_ids       = [oci_core_network_security_group.nsg_pods_tbhcuw.id]
      pod_subnet_ids    = [oci_core_subnet.subnet_pods_tbhcuw.id]
    }
    placement_configs {
      availability_domain = var.availability_domain_1
      fault_domains       = []
      subnet_id           = oci_core_subnet.subnet_workers_tbhcuw.id
    }
  }
  node_eviction_node_pool_settings {
    eviction_grace_duration              = "PT5M"
    is_force_action_after_grace_duration = false
    is_force_delete_after_grace_duration = true
  }
  node_pool_cycling_details {
    cycle_modes             = ["INSTANCE_REPLACE"]
    is_node_cycling_enabled = false
    maximum_surge           = jsonencode(1)
    maximum_unavailable     = jsonencode(0)
  }
  node_shape_config {
    memory_in_gbs = 32
    ocpus         = 8
  }
  node_source_details {
    boot_volume_size_in_gbs = jsonencode(256)
    image_id                = var.pool_oke_cpu_image_id
    source_type             = "IMAGE"
  }
}
