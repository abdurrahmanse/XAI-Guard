---
# 01 — Project Foundation

> **Phases 1–8** | Research scoping, project charter, monorepo setup, infrastructure, database schema, modular monolith design, API contract strategy, and frontend architecture.
>
> **How to use:** Pick one subphase. Copy its **Prompt** into your AI code editor. Implement it. Move to the next subphase. Complete phases in order.

---

## Phase 1 — Research Statement & Evaluation Framework

**Context:** Define the research question, the six models being compared, and the exact metrics that determine the winner. Every decision in later phases references this output.

#### Subphase 1.1 — Core Research Question
> **Prompt:** Write a formal research statement for XAI-Guard — an explainable multi-model cybersecurity threat detection platform. The central question is: which AI model offers the best balance of accuracy, recall, false-positive control, explainability, inference latency, computational cost, and human usefulness for real-world cybersecurity threat detection? The statement should be suitable as the opening section of an academic paper.

#### Subphase 1.2 — Eight Research Sub-Questions
> **Prompt:** Extend the XAI-Guard research statement with eight formally stated sub-questions covering: classical ML vs deep learning for IDS performance; LSTM vs Transformer for sequence-based detection; whether large Transformer accuracy gain justifies its compute cost; which XAI method is most useful to analysts; whether a measurable trade-off exists between prediction accuracy and explanation quality; which model is most cost-efficient for deployment; whether performance is consistent across attack types; and which model is most robust to data drift. State each as a numbered research question with a null hypothesis.

#### Subphase 1.3 — Three-Pillar Evaluation Framework
> **Prompt:** Design and document the three-pillar evaluation framework for XAI-Guard model comparison. Pillar 1 is Prediction Performance covering accuracy, precision, recall, F1-macro, F1 per attack class, ROC-AUC, and PR-AUC. Pillar 2 is Explainability covering SHAP stability, LIME-SHAP agreement, attention fidelity, and analyst actionability. Pillar 3 is Operations covering inference latency percentiles, throughput in events per second, peak memory in MB, and training cost in GPU-hours. Define how these combine into a weighted composite deployment score.

#### Subphase 1.4 — Six-Model Benchmark Specification
> **Prompt:** Write the model benchmark specification for XAI-Guard. Define the role of each of the six competing models: Logistic Regression as the interpretability baseline setting the performance floor; Random Forest as the classical ensemble benchmark; XGBoost as the strong tabular baseline and initial Champion model; LSTM as the sequence modelling baseline testing temporal pattern detection; Transformer Encoder as the primary research model testing attention-based architectures; and Lightweight Transformer as the cost-efficient deployment candidate built via knowledge distillation. For each model state which research sub-questions it primarily answers and what constitutes success.

#### Subphase 1.5 — Champion/Challenger Promotion Policy
> **Prompt:** Write the formal Champion/Challenger model promotion policy for XAI-Guard. Define what shadow evaluation mode means, how the nightly automated comparison works, the promotion thresholds for F1 improvement and ROC-AUC improvement, the latency budget constraint that candidates must meet, what triggers automatic promotion, and the rollback procedure. This policy document will be the specification that the model registry module implements.

#### Subphase 1.6 — Attack Taxonomy & Dataset Justification
> **Prompt:** Write the attack taxonomy and dataset selection rationale for XAI-Guard. Define the unified attack class taxonomy used across all four datasets. For each dataset — NSL-KDD, CICIDS-2017, UNSW-NB15, and BETH — document why it was chosen, its key characteristics and challenges, and which research sub-questions it helps answer. Map each dataset's native attack labels to the unified taxonomy.

---

## Phase 2 — Project Charter & Scope

**Context:** Define project boundaries, success criteria, non-goals, and terminology before any code is written. These documents prevent scope creep across 63 development phases.

#### Subphase 2.1 — Project Charter
> **Prompt:** Create the XAI-Guard project charter covering: project purpose and research objectives, full scope of what will be built across 63 phases, explicit success criteria tied to the evaluation framework from Phase 1, a stakeholder map, timeline overview, and a risk register with at least five identified risks and their mitigations.

#### Subphase 2.2 — Non-Goals & Explicit Boundaries
> **Prompt:** Write the XAI-Guard non-goals document. Explicitly state what the platform will not do: it will not capture raw network packets; it will not replace human security analysts; it will not integrate with any specific SIEM vendor out of the box; it will not train on classified data; it will not produce legally admissible forensic evidence. Being explicit prevents scope creep during development.

