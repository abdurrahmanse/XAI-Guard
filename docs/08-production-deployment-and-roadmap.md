# 08 — Production Deployment & Roadmap

> **Phases 32 · 33 · 34 · 35 · 36 · 37** — Kubernetes deployment, Terraform IaC, live threat intelligence, research documentation, SLA hardening, and project completion.

---

## Phase 32 — Kubernetes Deployment

**Goal:** Deploy the full XAI-Guard platform to Kubernetes for production-grade orchestration, horizontal scaling, and self-healing.

**Context:** Kubernetes (k8s) provides everything required for enterprise production: rolling deployments with zero downtime, horizontal pod autoscaling based on CPU or custom metrics, self-healing on crash, namespace isolation between staging and production. The three deployable service types are: stateless API pods (scale out), Celery worker pods (scale by queue depth), and frontend pods (scale out + CDN-cacheable).

**Tools:** Kubernetes 1.29+, Helm 3, Kustomize (environment overlays), `kubectl`, Horizontal Pod Autoscaler (HPA), Prometheus Adapter (custom metrics HPA)

**Tasks:**

- [ ] 32.1 Write `infrastructure/k8s/base/` manifests:
  ```
  infrastructure/k8s/base/
  ├── api-deployment.yaml        # FastAPI, 2 replicas base
  ├── api-service.yaml           # ClusterIP
  ├── celery-deployment.yaml     # Celery workers, 2 replicas base
  ├── web-deployment.yaml        # Next.js dashboard
  ├── admin-deployment.yaml      # Next.js admin
  ├── redis-statefulset.yaml     # Redis (single pod, persistent volume)
  ├── postgres-statefulset.yaml  # PostgreSQL (single pod, persistent volume)
  ├── mlflow-deployment.yaml     # MLflow tracking server
  ├── configmap.yaml             # Non-secret configuration
  ├── secrets.yaml               # Encrypted secrets (sealed-secrets)
  ├── ingress.yaml               # nginx-ingress with TLS (cert-manager)
  └── kustomization.yaml
  ```
- [ ] 32.2 Write Kustomize overlays:
  - `infrastructure/k8s/overlays/staging/`: 1 API replica, `resources.limits.cpu=1`, image tag from CI
  - `infrastructure/k8s/overlays/production/`: 3 API replicas, `resources.limits.cpu=2`, image tag locked to approved version
- [ ] 32.3 Configure HPA for `api` Deployment:
  ```yaml
  apiVersion: autoscaling/v2
  kind: HorizontalPodAutoscaler
  spec:
    minReplicas: 2
    maxReplicas: 10
    metrics:
      - type: Resource
        resource: {name: cpu, target: {type: Utilization, averageUtilization: 70}}
      - type: Pods
        pods:
          metric: {name: xaiguard_celery_queue_depth}
          target: {type: AverageValue, averageValue: 100}
  ```
- [ ] 32.4 Set resource requests/limits:
  - `api` pod: request=`500m CPU / 512Mi RAM`, limit=`2 CPU / 2Gi RAM`
  - `celery-worker` pod: request=`1 CPU / 1Gi RAM`, limit=`4 CPU / 4Gi RAM`
  - `web`/`admin` pods: request=`100m CPU / 128Mi RAM`, limit=`500m CPU / 512Mi RAM`
- [ ] 32.5 Configure `PodDisruptionBudget` for `api` and `celery-worker`:
  ```yaml
  spec:
    minAvailable: 1  # always at least 1 pod running during voluntary disruptions (node drain, rolling update)
  ```
- [ ] 32.6 Configure TLS: install `cert-manager` in cluster; use `ClusterIssuer` with Let’s Encrypt (or internal CA for enterprise); annotate `Ingress` with `cert-manager.io/cluster-issuer`
- [ ] 32.7 Write Helm chart `infrastructure/helm/xai-guard/` with `values.yaml` exposing: `image.tag`, `replicaCount`, `resources`, `ingress.host`, `secrets` (ref to k8s Secret)
- [ ] 32.8 Write `infrastructure/docs/deployment-runbook.md`:
  - How to deploy to staging: `kubectl apply -k infrastructure/k8s/overlays/staging/`
  - How to deploy to production: `kubectl apply -k infrastructure/k8s/overlays/production/`
  - How to scale manually: `kubectl scale deployment api --replicas=5`
  - How to roll back: `kubectl rollout undo deployment/api`
