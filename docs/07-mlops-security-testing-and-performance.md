# 07 — Backend Domain Modules & Security Dashboard

> **Phases 48–55** | Events, Predictions, Explanations, Model Registry, Alerts, WebSocket, Threat Intelligence, and the security analyst dashboard.
>
> **How to use:** Pick one subphase. Copy its **Prompt** into your AI code editor. Implement it. Move to the next subphase.

---

## Phase 48 — Events Module

**Context:** The events module is the front door of the XAI-Guard system. It receives raw security events from external systems, validates and deduplicates them, stores them, and queues them for processing. It is a self-contained module that owns only event ingestion and storage.

#### Subphase 48.1 — Event Ingestion Endpoint
> **Prompt:** Implement the bulk event ingestion endpoint for the XAI-Guard events module. The endpoint accepts a batch of up to 1000 validated SecurityEvent objects, deduplicates them, bulk-inserts accepted events to the database, publishes each to the processing queue, and returns a summary of how many were accepted and how many were skipped as duplicates. The response must be returned immediately without waiting for processing to complete.

#### Subphase 48.2 — Event Deduplication
> **Prompt:** Implement the event deduplication logic for the XAI-Guard events module. Compute a deterministic SHA-256 hash from the source IP, destination IP, timestamp to the nearest second, and protocol for each incoming event. Check the Redis cache for the presence of this hash with a TTL of 5 minutes. If present, mark the event as a duplicate and skip it. If absent, store the hash in Redis and proceed with ingestion. This prevents the same event being processed and alerted on multiple times.

#### Subphase 48.3 — Event Storage Service
> **Prompt:** Implement the event storage service for the XAI-Guard events module. Use SQLAlchemy async bulk insert to write accepted events to the security_events table in batches for efficiency. The service is called by the ingestion endpoint and must handle database errors gracefully by rolling back the transaction and returning the error in the response rather than failing silently.

#### Subphase 48.4 — Queue Publishing
> **Prompt:** Implement the Redis queue publishing step in the XAI-Guard events module. After successful database insertion, publish each event's database ID to the events:pending Redis Stream. The Celery event processor worker in Phase 49 consumes from this stream. Use a Redis Stream (not a list) for durability: messages survive a Redis restart and delivery can be acknowledged after successful processing.

#### Subphase 48.5 — Events Module Tests
> **Prompt:** Write comprehensive tests for the XAI-Guard events module. Test: valid batch of events is ingested and IDs returned; duplicate events are correctly detected and counted in the skipped field; oversized batches above the 1000 event limit return 422; events with invalid IP addresses return 422; a database failure during bulk insert returns a 500 response without partial data; and duplicate hash expiry works correctly after the TTL.

---

## Phase 49 — Predictions Module

**Context:** The predictions module orchestrates real-time ML inference. It loads the Champion model from the registry, runs the feature pipeline, makes predictions, and dispatches asynchronous explanation generation. It is the performance-critical core of the API.

#### Subphase 49.1 — Champion Model Loading Service
> **Prompt:** Implement the Champion model loading service for the XAI-Guard predictions module. On application startup the service loads the current Champion model artifact from MLflow by alias rather than by version number. It also loads the preprocessing pipeline artifact and the feature list. A background asyncio task polls the model registry every 60 seconds for a Champion version change and performs a zero-downtime swap if a new Champion is found.

#### Subphase 49.2 — Feature Pipeline Integration
> **Prompt:** Implement the feature pipeline integration for the XAI-Guard predictions module. The module applies the loaded preprocessing pipeline and feature engineering functions from the ML module to an incoming SecurityEvent before passing it to the model. For tabular models, the output is a 2D feature vector. For sequence models, the output is a windowed 3D sequence using the last N events from the same source IP retrieved from a short-term Redis cache.

