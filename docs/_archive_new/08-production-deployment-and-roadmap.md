# 08 — Admin Panel, MLOps & Production Deployment

> **Phases 57–63** | Admin Console (`apps/admin`), MLOps Pipeline, Observability, CI/CD, Deployment Architecture, and Research Paper Publication.

## 🗺️ Research Paper Map

| Phase | What You Build | Paper Section | Paper Artefact |
|-------|---------------|---------------|----------------|
| P57 | Admin Console & Registry UI | §6 System Architecture | "Models are managed via a dedicated Next.js Admin interface..." |
| P58 | Automated Retraining Pipeline | §6 Operational Fitness | Discussion of MLOps lifecycle |
| P59 | Observability (Prometheus) | §6 Operational Fitness | Production latency monitoring |
| P62 | Research Paper Finalization | All Sections | The complete `research-paper.pdf` |

---

## Phase 57 — Admin Console & Model Registry UI (`apps/admin`)

> **🎭 Role:** Internal Tools & MLOps Engineer
> **📍 Context:** The Admin Console is a highly privileged Next.js application used by Senior Data Scientists. It manages the Champion/Challenger model lifecycle and system metrics. It must be strictly isolated from the SOC Dashboard (`apps/dashboard`) and Marketing site (`apps/web`).
> **🔧 Task:** Scaffold `apps/admin/` as a Next.js 14 App Router project. Configure Tailwind CSS v4 and `next-themes`. Implement strict Role-Based Access Control (RBAC) middleware ensuring only `role === 'admin'` can access the app. Build the Model Registry view (`apps/admin/app/models/page.tsx`). Fetch models using TanStack Query from `GET /v1/registry`. Display a data table comparing F1, ROC-AUC, and p99 Latency. Implement a "Promote to Champion" modal that triggers `POST /v1/registry/promote`. Use Recharts to show historical F1 drift over time for the active Champion.
> **📦 Stack:** Next.js 14, Tailwind CSS v4, Zod, TanStack Query, Recharts, shadcn/ui
> **✅ Outcome:** `pnpm dev --filter=admin` runs on port 3002. Only admin JWTs can view the layout. Admins can view and promote models. Optimistic UI updates the table immediately upon successful promotion.

---

## Phase 58 — Automated ML Training Pipeline

> **🎭 Role:** Senior MLOps Engineer
> **📍 Context:** Models must be retrained on fresh data to combat drift. This pipeline orchestrates data extraction, preprocessing, and training in isolated background processes.
> **🔧 Task:** Implement `services/api/app/modules/training/tasks.py`. Create a Celery task `run_training_pipeline()` that triggers the DVC Python API to run `dvc repro`, trains a new XGBoost model, logs it to MLflow, and registers it as `CHALLENGER` in the SQL database. Add a manual trigger endpoint `POST /v1/training/trigger` that the Admin Console can call.
> **📦 Stack:** Celery, DVC API, MLflow, FastAPI
> **✅ Outcome:** Admins can click "Retrain Model" in the Admin UI, which kicks off an async Celery training job.

---

## Phase 59 — Observability & Security Hardening

> **🎭 Role:** DevSecOps Engineer
> **📍 Context:** A security product must itself be highly secure and monitored. We need Prometheus metrics for the API and rate limiting.
> **🔧 Task:** Add `prometheus-client` to `services/api`. Expose `GET /metrics` for Prometheus scraping. Track `xaiguard_predictions_total` and `xaiguard_inference_latency_seconds`. Implement `slowapi` rate limiting on the FastAPI instance (100 requests/minute per IP) to prevent DDoS on the ingestion endpoint.
> **📦 Stack:** prometheus-client, slowapi, Redis
> **✅ Outcome:** `/metrics` exposes application metrics. Hitting the API 101 times in a minute returns a 429 Too Many Requests.

---

## Phase 60 — CI/CD Pipeline (GitHub Actions)

