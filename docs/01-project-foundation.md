# 01 — Project Foundation

> **Phases 1–8** | Research scoping, project charter, monorepo setup, infrastructure, database schema, modular monolith design, API contract strategy, and frontend architecture.
>
> **How to use:** Each subphase contains a structured prompt. Copy the full prompt block into your AI code editor (antigraveti). The prompt includes your role, architectural context, precise tasks, required packages, and the expected outcome.

---

## Phase 1 — Research Statement & Evaluation Framework

**Context:** Define the research question, six competing models, and the exact metrics that determine the winner before a single line of code is written.

#### Subphase 1.1 — Core Research Statement

> **🎭 Role:** Principal Research Scientist specialising in Applied ML for Cybersecurity
> **📍 Context:** You are initialising the XAI-Guard research project — an explainable multi-model cybersecurity threat detection platform. Nothing exists yet. This research statement is the intellectual foundation every subsequent phase references.
> **🔧 Task:** Write a formal, academically rigorous research statement for XAI-Guard. The central research question is: *Which AI model offers the best balance of accuracy, recall, false-positive control, explainability, inference latency, computational cost, and human usefulness for real-world cybersecurity threat detection?* The statement must define the six competing model families (Logistic Regression, Random Forest, XGBoost, LSTM, Transformer Encoder, Lightweight Transformer), the four benchmark datasets (NSL-KDD, CICIDS-2017, UNSW-NB15, BETH), and the three evaluation pillars (Prediction Performance, Explainability Quality, Operational Fitness). Structure it as: Motivation → Problem Statement → Research Objectives → Scope → Expected Contributions.
> **📦 Stack:** Markdown, draw.io or Mermaid for architecture diagrams
> **✅ Outcome:** A `docs/research-statement.md` file suitable as the opening section of a peer-reviewed paper. Any team member reading it understands exactly what is being built and why.

#### Subphase 1.2 — Eight Research Sub-Questions

> **🎭 Role:** Academic Research Lead with experience in IDS evaluation methodology
> **📍 Context:** The core research statement from Subphase 1.1 exists. You must now decompose it into eight formally stated, testable sub-questions that map directly to the evaluation framework.
> **🔧 Task:** Write eight research sub-questions, each with a formal null hypothesis (H₀) and alternative hypothesis (H₁). Cover: (RQ1) classical ML vs deep learning F1 delta; (RQ2) LSTM vs Transformer sequence detection advantage; (RQ3) whether large Transformer accuracy gain exceeds its GPU-hour cost; (RQ4) which XAI method produces the most analyst-actionable explanations; (RQ5) measurable trade-off between prediction accuracy and explanation quality; (RQ6) most cost-efficient model for CPU-only production deployment; (RQ7) per-attack-type F1 consistency across four datasets; (RQ8) robustness to temporal data drift. For each RQ, specify the metric used to evaluate it and the statistical test that will confirm or reject H₀.
> **📦 Stack:** Markdown
> **✅ Outcome:** A structured RQ document where every experimental result in Phase 37–38 maps back to a specific sub-question and its hypothesis.

#### Subphase 1.3 — Three-Pillar Evaluation Framework

> **🎭 Role:** Senior ML Platform Engineer and Evaluation Methodology Expert
> **📍 Context:** RQ1–RQ8 are defined. The evaluation framework is the scoring system that decides which model wins. It must be objective, reproducible, and defensible to peer reviewers.
> **🔧 Task:** Design the three-pillar evaluation framework. **Pillar 1 — Prediction Performance:** Accuracy, Precision Macro, Recall Macro, F1 Macro, F1 per attack class (DDoS, PortScan, BruteForce, Botnet, WebAttack, Infiltration, Normal), ROC-AUC Macro OvR, PR-AUC Macro. **Pillar 2 — Explainability Quality:** SHAP stability score (1 − CV across 10 runs), LIME-SHAP rank correlation, Attention-SHAP rank correlation, Analyst utility composite score (5 sub-metrics). **Pillar 3 — Operational Fitness:** Inference latency P50/P95/P99 in ms, throughput events/sec, peak RSS memory MB, training GPU-hours, model artifact size MB, composite deployment score formula. Define the weighted composite deployment score: `CDS = 0.40 × norm(F1) + 0.35 × norm(1/latency_p99) + 0.25 × norm(1/memory_mb)`. Document normalisation procedure.
> **📦 Stack:** Markdown, YAML for metric config
> **✅ Outcome:** A `docs/evaluation-framework.md` that any engineer can implement directly. Metrics are unambiguous, formulas are explicit, and the composite score is reproducible.

#### Subphase 1.4 — Dataset Selection & Attack Taxonomy

> **🎭 Role:** Cybersecurity Data Scientist with IDS benchmark expertise
> **📍 Context:** The evaluation framework exists. You must define which datasets feed it and how their heterogeneous label spaces map to a unified taxonomy.
> **🔧 Task:** Document the four dataset selections with full justification. For each: official download URL, SHA-256 checksum, license, record count, feature count, class distribution, and primary research challenge it addresses. Then define the XAI-Guard unified attack taxonomy enum: `DDOS | PORT_SCAN | BRUTE_FORCE | BOTNET | WEB_ATTACK | INFILTRATION | NORMAL`. Create a complete mapping table from each dataset's native label strings to this taxonomy. Flag any attack subtypes with fewer than 100 training samples as low-resource classes.
> **📦 Stack:** Markdown, YAML for taxonomy config
> **✅ Outcome:** `docs/dataset-strategy.md` and `ml/configs/taxonomy.yaml`. Any engineer can reproduce the label mapping deterministically.

#### Subphase 1.5 — Champion/Challenger Promotion Policy

> **🎭 Role:** MLOps Platform Architect with production model governance experience
> **📍 Context:** Models will be continuously trained and evaluated in production. A formal policy prevents ad-hoc promotions and ensures the system self-improves safely.
> **🔧 Task:** Write the Champion/Challenger model promotion policy. Define: (1) Shadow evaluation mode — Challenger runs on every live event in parallel without serving responses; (2) Nightly automated comparison window — 24h of shadow predictions evaluated against ground-truth; (3) Promotion thresholds — Challenger must exceed Champion by ΔF1 ≥ +0.020 AND ΔROC-AUC ≥ +0.010; (4) Latency budget gate — Challenger P99 latency must be ≤ 100ms on CPU; (5) Statistical significance gate — McNemar's test p < 0.05 with Bonferroni correction; (6) Auto-promotion trigger and the 4-step process; (7) Rollback procedure with history retention. Document as a state machine with states: TRAINING → REGISTERED → CHALLENGER → CHAMPION → ARCHIVED.
> **📦 Stack:** Markdown, Mermaid state diagram
> **✅ Outcome:** `docs/champion-challenger-policy.md` — the formal specification the model registry module implements in Phase 51.

#### Subphase 1.6 — Hyperparameter Search Space Specification

> **🎭 Role:** Senior ML Researcher with hyperparameter optimisation expertise
> **📍 Context:** All six models need Optuna or GridSearchCV studies. The search spaces must be defined upfront so experiments are comparable and reproducible.
> **🔧 Task:** Write the hyperparameter search space configuration for all six models as YAML files under `ml/configs/`. For each model document: optimiser class (Optuna TPE / GridSearchCV), number of trials or grid size, validation strategy (5-fold StratifiedKFold for tabular, epoch-based for deep learning), early stopping criterion, and each hyperparameter with type, range or choices, and scale (linear/log). Deep learning models additionally specify: warm-up schedule, gradient clipping value, batch sizes, and mixed-precision training flag.
> **📦 Stack:** YAML, Optuna 3.x, scikit-learn 1.4
> **✅ Outcome:** Six YAML config files, one per model family, that the training scripts load directly. Changing a search space requires editing only the YAML.

