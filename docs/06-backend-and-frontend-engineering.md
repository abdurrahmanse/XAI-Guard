# 06 — Backend & Frontend Engineering

> **Phases 21 · 22 · 23 · 24 · 25** — FastAPI inference service, model registry, event ingestion, security dashboard, and admin panel.

---

## Phase 21 — FastAPI Inference Service

**Goal:** Build the production-grade Python inference service that serves real-time predictions and asynchronous XAI explanations within the defined latency budget.

**Context:** The FastAPI service is the ML serving layer. It loads the Champion model from the registry, runs the feature pipeline on incoming events, returns predictions with confidence and severity, and dispatches explanation generation to Celery workers asynchronously. Latency budget: P99 < 100 ms for prediction, < 500 ms for explanation (async).

**Tools:** FastAPI 0.110+, Uvicorn, Pydantic v2, SQLAlchemy 2 (async), Redis, Celery, MLflow (model loading), `prometheus-fastapi-instrumentator`, `structlog`

**Tasks:**

- [ ] 21.1 Scaffold `services/api/` structure:
  ```
  services/api/
  ├── main.py                  # FastAPI app factory
  ├── routers/
  │   ├── predictions.py        # POST /v1/predict
  │   ├── explanations.py       # POST /v1/explain, GET /v1/explain/{task_id}
  │   ├── models.py             # GET /v1/models
  │   ├── alerts.py             # GET /v1/alerts, WS /v1/ws/alerts
  │   ├── events.py             # POST /v1/events (ingestion)
  │   └── health.py             # GET /v1/health
  ├── schemas/                  # Pydantic models (Phase 5)
  ├── services/
  │   ├── inference.py          # Champion model loading + prediction
  │   ├── model_registry.py     # Champion/Challenger management
  │   ├── explanation.py        # XAI coordination
  │   └── threat_intel.py       # Threat intel (stub until Phase 34)
  ├── tasks/
  │   ├── celery_app.py         # Celery app config
  │   ├── explanation_tasks.py  # Async SHAP/LIME Celery tasks
  │   └── pipeline_tasks.py     # Event processing worker
  ├── models/                   # SQLAlchemy ORM models
  ├── alembic/                  # DB migrations
  ├── metrics.py                # Custom Prometheus metrics
  └── dependencies.py           # FastAPI dependency injection (DB, Redis, auth)
  ```
- [ ] 21.2 Implement `POST /v1/predict`:
  - Validate `SecurityEvent` input (Pydantic v2)
  - Check Redis cache: `GET feature:{hash(event)}` → use cached features if hit
  - Run `ml.src.features` pipeline on cache miss; cache result with TTL=60s
  - Load Champion model from in-memory model store (`services/inference.py`)
  - Run inference; compute `confidence`, `attack_type`, `severity`
  - Async DB write: store `Prediction` record
  - Dispatch SHAP explanation Celery task; include `explanation_task_id` in response
  - Return `PredictionResponse` in < 100 ms P99
- [ ] 21.3 Implement `POST /v1/explain` + `GET /v1/explain/{task_id}`:
  - `POST` dispatches `generate_shap_explanation.delay(prediction_id, model_id, X_sample)`
  - Celery task computes SHAP (or LIME per request param); stores result in PostgreSQL
  - `GET` polls task status: `{status: pending|processing|complete|failed, result: SHAPExplanation | null}`
- [ ] 21.4 Implement `GET /v1/models` — list all registered models with metrics, status (champion/challenger/archived), last_evaluated_at
- [ ] 21.5 Implement `GET /v1/alerts` — paginated, sortable by severity/timestamp; filter by severity, attack_type, acknowledged
- [ ] 21.6 Implement model caching in `services/inference.py`:
  - On startup: load Champion model artifact from MLflow into memory
  - Background thread polls every 60s: if champion model version changed → reload
  - Never reload during a live request (double-buffer swap)
- [ ] 21.7 Add Prometheus custom metrics in `metrics.py`:
  ```python
  prediction_counter = Counter('xaiguard_predictions_total', 'Total predictions', ['model', 'attack_type', 'severity'])
  prediction_latency = Histogram('xaiguard_prediction_latency_ms', 'Prediction latency', buckets=[10,25,50,75,100,250,500])
  confidence_histogram = Histogram('xaiguard_prediction_confidence', 'Confidence scores', buckets=[0.5,0.6,0.7,0.8,0.9,0.95,1.0])
  drift_score_gauge = Gauge('xaiguard_drift_score', 'Current MMD drift score', ['model'])
  champion_version = Info('xaiguard_champion_model', 'Current champion model info')
  ```
