# Generated master password (no special chars so it slots cleanly into the
# postgresql:// URL without escaping). Stored only in Secrets Manager + state.
resource "random_password" "db" {
  length  = 24
  special = false
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.project}-db-subnets"
  subnet_ids = data.aws_subnets.default.ids
}

resource "aws_db_instance" "postgres" {
  identifier     = "${var.project}-db"
  engine         = "postgres"
  engine_version = "16"
  instance_class = "db.t3.micro" # free-tier eligible

  allocated_storage = 20 # free tier includes 20 GB
  storage_type      = "gp2"

  db_name  = var.db_name
  username = var.db_username
  password = random_password.db.result

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  publicly_accessible    = false # only the ECS task SG can reach it
  multi_az               = false # single-AZ for free tier
  skip_final_snapshot    = true  # demo project — no final snapshot on destroy
  deletion_protection    = false
  apply_immediately      = true
}