---

## Phase 2 — Project Charter & Scope

**Context:** Prevent scope creep across 63 phases by defining explicit boundaries, success criteria, and shared vocabulary before any code is written.

#### Subphase 2.1 — Project Charter

> **🎭 Role:** Technical Project Manager and Principal Engineer
> **📍 Context:** Research questions and evaluation framework are defined. The charter translates them into a governed project with stakeholders, timeline, and measurable success criteria.
> **🔧 Task:** Write the XAI-Guard project charter covering: (1) Executive summary — one paragraph; (2) Objectives — four primary, tied to the eight RQs; (3) In-scope deliverables — the 8-doc, 63-phase development plan, all six trained models, the modular monolith API, the analyst dashboard, the admin panel, and the research paper; (4) Explicit non-goals — no raw packet capture, no SIEM vendor lock-in, no classified data, no legally admissible forensics, no real-time training; (5) Success criteria — each one measurable and tied to Pillar 1/2/3 metrics; (6) Stakeholder map — roles and responsibilities; (7) Risk register with 5 risks, probability, impact, and mitigation; (8) Milestone timeline across 63 phases.
> **📦 Stack:** Markdown
> **✅ Outcome:** `docs/project-charter.md` — any new team member reads this before touching code.

#### Subphase 2.2 — Glossary & Domain Terminology

> **🎭 Role:** Technical Writer and Domain Architect
> **📍 Context:** Eight domain modules, six model families, three XAI methods, and two frontend applications will be built. Shared vocabulary prevents communication failures across the team.
> **🔧 Task:** Write the XAI-Guard project glossary defining every domain term used across all 63 phases. Include: Champion model, Challenger model, shadow evaluation, composite deployment score (CDS), MMD drift score, SHAP value, LIME explanation, Attention Rollout, modular monolith, sequence window, knowledge distillation, event deduplication hash, PR-AUC, shadow inference flag, Celery task ID, feature stability score, analyst utility metric, attack taxonomy enum, zero-shot generalisation gap, burn rate alerting, IRSA.
> **📦 Stack:** Markdown
> **✅ Outcome:** `docs/glossary.md` — linked from every other doc. Terms used in code comments reference this glossary for consistency.

#### Subphase 2.3 — Technical Constraints & ADR Log

> **🎭 Role:** Principal Architect documenting Architecture Decision Records
> **📍 Context:** Several non-negotiable technical constraints have been established. They must be documented as formal ADRs so future engineers understand why decisions were made and cannot easily reverse them.
> **🔧 Task:** Write five Architecture Decision Records (ADRs) in the MADR format for: (ADR-001) Modular Monolith over Microservices — single deployable FastAPI app with enforced module boundaries; (ADR-002) Common Model Interface — all six models implement identical predict/predict_proba/save/load interface; (ADR-003) Async-First API — all FastAPI endpoints and SQLAlchemy queries use async/await; (ADR-004) Explanation Async — XAI generation is always a Celery task, never blocking prediction response; (ADR-005) DVC + MLflow Dual Tracking — DVC for data versioning, MLflow for model and metric tracking. For each ADR: Context, Decision, Status, Consequences, Alternatives Considered.
> **📦 Stack:** Markdown (MADR format)
> **✅ Outcome:** `docs/decisions/` directory with five ADR files. Engineers consult ADRs before proposing architectural changes.

#### Subphase 2.4 — Phase Dependency Map

> **🎭 Role:** Engineering Programme Manager
> **📍 Context:** 63 phases exist across 8 docs. Some are strictly sequential (data before training), others can be parallelised (XAI phases across different models). The critical path determines the minimum calendar time to completion.
> **🔧 Task:** Create the phase dependency map as a Mermaid graph. Group phases into five dependency layers: (L1) Foundation P1–P8 — no dependencies; (L2) Data P9–P17 — requires L1 complete; (L3) Features & Tracking P18–P25 — requires L2; (L4) ML Research P26–P39 — requires L3; can be parallelised per model family; (L5) XAI + Backend + Frontend P40–P63 — requires L4 evaluation results. Identify the critical path from Phase 1 to Phase 63. Mark phases that can be parallelised. Estimate hours per phase.
> **📦 Stack:** Markdown, Mermaid flowchart
> **✅ Outcome:** A visual dependency graph in `docs/phase-dependency-map.md` that shows the critical path and parallelisation opportunities.

#### Subphase 2.5 — Definition of Done

> **🎭 Role:** Engineering Quality Lead
> **📍 Context:** Without explicit done criteria per phase category, phases never truly finish. Different categories of work have different completion signals.
> **🔧 Task:** Write the Definition of Done for each work category in XAI-Guard. (1) ML Experiment phase done: model registered in MLflow, all three-pillar metrics logged, analysis notebook committed, per-attack-type F1 table in the research findings doc; (2) API Module phase done: all endpoints implemented and tested, Pydantic schemas validated, OpenAPI spec updated, module tests pass with ≥80% coverage; (3) Frontend phase done: all Zustand stores updated, TanStack Query hooks implemented, Zod schemas match API schemas, component tests pass, E2E Playwright test covers the user workflow; (4) Infrastructure phase done: all resources defined in Terraform, Kubernetes manifests verified with `kubectl --dry-run`, health checks pass in local Docker Compose.
> **📦 Stack:** Markdown
> **✅ Outcome:** `docs/definition-of-done.md` — the quality gate referenced at the end of every phase.

---

## Phase 3 — Monorepo & Developer Environment

**Context:** Any developer clones the repo and is fully productive in under 10 minutes. Environment setup is automated, reproducible, and enforced by tooling.

#### Subphase 3.1 — Monorepo Workspace Configuration

> **🎭 Role:** Senior Platform Engineer and Monorepo Architect
> **📍 Context:** The XAI-Guard repository uses Turborepo + pnpm workspaces for the JS/TS layer and uv for the Python layer. The workspace covers three apps (web dashboard, admin panel, and the Next.js BFF) and three shared packages (ui component library, eslint-config, typescript-config).
> **🔧 Task:** Configure the complete Turborepo workspace. Set up `pnpm-workspace.yaml` declaring `apps/*`, `services/*`, and `packages/*`. Configure `turbo.json` with a pipeline where `lint` must complete before `build`, `build` before `test`, and the `dev` task runs all applications concurrently with correct `dependsOn`. Enable Turborepo remote caching via Vercel Remote Cache. Set the root `package.json` with the correct Node 20 engine constraint and pnpm 9 package manager field.
> **📦 Stack:** pnpm 9, Turborepo 2.x, Node 20 LTS
> **✅ Outcome:** `pnpm install && pnpm dev` starts all services. `pnpm build` completes without errors. Remote cache hit rate reaches >70% on repeat builds.

#### Subphase 3.2 — Python ML Environment