- [ ] 32.9 Validate: deploy to local `kind` cluster (`kind create cluster`); run smoke tests against kind deployment; verify HPA triggers on simulated load

**Output:** Full k8s manifests; Helm chart; HPA with custom metrics; staging + production Kustomize overlays; deployment runbook; kind validation passing

---

## Phase 33 — Terraform Infrastructure-as-Code

**Goal:** All cloud infrastructure is defined, versioned, and reproducible as code — the entire platform can be rebuilt from git in < 30 minutes.

**Context:** Infrastructure-as-Code ensures auditability (every change is a git commit), reproducibility (disaster recovery), and eliminates configuration drift. Terraform is the standard for multi-cloud IaC. AWS EKS is the default target; equivalent modules for GCP GKE and Azure AKS are noted where they differ.

**Tools:** Terraform 1.7+, AWS provider (`hashicorp/aws`), S3 remote state, DynamoDB state locking

**Tasks:**

- [ ] 33.1 Write reusable Terraform modules in `infrastructure/terraform/modules/`:
  - `vpc/`: VPC, public + private subnets, NAT gateway, security groups
  - `eks-cluster/`: EKS cluster + managed node group (on-demand + spot mix), OIDC provider
  - `rds-postgres/`: RDS PostgreSQL 16, Multi-AZ enabled, automated backups 7-day retention
  - `elasticache-redis/`: Redis 7 cluster, in-VPC only
  - `s3-bucket/`: S3 bucket for DVC + MLflow artifacts; versioning enabled; server-side encryption
  - `ecr/`: Elastic Container Registry per service (api, web, admin)
- [ ] 33.2 Write environment compositions:
  - `infrastructure/terraform/environments/staging/main.tf`: composes modules with smaller instance types (t3.medium nodes, db.t3.medium)
  - `infrastructure/terraform/environments/production/main.tf`: composes modules with production sizing (m5.large nodes, db.r6g.large, Multi-AZ)
- [ ] 33.3 Configure remote state:
  ```hcl
  terraform {
    backend "s3" {
      bucket         = "xai-guard-terraform-state"
      key            = "production/terraform.tfstate"
      region         = "us-east-1"
      dynamodb_table = "xai-guard-terraform-locks"
      encrypt        = true
    }
  }
  ```
- [ ] 33.4 Write `infrastructure/terraform/variables.tf` exposing: `aws_region`, `cluster_size` (min/max nodes), `db_instance_class`, `environment`, `domain_name`
- [ ] 33.5 Configure IRSA (IAM Roles for Service Accounts):
  - `api` service account → IAM role with: `s3:GetObject` on artifacts bucket, `ecr:GetDownloadUrlForLayer`
  - `celery-worker` service account → same + `s3:PutObject` (artifact writes)
  - No wildcard `*` actions; principle of least privilege
- [ ] 33.6 GitHub Actions `terraform.yml` workflow:
  ```yaml
  on:
    pull_request:  # terraform plan (comment plan on PR)
    push:
      branches: [main]  # terraform apply (staging only; production requires manual approval)
  ```
- [ ] 33.7 Write `infrastructure/terraform/README.md`: `terraform init`, `terraform plan`, `terraform apply` instructions for each environment; note differences for GCP (`google` provider, GKE) and Azure (`azurerm` provider, AKS)

**Output:** Terraform modules for all infrastructure; remote state; IRSA least-privilege; plan-on-PR + apply workflow

---

## Phase 34 — Live Threat Intelligence Integration

**Goal:** Wire real-world threat intelligence feeds into the feature pipeline to enrich every prediction with live IP reputation and MITRE ATT&CK taxonomy.

**Context:** The stub threat intel features from Phase 8 are now replaced with live API integrations. IP reputation enrichment improves recall on known-bad actors and gives analysts immediately actionable context (“This IP is known to be a Tor exit node with AbuseIPDB confidence score 95”). MITRE ATT&CK mapping surfaces the attack technique directly in the dashboard.

**Tools:** `httpx` (async HTTP), Redis (TTL cache), AbuseIPDB API, MITRE ATT&CK STIX data (downloaded), Celery periodic task

**Tasks:**