#### Subphase 2.3 — Technical Constraints & Architectural Decisions
> **Prompt:** Document the non-negotiable technical constraints for XAI-Guard. The backend API will be implemented as a modular monolith — a single deployable application internally structured as self-contained domain modules that communicate only through defined service interfaces. All six ML models must share a common prediction interface. Explanation generation must be asynchronous and must never block prediction responses. The system must be fully runnable on CPU-only hardware for development. Document the rationale for each constraint.

#### Subphase 2.4 — Glossary & Domain Terminology
> **Prompt:** Write the XAI-Guard project glossary. Define all domain terms used across the 63 phases: Champion model, Challenger model, shadow evaluation, drift score, SHAP value, LIME explanation, attention rollout, modular monolith, composite deployment score, attack taxonomy, sequence window, knowledge distillation, shadow inference, PR-AUC, and any other project-specific terms. This glossary will be referenced throughout development to ensure consistent language.

#### Subphase 2.5 — Phase Dependency Map
> **Prompt:** Create a phase dependency map for all 63 XAI-Guard development phases. Identify which phases must be completed sequentially and which can be done in parallel. Identify the critical path from Phase 1 through to Phase 63. Highlight the key blockers: the data engineering phases must complete before any ML training, and the ML training phases must complete before the XAI and backend phases. This helps the developer plan which phases to prioritise.

---

## Phase 3 — Monorepo & Developer Environment

**Context:** Set up the complete development environment so any developer can clone the repo and be fully running in under 10 minutes.

#### Subphase 3.1 — Monorepo Workspace Configuration
> **Prompt:** Configure the XAI-Guard Turborepo monorepo workspace. Set up pnpm workspaces to cover the apps directory containing the security dashboard and admin panel, the services directory containing the Python API, and the packages directory containing shared UI components and config packages. Configure the Turborepo pipeline so lint runs before build, build before test, and the dev task starts all applications concurrently with correct task dependencies.

#### Subphase 3.2 — Python ML Environment Setup
> **Prompt:** Set up the Python machine learning environment for the XAI-Guard ML module using uv as the package manager. Create the pyproject.toml with pinned versions for PyTorch 2, scikit-learn, XGBoost, SHAP, LIME, transformers, MLflow, Optuna, alibi-detect, adversarial-robustness-toolbox, imbalanced-learn, and DVC. The environment must work identically on CPU-only machines and CUDA-enabled machines.

#### Subphase 3.3 — Environment Variables & Secrets Configuration
> **Prompt:** Create the XAI-Guard environment variable configuration. Document every required environment variable across the entire platform: database connection string, Redis connection string, MinIO endpoint and credentials, MLflow tracking server URI, threat intelligence API keys, JWT secret key, CORS allowed origins, and Celery broker URL. Create the example environment file that developers copy and populate. Establish the rule that no secrets are ever committed to the repository.

#### Subphase 3.4 — Code Quality & Pre-commit Hooks
> **Prompt:** Set up code quality tooling and pre-commit hooks for XAI-Guard. Configure pre-commit to enforce: ruff for Python linting and import sorting, black for Python formatting, mypy for Python type checking, ESLint for TypeScript linting, Prettier for TypeScript and CSS formatting, commitlint for conventional commit message format, and detect-secrets to prevent accidental secret commits. Every hook must pass before any commit is accepted.

#### Subphase 3.5 — Developer Onboarding Documentation
> **Prompt:** Write the XAI-Guard CONTRIBUTING.md developer onboarding guide. Cover prerequisites, clone-to-running steps, branch naming conventions using feature/, fix/, research/, and chore/ prefixes, the conventional commit message format, the pull request process and review expectations, how to run each category of tests, and how to start the full local stack. The guide should get a new developer productive in under 30 minutes.

#### Subphase 3.6 — IDE & Editor Configuration
> **Prompt:** Create VS Code workspace configuration for XAI-Guard to give all developers a consistent editing experience. Configure format-on-save with Prettier for TypeScript and Black for Python, ESLint auto-fix on save, Tailwind CSS IntelliSense, Python interpreter path, and mypy integration. Create the extensions recommendations file listing all necessary plugins for the full stack.

---

## Phase 4 — Infrastructure Services Setup

**Context:** Stand up all local development infrastructure — data stores and supporting services that every subsequent phase depends on.

#### Subphase 4.1 — Local Infrastructure Orchestration
> **Prompt:** Create the Docker Compose configuration for XAI-Guard local development infrastructure. Define services for PostgreSQL 16 as the primary database, Redis 7 as cache and task queue, MinIO as the S3-compatible artifact store for MLflow model artifacts and DVC datasets, and MLflow Tracking Server connected to PostgreSQL as its backend store and MinIO as its artifact root. Every service must have health checks and named persistent volumes.

