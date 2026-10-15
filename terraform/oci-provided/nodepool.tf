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
    user_data                = "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"
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
    user_data                = "H4sIAAAAAAAA/7RWXY/jthV9H2D/g+CHTILUY31Y03iKFB3JpG3ZokOKpGS+LGSRM5JFfawkf4yRH194drdNs0ne+mKDV4c89xwc4F6/qQdVD2P61qonozrqoWjTbphUxUXJfxj75ljLtHv7eRSuQuBtGZo/k93o7nYac9X1RVM/GdaD+eHuw914/FvQh7v/vN2ldf+iujGos0YW9euT8fd9MfwG8E4+qMswyXRzlOOsqV+K1w93YVGp39Ek41B1r+rLHV30w/dp26pa/vCjLLLh+7r52KlWp5n6W6eyY9erjzfQDz/2Q/cVeWt21B3rrJKjp7uxMcqOnTbG/cYYN8bklHaT7lhPmlKN61Olxl1ayIc+N/JhaPunyaRLzw+vxZAf98deddlnEQ9ZU02aLs20Gn86FlnZDzcfm6wY5202bko16dRLP8lVKvtJlRb15KXQqv+G5s4wvvvO+H6f9vlf9HJvmffGr78aKssb4x50XdMZRV0MRaqLa1G/GuR5Nb83/vmd/cPoLxUe98d6OI4/+3574f+r9I/o/lTxH/Z2f7IenOmDdW/cv6S6V//9/1877gxj3zRDP3Rp294c2a7BV0NGfZ9/TI9D3nTFVcmPpXrrPyeh7/OxkrbrWjPj+fn52XfQNfUtLeYrC1Hg3mqrTYlnSeiyl877BKzl1aGPiwR06xfvbbWP4Gu/PjpOeV1Nzc2dYXTHa358yHJV/+uzazcDR3ejc1cM6uO7NV9S+Nnf0ZMxsswHa2o+mA/O6M4wRm065LfyRA3ZzZl3d9K26FV3Ut3od5c3kTlsIssnTAa08OaEByxiIsAmZOT9mzn4pRVEjLQcoDmO3aUwoROxwBOmjjCz4MbOT/htNmTXYCN1APeJfuQMLWKtHQKhiMrhFJe6kRXaYg4hBQHBSbaOFy1kwPJCIL2Qc4gT6RALPabLNiDM9SmHV2kiEjMSMw6XJJFrrvkj4R7C1FtiCjlhgSNNSWIoHgWQvcQtYjR/5yVQEMYGgHmLd7a1SKtgyZMcEAA3uJJbXgZeZlpeONefdpxAalqeNL/0YkKHaLHkByJiYDl+mTc700Wp1lPKiKeYxcTVQxxAl9v5gZbWI0lyRAB0KSd1CCyGE52kZaApB1Npkq86bvwpBbMVjbM1ox5UAD1i1vrCdGNcQsEB7Lkmv9OR33T4AubbcAETtMyBKuH2q469afnpVbsxl9vs3KYccEQZPBETXDjjc+lIwOfBNgMWQUsJMNeAa0giRjyueRov8mbntHNsQholEjCu15E9S6M4t3em6zHGfb8MCGakFibHmJEbluxNdDv7mFnV2uIur0gVce8UHqAfWtzP4pUrqTdHZeuHB76Iy4stryQIY1Kgq1fR6Kc1LoOj4LkTM3zCtVesrfC6o2QTRbNeVZxllgwz7dFsMYObq16kFHS0bAcGtbexguWW8TlPUJLW3mFftYt9OXza4fYTt3QiKiuM54Ej7BmhMO92VLoIlm/kECwZcBPFEOcxIVJ7KKTZ2z4puxgIrqrGpkvYq+rVYY5wxUGeWSXOfpW5qhwAMd01OXDOFvCg5p7HD3qxBcLcUh7s7PKsqlnC44tg/synsXhkixaGdX5V8dmJ5+QTn2tXvA2H7RK2qfW8lkv8FpkSpJWso9q78sQ77Sru8bfBxvXKjuK8ixdomtrBSUSz0/oaTBXNzKiYlaGJztR2W7Fw3wQlIXWAy5kOo+d2HpVcEAeZgqOCQXlkNjgzC2lScsZrzyWMH/aOaCJYTmkF7BSIjYCav+efQW/H3Dll3JMmcd7ze/CYX0IS+TMfc+7gREJczB4xm73nN4JgiktYbcF7JuaYQyHNnHy5+wsuA0GYmIexSzfm7JwCct7TZ3dXhevtsjmRhADmhB2xLw1l4ExMRDMmaRSvrgRCiEvkcAY9BLSPOfQUcIstyEwWkzex9ADW3kpSj1CTmLKCa4xbKiCizL4IUsIDjbmPrOyCeR5RKK4Kwl2k+Tqydk6mdUy1tjPYMlS6dqw5yZi7opboaII27Bow6rQ10WLrV8Mvwp7hLOFxDOVS2BKtLTiPF+05W/AcgUu7S+CZVcimgJ/j2HpkWvRqEbR7Gjzuq4vYz/USO8xBjMe8hkXqvK73VmNR+3VKTcvdmMNBwvYgl9InXB4zf3YhMSeYo4ZXlykBM7C2+Gl3zf0sbgVbEH9X8RCbmZnG+pc9DS+yRBE6t+m+Gs7UHxAFMo2giDDNYbjMF1zLEypJF8b9KQLaYvbsxBOEidnq/UInGfSqffGTiRZBxOrgQCqRR3Hb7ljA/HKI0jifE9PdSLOdYtPdSkucFCf27gC7LctPKcCniOuNoGIeV0OH5ruzmq9OaS3qyAk6FF8goShKE6HT1+Z93mwY3xL/T2bR688/v4859WU/vA2x/eP0vdaca9XdCl3TDE+3n28nYnncq65Wg+onWfqQdV8gqquK/rY69jek+Tidjr7ZUsfjD3f/DgAA//+t8ptbBAsAAA=="
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