> **🎭 Role:** Senior ML Infrastructure Engineer
> **📍 Context:** The `ml/` module is a standalone Python project managed by uv. It must work identically on CPU-only developer machines and CUDA-enabled training servers. All versions are pinned for reproducibility.
> **🔧 Task:** Create `ml/pyproject.toml` with uv as the package manager. Pin these dependencies with exact versions: `torch==2.3.0`, `scikit-learn==1.5.0`, `xgboost==2.0.3`, `shap==0.45.0`, `lime==0.2.0.1`, `transformers==4.41.0`, `mlflow==2.14.0`, `optuna==3.6.1`, `alibi-detect==0.12.0`, `adversarial-robustness-toolbox==1.18.0`, `imbalanced-learn==0.12.3`, `dvc[s3]==3.51.0`, `pytest==8.2.0`, `pytest-asyncio==0.23.7`, `ruff==0.4.4`, `black==24.4.2`, `mypy==1.10.0`, `factory-boy==3.3.0`, `faker==25.2.0`, `coverage[toml]==7.5.3`. Configure optional `[cuda]` extras group for GPU dependencies. Configure tool sections for ruff, black, mypy, and pytest.
> **📦 Stack:** uv, Python 3.11
> **✅ Outcome:** `uv sync` completes in under 60 seconds. `uv run python -c "import torch, sklearn, xgboost, shap, mlflow; print('OK')"` succeeds.

#### Subphase 3.3 — Environment Variables & Secrets Management

> **🎭 Role:** Senior Security Engineer and Platform Architect
> **📍 Context:** Twelve services need configuration. Secrets must never be committed. The `.env.example` is the authoritative reference for onboarding.
> **🔧 Task:** Create `.env.example` with complete documentation for every environment variable grouped by service: DATABASE section (`DATABASE_URL`, `DATABASE_POOL_SIZE`, `DATABASE_MAX_OVERFLOW`); REDIS section (`REDIS_URL`, `REDIS_MAX_CONNECTIONS`); STORAGE section (`MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_BUCKET_NAME`); MLFLOW section (`MLFLOW_TRACKING_URI`, `MLFLOW_S3_ENDPOINT_URL`); SECURITY section (`SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`, `ALGORITHM`); THREAT_INTEL section (`ABUSEIPDB_API_KEY`, `VIRUSTOTAL_API_KEY`); OBSERVABILITY section (`SENTRY_DSN`, `OTEL_EXPORTER_OTLP_ENDPOINT`); APP section (`ENVIRONMENT`, `LOG_LEVEL`, `CORS_ORIGINS`, `ALLOWED_HOSTS`). Add a `scripts/validate-env.sh` that checks all required vars are set.
> **📦 Stack:** Bash, detect-secrets
> **✅ Outcome:** New developer copies `.env.example` to `.env`, fills in values, and every service starts. `detect-secrets scan` finds zero secrets in committed files.

#### Subphase 3.4 — Pre-commit Hooks & Code Quality

> **🎭 Role:** Engineering Quality Lead and DevEx Engineer
> **📍 Context:** Every commit must meet quality standards without manual enforcement. Pre-commit hooks run automatically and block commits that fail.
> **🔧 Task:** Configure `.pre-commit-config.yaml` with these hooks in order: `detect-secrets` (blocks accidental secret commits); `ruff` (Python linting and import sorting with `--fix`); `black` (Python formatting); `mypy` (Python type checking on changed files only); `eslint` (TypeScript linting); `prettier` (TypeScript, CSS, JSON, MD formatting); `commitlint` (enforces Conventional Commits: `feat|fix|docs|style|refactor|test|chore(scope): message`). Configure `.commitlintrc.json` with allowed scopes: `ml`, `api`, `web`, `admin`, `infra`, `docs`. Add `husky` for the Node side.
> **📦 Stack:** pre-commit, husky, lint-staged, commitlint, ruff, black, mypy, eslint, prettier
> **✅ Outcome:** `git commit -m "bad message"` is rejected. A commit with a badly formatted Python file is rejected. A commit with a secret-like string is rejected.

#### Subphase 3.5 — VS Code Workspace Configuration

> **🎭 Role:** Developer Experience Engineer
> **📍 Context:** All developers should have an identical, productive VS Code experience with zero configuration required after cloning.
> **🔧 Task:** Create `.vscode/settings.json` configuring: Python interpreter path pointing to the uv virtual environment, format-on-save with Black for Python and Prettier for TypeScript/CSS/MD, ESLint fix-on-save, Tailwind CSS IntelliSense, mypy as the Python type checker, `editor.rulers` at 88 (Python) and 100 (TypeScript). Create `.vscode/extensions.json` recommending: `ms-python.python`, `ms-python.vscode-pylance`, `charliermarsh.ruff`, `dbaeumer.vscode-eslint`, `esbenp.prettier-vscode`, `bradlc.vscode-tailwindcss`, `ms-azuretools.vscode-docker`, `eamodio.gitlens`, `GitHub.copilot`, `usernamehw.errorlens`.
> **📦 Stack:** VS Code
> **✅ Outcome:** A developer clones the repo, opens VS Code, installs recommended extensions, and has a fully configured environment with type checking, formatting, and linting without touching settings.

#### Subphase 3.6 — CONTRIBUTING Guide

> **🎭 Role:** Engineering Lead and Technical Writer
> **📍 Context:** The project spans ML research, a complex API, two frontend applications, and infrastructure. New contributors need a single guide that gets them productive without asking senior engineers.
> **🔧 Task:** Write `CONTRIBUTING.md` covering: prerequisites (Node 20, pnpm 9, Python 3.11, uv, Docker Desktop, Git); 10-step clone-to-running procedure; branch naming convention (`feature/`, `fix/`, `research/`, `chore/` + scope + kebab-case description); Conventional Commits format with examples for each scope; PR process (draft → ready → review → merge); how to run tests per layer (`pnpm test:web`, `pnpm test:admin`, `uv run pytest ml/`, `pnpm test:e2e`); how to start the full local stack with Docker Compose; how to access MLflow UI, Grafana, Jaeger; and the phase-by-phase development workflow.
> **📦 Stack:** Markdown
> **✅ Outcome:** A new engineer is productive within 30 minutes of reading this guide.

---

## Phase 4 — Infrastructure Services Setup

**Context:** Stand up all local development infrastructure as code so every developer has an identical environment that mirrors production.

#### Subphase 4.1 — Docker Compose Local Stack

> **🎭 Role:** Senior DevOps Engineer and Platform Architect
> **📍 Context:** The full XAI-Guard stack requires PostgreSQL, Redis, MinIO, and MLflow running locally. All services must be version-pinned, health-checked, and persistent across restarts.
> **🔧 Task:** Write `docker-compose.yml` defining: (1) `postgres` — image `postgres:16-alpine`, named volume `pg_data`, health check using `pg_isready`, env vars for user/password/database, port 5432; (2) `redis` — image `redis:7.2-alpine`, named volume `redis_data`, health check `redis-cli ping`, maxmemory policy `allkeys-lru`, port 6379; (3) `minio` — image `minio/minio:RELEASE.2024-05-01`, named volume `minio_data`, health check on `/minio/health/live`, ports 9000 and 9001; (4) `createbuckets` — one-shot MinIO client container that creates the required S3 bucket on startup; (5) `mlflow` — official MLflow image with `--backend-store-uri postgresql://...` and `--default-artifact-root s3://...`, depends on postgres and minio, port 5000. All services join a named `xaiguard` network.
> **📦 Stack:** Docker Compose v2, PostgreSQL 16, Redis 7.2, MinIO, MLflow 2
> **✅ Outcome:** `docker-compose up -d` starts all services. All health checks pass within 30 seconds. `docker-compose ps` shows all services as healthy.

#### Subphase 4.2 — Database Migrations Setup

