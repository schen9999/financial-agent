# ── Phase 3: ECS cluster, task definition, Fargate service ───────────────────

variable "image_tag" {
  description = "Container image tag the service runs (CI pushes 'latest' + the commit SHA)"
  type        = string
  default     = "latest"
}

variable "desired_count" {
  description = "Number of Fargate tasks"
  type        = number
  default     = 1
}

variable "task_cpu" {
  description = "Fargate CPU units (1024 = 1 vCPU)"
  type        = number
  default     = 1024
}

variable "task_memory" {
  description = "Fargate memory in MB (3 GB headroom for the torch/embedding stack)"
  type        = number
  default     = 3072
}

resource "aws_ecs_cluster" "main" {
  name = "${var.project}-cluster"

  setting {
    name  = "containerInsights"
    value = "disabled" # keep cost down; enable for metrics later
  }
}

resource "aws_cloudwatch_log_group" "api" {
  name              = "/ecs/${var.project}-api"
  retention_in_days = 14
}

locals {
  # env-var name -> Secrets Manager ARN; injected by the execution role.
  secret_arns_map = merge(
    {
      DATABASE_URL = aws_secretsmanager_secret.database_url.arn
      REDIS_URL    = aws_secretsmanager_secret.redis_url.arn
    },
    { for k, s in aws_secretsmanager_secret.user : k => s.arn },
  )
}

resource "aws_ecs_task_definition" "api" {
  family                   = "${var.project}-api"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.task_execution.arn
  task_role_arn            = aws_iam_role.task.arn

  container_definitions = jsonencode([{
    name      = "api"
    image     = "${aws_ecr_repository.api.repository_url}:${var.image_tag}"
    essential = true

    portMappings = [{ containerPort = var.container_port, protocol = "tcp" }]

    # Feature flags default-off; secrets come from Secrets Manager (below).
    environment = [
      { name = "RERANKING_ENABLED", value = "false" },
      { name = "USE_LOCAL_MODEL", value = "false" },
      { name = "LANGSMITH_TRACING", value = "true" },
      { name = "LANGSMITH_PROJECT", value = var.project },
    ]

    secrets = [for name, arn in local.secret_arns_map : { name = name, valueFrom = arn }]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.api.name
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "api"
      }
    }
  }])
}

resource "aws_ecs_service" "api" {
  name            = "${var.project}-api"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = true # public subnet, no NAT — needed to pull from ECR + reach the internet
  }

  # The CI/CD deploy registers new task-definition revisions and may scale, so
  # don't let terraform revert those on the next apply.
  lifecycle {
    ignore_changes = [task_definition, desired_count]
  }
}
