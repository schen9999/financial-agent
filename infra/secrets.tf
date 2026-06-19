locals {
  # Built from the RDS instance + generated password; injected into the task as
  # the DATABASE_URL env var (via the task definition in Phase 3).
  database_url = "postgresql://${var.db_username}:${random_password.db.result}@${aws_db_instance.postgres.address}:5432/${var.db_name}"
}

# ── Secrets Terraform populates ───────────────────────────────────────────────

resource "aws_secretsmanager_secret" "database_url" {
  name = "${var.project}/DATABASE_URL"
}
resource "aws_secretsmanager_secret_version" "database_url" {
  secret_id     = aws_secretsmanager_secret.database_url.id
  secret_string = local.database_url
}

# Placeholder so the app boots (cache.py / celery_worker.py require REDIS_URL at
# import). cache.py catches connection failures and no-ops, so caching is simply
# disabled; /research/async (Celery) is non-functional, as intended.
resource "aws_secretsmanager_secret" "redis_url" {
  name = "${var.project}/REDIS_URL"
}
resource "aws_secretsmanager_secret_version" "redis_url" {
  secret_id     = aws_secretsmanager_secret.redis_url.id
  secret_string = "redis://localhost:6379"
}

# ── Secrets YOU fill after apply (Terraform never sees the real values) ───────

resource "aws_secretsmanager_secret" "user" {
  for_each = toset(var.user_filled_secrets)
  name     = "${var.project}/${each.key}"
}

resource "aws_secretsmanager_secret_version" "user" {
  for_each      = aws_secretsmanager_secret.user
  secret_id     = each.value.id
  secret_string = "REPLACE_ME"

  # After you set the real value in the console/CLI, later applies won't revert it.
  lifecycle {
    ignore_changes = [secret_string]
  }
}