> **🎭 Role:** Senior Backend Engineer with SQLAlchemy and Alembic expertise
> **📍 Context:** The PostgreSQL database schema will evolve across 63 phases. Alembic manages schema migrations so every environment runs the same version. The async SQLAlchemy engine is configured here.
> **🔧 Task:** Initialise Alembic in the FastAPI API service. Configure `alembic.ini` to read `DATABASE_URL` from the environment variable, not a hardcoded value. Set up `env.py` to use the SQLAlchemy async engine with `asyncpg` driver and import all ORM models so Alembic detects them for autogenerate. Create the initial empty migration. Write a `scripts/db-migrate.sh` that runs migrations safely in CI by checking the current revision before applying. Document the naming convention for migration messages: `{scope}_{description}` (e.g., `events_add_threat_intel_column`).
> **📦 Stack:** Alembic 1.13, SQLAlchemy 2.x async, asyncpg
> **✅ Outcome:** `alembic upgrade head` runs against the local database without errors. `alembic history` shows the migration chain.

#### Subphase 4.3 — Infrastructure Health Check Script

> **🎭 Role:** Platform Reliability Engineer
> **📍 Context:** New developers and CI pipelines need a single command that verifies all infrastructure services are ready before running tests or starting the API.
> **🔧 Task:** Write `scripts/check-infra.py` using `httpx` and `asyncpg` for async connectivity checks. The script tests: PostgreSQL connectivity with a SELECT 1 query; Redis connectivity with PING/PONG; MinIO bucket accessibility with a HEAD request; MLflow server reachability at the `/api/2.0/mlflow/experiments/list` endpoint. For each service it reports PASS in green or FAIL in red using the `rich` library. Exit with code 0 if all pass, code 1 if any fail. Include a `--wait` flag that retries for up to 60 seconds before failing.
> **📦 Stack:** httpx, asyncpg, redis-py, rich, typer
> **✅ Outcome:** `uv run python scripts/check-infra.py` returns all green after `docker-compose up -d`. CI runs this before any test suite.

#### Subphase 4.4 — Development Seed Data

> **🎭 Role:** Full-Stack Engineer responsible for development productivity
> **📍 Context:** Frontend development and API integration testing require realistic data without waiting for real ML training. The seed creates a complete working dataset covering every entity in the system.
> **🔧 Task:** Write `scripts/seed.py` using SQLAlchemy async sessions and the `faker` library. Seed: (1) 2 users — one analyst, one admin — with bcrypt-hashed passwords; (2) 500 security events across all attack types and datasets; (3) 1 XGBoost Champion model record with realistic F1=0.957 and latency=12ms; (4) 1 Transformer Challenger model record with F1=0.971 and latency=67ms; (5) 1000 predictions linked to events, mix of all severity levels; (6) 50 unacknowledged HIGH and CRITICAL alerts; (7) 5 SHAP explanation records for a sample of predictions; (8) 3 drift reports with scores below, at, and above the WARNING threshold. Use `factory-boy` factories for each entity.
> **📦 Stack:** SQLAlchemy 2 async, faker, factory-boy, asyncpg, passlib
> **✅ Outcome:** `uv run python scripts/seed.py` populates the database. All dashboard pages load with real-looking data. The admin panel shows a Champion/Challenger comparison.

---

## Phase 5 — Database Schema & ORM Layer

**Context:** Define the complete data model as SQLAlchemy 2 async ORM models with full type annotations. All eight backend modules use these shared models.

#### Subphase 5.1 — ORM Base Configuration

> **🎭 Role:** Senior Backend Engineer specialising in async Python and PostgreSQL
> **📍 Context:** The SQLAlchemy async engine and session factory live in the core layer. Every domain module gets database access through a shared FastAPI dependency, never by instantiating its own session.
> **🔧 Task:** Implement the ORM foundation in the API core layer. Create the SQLAlchemy 2 async engine using `create_async_engine` with `asyncpg` driver, configuring pool size (10), max overflow (20), pool timeout (30s), and `echo=False` for production. Create the `AsyncSessionLocal` factory using `async_sessionmaker`. Define the `Base` declarative base with a `TimestampMixin` providing `created_at` and `updated_at` with server-side defaults. Implement the `get_db` FastAPI dependency as an `async_generator` that yields a session and commits on success or rolls back on exception. Add a `PrimaryKeyMixin` providing a UUID primary key generated by PostgreSQL's `gen_random_uuid()`.
> **📦 Stack:** SQLAlchemy 2.x, asyncpg, pydantic-settings
> **✅ Outcome:** `from api.core.database import get_db` works in any module. The dependency correctly commits or rolls back. UUID primary keys are generated server-side.

#### Subphase 5.2 — Security Events ORM Model

> **🎭 Role:** Senior Backend Engineer with PostgreSQL and data modelling expertise
> **📍 Context:** Security events are the core data entity. They arrive in bulk, must be deduplicated, indexed for fast queries by source IP and timestamp, and enriched with threat intelligence asynchronously.
> **🔧 Task:** Define the `SecurityEvent` SQLAlchemy ORM model. Fields: `id` (UUID PK, server default), `dedup_hash` (SHA-256, unique, indexed), `source_ip` (INET type, indexed), `destination_ip` (INET type, indexed), `source_port` (Integer, 0–65535), `destination_port` (Integer, 0–65535), `protocol` (Enum: TCP/UDP/ICMP/OTHER), `timestamp` (TIMESTAMPTZ, indexed), `duration_ms` (Float), `bytes_sent` (BigInteger), `bytes_received` (BigInteger), `packet_count` (Integer), `tcp_flags` (JSONB), `service` (String 64), `features` (JSONB — full feature vector after preprocessing), `dataset_source` (Enum: NSL_KDD/CICIDS_2017/UNSW_NB15/BETH/LIVE), `threat_intel_data` (JSONB, nullable, populated async), `created_at` (TIMESTAMPTZ, server default). Add a composite index on `(source_ip, timestamp)` and a partial index on `threat_intel_data IS NULL` for the enrichment queue.
> **📦 Stack:** SQLAlchemy 2.x, PostgreSQL INET, JSONB, Enum types
> **✅ Outcome:** `alembic revision --autogenerate -m "events_initial"` generates the correct migration. The partial index exists in the database.

#### Subphase 5.3 — Model Registry ORM Models

> **🎭 Role:** MLOps Engineer with model lifecycle management expertise
> **📍 Context:** The model registry tracks every trained model version, its evaluation results, and its full promotion/rollback history. This data feeds both the admin panel and the automated Champion/Challenger evaluation logic.
> **🔧 Task:** Define three ORM models. `ModelVersion`: `id` (UUID PK), `mlflow_run_id` (String, unique, indexed), `mlflow_model_name` (String), `mlflow_model_version` (Integer), `framework` (Enum: SKLEARN/XGBOOST/PYTORCH), `model_family` (Enum: LR/RF/XGBOOST/LSTM/TRANSFORMER/LIGHTWEIGHT_TRANSFORMER), `hyperparameters` (JSONB), `metrics` (JSONB — all three-pillar metrics), `feature_list` (ARRAY of String), `dataset_version` (String — DVC tag), `git_sha` (String 40), `status` (Enum: TRAINING/REGISTERED/CHALLENGER/CHAMPION/ARCHIVED), `is_shadow_active` (Boolean), `promoted_at` (TIMESTAMPTZ nullable), `created_at`. `ModelEvaluation`: `id`, `champion_id` (FK → ModelVersion), `challenger_id` (FK → ModelVersion), `evaluation_window_hours` (Integer), `champion_metrics_snapshot` (JSONB), `challenger_metrics_snapshot` (JSONB), `f1_delta` (Float), `auc_delta` (Float), `latency_ok` (Boolean), `significance_p_value` (Float), `promotion_triggered` (Boolean), `evaluated_at`. `PromotionHistory`: `id`, `promoted_model_id` (FK), `demoted_model_id` (FK), `trigger` (Enum: MANUAL/AUTOMATIC/DRIFT_TRIGGERED), `reason` (Text), `performed_by` (String nullable), `promoted_at`.
> **📦 Stack:** SQLAlchemy 2.x, PostgreSQL ARRAY, JSONB, Enum
> **✅ Outcome:** Three tables with correct FK constraints and indexes. Autogenerated Alembic migration is clean.

