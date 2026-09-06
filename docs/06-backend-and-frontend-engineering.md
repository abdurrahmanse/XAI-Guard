# 06 — LIME, XAI Evaluation & Backend Core

> **Phases 40–47** | LIME explainability, Attention XAI, XAI stability, human-centred evaluation, robustness testing, drift detection, modular monolith core layer, and auth module.
>
> **Prompt Engineering Format:** Each subphase includes Role, Context, Task, Stack, and Outcome.

---

## Phase 40 — LIME Explainability

**Context:** LIME provides model-agnostic explanations by perturbing the input and fitting a local linear model. It is the second XAI method compared against SHAP for analyst utility.

#### Subphase 40.1 — LIME Explainer Implementation

> **🎭 Role:** Senior XAI Research Engineer
> **📍 Context:** SHAP is implemented in Phase 39. LIME uses a fundamentally different approach — perturbing inputs and fitting a local linear surrogate. It must use the same XAIGuardModel interface and return results in the same FeatureContribution schema.
> **🔧 Task:** Implement `ml/src/xai/lime_explainer.py`. `XAIGuardLIMEExplainer` with `explain(model: XAIGuardModel, X_sample: np.ndarray, feature_names: list[str], n_perturbations: int = 5000) -> LIMEExplanation`. Use `lime.lime_tabular.LimeTabularExplainer` with `mode="classification"`, `discretize_continuous=False`, and the training data distribution as background. The `feature_names` are the selected features from Phase 22. Return `LIMEExplanation` matching the Pydantic schema: feature contributions list sorted by absolute contribution descending. Measure and log computation time per explanation to MLflow.
> **📦 Stack:** lime 0.2.0.1, numpy, pydantic v2, mlflow 2.14
> **✅ Outcome:** `lime_explainer.explain(xgboost_model, X_test[0])` returns a `LIMEExplanation` in under 5 seconds. The feature contribution schema matches the Pydantic model exactly.

#### Subphase 40.2 — SHAP vs LIME Feature Ranking Correlation

> **🎭 Role:** XAI Research Scientist
> **📍 Context:** Research question RQ5 asks whether there is a measurable trade-off between prediction performance and explanation quality. The SHAP-LIME rank correlation is the primary metric for this analysis.
> **🔧 Task:** Create `ml/notebooks/xai/02_lime_shap_comparison.ipynb`. For each model family: compute SHAP and LIME explanations for 200 identical test samples. For each sample, extract the top-10 feature ranking from SHAP and LIME. Compute Spearman rank correlation between the two rankings per sample. Report mean and standard deviation of the correlation. Generate a scatter plot of SHAP contribution magnitude vs LIME contribution magnitude per feature. Log all correlation statistics to MLflow as `shap_lime_spearman_mean` and `shap_lime_spearman_std`.
> **📦 Stack:** lime, shap 0.45, scipy, matplotlib, mlflow 2.14
> **✅ Outcome:** Spearman correlations are computed for all six model families. The notebook produces a cross-method agreement table ready for the research paper.

#### Subphase 40.3 — LIME Stability Testing

> **🎭 Role:** XAI Research Engineer
> **📍 Context:** LIME is inherently stochastic — it uses random perturbations. Stability testing quantifies how much the explanation varies across repeated calls on the same input, determining whether LIME can be trusted for individual analyst decisions.
> **🔧 Task:** Extend `ml/src/xai/stability.py` with `LIMEStabilityTester`. Run LIME 10 times on the same 50 samples with different random seeds. Compute CV of feature contribution values per feature per sample. Report `lime_stability_score = 1 - mean(CV)`. Compare with SHAP stability scores. Document the threshold: `lime_stability_score > 0.90` means LIME can be trusted for analyst decisions. Fix seeds for production: the production LIME explainer always uses `random_state=42`.
> **📦 Stack:** lime, numpy, mlflow 2.14
> **✅ Outcome:** LIME stability scores are logged for all six models. The production LIME explainer uses a fixed seed and returns deterministic results.

