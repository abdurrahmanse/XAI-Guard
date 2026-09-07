# 08 — Admin Panel, MLOps & Production

> **Phases 56–63** | XAI Panel & Metrics Dashboard, Admin Panel, Champion/Challenger UI, automated ML pipeline, observability, CI/CD, Kubernetes, Terraform, production hardening, research paper, and v1.0.0 launch.
>
> **Prompt Engineering Format:** Each subphase includes Role, Context, Task, Stack, and Outcome.

---

## Phase 56 — XAI Panel & Metrics Dashboard Components

**Context:** Complete the analyst dashboard. The XAI panel gives analysts full explanation detail. The metrics dashboard provides model performance situational awareness for the duty analyst.

#### Subphase 56.1 — XAIPanel with SHAP Waterfall Chart

> **🎭 Role:** Senior React Engineer specialising in data visualisation
> **📍 Context:** The XAI panel opens from the ThreatDetailPanel's "XAI Details" button. It shows the full SHAP explanation as a Recharts horizontal bar chart, with the base value as a reference line — a visual representation of the SHAP waterfall plot.
> **🔧 Task:** Implement `apps/web/components/xai/XAIPanel.tsx`. Uses `useExplanation(taskId)` with polling. While status=processing: shadcn/ui `Skeleton` placeholder matching chart dimensions. When complete: Recharts `BarChart` (horizontal layout) with features on y-axis and SHAP values on x-axis. Positive bars `fill="#EF4444"`, negative bars `fill="#3B82F6"`. `ReferenceLine x={base_value}` with label "Base". Display prediction confidence and base value above chart. Display `computation_time_ms` and `stability_score` below. Include the SHAP/LIME toggle `Tabs` component from Subphase 56.2.
> **📦 Stack:** Recharts v2, @tanstack/react-query v5, shadcn/ui Skeleton + Tabs
> **✅ Outcome:** The waterfall chart renders for an XGBoost prediction. The base value reference line is at the correct x position. Chart animates on first render.

#### Subphase 56.2 — SHAP/LIME Method Toggle

> **🎭 Role:** Senior React Engineer
> **📍 Context:** Analysts may want to compare SHAP and LIME explanations for the same prediction. The toggle dispatches the LIME request and switches the chart without remounting the XAIPanel.
> **🔧 Task:** Extend `XAIPanel` with shadcn/ui `Tabs` with values `["shap", "lime"]`. On tab switch to LIME: check if LIME explanation already exists; if not, dispatch `POST /v1/explanations/request {method: "LIME"}`; start polling `useExplanation` for the LIME task ID; show `"Generating LIME explanation... {elapsed}s"` using a counting timer; switch chart to LIME data on complete. Display computation times side-by-side: `SHAP: {ms}ms | LIME: {ms}ms`. Persist selected method in `usePreferencesStore(state => state.explanationMethod)` (Zustand + `immer`, persisted to `localStorage` via `zustand/middleware/persist`).
> **📦 Stack:** shadcn/ui Tabs, @tanstack/react-query v5, Zustand v4 + immer + persist
> **✅ Outcome:** Switching to LIME dispatches the request and shows elapsed time. Returning to the panel later opens on the previously selected method.

#### Subphase 56.3 — MetricsDashboard Component

> **🎭 Role:** Senior React Data Visualisation Engineer
> **📍 Context:** The metrics dashboard gives the duty analyst a quick, always-current view of model performance. It auto-updates every 30 seconds without user interaction.
> **🔧 Task:** Implement `apps/web/components/metrics/MetricsDashboard.tsx` as a Client Component. Uses `useMetrics()` with `refetchInterval: 30_000`. Four panels: (1) F1 Macro + ROC-AUC as Recharts `RadialBarChart` gauges — green zone ≥ 90%, yellow 80–90%, red < 80%; (2) Precision + Recall as shadcn/ui `Card` blocks with large numeric value + delta-from-yesterday badge (green if positive, red if negative); (3) Alerts per hour (last 24h) as Recharts `AreaChart` with gradient fill; (4) Attack type distribution as Recharts `PieChart` with `RADIAN` label angles and custom legend. Framer Motion `motion.div` `initial={{ opacity: 0, y: 20 }}` `animate={{ opacity: 1, y: 0 }}` on each panel.
> **📦 Stack:** Recharts v2, Framer Motion v11, shadcn/ui Card, @tanstack/react-query v5
> **✅ Outcome:** All four chart panels render with real data. Polling updates charts without page refresh. Delta badges show correct direction.

#### Subphase 56.4 — ModelStatusBar Component

> **🎭 Role:** Senior Frontend Engineer
> **📍 Context:** The ModelStatusBar is always visible at the top of the dashboard layout, providing real-time system health at a glance so analysts are always aware of model state.
> **🔧 Task:** Implement `packages/ui/src/components/model-status-bar.tsx` as a Client Component. Uses `useModels()` with `refetchInterval: 60_000`. Renders a fixed horizontal bar: Champion name + version badge (green); Challenger name + version badge (blue) when active; drift status — small inline SVG gauge with three arcs (NONE=slate, WARNING=yellow, CRITICAL=red) and current MMD score as text; last evaluation time using `date-fns formatDistanceToNow`. Use Framer Motion `AnimatePresence` on the Champion name text so a model promotion smoothly crossfades to the new name. Export `ModelStatusBar.Skeleton` for the loading state.
> **📦 Stack:** Framer Motion v11 AnimatePresence, date-fns v3, @tanstack/react-query v5, packages/ui
> **✅ Outcome:** Status bar updates every 60 seconds. A model promotion animates the Champion name to the new model. The drift gauge renders with correct colour zone.

