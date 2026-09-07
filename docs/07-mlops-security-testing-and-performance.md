# 07 — Backend Domain Modules & Security Dashboard

> **Phases 48–55** | Events, Predictions, Explanations, Model Registry, Alerts & WebSocket, Threat Intelligence, Dashboard Foundation, and Alert Feed components.

## 🗺️ Research Paper Map

| Phase | What You Build | Paper Section | Paper Artefact |
|-------|---------------|---------------|----------------|
| P48 | Event ingestion + deduplication | §6 System Architecture | "Events are ingested via POST /v1/events/ingest..." |
| P49 | Prediction endpoint + feature cache | §6 Operational Fitness | Latency measurements Table 6 Row: API overhead |
| P50 | SHAP/LIME Celery explanation tasks | §6 + §4.4 | Async XAI architecture diagram |
| P51 | Champion/Challenger model registry API | §6 + §4.3 | "Promotion requires ΔF1≥0.020 AND p<0.0033..." |
| P52 | Alerts + WebSocket real-time delivery | §6 System Architecture | "Alerts delivered via WebSocket within 10s..." |
| P53 | MITRE ATT&CK threat intelligence | §6 + §1 Motivation | MITRE mapping table (attack type → technique ID) |
| P54–55 | Dashboard + Alert Feed UI | §6 Demo / Appendix | System demonstration screenshots |

> **Research Priority in This Doc:** Phases 48–53 are production infrastructure. Their value for the paper is primarily in **§6 (System Implementation and Operational Fitness)**. Focus on Phase 51 (model registry) and Phase 52 (alerts) first — they directly demonstrate the Champion/Challenger governance policy and the end-to-end detection pipeline that the paper describes. The dashboard phases (P54–55) come last.

---

---

## Phase 48 — Events Module

**Context:** The front door of the XAI-Guard system. Receives, validates, deduplicates, stores, and queues all incoming security events. Every correctness requirement here is safety-critical — missed events mean missed detections.


### 🎓 What You Will Learn in Phase 48
You will build the entry point of the entire XAI-Guard production system. Every security event flows through the events module: validation → deduplication → storage → queuing. This teaches you: async FastAPI patterns, Redis deduplication with pipelines, PostgreSQL bulk insert, and Redis Streams as a durable message queue.

### 📄 Research Paper Connection
Phase 48 → **§6 System Architecture**: "Security events are ingested via POST /v1/events/ingest (accepting up to 1000 events per batch). Events are deduplicated using a 5-minute SHA-256 hash window before storage and prediction queuing."

### 📖 Concept: Why Redis Streams over Kafka for This Project?
Kafka is the industry standard for high-throughput streaming, but requires a ZooKeeper or KRaft cluster (operational complexity). Redis Streams provide similar guarantees (durable, consumer-group acknowledgement, pending-entries for replay) with zero additional infrastructure — Redis is already in the stack for deduplication and caching.

**In your paper:** "We use Redis Streams for event queueing. Events persist in the stream until explicitly acknowledged by the prediction worker, ensuring zero event loss even if the prediction service restarts."

#### Subphase 48.1 — Event Ingestion Endpoint

> **🎭 Role:** Senior Backend Engineer specialising in high-throughput API design
> **📍 Context:** The events module receives security events from SIEMs, network sensors, and agent collectors. A single endpoint handles both individual and bulk ingestion using batch processing for efficiency.
> **🔧 Task:** Implement `POST /v1/events/ingest`. Accept `BatchEventRequest` (list of `SecurityEventInput`, max 1000 items, Pydantic v2 `model_config extra="forbid"`). Pipeline: (1) validate all events via Pydantic; (2) compute SHA-256 deduplication hash per event; (3) batch Redis `MGET` for existing hashes; (4) bulk insert accepted events to PostgreSQL using `insert().values([...]).on_conflict_do_nothing()` returning IDs; (5) batch `XADD events:pending` to Redis Stream for each accepted event; (6) return `BatchIngestionResponse(accepted_count, duplicate_count, error_count, accepted_event_ids)` serialised with `orjson`.
> **📦 Stack:** FastAPI 0.111, SQLAlchemy 2 async, asyncpg, redis[asyncio] 5.x, orjson, pydantic v2
> **✅ Outcome:** `POST /v1/events/ingest` with 100 events completes in under 50ms P50. Duplicate events are counted correctly. The Redis Stream contains exactly `accepted_count` new entries.

#### Subphase 48.2 — Deduplication Service

> **🎭 Role:** Senior Backend Engineer
> **📍 Context:** Event deduplication prevents the same network flow from generating multiple alerts when multiple sensors report the same connection. The hash must be deterministic, collision-resistant, and computed in O(1).
> **🔧 Task:** Implement `services/api/events/deduplication.py`. `EventDeduplicator` class. `compute_hash(event: SecurityEventInput) -> str`: `sha256(f"{event.source_ip}|{event.destination_ip}|{int(event.timestamp.timestamp())}|{event.protocol}").hexdigest()`. `async def check_and_mark_duplicates(hashes: list[str], redis: AsyncRedis, ttl_seconds: int = 300) -> list[bool]`: pipeline a `MGET` for all hashes in one round-trip; pipeline `SET key 1 NX PX {ttl_ms}` for all non-existing hashes in a second round-trip; return bool list where True = duplicate. Total: exactly 2 Redis round-trips regardless of batch size. Write unit tests for hash determinism (same input → same hash) and pipeline round-trip count.
> **📦 Stack:** redis[asyncio] 5.x, hashlib (stdlib), pytest-asyncio
> **✅ Outcome:** Two identical events produce identical hashes. `check_and_mark_duplicates` uses exactly 2 Redis round-trips for any batch size.

#### Subphase 48.3 — Event Storage Service

> **🎭 Role:** Senior Backend Engineer with PostgreSQL bulk insert expertise
> **📍 Context:** Events arrive in bulk. Row-by-row insertion would be too slow and create excessive database round-trips. Bulk insert with conflict resolution is the correct pattern for this workload.
> **🔧 Task:** Implement `services/api/events/storage.py`. `EventStorageService.bulk_insert(events: list[SecurityEventInput], db: AsyncSession) -> list[UUID]`. Use `insert(SecurityEvent).values([event_to_dict(e) for e in events]).on_conflict_do_nothing(index_elements=["dedup_hash"]).returning(SecurityEvent.id)`. Return the list of inserted IDs (excluding conflicts). Handle `asyncpg.exceptions.PostgresError` by rolling back the session and raising `ServiceUnavailableException`. Log: inserted count, conflict count, and bulk insert duration to structlog with `structlog.stdlib.BoundLogger`.
> **📦 Stack:** SQLAlchemy 2 async, asyncpg, structlog
> **✅ Outcome:** `bulk_insert(1000_events)` completes in under 200ms. Database conflicts are counted and logged, not raised as exceptions.