---

## Phase 41 — Attention-Based Explainability

**Context:** For LSTM and Transformer models, attention weights provide a model-native explanation of which time steps in the event sequence the model focused on, complementing SHAP and LIME.

#### Subphase 41.1 — Attention Rollout Visualisation

> **🎭 Role:** Senior XAI Research Engineer
> **📍 Context:** Attention Rollout scores from Phase 33 indicate which events in the sequence window the Transformer focused on. Visualising as a heatmap gives analysts an intuitive sequence-level explanation of why a threat was detected.
> **🔧 Task:** Create `ml/notebooks/xai/03_attention_xai.ipynb`. Load 50 test samples with known attack labels. For each sample: run AttentionRolloutExtractor, plot rollout scores as a horizontal bar chart with event timestamp on y-axis and importance score on x-axis. Highlight the event with the highest rollout score. For BruteForce attacks, verify that the event immediately before authentication success has a high rollout score. For PortScan attacks, verify that events with high unique_dst_ports feature values have high rollout scores. Save figures as publishable PNG files.
> **📦 Stack:** torch 2.3, numpy, matplotlib
> **✅ Outcome:** The notebook produces 50 attention rollout visualisations. The analysis confirms attention focuses on semantically meaningful events.

#### Subphase 41.2 — Cross-Method Attribution Comparison

> **🎭 Role:** XAI Research Scientist
> **📍 Context:** For sequence models, SHAP, LIME, and Attention provide three different attributions at different granularities (feature-level vs timestep-level). Comparing them reveals whether they agree on what matters.
> **🔧 Task:** Add a comparison section to the attention XAI notebook. For the Transformer model, for 20 identical test samples, compute: SHAP feature importance (DeepExplainer, feature-level), LIME feature importance (tabular, feature-level), Attention Rollout timestep importance (timestep-level). Create combined analysis: do high-attention timesteps also have high SHAP feature contributions? Compute correlation between rollout score of the most recent event and the SHAP value of time-based features. Document whether the three methods reach consistent conclusions.
> **📦 Stack:** shap 0.45, lime, torch 2.3, scipy
> **✅ Outcome:** The cross-method comparison is documented. The notebook answers whether the three XAI methods agree for the Transformer model, informing the answer to RQ4.

---

## Phase 42 — XAI Stability & Cross-Method Fidelity

**Context:** XAI stability and fidelity scores constitute Pillar 2 of the evaluation framework. They determine the explanation quality ranking in the master comparison table.

#### Subphase 42.1 — XAI Pillar 2 Metrics Computation

> **🎭 Role:** XAI Research Lead
> **📍 Context:** Pillar 2 requires four metrics: SHAP stability score, LIME stability score, SHAP-LIME rank correlation, and computation time comparison. These must be computed for all six models and logged to MLflow before the comparative analysis in Phase 37.
> **🔧 Task:** Implement `ml/src/evaluation/xai_metrics.py`. `XAIPillar2Evaluator` with `evaluate(model: XAIGuardModel, X_test: np.ndarray, feature_names: list[str]) -> XAIPillar2Metrics`. Compute: `shap_stability` (from SHAPStabilityTester), `lime_stability` (from LIMEStabilityTester), `shap_lime_spearman_mean` (mean Spearman correlation across 100 samples), `shap_lime_spearman_std`, `computation_time_shap_ms` (P50 from 50 runs), `computation_time_lime_ms` (P50 from 50 runs). Return `XAIPillar2Metrics` Pydantic v2 model. Add results to `ThreePillarMetrics` Pillar 2 section. Log all metrics to MLflow.
> **📦 Stack:** shap 0.45, lime, numpy, scipy, pydantic v2, mlflow 2.14
> **✅ Outcome:** `XAIPillar2Evaluator().evaluate(model, X_test, feature_names)` returns a fully populated `XAIPillar2Metrics` for any model family. All six models have Pillar 2 results in MLflow.

---

## Phase 43 — Human-Centred XAI Evaluation