#### Subphase 4.2 — MLflow Server Configuration
> **Prompt:** Configure the MLflow Tracking Server for XAI-Guard. The server should use PostgreSQL as its backend store so experiment metadata is persisted, and MinIO as its artifact store so model files and data artifacts are stored outside the container. Set the default artifact root to a named MinIO bucket. Document the MLflow UI URL and how to access it during development.

#### Subphase 4.3 — Infrastructure Health Verification
> **Prompt:** Create an infrastructure health check utility for XAI-Guard that verifies all required services are reachable and correctly configured. The utility should test PostgreSQL connectivity, Redis connectivity with a ping/pong check, MinIO bucket accessibility, and MLflow server reachability. It should output a clear pass/fail report for each service and exit with a non-zero code if any check fails.

#### Subphase 4.4 — Development Seed Data
> **Prompt:** Create a database seed script for XAI-Guard that populates the development database with realistic test data for frontend and API development. The seed data should include security events covering all attack types, a registered XGBoost model as the Champion with realistic metrics, a Transformer as the registered Challenger, recent predictions at varying severity levels, and a set of unacknowledged alerts. Running this seed enables full dashboard development without waiting for real ML training.

---

## Phase 5 — Database Schema & ORM Layer

**Context:** Define the complete data model as SQLAlchemy 2 async ORM models. All eight backend modules will use these shared models for data access.

#### Subphase 5.1 — ORM Base & Async Session Configuration
> **Prompt:** Set up the SQLAlchemy 2 async ORM foundation for the XAI-Guard modular monolith. Configure the async engine, the async session factory, the declarative base class, and the FastAPI dependency that provides a session per request with proper cleanup. This shared configuration lives in the core layer and is imported by all eight domain modules.

#### Subphase 5.2 — Security Event ORM Model
> **Prompt:** Create the SQLAlchemy ORM model for security events in XAI-Guard. The model stores a processed security event with all its network features in a JSONB column for schema flexibility, with indexed columns for source IP, destination IP, timestamp, protocol, dataset source, and a SHA-256 event hash used for deduplication. Include a JSONB column for threat intelligence enrichment data that is populated asynchronously after the event is stored.

#### Subphase 5.3 — Model Registry ORM Models
> **Prompt:** Create the SQLAlchemy ORM models for the XAI-Guard model registry. Define three models: the model version record linking to an MLflow run ID and storing the framework type, hyperparameters as JSONB, all evaluation metrics as JSONB, and a status field using a PostgreSQL enum of champion, challenger, archived, and training; the model evaluation record that stores the metric comparison results between champion and challenger from the nightly job; and the promotion history record that tracks every promotion and rollback event with the reason and timestamp.

#### Subphase 5.4 — Prediction & Explanation ORM Models
> **Prompt:** Create the SQLAlchemy ORM models for predictions and XAI explanations. The prediction model references both the security event and the model version that generated it, and stores the predicted attack type as an enum, confidence score, severity level as an enum, inference latency in milliseconds, and a flag indicating whether shadow inference is recorded. The explanation model references a prediction and stores the explanation type as an enum (SHAP, LIME, attention), feature contributions as a JSONB array of name-value-direction objects, stability score, and computation time.

#### Subphase 5.5 — Alert ORM Model
> **Prompt:** Create the SQLAlchemy ORM model for the XAI-Guard alert system. An alert references a prediction and stores severity level, acknowledged status, acknowledging user and timestamp, a deduplication key combining source IP and attack type, alert count for deduplicated groups representing repeated alerts from the same source within a 5-minute window, and a JSONB field for MITRE ATT&CK technique information.

#### Subphase 5.6 — Drift Report ORM Model
> **Prompt:** Create the SQLAlchemy ORM model for drift detection reports. The model references a model version and stores the MMD drift score, whether drift was detected as a boolean, the detection timestamp, reference window statistics as JSONB, current window statistics as JSONB, and a flag indicating whether this report triggered a retraining pipeline run.

---

## Phase 6 — Modular Monolith Architecture Design

**Context:** Design the internal architecture of the FastAPI application. A modular monolith is a single deployable application internally structured into self-contained domain modules with enforced boundaries — the best of microservices organisation without distributed system complexity.

#### Subphase 6.1 — Modular Monolith Pattern Guide
> **Prompt:** Write the modular monolith architecture guide for XAI-Guard. Explain the pattern: a single deployable FastAPI application internally structured into eight domain modules, each fully self-contained with its own router, service layer, and any module-specific schemas. Modules communicate only through each other's service interfaces — never by importing internal implementation details. Document why this pattern was chosen over microservices for this project, and what rules enforce the module boundaries.

