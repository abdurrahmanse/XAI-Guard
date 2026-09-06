# 07 — MLOps, Security, Testing & Performance

> **Phases 26 · 27 · 28 · 29 · 30 · 31** — Automated ML pipeline, observability, security hardening, testing strategy, performance optimisation, and CI/CD.

---

## Phase 26 — MLOps Pipeline: Automated Training & Retraining

**Goal:** Automate the full ML lifecycle — data → train → evaluate → register → promote — triggered by schedule or drift detection.

**Context:** Models degrade as attack patterns evolve. Manual retraining is slow and error-prone. An automated MLOps pipeline runs weekly on schedule and on-demand when drift is detected. The pipeline uses the exact same code from Phases 10–15, orchestrated via GitHub Actions + Celery Beat. DVC ensures dataset reproducibility across runs.

**Tools:** Celery Beat, GitHub Actions, DVC, MLflow, Docker

**Tasks:**

- [ ] 26.1 Write `ml/src/pipeline.py` — the orchestration entrypoint:
  ```python
  def run_pipeline(
      models: list[str] = ALL_MODELS,
      dataset: str = 'cicids2017',
      experiment_name: str = None
  ):
      load_data()           # DVC pull latest data version
      preprocess()          # Phase 7 pipeline
      feature_engineer()    # Phase 8 features
      for model in models:
          train(model)      # Phases 10-15
          evaluate(model)   # Metrics + XAI checks
      select_challenger()   # Phase 16 composite score
      register_models()     # MLflow + DB registry
  ```
  All steps log to MLflow; pipeline run metadata stored in `pipeline_runs` DB table.
- [ ] 26.2 Write `.github/workflows/ml-pipeline.yml`:
  ```yaml
  on:
    schedule:
      - cron: '0 2 * * 0'  # Every Sunday at 02:00 UTC
    workflow_dispatch:       # Manual trigger with optional model filter
  jobs:
    train:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
          with: {python-version: '3.11'}
        - run: pip install uv && uv sync
        - run: dvc pull  # Download latest data from MinIO
        - run: uv run python ml/src/pipeline.py
        - run: dvc push  # Push new processed data + artifacts
  ```
- [ ] 26.3 Write Celery Beat task `drift_triggered_retrain` in `services/api/tasks/pipeline_tasks.py`:
  - Called by `DriftDetector` when `drift_score > 0.10` (CRITICAL threshold)
  - Runs `pipeline.py` for the Champion model family only (targeted retraining)
  - Sends Slack/webhook notification on completion with new model metrics
- [ ] 26.4 Implement model alias pinning in the serving layer:
  - `services/inference.py` loads model by alias `'champion'`, never by version number
  - MLflow Model Registry alias ensures zero-code-change model upgrades
- [ ] 26.5 Implement pipeline health checks in `pipeline.py`:
  - After training: if new model F1 drops > 5% vs previous run → flag as anomaly, do NOT promote
  - Alert via webhook: `{alert: "pipeline_anomaly", model: ..., f1_delta: ..., action: "manual_review_required"}`
- [ ] 26.6 Ensure DVC push runs after every pipeline run: new processed dataset version + model artifact pushed to MinIO
- [ ] 26.7 Write integration test: trigger `pipeline.py` on a 500-sample synthetic dataset; verify new model registered in MLflow within 5 minutes

**Output:** Automated weekly pipeline; drift-triggered retraining; pipeline health anomaly detection; DVC push on every run

---

## Phase 27 — Observability & Monitoring

**Goal:** Full-stack observability — metrics, distributed traces, and logs — covering both application performance and ML-specific signals.

**Context:** Production ML systems fail in subtle ways that standard APM tools miss: model accuracy degrades silently, Celery queues back up, drift scores spike. Standard metrics (Prometheus/Grafana) are extended with ML-specific metrics. OpenTelemetry provides distributed tracing across FastAPI + Celery. Loki aggregates structured logs.

**Tools:** Prometheus, Grafana, OpenTelemetry SDK (Python), Jaeger (tracing), Loki, structlog

**Tasks:**

- [ ] 27.1 Add `prometheus-fastapi-instrumentator` to `main.py` — auto-instruments all routes with `http_request_duration_seconds` histogram and `http_requests_total` counter
- [ ] 27.2 Custom Prometheus metrics (Phase 21 already defined — ensure all are scraped):
  - `xaiguard_predictions_total` (counter, labels: `model`, `attack_type`, `severity`)
  - `xaiguard_prediction_latency_ms` (histogram, buckets: 10‡25‡50‡75‡100‡250‡500)
  - `xaiguard_prediction_confidence` (histogram)
  - `xaiguard_drift_score` (gauge, label: `model`)
  - `xaiguard_champion_model` (info: `{name, version}`)
  - `xaiguard_celery_queue_depth` (gauge, label: `queue_name`)
  - `xaiguard_active_alerts_total` (gauge, labels: `severity`)
