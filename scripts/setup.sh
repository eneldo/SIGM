#!/usr/bin/env bash
# SIGM Colombia — Setup script
# Sets up development environment from scratch

set -euo pipefail

echo "=== SIGM Colombia — Setup ==="

# Check dependencies
command -v docker >/dev/null 2>&1 || { echo "ERROR: docker not found"; exit 1; }
command -v docker compose >/dev/null 2>&1 || { echo "ERROR: docker compose not found"; exit 1; }

# Create .env if not exists
if [ ! -f .env ]; then
  echo "Creating .env from .env.example..."
  cat > .env <<'EOF'
# SIGM Environment
SECRET_KEY=dev-secret-key-change-in-production
DB_PASSWORD=sigm
DATABASE_URL=postgresql+asyncpg://sigm:sigm@localhost:5432/sigm
CORS_ORIGINS=["http://localhost:3000"]
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
EOF
  echo ".env created"
fi

# Start infrastructure
echo "Starting infrastructure..."
docker compose -f docker-compose.dev.yml up -d postgres

echo "Waiting for PostgreSQL..."
sleep 5

# Setup backend
echo "Setting up backend..."
cd backend
python -m venv .venv 2>/dev/null || true

if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
elif [ -f .venv/Scripts/activate ]; then
  source .venv/Scripts/activate
fi

pip install -e ".[dev]" --quiet

# Run migrations
echo "Running migrations..."
alembic upgrade head

# Seed demo data
echo "Seeding demo data..."
python -m scripts.seed_demo 2>/dev/null || echo "Seed skipped (may need DB)"

cd ..

# Setup frontend
echo "Setting up frontend..."
cd frontend
npm install --silent
cd ..

echo ""
echo "=== Setup complete ==="
echo ""
echo "To start development:"
echo "  docker compose -f docker-compose.dev.yml up"
echo ""
echo "Or manually:"
echo "  Backend:  cd backend && uvicorn app.main:app --reload --port 8000"
echo "  Frontend: cd frontend && npm run dev"
echo ""
echo "Access:"
echo "  API:   http://localhost:8000/docs"
echo "  App:   http://localhost:3000"
echo ""