> **🎭 Role:** DevOps Engineer
> **📍 Context:** Ensure code quality and test coverage before deployment. TurboRepo caching dramatically speeds up CI times.
> **🔧 Task:** Create `.github/workflows/ci.yml`. Define jobs: (1) `lint-and-typecheck`: runs `pnpm turbo run lint check-types`; (2) `test-api`: runs Pytest on `services/api` (Phases 48-53); (3) `test-web`: runs vitest on the frontend apps. Ensure `Vercel Remote Caching` or standard Turbo cache is enabled.
> **📦 Stack:** GitHub Actions, TurboRepo, Pytest, Vitest
> **✅ Outcome:** CI runs in under 3 minutes on every Pull Request.

---

## Phase 61 — Deployment Architecture (Docker & Vercel)

> **🎭 Role:** Cloud Solutions Architect
> **📍 Context:** The frontend apps (`web`, `dashboard`, `admin`) are best hosted on Vercel for Edge caching and ease of deployment. The backend (`api`, `celery`, `redis`, `postgres`) must be deployed as Docker containers.
> **🔧 Task:** 
> 1. Write `Dockerfile` for `services/api`. Use `uv` to install dependencies into a minimal distroless Python 3.11 image.
> 2. Write `docker-compose.prod.yml` orchestrating: FastAPI, Celery Worker, Redis, and PostgreSQL.
> 3. Add `vercel.json` to the frontend apps to configure the Vercel deployments, routing `/api/proxy/*` rewrites to the production Docker domain.
> **📦 Stack:** Docker, Docker Compose, Vercel
> **✅ Outcome:** The entire stack can be brought up in production mode with `docker-compose -f docker-compose.prod.yml up -d` and the frontends deployed to Vercel.

---

## Phase 62 — Research Paper Finalization

> **🎭 Role:** Principal Research Scientist
> **📍 Context:** The engineering is complete. Now the findings must be written into a publishable academic format.
> **🔧 Task:** Compile all generated notebooks, charts (SHAP, LIME, EMD), and architecture diagrams into a final `docs/research-paper.md`. Follow standard IEEE format: Abstract, Introduction, Related Work, Methodology, Experiments, Results, Discussion, Conclusion. Export to PDF using pandoc. Prepare `docs/supplementary-materials.md` detailing hyperparameters and reproducibility instructions (DVC + Git).
> **📦 Stack:** Markdown, Pandoc, LaTeX
> **✅ Outcome:** A complete, peer-review-ready PDF research paper.

---

## Phase 63 — Production Release & Project Completion

> **🎭 Role:** QA Lead & Release Manager
> **📍 Context:** The final sign-off before v1.0.0.
> **🔧 Task:** Write `tests/acceptance/test_production.py`. Replay 10,000 CICIDS-2017 events at 500 events/sec. Assert that alerts appear in the WebSocket stream and latency stays under 100ms. Create a `CHANGELOG.md` summarising the 63 phases. Tag the release `git tag -a v1.0.0 -m "XAI-Guard v1.0.0"`.
> **📦 Stack:** httpx, pytest, git
> **✅ Outcome:** The `v1.0.0` git tag is pushed. The project is officially complete.

---

## Complete 63-Phase Map

| # | Phase | Doc |
|---|-------|-----|
| 1–8 | Project Foundation | 01 |
| 9–17 | Data Engineering | 02 |
| 18–25 | Feature Engineering & Experiment Tracking | 03 |
| 26–32 | Classical ML & Sequence Models | 04 |
| 33–39 | Transformer & XAI Evaluation | 05 |
| 40–47 | LIME, XAI Evaluation & Backend Core | 06 |
| 48–56 | Backend Domain Modules & Frontends (Web/Dashboard) | 07 |
| 57–63 | Admin Console, MLOps & Production | 08 |

**Previous ←** [07 — Backend Domain Modules & Frontend Architecture](07-mlops-security-testing-and-performance.md)

---
*XAI-Guard: 63 phases · 350+ prompt-driven subphases · Research-grade ML · Production-grade Modular Monolith API · Enterprise-quality Next.js 14 Dashboard & Admin Panel.*