- [ ] 27.3 Configure OpenTelemetry SDK:
  ```python
  # services/api/telemetry.py
  from opentelemetry import trace
  from opentelemetry.sdk.trace import TracerProvider
  from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

  def configure_otel(service_name: str):
      provider = TracerProvider(resource=Resource({SERVICE_NAME: service_name}))
      provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
      trace.set_tracer_provider(provider)
  ```
  Instrument: FastAPI requests, SQLAlchemy queries, Redis calls, Celery tasks
- [ ] 27.4 Write `infrastructure/grafana/dashboards/xai-guard-main.json` — main Grafana dashboard panels:
  - **RPS**: `rate(http_requests_total[5m])`
  - **P99 Latency**: `histogram_quantile(0.99, rate(xaiguard_prediction_latency_ms_bucket[5m]))`
  - **Prediction Distribution**: pie chart by `attack_type`
  - **Confidence Over Time**: line chart of mean confidence
  - **Drift Score**: line chart with WARNING/CRITICAL threshold lines
  - **Champion Model**: current version info panel
  - **Celery Queue Depth**: bar chart by queue name
  - **Active Alerts**: stat panels by severity
- [ ] 27.5 Write `infrastructure/grafana/dashboards/model-performance.json`:
  - F1 and ROC-AUC per model over time (filled from model_evaluations DB via Grafana PostgreSQL datasource)
  - Per-attack-type accuracy heatmap (refreshed after each Champion/Challenger evaluation)
- [ ] 27.6 Configure Grafana alert rules (send to Slack/PagerDuty):
  - P99 latency > 200 ms for 5 minutes → HIGH
  - Drift score > 0.05 → WARNING; > 0.10 → CRITICAL
  - Mean confidence drops > 10% vs 7-day moving average → WARNING
  - Celery queue depth > 10,000 → WARNING
- [ ] 27.7 Configure Loki log aggregation: ship structlog JSON logs from FastAPI + Celery; add Loki datasource to Grafana; create Logs panel in main dashboard

**Output:** Prometheus metrics scraped; Grafana dashboards with alerting; OTel traces visible in Jaeger; structured logs in Loki

---

## Phase 28 — Security Hardening

**Goal:** Ensure the XAI-Guard platform itself is secure — a cybersecurity tool that is insecure is both ironic and dangerous.

**Context:** Key attack vectors for this platform: unauthenticated inference endpoints (model theft, adversarial manipulation), SQL injection via event payloads, insecure model artifact loading, secrets exposure, CORS misconfiguration. Defence-in-depth: JWT auth + RBAC + input validation + rate limiting + SAST/DAST.

**Tools:** `python-jose` (JWT), `passlib[bcrypt]` (password hashing), `slowapi` (rate limiting), Bandit (SAST), OWASP ZAP (DAST), `detect-secrets` (pre-commit)

**Tasks:**

- [ ] 28.1 Implement JWT authentication in `services/api/routers/auth.py`:
  - `POST /v1/auth/login` → validates credentials vs PostgreSQL `users` table → returns `{access_token, refresh_token}`
  - Access token: JWT, expires 15 minutes; refresh token: opaque, expires 7 days, stored in DB
  - `POST /v1/auth/refresh` → validates refresh token → issues new access token
  - All non-health endpoints: `Depends(get_current_user)` — verify JWT signature + expiry
- [ ] 28.2 Implement RBAC middleware `dependencies.py`:
  ```python
  def require_role(*roles: str):
      def dependency(current_user: User = Depends(get_current_user)):
          if current_user.role not in roles:
              raise HTTPException(status_code=403, detail="Insufficient permissions")
      return Depends(dependency)
  ```
  Protect: `POST /v1/models/promote` — admin only; `POST /v1/models/rollback` — admin only
- [ ] 28.3 Strict Pydantic v2 validation on all schemas:
  - `model_config = ConfigDict(extra='forbid')` — reject unknown fields
  - IP addresses: `IPvAnyAddress` type
  - Strings: `max_length=255` on all free-text fields
  - Numeric fields: explicit `ge`/`le` bounds
- [ ] 28.4 Configure CORS in `main.py`:
  ```python
  app.add_middleware(CORSMiddleware,
      allow_origins=['http://localhost:3000', 'https://dashboard.xaiguard.internal'],
      allow_credentials=True,
      allow_methods=['GET', 'POST'],
      allow_headers=['Authorization', 'Content-Type']
  )
  ```
  No wildcard origins ever.