**Context:** Technical XAI metrics alone cannot determine analyst utility. The Analyst Utility Score (AUS) provides a structured framework for human evaluation that answers RQ4.

#### Subphase 43.1 — Human Evaluation Protocol Design

> **🎭 Role:** Human-Computer Interaction Researcher and XAI Evaluation Expert
> **📍 Context:** Research question RQ4 asks which XAI method is most useful for security analysts. Technical stability scores cannot answer this — only structured human evaluation can. The protocol must be rigorous enough for a peer-reviewed paper.
> **🔧 Task:** Design the XAI-Guard human evaluation protocol and write it as `docs/human-eval-protocol.md`. Cover: (1) Participant selection — 5–10 security analysts with IDS experience; (2) Scenario construction — 10 alert scenarios with known ground truth, 2 per attack class; (3) XAI presentation — SHAP waterfall chart vs LIME contribution list vs text summary; (4) Analyst tasks — (a) identify primary attack feature, (b) rate confidence 1–10, (c) choose recommended action; (5) Five sub-metrics: interpretability, completeness, actionability, trustworthiness, efficiency; (6) AUS formula: `AUS = 0.2 × (interpretability + completeness + actionability + trustworthiness + efficiency)`; (7) Statistical analysis: Wilcoxon signed-rank test to compare SHAP vs LIME AUS. Implement `AUSCalculator` in `ml/src/evaluation/human_eval.py`.
> **📦 Stack:** scipy (Wilcoxon), pandas, numpy
> **✅ Outcome:** `docs/human-eval-protocol.md` is detailed enough to run a formal user study. `AUSCalculator().compute(ratings_df)` returns a valid AUS for each XAI method.

---

## Phase 44 — Robustness Testing

**Context:** Real-world attack traffic is adversarial. Models must maintain performance when inputs are perturbed by noise or adversarial manipulation, quantifying how resistant each model is to evasion.

#### Subphase 44.1 — Gaussian Noise Robustness

> **🎭 Role:** ML Security Research Engineer with adversarial robustness expertise
> **📍 Context:** Attackers can slightly manipulate network statistics (e.g., padding packets to change byte counts) to evade detection. Gaussian noise tests approximate this evasion scenario across a range of perturbation magnitudes.
> **🔧 Task:** Implement `ml/src/evaluation/robustness.py`. `GaussianNoiseRobustnessTester(noise_levels: list[float] = [0.01, 0.05, 0.10, 0.20])`. For each noise level σ: add `N(0, σ²)` noise to each feature, clip to valid feature ranges, compute F1 macro. Plot F1 vs noise level for all six models on the same axes. Compute `R = 1 - (F1_clean - F1_sigma_0.10) / F1_clean`. Models with R > 0.95 at σ=0.10 are considered robust. Log all scores to MLflow as `robustness_score_sigma_{level}` metrics.
> **📦 Stack:** numpy, sklearn 1.5, matplotlib, mlflow 2.14
> **✅ Outcome:** Robustness curves are plotted for all six models. The XGBoost robustness score at σ=0.10 is documented as a research finding.

#### Subphase 44.2 — ART Adversarial Examples

> **🎭 Role:** ML Security Research Engineer
> **📍 Context:** IBM's Adversarial Robustness Toolbox generates principled adversarial examples that maximally reduce model confidence while making minimal feature perturbations, simulating sophisticated evasion attempts.
> **🔧 Task:** Implement ART-based adversarial testing in `robustness.py`. For XGBoost (Champion): use `art.attacks.evasion.HopSkipJump` to generate adversarial examples for 100 correctly-classified CRITICAL threat samples. Compute: success rate (proportion misclassified), mean L2 distance of perturbation, mean confidence drop. For the Transformer: use `art.attacks.evasion.FastGradientMethod`. Compare adversarial vulnerability between Champion and Challenger. Log all metrics to MLflow.
> **📦 Stack:** adversarial-robustness-toolbox 1.18, numpy, mlflow 2.14
> **✅ Outcome:** Adversarial attack success rates are computed for Champion and Challenger. The comparison informs the robustness dimension of the Champion/Challenger decision.

