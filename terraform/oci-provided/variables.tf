# The PROVIDED OKE cluster, codified via terraform import: plan only, NEVER
# apply (CLAUDE.md, the 2026-10-07 exception); every command through
# scripts/tf_provided.sh. Written by scripts/tf_provided_codify.py from the
# generated configuration: OCIDs are references or variables (values in the
# gitignored terraform.tfvars), tags and null attributes dropped.

variable "region" {
  description = "Region of the provided cluster."
  type        = string
  default     = "us-ashburn-1"
}

variable "availability_domain_1" {
  description = "Availability-domain name (tenancy-prefixed)."
  type        = string
}

variable "compartment_ocid" {
  description = "OCID: compartment_id of sl_pub_lb_tbhcuw (not a codified resource, so a variable)."
  type        = string
}

variable "nat_nat_gateway_public_ip_id" {
  description = "OCID: public_ip_id of nat_nat_gateway (not a codified resource, so a variable)."
  type        = string
}

variable "pool_oke_cpu_image_id" {
  description = "OCID: image_id of pool_oke_cpu (not a codified resource, so a variable)."
  type        = string
}

variable "pool_oke_cpu_ssh_public_key" {
  description = "SSH public key set on pool_oke_cpu."
  type        = string
}

variable "pool_oke_cpu_user_data" {
  description = "Node cloud-init (base64 gzip) set on pool_oke_cpu: an SSH key with its owner, the cluster CA."
  type        = string
}

variable "sgw_service_gateway_service_id" {
  description = "OCID: service_id of sgw_service_gateway (not a codified resource, so a variable)."
  type        = string
}
