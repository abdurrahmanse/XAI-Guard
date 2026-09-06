import os
import json
import yaml

os.makedirs('.vscode', exist_ok=True)

# 3.4 Pre-commit Config
pre_commit = {
    "repos": [
        {
            "repo": "https://github.com/Yelp/detect-secrets",
            "rev": "v1.4.0",
            "hooks": [{"id": "detect-secrets", "args": ["--baseline", ".secrets.baseline"]}]
        },
        {
            "repo": "https://github.com/astral-sh/ruff-pre-commit",
            "rev": "v0.4.4",
            "hooks": [
                {"id": "ruff", "args": ["--fix"]},
                {"id": "ruff-format"}
            ]
        },
        {
            "repo": "https://github.com/pre-commit/mirrors-prettier",
            "rev": "v3.1.0",
            "hooks": [{"id": "prettier", "types_or": ["typescript", "javascript", "css", "json", "markdown"]}]
        },
        {
            "repo": "https://github.com/alessandrojcm/commitlint-pre-commit-hook",
            "rev": "v9.16.0",
            "hooks": [{"id": "commitlint", "stages": ["commit-msg"], "additional_dependencies": ["@commitlint/config-conventional"]}]
        }
    ]
}

with open('.pre-commit-config.yaml', 'w') as f:
    yaml.dump(pre_commit, f, sort_keys=False)

commitlintrc = {
    "extends": ["@commitlint/config-conventional"],
    "rules": {
        "scope-enum": [2, "always", ["ml", "api", "web", "admin", "infra", "docs"]]
    }
}
with open('.commitlintrc.json', 'w') as f:
    json.dump(commitlintrc, f, indent=2)


# 3.5 VS Code Configuration
vscode_settings = {
    "python.defaultInterpreterPath": "${workspaceFolder}/services/api/.venv/bin/python",
    "editor.formatOnSave": True,
    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": "explicit",
        "source.organizeImports": "explicit"
    },
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.rulers": [88]
    },
    "[typescript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.rulers": [100]
    },
    "[typescriptreact]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "python.analysis.typeCheckingMode": "strict",
    "tailwindCSS.experimental.classRegex": [
        ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"]
    ]
}
with open('.vscode/settings.json', 'w') as f:
    json.dump(vscode_settings, f, indent=2)

vscode_extensions = {
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "charliermarsh.ruff",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "bradlc.vscode-tailwindcss",
        "ms-azuretools.vscode-docker",
        "eamodio.gitlens",
        "GitHub.copilot",
        "usernamehw.errorlens"
    ]
}
with open('.vscode/extensions.json', 'w') as f:
    json.dump(vscode_extensions, f, indent=2)


# 3.6 CONTRIBUTING.md
with open('CONTRIBUTING.md', 'w') as f:
    f.write("""# Contributing to XAI-Guard

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
""")

print("Successfully generated Phase 3: Developer Environment.")