---

## Phase 45 — Drift Detection System

**Context:** Production models degrade as network traffic patterns evolve. The drift detection system triggers retraining before accuracy drops cause missed attacks — the most safety-critical MLOps component.

#### Subphase 45.1 — MMD Drift Detector

> **🎭 Role:** Senior MLOps Engineer with data drift expertise
> **📍 Context:** Maximum Mean Discrepancy (MMD) measures the statistical distance between two feature distributions. When production traffic drifts from the training distribution, MMD increases above a threshold, signalling that the model may be operating outside its training domain.
> **🔧 Task:** Implement `ml/src/drift/mmd_detector.py`. `MMDDriftDetector` using `alibi_detect.cd.MMDDrift(p_val=0.05, backend="pytorch")`. Initialise with a 5000-sample training reference window. `detect(X_current_window: np.ndarray) -> DriftReport` runs the MMD test and returns `DriftReport` Pydantic v2 model: `mmd_score: float`, `drift_detected: bool`, `threshold_level: DriftThreshold` (NONE / WARNING at 0.05 / CRITICAL at 0.10), `features_drifted: list[str]` (per-feature univariate test results using `alibi_detect.cd.TabularDrift`). Log every DriftReport to the `drift_detections` database table.
> **📦 Stack:** alibi-detect 0.12, torch 2.3, numpy, pydantic v2, SQLAlchemy 2 async
> **✅ Outcome:** `detector.detect(X_production_window)` returns a `DriftReport`. BETH data from a late drift window triggers CRITICAL drift. CICIDS-2017 training data does not trigger drift (false positive rate < 5%).

#### Subphase 45.2 — Drift Simulation & Validation

> **🎭 Role:** MLOps Research Engineer
> **📍 Context:** The drift detector must be validated on known-drift data before production deployment. BETH's natural drift windows from Phase 13 provide ground truth for this validation.
> **🔧 Task:** Write `ml/notebooks/drift/01_drift_validation.ipynb`. Load BETH data from three windows: pre-drift (expected: no drift), during-drift window 1 (expected: WARNING), during-drift window 2 (expected: CRITICAL). Run the MMD detector on sliding windows of 1000 events. Plot MMD scores over time as a line chart with WARNING and CRITICAL threshold reference lines. Compute detection delay: how many batches of 1000 events does the detector take to fire after drift begins? Log detection delay to MLflow as `drift_detection_delay_batches`.
> **📦 Stack:** alibi-detect 0.12, matplotlib, mlflow 2.14
> **✅ Outcome:** The detector correctly classifies all three BETH windows. Detection delay is documented in the MLflow run and referenced in the research paper.

#### Subphase 45.3 — Drift-Triggered Retraining Integration

> **🎭 Role:** Senior MLOps Engineer
> **📍 Context:** CRITICAL drift must trigger automated retraining of the Champion model. The trigger uses Redis pub/sub to decouple the drift detector (ML layer) from the Celery retraining task (API layer).
> **🔧 Task:** Implement `ml/src/drift/retraining_trigger.py`. `DriftRetrigger` that: on CRITICAL drift, publishes `drift:critical:{model_family}:{mmd_score:.4f}` to the Redis pub/sub channel `xaiguard:retraining`. Implement cooldown: if retraining was triggered in the last 6 hours (checked via a Redis key `drift:cooldown:{model_family}` with 6h TTL), skip and log a warning. The backend Celery task (Phase 59) subscribes to this channel and dispatches the retraining pipeline. Write unit tests for the cooldown logic using a mock Redis client.
> **📦 Stack:** redis-py (asyncio), Celery 5.x, pytest-asyncio
> **✅ Outcome:** CRITICAL drift publishes to Redis and the Celery task fires. Sending CRITICAL drift twice within 6 hours triggers exactly one retraining.

---

