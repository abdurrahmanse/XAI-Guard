# 08 — Admin Panel, MLOps & Production

> **Phases 56–63** | XAI Panel and Metrics Dashboard, Admin Panel, Champion/Challenger UI, automated ML pipeline, observability, security hardening, CI/CD, Kubernetes, Terraform, production hardening, research report, and project completion.
>
> **How to use:** Pick one subphase. Copy its **Prompt** into your AI code editor. Implement it. Move to the next subphase.

---

## Phase 56 — XAI Panel & Metrics Dashboard Components

**Context:** These components complete the analyst dashboard. The XAI panel gives analysts the full explanation for a threat. The metrics dashboard gives situational awareness of model performance.

#### Subphase 56.1 — XAI Panel Component
> **Prompt:** Implement the XAIPanel component for the XAI-Guard security dashboard. The component accepts a prediction ID, fetches the SHAP explanation via the useExplanation SWR hook, and renders a full SHAP waterfall chart using Recharts horizontal BarChart with features on the y-axis and SHAP values on the x-axis. Positive contributions use red-warm colours and negative contributions use blue-cool colours. A base value reference line is drawn on the chart. While the explanation is loading show a skeleton placeholder.

#### Subphase 56.2 — SHAP/LIME Toggle
> **Prompt:** Add a SHAP/LIME explanation method toggle to the XAI-Guard XAIPanel component. When the analyst switches to LIME the component dispatches a LIME explanation request for the same prediction and polls for the result using the task ID. Display the explanation computation time for each method so analysts understand the speed trade-off. If the LIME explanation is not yet computed show an estimating indicator with elapsed time.

#### Subphase 56.3 — MetricsDashboard Component
> **Prompt:** Implement the MetricsDashboard component for the XAI-Guard security dashboard. The component fetches current model performance metrics from the API and displays: F1 macro and ROC-AUC as Recharts RadialBarChart gauges; precision and recall as large numeric stat cards; an AreaChart showing alerts per hour for the last 24 hours; and a PieChart showing attack type distribution for the last 24 hours. Refresh all metrics every 30 seconds using SWR polling.

#### Subphase 56.4 — Model Status Bar Component
> **Prompt:** Implement the ModelStatusBar component for the XAI-Guard security dashboard. This is a fixed strip at the top of every dashboard page showing: Champion model name and version with a green badge; Challenger model name and version with a blue badge if registered; the current drift score as a colour-coded gauge (green below 0.05, yellow 0.05 to 0.10, red above 0.10); and the timestamp of the last Champion evaluation. The status bar polls every 60 seconds using SWR.

#### Subphase 56.5 — Dashboard E2E Tests
> **Prompt:** Write Playwright end-to-end tests for the XAI-Guard security dashboard. Test the complete analyst workflow: analyst logs in, dashboard loads with ModelStatusBar visible, a simulated WebSocket alert arrives and appears in the AlertsFeed, analyst clicks the alert and ThreatDetailPanel opens, the XAI panel loads with a SHAP waterfall chart, analyst toggles to LIME and the LIME chart loads, and the MetricsDashboard shows current model performance. Run tests against the local development server with seeded data from Phase 4.

---

## Phase 57 — Admin Panel Foundation & Experiment Browser

**Context:** The admin panel serves data scientists and platform engineers. It is a separate Next.js application sharing the UI component library but with different routing, access requirements, and operational focus.

#### Subphase 57.1 — Admin App Setup & Layout
> **Prompt:** Set up the XAI-Guard admin panel as a separate Next.js 14 App Router application importing components from the shared packages/ui library. Configure the same dark-mode Tailwind theme as the dashboard. The admin layout sidebar has five navigation sections: Experiments, Model Comparison, Champion/Challenger, Drift Monitor, and Reports. Apply the authentication guard middleware and add an admin-only route guard that redirects analyst-role users back to the security dashboard.

#### Subphase 57.2 — RBAC Enforcement
> **Prompt:** Implement role-based access control enforcement in the XAI-Guard admin panel. The Next.js middleware reads the JWT role claim from the access token stored in an httpOnly cookie. If the role is analyst rather than admin, redirect all admin panel routes to the dashboard. Within admin panel pages, conditionally render destructive action buttons like Promote and Rollback only for admin-role users. Analyst-role users must never see these buttons even if they navigate directly.

