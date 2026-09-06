import os

os.makedirs('docs/decisions', exist_ok=True)

# 2.1 Project Charter
with open('docs/project-charter.md', 'w') as f:
    f.write("""# XAI-Guard Project Charter

## 1. Executive Summary
XAI-Guard is a research-driven cybersecurity initiative designed to empirically evaluate and operationalize the trade-offs between predictive accuracy, algorithmic explainability, and hardware efficiency in Intrusion Detection Systems (IDS). By systematically benchmarking six model architectures against four heterogeneous datasets, XAI-Guard will deliver a production-ready Modular Monolith API, a real-time analyst dashboard, and a seminal research paper demonstrating how to safely deploy Deep Learning at the network edge using a mathematically rigorous Champion/Challenger promotion lifecycle.

## 2. Primary Objectives
1. **Model Efficacy (RQ1, RQ2, RQ7, RQ8):** Prove which model architecture achieves the highest F1-Macro across zero-day temporal drifts and class-imbalanced network flows.
2. **Explainability Utility (RQ4, RQ5):** Quantify the stability and actionable analyst-utility of SHAP, LIME, and Attention Rollout.
3. **Operational Viability (RQ3, RQ6):** Ensure production models strictly adhere to a $P99 < 100\\text{ms}$ inference latency budget on CPU-only edge hardware.
4. **Automated MLOps:** Implement a zero-touch promotion pipeline driven by the Composite Deployment Score (CDS).

## 3. In-Scope Deliverables
- **Documentation:** The 8-document, 63-phase architectural blueprint.
- **Machine Learning:** 6 fully trained, hyperparameter-optimized model families.
- **Backend:** A Domain-Driven FastAPI Modular Monolith (API layer).
- **Frontend:** A Next.js 15 / React 19 Analyst Dashboard and Admin Panel.
- **Research:** A peer-review-ready academic paper detailing the empirical findings.

## 4. Explicit Non-Goals
To strictly prevent scope creep, XAI-Guard will **NOT**:
- Perform raw packet capture (PCAP) ingestion (relies on pre-extracted tabular features like CICFlowMeter).
- Build SIEM vendor lock-in (exports standard JSON webhooks only).
- Process classified or proprietary client data (strictly open-source academic datasets).
- Guarantee legally admissible forensics chains-of-custody.
- Perform real-time online training (model weights are frozen at deployment).

## 5. Success Criteria
- **Performance:** At least one model achieves an F1-Macro $\ge 0.85$ on the CICIDS-2017 minority classes.
- **Latency:** The production API serves $P99$ predictions in $\le 100\\text{ms}$.
- **Usability:** 100% of generated explanations map back to human-readable network features within 500ms.
- **Automation:** The MLflow pipeline successfully auto-promotes a Challenger model without manual intervention.

## 6. Stakeholder Map
| Role | Responsibility |
|------|----------------|
| **Principal Investigator** | Experimental design, hypothesis validation, final CDS tuning. |
| **MLOps Engineer** | Pipeline orchestration, MLflow tracking, GPU resource allocation. |
| **Backend Architect** | FastAPI Modular Monolith, Celery queues, PostgreSQL schemas. |
| **Frontend Engineer** | Dashboard UI/UX, WebSocket real-time streams, TanStack Query. |

## 7. Risk Register
| ID | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Transformer exceeds 100ms latency on CPU | High | Critical | Introduce Lightweight Transformer and Knowledge Distillation. |
| R2 | Infiltration class ($N<40$) fails to converge | High | High | Mandate SMOTE/ADASYN augmentation in ETL pipeline. |
| R3 | SHAP Explainer OOM on 1024-dim embeddings | Medium | High | Use DeepSHAP or sub-sample background datasets. |
| R4 | Celery Queue backing up during DDoS | Medium | Moderate | Drop XAI generation dynamically if load > 5,000 EPS. |
| R5 | Concept drift permanently degrades Champion | Low | Critical | Automated MMD monitoring triggers rollback to Archived model. |

## 8. Milestone Timeline
- **M1 (Phases 1-8):** Foundation & Architecture Locked.
- **M2 (Phases 9-17):** Data Engineering & ETL Complete.
- **M3 (Phases 18-25):** Feature Stores & MLflow Live.
- **M4 (Phases 26-39):** ML Research & 6 Models Trained.
- **M5 (Phases 40-51):** XAI Generation & Backend API Live.
- **M6 (Phases 52-63):** Frontend Dashboard & CI/CD Deployed.
""")