#### Subphase 48.4 — Redis Stream Publishing

> **🎭 Role:** Senior Backend Engineer with Redis Streams expertise
> **📍 Context:** Redis Streams provide durable, consumer-group-based message delivery. Messages survive a Redis restart (unlike pub/sub) and are acknowledged after successful processing, ensuring no event is lost.
> **🔧 Task:** Implement `services/api/events/queue.py`. `EventQueuePublisher.publish_batch(event_ids: list[UUID], redis: AsyncRedis) -> None`: pipeline `XADD events:pending * event_id {uuid} timestamp {iso}` for each event in a single pipeline batch. Create consumer group `predictions_worker` on stream `events:pending` using `XGROUP CREATE ... MKSTREAM` if it does not exist. `async def acknowledge(stream_id: str, redis: AsyncRedis)`: sends `XACK events:pending predictions_worker {stream_id}`. Write an integration test that publishes 10 events, reads them via `XREADGROUP`, acknowledges them, and verifies `XLEN` returns 0 pending.
> **📦 Stack:** redis[asyncio] 5.x, pytest-asyncio
> **✅ Outcome:** Published events are durably stored in the Redis Stream. Consumer group ACK correctly removes entries from the pending-entries list.

#### Subphase 48.5 — Events Module Tests

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** The events module is the entry point for all data. Comprehensive tests cover correctness, edge cases, and failure modes — all must pass before any downstream module is built.
> **🔧 Task:** Write `services/api/tests/events/test_ingestion.py`. Test: (1) valid batch of 100 events returns `accepted_count=100`; (2) batch with 50% duplicates returns `duplicate_count=50`; (3) batch exceeding 1000 items returns 422 ProblemDetail; (4) event with invalid IP format returns 422 with field-level error; (5) database failure returns 503; (6) empty batch returns 422; (7) Redis Stream contains exactly `accepted_count` new entries after ingestion; (8) re-ingesting the same batch after TTL expiry creates new events. Use `factory-boy` for `SecurityEventInput` fixtures and an in-memory test database.
> **📦 Stack:** pytest-asyncio, httpx, factory-boy, faker
> **✅ Outcome:** All 8 events module tests pass. Test 7 (stream count verification) directly verifies the queueing behaviour.

---

## Phase 49 — Predictions Module

**Context:** The performance-critical hot path. Loads the Champion model, runs the feature pipeline, makes predictions, and dispatches async explanation generation — all within a P99 ≤ 100ms budget.


### 🎓 What You Will Learn in Phase 49
The prediction endpoint is the hottest path in the entire system — every security event passes through it. You will learn: how to load ML models into API memory at startup, hot-reload without downtime, feature caching to reduce computation, and the fire-and-forget pattern for async SHAP generation.

### 📄 Research Paper Connection
Phase 49 → **§6 Operational Fitness (Table 6, "API overhead" row)**: "The end-to-end prediction latency (event ingestion → prediction response, measured at P99) was X ms. Feature engineering contributes Y ms; model inference Z ms; async SHAP dispatch is non-blocking."

### 📖 Concept: Fire-and-Forget for XAI (Why Not Compute SHAP Synchronously?)
SHAP computation takes 1–5 seconds per prediction (for TreeExplainer on a trained XGBoost with 50 features). If you computed SHAP synchronously in the prediction endpoint, your P99 latency would exceed 5 seconds — violating the 100ms production budget and making the system unusable for real-time detection.

Fire-and-forget pattern:
1. Prediction endpoint returns response in <100ms
2. `asyncio.create_task(dispatch_shap_celery_task(prediction_id))` — non-blocking dispatch
3. SHAP runs in a Celery worker (separate process) while the analyst already sees the alert
4. When SHAP finishes (5–30 seconds later), it updates the database and pushes to WebSocket

**In your paper:** "Explanation generation is asynchronous. The prediction endpoint dispatches a Celery task and returns immediately. Analysts receive the alert in under 100ms P99; SHAP explanations appear within 30 seconds via WebSocket push."

#### Subphase 49.1 — Champion Model Loading Service

> **🎭 Role:** Senior ML Platform Engineer
> **📍 Context:** The prediction endpoint must serve the current Champion model at low latency. The model is loaded into memory on startup and hot-swapped atomically when a new Champion is promoted, without dropping any in-flight requests.
> **🔧 Task:** Implement `services/api/predictions/model_service.py`. `ChampionModelService` singleton initialised in the FastAPI application lifespan. `async def load_champion()`: queries the model registry DB for the current CHAMPION `ModelVersion`, downloads artifacts from MLflow via `mlflow.artifacts.download_artifacts`, loads preprocessing pipeline with `joblib.load`, loads feature list from config. `async def hot_reload()`: background `asyncio.Task` polling the registry every 60 seconds; if the Champion version changes, downloads new artifacts into a staging slot, swaps atomically using a `threading.Lock`. Log all loads and hot-reloads to structlog.
> **📦 Stack:** mlflow 2.14, joblib, asyncio, threading, structlog
> **✅ Outcome:** Application startup loads the Champion model. Hot-reload swaps the model without raising errors on concurrent in-flight predictions.

#### Subphase 49.2 — Prediction Endpoint

> **🎭 Role:** Senior Backend Performance Specialist
> **📍 Context:** The prediction endpoint is the busiest in the system. The full pipeline — feature engineering, Redis cache check, inference, async dispatch — must complete within 100ms P99.
> **🔧 Task:** Implement `POST /v1/predictions/predict`. Accept `SecurityEventInput` (single event). Execution order: (1) compute feature cache key; (2) check Redis feature cache; (3) on miss: run feature engineering pipeline; (4) run `ChampionModelService.predict_proba(features)`; (5) map confidence to severity using configurable thresholds; (6) `asyncio.create_task(store_prediction_async(data, db))` — fire and forget; (7) dispatch SHAP Celery task `apply_async(args=[prediction_id], queue="explanations")`; (8) if Challenger active, dispatch shadow inference Celery task. Return `PredictionResponse(prediction_id, attack_type, confidence, severity, inference_latency_ms, model_version)` using `orjson`.
> **📦 Stack:** FastAPI 0.111, Celery 5.x, redis[asyncio], asyncio, orjson, msgspec
> **✅ Outcome:** `POST /v1/predictions/predict` returns `PredictionResponse` in under 100ms P99 measured across 5000 production-representative calls.