#### Subphase 57.3 — ExperimentsTable Component
> **Prompt:** Implement the ExperimentsTable component for the XAI-Guard admin panel. The component fetches all registered MLflow experiment runs from the API and renders them in a sortable filterable table. Columns include: model name, dataset used, F1 macro, ROC-AUC, inference latency P99, training time in minutes, current status, and created date. Clicking a row opens a run detail drawer. Include filter controls for model family, dataset, and date range.

#### Subphase 57.4 — Run Detail Drawer
> **Prompt:** Implement the run detail drawer for the XAI-Guard admin panel. The drawer slides in from the right when a run row is clicked. It displays all logged MLflow parameters as a key-value list, all metrics, the DVC data tag used, the git commit SHA, and links to the model artifact in MLflow. Include a Register as Challenger button that calls the model registration service and transitions the model to challenger status in the registry.

#### Subphase 57.5 — Admin Routing Structure
> **Prompt:** Set up the complete routing structure for the XAI-Guard admin panel using Next.js 14 App Router. Define routes for experiments, model comparison, Champion/Challenger management, drift monitor, and report generator. Apply the authenticated and admin-only layout using a route group. Define loading skeleton components for data-heavy pages and error boundary components for each route segment that show a helpful message rather than a blank page.

---

## Phase 58 — Champion/Challenger Management UI

**Context:** The operational control centre for platform engineers to compare models, approve promotions, monitor drift, and export research reports.

#### Subphase 58.1 — ModelComparisonView Component
> **Prompt:** Implement the ModelComparisonView component for the XAI-Guard admin panel. The component fetches the master comparison table data and renders all six models as rows with all evaluation metrics as sortable columns including F1 macro, ROC-AUC, PR-AUC, recall, precision, per-attack F1, latency P99, memory, training time, and composite deployment score. The Champion row is highlighted in green and the Challenger row in blue. The best value in each column is bolded. Include a Download CSV button.

#### Subphase 58.2 — ChampionChallengerPanel Component
> **Prompt:** Implement the ChampionChallengerPanel component for the XAI-Guard admin panel. The panel shows Champion and Challenger side-by-side with key metrics: F1 macro, ROC-AUC, latency P99, peak memory, and last evaluation timestamp. Performance delta badges show whether the Challenger is ahead or behind on each metric using green for positive delta and red for negative delta. Below the comparison show the last 5 nightly evaluation results as a history table with timestamps and outcomes.

#### Subphase 58.3 — Promote Action with Confirmation
> **Prompt:** Implement the Promote action in the XAI-Guard ChampionChallengerPanel. The Promote button is rendered only for admin-role users. Clicking opens a confirmation modal showing which model becomes Champion, which is Archived, the performance delta justifying promotion, and a required text input for the promotion reason. The modal has Confirm and Cancel buttons. On confirm it shows a progress spinner then a success state with the new Champion name, or an error state with the failure reason.

#### Subphase 58.4 — Rollback Action with Confirmation
> **Prompt:** Implement the Rollback action in the XAI-Guard ChampionChallengerPanel for admin-role users only. The confirmation modal shows the current Champion being archived and the previous Champion being restored from history. Display a warning that the Challenger shadow evaluation data is preserved but automatic evaluation stops. Require the admin to type the word confirm before the Confirm button becomes enabled.

#### Subphase 58.5 — DriftMonitorPanel Component
> **Prompt:** Implement the DriftMonitorPanel component for the XAI-Guard admin panel. The panel shows a Recharts LineChart of MMD drift scores over the last 30 days with a dashed orange reference line at the WARNING threshold (0.05) and a dashed red reference line at the CRITICAL threshold (0.10). Below show the current drift status badge, timestamp of the last drift report, and whether the last report triggered an early Challenger evaluation. Include a table of the 10 most recent drift reports.

#### Subphase 58.6 — ReportGenerator Component
> **Prompt:** Implement the ReportGenerator component for the XAI-Guard admin panel with two export options. The first is a CSV export of the master model comparison table that downloads immediately as a Blob. The second is a PDF report generated using @react-pdf/renderer client-side containing: an executive summary with the key research finding, the full model comparison table, the per-attack-type heatmap as an embedded image, and the recommendations section. Show a progress bar while the PDF renders.