# 2.2 Glossary
with open('docs/glossary.md', 'w') as f:
    f.write("""# XAI-Guard Domain Glossary

**Analyst Utility Metric:** A 0-1 composite heuristic scoring an explanation based on sparsity, feature comprehensibility, temporal relevance, and compute latency.
**Attack Taxonomy Enum:** The 7-class standardized classification target: `DDOS`, `PORT_SCAN`, `BRUTE_FORCE`, `BOTNET`, `WEB_ATTACK`, `INFILTRATION`, `NORMAL`.
**Burn Rate Alerting:** Monitoring the velocity at which the error budget (e.g., latency > 100ms) is consumed over a rolling window.
**Celery Task ID:** The UUID tracking the asynchronous background job responsible for generating XAI explanations.
**Champion Model:** The reigning production model currently serving 100% of synchronous live API traffic.
**Challenger Model:** A candidate model running in Shadow Evaluation Mode, attempting to depose the Champion.
**Composite Deployment Score (CDS):** The scalar heuristic used for auto-promotion, weighting F1-Macro, Latency, and Memory.
**Event Deduplication Hash:** A SHA-256 hash of a security event's raw payload and timestamp used to prevent DB collisions.
**Feature Stability Score:** The mathematical consistency of SHAP values, calculated as $1 - CV$ across 10 identical runs.
**Knowledge Distillation:** Training a smaller "student" model to replicate the outputs of a massive "teacher" model.
**LIME Explanation:** Local Interpretable Model-agnostic Explanations; building a local linear surrogate to explain a single prediction.
**MMD Drift Score:** Maximum Mean Discrepancy; a statistical test comparing the distribution of incoming traffic to the original training data to detect zero-day shifts.
**Modular Monolith:** A single deployable backend application containing strictly isolated domain modules that communicate only via public interfaces, avoiding microservice network overhead.
**PR-AUC:** Precision-Recall Area Under Curve; the definitive metric for highly imbalanced datasets.
**Sequence Window:** The chronological subset of packets/events passed into recurrent (LSTM) or attention (Transformer) models.
**Shadow Evaluation:** Running a Challenger model on live traffic silently in the background without affecting the user response.
**Shadow Inference Flag:** A boolean (`is_shadow=True`) attached to a prediction preventing it from triggering alerts or API responses.
**SHAP Value:** Shapley Additive exPlanations; game-theoretic values assigning credit for a prediction to individual features.
**Zero-Shot Generalisation Gap:** The drop in F1 performance when a model trained on one dataset is evaluated on a completely unseen dataset.
""")

# 2.3 ADRs
def write_adr(num, title, status, context, decision, consequence, alternatives):
    with open(f'docs/decisions/ADR-{num:03d}.md', 'w') as f:
        f.write(f"""# ADR-{num:03d}: {title}

## Status
**{status}**

## Context
{context}

## Decision
{decision}

## Consequences
{consequence}

## Alternatives Considered
{alternatives}
""")

write_adr(1, "Modular Monolith over Microservices", "Accepted", 
"The XAI-Guard platform requires distinct domains (Inference, Alerts, Registry, Events). Historically, teams default to microservices. However, microservices introduce severe network latency, complex distributed tracing, and CI/CD overhead, which threatens our strict 100ms P99 latency budget.",
"We will build the FastAPI backend as a strict Domain-Driven Modular Monolith. All domains will live in `services/api/app/modules/`. Modules must not directly import each other's SQLAlchemy models; communication must happen via module-level service interfaces or async event buses.",
"- **Positive:** Zero network overhead between domains; guarantees < 1ms internal communication.\n- **Positive:** Dramatically simplifies local developer setup (one container).\n- **Negative:** Requires strict discipline via tools like `import-linter` to prevent spaghetti coupling.",
"- **Microservices (Rejected):** Network hops between an Inference Service and an Alert Service would breach the 100ms latency budget.\n- **Traditional MVC Layered (Rejected):** Does not scale well as domain complexity grows.")

