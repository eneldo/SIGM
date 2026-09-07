#!/usr/bin/env bash
# SIGM Colombia — Install git hooks
# Run after clone: ./scripts/install-hooks.sh

set -euo pipefail

echo "Installing pre-commit hooks..."

if command -v pre-commit >/dev/null 2>&1; then
  pre-commit install
  echo "Pre-commit hooks installed ✓"
else
  echo "pre-commit not found. Installing..."
  pip install pre-commit
  pre-commit install
  echo "Pre-commit hooks installed ✓"
fi