- [ ] 34.1 Write `services/api/services/threat_intel.py` — `ThreatIntelService`:
  ```python
  class ThreatIntelService:
      async def get_ip_reputation(self, ip: str) → IPReputationResult:
          # Check Redis: GET threat_intel:ip:{ip}
          # On miss: call AbuseIPDB API
          # Cache result with TTL=3600 (1 hour)
          # Returns: {score: 0-100, is_whitelisted, usage_type, country_code, isp}

      async def is_tor_exit_node(self, ip: str) → bool:
          # Check against downloaded TorDNSEL list (updated daily)
          # Cached in Redis as a Set: SISMEMBER tor_exit_nodes {ip}

      def get_mitre_attack_technique(self, attack_type: AttackType) → MITREResult:
          # Static mapping (no API call)
          # Returns: {technique_id, technique_name, tactic, tactic_id}
          # e.g. BruteForce → T1110 Brute Force / TA0006 Credential Access
  ```
- [ ] 34.2 Replace stub functions in `ml/src/features/threat_intel_features.py`:
  - `known_malicious_ip_flag(ip)` → calls `ThreatIntelService.get_ip_reputation(ip).score / 100`
  - `known_tor_exit_node_flag(ip)` → calls `ThreatIntelService.is_tor_exit_node(ip)`
  - Note: feature pipeline calls these synchronously; service returns cached values (no API latency in hot path)
- [ ] 34.3 Async enrichment Celery task `enrich_event_with_threat_intel`:
  - Called for every stored event (after prediction, not blocking it)
  - Fetches live IP reputation and stores in `security_events.threat_intel_data` JSONB column
- [ ] 34.4 Celery Beat task `refresh_threat_intel_cache` (runs hourly):
  - Fetch top 1000 most frequent source IPs from last 24h
  - Pre-fetch AbuseIPDB reputation for all 1000 → warm Redis cache
  - Download updated Tor exit node list → refresh Redis Set
- [ ] 34.5 Wire `MITREResult` into the Threat Detection card in `apps/web` (`ThreatDetailPanel`):
  - Show MITRE ATT&CK badge: `T1110 • Brute Force • Credential Access`
  - Link to `attack.mitre.org` technique page
- [ ] 34.6 Write integration tests with `httpx` mock (pytest `respx` library) for all threat intel API calls
- [ ] 34.7 Add `ABUSEIPDB_API_KEY` to all environment configs; document rate limits (free tier: 1000/day; paid: 100k/day)

**Output:** Live threat intel in feature pipeline (cached); MITRE ATT&CK mapping in dashboard; pre-warming cache job

---

## Phase 35 — Research Report & Academic Documentation

**Goal:** Produce the definitive research paper documenting findings, methodology, and evidence — suitable for academic submission or enterprise research report.

**Context:** XAI-Guard is a research platform. Its core contribution is the systematic, evidence-based comparison of six models across prediction, explainability, and operational dimensions for cybersecurity. The research report must be rigorous, reproducible, and backed by statistical evidence. It answers all 8 research questions with data from Phases 10–20.

**Tasks:**

- [ ] 35.1 Write `docs/research-paper.md` structured as an academic paper:
  - **Abstract** (250 words): problem, approach, key finding, implication
  - **Introduction**: cybersecurity ML landscape, the explainability gap, research questions
  - **Related Work**: IDS/IPS ML literature, XAI for security, Transformer applications in security
  - **Methodology**: datasets, models, evaluation framework, experimental setup (hardware, seeds, splits)
  - **Results**: all quantitative results (referenced from Phase 16 artifacts)
  - **Discussion**: interpret results, limitations, threats to validity
  - **Conclusion**: direct answers to each RQ, practical recommendations
  - **References**: cite NSL-KDD, CICIDS-2017, UNSW-NB15, BETH papers; SHAP paper (Lundberg & Lee 2017); LIME paper (Ribeiro et al. 2016); Attention Rollout; relevant IDS/XAI papers
- [ ] 35.2 Include the following figures/tables directly in the paper:
  - Table 1: Master model comparison (Phase 16)
  - Table 2: McNemar significance test results
  - Figure 1: System architecture diagram (Phase 4)
  - Figure 2: Per-attack-type F1 heatmap (Phase 16)
  - Figure 3: XAI Trade-off Matrix radar chart (Phase 19)
  - Figure 4: F1 vs XAI Quality scatter plot (RQ5, Phase 19)
  - Figure 5: Pareto efficiency frontier (Phase 15)
  - Figure 6: Temporal drift degradation (Phase 20)
