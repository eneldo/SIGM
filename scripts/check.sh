#!/usr/bin/env bash
# SIGM Colombia — Run all checks
# Validates code quality before commit

set -euo pipefail

echo "=== SIGM Colombia — Code Quality Checks ==="
ERRORS=0

# ─── Backend Lint ───
echo ""
echo "▶ Backend: Ruff lint"
cd backend
if python -m ruff check . ; then
  echo "  ✓ Ruff check passed"
else
  echo "  ✗ Ruff check failed"
  ERRORS=$((ERRORS + 1))
fi

echo "▶ Backend: Ruff format"
if python -m ruff format --check . ; then
  echo "  ✓ Ruff format passed"
else
  echo "  ✗ Ruff format failed"
  ERRORS=$((ERRORS + 1))
fi

# ─── Backend Type Check ───
echo ""
echo "▶ Backend: mypy"
if python -m mypy app --ignore-missing-imports ; then
  echo "  ✓ mypy passed"
else
  echo "  ✗ mypy failed"
  ERRORS=$((ERRORS + 1))
fi

# ─── Backend Tests ───
echo ""
echo "▶ Backend: pytest"
if python -m pytest tests/ -v --tb=short -x ; then
  echo "  ✓ Tests passed"
else
  echo "  ✗ Tests failed"
  ERRORS=$((ERRORS + 1))
fi

cd ..

# ─── Frontend ───
echo ""
echo "▶ Frontend: ESLint"
cd frontend
if npm run lint --silent 2>&1; then
  echo "  ✓ ESLint passed"
else
  echo "  ✗ ESLint failed"
  ERRORS=$((ERRORS + 1))
fi

echo "▶ Frontend: TypeScript"
if npm run typecheck --silent 2>&1; then
  echo "  ✓ TypeCheck passed"
else
  echo "  ✗ TypeCheck failed"
  ERRORS=$((ERRORS + 1))
fi

cd ..

echo ""
echo "=== Results ==="
if [ $ERRORS -eq 0 ]; then
  echo "All checks passed ✓"
  exit 0
else
  echo "$ERRORS check(s) failed ✗"
  exit 1
fi
