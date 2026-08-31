data "oci_identity_availability_domains" "ads" {
  compartment_id = var.tenancy_ocid
}

# OKE-optimized node images for this cluster's Kubernetes version. Source names
# look like "Oracle-Linux-8.10-2026.06.30-0-OKE-1.33.1-760" (plain) and
# "Oracle-Linux-8.10-Gen2-GPU-2026.06.30-0-OKE-1.33.1-760" (GPU, ships the
# NVIDIA driver + container toolkit — required for the A10 pool).
data "oci_containerengine_node_pool_option" "oke" {
  node_pool_option_id = oci_containerengine_cluster.oke.id
  compartment_id      = var.compartment_ocid
}

locals {
  oke_version_tag = "OKE-${trimprefix(var.kubernetes_version, "v")}"

  app_node_image_ids = [
    for s in data.oci_containerengine_node_pool_option.oke.sources : s.image_id
    if strcontains(s.source_name, local.oke_version_tag)
    && !strcontains(s.source_name, "GPU")
    && !strcontains(s.source_name, "aarch64")
  ]

  gpu_node_image_ids = [
    for s in data.oci_containerengine_node_pool_option.oke.sources : s.image_id
    if strcontains(s.source_name, local.oke_version_tag)
    && strcontains(s.source_name, "GPU")
    && !strcontains(s.source_name, "aarch64")
  ]

  gpu_ad = coalesce(
    var.gpu_availability_domain,
    data.oci_identity_availability_domains.ads.availability_domains[0].name,
  )
}

# App pool: everything except vLLM (api, worker, streamlit, mcp, redis,
# postgres, Argo). 2x E4.Flex @ 4 OCPUs / 32 GB = 16 vCPU / 64 GB schedulable
# budget for K8s requests/limits.
resource "oci_containerengine_node_pool" "app" {
  cluster_id         = oci_containerengine_cluster.oke.id
  compartment_id     = var.compartment_ocid
  name               = "${var.project}-app-pool"
  kubernetes_version = var.kubernetes_version
  node_shape         = "VM.Standard.E4.Flex"
  freeform_tags      = local.tags

  node_shape_config {
    ocpus         = var.app_node_ocpus
    memory_in_gbs = var.app_node_memory_gbs
  }

  node_source_details {
    source_type             = "IMAGE"
    image_id                = local.app_node_image_ids[0]
    boot_volume_size_in_gbs = 100
  }

  node_config_details {
    size = var.app_pool_size

    # Spread across all ADs in the region (single-AD regions get one entry).
    dynamic "placement_configs" {
      for_each = data.oci_identity_availability_domains.ads.availability_domains
      content {
        availability_domain = placement_configs.value.name
        subnet_id           = oci_core_subnet.workers.id
      }
    }

    node_pool_pod_network_option_details {
      cni_type = "FLANNEL_OVERLAY"
    }
  }

  initial_node_labels {
    key   = "pool"
    value = "app"
  }
}

# GPU pool: 1x VM.GPU.A10.1 (1x A10 24 GB VRAM, 15 OCPUs, 240 GB RAM) for vLLM
# serving the fine-tuned Qwen2.5-1.5B. Fixed shape — no node_shape_config.
# OKE auto-taints GPU-image nodes with nvidia.com/gpu:NoSchedule, so the vLLM
# deployment (and nothing else) needs the matching toleration + selector; that
# lands in the k8s oke overlay. Boot volume sized for the CUDA image + model.
resource "oci_containerengine_node_pool" "gpu" {
  cluster_id         = oci_containerengine_cluster.oke.id
  compartment_id     = var.compartment_ocid
  name               = "${var.project}-gpu-pool"
  kubernetes_version = var.kubernetes_version
  node_shape         = "VM.GPU.A10.1"
  freeform_tags      = local.tags

  node_source_details {
    source_type             = "IMAGE"
    image_id                = local.gpu_node_image_ids[0]
    boot_volume_size_in_gbs = 250
  }

  node_config_details {
    size = var.gpu_pool_size

    placement_configs {
      availability_domain = local.gpu_ad
      subnet_id           = oci_core_subnet.workers.id
    }

    node_pool_pod_network_option_details {
      cni_type = "FLANNEL_OVERLAY"
    }
  }

  initial_node_labels {
    key   = "pool"
    value = "gpu"
  }
}
