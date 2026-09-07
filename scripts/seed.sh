#!/usr/bin/env bash
# SIGM Colombia — Seed demo data
# Usage: ./scripts/seed.sh

set -euo pipefail

echo "=== SIGM Colombia — Seed Demo Data ==="

cd backend
python -m scripts.seed_demo
cd ..

echo "Seed complete ✓"