#### Subphase 49.3 — Prediction Endpoint
> **Prompt:** Implement the POST /v1/predict endpoint for the XAI-Guard predictions module. The endpoint validates the SecurityEvent input, checks the feature cache for the source IP, runs the feature pipeline, calls the Champion model for inference, maps the confidence score to a severity level, stores the prediction to the database asynchronously without blocking the response, dispatches the SHAP explanation Celery task, and returns a PredictionResponse within the P99 100 millisecond budget.

#### Subphase 49.4 — Shadow Inference Dispatch
> **Prompt:** Implement shadow inference dispatch for the XAI-Guard predictions module. After the Champion inference completes and the response is prepared, asynchronously dispatch a Celery task that runs the same event through the registered Challenger model. The Challenger prediction is stored in the database with a shadow_inference flag. Shadow predictions are never returned to the caller and never trigger alerts. They are used only by the nightly evaluation job in Phase 51.

#### Subphase 49.5 — Redis Feature Cache
> **Prompt:** Implement the Redis feature cache for the XAI-Guard predictions module. Cache the computed feature vector for each event using a hash of the event payload as the cache key with a TTL of 60 seconds. On a cache hit, skip the feature pipeline computation and use the cached vector. Log cache hit and miss rates to the Prometheus metrics registry. Target a hit rate above 30% under steady-state load.

#### Subphase 49.6 — Predictions Module Tests
> **Prompt:** Write comprehensive tests for the XAI-Guard predictions module. Test: a valid event returns a PredictionResponse with the correct schema; the feature cache is populated after the first prediction; the model hot-reload detects a Champion version change; shadow inference is dispatched as a Celery task without blocking the response; an invalid event payload returns 422; and the endpoint returns a response within 200 milliseconds for a mocked model on a standard CI machine.

---

## Phase 50 — Explanations Module

**Context:** The explanations module owns XAI generation and retrieval. Explanation generation is compute-heavy and always asynchronous. Analysts request explanations and poll for results without the response being blocked.

#### Subphase 50.1 — SHAP Explanation Celery Task
> **Prompt:** Implement the SHAP explanation Celery task for the XAI-Guard explanations module. The task accepts a prediction ID, loads the corresponding prediction and model from the database and MLflow, loads the original event features, creates the appropriate SHAP explainer variant for the model type, computes SHAP values, structures the result into a SHAPExplanation schema, stores it in the xai_explanations database table, and marks the task as complete. Log computation time to the database and to MLflow.

#### Subphase 50.2 — LIME Explanation Celery Task
> **Prompt:** Implement the LIME explanation Celery task for the XAI-Guard explanations module following the same pattern as the SHAP task. The LIME task is dispatched only when the caller explicitly requests LIME via a query parameter on the explanation request endpoint. LIME is slower than SHAP so it is a separate optional task not triggered automatically. Store the LIME result in the xai_explanations table with the method field set to lime.

#### Subphase 50.3 — Explanation Request Endpoint
> **Prompt:** Implement the POST /v1/explain endpoint for the XAI-Guard explanations module. The endpoint accepts a prediction ID and an optional explanation method parameter defaulting to SHAP. It dispatches the corresponding Celery task and returns the Celery task ID immediately. The caller uses the task ID to poll for results. If an explanation for this prediction and method already exists in the database, return the existing result immediately without dispatching a new task.

#### Subphase 50.4 — Explanation Polling Endpoint
> **Prompt:** Implement the GET /v1/explain/{task_id} endpoint for the XAI-Guard explanations module. The endpoint checks the Celery task state: if pending or running it returns status processing with a null result; if complete it returns status complete with the full explanation schema from the database; if failed it returns status failed with an error message. Include the computation time and the explanation stability score in all complete responses.

#### Subphase 50.5 — Explanations Module Tests
> **Prompt:** Write tests for the XAI-Guard explanations module. Test: dispatching a SHAP explanation task for a valid prediction returns a task ID; polling a completed task returns the full explanation; polling a pending task returns processing status; requesting an explanation for a non-existent prediction returns 404; re-requesting an explanation for a prediction that already has one returns the cached result without dispatching a new task; and the Celery task correctly handles a model loading failure.