- [ ] 28.5 Add rate limiting with `slowapi`:
  - `POST /v1/predict`: 100 req/min per IP
  - `POST /v1/explain`: 10 req/min per IP
  - `POST /v1/events`: 50 req/min per IP
  - Rate limit exceeded → HTTP 429 with `Retry-After` header
- [ ] 28.6 Run Bandit SAST on `services/api/`: `bandit -r services/api/ -ll` (flag HIGH + MEDIUM only); fix all findings; add to CI (Phase 31)
- [ ] 28.7 Run OWASP ZAP baseline scan against local Docker deployment: `docker run -t owasp/zap2docker-stable zap-baseline.py -t http://localhost:8000`; fix all MEDIUM+ alerts
- [ ] 28.8 Implement secrets management:
  - All credentials from environment variables (never hardcoded)
  - Add `detect-secrets` to pre-commit hooks; baseline scan stored as `.secrets.baseline`
  - CI fails if new secrets detected in diff
- [ ] 28.9 SQL injection prevention: SQLAlchemy ORM only; `text()` queries forbidden; all queries use parameter binding
- [ ] 28.10 Write security tests in `tests/api/test_security.py`:
  - Unauthenticated `POST /v1/predict` → 401
  - Expired token → 401
  - Analyst role calls `POST /v1/models/promote` → 403
  - Extra field in SecurityEvent payload → 422
  - Malformed IP address in event → 422
  - Rate limit: 101st request → 429

**Output:** JWT auth; RBAC; strict input validation; CORS configured; rate limiting; Bandit + ZAP clean; secrets detection; security tests passing

---

## Phase 29 — Comprehensive Testing Strategy

**Goal:** Achieve > 80% test coverage across all components with a layered testing strategy that catches regressions before production.

**Context:** ML systems have two distinct layers to test: ML code (correctness of training, evaluation, explainability) and application code (API, pipeline, frontend). Each requires different testing strategies. Property-based testing with `hypothesis` catches edge cases that example-based tests miss. Load testing establishes the performance baseline before optimisation.

**Tools:** pytest, pytest-asyncio, pytest-cov, httpx, Playwright, locust, hypothesis

**Testing Pyramid:**

```
          [E2E: Playwright]
       [Integration: API + DB + ML]
    [Unit: ML code + API handlers]
  [Property-based: hypothesis]
[Load: locust]
```

**Tasks:**

- [ ] 29.1 **ML Unit Tests** (`tests/ml/`) — target 90% coverage on `ml/src/`:
  - `test_preprocessing.py`: each cleaner/encoder/sampler/sequence_builder in isolation
  - `test_features.py`: each feature function with synthetic DataFrames; assert shape + dtype
  - `test_models.py`: fit/predict/predict_proba on 100-sample synthetic data for all 6 models; assert output shape, values in [0,1] for probabilities
  - `test_explainers.py`: SHAPExplainer, LIMEExplainer, AttentionExplainer on synthetic data; assert output schema
  - `test_evaluation.py`: metrics calculations; drift detector initialisation and detection
- [ ] 29.2 **ML Integration Tests** (`tests/ml/integration/`):
  - Train each model on 1000-sample synthetic dataset; verify F1 > 0.5 (above random baseline for imbalanced data)
  - Run full DVC pipeline stage on dummy data; verify output files exist
  - Run MLflow logging; verify metrics appear in SQLite tracking (test mode)
- [ ] 29.3 **API Unit Tests** (`tests/api/`) — target 85% coverage on `services/api/`:
  - `test_predict.py`: valid event → 200 + PredictionResponse; invalid IP → 422; missing field → 422
  - `test_auth.py`: valid credentials → 200 + tokens; invalid credentials → 401; expired token → 401
  - `test_registry.py`: register, promote, rollback model operations
  - `test_security.py`: (from Phase 28)
  - All tests use `httpx.AsyncClient` + mock ML model (no real inference in unit tests)
- [ ] 29.4 **API Integration Tests** (`tests/api/integration/`):
  - Spin up real FastAPI + PostgreSQL (test database) + Redis via Docker Compose test profile
  - Send event → prediction stored in DB → explanation Celery task dispatched → poll until complete
  - WebSocket test: connect to `/v1/ws/alerts`, send event, verify alert received within 5 seconds
- [ ] 29.5 **Frontend Unit Tests** (`apps/web/__tests__/`, `apps/admin/__tests__/`):
  - Jest + React Testing Library for: `AlertsFeed`, `ThreatDetailPanel`, `XAIPanel`, `MetricsDashboard`
  - Mock WebSocket and API calls
  - Test RBAC: Promote button hidden for analyst role