#### Subphase 6.2 — Module Catalogue & Ownership
> **Prompt:** Define the complete module catalogue for the XAI-Guard modular monolith. Document each of the eight domain modules and their exact ownership: the core module provides shared infrastructure and must not import from any domain module; the auth module owns all identity and access concerns; the events module owns security event ingestion and storage; the predictions module owns ML inference orchestration; the explanations module owns XAI generation and retrieval; the models module owns the Champion/Challenger registry; the alerts module owns alert lifecycle and real-time delivery; the threat_intel module owns IP reputation and MITRE mapping; the drift module owns drift detection and reporting. For each module define what it owns and what it is forbidden from touching.

#### Subphase 6.3 — Inter-Module Dependency Graph
> **Prompt:** Document the allowed inter-module dependencies for the XAI-Guard modular monolith. Define which modules may call which other modules' public service interfaces. The predictions module orchestrates inference by calling the models module for the Champion model reference. The alerts module is triggered only by the predictions module when a high-confidence prediction is made. The drift module is triggered only by the models module's evaluation job. Draw or describe the full dependency graph and flag any circular dependencies as forbidden.

#### Subphase 6.4 — Core Layer Design
> **Prompt:** Design the shared core layer for the XAI-Guard modular monolith. The core layer provides shared infrastructure used by all modules: the database session factory, Redis client, application configuration loaded from environment variables, structured logging configuration, base exception classes that all modules raise, the Prometheus metrics registry, and HTTP middleware for request ID injection and structured request logging. The core layer must never import from any domain module.

#### Subphase 6.5 — Async Task Architecture
> **Prompt:** Design the asynchronous task architecture for XAI-Guard. Celery with Redis as the broker handles three task categories: event processing tasks that consume the ingestion queue and run predictions; explanation generation tasks that run SHAP and LIME computation asynchronously without blocking API responses; and pipeline tasks including the nightly Champion/Challenger evaluation and scheduled weekly retraining. Define the queue names, worker concurrency configuration, and how task results are communicated back to the API layer via the database.

#### Subphase 6.6 — Router Registration & API Versioning
> **Prompt:** Design the API versioning and router registration strategy for the XAI-Guard modular monolith. All routes are prefixed with /v1/. Each module registers its own router with the main FastAPI application during startup. Define the URL prefix convention for each module: auth, events, predict, explain, models, alerts, threat-intel, drift, and health. Define the OpenAPI documentation tags grouping routes by module. Document how new modules are added to the application without modifying the main application file.

---

## Phase 7 — API Contract & Schema Strategy

**Context:** Lock down all data contracts between the backend, ML pipeline, and both frontend applications before any implementation. This enables parallel development across all layers.

#### Subphase 7.1 — Schema Design Conventions
> **Prompt:** Write the Pydantic v2 schema design conventions for XAI-Guard that apply across all eight modules. Define the rules: all input schemas forbid extra fields; all response schemas include a request ID and timestamp; enum types are used for all fixed-value fields such as attack types, severity levels, model status, and explanation types; pagination follows a cursor-based pattern with a consistent structure; error responses follow RFC 7807 Problem Details format; and all monetary or computational cost fields use explicit units in their field names.

#### Subphase 7.2 — Security Event & Prediction Schemas
> **Prompt:** Define the Pydantic v2 request and response schemas for the core prediction workflow in XAI-Guard. The SecurityEvent input schema captures all network flow features with strict type validation including IP address types, bounded port numbers, and an enum for protocol. The PredictionResponse returns attack type, confidence score, severity level, the model version that generated the prediction, inference latency, and the Celery task ID for the asynchronous explanation request.

#### Subphase 7.3 — XAI Explanation Schemas
> **Prompt:** Define the Pydantic v2 schemas for XAI explanations in XAI-Guard. Create a common base explanation schema with prediction reference, computation time, and stability score. Extend it into three specific schemas: SHAP explanation with feature names, SHAP values per feature, base value, and a top-K list of the most influential factors with direction; LIME explanation with feature contributions from the local linear surrogate; and attention explanation with per-time-step attention weights from the Transformer's last encoder layer.

#### Subphase 7.4 — Model Registry & Comparison Schemas
> **Prompt:** Define the Pydantic v2 schemas for model registry operations in XAI-Guard. Include: the model metadata response with version, framework, metrics, status, and registration timestamp; the Champion/Challenger status response showing both models side-by-side with their metrics and the performance delta between them; the nightly evaluation result schema; the promotion request schema with a required justification field; and the rollback request schema.