---

## Phase 51 — Model Registry Module

**Context:** The model registry module owns the Champion/Challenger lifecycle. It provides endpoints for registering models, checking status, promoting Challengers, rolling back, and querying history. It runs the nightly automated evaluation job.

#### Subphase 51.1 — Model Status & History Endpoints
> **Prompt:** Implement the model status and history endpoints for the XAI-Guard model registry module. The GET /v1/models endpoint lists all registered model versions with their metrics and current status. The GET /v1/models/champion endpoint returns the current Champion's full details. The GET /v1/models/challenger endpoint returns the Challenger's details including its shadow evaluation metrics accumulated so far. The GET /v1/models/history endpoint returns all promotion and rollback events with timestamps.

#### Subphase 51.2 — Model Registration Service
> **Prompt:** Implement the model registration service for the XAI-Guard model registry module. The service accepts an MLflow run ID, validates that the run exists and completed successfully, fetches all logged metrics, creates a model version record in the database, and updates the MLflow model alias. If the model status is set to challenger it also updates the in-memory Challenger reference that the predictions module uses for shadow inference dispatch.

#### Subphase 51.3 — Nightly Challenger Evaluation Task
> **Prompt:** Implement the nightly Champion/Challenger evaluation Celery Beat task for the XAI-Guard model registry module. The task fetches all shadow predictions from the last 24 hours alongside the Champion predictions for the same events. It computes F1 macro and ROC-AUC for both models on those events with their ground-truth labels. If the Challenger exceeds the Champion by the promotion thresholds and meets the latency budget it calls the promotion service. Log all evaluation results to the model_evaluations database table.

#### Subphase 51.4 — Promotion & Rollback Endpoints
> **Prompt:** Implement the promotion and rollback endpoints for the XAI-Guard model registry module. Both endpoints require the admin role from the auth module. The POST /v1/models/promote endpoint transitions the Challenger to Champion and the current Champion to Archived, updates all MLflow aliases, notifies the predictions module to reload the model, and records the promotion event. The POST /v1/models/rollback endpoint reverts to the previous Champion from the history table.

#### Subphase 51.5 — Drift-Triggered Evaluation
> **Prompt:** Implement the drift-triggered evaluation path for the XAI-Guard model registry module. When the drift module publishes a CRITICAL drift event the model registry module's Celery task is triggered immediately rather than waiting for the nightly schedule. The triggered evaluation uses a shorter window of the most recent 6 hours of shadow predictions rather than 24 hours to get a fast signal on whether the Challenger performs better on the new data distribution.

#### Subphase 51.6 — Registry Module Tests
> **Prompt:** Write tests for the XAI-Guard model registry module. Test: registering a valid MLflow run creates a database record; the nightly evaluation task correctly computes metrics from shadow predictions; auto-promotion fires when thresholds are met; auto-promotion does not fire when the latency constraint is violated even if accuracy thresholds are met; rollback reverts to the correct previous Champion; and analyst role users receive 403 when calling promotion and rollback endpoints.

---

## Phase 52 — Alerts & WebSocket Module

**Context:** The alerts module owns alert creation, deduplication, lifecycle management, and real-time delivery to connected dashboard clients via WebSocket. Real-time delivery is the feature analysts depend on most.

#### Subphase 52.1 — Alert Creation Service
> **Prompt:** Implement the alert creation service for the XAI-Guard alerts module. The service is called by the Celery event processor after a prediction is made. If the prediction confidence exceeds the severity threshold for HIGH or CRITICAL level, an alert record is created in the database and published to the Redis alerts:live pub/sub channel. The service applies deduplication logic before creating any alert.

#### Subphase 52.2 — Alert Deduplication
> **Prompt:** Implement alert deduplication for the XAI-Guard alerts module. When a new alert would be created, check whether an unacknowledged alert with the same source IP and attack type already exists and was created within the last 5 minutes. If yes, increment the alert_count field of the existing alert rather than creating a new record. This prevents alert storms where a single ongoing attack generates hundreds of identical notifications.