#### Subphase 56.5 — Dashboard E2E Tests

> **🎭 Role:** Senior Frontend Test Engineer
> **📍 Context:** End-to-end tests verify the complete analyst workflow from authentication through explanation display, catching integration regressions that unit tests miss.
> **🔧 Task:** Write Playwright E2E tests in `apps/web/tests/e2e/analyst-workflow.spec.ts`. Full workflow: (1) navigate to `/login`, enter analyst credentials, assert redirect to `/`; (2) assert `ModelStatusBar` shows Champion model name text; (3) mock WebSocket to send a CRITICAL DDoS alert, assert alert appears in AlertsFeed within 2 seconds; (4) click the alert, assert ThreatDetailPanel slides in with attack type "DDoS"; (5) click "XAI Details", assert XAIPanel loads with `data-testid="shap-chart"`; (6) click LIME tab, assert `"Generating LIME explanation"` text appears; (7) click Acknowledge, assert alert row has `data-acknowledged="true"`. Run against Docker Compose with seed data.
> **📦 Stack:** Playwright, @playwright/test
> **✅ Outcome:** All 7 E2E steps pass. Test suite runs in under 60 seconds.

---

## Phase 57 — Admin Panel Foundation & Experiment Browser

**Context:** The admin panel serves data scientists and platform engineers. Separate Next.js app, stricter access control (`role === "admin"` required), and heavy data tables for experiment management.

#### Subphase 57.1 — Admin App Setup & RBAC Middleware

> **🎭 Role:** Senior Full-Stack Engineer
> **📍 Context:** The admin panel is a separate Next.js 14 app in `apps/admin/`. It shares `packages/ui`, `packages/api-types`, and `packages/typescript-config` with the web app but has stricter RBAC requirements.
> **🔧 Task:** Set up `apps/admin/` as a Next.js 14 App Router application. `apps/admin/middleware.ts`: reads JWT from cookie, checks `exp` (unauthenticated → `/login`), checks `role === "admin"` (analyst → redirect to `/dashboard` with URL param `?error=insufficient_permissions`). Configure root layout with sidebar (5 sections: Experiments, Model Comparison, Champion/Challenger, Drift Monitor, Reports). Set up TanStack Query v5 `QueryClientProvider`, Zustand v4 store, and all shared packages identically to the web app. `next.config.ts` with `experimental.typedRoutes: true`.
> **📦 Stack:** Next.js 14 App Router + Middleware, @tanstack/react-query v5, Zustand v4, shadcn/ui
> **✅ Outcome:** `pnpm dev --filter=admin` starts on port 3001. An analyst JWT is rejected at middleware and redirected. All shared packages import without errors.

#### Subphase 57.2 — ExperimentsTable with TanStack Table

> **🎭 Role:** Senior React Engineer with TanStack expertise
> **📍 Context:** The experiments table may show thousands of MLflow runs. TanStack Table v8 with server-side pagination and TanStack Virtual enables this at any scale without UI degradation.
> **🔧 Task:** Implement `apps/admin/components/experiments/ExperimentsTable.tsx`. Use `@tanstack/react-table` with `getCoreRowModel`, `getSortedRowModel`, `getFilteredRowModel`. Server-side sort + filter: pass sort column and direction as query params to `GET /v1/experiments`. Columns: model family (filterable, cmdk ComboBox multi-select), dataset, F1 macro (sortable), ROC-AUC (sortable), latency P99 ms (sortable), training time, status badge (`SeverityBadge` repurposed), created date. Filter state synced to URL via `nuqs useQueryStates`. `@tanstack/react-virtual` for virtualised rows. Row click opens `RunDetailDrawer`.
> **📦 Stack:** @tanstack/react-table v8, @tanstack/react-virtual v3, nuqs, cmdk, shadcn/ui
> **✅ Outcome:** Table handles 10,000 rows without frame drops. Sort/filter state survives browser refresh via URL.

#### Subphase 57.3 — RunDetailDrawer & Register as Challenger

> **🎭 Role:** Senior React Engineer
> **📍 Context:** The run detail drawer gives data scientists the full context of an MLflow experiment run and allows promoting it to Challenger with a single action, directly from the experiment browser.
> **🔧 Task:** Implement `apps/admin/components/experiments/RunDetailDrawer.tsx` as a shadcn/ui `Sheet` sliding from the right (width=`w-[600px]`). Displays: MLflow parameters as a 2-column sortable key-value table; all metrics as Recharts `LineChart` sparklines (no axes, just the trend line); DVC data version tag; git SHA (7 chars with shadcn/ui `Button` copy icon). **Register as Challenger** `Button` with variant `"default"`: `useMutation` on `POST /v1/models/register { mlflow_run_id }`, shows `Loader2` spinner during mutation, on success shows shadcn/ui `toast({ title: "Registered as Challenger" })` and invalidates the `["models"]` query cache.
> **📦 Stack:** shadcn/ui Sheet + toast, Recharts v2, @tanstack/react-query v5 useMutation
> **✅ Outcome:** Drawer opens within 200ms. Register as Challenger shows loading state and success toast. Query cache is invalidated so the Challenger panel updates immediately.

---

## Phase 58 — Champion/Challenger Management UI

**Context:** The operational control centre for platform engineers: model comparison, promotion controls, drift monitoring, and research report export.

#### Subphase 58.1 — ModelComparisonView with Conditional Formatting

