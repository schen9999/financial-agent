# Security group for the Fargate task: the API is reachable ONLY from your IP.
# Widen the ingress CIDR temporarily when you want to demo from elsewhere.
resource "aws_security_group" "ecs_tasks" {
  name        = "${var.project}-ecs-tasks"
  description = "Fargate API task: inbound on the app port from the allowed IP only"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "API from allowed IP"
    from_port   = var.container_port
    to_port     = var.container_port
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ip]
  }

  egress {
    description = "All outbound (ECR pull, Anthropic/Pinecone/NewsAPI, RDS)"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${var.project}-ecs-tasks" }
}

# RDS is reachable only from the Fargate task SG (not the internet).
resource "aws_security_group" "rds" {
  name        = "${var.project}-rds"
  description = "RDS Postgres: inbound 5432 from the ECS task SG only"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description     = "Postgres from ECS tasks"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_tasks.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${var.project}-rds" }
}