#### Subphase 52.3 — Alert Management Endpoints
> **Prompt:** Implement the alert management endpoints for the XAI-Guard alerts module. The GET /v1/alerts endpoint returns a paginated list of alerts sortable by severity and timestamp with filters for severity level, attack type, and acknowledgement status. The PATCH /v1/alerts/{id}/acknowledge endpoint marks an alert as acknowledged, records the acknowledging user from the JWT token, and records the acknowledgement timestamp.

#### Subphase 52.4 — WebSocket Connection Manager
> **Prompt:** Implement the WebSocket connection manager for the XAI-Guard alerts module. The manager maintains a registry of all active WebSocket connections authenticated by JWT token provided as a query parameter. On connection, authenticate the token using the auth module's token validation function. Maintain the connection in the registry keyed by connection ID. On disconnect, remove from registry and cancel the Redis subscription.

#### Subphase 52.5 — Real-Time Alert Broadcasting
> **Prompt:** Implement real-time alert broadcasting for the XAI-Guard alerts module. For each active WebSocket connection, start a background asyncio task that subscribes to the Redis alerts:live pub/sub channel and forwards every received message to the connected client as a WebSocket message in the AlertMessage schema format. Handle backpressure by dropping messages to slow clients rather than blocking the pub/sub subscription.

#### Subphase 52.6 — Alerts Module Tests
> **Prompt:** Write tests for the XAI-Guard alerts module. Test: a CRITICAL prediction creates an alert record; a duplicate alert within 5 minutes increments the count rather than creating a new record; the acknowledge endpoint correctly records the user and timestamp; the alert list endpoint respects severity and acknowledgement filters; a WebSocket client receives an alert within 2 seconds of a CRITICAL prediction being processed in a test pipeline.

---

## Phase 53 — Threat Intelligence Module

**Context:** The threat intelligence module replaces the stubs created in Phase 21 with live integrations. It enriches predictions with IP reputation data and MITRE ATT&CK technique mappings that analysts see in the Threat Detection card.

#### Subphase 53.1 — AbuseIPDB Integration
> **Prompt:** Implement the AbuseIPDB IP reputation integration for the XAI-Guard threat intelligence module. The service makes an authenticated async HTTP GET request to the AbuseIPDB v2 check endpoint for a given IP address and returns the confidence score from 0 to 100, usage type, country code, ISP, and whether the IP is whitelisted. Cache the result in Redis with a TTL of 3600 seconds so the API is called at most once per hour per IP.

#### Subphase 53.2 — Tor Exit Node Integration
> **Prompt:** Implement the Tor exit node detection for the XAI-Guard threat intelligence module. Download the current Tor exit node list from the TorDNSEL service daily via a Celery Beat task and store all IPs as members of a Redis Set. The is_tor_exit_node function checks Redis Set membership for instant lookup without any external API call. This replaces the stub from Phase 21 with a real implementation requiring only a Redis operation at inference time.

#### Subphase 53.3 — MITRE ATT&CK Mapping
> **Prompt:** Implement the MITRE ATT&CK technique mapping for the XAI-Guard threat intelligence module. Create a static mapping from each attack type in the unified taxonomy to the corresponding MITRE ATT&CK technique ID, technique name, tactic name, and tactic ID. For example BruteForce maps to T1110 with tactic TA0006 Credential Access. Include a link template to the attack.mitre.org technique page. This mapping is used by both the dashboard Threat Detection card and the alert schema.

#### Subphase 53.4 — Cache Warming Celery Task
> **Prompt:** Implement the threat intelligence cache warming Celery Beat task for XAI-Guard. The task runs hourly, fetches the 1000 most frequent source IPs from the security_events table over the last 24 hours, pre-fetches AbuseIPDB reputation for all of them in batches respecting the API rate limit, and stores all results in Redis. This ensures that the most common IPs in production traffic are always cache-warm and never add API latency to the prediction hot path.