- [ ] 21.8 Add `structlog` structured logging: every prediction logs `{model_version, attack_type, confidence, severity, latency_ms, source_ip}`
- [ ] 21.9 Write unit tests in `tests/api/test_predict.py` using `pytest` + `httpx.AsyncClient`; mock ML model with `unittest.mock.patch`
- [ ] 21.10 Write integration test: send 100 events sequentially; assert all return < 100 ms; assert P99 < 100 ms

**Output:** FastAPI service with all endpoints; Celery workers running; Prometheus metrics exposed at `/metrics`; unit + integration tests passing

---

## Phase 22 — Champion/Challenger Model Registry

**Goal:** Build the model lifecycle management system — safe registration, shadow inference, automated evaluation, promotion, and rollback.

**Context:** The Champion/Challenger pattern is the production-safe way to introduce new models. The Challenger runs in shadow mode: receives the same events as the Champion, its predictions are stored but NOT served to analysts. A nightly Celery job compares metrics. If the Challenger wins by defined thresholds, it is automatically promoted. Rollback always reverts to the previous Champion.

**Tools:** FastAPI, SQLAlchemy 2, MLflow Model Registry, Celery Beat, PostgreSQL

**Promotion Criteria (from Phase 1):**
- F1_macro improvement ≥ 0.02 (`+2%`)
- ROC-AUC improvement ≥ 0.01 (`+1%`)
- Challenger P99 latency ≤ 100 ms (within budget)

**Tasks:**

- [ ] 22.1 Write `services/api/services/model_registry.py` — `ModelRegistryService`:
  ```python
  class ModelRegistryService:
      def register_model(self, mlflow_run_id, name, version, metrics) → ModelRecord: ...
      def set_champion(self, model_id) → None: ...
      def set_challenger(self, model_id) → None: ...
      def get_champion(self) → ModelRecord: ...
      def get_challenger(self) → ModelRecord | None: ...
      def evaluate_challenger(self, window_hours=24) → EvaluationResult: ...
      def promote_challenger(self) → None:  # Champion → archived; Challenger → champion
      def rollback(self) → None:  # Champion → archived; previous_champion → champion
  ```
- [ ] 22.2 Implement shadow inference in `services/inference.py`:
  - Every prediction: async dispatch `run_shadow_inference.delay(event, challenger_model_id)`
  - Celery task loads Challenger model, runs inference, stores `shadow_prediction` in DB
  - This never blocks the Champion prediction latency path
- [ ] 22.3 Implement nightly evaluation Celery Beat task (`tasks/pipeline_tasks.py`):
  ```python
  @app.task
  def evaluate_challenger_nightly():
      # 1. Fetch last 24h shadow predictions + champion predictions for same events
      # 2. Compute F1, ROC-AUC for both on same ground-truth labels
      # 3. Compute performance delta
      # 4. If delta > thresholds AND latency OK → auto-promote
      # 5. Log result to model_evaluations DB table + MLflow
  ```
- [ ] 22.4 Implement `POST /v1/models/rollback` endpoint — admin role only; reverts champion to previous_champion
- [ ] 22.5 Implement `GET /v1/models/history` — list all model versions with promotion/demotion events and timestamps
- [ ] 22.6 Write tests for all registry operations, including promotion and rollback scenarios

**Output:** Shadow inference working; nightly evaluation job; auto-promotion; rollback endpoint; model history

---

## Phase 23 — Event Ingestion & Alert Pipeline

**Goal:** Build the data ingestion pipeline that receives security events from external sources and routes them through the ML pipeline, with real-time WebSocket alert delivery.

**Context:** In production, security events arrive via REST (bulk POST), webhooks, or Kafka. Events are validated, deduplicated, enqueued, and processed by Celery workers. High-severity predictions trigger real-time WebSocket alerts to connected dashboard clients. Event deduplication prevents alert storms.

**Tools:** FastAPI, Celery, Redis Streams, PostgreSQL, WebSocket (Starlette), structlog

**Tasks:**

- [ ] 23.1 Implement `POST /v1/events` — bulk ingestion endpoint:
  - Accept up to 1000 events per batch (list of `SecurityEvent`)
  - Deduplicate: compute `event_hash = sha256(source_ip + dest_ip + timestamp + protocol)`; skip if hash exists in Redis (TTL=5 min)
  - Bulk insert raw events to PostgreSQL `security_events` table
  - Enqueue each event to Redis Stream `events:pending`
  - Return `{accepted: N, duplicates_skipped: M}` immediately (no inference wait)
- [ ] 23.2 Write Celery worker `event_processor_worker` (consumes from Redis Stream):
  - Pop event from `events:pending`
  - Run feature pipeline
  - Call inference service → get prediction
  - Store prediction + alert in DB
  - If severity ≥ HIGH: publish to Redis channel `alerts:live`
  - Acknowledge message in Redis Stream
- [ ] 23.3 Implement alert severity classification:
  ```python
  SEVERITY_THRESHOLDS = {
      SeverityLevel.critical: 0.90,
      SeverityLevel.high: 0.75,
      SeverityLevel.medium: 0.50,
      SeverityLevel.low: 0.0
  }
  ```