#### Subphase 49.3 — Redis Feature Cache

> **🎭 Role:** Senior Backend Engineer
> **📍 Context:** Feature engineering is the most compute-intensive step in the prediction pipeline. Caching processed feature vectors eliminates redundant computation for repeated source IPs — common during sustained attacks.
> **🔧 Task:** Implement `services/api/predictions/feature_cache.py`. `FeatureCache.get_or_compute(event: SecurityEventInput, pipeline, redis: AsyncRedis) -> tuple[np.ndarray, bool]`. Cache key: `sha256(event.model_dump_json())`. On cache miss: compute features, encode with `msgspec.json.encode`, store with `SET key data EX 60`. On hit: decode and return. Track hit/miss with Prometheus counters: `xaiguard_feature_cache_hits_total` and `xaiguard_feature_cache_misses_total`. Log cache hit ratio to structlog every 1000 requests.
> **📦 Stack:** redis[asyncio] 5.x, msgspec, prometheus-client, numpy
> **✅ Outcome:** Cache hit rate exceeds 30% under sustained attack simulation (same source IP repeated). Prometheus shows live hit/miss ratio.

#### Subphase 49.4 — Prediction Module Tests

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** The prediction module is the most critical runtime path. Tests must verify correctness, performance contracts, caching behaviour, and graceful failure modes.
> **🔧 Task:** Write `services/api/tests/predictions/test_predict.py`. Test: (1) valid event returns `PredictionResponse` with correct schema; (2) feature cache is populated on first call and hit on second call with same event; (3) hot-reload correctly switches to new Champion version and subsequent predictions use new model; (4) SHAP Celery task is dispatched (assert `apply_async` was called); (5) invalid event payload returns 422; (6) mocked model returns response in under 200ms in CI; (7) model loading failure returns 503 and falls back to heuristic classifier. Mock all MLflow calls in tests.
> **📦 Stack:** pytest-asyncio, httpx, unittest.mock, factory-boy
> **✅ Outcome:** All 7 prediction tests pass. Test 6 is run in CI and enforces the latency contract via `assert latency < 200`.

---

## Phase 50 — Explanations Module

**Context:** XAI generation is compute-heavy and always asynchronous. Analysts request explanations and receive them via polling or WebSocket, never blocking the prediction response.

#### Subphase 50.1 — SHAP Celery Task

> **🎭 Role:** Senior ML Platform Engineer
> **📍 Context:** The SHAP Celery task runs in the dedicated `explanations` queue with 2 workers. It is the bridge between the ML and API layers — loading the correct model version and computing SHAP values for the given prediction.
> **🔧 Task:** Implement `services/api/explanations/tasks.py`. `@celery_app.task(name="explanations.shap", queue="explanations", max_retries=3, default_retry_delay=60, bind=True)`. Steps: (1) load prediction record from DB; (2) update `XAIExplanation.status = COMPUTING`; (3) load model from MLflow by `model_version_id`; (4) load event features from `SecurityEvent.features` JSON; (5) `XAIGuardSHAPExplainer().explain(model, X, feature_names)`; (6) compute stability score; (7) update `XAIExplanation` status to COMPLETE with all fields; (8) publish `explanation:ready:{prediction_id}` to Redis pub/sub. On any exception: `self.retry(exc=exc)` or, after max retries, set status to FAILED and log to Sentry.
> **📦 Stack:** Celery 5.x, mlflow 2.14, shap 0.45, SQLAlchemy 2 async, redis-py, sentry-sdk[fastapi]
> **✅ Outcome:** The task transitions the XAIExplanation record from PENDING → COMPUTING → COMPLETE. The Redis pub/sub event fires on completion.

#### Subphase 50.2 — Explanation Request & Polling Endpoints

> **🎭 Role:** Senior Backend Engineer
> **📍 Context:** Two endpoints implement the async explanation workflow: one dispatches the task (or returns a cached result), the other allows polling for the result status.
> **🔧 Task:** Implement `POST /v1/explanations/request` and `GET /v1/explanations/{task_id}`. POST accepts `ExplanationRequest(prediction_id: UUID, method: ExplanationMethod = SHAP)`. Check DB for existing explanation — if COMPLETE, return it immediately. Otherwise create `XAIExplanation(status=PENDING)`, dispatch Celery task, return `ExplanationRequestResponse(task_id, status=PENDING, estimated_seconds=30)`. GET checks Celery task state via `AsyncResult(task_id)`: PENDING/STARTED → `{"status": "processing"}`; SUCCESS → full `ExplanationUnion` from DB with `computation_time_ms` and `stability_score`; FAILURE → `{"status": "failed", "error": message}`.
> **📦 Stack:** FastAPI, Celery 5.x, SQLAlchemy 2 async, pydantic v2
> **✅ Outcome:** Requesting and polling for a SHAP explanation completes within 30 seconds on the Champion model. Re-requesting an explained prediction returns the cached result immediately.

#### Subphase 50.3 — Explanations Module Tests

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** The explanation workflow involves Celery tasks, database state transitions, and polling. Tests must verify the async lifecycle using Celery's `ALWAYS_EAGER` test mode.
> **🔧 Task:** Write `services/api/tests/explanations/test_explanations.py`. Test: (1) requesting SHAP explanation returns a task ID and creates a PENDING record; (2) polling a PENDING task returns `status="processing"`; (3) polling a COMPLETE task returns full explanation schema with `stability_score`; (4) requesting explanation for non-existent prediction returns 404; (5) re-requesting for a COMPLETE prediction returns cached result without creating a new Celery task; (6) SHAP task handles model loading failure → sets status FAILED; (7) requesting LIME explanation dispatches the LIME task, not the SHAP task. Use `CELERY_TASK_ALWAYS_EAGER=True` in test settings.
> **📦 Stack:** pytest-asyncio, httpx, Celery test utilities
> **✅ Outcome:** All 7 explanation tests pass. Test 5 (cache hit without re-dispatch) directly verifies the efficiency requirement.

---

## Phase 51 — Model Registry Module

