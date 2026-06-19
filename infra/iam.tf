data "aws_iam_policy_document" "ecs_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# ── Task execution role: pulls the image, reads secrets, writes logs ─────────

resource "aws_iam_role" "task_execution" {
  name               = "${var.project}-task-execution"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}

resource "aws_iam_role_policy_attachment" "task_execution_managed" {
  role       = aws_iam_role.task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Permission to read exactly this project's secrets (injected as task env vars).
resource "aws_iam_role_policy" "task_execution_secrets" {
  name = "read-${var.project}-secrets"
  role = aws_iam_role.task_execution.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["secretsmanager:GetSecretValue"]
      Resource = concat(
        [aws_secretsmanager_secret.database_url.arn, aws_secretsmanager_secret.redis_url.arn],
        [for s in aws_secretsmanager_secret.user : s.arn],
      )
    }]
  })
}

# ── Task role: the app's own runtime identity. The app doesn't call AWS APIs
# (secrets arrive as env vars), so this role intentionally has no policies. ───

resource "aws_iam_role" "task" {
  name               = "${var.project}-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}