## Phase 46 — Modular Monolith Core Layer

**Context:** The core layer provides shared infrastructure to all nine domain modules. It owns no business logic and exports only utilities — all domain modules import from core but never from each other.

#### Subphase 46.1 — Settings & Configuration

> **🎭 Role:** Senior Backend Platform Engineer
> **📍 Context:** pydantic-settings provides type-safe configuration that validates all environment variables on startup. A missing required variable causes immediate startup failure with a clear error — preventing silent misconfiguration in production.
> **🔧 Task:** Implement `services/api/core/config.py`. `Settings(BaseSettings)` with `model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="forbid")`. Required fields: `database_url: PostgresDsn`, `redis_url: RedisDsn`, `secret_key: SecretStr`. Optional with defaults: `environment: Literal["development","staging","production"] = "development"`, `debug: bool = False`, `log_level: str = "INFO"`, `database_pool_size: int = 10`, `redis_max_connections: int = 100`, `algorithm: str = "HS256"`, `access_token_expire_minutes: int = 30`, `refresh_token_expire_days: int = 7`, `cors_origins: list[str] = []`, `mlflow_tracking_uri: str = "http://localhost:5000"`, `minio_endpoint: str`, `minio_access_key: SecretStr`, `minio_secret_key: SecretStr`, `minio_bucket_name: str = "xaiguard"`, `abuseipdb_api_key: SecretStr | None = None`, `sentry_dsn: SecretStr | None = None`. Use `@lru_cache` on `get_settings()` factory function.
> **📦 Stack:** pydantic-settings 2.x, pydantic v2
> **✅ Outcome:** `get_settings()` is cached and returns the same instance on every call. Missing `DATABASE_URL` raises `ValidationError` at startup with a clear field-level error message.

#### Subphase 46.2 — Exception Handlers & RFC 7807 Error Responses

> **🎭 Role:** Senior API Engineer
> **📍 Context:** All API errors must return RFC 7807 ProblemDetail JSON responses. Unhandled exceptions must be caught before they leak stack traces to clients. Every error response must include the request ID for log correlation.
> **🔧 Task:** Implement `services/api/core/exceptions.py`. Domain exceptions inheriting `XAIGuardException(Exception)`: `ResourceNotFoundException` (404), `ValidationException` (422), `PermissionDeniedException` (403), `RateLimitExceededException` (429), `ServiceUnavailableException` (503). `ProblemDetail` Pydantic model: `type: str`, `title: str`, `status: int`, `detail: str`, `instance: str`, `request_id: str`. `register_exception_handlers(app: FastAPI)`: handles `XAIGuardException` → `ProblemDetail` JSON; `RequestValidationError` → 422 with field-level errors; bare `Exception` → logs traceback to structlog at ERROR, reports to Sentry, returns generic 500 ProblemDetail (never exposes internals in production).
> **📦 Stack:** FastAPI 0.111, sentry-sdk[fastapi], structlog, pydantic v2
> **✅ Outcome:** An unhandled exception in any route handler returns `{"status": 500, "detail": "An unexpected error occurred"}` in production with the traceback visible in Sentry.

#### Subphase 46.3 — Redis Client & Cache Utilities

> **🎭 Role:** Senior Backend Engineer
> **📍 Context:** Multiple domain modules use Redis for different purposes: deduplication hashes, feature caching, pub/sub, and rate limiting. A shared client prevents connection pool fragmentation and ensures consistent serialisation.
> **🔧 Task:** Implement `services/api/core/redis_client.py`. Create a connection pool using `redis.asyncio.ConnectionPool.from_url(REDIS_URL, max_connections=MAX_CONNECTIONS, decode_responses=True)`. Expose `get_redis()` FastAPI dependency that yields `AsyncRedis` from the pool. Typed cache utilities: `async def cache_set(key: str, value: BaseModel, ttl: int, client: AsyncRedis) -> None` (serialises with `orjson`); `async def cache_get(key: str, model_class: type[T], client: AsyncRedis) -> T | None` (deserialises with Pydantic v2 `model_validate_json`); `async def publish(channel: str, message: dict, client: AsyncRedis) -> None` for pub/sub. All utilities include structured error logging on failure.
> **📦 Stack:** redis[asyncio] 5.x, orjson, pydantic v2
> **✅ Outcome:** `cache_set("pred:abc", prediction_response, ttl=3600, redis=client)` stores the Pydantic model as orjson bytes. `cache_get("pred:abc", PredictionResponse, client)` returns the correctly typed object.

