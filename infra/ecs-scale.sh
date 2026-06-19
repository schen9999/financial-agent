#!/usr/bin/env bash
# Pause / resume the Fargate backend to control cost.
#   infra/ecs-scale.sh 0   # pause  — stop the task (no Fargate compute cost)
#   infra/ecs-scale.sh 1   # resume — launch a fresh task (gets a new public IP)
#
# The ECS service ignores desired_count in Terraform, so this won't be reverted
# by `terraform apply`. RDS keeps running (free tier) either way.
set -euo pipefail

COUNT="${1:-}"
if [[ "$COUNT" != "0" && "$COUNT" != "1" ]]; then
  echo "usage: $0 <0|1>   (0 = pause, 1 = resume)" >&2
  exit 1
fi

REGION="us-east-1"
CLUSTER="financial-agent-cluster"
SERVICE="financial-agent-api"

aws ecs update-service \
  --cluster "$CLUSTER" \
  --service "$SERVICE" \
  --desired-count "$COUNT" \
  --region "$REGION" \
  --query 'service.{service:serviceName,desired:desiredCount,running:runningCount}' \
  --output table

if [[ "$COUNT" == "1" ]]; then
  echo "Resuming — the task takes ~1-2 min to start. Get its new public IP with:"
  echo "  infra/ecs-ip.sh"
fi