**Context:** Owns the Champion/Challenger lifecycle. Provides management endpoints, automates nightly shadow evaluation, and enforces the multi-gate promotion policy from Phase 1.


### 🎓 What You Will Learn in Phase 51
The model registry module is the most research-relevant backend phase. It implements the Champion/Challenger governance policy from Phase 1.5 as production code. You will learn: how to expose admin-only API endpoints, how to enforce multi-gate promotion logic, and how Celery Beat schedules the nightly evaluation.

### 📄 Research Paper Connection
Phase 51 → **§4.3 Champion Selection** + **§6 Production System**:
- "The Champion model is selected via automated nightly evaluation. Promotion requires: ΔF1 ≥ 0.020, ΔROC-AUC ≥ 0.010, P99 ≤ 100ms, McNemar's p < 0.0033 (Bonferroni-corrected)."
- "In 3 months of shadow evaluation, the Champion was promoted from XGBoost v1.0 to XGBoost v2.1 after the Challenger accumulated sufficient shadow predictions."

### 📖 Concept: Why 4 Promotion Gates?
A single-gate promotion (ΔF1 > threshold) is not sufficient for a security system:
1. **ΔF1 ≥ 0.020**: Ensures the improvement is practically meaningful (not just random variance)
2. **ΔROC-AUC ≥ 0.010**: Ensures the improvement extends to ranking quality, not just threshold-specific F1
3. **P99 ≤ 100ms**: Ensures the Challenger doesn't introduce latency regression (a faster model with lower F1 is not an improvement)
4. **McNemar's test p < 0.0033**: Ensures the error patterns are statistically different (the Challenger catches cases the Champion misses, not the same errors)

A Challenger that passes all 4 gates is genuinely, reliably better. This is the methodological rigour that makes your paper's Champion selection defensible.

#### Subphase 51.1 — Registry Endpoints

> **🎭 Role:** Senior Backend Engineer and MLOps Specialist
> **📍 Context:** The registry module exposes read endpoints for the admin panel and write endpoints (admin-only) for promotion and rollback. All write operations are audited and logged.
> **🔧 Task:** Implement the model registry router at `/v1/models/`. Endpoints: `GET /` — paginated list of all ModelVersions with metrics; `GET /champion` — current Champion's full `ModelVersionResponse`; `GET /challenger` — Challenger with shadow evaluation progress; `GET /history` — all `PromotionHistory` records; `POST /register` (admin) — validates MLflow run ID, creates ModelVersion, sets as CHALLENGER; `POST /promote` (admin) — promotes Challenger to Champion with `promotion_reason`, logs to AuditLog, triggers `ChampionModelService.hot_reload()`; `POST /rollback` (admin) — reverts to previous Champion from PromotionHistory, logs to AuditLog. All writes require `Depends(require_admin)`.
> **📦 Stack:** FastAPI, SQLAlchemy 2 async, mlflow 2.14, pydantic v2
> **✅ Outcome:** `POST /v1/models/promote` without admin JWT returns 403. Successful promotion creates an AuditLog record and triggers hot-reload.

#### Subphase 51.2 — Nightly Evaluation Celery Task

> **🎭 Role:** Senior MLOps Engineer
> **📍 Context:** The nightly evaluation is the heart of Champion/Challenger automation. It uses shadow predictions collected during the day to compute real-world performance comparisons without requiring ground-truth labels on live traffic.
> **🔧 Task:** Implement `services/api/models/tasks.py`. `@celery_app.task(name="models.nightly_evaluation")` scheduled via Celery Beat at `0 2 * * *` (02:00 UTC). Steps: (1) query DB for shadow predictions from the last 24h that have ground-truth labels; (2) compute F1 macro and ROC-AUC for Champion and Challenger on the same event set; (3) check all four promotion gates: ΔF1 ≥ 0.020 AND ΔROC-AUC ≥ 0.010 AND Challenger P99 ≤ 100ms (from LatencyProfiler) AND McNemar's test p < 0.05; (4) if all gates pass, call the promotion service; (5) store results in `ModelEvaluation` table; (6) log all metrics and gate results to structlog.
> **📦 Stack:** Celery 5.x, SQLAlchemy 2 async, sklearn 1.5, statsmodels
> **✅ Outcome:** The nightly task runs at 02:00 UTC. Auto-promotion fires only when all four gates pass simultaneously.

#### Subphase 51.3 — Registry Module Tests

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** Registry bugs silently cause model degradation. The promotion gate logic is particularly critical — tests must verify each gate independently.
> **🔧 Task:** Write `services/api/tests/models/test_registry.py`. Test: (1) registering a valid MLflow run creates a ModelVersion record; (2) nightly evaluation with ΔF1=+0.025 and all gates passing triggers auto-promotion; (3) nightly evaluation with ΔF1=+0.025 but Challenger P99=150ms does NOT promote (latency gate failure); (4) nightly evaluation with ΔF1=+0.025 and ΔF1 passing but McNemar p=0.12 does NOT promote (significance gate failure); (5) rollback reverts to the previous Champion from history; (6) analyst JWT returns 403 on `POST /promote`; (7) promoting a model not in CHALLENGER status returns 422.
> **📦 Stack:** pytest-asyncio, httpx, factory-boy, statsmodels
> **✅ Outcome:** All 7 registry tests pass. Tests 3 and 4 each isolate a single gate failure to verify the AND logic.

---

## Phase 52 — Alerts & WebSocket Module

**Context:** Real-time alert delivery to analysts is the primary analyst-facing feature. The module creates, deduplicates, manages alert state, and broadcasts via WebSocket.


### 🎓 What You Will Learn in Phase 52
The alerts module closes the loop from event ingestion to analyst notification. You will learn WebSocket connection management — keeping thousands of concurrent connections alive and broadcasting alert messages to all connected analysts in real-time.

### 📄 Research Paper Connection
Phase 52 → **§6**: "Alert delivery latency (event ingestion → analyst notification) was measured at P99=Xms, meeting the SLO of ≤10 seconds. Alerts are pushed via WebSocket to all connected analyst dashboards simultaneously."

### 📖 Concept: WebSocket vs REST Polling
REST polling: analyst's browser sends `GET /v1/alerts?since=last_timestamp` every N seconds. Problems: N-second delay before analyst sees critical alert; N×(analyst count) requests/second, even when there are no new alerts.