#### Subphase 46.4 — Request ID, Timing & Security Header Middleware

> **🎭 Role:** Observability and Security Engineer
> **📍 Context:** Every API request needs a unique ID for log correlation across middleware, route handlers, Celery tasks, and OpenTelemetry traces. Security headers protect against common web attacks.
> **🔧 Task:** Implement `services/api/core/middleware.py`. `RequestIDMiddleware(BaseHTTPMiddleware)`: generates UUID4 request ID, stores in `contextvars.ContextVar`, injects into structlog context, adds `X-Request-ID` response header. `RequestTimingMiddleware`: adds `X-Process-Time-Ms` with wall-clock duration in milliseconds. `SecurityHeadersMiddleware`: adds `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security: max-age=31536000; includeSubDomains`, `X-XSS-Protection: 0` (modern CSP replaces this), `Referrer-Policy: strict-origin-when-cross-origin`. Register all three in the application factory in dependency order.
> **📦 Stack:** FastAPI, starlette, contextvars (stdlib), structlog
> **✅ Outcome:** Every response has all three custom headers and all five security headers. The request ID appears on every structlog line for that request.

---

## Phase 47 — Auth Module

**Context:** The auth module owns user authentication, JWT token management, and role-based access control. It is the security boundary that all other modules depend on but never modify.

#### Subphase 47.1 — JWT Service Implementation

> **🎭 Role:** Senior Security-Focused Backend Engineer
> **📍 Context:** The auth module uses JWT access tokens (HS256, 30 min expiry) and refresh tokens (7-day, stored hash in Redis). The access token carries the `role` claim used by all RBAC checks across every module.
> **🔧 Task:** Implement `services/api/auth/jwt_service.py`. `JWTService` using `python-jose[cryptography]`. `create_access_token(user_id, username, role, expire_minutes) -> str`: HS256-signed with claims `sub`, `username`, `role`, `exp`, `iat`, `jti` (UUID4 for revocation). `create_refresh_token(user_id) -> tuple[str, str]` (token + jti): stores `sha256(token)` hash in Redis with 7-day TTL keyed by `refresh:{jti}`. `verify_access_token(token) -> TokenPayload`: decodes and validates all claims; raises `CredentialsException` on invalid, expired, or malformed tokens. `revoke_refresh_token(jti)`: deletes `refresh:{jti}` from Redis. `is_refresh_token_valid(jti, token) -> bool`: compares stored hash to `sha256(token)`.
> **📦 Stack:** python-jose[cryptography], redis[asyncio], passlib[bcrypt], pydantic v2
> **✅ Outcome:** An access token decoded by `verify_access_token` returns the correct `TokenPayload`. An expired token raises `CredentialsException`. A revoked refresh token returns False from `is_refresh_token_valid`.

#### Subphase 47.2 — Auth Routes & Dependencies