> **🎭 Role:** Senior React Engineer
> **📍 Context:** The master comparison table is the central deliverable of the ML research. The admin panel renders it from the API with conditional formatting that makes champions, challengers, and best/worst values immediately visible.
> **🔧 Task:** Implement `apps/admin/components/models/ModelComparisonView.tsx`. Fetches `GET /v1/models`. Renders a shadcn/ui `Table` with all 6 model families as rows and all metrics as columns. Row highlights: Champion row — `bg-green-950/50 border-l-2 border-green-500`; Challenger row — `bg-blue-950/50 border-l-2 border-blue-500`. Column value highlights: best value in column — `font-bold text-emerald-400`; worst value — `text-red-400`. Sort by CDS descending by default. **Download CSV** button: builds CSV string from table data, creates `URL.createObjectURL(new Blob([csv], { type: "text/csv" }))`, triggers `<a download>` click. **Generate PDF** button opens `ReportGenerator`.
> **📦 Stack:** shadcn/ui Table + Button, @tanstack/react-query v5, TypeScript
> **✅ Outcome:** Champion and Challenger rows are visually distinct. Best metric values are bold green. CSV download works and produces a correctly formatted file.

#### Subphase 58.2 — ChampionChallengerPanel with Promotion Actions

> **🎭 Role:** Senior React Engineer
> **📍 Context:** Platform engineers use this panel for the most consequential action in the system: promoting a Challenger to Champion. The UI must require explicit confirmation and a written justification to prevent accidental promotions.
> **🔧 Task:** Implement `apps/admin/components/models/ChampionChallengerPanel.tsx`. Side-by-side cards: Champion (green border) and Challenger (blue border) with key metrics and delta badges (↑/↓ with color). **Promote to Champion** button: only renders if `userRole === "admin"` (from Zustand JWT decode store). Opens shadcn/ui `AlertDialog` with: a delta metrics table, a `Textarea` for `promotion_reason` (Zod: `z.string().min(10, "Reason must be at least 10 characters")`), Confirm `Button` disabled until reason is valid (React Hook Form v7 + Zod resolver). On confirm: `useMutation` on `POST /v1/models/promote`. **Rollback** button: same pattern, confirm input must type the word "rollback" exactly.
> **📦 Stack:** shadcn/ui AlertDialog + Textarea, React Hook Form v7, Zod v3, @tanstack/react-query v5 useMutation, Zustand v4
> **✅ Outcome:** Analyst role never renders Promote/Rollback buttons. Promotion requires a ≥10-char reason. Rollback requires typing "rollback". The confirm button is disabled until validation passes.

#### Subphase 58.3 — DriftMonitorPanel

> **🎭 Role:** Senior React Data Visualisation Engineer
> **📍 Context:** The drift monitor shows 30 days of MMD scores alongside discrete drift events. Platform engineers use it to understand the model health trend and decide if manual retraining is needed.
> **🔧 Task:** Implement `apps/admin/components/models/DriftMonitorPanel.tsx`. Fetches `GET /v1/drift/reports?days=30`. Renders: (1) Recharts `LineChart` with `mmd_score` on y-axis, date on x-axis; two `ReferenceLine` elements: `y={0.05}` yellow "WARNING", `y={0.10}` red "CRITICAL"; custom `Tooltip` showing score + threshold level + action triggered; (2) current drift status as large `SeverityBadge`; (3) TanStack Table of last 10 reports with columns: date (formatted), MMD score (2 decimal places), threshold level (`SeverityBadge`), features drifted (comma-separated chip list), action triggered (string). Default sort: date descending.
> **📦 Stack:** Recharts v2, @tanstack/react-table v8, shadcn/ui, @tanstack/react-query v5
> **✅ Outcome:** WARNING and CRITICAL reference lines render at correct y positions. Table sorts by date descending. Threshold level column uses SeverityBadge.

#### Subphase 58.4 — ReportGenerator with @react-pdf/renderer

> **🎭 Role:** Senior React Engineer
> **📍 Context:** Platform engineers and research leads export comparison data as a structured PDF report for stakeholder communication and research paper supplementary materials.
> **🔧 Task:** Implement `apps/admin/components/reports/ReportGenerator.tsx`. Two export actions: (1) CSV — client-side, immediate download using `URL.createObjectURL`; (2) PDF — uses `@react-pdf/renderer`. Define `<XAIGuardReport>` as a `@react-pdf/renderer` `Document` with: a cover `Page` (XAI-Guard title, report date, system version); a comparison `Page` with a `@react-pdf/renderer` `View`-based table (6 rows × 12 columns); a findings summary `Page`. Generate using `pdf(<XAIGuardReport data={metrics} />).toBlob()`. Run in a Web Worker via `new Worker(new URL("./report.worker.ts", import.meta.url))` to avoid UI blocking. Show `Progress` bar during generation.
> **📦 Stack:** @react-pdf/renderer, shadcn/ui Progress + Button
> **✅ Outcome:** PDF generation completes in under 10 seconds without freezing the UI. Downloaded PDF contains all 6 model rows with correct metric values.

---

## Phase 59 — Automated ML Training Pipeline

**Context:** Automate the complete ML lifecycle: weekly scheduled retraining and drift-triggered retraining keep XAI-Guard current without manual intervention.

#### Subphase 59.1 — Pipeline Orchestration Script