WebSocket: persistent bidirectional connection. Server pushes new alert to all connected analysts immediately when it is created. No delay, no unnecessary requests. For a security dashboard where analysts need to see CRITICAL alerts in seconds, WebSocket is the correct choice.

#### Subphase 52.1 — Alert Creation & Deduplication Service

> **🎭 Role:** Senior Backend Engineer
> **📍 Context:** Alerts are created after every CRITICAL or HIGH severity prediction. Without deduplication, a sustained DDoS attack generates thousands of identical alerts, causing analyst fatigue and missing the signal in the noise.
> **🔧 Task:** Implement `services/api/alerts/alert_service.py`. `AlertService.create_or_increment(prediction: Prediction, db: AsyncSession, redis: AsyncRedis) -> Alert`: (1) compute `dedup_key = sha256(f"{prediction.source_ip}|{prediction.attack_type}")` as hex; (2) query DB for an unacknowledged alert with the same dedup_key created in the last 5 minutes; (3) if found: `UPDATE alerts SET alert_count += 1, last_seen_at = now() WHERE id = {id}` using `with_for_update(skip_locked=True)`; (4) if not found: create new Alert with MITRE mapping from the threat intel module; (5) publish the alert to Redis pub/sub channel `xaiguard:alerts:live` for WebSocket forwarding using `orjson.dumps`.
> **📦 Stack:** SQLAlchemy 2 async, redis[asyncio] 5.x, structlog, hashlib, orjson
> **✅ Outcome:** A 60-second sustained DDoS attack generates 1 alert with incrementing count, not separate alerts per event.

#### Subphase 52.2 — Alert Management Endpoints

> **🎭 Role:** Senior Backend Engineer
> **📍 Context:** Analysts need to view, filter, sort, and acknowledge alerts efficiently. The endpoint supports all analyst UI use cases using cursor-based pagination for performance at scale.
> **🔧 Task:** Implement alerts router at `/v1/alerts/`. `GET /` with query params: `severity: list[Severity] | None`, `acknowledged: bool | None`, `attack_type: list[AttackType] | None`, `cursor: str | None`, `limit: int = 50`. Returns `CursorPage[AlertResponse]` using base64-encoded `{last_seen_at}_{id}` composite cursor. Eager-load related prediction and MITRE info using SQLAlchemy `selectinload`. `GET /{id}` returns single `AlertResponse`. `PATCH /{id}/acknowledge` sets `acknowledged=True`, `acknowledged_by=user.username` from JWT, `acknowledged_at=now()`, logs to AuditLog. All responses serialised with `orjson`.
> **📦 Stack:** FastAPI, SQLAlchemy 2 async, orjson, pydantic v2
> **✅ Outcome:** Cursor pagination returns correct page sizes. `GET /v1/alerts?severity=CRITICAL&acknowledged=false` returns only unacknowledged CRITICAL alerts.

#### Subphase 52.3 — WebSocket Connection Manager

> **🎭 Role:** Senior Backend Engineer with real-time systems expertise
> **📍 Context:** The WebSocket connection delivers alerts in real time to every connected analyst dashboard. The connection manager handles authentication, reconnection, and slow-client back-pressure.
> **🔧 Task:** Implement `services/api/alerts/websocket_manager.py`. `ConnectionManager` singleton. `connect(websocket: WebSocket, token: str) -> str`: validate JWT via `JWTService.verify_access_token`; close with code 4001 if invalid; store connection in `dict[str, WebSocket]`; start background `asyncio.Task` `_listen_redis(connection_id, redis)`. `_listen_redis`: subscribes to `xaiguard:alerts:live` using `redis.asyncio.PubSub`; on each message, parse with `AlertWebSocketMessageSchema`, send to client; discard message if send takes > 100ms (slow client protection). `disconnect(connection_id)`: remove from registry, cancel listener task.
> **📦 Stack:** FastAPI WebSockets, redis[asyncio] 5.x, asyncio, orjson
> **✅ Outcome:** Authenticated WebSocket client receives a CRITICAL alert within 2 seconds of a prediction being processed. Invalid JWT closes with code 4001 immediately.

#### Subphase 52.4 — Alerts Module Tests

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** WebSocket testing requires starlette's test client. The alert deduplication logic is the most important correctness requirement.
> **🔧 Task:** Write `services/api/tests/alerts/test_alerts.py`. Test: (1) CRITICAL prediction creates an Alert record; (2) second CRITICAL from same IP within 5 minutes increments `alert_count` rather than creating a new Alert; (3) `PATCH /alerts/{id}/acknowledge` sets `acknowledged=True` with the correct `acknowledged_by` username; (4) `GET /alerts?severity=CRITICAL` returns only CRITICAL alerts; (5) WebSocket connection with invalid JWT closes with code 4001; (6) WebSocket client receives an alert within 2 seconds in a controlled test pipeline; (7) cursor pagination returns correct page sizes.
> **📦 Stack:** pytest-asyncio, httpx, starlette.testclient WebSocket support
> **✅ Outcome:** All 7 alerts tests pass. Test 2 (deduplication increment) is the safety-critical test.

---

## Phase 53 — Threat Intelligence Module

**Context:** Replaces Phase 21 stubs with live integrations. Enriches every prediction with IP reputation, Tor exit node detection, and MITRE ATT&CK technique mapping from the definitive taxonomy.


### 🎓 What You Will Learn in Phase 53
Threat intelligence enriches predictions with context from external databases (AbuseIPDB for known malicious IPs) and the MITRE ATT&CK framework (mapping attack types to standardised technique IDs). This is what transforms a raw ML classification into an actionable security finding.

### 📄 Research Paper Connection
Phase 53 → **§1 Motivation** + **§6**: "Each prediction is enriched with MITRE ATT&CK technique mappings, grounding the ML classification in the structured threat knowledge base used by enterprise SOC teams."

The MITRE mapping table (PortScan → T1046, BruteForce → T1110, DDoS → T1498) demonstrates that your attack taxonomy aligns with the industry-standard threat taxonomy — a point reviewers will appreciate.

#### Subphase 53.1 — AbuseIPDB & Tor Integration

