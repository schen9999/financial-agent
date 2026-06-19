#!/usr/bin/env bash
# Print the public IP + base URL of the running Fargate task (there's no ALB,
# so the IP changes each time the task is replaced).
set -euo pipefail

REGION="us-east-1"
CLUSTER="financial-agent-cluster"
SERVICE="financial-agent-api"

TASK=$(aws ecs list-tasks --cluster "$CLUSTER" --service-name "$SERVICE" \
  --region "$REGION" --query 'taskArns[0]' --output text)

if [[ "$TASK" == "None" || -z "$TASK" ]]; then
  echo "No running task — resume with: infra/ecs-scale.sh 1" >&2
  exit 1
fi

ENI=$(aws ecs describe-tasks --cluster "$CLUSTER" --tasks "$TASK" --region "$REGION" \
  --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value' --output text)

IP=$(aws ec2 describe-network-interfaces --network-interface-ids "$ENI" --region "$REGION" \
  --query 'NetworkInterfaces[0].Association.PublicIp' --output text)

echo "http://$IP:8000"
echo "health: curl -s http://$IP:8000/health"