#### Subphase 53.5 — Async Event Enrichment Task
> **Prompt:** Implement the async event enrichment Celery task for the XAI-Guard threat intelligence module. After each event is stored and its prediction is made, this task fetches the live threat intelligence for the event's source IP and stores the enrichment data in the security_events table's threat_intel_data JSONB column. This enrichment is never on the critical prediction path and does not affect response latency.

#### Subphase 53.6 — Threat Intel Module Tests
> **Prompt:** Write tests for the XAI-Guard threat intelligence module. Use pytest with the respx library to mock all external HTTP calls. Test: AbuseIPDB returns a cached result on the second call for the same IP; a Tor exit node IP returns true from the Redis Set lookup; a non-Tor IP returns false; the MITRE mapping returns the correct technique for each attack type; and the cache warming task correctly batches AbuseIPDB requests within the rate limit.

---

## Phase 54 — Security Dashboard Foundation & Layout

**Context:** The security analyst dashboard is a Next.js 14 App Router application using the shared component library. The foundation phase establishes authentication, layout, API client, and WebSocket client before any feature components are built.

#### Subphase 54.1 — Next.js App Setup & Dark Mode
> **Prompt:** Set up the XAI-Guard security dashboard Next.js 14 application with App Router. Configure Tailwind CSS with a dark-mode-first configuration suitable for SOC environments: near-black background, dark surface cards, and the accent colours for severity levels (critical red, high orange, medium yellow, low blue). Establish the global CSS variables for the colour palette and apply them to the root layout so all components inherit consistent theming.

#### Subphase 54.2 — Root Layout & Navigation Sidebar
> **Prompt:** Implement the root layout and navigation sidebar for the XAI-Guard security dashboard. The sidebar provides navigation between the four dashboard sections: Live Alerts, Threat Details, Metrics Overview, and Model Status. Include the current user display with their role badge and a logout button. The sidebar should be collapsible for wide content. The main content area fills the remaining viewport width.

#### Subphase 54.3 — Authentication Guard Middleware
> **Prompt:** Implement the Next.js middleware authentication guard for the XAI-Guard security dashboard. All routes except the login page require a valid JWT access token stored in an httpOnly cookie. The middleware reads the token, verifies it is not expired, and redirects to the login page if validation fails. On the login page, implement the form that calls the API login endpoint and stores the returned tokens in httpOnly cookies.

#### Subphase 54.4 — API Client Configuration
> **Prompt:** Implement the XAI-Guard dashboard API client using SWR for data fetching. Create a typed fetch wrapper that automatically includes the JWT access token from cookies in every request, handles 401 responses by redirecting to login, and retries on network failures. Create SWR hooks for each module's endpoints: useAlerts, usePrediction, useExplanation, useModels, and useMetrics. These hooks are used by all dashboard feature components.

#### Subphase 54.5 — WebSocket Client Setup
> **Prompt:** Implement the WebSocket client for the XAI-Guard security dashboard. Create a custom React context and hook that manages a persistent WebSocket connection to the alerts endpoint. The hook reconnects automatically with exponential backoff on connection loss. It exposes the stream of received alert messages and a connection status indicator. The AlertsFeed component from Phase 55 consumes this hook.

#### Subphase 54.6 — Dashboard Routing Structure
> **Prompt:** Set up the complete routing structure for the XAI-Guard security dashboard using Next.js 14 App Router. Define routes for the main dashboard overview, the alerts list page, the alert detail page that displays the Threat Detection card and XAI panel, the metrics page, and the model status page. Use route groups to apply the authenticated layout to all routes except login. Define loading and error boundary components for each route segment.

---

## Phase 55 — Alert Feed & Threat Detail Components

**Context:** These are the primary analyst-facing components. The alert feed shows all incoming threats in real time. The threat detail panel is what analysts open when they need to understand a specific threat and decide how to respond.