> **🎭 Role:** Senior Backend Engineer with external API integration expertise
> **📍 Context:** AbuseIPDB provides IP confidence scores (0-100 abuse confidence). Tor exit node detection uses a Redis Set populated by a daily Celery Beat task. Both must be cache-first to add zero latency to the 100ms prediction budget.
> **🔧 Task:** Implement `services/api/threat_intel/ip_reputation.py`. `AbuseIPDBClient(api_key: str, client: AsyncClient)`: `async def check(ip: str) -> IPReputationResult` — check Redis cache first (key=`abuseipdb:{ip}`, TTL=3600s); on miss call `https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=30` with `tenacity.retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))`; cache with `msgspec.json.encode`. `TorExitNodeChecker`: `async def is_exit_node(ip: str) -> bool` — `SISMEMBER tor:exit_nodes {ip}`. Daily Celery Beat task: download TorDNSEL from `https://check.torproject.org/exit-addresses`, parse, `DEL tor:exit_nodes` and `SADD tor:exit_nodes ...` atomically in a pipeline.
> **📦 Stack:** httpx, tenacity, redis[asyncio] 5.x, msgspec, Celery 5.x, pydantic v2
> **✅ Outcome:** Second call for the same IP hits Redis cache with zero HTTP calls. Tor Set lookup is O(1). Daily task rebuilds the Tor exit node list.

#### Subphase 53.2 — MITRE ATT&CK Mapping

> **🎭 Role:** Cybersecurity Engineer
> **📍 Context:** Every alert displayed to an analyst must include the MITRE ATT&CK technique ID, name, tactic, and a link to the official documentation. The mapping is loaded at startup from a static config — no network call.
> **🔧 Task:** Implement `services/api/threat_intel/mitre_mapping.py`. `MITRE_MAPPING: dict[AttackType, MITREInfo]` with complete data for all 6 taxonomy classes: `DDOS → T1499.001 (Endpoint DoS: OS Exhaustion Flood, TA0040 Impact)`, `PORT_SCAN → T1046 (Network Service Discovery, TA0007 Discovery)`, `BRUTE_FORCE → T1110 (Brute Force, TA0006 Credential Access)`, `BOTNET → T1571 (Non-Standard Port, TA0011 C2)`, `WEB_ATTACK → T1190 (Exploit Public-Facing Application, TA0001 Initial Access)`, `INFILTRATION → T1078 (Valid Accounts, TA0001 Initial Access)`. `MITREInfo` Pydantic model: `technique_id`, `technique_name`, `tactic_id`, `tactic_name`, `attack_url` (pattern: `https://attack.mitre.org/techniques/T{id}/`). `get_mitre_info(attack_type) -> MITREInfo` raises `ResourceNotFoundException` for unknown attack types.
> **📦 Stack:** pydantic v2, Python StrEnum
> **✅ Outcome:** `get_mitre_info(AttackType.DDOS)` returns `technique_id="T1499.001"`. The URL correctly links to the ATT&CK framework page.

#### Subphase 53.3 — Threat Intel Module Tests

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** External API calls must be mocked in all tests to avoid network dependencies, API quota consumption, and test flakiness.
> **🔧 Task:** Write `services/api/tests/threat_intel/test_threat_intel.py` using `respx` to mock HTTP calls. Test: (1) AbuseIPDB returns cached result on second call for same IP — zero HTTP calls made; (2) Tor exit node IP returns True from Redis Set; (3) non-Tor IP returns False; (4) MITRE mapping returns correct technique for all 6 attack types; (5) AbuseIPDB client retries exactly 3 times on HTTP 429 from the external API; (6) daily Tor update task rebuilds the Redis Set with the new list; (7) unknown attack type raises `ResourceNotFoundException`.
> **📦 Stack:** pytest-asyncio, respx, factory-boy
> **✅ Outcome:** All 7 threat intel tests pass with zero real HTTP calls. Test 5 verifies retry logic without network access.

---

## Phase 54 — Security Dashboard Foundation & Layout

**Context:** The Next.js 14 App Router security analyst dashboard. Dark-mode-first, real-time, and purpose-built for SOC environments with persistent colour-coded severity signals.


### 🎓 What You Will Learn in Phases 54–55
You will build the analyst-facing dashboard that makes the entire system visible and usable. This teaches you: Next.js 14 App Router with RSC, TanStack Query for async data, Recharts for analytical data visualisation, and Tailwind CSS with shadcn/ui for Swiss + Minimalist enterprise UI (see `docs/design.md` for the full design system specification).

### 📄 Research Paper Connection
Phases 54–55 → **§6 + Appendix**: System demonstration screenshots. Include in your paper:
1. The main dashboard showing CRITICAL alerts feed (demonstrates end-to-end detection)
2. An alert detail view showing the SHAP waterfall chart (demonstrates XAI integration)
3. The model comparison view showing Table 4 inline (demonstrates the research connection)

**In your paper appendix:** "Figure A1: XAI-Guard analyst dashboard. Figure A2: Alert detail with SHAP explanation. Figure A3: Model comparison view showing Champion/Challenger status."

These screenshots, combined with the system description in §6, show that your research produced a deployable system — not just offline notebook experiments.

### 📖 Concept: Why a Real Dashboard Matters for a Research Paper
Most IDS papers present only offline evaluation results (Table of F1 scores + some XAI plots). Building a live system that serves real-time predictions via a production-grade dashboard demonstrates:
1. **Practical deployability** — the research is not just academic
2. **End-to-end integration** — all six models, XAI, and the Champion/Challenger policy work together
3. **Analyst-centred design** — the XAI explanations are actually surfaced to end users, not just computed

This is a meaningful contribution that separates your paper from "yet another IDS benchmark paper."

#### Subphase 54.1 — App Setup, Theme & Global Styles

> **🎭 Role:** Senior Frontend Engineer and Design Systems Architect
> **📍 Context:** The security dashboard is used in dark SOC environments 24/7. Every component inherits from the dark-mode-first design system. The theme is never user-changeable — SOC requirements mandate dark.
> **🔧 Task:** Set up `apps/web/` as Next.js 14 App Router. Configure Tailwind CSS with custom CSS variables for the SOC dark palette: `--critical: 0 72% 51%`, `--high: 27 96% 61%`, `--medium: 48 96% 53%`, `--low: 213 97% 67%`, `--background: 222 47% 6%`, `--card: 222 47% 9%`. Configure `next-themes` with `defaultTheme="dark"`, `forcedTheme="dark"` (no user toggle). Set up `cn(...)` utility from `packages/ui/src/utils/cn.ts` using `clsx + tailwind-merge`. Configure `tsconfig.json` with `exactOptionalPropertyTypes: true`, `noUncheckedIndexedAccess: true`. Enable `experimental.typedRoutes: true` in `next.config.ts`.
> **📦 Stack:** Next.js 14, Tailwind CSS v3, next-themes, clsx, tailwind-merge, CVA, TypeScript 5
> **✅ Outcome:** `pnpm dev --filter=web` starts the dashboard in dark mode. All severity CSS variables render correctly in components. Type-safe routes prevent invalid `href` values.