> **🎭 Role:** MLOps Platform Engineer
> **📍 Context:** The orchestration script is the single entry point for all ML pipeline execution. It must be idempotent (safe to run multiple times), resumable from any failed stage, and produce consistent MLflow tracking.
> **🔧 Task:** Implement `ml/scripts/run_pipeline.py` using `typer`. CLI: `run_pipeline [--models FAMILY] [--skip-to STAGE] [--dry-run] [--run-id UUID]`. Stages in order: `download`, `validate`, `clean`, `encode`, `features`, `select`, `split`, `train_{model}`, `evaluate`, `register`. On each stage: write stage+status+timestamp to `/tmp/pipeline_progress_{run_id}.json`. On resume (`--run-id`): read progress file, skip stages with status `"complete"`. Each stage calls its script via `subprocess.run(["uv", "run", "python", ...], check=True)`. Log stage durations to MLflow. Exit code 0 on success, 1 on any stage failure.
> **📦 Stack:** typer, subprocess (stdlib), mlflow 2.14, structlog, rich
> **✅ Outcome:** `uv run python ml/scripts/run_pipeline.py --models xgboost --dry-run` logs all stages without executing. Resuming from a failed `train_xgboost` stage skips `download` through `split`.

#### Subphase 59.2 — GitHub Actions Cron & Drift-Triggered Retraining

> **🎭 Role:** DevOps Engineer and MLOps Specialist
> **📍 Context:** Two automation paths trigger ML training: weekly scheduled cron (preventive maintenance) and drift-triggered retraining (reactive response to distribution shift).
> **🔧 Task:** Write `.github/workflows/ml-pipeline-weekly.yml`. Trigger: `schedule: [{cron: "0 2 * * 0"}]`. Steps: `actions/checkout`; `astral-sh/setup-uv`; configure DVC remote with AWS secrets (`DVC_ACCESS_KEY_ID`, `DVC_SECRET_ACCESS_KEY`); `uv run dvc pull`; `uv run python ml/scripts/run_pipeline.py --models all`; send Slack webhook with F1 metrics; on failure, create GitHub Issue via `actions/github-script`. Implement `services/api/models/tasks.py` `retrain_on_drift` Celery task: subscribes to `xaiguard:retraining` Redis channel, on `drift:critical:*` message calls `subprocess.Popen(["uv", "run", "python", "ml/scripts/run_pipeline.py", "--models", model_family])` with stdout/stderr streamed to structlog.
> **📦 Stack:** GitHub Actions, Celery 5.x, subprocess, structlog
> **✅ Outcome:** The weekly workflow appears in GitHub Actions with the correct cron schedule. The drift-triggered task only retrains the Champion model family.

#### Subphase 59.3 — Pipeline Health Gate

> **🎭 Role:** MLOps Quality Engineer
> **📍 Context:** A health gate prevents degraded models from entering the registry. Any training run that produces a significant F1 regression is blocked automatically, preventing silent performance degradation.
> **🔧 Task:** Implement `ml/src/pipeline/health_gate.py`. `PipelineHealthGate(f1_regression_threshold: float = 0.05, p99_latency_budget_ms: float = 100.0)`. `check(new_metrics: ThreePillarMetrics, previous_run_id: str) -> HealthGateResult`: fetch previous F1 from MLflow using `mlflow.get_run(previous_run_id).data.metrics["f1_macro"]`; compute delta; if `delta < -threshold`: `HealthGateResult(passed=False, reason=f"F1 regression: {delta:.3f}", block_registration=True)`; if `new_metrics.latency_p99_ms > p99_latency_budget_ms`: `HealthGateResult(passed=False, reason=f"P99 latency {new_metrics.latency_p99_ms:.0f}ms exceeds {p99_latency_budget_ms:.0f}ms budget", block_registration=True)`; else `HealthGateResult(passed=True)`. On block: send Slack webhook alert. The orchestration script calls this gate after `evaluate` and before `register`.
> **📦 Stack:** mlflow 2.14, httpx, pydantic v2, structlog
> **✅ Outcome:** Simulated F1 drop of 0.06 triggers `block_registration=True` and fires the Slack alert. The `register` stage is skipped. A P99 regression of 120ms also triggers the gate.

---

## Phase 60 — Observability, Security Hardening & Testing

**Context:** Three quality pillars that make XAI-Guard production-safe: pre-configured Grafana dashboards, OpenTelemetry traces, and enforced security gates.

#### Subphase 60.1 — Grafana Dashboard Configuration

> **🎭 Role:** Site Reliability Engineer with Grafana expertise
> **📍 Context:** Grafana dashboards are provisioned from JSON files committed to the repository. No manual dashboard creation is required after deployment — infrastructure as code applies to observability too.
> **🔧 Task:** Write Grafana provisioning in `infra/grafana/`. `provisioning/datasources/prometheus.yml` and `provisioning/datasources/postgres.yml`. `provisioning/dashboards/main.yml` with `path: /etc/grafana/dashboards`. Dashboard JSON in `dashboards/operational.json`: panels for requests/sec (rate PromQL), prediction P99 latency (histogram_quantile PromQL), confidence score distribution (heatmap), Celery queue depth, active WebSocket connections. Dashboard JSON in `dashboards/model-performance.json`: panels querying `model_evaluations` PostgreSQL table for F1 trend over time, promotion history timeline. Configure `docker-compose.yml` to mount both directories.
> **📦 Stack:** Grafana 10, Prometheus 2.x, PostgreSQL datasource
> **✅ Outcome:** `docker compose up grafana` shows both dashboards pre-populated from seed data without any manual configuration.

#### Subphase 60.2 — OpenTelemetry Instrumentation & Grafana Alerting

