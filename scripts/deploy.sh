#!/usr/bin/env bash
# build image, push to ecr, bounce ecs service; fails loud if any step breaks
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
  echo "usage: $0 <aws_region> <ecr_repo> <ecs_cluster> <ecs_service>"
}

if [[ $# -ne 4 ]]; then usage; exit 1; fi
REGION="$1"
ECR_REPO="$2"
CLUSTER="$3"
SERVICE="$4"

need() { command -v "$1" >/dev/null 2>&1 || { echo -e "${RED}missing:${NC} $1"; exit 1; }; }
need aws
need docker

ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
IMAGE="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ECR_REPO}:$(date +%Y%m%d%H%M%S)"

echo -e "${GREEN}logging docker into ecr${NC}"
aws ecr get-login-password --region "$REGION" \
  | docker login --username AWS --password-stdin "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"

echo -e "${GREEN}building${NC}"
docker build -t "$IMAGE" .

echo -e "${GREEN}pushing${NC}"
docker push "$IMAGE"

echo -e "${YELLOW}forcing new deployment${NC}"
aws ecs update-service --region "$REGION" --cluster "$CLUSTER" --service "$SERVICE" \
  --force-new-deployment >/dev/null

echo -e "${GREEN}deploy triggered for${NC} $IMAGE"