write_adr(2, "Common Model Interface (CMI)", "Accepted",
"We are evaluating six distinct model families ranging from Scikit-Learn (Logistic Regression) to PyTorch (Transformers). MLflow deployment requires a standardized way to instantiate and predict across these radically different libraries.",
"All six models must implement a strict abstract base class (`XAIModelBase`) enforcing identical signatures for `predict()`, `predict_proba()`, `save()`, and `load()`. For PyTorch models, the `predict` method must handle its own tensor conversion and softmax application internally.",
"- **Positive:** The API inference router does not need to know what architecture the Champion model is.\n- **Positive:** A new model family (e.g., TabNet) can be added instantly by adhering to the CMI.",
"- **Library-Specific Handlers (Rejected):** `if type == 'pytorch': ... else: ...` creates brittle, unmaintainable router code.")

write_adr(3, "Async-First API & Database", "Accepted",
"FastAPI supports both `def` and `async def`. Under high SOC traffic loads (10,000+ EPS), synchronous blocking I/O (like waiting for PostgreSQL to write an event) will exhaust the thread pool and crash the API.",
"All FastAPI endpoints must be `async def`. All database interactions must use `asyncpg` and SQLAlchemy 2.0 AsyncSessions. No synchronous `requests` or `psycopg2` are allowed in the critical path.",
"- **Positive:** Massive concurrency scale on minimal hardware.\n- **Negative:** Async Python stack traces are notoriously difficult to debug.\n- **Negative:** ML model inference (PyTorch/XGBoost) is inherently CPU-bound and synchronous.",
"- **Synchronous WSGI (Rejected):** Cannot handle the required throughput without massive horizontal scaling.")

write_adr(4, "Asynchronous XAI Generation via Celery", "Accepted",
"Generating SHAP values for a Transformer can take 200-500ms. If we generate XAI synchronously during the `POST /v1/events` payload, we will breach the 100ms P99 latency budget.",
"Model inference will execute synchronously. XAI generation will be offloaded to a Redis-backed Celery task. The API will immediately return the prediction along with an `explanation_task_id` for the client to poll or receive via WebSocket.",
"- **Positive:** Protects the 100ms inference SLA.\n- **Negative:** Requires standing up and managing Redis and Celery workers.\n- **Negative:** Adds eventual consistency complexity to the UI.",
"- **Synchronous XAI (Rejected):** Physically impossible to compute SHAP on a deep neural network within 100ms on CPU.")

write_adr(5, "Dual Tracking: DVC + MLflow", "Accepted",
"Git cannot store 10GB CSV datasets. MLflow cannot easily track massive dataset lineage across branches. We need a way to version both the data that produced a model and the metrics of the model itself.",
"We will use Data Version Control (DVC) exclusively for versioning large raw/processed datasets, tied to Git commits. We will use MLflow exclusively for tracking hyperparameter runs, metrics, and storing the final serialized model weights.",
"- **Positive:** Separation of concerns. DVC handles the bytes; MLflow handles the metadata.\n- **Negative:** Developers must learn two separate tools (`dvc pull` vs MLflow UI).",
"- **MLflow for everything (Rejected):** MLflow Artifacts is not designed for branching 10GB datasets.\n- **DVC for everything (Rejected):** DVC does not provide a robust UI for comparing 100 hyperparameter runs.")