> **🎭 Role:** Observability Platform Engineer
> **📍 Context:** Distributed traces show the full latency breakdown of individual requests across FastAPI, SQLAlchemy, Redis, and Celery — enabling precise identification of bottlenecks.
> **🔧 Task:** Configure OpenTelemetry in `services/api/core/telemetry.py`. Set up `TracerProvider` with `OTLPSpanExporter(endpoint="http://jaeger:4317")`. Instrument: `FastAPIInstrumentor().instrument_app(app)`, `SQLAlchemyInstrumentor().instrument(engine=engine)`, `RedisInstrumentor().instrument()`, `CeleryInstrumentor().instrument()`. Add `X-Trace-ID` response header from `trace.get_current_span().get_span_context().trace_id`. Write Grafana alert rules in `infra/grafana/alerts/rules.json`: alert if `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 0.2` for 5 min (P99 > 200ms); alert if `mmd_score > 0.10` (CRITICAL drift); alert if `rate(http_requests_total{status=~"5.."}[5m]) > 0.01` (error rate > 1%).
> **📦 Stack:** opentelemetry-sdk, opentelemetry-instrumentation-fastapi, opentelemetry-instrumentation-sqlalchemy, opentelemetry-instrumentation-redis, opentelemetry-instrumentation-celery, Jaeger
> **✅ Outcome:** A prediction request shows a distributed trace in Jaeger with spans for FastAPI, SQLAlchemy, and Redis. All three Grafana alerts fire in a controlled test injection.

#### Subphase 60.3 — Security Hardening & Coverage Enforcement

> **🎭 Role:** Application Security Engineer and QA Lead
> **📍 Context:** Security hardening and test coverage gates are enforced together in CI so neither can slip through a PR review. Both requirements must pass for the merge to proceed.
> **🔧 Task:** Security: run `bandit -r services/api/ ml/ -ll -x tests/` and fix all HIGH/MEDIUM findings; run `detect-secrets scan --update .secrets.baseline`; add `SECURITY.md` with responsible disclosure policy; configure `slowapi` rate limits in `services/api/core/middleware.py`: `/v1/predictions/predict` 100/min, `/v1/explanations/request` 10/min, `/v1/events/ingest` 50/min. Coverage: configure `pyproject.toml` `[tool.coverage.run] branch = true` + `[tool.coverage.report] fail_under = 80`. Write `scripts/security-check.sh` that runs Bandit and detect-secrets and exits 1 if any HIGH issues found.
> **📦 Stack:** bandit, detect-secrets, slowapi, coverage[toml]
> **✅ Outcome:** `bash scripts/security-check.sh` exits 0. `coverage report` shows ≥80% for all API modules. Rate limit returns 429 with `Retry-After` header after threshold.

#### Subphase 60.4 — Load Testing Baseline

> **🎭 Role:** Performance Engineer
> **📍 Context:** The load test baseline establishes the performance contract. All future optimisations must maintain or improve these numbers, verified by re-running the load test in staging.
> **🔧 Task:** Write `tests/load/locustfile.py`. Three `HttpUser` task classes: `EventIngestionUser(weight=10)` — `POST /v1/events/ingest` with 100-event batches; `PredictionUser(weight=70)` — `POST /v1/predictions/predict` with single events; `AlertPollingUser(weight=20)` — `GET /v1/alerts?severity=CRITICAL`. Target: ramp to 500 concurrent users over 5 minutes, sustain 10 minutes. Implement `--check-targets` custom argument: if set, the `test_stop` hook asserts `p99_predict < 150ms` and `failure_rate < 0.5%`, exiting 1 on failure. Document results in `docs/performance-baseline.md` after first run.
> **📦 Stack:** locust 2.x
> **✅ Outcome:** The baseline is documented. `--check-targets` enforces the latency SLO in staging CI.

---

## Phase 61 — CI/CD Pipeline

**Context:** Automated quality gates from every pull request to production deployment. Fast feedback, parallel jobs, and enforced manual approval for production.

#### Subphase 61.1 — CI Workflow

> **🎭 Role:** Senior DevOps Engineer and CI/CD Specialist
> **📍 Context:** Every pull request must pass all quality gates before merging. Parallel jobs (quality, test-api, test-ml, test-e2e, security) minimise total CI duration while maintaining comprehensive coverage.
> **🔧 Task:** Write `.github/workflows/ci.yml`. Trigger: `on: pull_request: branches: [main]`. Parallel jobs (using `needs` only where sequential): (1) `quality` — `pnpm lint`, `pnpm typecheck`, `uv run ruff check ml/ services/`, `uv run mypy services/api/ ml/`, `uv run bandit -r services/ ml/ -ll -x tests/`, commitlint; (2) `test-api` — Docker Compose up (postgres, redis), `uv run pytest services/api/ --cov=services/api --cov-fail-under=80 --cov-report=xml`, upload to Codecov; (3) `test-ml` — run ML pipeline integration tests on 100-row fixture data; (4) `test-e2e` — build images, `docker compose up --wait`, `pnpm exec playwright test`; (5) `security` — Trivy scan Docker images built in `test-e2e`, `trivy image --exit-code 1 --severity CRITICAL`.
> **📦 Stack:** GitHub Actions, Docker Compose, pytest-asyncio, Playwright, trivy
> **✅ Outcome:** All 5 CI jobs appear in GitHub's PR check list. Failed coverage gate blocks the merge. Trivy blocks on CRITICAL CVEs.

#### Subphase 61.2 — Multi-Stage Docker Builds & CD Workflows

