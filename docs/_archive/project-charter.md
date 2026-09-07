# XAI-Guard Project Charter

## 1. Executive Summary
XAI-Guard is a research-driven cybersecurity initiative designed to empirically evaluate and operationalize the trade-offs between predictive accuracy, algorithmic explainability, and hardware efficiency in Intrusion Detection Systems (IDS). By systematically benchmarking six model architectures against four heterogeneous datasets, XAI-Guard will deliver a production-ready Modular Monolith API, a real-time analyst dashboard, and a seminal research paper demonstrating how to safely deploy Deep Learning at the network edge using a mathematically rigorous Champion/Challenger promotion lifecycle.

## 2. Primary Objectives
1. **Model Efficacy (RQ1, RQ2, RQ7, RQ8):** Prove which model architecture achieves the highest F1-Macro across zero-day temporal drifts and class-imbalanced network flows.
2. **Explainability Utility (RQ4, RQ5):** Quantify the stability and actionable analyst-utility of SHAP, LIME, and Attention Rollout.
3. **Operational Viability (RQ3, RQ6):** Ensure production models strictly adhere to a $P99 < 100\text{ms}$ inference latency budget on CPU-only edge hardware.
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
- **Latency:** The production API serves $P99$ predictions in $\le 100\text{ms}$.
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
