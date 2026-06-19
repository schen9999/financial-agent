output "ecr_repository_url" {
  description = "Push the image here (used by the deploy workflow in Phase 4)"
  value       = aws_ecr_repository.api.repository_url
}

output "rds_endpoint" {
  description = "RDS Postgres host"
  value       = aws_db_instance.postgres.address
}

output "ecs_tasks_security_group_id" {
  value = aws_security_group.ecs_tasks.id
}

output "subnet_ids" {
  description = "Public subnets the Fargate service runs in"
  value       = data.aws_subnets.default.ids
}

output "task_execution_role_arn" {
  value = aws_iam_role.task_execution.arn
}

output "task_role_arn" {
  value = aws_iam_role.task.arn
}

# Non-sensitive: ARNs/names, not values. Use these to fill the secrets and wire
# the task definition in Phase 3.
output "secret_arns" {
  description = "Secrets Manager ARNs by env-var name"
  value = merge(
    {
      DATABASE_URL = aws_secretsmanager_secret.database_url.arn
      REDIS_URL    = aws_secretsmanager_secret.redis_url.arn
    },
    { for k, s in aws_secretsmanager_secret.user : k => s.arn },
  )
}

output "user_filled_secret_names" {
  description = "Set real values for these after apply"
  value       = [for k in var.user_filled_secrets : "${var.project}/${k}"]
}
