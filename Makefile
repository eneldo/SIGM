.PHONY: help setup dev test lint format check deploy migrate seed clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Full development setup
	@bash scripts/setup.sh

dev: ## Start development servers
	docker compose -f docker-compose.dev.yml up

dev-bg: ## Start development servers (background)
	docker compose -f docker-compose.dev.yml up -d

stop: ## Stop development servers
	docker compose -f docker-compose.dev.yml down

test: ## Run all tests
	cd backend && python -m pytest tests/ -v --tb=short

test-cov: ## Run tests with coverage
	cd backend && python -m pytest tests/ -v --tb=short --cov=app --cov-report=term-missing

lint: ## Run linting
	cd backend && ruff check .
	cd backend && ruff format --check .
	cd frontend && npm run lint

format: ## Format code
	cd backend && ruff check --fix .
	cd backend && ruff format .

check: ## Run all quality checks
	@bash scripts/check.sh

typecheck: ## Run type checking
	cd backend && mypy app --ignore-missing-imports
	cd frontend && npm run typecheck

migrate: ## Generate migration (usage: make migrate MSG="add table")
	cd backend && alembic revision --autogenerate -m "$(MSG)"

migrate-up: ## Apply pending migrations
	cd backend && alembic upgrade head

seed: ## Seed demo data
	@bash scripts/seed.sh

build: ## Build production images
	docker build -f Dockerfile.backend -t sigm-backend:latest .
	docker build -f frontend/Dockerfile -t sigm-frontend:latest ./frontend

deploy: ## Deploy (usage: make deploy ENV=staging)
	@bash scripts/deploy.sh $(ENV)

clean: ## Clean generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf frontend/.next frontend/node_modules
	rm -rf backend/.venv