# 2.4 Phase Dependency Map
with open('docs/phase-dependency-map.md', 'w') as f:
    f.write("""# Phase Dependency Map

```mermaid
graph TD
    %% Layer 1: Foundation
    subgraph L1 [L1: Foundation P1-P8]
        P1[P1: Research Scoping] --> P2[P2: Charter & Scope]
        P2 --> P3[P3: Dev Environment]
        P3 --> P4[P4: Architecture]
        P4 --> P5[P5: API Contracts]
        P5 --> P6[P6: Modular Monolith]
        P6 --> P7[P7: API Schemas]
        P7 --> P8[P8: API Routing]
    end

    %% Layer 2: Data Engineering
    subgraph L2 [L2: Data P9-P17]
        P8 --> P9[P9: Ingestion Core]
        P9 --> P10[P10: DVC Setup]
        P10 --> P11[P11: Raw Data ETL]
        P11 --> P12[P12: Imputation]
        P12 --> P13[P13: Feature Scaling]
        P13 --> P14[P14: Time-Series Windows]
        P14 --> P15[P15: Class Imbalance]
        P15 --> P16[P16: PCA Reduction]
        P16 --> P17[P17: DVC Push]
    end

    %% Layer 3: ML Tracking
    subgraph L3 [L3: ML Tracking P18-P25]
        P17 --> P18[P18: MLflow Backend]
        P18 --> P20[P20: Dataset Registry]
        P20 --> P25[P25: CMI Implementation]
    end

    %% Layer 4: ML Research (Parallelizable)
    subgraph L4 [L4: ML Research P26-P39]
        P25 --> P26[P26: Logistic Regression]
        P25 --> P28[P28: Random Forest]
        P25 --> P30[P30: XGBoost]
        P25 --> P32[P32: LSTM]
        P25 --> P34[P34: Transformer]
        P25 --> P36[P36: Light Transformer]
        
        P26 --> P39[P39: Research Checkpoint]
        P28 --> P39
        P30 --> P39
        P32 --> P39
        P34 --> P39
        P36 --> P39
    end

    %% Layer 5: XAI & UI
    subgraph L5 [L5: XAI & Fullstack P40-P63]
        P39 --> P40[P40: SHAP Integration]
        P40 --> P44[P44: Celery Workers]
        P44 --> P50[P50: Champion Promotion]
        P50 --> P55[P55: Dashboard Frontend]
        P55 --> P60[P60: CI/CD Pipeline]
        P60 --> P63[P63: Project Wrap]
    end
```

**Critical Path:** P1 → P17 (Data) → P25 (Interface) → P34 (Transformer) → P39 (Checkpoint) → P44 (Celery) → P55 (Dashboard) → P63 (Finish).
**Parallelization:** Phases 26 through 38 (The six ML models) can be executed concurrently by separate research teams.
""")

# 2.5 Definition of Done
with open('docs/definition-of-done.md', 'w') as f:
    f.write("""# Definition of Done (DoD)

To prevent partially finished work from halting the critical path, every phase must meet its specific category's Definition of Done before progressing.

## 1. ML Experiment Phase (DoD)
- [ ] Model architecture script is checked into `ml/src/models/`.
- [ ] Hyperparameter search completed via Optuna and logged to MLflow.
- [ ] Final trained artifact is registered in the MLflow Model Registry.
- [ ] Pillar 1, 2, and 3 metrics are populated in the Registry tags.
- [ ] Analysis Jupyter Notebook is committed to `ml/notebooks/`.
- [ ] The research findings document is updated with the per-attack-type F1 table.

## 2. API Backend Module Phase (DoD)
- [ ] All specified endpoints are implemented in the `router.py`.
- [ ] Input/Output validation is strictly enforced via Pydantic (`schemas.py`).
- [ ] Business logic is isolated in `service.py` (no database calls in routers).
- [ ] Database interactions utilize `asyncpg` and SQLAlchemy 2.0.
- [ ] OpenAPI (Swagger) specification generates without errors.
- [ ] `pytest` module coverage is $\ge 80\%$.

## 3. Frontend Application Phase (DoD)
- [ ] UI built utilizing Next.js 15, React 19, Tailwind CSS 4, and shadcn/ui.
- [ ] Global state is strictly managed via Zustand.
- [ ] Async server state and caching is managed via TanStack Query v5.
- [ ] Zod schemas perfectly mirror the Backend Pydantic schemas.
- [ ] Accessibility (a11y) passes Chrome DevTools audits.
- [ ] End-to-End Playwright test covering the user workflow executes successfully.

## 4. Infrastructure & Architecture Phase (DoD)
- [ ] Resource is formally defined (e.g., Docker Compose, ADR, Schema).
- [ ] Containers boot successfully and pass health checks on a clean machine.
- [ ] Documentation is updated, linking to the relevant Glossary or ADR files.
- [ ] No manual UI configuration is required (100% Infrastructure as Code).
""")

print("Successfully generated Phase 2: Project Charter & Scope.")