> **🎭 Role:** Senior DevOps Engineer
> **📍 Context:** Multi-stage builds minimise image sizes and attack surface. Staging deployments are automatic; production requires a named reviewer's approval in a GitHub Environment.
> **🔧 Task:** Write multi-stage Dockerfiles. `services/api/Dockerfile`: stage 1 `python:3.11-slim` + uv install deps; stage 2 `python:3.11-slim` runtime, copy venv and source only, `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`. `apps/web/Dockerfile`: stage 1 node build with `pnpm build`; stage 2 Node 20 slim with Next.js `standalone` output only. Target sizes: API < 500MB, web/admin < 200MB. `.github/workflows/cd-staging.yml`: trigger `push: branches: [main]`; build+push to ECR with git SHA tag; `kubectl apply -k infra/kubernetes/overlays/staging/`; wait for rollout with `kubectl rollout status`; run smoke tests. `.github/workflows/cd-production.yml`: trigger `workflow_dispatch: inputs: {image_tag: string}`; requires `production` GitHub Environment with 2 required reviewers; apply production overlay.
> **📦 Stack:** Docker multi-stage, GitHub Actions Environments, kubectl kustomize, AWS ECR
> **✅ Outcome:** API Docker image is under 500MB. Web image is under 200MB. Production deployment requires 2 reviewer approvals.

---

## Phase 62 — Kubernetes & Infrastructure as Code

**Context:** Production-grade Kubernetes with HPA, PDB, and Terraform-managed cloud infrastructure in AWS. All infrastructure is code — no manual cloud console operations.

#### Subphase 62.1 — Kubernetes Manifests & Kustomize Overlays

> **🎭 Role:** Senior Platform Engineer and Kubernetes Expert
> **📍 Context:** All Kubernetes resources are base manifests with Kustomize overlays for staging and production. This single-source-of-truth approach prevents configuration drift between environments.
> **🔧 Task:** Write base manifests in `infra/kubernetes/base/`. `deployment-api.yaml`: 2 replicas, `resources.requests: {cpu: 500m, memory: 512Mi}`, `limits: {cpu: 2, memory: 2Gi}`, liveness `GET /v1/health` (30s delay, 10s period, 3 failures), readiness `GET /v1/health/ready` (10s delay, 5s period). `deployment-celery.yaml`: 2 replicas. `deployment-web.yaml` and `deployment-admin.yaml`. `hpa-api.yaml`: CPU 70%, min 2 max 10. `hpa-celery.yaml`: custom metric `celery_queue_length`, min 2 max 8 via KEDA. `pdb-api.yaml` and `pdb-celery.yaml`: `minAvailable: 1`. Overlays: `staging/kustomization.yaml` patches replicas to 1, reduces resource limits by 50%; `production/kustomization.yaml` uses base as-is.
> **📦 Stack:** Kubernetes 1.29+, Kustomize 5.x, KEDA (for queue-based HPA)
> **✅ Outcome:** `kubectl apply -k infra/kubernetes/overlays/staging --dry-run=client` succeeds. Staging patches reduce API replicas to 1.

#### Subphase 62.2 — Terraform Infrastructure Modules

> **🎭 Role:** Senior Infrastructure Engineer with AWS Terraform expertise
> **📍 Context:** Six Terraform modules provision the complete AWS infrastructure. IRSA bindings ensure pods access only the S3 resources they need — no wildcard IAM permissions.
> **🔧 Task:** Write Terraform modules in `infra/terraform/modules/`. `vpc`: VPC with 3 public + 3 private subnets across 3 AZs, NAT Gateway, security groups (API port 8000, Redis 6379, PostgreSQL 5432). `eks`: managed node group with mixed instance policy `[m5.large, m5a.large]`, on-demand base 2 + spot. `rds`: PostgreSQL 16, Multi-AZ, 7-day backup retention, `storage_encrypted=true`, parameter group `log_statement=ddl`. `elasticache`: Redis 7 cluster mode disabled, `at_rest_encryption_enabled=true`, `transit_encryption_enabled=true`. `s3`: versioned bucket, SSE-S3 encryption, `block_public_acls=true`. `ecr`: one repo per service, lifecycle policy keeping last 10 images. IRSA: API SA → `s3:GetObject` on `arn:aws:s3:::xaiguard-artifacts/*`; Celery SA → `s3:GetObject, s3:PutObject` on same.
> **📦 Stack:** Terraform ≥1.8, AWS provider 5.x
> **✅ Outcome:** `terraform plan` on staging shows expected creates with no drift. IRSA role policies have no `*` actions.

---

## Phase 63 — Production Hardening, Research Paper & Project Completion

**Context:** SLOs, disaster recovery, the peer-review-quality research paper, acceptance testing, and the v1.0.0 release that marks the project's completion.

#### Subphase 63.1 — SLO Definition & Multi-Window Burn Rate Alerting

> **🎭 Role:** Site Reliability Engineer
> **📍 Context:** SLOs define the quality commitment. Multi-window burn rate alerting catches violations early: fast-burn for immediate pages, slow-burn for proactive tickets — matching Google's SRE book pattern.
> **🔧 Task:** Define five SLOs in `docs/slos.md`: (1) availability 99.9% / 30-day; (2) prediction P99 ≤ 100ms; (3) error rate ≤ 0.1%; (4) alert delivery freshness ≤ 10 seconds from prediction to WebSocket delivery; (5) explanation P99 ≤ 500ms. Implement multi-window burn rate Grafana alert rules in `infra/grafana/alerts/slo-rules.json`: fast-burn alert (5% error budget in 1 hour → PagerDuty critical), slow-burn alert (10% in 6 hours → Slack ticket). Configure Grafana contact points: PagerDuty integration for critical pages, Slack webhook for tickets. Write error budget policy in `docs/error-budget-policy.md`: if budget < 50%, freeze new features.
> **📦 Stack:** Grafana 10, Prometheus, PagerDuty, Slack webhooks
> **✅ Outcome:** Five SLOs are defined and monitored. A test injection of 10× normal error rate fires the fast-burn alert within 5 minutes.

