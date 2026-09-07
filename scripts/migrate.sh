#!/usr/bin/env bash
# SIGM Colombia — Database migration script
# Usage: ./scripts/migrate.sh [message]

set -euo pipefail

MESSAGE="${1:-auto migration}"

echo "=== SIGM Colombia — Database Migration ==="

cd backend

# Check if alembic is available
if ! command -v alembic >/dev/null 2>&1; then
  echo "Installing alembic..."
  pip install alembic --quiet
fi

echo "Generating migration: $MESSAGE"
alembic revision --autogenerate -m "$MESSAGE"

echo ""
echo "Apply migration? (y/n)"
read -r REPLY
if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
  echo "Applying migration..."
  alembic upgrade head
  echo "Migration applied ✓"
else
  echo "Migration generated but not applied"
  echo "To apply later: cd backend && alembic upgrade head"
fi

cd ..