- [ ] 23.4 Implement WebSocket endpoint `GET /v1/ws/alerts`:
  - On connect: authenticate JWT from query param `?token=`
  - Subscribe to Redis channel `alerts:live`
  - Stream all new alerts to connected clients in real time
  - Handle disconnect gracefully (cancel Redis subscription)
- [ ] 23.5 Implement alert deduplication: same `(source_ip, attack_type)` within 5 minutes → suppress duplicate alert, increment `alert.alert_count` on existing record
- [ ] 23.6 Write `services/api/scripts/replay_events.py` — reads a CSV or JSON file of historical events and replays them at configurable rate (e.g., 100 events/sec for integration testing)
- [ ] 23.7 Write load test with `locust`:
  ```python
  class EventIngestionUser(HttpUser):
      @task
      def send_events(self):
          self.client.post('/v1/events', json={'events': [random_event() for _ in range(100)]})
  ```
  Target: 1000 events/sec sustained; verify queue depth stays bounded; no 5xx errors

**Output:** Bulk ingestion endpoint; Celery event processing workers; WebSocket real-time alerts; deduplication; load test passing

---

## Phase 24 — Security Dashboard (Next.js) — Core

**Goal:** Build the primary analyst-facing Security Dashboard with real-time threat detections, SHAP explanations, and model status — the interface described in the project’s Threat Detection card design.

**Context:** Security Operations Centre (SOC) analysts need: live alerts sorted by severity, threat detail with the “Why?” explanation panel, and model confidence. The dashboard is always dark mode (SOC environments), real-time via WebSocket, and optimised for fast triage decisions.

**Tools:** Next.js 14 (App Router), TypeScript, Tailwind CSS, Recharts, SWR, Socket.io-client, Zod, Playwright

**Reference design (Threat Detection card from spec):**
```
┌────────────────────────────────────────┐
│ THREAT DETECTED                            │
│ Type: Credential Attack                    │
│ Confidence: 93%         Severity: CRITICAL │
│                                            │
│ Why?                                       │
│ ─────────────────────────────────────  │
│ Failed login attempts        +34%          │
│ Unusual IP geolocation       +27%          │
│ Login time anomaly           +18%          │
│ Request frequency            +14%          │
│                                            │
│ Action: Investigate IP + block temporarily │
└────────────────────────────────────────┘
```

**Tasks:**

- [ ] 24.1 Scaffold `apps/web/` with Next.js 14 App Router:
  ```
  apps/web/app/
  ├── layout.tsx            # Root layout: dark mode, nav, sidebar
  ├── page.tsx              # Dashboard overview (redirects to /dashboard)
  ├── dashboard/            # Main dashboard
  ├── alerts/               # Alert list + detail pages
  ├── models/               # Model status page
  └── reports/              # Research reports view
  ```
- [ ] 24.2 Build `AlertsFeed` component (`packages/ui/src/components/AlertsFeed.tsx`):
  - WebSocket connection to `/v1/ws/alerts`
  - Renders scrollable list of alerts sorted by severity then timestamp
  - Severity badge: CRITICAL=red, HIGH=orange, MEDIUM=yellow, LOW=blue
  - Click on alert → opens `ThreatDetailPanel`
  - Auto-scroll to top on new alert (with “N new alerts” toast if scrolled down)
- [ ] 24.3 Build `ThreatDetailPanel` component — renders the Threat Detection card:
  - `attack_type`, `confidence` (formatted as `%`), `severity` badge
  - **Why?** section: top 5 SHAP factors as a horizontal bar chart (feature name + `+XX%` contribution)
  - Recommended Action (from Phase 19 analyst evaluation dataset mapping)
  - Source IP + Destination IP + Protocol display
  - MITRE ATT&CK technique badge (Phase 34)
- [ ] 24.4 Build `XAIPanel` component — full SHAP waterfall chart:
  - Use Recharts `BarChart` (horizontal)
  - Features on Y-axis, SHAP values on X-axis
  - Positive contributions (red/warm), negative contributions (blue/cool)
  - Base value line
  - Toggle between SHAP / LIME views (if LIME also available for that prediction)
- [ ] 24.5 Build `MetricsDashboard` component:
  - Live model performance: F1 gauge, ROC-AUC gauge (Recharts `RadialBarChart`)
  - Precision/Recall as numeric displays
  - Alerts per hour trend (Recharts `AreaChart`, last 24h)
  - Attack type distribution (Recharts `PieChart`)
- [ ] 24.6 Build `ModelStatusBar` — top-level status strip:
  - Champion model: name, version, last updated
  - Challenger model: name, version, evaluation status
  - Drift score gauge (green/yellow/red)