#### Subphase 63.2 — Disaster Recovery Runbook & Graceful Degradation

> **🎭 Role:** Senior Platform Reliability Engineer
> **📍 Context:** Production outages need pre-documented recovery procedures so on-call engineers can restore service without improvising under pressure. Graceful degradation ensures analysts continue receiving alerts even when ML inference is unavailable.
> **🔧 Task:** Write `docs/disaster-recovery-runbook.md` with exact CLI commands for 4 scenarios: (1) RDS failure — `aws rds restore-db-cluster-to-point-in-time` targeting RTO=4h; (2) MLflow registry loss — `aws s3 cp s3://... ml/artifacts/ --recursive` + re-register commands, RTO=1h; (3) Kubernetes namespace corruption — `kubectl apply -k infra/kubernetes/overlays/production/`, RTO=30min; (4) full cluster loss — `terraform apply` + `kubectl apply -k` + `dvc pull`, RTO=2h. Implement graceful degradation in `services/api/predictions/router.py`: catch `ModelNotLoadedError`, call `HeuristicFallbackClassifier.predict(event)` from `services/api/predictions/fallback.py` (rule-based: port scan if unique_dst_ports > 50, DDoS if packet_rate > 10000, else Normal), add `X-Degraded-Mode: true` response header.
> **📦 Stack:** AWS CLI, kubectl, Terraform, FastAPI
> **✅ Outcome:** The runbook provides copy-paste CLI commands for every scenario. `X-Degraded-Mode: true` is set when the model is unavailable.

#### Subphase 63.3 — Research Paper Writing Guide

> **🎭 Role:** Principal Research Scientist and Lead Author
> **📍 Context:** The research paper is the primary academic output of the XAI-Guard project. It must be complete enough for submission to a workshop at IEEE S&P, USENIX Security, or a top ML venue. By now, every section has been drafted incrementally: Abstract (P2), Introduction (P1), Datasets (P9–P17), Feature Engineering (P18–P25), Experiments (P26–P39), Statistical Analysis (P38.4), Discussion (P37). This subphase assembles and polishes all pieces.
> **🔧 Task:** Write the XAI-Guard research paper in `docs/research-paper.md`. Use the following template:
>
> **Abstract** (250 words): Problem statement → Approach (4 datasets, 6 models, 3 XAI methods, 3-pillar evaluation) → 3 key quantitative findings → Implication for production deployment. Use specific numbers (e.g., "XGBoost achieved F1=0.941 with P99 latency of X ms").
>
> **§1 Introduction**: (a) Motivation: why is explainable IDS research needed now? (cite 3 papers showing the gap); (b) Problem: existing IDS studies compare models without explainability or operational constraints; (c) Our approach: XAI-Guard's three-pillar framework; (d) 4 Contributions: [1] First multi-dataset comparative study of 6 model families under unified evaluation, [2] Three-pillar framework combining prediction, explainability, and operational fitness, [3] Open-source implementation with reproducible DVC pipeline, [4] Champion/Challenger production deployment policy; (e) 8 Research Questions (from P1.2).
>
> **§2 Related Work**: Survey prior work in 3 areas: (a) ML-based IDS (NSL-KDD/CICIDS papers, 2019–2025); (b) XAI for cybersecurity (SHAP/LIME applications to intrusion detection); (c) Limitations of prior work (single dataset, no XAI, no latency reporting). The Related Work section establishes WHY your contribution is novel.
>
> **§3 Datasets & Preprocessing** (from P9–P17 notebooks): Table 1 (dataset statistics), Table 2 (feature schema), Figure 1 (class distributions), split strategy description, SMOTE justification. Every preprocessing decision must be justified.
>
> **§4 Experiments & Results**: §4.1 Experimental Setup (hardware, software versions, seeds); §4.2 Ablation Study (Table 3 — from P22B); §4.3 Model Performance (Table 4 — the main result); §4.4 Explainability (Figure 3 SHAP, Table 8 LIME-SHAP correlation); §4.5 Cross-dataset Transfer (Table 7).
>
> **§5 Statistical Analysis** (from P38.4 notebook): McNemar matrix, 95% CIs, Cohen's d effect sizes.
>
> **§6 Operational Fitness** (from P36): Table 6 latency, Figure 5 Pareto frontier, CDS ranking.
>
> **§7 Discussion**: Answer each RQ1–RQ8 with a specific number and a one-sentence interpretation. Acknowledge limitations.
>
> **§8 Conclusion**: 3–4 sentences: what was done, main finding, implication, future work.
>
> **References**: Minimum 25 references. Use IEEE citation format. Must include: Lundberg & Lee 2017 (SHAP), Vaswani et al. 2017 (Transformer), Ribeiro et al. 2016 (LIME), Hinton et al. 2015 (distillation), the four dataset papers.
>
> **📦 Stack:** Markdown (LaTeX-compatible for paper export via pandoc)
> **✅ Outcome:** The paper draft is complete in `docs/research-paper.md`. All quantitative claims reference specific MLflow run IDs. Use `pandoc research-paper.md --citeproc -o research-paper.pdf` to produce a PDF draft.

#### Subphase 63.5 — Supplementary Materials Checklist

