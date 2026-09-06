# XAI-Guard

> **Explainable Multi-Model Transformer-Based Cybersecurity Threat Detection & Risk Analytics Platform**

XAI-Guard is a production-grade, enterprise-level research platform that answers one central question:

> *Which AI model offers the best balance of accuracy, recall, false-positive control, explainability, inference latency, computational cost, and human usefulness for cybersecurity threat detection?*

---

## What It Does

- Ingests real-world security event streams (logs, network flows, auth events)
- Runs six competing models in parallel: Logistic Regression → Random Forest → XGBoost → LSTM → Transformer Encoder → Lightweight Transformer
- Evaluates every model across **Prediction · Explainability · Operations** dimensions
- Produces analyst-facing explanations (SHAP, LIME, attention maps) for every detection
- Operates a Champion/Challenger model registry for safe production promotion
- Serves a real-time Security Dashboard with alert triage, risk scoring, and XAI panels

---

## Monorepo Structure

```
XAI-Guard/
├── apps/
│   ├── web/          # Next.js Security Dashboard (analyst UI)
│   ├── admin/        # Next.js Admin / MLOps control panel
│   └── api/          # Next.js API routes (BFF layer)
├── services/
│   └── api/          # FastAPI inference & event ingestion service (Python)
├── ml/
│   ├── src/
│   │   ├── models/           # All six model implementations
│   │   ├── features/         # Feature engineering pipeline
│   │   ├── preprocessing/    # Data cleaning & encoding
│   │   ├── evaluation/       # Metrics, benchmarking, drift detection
│   │   └── explainability/   # SHAP, LIME, attention visualisers
│   ├── experiments/          # MLflow experiment configs
│   ├── notebooks/            # EDA & research notebooks
│   ├── configs/              # Hydra / YAML model configs
│   └── artifacts/            # Saved models, reports
├── packages/
│   ├── ui/                   # Shared React component library
│   ├── eslint-config/
│   └── typescript-config/
├── infrastructure/           # Docker, Kubernetes, Terraform, CI/CD
├── tests/                    # End-to-end & integration tests
└── docs/                     # Phase-by-phase implementation guide
```

---

## Documentation — Build Phases

| # | Doc | Phases Covered |
|---|-----|----------------|
| 1 | [01 — Project Foundation](docs/01-project-foundation.md) | P1 · P2 · P3 |
| 2 | [02 — System Architecture](docs/02-system-architecture.md) | P4 · P5 |
| 3 | [03 — Data Engineering](docs/03-data-engineering.md) | P6 · P7 · P8 · P9 |
| 4 | [04 — ML Research & Experiments](docs/04-ml-research-and-experiments.md) | P10 · P11 · P12 · P13 · P14 · P15 · P16 |
| 5 | [05 — XAI & Model Evaluation](docs/05-xai-and-model-evaluation.md) | P17 · P18 · P19 · P20 |
| 6 | [06 — Backend & Frontend Engineering](docs/06-backend-and-frontend-engineering.md) | P21 · P22 · P23 · P24 · P25 |
| 7 | [07 — MLOps, Security, Testing & Performance](docs/07-mlops-security-testing-and-performance.md) | P26 · P27 · P28 · P29 · P30 · P31 |
| 8 | [08 — Production Deployment & Roadmap](docs/08-production-deployment-and-roadmap.md) | P32 · P33 · P34 · P35 · P36 · P37 |

---

## Tech Stack (Summary)

| Layer | Technology |
|-------|-----------|
| ML / Research | Python 3.11, PyTorch 2, scikit-learn, XGBoost, MLflow |
| XAI | SHAP, LIME, Captum (attention) |
| Backend API | FastAPI, Celery, Redis, PostgreSQL |
| Frontend | Next.js 14, TypeScript, Tailwind CSS, Recharts |
| Monorepo | Turborepo, pnpm workspaces |
| Infrastructure | Docker, Kubernetes (k8s), Terraform, GitHub Actions |
| Observability | Prometheus, Grafana, OpenTelemetry |

---

## Quick Start

```bash
# Install dependencies
pnpm install

# Run all apps in development mode
turbo dev

# Run ML pipeline (Python)
cd ml && uv run python src/pipeline.py

# Run tests
turbo test
```

---

## Research Questions Addressed

1. Classical ML vs Deep Learning — which wins on cybersecurity tabular + sequence data?
2. LSTM vs Transformer — which is better for sequence-based threat detection?
3. Does Large Transformer justify its computational cost?
4. Which XAI method is most useful for security analysts?
5. Is there a trade-off between prediction performance and explanation quality?
6. Which model is most cost-efficient for real-world deployment?
7. Does model performance generalise across different attack types?
8. Which model is most robust to data drift?

---

*See `docs/` for the complete phased implementation guide.*
