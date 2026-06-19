# Infrastructure (Terraform)

Provisions the AWS foundation for the FastAPI backend: ECR, RDS Postgres,
Secrets Manager, IAM roles, and networking (security groups over the default
VPC's public subnets — no NAT gateway). ECS Fargate (the service) and the
GitHub OIDC deploy role come in later phases.

State is **local** (`terraform.tfstate`, gitignored — it contains the generated
RDS password).

## Apply

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars   # then set allowed_ip to your IP/32
terraform init
terraform plan
terraform apply
```

RDS takes ~5–10 minutes to come up.

## After apply: fill the secrets

Terraform creates these empty (value `REPLACE_ME`). Set the real values — later
applies won't overwrite them:

```bash
for s in ANTHROPIC_API_KEY NEWS_API_KEY PINECONE_API_KEY LANGSMITH_API_KEY; do
  aws secretsmanager put-secret-value \
    --secret-id "financial-agent/$s" \
    --secret-string "YOUR_REAL_VALUE" --region us-east-1
done
```

`DATABASE_URL` and `REDIS_URL` are populated by Terraform (RDS URL + a Redis
placeholder), so you don't touch those.

## Useful outputs

```bash
terraform output ecr_repository_url     # where the image gets pushed
terraform output secret_arns            # ARNs for the task definition (Phase 3)
terraform output rds_endpoint
```

## Teardown

```bash
terraform destroy
```