#### Subphase 7.5 — Alert & WebSocket Message Schemas
> **Prompt:** Define the Pydantic v2 schemas for alerts and real-time WebSocket messages in XAI-Guard. The alert schema includes all fields needed for analyst triage: severity, attack type, source and destination IPs, confidence, timestamp, acknowledgement status, MITRE ATT&CK technique information, and links to the prediction and explanation. Define the WebSocket message envelope schema wrapping alerts with a message type discriminator, payload, and server timestamp.

#### Subphase 7.6 — TypeScript Schema Mirroring
> **Prompt:** Design the TypeScript schema mirroring strategy for XAI-Guard. The goal is identical type definitions in both Python Pydantic schemas and TypeScript Zod schemas so that the frontend is always in sync with the API. The process is: FastAPI auto-generates an OpenAPI 3.1 spec; TypeScript Zod schemas are written to match; a contract test validates parity. Define where the shared TypeScript types live in the monorepo packages directory and how they are imported by both the dashboard and admin applications.

---

## Phase 8 — Frontend Application Architecture

**Context:** Design both the security dashboard and the admin panel architectures before any frontend code is written, establishing component boundaries, data fetching strategies, and the shared design system.

#### Subphase 8.1 — Shared Component Library Design
> **Prompt:** Design the shared React component library for XAI-Guard that is consumed by both the security dashboard and the admin panel. Define four component categories: data display components including charts using Recharts, tables, metric stat cards, and severity badges; XAI-specific components including a SHAP waterfall chart, LIME bar chart, and confidence gauge; form and interaction components; and layout components including sidebar and page containers. Establish the design system rules: dark-mode-first palette appropriate for SOC environments, typography scale, and spacing system.

#### Subphase 8.2 — Security Dashboard Architecture
> **Prompt:** Design the Next.js 14 App Router architecture for the XAI-Guard security dashboard serving analysts. Define four main sections: the live alert feed using a persistent WebSocket connection for real-time alert delivery; the threat detail view that opens when an analyst clicks an alert and shows the full Threat Detection card with the XAI explanation panel; the metrics overview showing live model performance and alert statistics; and the model status bar showing Champion and Challenger model info. Define the routing structure, the SWR data fetching strategy for polling endpoints, and the WebSocket client management approach.

#### Subphase 8.3 — Admin Panel Architecture
> **Prompt:** Design the Next.js 14 App Router architecture for the XAI-Guard admin panel serving data scientists and platform engineers. Define five main sections: the experiment browser showing all MLflow runs with filters; the model comparison view rendering the master comparison table from Phase 37; the Champion/Challenger management panel with promote and rollback controls; the drift monitoring panel showing drift score timeline; and the report generator exporting the research comparison as PDF and CSV. Define how role-based access control is enforced at the Next.js middleware level.

#### Subphase 8.4 — Real-Time Architecture Design
> **Prompt:** Design the end-to-end real-time alert delivery architecture for XAI-Guard. Trace the full path from event arrival to analyst notification: security event arrives at the ingestion endpoint, a Celery worker processes it and runs prediction, if the prediction exceeds the high-severity threshold an alert record is created and published to a Redis pub/sub channel, the WebSocket server's subscription to that channel pushes the alert to all connected clients, and the dashboard AlertsFeed component receives and displays the alert. Identify latency risks at each step and define the 10-second end-to-end latency budget.

#### Subphase 8.5 — Authentication & Authorization Flow
> **Prompt:** Design the authentication and authorization flow for XAI-Guard across the API, dashboard, and admin panel. The system has two roles: analyst with read-only access to the dashboard, and admin with full access to the admin panel including model promotion and rollback. Design the JWT token lifecycle, how tokens are stored in the browser, how Next.js middleware enforces route protection for both applications, how the FastAPI API validates tokens on every request, and how the admin panel renders different UI based on the current user's role.

#### Subphase 8.6 — Threat Detection Card Design Specification
> **Prompt:** Write the design specification for the XAI-Guard Threat Detection card — the primary UI component analysts interact with. The card must display: threat type with an icon, confidence percentage, severity badge using colour coding (critical in red, high in orange, medium in yellow, low in blue), a Why section showing the top four SHAP feature contributions as a horizontal bar list with percentage values and positive/negative indicators, a MITRE ATT&CK technique badge with a link, a recommended action statement, and source and destination IP information. Define the exact information hierarchy and interaction behaviour when the card is expanded.

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
| P7 | API Contract & Schema Strategy | 6 |
| P8 | Frontend Application Architecture | 6 |

**Next →** [02 — Data Engineering](02-data-engineering.md)