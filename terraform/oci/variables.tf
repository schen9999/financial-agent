variable "region" {
  description = "OCI region. Confirm A10 capacity in the chosen region before Phase 2 apply (VM.GPU.A10.1 is not available everywhere)."
  type        = string
  default     = "us-ashburn-1"
}

variable "tenancy_ocid" {
  description = "Tenancy OCID. Required for the Object Storage namespace lookup even when provider auth comes from ~/.oci/config."
  type        = string
}

variable "compartment_ocid" {
  description = "Compartment all resources are created in"
  type        = string
}

# --- Provider auth (all optional; unset -> ~/.oci/config or OCI_* env vars) ---

variable "user_ocid" {
  description = "API user OCID (leave null to use the CLI config file)"
  type        = string
  default     = null
}

variable "fingerprint" {
  description = "API key fingerprint (leave null to use the CLI config file)"
  type        = string
  default     = null
}

variable "private_key_path" {
  description = "Path to the API private key (leave null to use the CLI config file)"
  type        = string
  default     = null
}

# --- Naming / cluster ---

variable "project" {
  description = "Project name; prefixes all resource names (matches infra/ convention)"
  type        = string
  default     = "financial-agent"
}

variable "kubernetes_version" {
  description = "OKE Kubernetes version. OKE retires versions quickly — before the Phase 2 apply, confirm with `oci ce cluster-options get --cluster-option-id all` and bump if needed."
  type        = string
  default     = "v1.33.1"
}

variable "api_allowed_cidr" {
  description = "CIDR allowed to reach the public Kubernetes API endpoint (6443). Tighten to your IP (e.g. 1.2.3.4/32) in terraform.tfvars for the demo."
  type        = string
  default     = "0.0.0.0/0"
}

# --- Node pools ---
# App pool per CLAUDE.md: 2x VM.Standard.E4.Flex, 4 OCPUs / 32 GB each.
# 1 OCPU = 2 vCPUs, so the pool totals 16 vCPU / 64 GB for K8s requests/limits.

variable "app_pool_size" {
  description = "Number of app-pool worker nodes"
  type        = number
  default     = 2
}

variable "app_node_ocpus" {
  description = "OCPUs per app node (E4.Flex is a flexible shape)"
  type        = number
  default     = 4
}

variable "app_node_memory_gbs" {
  description = "Memory (GB) per app node"
  type        = number
  default     = 32
}

variable "gpu_pool_size" {
  description = "Number of GPU nodes (VM.GPU.A10.1: 1x A10 24 GB, 15 OCPUs, 240 GB)"
  type        = number
  default     = 1
}

variable "gpu_availability_domain" {
  description = "AD name for the GPU pool (A10 capacity varies by AD). Null picks the first AD; override in terraform.tfvars if launch fails with 'out of capacity'."
  type        = string
  default     = null
}

# --- Storage ---

variable "storage_class_name" {
  description = "Name of the Block Volume StorageClass created in the cluster; the k8s oke overlay must reference the same name"
  type        = string
  default     = "financial-agent-bv"
}
