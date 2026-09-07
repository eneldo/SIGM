# SIGM Colombia

Sistema Integral de Gestión Municipal — Plataforma SaaS multi-tenant para Alcaldías colombianas.

## Arquitectura

- **Backend:** FastAPI + SQLAlchemy 2 + PostgreSQL 17
- **Frontend:** Next.js 15 + React 19 + TypeScript + Tailwind CSS
- **Auth:** JWT + Argon2id + RBAC
- **Multitenancy:** tenant_id en todas las tablas de negocio

## Quick Start

```bash
# Setup
./scripts/setup.sh

# Start dev
docker compose -f docker-compose.dev.yml up

# Access
# API: http://localhost:8000/docs
# App: http://localhost:3000
```

## Structure

```
├── backend/          FastAPI application
│   ├── app/          Core application code
│   │   ├── api/      Route handlers
│   │   ├── core/     Config, security, database
│   │   ├── models/   SQLAlchemy models (25 tables)
│   │   ├── repositories/  Data access layer
│   │   ├── schemas/  Pydantic schemas
│   │   └── services/ Business logic
│   ├── tests/        Integration tests
│   ├── alembic/      Database migrations
│   └── scripts/      Seed data
├── frontend/         Next.js application
│   └── src/
│       ├── app/      Pages and routing
│       ├── components/  Reusable UI components
│       ├── features/ Feature modules
│       ├── lib/      Utilities and API client
│       └── types/    TypeScript types
├── docs/             Architecture documentation
├── scripts/          Utility scripts
└── .github/workflows/ CI/CD pipelines
```

## Scripts

| Script | Description |
|--------|-------------|
| `./scripts/setup.sh` | Full development setup |
| `./scripts/check.sh` | Run all code quality checks |
| `./scripts/migrate.sh` | Generate and apply migrations |
| `./scripts/seed.sh` | Seed demo data |
| `./scripts/deploy.sh` | Build and deploy |

## CI/CD

GitHub Actions workflows:
- `backend-ci.yml` — Lint, typecheck, test, build (on backend changes)
- `frontend-ci.yml` — Lint, typecheck, build (on frontend changes)
- `deploy.yml` — Build Docker images and deploy (on main push)

## Demo Users

| Email | Password | Role |
|-------|----------|------|
| admin@demo.com | Admin123! | SUPERADMIN |
| planeacion@demo.com | Planeacion123! | PLANEACION |
| alcalde@demo.com | Alcalde123! | ALCALDE |

## Documentation

- [Architecture](docs/01_ALCANCE_ARQUITECTURA_V1.md)
- [Data Dictionary](docs/02_ER_DICCIONARIO_DATOS_V1.md)