- [ ] 29.6 **E2E Tests** (`tests/e2e/`) — Playwright:
  - `dashboard.spec.ts`: login → dashboard loads → WebSocket alert appears → click → XAI panel shows
  - `admin.spec.ts`: admin login → model comparison loads → promote button visible → confirm promote → champion updates
  - `auth.spec.ts`: analyst login → promote button NOT visible
- [ ] 29.7 **Property-Based Tests** (`tests/property/`) with `hypothesis`:
  - Preprocessing pipeline: any valid DataFrame (generated by hypothesis) → pipeline never raises (only returns)
  - SHAP explainer: any valid feature vector → sum of SHAP values + base_value ≈ model prediction
  - SecurityEvent schema: any valid IP + port combination → Pydantic validation passes
- [ ] 29.8 **Load Tests** (`tests/load/`) with locust:
  - Ramp to 500 concurrent users; run for 5 minutes
  - Metrics to capture: RPS, median latency, P95 latency, P99 latency, failure rate
  - Pass criteria: P99 < 200 ms, failure rate < 0.1%
  - Document baseline: `tests/load/baseline_results.md`
- [ ] 29.9 Configure pytest in `pyproject.toml`:
  ```toml
  [tool.pytest.ini_options]
  asyncio_mode = "auto"
  testpaths = ["tests"]
  [tool.coverage.report]
  fail_under = 80
  ```

**Output:** Full test suite; > 80% coverage enforced in CI; load test baseline documented

---

## Phase 30 — Performance Optimisation

**Goal:** Optimise the system to meet all latency budgets under production load, without compromising model accuracy.

**Context:** The latency budget is: prediction P99 < 100 ms, explanation P99 < 500 ms, dashboard first load < 2 s. Optimisation is data-driven: profile first, optimise the bottleneck, measure the impact, repeat. Common ML serving bottlenecks: feature pipeline (CPU-bound), DB writes (I/O-bound), model loading on cold start.

**Tools:** `cProfile`, `py-spy`, ONNX Runtime, `torch.quantization`, Next.js Bundle Analyzer, Uvicorn HTTP/2

**Tasks:**

- [ ] 30.1 Profile the prediction hot path:
  ```bash
  py-spy record -o profile.svg -- uvicorn services.api.main:app
  # Send 1000 predictions; analyse flame graph
  ```
  Identify whether bottleneck is: feature pipeline, model inference, DB write, or serialisation
- [ ] 30.2 ONNX export for XGBoost and Transformer:
  ```python
  # XGBoost
  xgb_model.save_model('model.onnx')  # native ONNX export
  # Transformer (via torch.onnx)
  torch.onnx.export(model, dummy_input, 'transformer.onnx', opset_version=17)
  ```
  Measure P99 latency before/after ONNX; document speedup
- [ ] 30.3 Implement request batching in `services/inference.py`:
  - Accumulate prediction requests for 10 ms (configurable `BATCH_WINDOW_MS`)
  - Process accumulated batch in single model inference call
  - Return individual results to each waiting request
  - Effective for LSTM/Transformer which benefit from batching
- [ ] 30.4 Redis feature cache (Phase 21 already designed — validate it’s working and measure hit rate):
  - Add cache hit rate metric: `xaiguard_cache_hit_rate` gauge
  - Target: > 30% cache hit rate under steady-state load (many events from same IPs)
- [ ] 30.5 Optimise DB writes:
  - Use `async with session.begin()` with bulk insert: `session.execute(insert(Prediction).values([...]))`
  - DB writes must NOT block prediction response: use `asyncio.create_task(db_write(...))`
- [ ] 30.6 Profile dashboard bundle:
  ```bash
  ANALYZE=true pnpm build --filter=web
  ```
  Ensure: initial JS bundle < 200 KB compressed; lazy-load Recharts charts; lazy-load XAI panel
- [ ] 30.7 Enable HTTP/2 in Uvicorn + nginx (infrastructure):
  - HTTP/2 multiplexing reduces connection overhead for dashboard’s multiple concurrent API calls
  - Enable gzip compression on responses > 1 KB
- [ ] 30.8 Run load test after each optimisation; document before/after in `docs/performance-optimisation-log.md`:
  | Optimisation | Before P99 | After P99 | Delta |
  |-------------|-----------|----------|-------|
  | ONNX export | X ms | Y ms | -Z% |

**Output:** All latency budgets met under 500-concurrent-user load; optimisation log documenting each change

---

## Phase 31 — CI/CD Pipeline