#### Subphase 5.4 — Predictions & Explanations ORM Models

> **🎭 Role:** Senior Backend Engineer
> **📍 Context:** Predictions are generated synchronously and must be stored immediately. Explanations are generated asynchronously by Celery and reference the prediction. Both are queried heavily by the dashboard.
> **🔧 Task:** Define `Prediction` model: `id` (UUID PK), `event_id` (FK → SecurityEvent, indexed), `model_version_id` (FK → ModelVersion, indexed), `predicted_class` (Enum — attack taxonomy), `confidence_score` (Float, 0–1), `class_probabilities` (JSONB — dict of class→probability), `severity_level` (Enum: LOW/MEDIUM/HIGH/CRITICAL), `inference_latency_ms` (Float), `is_shadow` (Boolean, default False, indexed), `preprocessing_time_ms` (Float), `feature_extraction_time_ms` (Float), `created_at`. Define `XAIExplanation` model: `id` (UUID PK), `prediction_id` (FK → Prediction, indexed), `celery_task_id` (String, indexed), `method` (Enum: SHAP/LIME/ATTENTION), `status` (Enum: PENDING/COMPUTING/COMPLETE/FAILED), `feature_contributions` (JSONB — array of {name, value, direction, rank}), `base_value` (Float nullable), `stability_score` (Float nullable), `computation_time_ms` (Float nullable), `error_message` (Text nullable), `created_at`, `completed_at`.
> **📦 Stack:** SQLAlchemy 2.x
> **✅ Outcome:** FK constraints enforced. Index on `(event_id, is_shadow)` for shadow evaluation queries. Index on `(status, created_at)` for pending explanation polling.

#### Subphase 5.5 — Alerts & Drift ORM Models

> **🎭 Role:** Senior Backend Engineer
> **📍 Context:** Alerts are the primary analyst-facing entity. Drift reports are the primary MLOps safety mechanism. Both are generated continuously and must be queryable efficiently.
> **🔧 Task:** Define `Alert` model: `id` (UUID PK), `prediction_id` (FK → Prediction, unique — one alert per prediction), `severity` (Enum, indexed), `attack_type` (Enum, indexed), `source_ip` (INET, indexed), `destination_ip` (INET), `confidence_score` (Float), `dedup_key` (String — hash of source_ip + attack_type, indexed), `alert_count` (Integer default 1 — for deduplication grouping), `mitre_technique_id` (String), `mitre_technique_name` (String), `mitre_tactic_id` (String), `mitre_tactic_name` (String), `acknowledged` (Boolean default False, indexed), `acknowledged_by` (String nullable), `acknowledged_at` (TIMESTAMPTZ nullable), `created_at` (indexed). Define `DriftReport` model: `id`, `model_version_id` (FK → ModelVersion), `mmd_score` (Float), `drift_detected` (Boolean, indexed), `threshold_level` (Enum: NONE/WARNING/CRITICAL), `reference_stats` (JSONB), `current_window_stats` (JSONB), `features_drifted` (ARRAY of String), `retraining_triggered` (Boolean default False), `evaluated_at`.
> **📦 Stack:** SQLAlchemy 2.x, PostgreSQL INET
> **✅ Outcome:** Composite index on `(dedup_key, acknowledged, created_at)` for deduplication queries. Partial index on `(acknowledged=False, severity)` for the analyst dashboard unread count.

#### Subphase 5.6 — Users & Audit ORM Models

> **🎭 Role:** Security-Focused Backend Engineer
> **📍 Context:** User authentication and RBAC are owned by the auth module. An audit log tracks all security-sensitive actions for compliance.
> **🔧 Task:** Define `User` model: `id` (UUID PK), `username` (String, unique, indexed), `email` (String, unique, indexed), `hashed_password` (String), `role` (Enum: ANALYST/ADMIN), `is_active` (Boolean default True), `last_login_at` (TIMESTAMPTZ nullable), `created_at`. Define `AuditLog` model: `id` (UUID PK), `user_id` (FK → User nullable — for system events), `action` (Enum: LOGIN/LOGOUT/PROMOTE_MODEL/ROLLBACK_MODEL/ACKNOWLEDGE_ALERT/EXPORT_REPORT), `resource_type` (String), `resource_id` (UUID nullable), `ip_address` (INET), `user_agent` (String), `details` (JSONB), `created_at` (indexed). Add a DB-level constraint that `AuditLog.created_at` rows older than 90 days can be purged by a scheduled job.
> **📦 Stack:** SQLAlchemy 2.x
> **✅ Outcome:** All six ORM models exist and Alembic generates a clean migration covering all of them. `alembic upgrade head` creates all tables with correct constraints.

---

## Phase 6 — Modular Monolith Architecture Design

**Context:** Design the internal architecture of the single FastAPI application before any module is implemented. This is the most important design decision in the project.

#### Subphase 6.1 — Module Catalogue & Boundary Rules

> **🎭 Role:** Principal Backend Architect specialising in modular monolith design
> **📍 Context:** XAI-Guard is a single deployable FastAPI application internally structured into nine self-contained domain modules. The architecture delivers microservices-level organisation without distributed system complexity.
> **🔧 Task:** Write the complete module catalogue document. For each of the nine modules define: (1) ownership scope — what data it owns exclusively; (2) public service interface — the only functions other modules may call; (3) forbidden imports — what it must never import; (4) Celery tasks it owns; (5) Prometheus metrics it increments. Modules: `core` (shared infra, owns nothing), `auth` (users, JWT, audit), `events` (ingestion, deduplication), `predictions` (inference orchestration, Champion loading), `explanations` (SHAP/LIME/Attention Celery tasks), `models` (registry, Champion/Challenger lifecycle), `alerts` (alert creation, WebSocket broadcasting), `threat_intel` (AbuseIPDB, Tor, MITRE mapping), `drift` (MMD detection, drift reports). Include the forbidden cross-module import matrix as a table.
> **📦 Stack:** Markdown, Mermaid component diagram
> **✅ Outcome:** `docs/module-catalogue.md` — referenced by every developer before adding code to a module. Import violations are caught by `ruff` rules.

#### Subphase 6.2 — Application Factory & Module Registration

> **🎭 Role:** Senior FastAPI Architect
> **📍 Context:** A clean application factory pattern allows modules to be registered without modifying the main file. It also makes testing easier as modules can be registered selectively.
> **🔧 Task:** Implement the FastAPI application factory in `api/main.py`. The factory function `create_application()` accepts a `Settings` object and: (1) creates the FastAPI instance with `title`, `version`, `openapi_url` conditionally disabled in production; (2) registers all middleware in the correct order (CORS → HTTPS redirect → request ID → timing → Prometheus); (3) calls each module's `register_router(app)` function from a module registry list; (4) registers all FastAPI exception handlers from the core layer; (5) adds lifespan context manager that initialises the DB engine, Redis pool, loads the Champion model, warms the threat intel cache, and cleans up on shutdown. Route each module under `/v1/{module-prefix}/` with OpenAPI tags.
> **📦 Stack:** FastAPI 0.111, pydantic-settings, orjson
> **✅ Outcome:** `GET /v1/health` returns `{"status": "healthy", "version": "..."}`. All module routes appear in the OpenAPI docs at `/docs`. Adding a new module requires only one line in the module registry list.