- [ ] 35.3 Write explicit answers to all 8 Research Questions in `docs/research-paper.md#discussion`:
  - **RQ1**: Classical ML vs Deep Learning → which model family wins and by what margin
  - **RQ2**: LSTM vs Transformer → which captures temporal patterns better
  - **RQ3**: Large Transformer cost justification → compute cost / F1 gain ratio
  - **RQ4**: Best XAI method → which method analysts rated most actionable
  - **RQ5**: Performance vs explanation trade-off → Pareto frontier analysis
  - **RQ6**: Cost-efficient deployment model → Pareto efficiency scores
  - **RQ7**: Cross-attack generalisation → per-attack heatmap findings
  - **RQ8**: Drift robustness → temporal drift and cross-dataset generalisation gap
- [ ] 35.4 Write `docs/reproducibility-guide.md`:
  ```bash
  # Step 1: Clone and setup
  git clone https://github.com/org/xai-guard && cd xai-guard
  git checkout v1.0.0
  pnpm install && uv sync

  # Step 2: Pull data
  dvc pull

  # Step 3: Run full ML pipeline
  uv run python ml/src/pipeline.py

  # Step 4: View results in MLflow
  mlflow ui --backend-store-uri postgresql://...
  ```
- [ ] 35.5 Archive all referenced artifacts:
  - DVC tag: `dvc tag data-v1.0-paper`
  - MLflow experiment IDs for each model’s best run: document in `docs/experiment-archive.md`
  - Export all paper figures as 300 DPI PNGs: `ml/artifacts/figures/`

**Output:** `docs/research-paper.md`; `docs/reproducibility-guide.md`; `docs/experiment-archive.md`; all paper figures exported

---

## Phase 36 — Production Hardening & SLA Definition

**Goal:** Define and enforce production SLAs; complete all remaining hardening before go-live.

**Context:** Enterprise production systems require formally defined Service Level Objectives (SLOs). SLOs are measured by Prometheus and alert when the error budget is burning too fast. Disaster recovery, graceful degradation, and a final security audit ensure the platform can handle production failures safely.

**Tasks:**

- [ ] 36.1 Define SLOs (document in `infrastructure/docs/slos.md`):
  | SLO | Target | Measurement |
  |-----|--------|-------------|
  | Availability | 99.9% (max 8.7 hours downtime/year) | `1 - error_rate` over 30d rolling |
  | Prediction P99 Latency | < 100 ms | `histogram_quantile(0.99, ...)` |
  | Error Rate | < 0.1% | `rate(http_5xx_total) / rate(http_requests_total)` |
  | Alert Freshness | < 10 seconds | `event_timestamp - alert_dashboard_timestamp` |
  | Explanation P99 | < 500 ms | Celery task duration P99 |

- [ ] 36.2 Implement SLO burn rate alerting in Grafana:
  - **Fast burn** (immediate action required): consuming > 5% of 30-day error budget in 1 hour → PAGE
  - **Slow burn** (investigate soon): consuming > 2% of budget per day → TICKET
  - Configure Grafana alert rules using multi-window, multi-burn-rate method (Google SRE book)

- [ ] 36.3 Write `infrastructure/docs/disaster-recovery.md`:
  - **DB failure**: restore from RDS automated backup (`aws rds restore-db-instance-to-point-in-time`); target RTO < 4 hours
  - **Model registry loss**: re-pull from MinIO; re-register in MLflow; target RTO < 1 hour
  - **k8s namespace corruption**: `kubectl apply -k infrastructure/k8s/overlays/production/`; target RTO < 30 minutes
  - **Complete cluster loss**: `terraform apply` + k8s manifests + DVC pull; target RTO < 2 hours

- [ ] 36.4 Implement automated DB backup:
  - AWS RDS: enable automated backups with 30-day retention (or equivalent pg_dump Kubernetes CronJob for self-hosted)
  - Monthly restore drill: scheduled GitHub Actions workflow that restores from backup to a test DB and verifies row counts

- [ ] 36.5 Implement graceful degradation:
  - If ML inference service unavailable (health check fails): `services/api` falls back to a rule-based heuristic:
    ```python
    HEURISTIC_RULES = [
        Rule(condition=lambda e: e.failed_login_rate_5min > 10, attack_type='brute_force', confidence=0.70),
        Rule(condition=lambda e: e.unique_dest_ports_per_src > 100, attack_type='port_scan', confidence=0.65),
    ]
    ```
  - Dashboard shows a banner: `⚠️ ML model offline — rule-based detection active`
  - No silent failures — analyst always knows detection mode