> **🎭 Role:** Principal Research Scientist
> **📍 Context:** Most ML venues (NeurIPS, ICML, AAAI, IJCAI) require a reproducibility checklist or supplementary materials document. Without it, papers can be rejected on grounds of non-reproducibility, regardless of the technical quality.
> **🔧 Task:** Create `docs/supplementary-materials.md`. Include:
>
> **Reproducibility Statement** (required by most venues):
> ```
> All experiments are reproducible using:
>   git clone https://github.com/[your-username]/xai-guard
>   git checkout v1.0.0
>   dvc pull   # retrieves exact dataset versions
>   dvc repro  # reproduces all preprocessing + training + evaluation
> ```
>
> **Model Hyperparameter Tables** (supplementary Table S1–S6): One table per model family listing ALL searched and final hyperparameter values. This is required for reproducibility.
>
> **Dataset Statistics** (supplementary Table S7): Exact record counts per class, per split, per dataset — more detail than the main paper allows.
>
> **Computational Resources**: "All experiments were run on [hardware]. Training the full pipeline from raw datasets to evaluation took approximately X GPU-hours."
>
> **Ethical Statement**: "All datasets used are publicly available and contain no personally identifiable information. Network traffic analysis was conducted on anonymised simulation data."
>
> **Data Availability**: "The preprocessed DVC-tracked datasets are available at [DVC remote URL]. The raw datasets are available at their respective official URLs (NSL-KDD: [...], CICIDS-2017: [...], UNSW-NB15: [...], BETH: [...])."
>
> **📦 Stack:** Markdown
> **✅ Outcome:** `docs/supplementary-materials.md` is complete. Submission to any venue requiring supplementary materials is ready.

#### Subphase 63.6 — Venue Selection Guide

> **🎭 Role:** Principal Research Scientist
> **📍 Context:** Choosing the right venue for your first paper dramatically affects your probability of acceptance. This subphase provides a structured guide for matching your paper to the right conference or journal.
> **🔧 Task:** Review your paper's contributions and select a primary and two backup venues. Use this decision framework:
>
> **Tier 1 — Security venues (higher impact, harder to get in):**
> - IEEE Symposium on Security and Privacy (IEEE S&P) — Top-tier, ~15% acceptance rate
> - USENIX Security Symposium — Top-tier, ~15% acceptance rate
> - ACM CCS — Top-tier, ~18% acceptance rate
> - NDSS — Strong-tier, ~20% acceptance rate
>
> **Tier 2 — ML venues with security track:**
> - ICML Security Workshop — Good exposure to ML community
> - NeurIPS Workshop on ML for Cybersecurity — Annual workshop, good for a first paper
> - AAAI — Accepts applied ML papers including IDS studies
>
> **Tier 3 — Best for a first full paper submission (recommended starting point):**
> - IEEE Access — Open access, high acceptance rate, peer-reviewed
> - Computers & Security (Elsevier) — The primary IDS research journal, ~30% acceptance rate
> - IEEE Transactions on Information Forensics and Security (TIFS) — Top-tier journal for security ML
>
> **For a student's first paper, recommended path:**
> 1. Submit to NeurIPS or ICML Workshop on ML for Cybersecurity (lower bar, fast feedback)
> 2. Use workshop feedback to revise, submit to Computers & Security journal
> 3. Upon journal acceptance, submit an extended version to IEEE S&P
>
> **What reviewers will look for:** (1) Novelty — is the comparison truly the first of its kind? Check prior surveys; (2) Statistical rigour — McNemar's + bootstrap CIs + effect sizes are expected; (3) Reproducibility — DVC pipeline + open code are major positives; (4) Practical significance — does the CDS and latency analysis make the paper actionable?
>
> **📦 Stack:** None (planning task)
> **✅ Outcome:** `docs/venue-selection.md` documents your primary and two backup venues, their submission deadlines, page limits, and the specific contributions that differentiate your paper for each venue.

---



> **🎭 Role:** QA Lead, Release Manager, and Project Completion Authority
> **📍 Context:** The acceptance test formally certifies the production system before the v1.0.0 tag. The release bundles all research artifacts, documentation, and code in a stable, reproducible state.
> **🔧 Task:** Write `tests/acceptance/test_production.py`. Replay 10,000 CICIDS-2017 events at 500 events/sec using `httpx.AsyncClient` with `asyncio.gather(*(predict(event) for event in events))`. Assert: (1) all CRITICAL+HIGH alerts appear in the WebSocket stream within 10 seconds; (2) classification F1 on replayed events is within ±0.01 of the reported research paper value; (3) `xaiguard_predictions_total` Prometheus counter incremented by 10,000; (4) Grafana API shows both dashboards as healthy; (5) XAIPanel loads for a sampled alert. On success: `git tag -a v1.0.0 -m "XAI-Guard v1.0.0 — Production Release"`, write `CHANGELOG.md` with one-line summaries for all 63 phases, write `docs/future-roadmap.md` with 7 research directions: (a) LLM-based natural language XAI summaries, (b) online learning without full retraining, (c) federated learning for multi-organisation threat sharing, (d) Graph Neural Network for lateral movement detection, (e) multi-modal detection combining logs + NetFlow + endpoint telemetry, (f) active learning loop for analyst feedback, (g) Kafka streaming for 100k+ events/sec.
> **📦 Stack:** httpx, asyncio, prometheus_client (query API), Playwright (Grafana check), git
> **✅ Outcome:** All 5 acceptance assertions pass. The `v1.0.0` git tag exists and is pushed. `CHANGELOG.md` covers all 63 phases.

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
| 48–55 | Backend Domain Modules & Dashboard | 07 |
| 56–63 | Admin Panel, MLOps & Production | 08 |

**Previous ←** [07 — Backend Domain Modules & Dashboard](07-mlops-security-testing-and-performance.md)

---
*XAI-Guard: 63 phases · 350+ prompt-driven subphases · Research-grade ML · Production-grade Modular Monolith API · Enterprise-quality Next.js 14 Dashboard & Admin Panel.*
