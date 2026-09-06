# Contributing to XAI-Guard

Welcome to XAI-Guard! This guide will get you from `git clone` to a fully running local environment in under 10 minutes.

## Prerequisites
Ensure your machine has the following installed:
- Node.js 20 LTS & pnpm 9+
- Python 3.11 & uv
- Docker Desktop
- Git

## 10-Step Setup
1. **Clone:** `git clone https://github.com/abdurrahmanse/XAI-Guard.git && cd XAI-Guard`
2. **Install JS dependencies:** `pnpm install`
3. **Install Python backend:** `cd services/api && uv sync`
4. **Install ML environment:** `cd ../../ml && uv sync`
5. **Start Infrastructure:** `cd ../infrastructure && docker-compose up -d`
6. **Wait for DB:** Wait 10 seconds for Postgres to become healthy.
7. **Run Migrations:** `cd ../services/api && uv run alembic upgrade head`
8. **Set Environment:** Copy `.env.example` to `.env` and fill it out.
9. **Start Turbo Dev:** `cd ../../ && pnpm dev`
10. **Verify:** Web UI is at `http://localhost:3000`, API at `http://localhost:8000`, MLflow at `http://localhost:5500`.

## Branching & Commit Conventions
We strictly enforce Conventional Commits. Commits failing this regex will be blocked by husky/pre-commit.
- **Format:** `type(scope): description`
- **Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
- **Scopes Allowed:** `ml`, `api`, `web`, `admin`, `infra`, `docs`.
- **Branch Naming:** `type/scope-kebab-case-description` (e.g., `feat/ml-transformer-hpo`).

## Pre-Commit Hooks
Run `pre-commit install` in the root. Every commit will automatically run:
1. `detect-secrets`
2. `ruff` (Auto-fixes Python linting)
3. `prettier` (Formats JS/TS)
4. `commitlint`

## Testing
- **Backend:** `cd services/api && uv run pytest`
- **ML:** `cd ml && uv run pytest`
- **Frontend:** `pnpm test:web`