#### Subphase 55.1 — AlertsFeed Component
> **Prompt:** Implement the AlertsFeed component for the XAI-Guard security dashboard. The component connects to the WebSocket client hook from Phase 54 and renders a scrollable, real-time list of alerts sorted by severity then timestamp. Each alert row shows the severity badge, attack type, source IP, confidence percentage, and time elapsed. On new alerts, auto-scroll to the top if the user is already at the top; otherwise show a floating notification badge with the count of new alerts.

#### Subphase 55.2 — Severity Badge System
> **Prompt:** Implement the severity badge component system for the XAI-Guard security dashboard. Each severity level has a distinct visual style: CRITICAL uses a pulsing red badge to convey urgency, HIGH uses a solid orange badge, MEDIUM uses a yellow badge, and LOW uses a blue badge. The badge system is shared between the AlertsFeed, ThreatDetailPanel, and the alert list page. Implement it as a shared component in the packages/ui library.

#### Subphase 55.3 — ThreatDetailPanel Component
> **Prompt:** Implement the ThreatDetailPanel component for the XAI-Guard security dashboard. This component renders the Threat Detection card when an analyst clicks an alert. It displays: the attack type with a security-relevant icon, confidence percentage, severity badge, source and destination IPs, the Why section showing the top 4 SHAP feature contributions as a horizontal bar list with feature names and percentage contribution values, the recommended action text, and the MITRE ATT&CK technique badge linking to attack.mitre.org.

#### Subphase 55.4 — Feature Contribution Display
> **Prompt:** Implement the feature contribution display sub-component for the XAI-Guard ThreatDetailPanel. The component takes an array of the top SHAP feature contributions and renders each as a horizontal bar where the bar width represents the contribution magnitude and the colour indicates direction: positive contributions in red-warm tones (indicating the feature increased threat confidence) and negative contributions in blue-cool tones. Show the percentage contribution next to each bar.

#### Subphase 55.5 — Recommended Action Display
> **Prompt:** Implement the recommended action display for the XAI-Guard ThreatDetailPanel. Map each attack type to a set of prioritised recommended analyst actions. For BruteForce the actions are: block the source IP temporarily, investigate the targeted user account, check for successful logins in the 5 minutes following the attack. For DDoS: enable rate limiting on the ingress path, notify network operations. For PortScan: flag the source IP for monitoring, check for subsequent exploitation attempts. Render these as a numbered action list below the XAI explanation.

#### Subphase 55.6 — MITRE ATT&CK Badge Component
> **Prompt:** Implement the MITRE ATT&CK badge component for the XAI-Guard security dashboard. The badge displays the technique ID, technique name, and tactic name in a compact format. Clicking the badge opens the corresponding attack.mitre.org page in a new tab. The badge is used in the ThreatDetailPanel and in the alert list row for HIGH and CRITICAL severity alerts. Implement it as a shared component in the packages/ui library.

#### Subphase 55.7 — Alert Component Tests
> **Prompt:** Write component tests for the XAI-Guard alert feed and threat detail components using React Testing Library. Test: the AlertsFeed renders existing alerts on mount; a new WebSocket message adds an alert to the top of the feed; clicking an alert opens the ThreatDetailPanel; the ThreatDetailPanel displays the correct SHAP feature contributions; the severity badge renders the correct colour class for each severity level; and the MITRE ATT&CK badge renders the correct technique information.

---

## Phase Map

| Phase | Title | Subphases |
|-------|-------|-----------|
| P48 | Events Module | 5 |
| P49 | Predictions Module | 6 |
| P50 | Explanations Module | 5 |
| P51 | Model Registry Module | 6 |
| P52 | Alerts & WebSocket Module | 6 |
| P53 | Threat Intelligence Module | 6 |
| P54 | Dashboard Foundation & Layout | 6 |
| P55 | Alert Feed & Threat Detail Components | 7 |

**Previous ←** [06 — LIME, XAI Evaluation & Backend Core](06-backend-and-frontend-engineering.md) | **Next →** [08 — Admin Panel, MLOps & Production](08-production-deployment-and-roadmap.md)