#### Subphase 58.7 — Admin Panel E2E Tests
> **Prompt:** Write Playwright end-to-end tests for the XAI-Guard admin panel. Test: admin login redirects to experiments page; ExperimentsTable loads all registered runs; clicking a run opens the detail drawer with correct metrics; ModelComparisonView renders all six models with Champion row highlighted; ChampionChallengerPanel shows the Promote button for admin role; an analyst-role user is redirected away from the admin panel; and DriftMonitorPanel renders the drift score chart with correct threshold lines.

---

## Phase 59 — Automated ML Training Pipeline

**Context:** Automate the complete ML lifecycle so the system continuously improves without manual intervention. Weekly scheduled runs and drift-triggered on-demand runs keep the Champion model current.

#### Subphase 59.1 — Pipeline Orchestration Script
> **Prompt:** Implement the XAI-Guard ML pipeline orchestration script that runs the full training workflow end-to-end. Stages execute in order: pull the latest DVC data version, run preprocessing, run feature engineering and selection, train all configured models, evaluate each model with the standard metrics harness, select the best candidate as Challenger, register all models in MLflow, and push pipeline outputs to DVC remote. Accept a models filter argument to train a subset of model families for targeted retraining.

#### Subphase 59.2 — GitHub Actions Weekly Schedule
> **Prompt:** Implement the GitHub Actions workflow for weekly automated ML training in XAI-Guard. The workflow triggers on a Sunday 02:00 UTC cron and on manual dispatch with an optional models filter input. It sets up the Python environment with uv, authenticates to the MinIO DVC remote, pulls the latest validated data version, runs the pipeline orchestration script, and sends a Slack webhook notification with the new model's key metrics. The workflow fails with a non-zero exit code if the pipeline health anomaly check triggers.

#### Subphase 59.3 — Drift-Triggered Retraining Task
> **Prompt:** Implement the drift-triggered retraining Celery task for XAI-Guard. When the drift module publishes a CRITICAL drift event this task runs the pipeline orchestration script for the Champion model family only to reduce retraining time. After completion the task automatically triggers the Challenger evaluation task from Phase 51. Log the triggering drift score and resulting model metrics to a pipeline_runs database table.

#### Subphase 59.4 — Pipeline Health Anomaly Detection
> **Prompt:** Implement pipeline health anomaly detection for the XAI-Guard training pipeline. After each run compare the new model's F1 macro against the previous successful run's F1 for the same model family. If the drop exceeds 5 percentage points, mark the run as anomalous, skip model registration to prevent a degraded model entering the registry, and send a high-priority webhook alert with the F1 delta, data version used, and a link to the MLflow run.

#### Subphase 59.5 — Pipeline Integration Test
> **Prompt:** Implement a pipeline integration test for XAI-Guard. The test runs the full orchestration script on a 500-sample synthetic dataset that exercises every stage. Verify: the pipeline completes without error, a new model version appears in the MLflow Model Registry, DVC push records a new pipeline output version, the pipeline health check passes on the synthetic dataset, and execution completes under 5 minutes. Run this test in CI on every pull request modifying the ML module.

---

## Phase 60 — Observability, Security Hardening & Testing

**Context:** Three quality pillars implemented together. Observability reveals security incidents. Security controls create testable behaviour. Coverage requirements enforce quality discipline.

#### Subphase 60.1 — Grafana Operational Dashboard
> **Prompt:** Implement the Grafana main operational dashboard configuration for XAI-Guard as a JSON provisioning file. Define panels for: requests per second, P99 prediction latency, prediction distribution by attack type as a pie chart, confidence score distribution as a histogram, current drift score per model as gauges, Champion model version as an info panel, Celery queue depth by queue name, and active alert counts by severity as stat panels.

#### Subphase 60.2 — Grafana Model Performance Dashboard
> **Prompt:** Implement the Grafana model performance dashboard for XAI-Guard using the PostgreSQL datasource to query the model_evaluations table directly. Define panels showing F1 macro and ROC-AUC per model over time as line charts with one line per model family. Add a heatmap panel showing per-attack-type F1 distribution refreshed after each Champion/Challenger evaluation. This is the primary operational view for monitoring model quality over time.

