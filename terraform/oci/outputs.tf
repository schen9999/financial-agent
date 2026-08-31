output "cluster_id" {
  description = "OKE cluster OCID"
  value       = oci_containerengine_cluster.oke.id
}

output "kubeconfig_command" {
  description = "Run after apply to merge cluster access into ~/.kube/config"
  value       = "oci ce cluster create-kubeconfig --cluster-id ${oci_containerengine_cluster.oke.id} --region ${var.region} --token-version 2.0.0 --kube-endpoint PUBLIC_ENDPOINT"
}

output "ocir_app_repo_url" {
  description = "Push target for the app image (docker tag financial-agent-app:local <this>:<tag>)"
  value       = "${local.ocir_host}/${data.oci_objectstorage_namespace.ns.namespace}/${oci_artifacts_container_repository.app.display_name}"
}

output "ocir_login_hint" {
  description = "OCIR docker login: username is <namespace>/<user>, password is an auth token"
  value       = "docker login ${local.ocir_host} -u '${data.oci_objectstorage_namespace.ns.namespace}/<oci-username>'"
}

output "eval_artifacts_bucket" {
  description = "Object Storage bucket for eval artifacts"
  value       = oci_objectstorage_bucket.eval_artifacts.name
}

output "storage_class_name" {
  description = "StorageClass the k8s oke overlay must reference for PVCs"
  value       = kubernetes_storage_class_v1.block_volume.metadata[0].name
}

output "app_node_pool_id" {
  description = "App node pool OCID"
  value       = oci_containerengine_node_pool.app.id
}

output "gpu_node_pool_id" {
  description = "GPU node pool OCID"
  value       = oci_containerengine_node_pool.gpu.id
}