#### Subphase 54.2 — Authentication Guard Middleware

> **🎭 Role:** Senior Full-Stack Engineer
> **📍 Context:** All dashboard routes require a valid, non-expired JWT. Next.js middleware intercepts all requests before they reach route handlers, providing a universal auth guard with zero per-route configuration.
> **🔧 Task:** Implement `apps/web/middleware.ts`. Read `access_token` cookie. Decode the JWT payload using `atob(token.split('.')[1])` (client-safe, no signature verification — the API verifies signatures). Check the `exp` claim: if expired or missing, redirect to `/login?next={encoded_path}`. Apply to all paths except `/login`, `/api/auth/**`, `/_next/**`, `/favicon.ico`. Implement `apps/web/app/(auth)/login/page.tsx`: React Hook Form v7 + Zod schema `{username: z.string().min(3), password: z.string().min(8)}`, calls `POST /v1/auth/login`, stores `access_token` as HttpOnly cookie via a Next.js Server Action, redirects to the `next` param.
> **📦 Stack:** Next.js 14 Middleware, React Hook Form v7, Zod v3, shadcn/ui Input + Button
> **✅ Outcome:** An expired JWT redirects to `/login?next=/`. Successful login sets the cookie and redirects. The login form shows field-level validation errors.

#### Subphase 54.3 — Root Layout & Navigation Sidebar

> **🎭 Role:** Senior Frontend Engineer
> **📍 Context:** The sidebar is a React Server Component that reads the user's role from the JWT cookie server-side — no client-side decoding needed for this render. The collapse state is client-side only, managed by Zustand.
> **🔧 Task:** Implement `apps/web/app/(dashboard)/layout.tsx` as a React Server Component. Renders: left sidebar with navigation links (Live Alerts `/`, Threat Details, Metrics, Model Status), user info block (username + role badge decoded from JWT cookie server-side), logout Server Action (clears cookie, redirects), `<ModelStatusBar>` client boundary. Implement the sidebar collapse: `usePreferencesStore().sidebarCollapsed` from Zustand `immer` middleware store; toggle button triggers collapse; Framer Motion `AnimatePresence` with `initial={false}` and `exit={{ width: 0 }}` for smooth animation.
> **📦 Stack:** Next.js 14 RSC + Server Actions, Zustand v4 + immer, Framer Motion v11, Lucide React
> **✅ Outcome:** Sidebar renders with correct user info on server. Collapse animation is smooth (60fps). Navigation links show active state using `usePathname()`.

#### Subphase 54.4 — API Client & TanStack Query Hooks

> **🎭 Role:** Senior React Engineer
> **📍 Context:** All data fetching uses TanStack Query hooks with Zod-validated fetchers. The `nuqs` library synchronises filter state with URL search params, making alert filters bookmarkable.
> **🔧 Task:** Implement dashboard-specific TanStack Query hooks in `apps/web/lib/queries/`. `useAlerts(filters: AlertFilters)`: fetches `/v1/alerts` with filter params; uses `nuqs` `useQueryStates` for URL synchronisation; `staleTime: 10_000`. `useExplanation(taskId: string)`: polls `/v1/explanations/{taskId}` every 2s with `refetchInterval: (data) => data?.status === "processing" ? 2000 : false`. `useModels()`: fetches champion + challenger; `staleTime: 30_000`. `useMetrics()`: `refetchInterval: 30_000`. Each hook uses a `zodFetcher<Schema>(url, schema)` utility that calls `schema.parse(await res.json())` and throws `ZodError` on mismatch.
> **📦 Stack:** @tanstack/react-query v5, nuqs, Zod v3
> **✅ Outcome:** `useExplanation` stops polling automatically when status changes to `"complete"` or `"failed"`. Alert filters in the URL survive browser refresh.

#### Subphase 54.5 — WebSocket Client Context

> **🎭 Role:** Senior React Engineer with real-time systems expertise
> **📍 Context:** The WebSocket connection is a singleton per browser tab. A React context provides connection state and live messages to all consumer components without prop drilling.
> **🔧 Task:** Implement `apps/web/contexts/websocket-context.tsx`. `WebSocketProvider` wraps the authenticated layout. Uses `reconnecting-websocket` with `maxReconnectionDelay: 10_000`, `minReconnectionDelay: 1_000`, `reconnectionDelayGrowFactor: 1.3`. On `message`: parse with `AlertWebSocketMessageSchema.safeParse(JSON.parse(e.data))`; on parse success, call `useWebSocketStore.getState().pushAlert(alert)` and increment `unreadCount`. `useWebSocketStore` (Zustand with `immer`): `status: "connecting"|"connected"|"disconnected"`, `alerts: AlertResponse[]` (max 100, FIFO), `unreadCount: number`, `clearUnread()`. Expose `useWebSocket()` hook.
> **📦 Stack:** reconnecting-websocket, Zustand v4 + immer, Zod v3
> **✅ Outcome:** WebSocket reconnects automatically. `unreadCount` increments correctly. `clearUnread()` resets without losing the alerts array.

---

## Phase 55 — Alert Feed & Threat Detail Components

**Context:** The primary analyst workflow: real-time alert feed → click alert → threat detail card with XAI explanation. Performance and UX correctness here directly affects SOC response time.

#### Subphase 55.1 — AlertsFeed with TanStack Virtual

> **🎭 Role:** Senior React Performance Engineer
> **📍 Context:** The alert feed accumulates thousands of alerts during sustained attacks. TanStack Virtual renders only visible rows, keeping the feed at 60fps regardless of total item count.
> **🔧 Task:** Implement `apps/web/components/alerts/AlertsFeed.tsx` as a Client Component. Merge data from `useAlerts()` (server-persisted) with `useWebSocketStore().alerts` (real-time buffer). Use `@tanstack/react-virtual useVirtualizer(items, { estimateSize: () => 56, overscan: 5 })`. Auto-scroll logic: if `scrollOffset < 200`, scroll to top on new WebSocket alerts; otherwise show a Framer Motion `AnimatePresence` floating pill `"↑ {count} new alerts"` that scrolls to top on click. Each row: `SeverityBadge`, attack type icon (Lucide), source IP (monospace), confidence %, `formatDistanceToNow(alert.created_at, { addSuffix: true })`. Row click: `useAlertsStore.getState().setSelectedAlertId(alert.id)`.
> **📦 Stack:** @tanstack/react-virtual v3, Framer Motion v11, Lucide React, date-fns v3, Zustand v4
> **✅ Outcome:** Feed renders 10,000 alerts without jank (verified with React DevTools Profiler: render time < 16ms). Auto-scroll works correctly.