#### Subphase 60.3 — Grafana Alerting Rules
> **Prompt:** Configure Grafana alerting rules for XAI-Guard. Page immediately when: P99 latency exceeds 200 milliseconds sustained for 5 minutes; drift score exceeds the CRITICAL threshold; error rate exceeds 1 percent. Create warning tickets when: P99 latency exceeds 150 milliseconds; drift score exceeds the WARNING threshold; mean confidence drops more than 10 percent relative to the 7-day average; Celery queue depth exceeds 10,000. Route pages to PagerDuty and tickets to Slack.

#### Subphase 60.4 — OpenTelemetry Tracing
> **Prompt:** Configure OpenTelemetry distributed tracing for XAI-Guard. Instrument the FastAPI application, SQLAlchemy queries, Redis operations, and Celery tasks with OpenTelemetry spans. Configure the OTLP exporter to send traces to Jaeger. A complete prediction trace should display spans for: the HTTP handler, feature pipeline computation, model inference, async database write, and Celery task dispatch, enabling full per-stage latency visibility.

#### Subphase 60.5 — Rate Limiting Implementation
> **Prompt:** Implement rate limiting for the XAI-Guard API using slowapi. Apply per-IP rate limits: prediction endpoint at 100 requests per minute, explanation request at 10 requests per minute, event ingestion at 50 requests per minute, and auth login at 10 requests per minute to prevent credential stuffing. When the rate limit is exceeded return HTTP 429 with a Retry-After header and log the violation to the structured logging system.

#### Subphase 60.6 — Security Hardening
> **Prompt:** Apply security hardening to the XAI-Guard API. Run Bandit SAST and fix all HIGH and MEDIUM severity findings. Run OWASP ZAP baseline scan against the local Docker stack and fix all MEDIUM and above alerts. Verify all Pydantic input schemas have extra set to forbid. Confirm CORS configuration uses no wildcard origins. Verify all database queries use SQLAlchemy ORM with parameterised binding only. Document each finding and its fix in a security remediation log.

#### Subphase 60.7 — Test Coverage & Load Testing
> **Prompt:** Configure test coverage requirements and run a load testing baseline for XAI-Guard. Set the minimum coverage threshold to 80 percent for API and ML modules via pytest-cov with a CI failing gate. Then run a Locust load test ramping to 500 concurrent users over 5 minutes with tasks for event ingestion, predictions, alert polling, and WebSocket connections. Sustain for 10 minutes and record P50, P95, P99 latency, failure rate, and peak RPS. Document results as the performance baseline.

---

## Phase 61 — CI/CD Pipeline

**Context:** Automated quality gates ensure no code reaches production without passing lint, type checking, tests, security scanning, and build verification.

#### Subphase 61.1 — CI Quality & Test Workflow
> **Prompt:** Implement the XAI-Guard CI GitHub Actions workflow that runs on every pull request with parallel jobs: a quality job running ESLint, Prettier check, ruff, mypy, and commitlint; a test job running all unit and integration tests with coverage reporting failing if below 80 percent; a build job building all Docker images to verify compilation; a security job running Bandit and detect-secrets; and a container scanning job running trivy failing on any CRITICAL CVE findings.

#### Subphase 61.2 — CD Staging Workflow
> **Prompt:** Implement the XAI-Guard CD staging GitHub Actions workflow triggering automatically on every push to main. The workflow builds all Docker images tagged with the git SHA, pushes to the container registry, applies the staging Kubernetes Kustomize overlay, waits for the rollout using kubectl rollout status, runs the smoke test suite against staging, and sends a Slack notification. A failed deployment automatically redeploys the previous image tag to restore staging.

#### Subphase 61.3 — CD Production Workflow
> **Prompt:** Implement the XAI-Guard CD production GitHub Actions workflow that is manually triggered only. It accepts a specific Docker image tag as input validated in staging, requires approval from a designated reviewer via a GitHub environment protection rule, applies the production Kustomize overlay, waits for the rollout, runs the production smoke test suite, and sends a Slack notification. All production deployment events are logged to an audit trail.