**Goal:** Fully automated, gated CI/CD — no code reaches production without passing all quality gates.

**Context:** Enterprise software requires automated quality enforcement. The CI pipeline runs on every PR and must pass before merge. CD deploys to staging automatically on merge to main. CD to production requires manual approval. ML model deployment is gated separately by the Champion/Challenger evaluation (Phase 22) and is not part of the app deployment.

**Tools:** GitHub Actions, Docker (multi-stage builds), pnpm, Turborepo, pytest, Playwright, trivy (container scanning), Dependabot

**Tasks:**

- [ ] 31.1 Write `.github/workflows/ci.yml`:
  ```yaml
  on: [pull_request]
  jobs:
    quality:
      steps:
        - Install deps (pnpm install + uv sync)
        - Lint: turbo lint  (eslint + ruff)
        - Type-check: turbo type-check  (tsc --noEmit + mypy)
        - Test: turbo test  (jest + pytest with coverage)
        - Coverage gate: fail if coverage < 80%
        - Security scan: bandit -r services/api/ -ll
        - Secret detection: detect-secrets scan
    build:
      needs: quality
      steps:
        - Build all apps: turbo build
        - Build Docker images: docker build for api, web, admin
        - Container scan: trivy image xaiguard/api:$SHA (fail on CRITICAL CVE)
  ```
- [ ] 31.2 Write `.github/workflows/cd-staging.yml`:
  ```yaml
  on:
    push:
      branches: [main]
  jobs:
    deploy-staging:
      steps:
        - Build + push Docker images to registry (tagged with git SHA)
        - kubectl apply -k infrastructure/k8s/overlays/staging/
        - Wait for rollout: kubectl rollout status deployment/api -n staging
        - Run smoke tests: pytest tests/smoke/ --env=staging
        - Notify Slack: ✅ Staging deploy succeeded / ❌ Deploy failed
  ```
- [ ] 31.3 Write `.github/workflows/cd-production.yml`:
  ```yaml
  on:
    workflow_dispatch:  # Manual trigger only
      inputs:
        version: {description: 'Docker image tag to deploy', required: true}
  jobs:
    deploy-production:
      environment: production  # Requires GitHub environment protection rule (1 reviewer)
      steps:
        - kubectl apply -k infrastructure/k8s/overlays/production/
        - kubectl rollout status
        - Run smoke tests: pytest tests/smoke/ --env=production
        - Notify Slack
  ```
- [ ] 31.4 Write `infrastructure/docker/Dockerfile.api` (multi-stage):
  ```dockerfile
  FROM python:3.11-slim AS builder
  RUN pip install uv
  COPY ml/pyproject.toml ml/uv.lock ./
  RUN uv sync --frozen --no-dev

  FROM python:3.11-slim AS runtime
  COPY --from=builder /app/.venv /app/.venv
  COPY services/api/ /app/api/
  COPY ml/src/ /app/ml/
  CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
  Target image size: < 500 MB
- [ ] 31.5 Write `infrastructure/docker/Dockerfile.web` and `Dockerfile.admin` (Next.js standalone output):
  ```dockerfile
  FROM node:20-alpine AS builder
  RUN corepack enable pnpm
  COPY . .
  RUN pnpm install --frozen-lockfile && pnpm build --filter=web

  FROM node:20-alpine AS runtime
  COPY --from=builder /app/apps/web/.next/standalone ./
  CMD ["node", "server.js"]
  ```
- [ ] 31.6 Add branch protection rules on GitHub:
  - `main`: require CI pass + 1 code review + no unresolved comments
  - `production`: require additional environment approval
- [ ] 31.7 Configure Dependabot in `.github/dependabot.yml`: weekly updates for npm + pip + GitHub Actions

**Output:** CI pipeline on all PRs; CD to staging automated; CD to production manual-gated; container scanning; Dependabot configured

---

## Phase Map

| Phase | Title | Key Output |
|-------|-------|------------|
| P26 | MLOps Pipeline | Automated weekly training + drift-triggered retraining |
| P27 | Observability | Prometheus, Grafana dashboards, OTel traces, Loki logs |
| P28 | Security Hardening | JWT, RBAC, rate limiting, SAST/DAST clean |
| P29 | Testing Strategy | > 80% coverage, load test baseline |
| P30 | Performance Optimisation | All latency budgets met under load |
| P31 | CI/CD Pipeline | Fully automated quality gates + deployments |

**Previous:** ← [06 — Backend & Frontend Engineering](06-backend-and-frontend-engineering.md) | **Next:** → [08 — Production Deployment & Roadmap](08-production-deployment-and-roadmap.md)