- [ ] 24.7 Dark mode implementation:
  - Tailwind `dark:` classes; default to dark; CSS variables for SOC-appropriate colours
  - Background: `#0a0a0f` (near-black), surface: `#12121a`, accent: `#ff4444` (critical alerts)
- [ ] 24.8 Write Storybook stories in `packages/ui/.storybook/` for: `AlertsFeed`, `ThreatDetailPanel`, `XAIPanel`, `MetricsDashboard`, `ModelStatusBar`
- [ ] 24.9 Write Playwright E2E tests:
  - Login → dashboard loads with `ModelStatusBar`
  - WebSocket alert appears → click → `ThreatDetailPanel` opens with XAI panel
  - XAI panel loads SHAP chart

**Output:** Security Dashboard with real-time alerts, Threat Detection card, XAI panel, dark SOC mode; Storybook stories; E2E tests passing

---

## Phase 25 — Admin Panel & Research Reports

**Goal:** Build the MLOps control panel for data scientists and platform engineers to manage models, browse experiments, and export the research comparison report.

**Context:** The Admin Panel is the operational brain of XAI-Guard. It surfaces the Model Registry, Champion/Challenger promotion controls, MLflow experiment data, drift monitoring, and the research report export. Role-based access prevents analysts from accidentally promoting or rolling back models.

**Tools:** Next.js 14 (App Router), TypeScript, Tailwind CSS, Recharts, `@react-pdf/renderer` (PDF export), Playwright

**Tasks:**

- [ ] 25.1 Scaffold `apps/admin/` — separate Next.js app (same packages/ui shared library):
  ```
  apps/admin/app/
  ├── layout.tsx
  ├── experiments/          # MLflow experiment browser
  ├── models/               # Model Registry management
  ├── datasets/             # Dataset statistics
  ├── drift/                # Drift monitor
  └── reports/              # Research report export
  ```
- [ ] 25.2 Build `ExperimentsTable` component:
  - Fetches all MLflow runs via `/v1/models` API
  - Filterable by: model family, dataset, date range
  - Sortable by: F1, ROC-AUC, latency, training time
  - Click on run → opens run detail drawer with all logged params and metrics
- [ ] 25.3 Build `ModelComparisonView` — renders the master comparison table (Phase 16):
  - All 6 models as rows, all metrics as columns
  - Champion highlighted in green, Challenger in blue, others in neutral
  - Sortable columns; download as CSV button
- [ ] 25.4 Build `ChampionChallengerPanel`:
  - Side-by-side metric comparison: Champion (left) vs Challenger (right)
  - Shows: F1, ROC-AUC, Latency-P99, last_evaluated_at
  - Performance delta badges: `+0.023 F1` (green if positive, red if negative)
  - **Promote** button (admin role only) → confirmation modal → calls `POST /v1/models/promote`
  - **Rollback** button (admin role only) → confirmation modal → calls `POST /v1/models/rollback`
- [ ] 25.5 Build `DriftMonitorPanel`:
  - Drift score timeline (Recharts `LineChart`): last 30 days drift score per model
  - Current status badge: OK (< 0.05), WARNING (0.05–0.10), CRITICAL (> 0.10)
  - Last drift report timestamp + summary
- [ ] 25.6 Build `ReportGenerator` — research export:
  - Download master comparison table as CSV
  - Generate PDF report with `@react-pdf/renderer`: includes comparison table, per-attack heatmap image, radar chart image
  - PDF structured as: Executive Summary, Model Comparison, XAI Trade-off, Recommendations
- [ ] 25.7 Implement RBAC in Next.js middleware:
  - `analyst` role: read-only access to all admin pages; Promote/Rollback buttons hidden
  - `admin` role: full access; Promote/Rollback enabled
  - Middleware reads JWT claims: `{role: "analyst" | "admin"}` from auth service
- [ ] 25.8 Write Playwright E2E tests: admin login → model comparison view loads → promote button visible → click → confirmation modal → confirm → champion badge updates

**Output:** Admin panel with model management, experiment browser, drift monitor, PDF report export, RBAC, E2E tests passing

---

## Phase Map

| Phase | Title | Key Output |
|-------|-------|------------|
| P21 | FastAPI Inference Service | Prediction + explanation API, Prometheus metrics |
| P22 | Champion/Challenger Registry | Shadow inference, auto-promotion, rollback |
| P23 | Event Ingestion & Alerts | Bulk ingestion, WebSocket real-time alerts |
| P24 | Security Dashboard | Real-time alert feed, Threat Detection card, XAI panel |
| P25 | Admin Panel & Reports | Model management, research report PDF export, RBAC |

**Previous:** ← [05 — XAI & Model Evaluation](05-xai-and-model-evaluation.md) | **Next:** → [07 — MLOps, Security, Testing & Performance](07-mlops-security-testing-and-performance.md)