- [ ] 36.6 Conduct tabletop security exercise (document findings in `docs/security-exercise-report.md`):
  - Scenario A: Compromised analyst account → mitigations: JWT rotation, suspicious login alerting
  - Scenario B: Poisoned model artifact in MinIO → mitigations: artifact signing, checksum verification on load
  - Scenario C: Data exfiltration via XAI explanation API → mitigations: rate limiting, data masking on IPs in explanations

- [ ] 36.7 Final pre-launch security audit checklist (`docs/security-audit-checklist.md`):
  - [ ] All endpoints require authentication except `/v1/health`
  - [ ] HTTPS enforced (HTTP redirects to HTTPS)
  - [ ] No secrets in environment (detect-secrets scan clean)
  - [ ] Bandit scan clean
  - [ ] OWASP ZAP scan clean
  - [ ] Rate limiting active on all public endpoints
  - [ ] DB credentials rotated from development values
  - [ ] Container images scanned (trivy clean)
  - [ ] Graceful degradation tested

**Output:** SLOs defined + measured; burn rate alerting; disaster recovery runbook; automated backups; graceful degradation; security exercise report; pre-launch audit checklist completed

---

## Phase 37 — Project Completion & Future Roadmap

**Goal:** Final end-to-end validation, stakeholder sign-off, and a clear roadmap for future research and engineering enhancements.

**Context:** This is the final phase. The platform is in production, the research report is written, and all 37 phases are complete. This phase formally closes the project with an acceptance test and defines the next evolution of XAI-Guard.

**Tasks:**

- [ ] 37.1 Run full end-to-end acceptance test:
  1. Replay 10,000 CICIDS-2017 events via `services/api/scripts/replay_events.py` at 500 events/sec
  2. Verify: all alerts appear in dashboard within 10 seconds
  3. Verify: attack type classifications match ground-truth labels with F1 ≥ reported value in research paper
  4. Verify: clicking an alert shows XAI panel with SHAP explanation loaded
  5. Verify: Champion model version displayed in dashboard matches Model Registry
  6. Verify: Prometheus metrics updating; Grafana dashboard shows live data
  7. Document results in `docs/acceptance-test-report.md`

- [ ] 37.2 Conduct stakeholder demo (prepare `docs/demo-script.md`):
  - **Segment 1** (5 min): Dashboard walkthrough — live alert feed, severity triage, Threat Detection card
  - **Segment 2** (5 min): XAI panel — SHAP waterfall for a BruteForce attack, explain the “Why?” in plain language
  - **Segment 3** (5 min): Research findings — model comparison table, key finding (which model won and why)
  - **Segment 4** (3 min): Champion/Challenger — show Challenger evaluation panel, explain promotion criteria
  - **Segment 5** (2 min): Future roadmap

- [ ] 37.3 Write `docs/lessons-learned.md`:
  - What worked: (e.g., Optuna + MLflow integration, DVC reproducibility, pnpm workspaces for monorepo)
  - What was harder than expected: (e.g., SHAP for deep models is slow, CICIDS-2017 data quality issues)
  - Unexpected findings: (e.g., XGBoost outperforms Transformer on CICIDS-2017 tabular data despite Transformer’s parameter count)
  - Process improvements for next project

- [ ] 37.4 Write `docs/future-roadmap.md` — priority-ordered future enhancements:
  - **P1 — LLM-Based Explanation Generation**: Fine-tune Gemma-2B or Mistral-7B to generate natural language threat summaries from SHAP values. “This looks like a brute-force attack because the failed login rate is 47 attempts/minute from a Tor exit node.”
  - **P2 — Online Learning**: Incremental model updates (scikit-learn `partial_fit`, PyTorch streaming) without full retraining. Reduces retraining cycle from weekly to hourly.
  - **P3 — Federated Learning**: Train across multiple organisations’ data without sharing raw events. Use Flower (flwr) framework. Addresses the “I can’t share my logs” enterprise objection.
  - **P4 — Graph Neural Network Model**: Model network topology as a graph (nodes=hosts, edges=connections). GNN can detect lateral movement patterns invisible to per-event models.
  - **P5 — Multi-Modal Detection**: Combine network flow features + system call sequences + process trees. Each modality has a separate encoder; outputs fused before classification.
  - **P6 — Active Learning Loop**: Analyst marks false positives/negatives in the dashboard. These corrections feed back into retraining. Model improves from analyst expertise continuously.
  - **P7 — Streaming Architecture**: Replace Redis Streams with Apache Kafka for > 100k events/sec throughput. Add Flink for real-time feature aggregation.