#### Subphase 61.4 — Multi-Stage Docker Builds
> **Prompt:** Implement multi-stage Docker builds for all XAI-Guard services. The API Dockerfile uses a builder stage for installing Python dependencies with uv sync and a minimal python:3.11-slim runtime stage copying only the virtual environment and application code targeting under 500 MB. The Next.js Dockerfiles use standalone output mode with a node:20-alpine runtime stage targeting under 200 MB. Use build ARGs for configuration values that differ between environments.

#### Subphase 61.5 — ML Pipeline CI Workflow
> **Prompt:** Implement the XAI-Guard ML pipeline CI workflow running on every pull request that modifies the ML module. The workflow sets up the Python environment, pulls the DVC synthetic test data version, runs the full pipeline orchestration script on that data, and verifies the output models are registered in the MLflow test instance. This prevents ML pipeline regressions from reaching main without being caught by CI.

#### Subphase 61.6 — Branch Protection & Dependabot
> **Prompt:** Configure GitHub branch protection rules and Dependabot for XAI-Guard. Require all CI jobs to pass before merging to main and require at least one code review approval. Block direct pushes to main. Configure Dependabot to check npm, pip, and GitHub Actions dependency updates weekly and open automated pull requests for patch and minor updates. Configure Dependabot auto-merge for patch updates that pass all CI checks to reduce maintenance burden.

---

## Phase 62 — Kubernetes & Infrastructure as Code

**Context:** Deploy XAI-Guard to Kubernetes for production-grade orchestration. Define all cloud infrastructure as Terraform so the complete platform can be rebuilt from git in under 2 hours.

#### Subphase 62.1 — Base Kubernetes Manifests
> **Prompt:** Write the base Kubernetes manifests for XAI-Guard. Define Deployments for the FastAPI API, Celery workers, Next.js dashboard, and admin panel. Define StatefulSets for Redis and PostgreSQL each with a persistent volume claim. Define a Deployment for the MLflow Tracking Server. Configure resource requests and limits for every workload. Add liveness and readiness probes to every service using the /v1/health endpoint or service-specific health checks.

#### Subphase 62.2 — Kustomize Overlays
> **Prompt:** Implement Kustomize overlays for XAI-Guard staging and production environments. The staging overlay patches replica counts to one per deployment, uses smaller resource limits, and patches the image tag with the CI-built SHA. The production overlay sets minimum two replicas for API and Celery worker, uses production resource limits, and locks the image tag to the approved version. Both overlays reference the base manifests using kustomization.yaml with strategic merge patches.

#### Subphase 62.3 — Horizontal Pod Autoscaler & PodDisruptionBudget
> **Prompt:** Configure Horizontal Pod Autoscaler and PodDisruptionBudget for the XAI-Guard API and Celery worker. The API HPA scales between 2 and 10 replicas based on 70 percent CPU utilisation. The Celery worker HPA scales between 2 and 8 replicas based on the custom queue depth metric exposed via the Prometheus Adapter. Configure PodDisruptionBudget for both deployments with minAvailable of 1 to ensure at least one pod remains available during node drains and rolling updates.

#### Subphase 62.4 — TLS, Ingress & cert-manager
> **Prompt:** Configure TLS and ingress for XAI-Guard Kubernetes deployment. Install cert-manager and create a ClusterIssuer using Let's Encrypt ACME for automated certificate provisioning and renewal. Define an nginx-ingress Ingress resource routing requests to the API, dashboard, and admin panel by path prefix. Annotate the Ingress so cert-manager automatically manages the TLS certificate. Configure nginx to redirect all HTTP traffic to HTTPS.

#### Subphase 62.5 — Terraform Infrastructure Modules
> **Prompt:** Write reusable Terraform modules for the XAI-Guard cloud infrastructure on AWS. Create modules for: VPC with public and private subnets and NAT gateway; EKS cluster with a managed node group supporting on-demand and spot instances; RDS PostgreSQL 16 with Multi-AZ and 7-day automated backup retention; ElastiCache Redis 7 accessible only within the VPC; S3 bucket for DVC and MLflow artifacts with versioning and server-side encryption; and ECR repositories for each service image with lifecycle policies for old image cleanup.

