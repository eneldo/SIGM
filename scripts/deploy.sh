#!/usr/bin/env bash
# SIGM Colombia — Production deployment
# Usage: ./scripts/deploy.sh [environment]

set -euo pipefail

ENV="${1:-staging}"

echo "=== SIGM Colombia — Deploy to $ENV ==="

# Build images
echo "Building backend image..."
docker build -f Dockerfile.backend -t sigm-backend:latest .

echo "Building frontend image..."
docker build -f frontend/Dockerfile -t sigm-frontend:latest ./frontend

# Deploy
if [ "$ENV" = "production" ]; then
  echo "Deploying to production..."
  docker compose -f docker-compose.prod.yml up -d --force-recreate
elif [ "$ENV" = "staging" ]; then
  echo "Deploying to staging..."
  docker compose -f docker-compose.prod.yml up -d --force-recreate
else
  echo "Unknown environment: $ENV"
  exit 1
fi

echo ""
echo "=== Deploy complete ==="
echo "Backend:  http://localhost:8000/docs"
echo "Frontend: http://localhost:3000"
