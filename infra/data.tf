data "aws_caller_identity" "current" {}

# Use the account's default VPC and its (public) subnets — Fargate tasks get a
# public IP and reach the internet via the VPC's internet gateway, so there's
# no NAT gateway cost.
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}