#### Subphase 62.6 — Terraform Environments & IRSA
> **Prompt:** Implement Terraform environment compositions for XAI-Guard staging and production. Staging uses t3.medium EKS nodes and db.t3.medium RDS in a single AZ to minimise cost. Production uses m5.large EKS nodes and db.r6g.large RDS with Multi-AZ. Configure IRSA granting the API pod read access to the S3 artifacts bucket and the Celery worker pod read and write access. Follow least privilege with no wildcard IAM actions anywhere in the configuration.

---

## Phase 63 — Production Hardening, Research Report & Project Completion

**Context:** The final phase: SLOs, disaster recovery, the research paper, acceptance testing, and the v1.0.0 release that formally completes the XAI-Guard project.

#### Subphase 63.1 — SLO Definition & Burn Rate Alerting
> **Prompt:** Define the XAI-Guard Service Level Objectives and configure burn rate alerting. Define five SLOs: availability at 99.9 percent over a 30-day rolling window; prediction latency P99 below 100 milliseconds; error rate below 0.1 percent; alert delivery freshness below 10 seconds end-to-end from event ingestion to WebSocket delivery; and explanation latency P99 below 500 milliseconds. Implement multi-window multi-burn-rate alerting in Grafana: fast burn pages immediately for high error budget consumption, slow burn creates a warning ticket for sustained consumption.

#### Subphase 63.2 — Disaster Recovery Runbook
> **Prompt:** Write the XAI-Guard disaster recovery runbook covering four scenarios with concrete step-by-step recovery instructions. Scenario one database failure: restore from RDS automated backup to a specific timestamp targeting RTO under 4 hours. Scenario two model registry loss: re-pull artifacts from MinIO and re-register in MLflow targeting RTO under 1 hour. Scenario three Kubernetes namespace corruption: reapply the production Kustomize overlay targeting RTO under 30 minutes. Scenario four complete cluster loss: run Terraform apply then Kubernetes manifests then DVC pull targeting RTO under 2 hours.

#### Subphase 63.3 — Graceful Degradation
> **Prompt:** Implement graceful degradation for the XAI-Guard API. When ML inference is unavailable or model loading fails the prediction endpoint falls back to a rule-based heuristic classifier that maps threshold conditions on key features to attack type classifications with a fixed conservative confidence score. The dashboard displays a prominent warning banner when operating in degraded mode. All degraded-mode predictions are flagged in the database so they can be excluded from model evaluation metrics.

#### Subphase 63.4 — Research Paper
> **Prompt:** Write the XAI-Guard research paper structured as a formal academic paper with the following sections: Abstract of 250 words covering problem, approach, key finding, and practical implication; Introduction with research motivation and the eight sub-questions; Related Work citing all four datasets, SHAP, LIME, Attention Rollout, and relevant IDS and XAI literature; Methodology describing all six models, four datasets, and the three-pillar evaluation framework; Results presenting all quantitative findings from Phase 37 with tables and figures; Discussion answering each research sub-question with specific numbers and statistical significance values from Phase 38; and Conclusion with practical deployment recommendations.

#### Subphase 63.5 — Reproducibility Guide
> **Prompt:** Write the XAI-Guard reproducibility guide enabling anyone to reproduce every research paper result from only the git repository tag and DVC remote access. Provide step-by-step commands: clone the repository at the v1.0.0 tag, install all dependencies using uv sync and pnpm install, pull the exact DVC data version, run the full ML pipeline using the orchestration script, and view results in the MLflow UI cross-referenced with the paper's reported numbers. Document the hardware used for original experiments, all random seeds, and expected result variance across runs.

#### Subphase 63.6 — End-to-End Acceptance Test
> **Prompt:** Run the XAI-Guard end-to-end acceptance test to formally verify the production system. Replay 10,000 real CICIDS-2017 events at 500 events per second using the event replay script. Verify: all CRITICAL and HIGH alerts appear in the analyst dashboard within 10 seconds; the attack type classification F1 on the replayed events is at or above the reported paper value; clicking an alert shows the Threat Detection card with a loaded SHAP explanation; Prometheus metrics update correctly; and Grafana dashboards show live data. Document all results in an acceptance test report.