#### Subphase 6.3 — Celery Application & Queue Architecture

> **🎭 Role:** Senior Backend Engineer with Celery distributed task expertise
> **📍 Context:** Three task categories require separate Celery queues with different priorities and worker configurations: real-time event processing, async explanation generation, and scheduled pipeline jobs.
> **🔧 Task:** Configure the XAI-Guard Celery application. Use Redis as the broker with `redis+ssl://` in production. Define three queues: `events` (high priority, 4 workers, auto-ack disabled for durability), `explanations` (medium priority, 2 workers, rate-limited to 10/min), `pipeline` (low priority, 1 worker, Beat-scheduled). Configure Celery Beat schedule for: nightly evaluation at 02:00 UTC daily, weekly retraining at 02:00 UTC Sundays, hourly threat intel cache warming, daily Tor exit node list refresh. Use `msgspec` for Celery task serialisation instead of JSON for 3–5× faster serialisation. Configure `flower` for task monitoring at port 5555.
> **📦 Stack:** Celery 5.x, redis-py, celery-beat, flower, msgspec
> **✅ Outcome:** `celery -A api.celery worker -Q events --concurrency 4` starts successfully. Flower dashboard shows all queues. Beat schedule fires correctly.

#### Subphase 6.4 — OpenAPI & Contract-First Strategy

> **🎭 Role:** API Platform Engineer and TypeScript SDK author
> **📍 Context:** The dashboard and admin panel are developed in parallel with the API. Without a contract-first strategy, frontend and backend drift and integration bugs appear late.
> **🔧 Task:** Implement the contract-first strategy. (1) FastAPI auto-generates OpenAPI 3.1 spec at `/openapi.json`; (2) Add a CI step `scripts/generate-types.sh` that runs `openapi-typescript` to generate a `packages/api-types/index.ts` file from the spec; (3) The dashboard and admin import all API types from this package — never define them locally; (4) Add a CI contract test that fetches the running API's OpenAPI spec and diffs it against the committed spec, failing if they diverge; (5) Configure FastAPI's `response_model_exclude_unset=True` globally to prevent null fields from bloating responses. Document the workflow: API schema changes always start with modifying the Pydantic response schema.
> **📦 Stack:** FastAPI, openapi-typescript, TypeScript
> **✅ Outcome:** `pnpm generate:types` regenerates all TypeScript types from the running API. The generated types are importable in both dashboard and admin apps.

#### Subphase 6.5 — Prometheus Metrics Registry

> **🎭 Role:** Site Reliability Engineer with Prometheus expertise
> **📍 Context:** All domain modules must emit metrics through a single shared registry. Metrics are the primary signal for operational health and SLO alerting.
> **🔧 Task:** Implement the shared Prometheus metrics registry in the core layer. Register these metrics: `xaiguard_predictions_total` (Counter, labels: model_family, attack_class, severity, is_shadow); `xaiguard_prediction_latency_seconds` (Histogram, labels: model_family, is_shadow, buckets: [0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5]); `xaiguard_confidence_score` (Histogram, labels: attack_class, severity); `xaiguard_drift_score` (Gauge, labels: model_family); `xaiguard_champion_info` (Info — current champion model family and version); `xaiguard_celery_queue_depth` (Gauge, labels: queue_name); `xaiguard_active_alerts_total` (Gauge, labels: severity); `xaiguard_explanation_latency_seconds` (Histogram, labels: method, model_family). Expose via `prometheus-fastapi-instrumentator` at `/metrics`.
> **📦 Stack:** prometheus-client, prometheus-fastapi-instrumentator
> **✅ Outcome:** `curl http://localhost:8000/metrics` returns all custom metrics. Grafana can scrape the endpoint and display live values.

#### Subphase 6.6 — Structured Logging & Request Tracing

> **🎭 Role:** Observability Engineer
> **📍 Context:** Every log line must carry a request ID, user ID, and trace ID so operators can correlate logs, metrics, and traces for any incident.
> **🔧 Task:** Configure structlog for the XAI-Guard API. Set up two render pipelines: JSON format for production (parsed by log aggregators), human-readable coloured format for development (detected via `ENVIRONMENT` env var). Standard fields on every log entry: `service=xaiguard-api`, `environment`, `request_id` (UUID generated per request), `user_id` (injected after authentication), `trace_id` (injected from OpenTelemetry), `level`, `timestamp` (ISO 8601 with timezone). Implement a FastAPI middleware using `contextvars` to inject `request_id` into the logging context for every request. Log request start (DEBUG), request complete (INFO with duration and status), and request error (ERROR with full traceback) automatically.
> **📦 Stack:** structlog, python-json-logger, contextvars
> **✅ Outcome:** Every log line in production is valid JSON with all standard fields. Searching logs by `request_id` returns all log lines for that request across all middleware and module handlers.

---

## Phase 7 — API Schema Strategy

**Context:** Lock all data contracts between API, ML pipeline, and both frontend applications. This enables parallel development across all layers without integration surprises.

#### Subphase 7.1 — Pydantic v2 Schema Conventions

> **🎭 Role:** Senior Backend Engineer and API Design Expert
> **📍 Context:** Pydantic v2 is 5–50× faster than v1 and uses a fundamentally different validation model. All schemas must be v2-native and follow consistent conventions.
> **🔧 Task:** Write the Pydantic v2 schema conventions for XAI-Guard that apply across all nine modules. Rules: (1) All input schemas use `model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)`; (2) All response schemas extend `BaseResponse(request_id: UUID, timestamp: datetime)`; (3) All enums are Python `StrEnum` subclasses for JSON serialisation compatibility; (4) Pagination uses cursor-based pattern: `CursorPage[T]` with `items: list[T]`, `next_cursor: str | None`, `total: int`; (5) Error responses follow RFC 7807: `ProblemDetail` with `type`, `title`, `status`, `detail`, `instance`, `extensions: dict`; (6) All monetary/cost fields include units in the name: `training_cost_gpu_hours`, `inference_latency_ms`; (7) IP address fields use Pydantic's `IPvAnyAddress` type. Implement these as base classes in `api/core/schemas.py`.
> **📦 Stack:** Pydantic v2, Python StrEnum
> **✅ Outcome:** All module schemas extend the correct base classes. `from api.core.schemas import BaseResponse, CursorPage, ProblemDetail` imports work in all modules.

#### Subphase 7.2 — Security Event & Prediction Schemas

> **🎭 Role:** Senior Backend Engineer
> **📍 Context:** The prediction workflow is the hot path. Schema validation must be fast (Pydantic v2 provides this), fields must be exactly what the ML pipeline needs, and the response must include everything the dashboard needs to display the Threat Detection card.
> **🔧 Task:** Define the core prediction workflow schemas. `SecurityEventInput`: IP address fields using `IPvAnyAddress`, port fields with `Annotated[int, Field(ge=0, le=65535)]`, protocol Enum, timestamp with timezone, all network features with domain-specific validators (packet count must be positive, byte counts must be non-negative). `PredictionResponse(BaseResponse)`: prediction ID, event ID, predicted attack class (StrEnum), confidence score `Annotated[float, Field(ge=0.0, le=1.0)]`, class probabilities dict, severity level (StrEnum), model version ID, model family, inference latency ms, explanation task ID (for polling), MITRE technique info, recommended actions list. `BatchPredictionRequest`: `events: Annotated[list[SecurityEventInput], Field(min_length=1, max_length=1000)]`, `async_mode: bool = False`.
> **📦 Stack:** Pydantic v2
> **✅ Outcome:** An invalid IP address in `SecurityEventInput` raises a 422 with a clear error message. The `PredictionResponse` OpenAPI schema is exactly what `openapi-typescript` generates correct TypeScript types from.