> **🎭 Role:** Senior Backend Engineer
> **📍 Context:** The auth module provides two FastAPI route dependencies used by all other modules: `get_current_user` and `require_admin`. It also owns the login, refresh, and logout endpoints.
> **🔧 Task:** Implement `services/api/auth/router.py`. Routes: `POST /v1/auth/login` — validates credentials with `passlib.CryptContext`, creates access + refresh tokens, logs login event to AuditLog, returns `TokenResponse(access_token, refresh_token, token_type="bearer")`; `POST /v1/auth/refresh` — validates refresh token validity and hash match, issues new access token; `POST /v1/auth/logout` — revokes refresh token, logs logout. Dependencies in `services/api/auth/dependencies.py`: `get_current_user(token: Annotated[str, Security(oauth2_scheme)]) -> UserContext` — decodes JWT, fetches user from DB, validates active status; `require_admin(user: Annotated[UserContext, Depends(get_current_user)]) -> UserContext` — raises `PermissionDeniedException` if `user.role != UserRole.ADMIN`. Apply `slowapi` rate limit (10 req/min) on login.
> **📦 Stack:** FastAPI 0.111, python-jose, passlib[bcrypt], slowapi, SQLAlchemy 2 async
> **✅ Outcome:** `Depends(get_current_user)` works in any module router. `Depends(require_admin)` returns 403 for analyst-role JWTs. The login endpoint returns 429 after 11 requests in 1 minute.

#### Subphase 47.3 — Auth Module Test Suite

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** The auth module is the security boundary. Its tests are the most critical in the entire API codebase. All eight test cases must pass for any PR to merge.
> **🔧 Task:** Write `services/api/tests/test_auth.py` using `pytest-asyncio` and `httpx.AsyncClient`. Test: (1) successful login returns access and refresh tokens with correct schema; (2) wrong password returns 401 with ProblemDetail; (3) disabled user account returns 401; (4) expired access token returns 401; (5) `require_admin` returns 403 for analyst-role JWT; (6) refresh token rotation — using a refresh token twice returns 401 on the second use; (7) logout invalidates the refresh token; (8) login returns 429 after 11 requests in 1 minute. Use `factory-boy` for user fixtures. Target 100% branch coverage on `jwt_service.py`.
> **📦 Stack:** pytest-asyncio, httpx, factory-boy, coverage[toml]
> **✅ Outcome:** All 8 auth tests pass. Test 6 (token rotation) is the most security-critical: it prevents session hijacking by ensuring stolen refresh tokens cannot be reused.

#### Subphase 47.4 — Audit Log Integration

> **🎭 Role:** Security Compliance Engineer
> **📍 Context:** Every security-sensitive action must be recorded in the audit log for compliance, incident investigation, and SOC2 readiness. The audit log is append-only and cannot be modified after writing.
> **🔧 Task:** Implement `services/api/auth/audit.py`. `AuditLogger` async class with `log_action(db_session: AsyncSession, user_id: UUID, action: AuditAction, resource_type: str, resource_id: str, request: Request, details: dict)` that creates an `AuditLog` record with: user_id, action (StrEnum: LOGIN, LOGOUT, PROMOTE_MODEL, ROLLBACK_MODEL, ACKNOWLEDGE_ALERT), resource_type, resource_id, client_ip (extracted from `X-Forwarded-For` if present, falling back to `request.client.host`), user_agent, details as JSONB, timestamp. Inject `AuditLogger` into login, logout, promote, rollback, and acknowledge handlers. Write a test that verifies a login attempt creates an AuditLog record with the correct IP address from `X-Forwarded-For`.
> **📦 Stack:** SQLAlchemy 2 async, pydantic v2, asyncpg
> **✅ Outcome:** Every login, logout, model promotion, rollback, and alert acknowledgement creates an AuditLog record. IP address is correctly extracted from `X-Forwarded-For`.

---

## Phase Map

| Phase | Title | Subphases |
|-------|-------|-----------|
| P40 | LIME Explainability | 3 |
| P41 | Attention-Based Explainability | 2 |
| P42 | XAI Stability & Pillar 2 Metrics | 1 |
| P43 | Human-Centred XAI Evaluation | 1 |
| P44 | Robustness Testing | 2 |
| P45 | Drift Detection System | 3 |
| P46 | Modular Monolith Core Layer | 4 |
| P47 | Auth Module | 4 |

**Previous ←** [05 — Transformer & XAI](05-xai-and-model-evaluation.md) | **Next →** [07 — Backend Domain Modules & Dashboard](07-mlops-security-testing-and-performance.md)
