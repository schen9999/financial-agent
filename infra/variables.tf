variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project" {
  description = "Project name; prefixes all resource names"
  type        = string
  default     = "financial-agent"
}

variable "allowed_ip" {
  description = "Your public IP in CIDR form (e.g. 1.2.3.4/32) allowed to reach the API. Set in terraform.tfvars (gitignored) so it never lands in the public repo."
  type        = string
  # no default on purpose — must be provided via terraform.tfvars or -var
}

variable "container_port" {
  description = "Port the FastAPI container listens on"
  type        = number
  default     = 8000
}

variable "db_name" {
  description = "RDS database name"
  type        = string
  default     = "financial_agent"
}

variable "db_username" {
  description = "RDS master username"
  type        = string
  default     = "financial_admin"
}

# Secrets created empty for you to fill in the console/CLI (Terraform never sees
# your real keys). Their values are ignored on subsequent applies (see secrets.tf).
variable "user_filled_secrets" {
  description = "Secret names you populate by hand after apply"
  type        = list(string)
  default     = ["ANTHROPIC_API_KEY", "NEWS_API_KEY", "PINECONE_API_KEY", "LANGSMITH_API_KEY"]
}