#### Subphase 7.3 — XAI Explanation Schemas

> **🎭 Role:** Senior Backend Engineer with XAI systems experience
> **📍 Context:** Three XAI methods (SHAP, LIME, Attention) produce structurally different outputs. The dashboard XAI panel must handle all three interchangeably. A discriminated union type achieves this.
> **🔧 Task:** Define XAI explanation schemas using Pydantic v2 discriminated unions. `FeatureContribution`: `feature_name: str`, `shap_value: float`, `direction: Literal["positive", "negative"]`, `rank: int`, `percentage: float`. `BaseExplanation(BaseResponse)`: `prediction_id: UUID`, `method: ExplanationMethod`, `status: ExplanationStatus`, `computation_time_ms: float | None`, `stability_score: float | None`. `SHAPExplanation(BaseExplanation)`: `method: Literal[ExplanationMethod.SHAP]`, `feature_contributions: list[FeatureContribution]`, `base_value: float`, `top_k_features: list[FeatureContribution]` (top 5). `LIMEExplanation(BaseExplanation)`: similar structure. `AttentionExplanation(BaseExplanation)`: `attention_weights: list[list[float]]`, `rollout_scores: list[float]`, `top_k_timesteps: list[int]`. `ExplanationUnion = Annotated[SHAPExplanation | LIMEExplanation | AttentionExplanation, Field(discriminator="method")]`.
> **📦 Stack:** Pydantic v2 discriminated unions
> **✅ Outcome:** `ExplanationUnion` correctly discriminates between the three types. TypeScript generated types include the discriminated union pattern. The dashboard XAI panel can switch methods without changing component logic.

#### Subphase 7.4 — Model Registry & Alert Schemas

> **🎭 Role:** Senior Backend Engineer
> **📍 Context:** The admin panel and the analyst dashboard both query these schemas heavily. They must be complete, include all display data, and match the WebSocket message format.
> **🔧 Task:** Define `ModelVersionResponse(BaseResponse)`: all model version fields plus `metrics: ThreePillarMetrics` (nested Pydantic model with all metrics from all three pillars). Define `ChampionChallengerStatus(BaseResponse)`: champion and challenger `ModelVersionResponse` objects, `performance_delta: dict[str, float]` (metric name → delta), `last_evaluated_at: datetime`, `auto_promote_eligible: bool`, `reasons: list[str]`. Define `AlertResponse(BaseResponse)`: all alert fields plus `prediction: PredictionResponse` (nested), `explanation_status: ExplanationStatus`, `mitre: MITREInfo` (nested model with technique ID, name, tactic, URL). Define `AlertWebSocketMessage`: `type: Literal["alert"]`, `payload: AlertResponse`, `server_timestamp: datetime` — this is the exact structure sent over WebSocket.
> **📦 Stack:** Pydantic v2
> **✅ Outcome:** The dashboard and admin TypeScript types correctly represent all nested relationships. The WebSocket message TypeScript type enables discriminated union handling.

#### Subphase 7.5 — Zod Mirror Schemas (Frontend)

> **🎭 Role:** Senior TypeScript/React Engineer
> **📍 Context:** TypeScript types generated from OpenAPI are structural but not validated at runtime. Zod schemas validate API responses at runtime and provide excellent error messages when the API changes unexpectedly.
> **🔧 Task:** In the `packages/api-types/` package, write Zod schemas that mirror all Pydantic schemas. For each core schema: `SecurityEventInputSchema`, `PredictionResponseSchema`, `SHAPExplanationSchema`, `LIMEExplanationSchema`, `AlertResponseSchema`, `ModelVersionResponseSchema`, `ChampionChallengerStatusSchema`, `AlertWebSocketMessageSchema`. Create a `validateApiResponse<T>(schema: ZodSchema<T>, data: unknown): T` utility that validates and throws a typed `ApiValidationError` on failure. This error is caught by the TanStack Query error boundary. Create a `zodFetcher` utility that wraps `fetch` with automatic Zod validation for all API calls.
> **📦 Stack:** Zod v3, TypeScript 5
> **✅ Outcome:** `zodFetcher("/v1/alerts", AlertResponseSchema.array())` validates the response at runtime. A breaking API change is caught immediately with a specific Zod error rather than a cryptic runtime crash.

#### Subphase 7.6 — API Versioning & Deprecation Strategy

> **🎭 Role:** API Platform Architect
> **📍 Context:** XAI-Guard v1 API must support evolution without breaking existing integrations. A documented deprecation strategy prevents surprise breaking changes.
> **🔧 Task:** Document and implement the XAI-Guard API versioning and deprecation strategy. (1) All routes are prefixed `/v1/`; (2) A new major version creates a `/v2/` prefix with the old version maintained for 6 months; (3) Deprecated endpoints return a `Deprecation: true` and `Sunset: {date}` header; (4) Implement a `@deprecated(sunset_date, alternative)` FastAPI route decorator that adds these headers automatically; (5) The OpenAPI spec marks deprecated operations with `deprecated: true`; (6) A weekly CI check runs against the deprecation registry and fails if a sunset date has passed without the route being removed.
> **📦 Stack:** FastAPI, Python decorators
> **✅ Outcome:** Deprecated endpoints return the correct headers. The OpenAPI docs show deprecated routes with a strikethrough. The CI deprecation check passes.

---

## Phase 8 — Frontend Application Architecture

**Context:** Design both Next.js applications before writing component code. Establish the state management architecture, data fetching strategy, and shared design system.

#### Subphase 8.1 — Frontend Tech Stack Declaration

> **🎭 Role:** Principal Frontend Architect
> **📍 Context:** Both the security dashboard and admin panel are Next.js 14 App Router applications. They share a component library but have completely different UX requirements. The tech stack must be declared once and used consistently.
> **🔧 Task:** Write the frontend tech stack declaration and justify each choice. The full stack includes: **Next.js 14** (App Router, Server Components, streaming); **TypeScript 5** (strict mode, `exactOptionalPropertyTypes`); **TanStack Query v5** (server state, cache, optimistic updates); **TanStack Table v8** (headless table with sorting/filtering/virtualisation); **TanStack Virtual v3** (list and grid virtualisation for the 50k+ alert feed); **Zustand v4** (client state — WebSocket connection state, UI preferences, selected entities); **Zod v3** (runtime API response validation); **React Hook Form v7** with `@hookform/resolvers` + Zod (all forms); **shadcn/ui** (component library built on Radix UI); **Tailwind CSS v3** (utility-first styling); **Framer Motion v11** (micro-animations); **Recharts v2** (data visualisation); **Lucide React** (icons); **next-themes** (dark/light mode); **nuqs** (URL state management for table filters); **class-variance-authority** (component variants); **tailwind-merge** + **clsx** (conditional classes); **date-fns v3** (date formatting); **cmdk** (command palette); **reconnecting-websocket** (auto-reconnect WebSocket); **@react-pdf/renderer** (PDF export).
> **📦 Stack:** All 20+ packages listed above
> **✅ Outcome:** `packages/ui/package.json` and each app's `package.json` declare all dependencies. `pnpm install` succeeds. A technology decision log entry exists for each choice.