#### Subphase 63.7 — Future Roadmap & v1.0.0 Release
> **Prompt:** Write the XAI-Guard future roadmap and prepare the v1.0.0 release. The roadmap prioritises seven future research directions: LLM-based natural language explanation generation from SHAP values; online learning for incremental model updates without full retraining; federated learning for cross-organisation training without sharing raw event data; Graph Neural Network model for lateral movement and multi-hop attack detection; multi-modal detection combining network flows with system call sequences; an active learning loop where analyst feedback continuously improves the model; and Kafka streaming for high-throughput ingestion above 100,000 events per second. Tag the repository as v1.0.0 and write a CHANGELOG listing all 63 phases.

---

## Complete 63-Phase Map

| # | Phase | Doc |
|---|-------|-----|
| 1 | Research Statement & Evaluation Framework | 01 |
| 2 | Project Charter & Scope | 01 |
| 3 | Monorepo & Developer Environment | 01 |
| 4 | Infrastructure Services Setup | 01 |
| 5 | Database Schema & ORM Layer | 01 |
| 6 | Modular Monolith Architecture Design | 01 |
| 7 | API Contract & Schema Strategy | 01 |
| 8 | Frontend Application Architecture | 01 |
| 9 | Dataset Strategy & Acquisition | 02 |
| 10 | NSL-KDD EDA | 02 |
| 11 | CICIDS-2017 EDA | 02 |
| 12 | UNSW-NB15 EDA | 02 |
| 13 | BETH EDA | 02 |
| 14 | Cross-Dataset Schema Mapping | 02 |
| 15 | Data Cleaning Pipeline | 02 |
| 16 | Encoding & Scaling Pipeline | 02 |
| 17 | Class Imbalance Handling | 02 |
| 18 | Network Feature Engineering | 03 |
| 19 | Temporal Feature Engineering | 03 |
| 20 | Behavioral Feature Engineering | 03 |
| 21 | Threat Intel Feature Stubs | 03 |
| 22 | Feature Selection & Validation | 03 |
| 23 | Sequence Data Construction | 03 |
| 24 | DVC Pipeline Setup | 03 |
| 25 | MLflow Experiment Tracking | 03 |
| 26 | Common Model Interface Design | 04 |
| 27 | Logistic Regression Baseline | 04 |
| 28 | Random Forest Model | 04 |
| 29 | XGBoost Model & Champion Registration | 04 |
| 30 | LSTM Architecture | 04 |
| 31 | LSTM Training & Optimisation | 04 |
| 32 | LSTM Evaluation | 04 |
| 33 | Transformer Encoder Architecture | 05 |
| 34 | Transformer Encoder Training | 05 |
| 35 | Lightweight Transformer & Knowledge Distillation | 05 |
| 36 | Quantisation & Deployment Profiling | 05 |
| 37 | Cross-Model Comparative Analysis | 05 |
| 38 | Statistical Significance Testing | 05 |
| 39 | SHAP Explainability Implementation | 05 |
| 40 | LIME Explainability | 06 |
| 41 | Attention Explainability | 06 |
| 42 | XAI Stability & Cross-Method Agreement | 06 |
| 43 | Human-Centred XAI Evaluation | 06 |
| 44 | Robustness Testing | 06 |
| 45 | Drift Detection System | 06 |
| 46 | Modular Monolith Core Layer | 06 |
| 47 | Auth Module | 06 |
| 48 | Events Module | 07 |
| 49 | Predictions Module | 07 |
| 50 | Explanations Module | 07 |
| 51 | Model Registry Module | 07 |
| 52 | Alerts & WebSocket Module | 07 |
| 53 | Threat Intelligence Module | 07 |
| 54 | Dashboard Foundation & Layout | 07 |
| 55 | Alert Feed & Threat Detail Components | 07 |
| 56 | XAI Panel & Metrics Dashboard | 08 |
| 57 | Admin Panel Foundation & Experiment Browser | 08 |
| 58 | Champion/Challenger Management UI | 08 |
| 59 | Automated ML Training Pipeline | 08 |
| 60 | Observability, Security Hardening & Testing | 08 |
| 61 | CI/CD Pipeline | 08 |
| 62 | Kubernetes & Infrastructure as Code | 08 |
| 63 | Production Hardening, Research Report & Launch | 08 |

**Previous ←** [07 — Backend Domain Modules & Dashboard](07-mlops-security-testing-and-performance.md)

*End of XAI-Guard implementation guide. 63 phases. 350+ prompt-driven subphases. Modular monolith API. Production-grade.*