#### Subphase 55.2 — SeverityBadge Component

> **🎭 Role:** Design Systems Engineer
> **📍 Context:** The SeverityBadge is the highest-frequency rendered component. It must be accessible, visually distinct under all lighting conditions, and use CSS-only animation to avoid JavaScript runtime cost.
> **🔧 Task:** Implement `packages/ui/src/components/severity-badge.tsx` using CVA. Variants by severity: `critical` — `animate-pulse bg-red-600 text-white`; `high` — `bg-orange-500 text-white`; `medium` — `bg-yellow-500 text-black`; `low` — `bg-blue-600 text-white`; `normal` — `bg-slate-600 text-white`. ARIA: `role="status"`, `aria-label={severity + " severity"}}`. Props: `severity: Severity`, `size: "sm"|"md"|"lg"` (controls `text-xs|text-sm|text-base` and `px-1.5|px-2|px-3`). No hooks — pure server component. Export from `packages/ui/src/index.ts`.
> **📦 Stack:** CVA (class-variance-authority), Tailwind CSS v3, TypeScript 5
> **✅ Outcome:** `<SeverityBadge severity="critical" />` renders with pulsing red and correct `aria-label`. Component passes all Storybook a11y checks.

#### Subphase 55.3 — ThreatDetailPanel

> **🎭 Role:** Senior Frontend Engineer with security domain knowledge
> **📍 Context:** The ThreatDetailPanel is the centrepiece of the analyst workflow. It shows everything an analyst needs to understand and respond to a threat in one view, without switching context.
> **🔧 Task:** Implement `apps/web/components/alerts/ThreatDetailPanel.tsx` using shadcn/ui `Sheet` (slide from right). Triggered when `useAlertsStore().selectedAlertId !== null`. Fetches `useAlert(selectedAlertId)`. Sections: (1) header — attack type icon + name + `SeverityBadge` + confidence %; (2) source IP + destination IP with copy-to-clipboard (shadcn/ui `Button` + `navigator.clipboard.writeText`); (3) **Why this alert?** — `FeatureContributionBars` component with top-4 SHAP features; (4) **Recommended Actions** — numbered list from MITRE recommended_actions field; (5) **MITRE ATT&CK** — `MITREBadge`; (6) **XAI Details** link → `/alerts/{id}/xai`; (7) **Acknowledge** button — `useMutation` on `PATCH /v1/alerts/{id}/acknowledge` with optimistic update.
> **📦 Stack:** shadcn/ui Sheet, @tanstack/react-query v5 useMutation, Lucide React
> **✅ Outcome:** Panel slides in within 200ms. Acknowledge button shows optimistic `acknowledged` state immediately.

#### Subphase 55.4 — FeatureContributionBars Component

> **🎭 Role:** Senior Frontend Data Visualisation Engineer
> **📍 Context:** The SHAP feature contribution bars are the primary XAI output that analysts read. They must be immediately interpretable without statistical training, using colour and size to convey the information.
> **🔧 Task:** Implement `packages/ui/src/components/feature-contribution-bar.tsx`. Props: `contributions: FeatureContribution[]` (top 4 items). For each contribution: left column — feature name truncated to 20 chars with shadcn/ui `Tooltip` showing the full name on hover; middle column — horizontal bar with `width = (Math.abs(shap_value) / maxAbsSHAP) * 100 + "%"`, `backgroundColor` is `#EF4444` if SHAP value > 0 (increases threat confidence) or `#3B82F6` if < 0 (decreases); right column — `{(Math.abs(shap_value) * 100).toFixed(1)}%`. Add `aria-label="Feature contribution: {name}, {direction} {pct}% impact"` on each bar.
> **📦 Stack:** shadcn/ui Tooltip, Tailwind CSS v3, CVA
> **✅ Outcome:** The top SHAP feature bar is the widest. Red bars increase threat confidence. Blue bars decrease it. Screen reader labels are descriptive.

#### Subphase 55.5 — MITREBadge & Alert Component Tests

> **🎭 Role:** Senior Frontend Test Engineer
> **📍 Context:** Component tests with React Testing Library verify correctness of critical UI components. These tests run in CI on every pull request.
> **🔧 Task:** Implement `packages/ui/src/components/mitre-badge.tsx`: renders `technique_id — technique_name` in `font-mono text-xs` with Lucide `ExternalLink` icon, clicking opens `attack_url` with `window.open(url, "_blank", "noopener,noreferrer")`. Then write `apps/web/tests/alerts.test.tsx` using React Testing Library + vitest. Test: (1) AlertsFeed renders existing alerts from `useAlerts` mock; (2) simulating a WebSocket message via the context adds an alert to the top; (3) clicking an alert sets `selectedAlertId` and renders ThreatDetailPanel; (4) SeverityBadge renders with `animate-pulse` class for CRITICAL; (5) FeatureContributionBars renders bars with widths proportional to SHAP magnitudes; (6) MITREBadge link has `rel="noopener noreferrer"`.
> **📦 Stack:** React Testing Library, vitest, @testing-library/user-event
> **✅ Outcome:** All 6 component tests pass. Tests run in under 10 seconds in CI.

---

## Phase Map

| Phase | Title | Subphases |
|-------|-------|-----------|
| P48 | Events Module | 5 |
| P49 | Predictions Module | 4 |
| P50 | Explanations Module | 3 |
| P51 | Model Registry Module | 3 |
| P52 | Alerts & WebSocket Module | 4 |
| P53 | Threat Intelligence Module | 3 |
| P54 | Dashboard Foundation & Layout | 5 |
| P55 | Alert Feed & Threat Detail | 5 |

**Previous ←** [06 — LIME, XAI Evaluation & Backend Core](06-backend-and-frontend-engineering.md) | **Next →** [08 — Admin Panel, MLOps & Production](08-production-deployment-and-roadmap.md)