#### Subphase 8.2 — Zustand Store Architecture

> **🎭 Role:** Senior React/State Management Engineer
> **📍 Context:** TanStack Query owns server state (remote data). Zustand owns client state (UI state that does not need to be fetched from the server). The boundary between them must be clear.
> **🔧 Task:** Design and implement the four Zustand stores for XAI-Guard. (1) `useWebSocketStore`: `status: "connecting" | "connected" | "disconnected" | "error"`, `lastError: string | null`, `reconnectAttempts: number`, `connect()`, `disconnect()`, `subscribe(handler)` — owns the WebSocket connection lifecycle; (2) `useAlertsStore`: `selectedAlertId: string | null`, `filters: AlertFilters`, `unreadCount: number`, `setSelectedAlert()`, `incrementUnread()`, `clearUnread()` — owns UI selection state and the unread badge; (3) `usePreferencesStore`: `alertSoundEnabled: boolean`, `compactMode: boolean`, `explanationMethod: "SHAP" | "LIME"` — persisted to localStorage via the `persist` middleware; (4) `useCommandStore`: `open: boolean`, `query: string`, `toggle()` — owns the command palette state. Each store uses the Zustand `immer` middleware for immutable updates.
> **📦 Stack:** Zustand v4, immer, zustand/middleware
> **✅ Outcome:** All four stores are importable. The `usePreferencesStore` correctly persists to and rehydrates from localStorage. The WebSocket store reconnects automatically using `reconnecting-websocket`.

#### Subphase 8.3 — TanStack Query Configuration

> **🎭 Role:** Senior React Engineer with TanStack Query expertise
> **📍 Context:** TanStack Query v5 is the single source of truth for all server state. Its configuration determines caching behaviour, background refetching, error handling, and optimistic updates across both applications.
> **🔧 Task:** Configure the global TanStack Query `QueryClient` for XAI-Guard. Set: `defaultOptions.queries.staleTime` to 30 seconds (data is considered fresh for 30s); `retry` to 3 with exponential backoff using `retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000)`; `refetchOnWindowFocus: true` for alert-related queries, `false` for model metrics; `networkMode: "offlineFirst"` so the UI shows cached data when offline. Implement `onError` global handler that sends errors to Sentry. Implement a custom `queryFn` default that wraps all queries with `zodFetcher` from Phase 7.5. Define all query keys as typed constants in `packages/api-types/query-keys.ts`.
> **📦 Stack:** @tanstack/react-query v5, Zod
> **✅ Outcome:** All API calls go through TanStack Query. Cached data appears instantly on navigation. A network failure shows the last cached value with a stale indicator.

#### Subphase 8.4 — shadcn/ui Design System Setup

> **🎭 Role:** Senior Frontend Engineer and Design Systems Architect
> **📍 Context:** Both applications share the same design system hosted in `packages/ui`. The palette must be appropriate for Security Operations Centre environments: dark-mode first, high contrast, clear severity colour coding.
> **🔧 Task:** Set up the shadcn/ui design system for XAI-Guard. Configure the dark-mode-first Tailwind CSS palette in `packages/ui/tailwind.config.ts`: background `zinc-950`, surface `zinc-900`, border `zinc-800`, text primary `zinc-50`. Define custom CSS variables for severity colours: `--severity-critical: 0 84% 60%` (red), `--severity-high: 25 95% 53%` (orange), `--severity-medium: 48 96% 53%` (yellow), `--severity-low: 217 91% 60%` (blue). Install these shadcn/ui components: Button, Card, Badge, Table, Dialog, Sheet, Popover, Command, Dropdown, Input, Label, Tabs, Tooltip, ScrollArea, Skeleton, Avatar, Alert, Progress. Extend each with CVA variants for the severity levels.
> **📦 Stack:** shadcn/ui, Radix UI, Tailwind CSS v3, CVA, tailwind-merge
> **✅ Outcome:** `import { Button, SeverityBadge } from "@xaiguard/ui"` works in both apps. The Storybook preview (optional) shows all component variants in dark mode.

#### Subphase 8.5 — Security Dashboard App Architecture

> **🎭 Role:** Principal Frontend Architect
> **📍 Context:** The security dashboard is used by analysts in high-stress SOC environments. UI must be fast, scannable, dark, and optimised for triage speed. The real-time alert feed is the primary feature.
> **🔧 Task:** Design the complete Next.js 14 App Router architecture for the XAI-Guard security dashboard. Define the route structure: `(auth)/login/page.tsx`, `(dashboard)/layout.tsx` (authenticated, persistent WebSocket connection), `(dashboard)/page.tsx` (live alert feed + model status bar), `(dashboard)/alerts/page.tsx` (full alert table with TanStack Table), `(dashboard)/alerts/[id]/page.tsx` (Threat Detection card + XAI panel), `(dashboard)/metrics/page.tsx` (MetricsDashboard), `(dashboard)/models/page.tsx` (Model Status). The layout uses React Server Components for the sidebar and navigation, and Client Components only where interactivity is needed. The WebSocket connection lives in a context provider wrapping the authenticated layout. Use `nuqs` for all table filters so analysts can share URLs.
> **📦 Stack:** Next.js 14 App Router, TanStack Query, Zustand, nuqs
> **✅ Outcome:** All routes render correctly. Server components fetch initial data. WebSocket connection is established once per session. Table filters are bookmarkable URLs.

#### Subphase 8.6 — Admin Panel App Architecture

> **🎭 Role:** Principal Frontend Architect
> **📍 Context:** The admin panel is used by data scientists and platform engineers for model management and research report export. It is a separate Next.js application with different access control requirements.
> **🔧 Task:** Design the complete Next.js 14 App Router architecture for the XAI-Guard admin panel. Route structure: `(auth)/login/page.tsx`, `(admin)/layout.tsx` (admin-role guard + authenticated), `(admin)/experiments/page.tsx` (ExperimentsTable with TanStack Table + TanStack Virtual for 10k+ runs), `(admin)/experiments/[runId]/page.tsx` (RunDetailDrawer), `(admin)/models/page.tsx` (ModelComparisonView), `(admin)/champion/page.tsx` (ChampionChallengerPanel + DriftMonitorPanel), `(admin)/reports/page.tsx` (ReportGenerator). Implement the admin-only Next.js middleware: reads JWT role from cookie, redirects analyst-role users to the dashboard. Use TanStack Table with server-side pagination for the experiments table. Use `nuqs` for all experiment filter state.
> **📦 Stack:** Next.js 14 App Router, TanStack Table v8, TanStack Virtual v3, nuqs, Zustand
> **✅ Outcome:** An analyst JWT token causes middleware to redirect from any admin route. The experiments table handles 10,000+ rows without performance degradation using virtual scrolling.

---

## Phase Map

| Phase | Title | Subphases |
|-------|-------|-----------|
| P1 | Research Statement & Evaluation Framework | 6 |
| P2 | Project Charter & Scope | 5 |
| P3 | Monorepo & Developer Environment | 6 |
| P4 | Infrastructure Services Setup | 4 |
| P5 | Database Schema & ORM Layer | 6 |
| P6 | Modular Monolith Architecture Design | 6 |
| P7 | API Schema Strategy | 6 |
| P8 | Frontend Application Architecture | 6 |

**Next →** [02 — Data Engineering](02-data-engineering.md)