- [ ] 37.5 Tag the repository:
  ```bash
  git tag -a v1.0.0 -m "XAI-Guard v1.0.0 — production release"
  git push origin v1.0.0
  ```
  Write `CHANGELOG.md` with all 37 phases as entries

- [ ] 37.6 Archive final state:
  ```bash
  dvc tag data-v1.0-final  # Tag DVC data state
  dvc push                  # Push all artifacts to MinIO
  ```
  Document all MLflow experiment IDs for each model in `docs/experiment-archive.md` (update from Phase 35)

- [ ] 37.7 Update `README.md` with final project summary:
  - Link to `docs/research-paper.md`
  - Link to demo video (if recorded)
  - Link to `docs/architecture-diagram.md`
  - Add badges: CI status, coverage %, model Champion name + F1 score

**Output:** Acceptance test passed; stakeholder demo complete; lessons learned documented; future roadmap written; v1.0.0 tagged; CHANGELOG.md written

---

## Complete Phase Overview

| # | Phase | Doc | Key Deliverable |
|---|-------|-----|-----------------|
| 1 | Research Scoping | 01 | Research statement, evaluation framework |
| 2 | Monorepo Setup | 01 | Working dev environment |
| 3 | Infrastructure Baseline | 01 | Docker Compose, PostgreSQL, MLflow |
| 4 | System Architecture | 02 | Architecture diagram, API contracts |
| 5 | API Contract & Schemas | 02 | OpenAPI spec, Pydantic + Zod schemas |
| 6 | Dataset Acquisition & EDA | 03 | 4 EDA notebooks, schema mappings |
| 7 | Preprocessing Pipeline | 03 | `ml/src/preprocessing/` module |
| 8 | Feature Engineering | 03 | `ml/src/features/` module |
| 9 | Versioning & Tracking | 03 | DVC pipeline, MLflow configured |
| 10 | Logistic Regression | 04 | Baseline model, metrics |
| 11 | Random Forest | 04 | Ensemble baseline |
| 12 | XGBoost | 04 | **Champion model**, Optuna study |
| 13 | LSTM | 04 | Sequence baseline |
| 14 | Transformer Encoder | 04 | Main research model, attention weights |
| 15 | Lightweight Transformer | 04 | Cost-efficient candidate, Pareto scores |
| 16 | Comparative Analysis | 04 | Master comparison table, **Challenger selected** |
| 17 | SHAP Explainability | 05 | SHAPExplainer, stability scores |
| 18 | LIME & Attention | 05 | LIMEExplainer, AttentionExplainer, agreement scores |
| 19 | Human-Centred Evaluation | 05 | XAI Trade-off Matrix, analyst scores |
| 20 | Robustness & Drift | 05 | RobustnessEvaluator, DriftDetector |
| 21 | FastAPI Inference Service | 06 | Prediction + explanation API |
| 22 | Champion/Challenger Registry | 06 | Shadow inference, auto-promotion |
| 23 | Event Ingestion & Alerts | 06 | WebSocket real-time alerts |
| 24 | Security Dashboard | 06 | Threat Detection card, XAI panel |
| 25 | Admin Panel & Reports | 06 | Model management, PDF export |
| 26 | MLOps Pipeline | 07 | Automated retraining |
| 27 | Observability | 07 | Grafana dashboards, OTel traces |
| 28 | Security Hardening | 07 | JWT, RBAC, SAST/DAST clean |
| 29 | Testing Strategy | 07 | > 80% coverage |
| 30 | Performance Optimisation | 07 | All latency budgets met |
| 31 | CI/CD Pipeline | 07 | Automated quality gates + deployments |
| 32 | Kubernetes Deployment | 08 | k8s manifests, HPA, Helm chart |
| 33 | Terraform IaC | 08 | Full cloud infrastructure as code |
| 34 | Threat Intel Integration | 08 | AbuseIPDB + MITRE ATT&CK live |
| 35 | Research Report | 08 | Academic paper, reproducibility guide |
| 36 | Production Hardening & SLA | 08 | SLOs, DR runbook, security audit |
| 37 | Project Completion | 08 | v1.0.0 tagged, roadmap written |

---

**Previous:** ← [07 — MLOps, Security, Testing & Performance](07-mlops-security-testing-and-performance.md)

*End of XAI-Guard implementation guide. 37 phases. Production-grade. Enterprise-level.*
