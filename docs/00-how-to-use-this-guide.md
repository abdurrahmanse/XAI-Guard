# 00 — How to Use This Guide
## For Student Researchers: AI/ML Researcher & AI-Driven Full-Stack Engineer

> **This document is your starting point.** Read it before opening any other file.
> It tells you what you are building, why each step exists, and how the whole project maps to a publishable research paper.

---

## 🎯 What This Project Builds

**XAI-Guard** is a complete, end-to-end explainable cybersecurity threat detection platform. It:

1. **Trains and compares 6 AI models** on 4 real-world network security datasets
2. **Applies 3 XAI methods** (SHAP, LIME, Attention Rollout) to explain every prediction
3. **Serves predictions via a production API** with real-time alerts and drift detection
4. **Visualises everything** in a security analyst dashboard and admin panel
5. **Produces a peer-reviewable research paper** documenting the comparative study

Your **research question** is:
> *"Which AI model offers the best balance of accuracy, recall, false-positive control, explainability, inference latency, computational cost, and human usefulness for real-world cybersecurity threat detection?"*

---

## 📚 The 8 Documentation Files

Each doc covers a phase group. The files must be completed in order — later docs depend on earlier ones.

| Doc | Phases | What It Covers | Your Role |
|-----|--------|----------------|-----------|
| **01-project-foundation** | P1–P8 | Research design, architecture, infrastructure | Architect + Researcher |
| **02-data-engineering** | P9–P17 | Dataset acquisition, EDA, cleaning, splitting | Data Scientist |
| **03-data-engineering** | P18–P25 | Feature engineering, DVC pipeline, MLflow | ML Engineer |
| **04-ml-research-and-experiments** | P26–P32 | Classical ML + LSTM training | ML Researcher |
| **05-xai-and-model-evaluation** | P33–P39 | Transformer, distillation, XAI, statistics | Deep Learning Researcher |
| **06-backend-and-frontend-engineering** | P40–P47 | XAI API, drift detection, backend core | Full-Stack Engineer |
| **07-mlops-security-testing-and-performance** | P48–P55 | All 8 API modules, dashboard foundation | Full-Stack Engineer |
| **08-production-deployment-and-roadmap** | P56–P63 | Admin panel, CI/CD, paper writing | DevOps + Author |

---

## 🗺️ The 5 Dependency Layers

The 63 phases are organised into 5 layers. **You must complete each layer before the next.**

```
L1: Foundation (P1–P8)           ← Design decisions, infrastructure, schemas
    ↓
L2: Data Engineering (P9–P17)    ← The research begins here. Datasets + preprocessing.
    ↓
L3: Feature + Tracking (P18–P25) ← Domain features + MLflow + DVC pipeline
    ↓
L4: ML Research (P26–P39)        ← Train 6 models, evaluate, explain. Core research.
    ↓
L5: XAI + Backend + Frontend (P40–P63) ← Production system + paper writing
```

> **Student Priority Note:** L2–L4 are the research core. L5 is the engineering shell. If time is limited, complete L1–L4 first. A complete L4 alone is enough for a conference paper submission.

---

## 📄 How This Maps to a Research Paper

Your paper will have approximately 8 sections. Here is which phases produce the evidence for each section:

### Paper Section 1 — Introduction
**Produced by:** P1 (Research Statement), P2 (Project Charter)
- Motivation: Why is explainable IDS research needed?
- Research question and 8 sub-questions (RQ1–RQ8)
- Paper contributions (list 4–6 bullet points)

### Paper Section 2 — Related Work
**Produced by:** Your own literature review (2–3 hours after completing P1)
- Prior IDS ML studies (ML-based IDS papers from 2019–2025)
- XAI for security (SHAP/LIME applications in cybersecurity)
- Limitations of prior work (what your study adds)

### Paper Section 3 — Datasets & Preprocessing
**Produced by:** P9–P17
- **Table 1**: Dataset statistics (4 rows, 7 columns) ← from P14.3
- **Figure 1**: Class distribution charts for all 4 datasets ← from P10–P13
- **Table 2**: Unified feature schema ← from P14.1, P22.2
- Preprocessing pipeline description (cleaning, encoding, SMOTE) ← from P15–P17
- Split strategy rationale ← from P9.6

### Paper Section 4 — Experiments & Results
**Produced by:** P26–P43

#### 4.1 Experimental Setup
- Hardware specs, software versions, random seeds

#### 4.2 Ablation Study
- **Table 3**: Feature ablation results ← from P22B

#### 4.3 Model Performance (Pillar 1)
- **Table 4**: Master comparison table (6 models × all metrics) ← from P37.1
- **Figure 2**: Per-attack-class F1 heatmap ← from P37.2

#### 4.4 Explainability Results (Pillar 2)
- **Figure 3**: Global SHAP beeswarm plots ← from P39.2
- **Figure 4**: LIME vs SHAP correlation ← from P39.4
- SHAP stability scores per model ← from P39.3

#### 4.5 Temporal Robustness
- **Table 5**: Drift detection results ← from P45

### Paper Section 5 — Statistical Analysis
**Produced by:** P38
- McNemar's test significance matrix (15 pairwise comparisons) ← from P38.1
- 95% bootstrap confidence intervals per model ← from P38.2
- Effect sizes (Cohen's d) ← from P38.3

### Paper Section 6 — Operational Fitness (Pillar 3)
**Produced by:** P36
- **Table 6**: Inference latency P50/P95/P99 per model ← from P26.3
- **Figure 5**: Pareto frontier (F1 vs latency) ← from P36.2
- Composite Deployment Score (CDS) table

### Paper Section 7 — Discussion
Written by you based on all results:
- Which model wins? Why?
- Answer each RQ1–RQ8 with specific numbers
- Limitations and future work

### Paper Section 8 — Conclusion
1-page summary of contributions and winner.

---

## 🎓 How to Read Each Phase

Every phase (from doc-02 onwards) follows this structure:

```
## Phase N — Title

### 🎓 What You Will Learn
[Read this first. It tells you the concept being taught.]

### 📄 Research Paper Connection
[Read this second. It tells you what evidence this phase produces for your paper.]

### 📖 Concept: [Key Term]
[Read this before starting the tasks. It explains the theory.]

#### Subphase N.M — Title
> Role / Context / Task / Stack / Outcome
[This is where you actually implement.]

### ⚠️ Common Student Mistakes
[Read this after you think you're done. Check you didn't make these errors.]

### ✅ Learning Checkpoint
[Answer these 3 questions before moving on.]
```

---

## 🔬 The 6 Models You Will Train

| Model Family | Type | Key Strength | Key Weakness |
|-------------|------|-------------|-------------|
| **Logistic Regression** | Classical | Fast, interpretable | Low accuracy on non-linear patterns |
| **Random Forest** | Classical ensemble | Good accuracy, native feature importance | Slow inference, large model size |
| **XGBoost** | Gradient boosting | Best tabular accuracy, fast inference | Requires feature engineering |
| **BiLSTM** | Recurrent deep learning | Detects sequential attack patterns | Slow, requires sequence input |
| **Transformer Encoder** | Attention deep learning | Best raw accuracy, rich XAI signal | Slowest, most compute |
| **Lightweight Transformer** | Distilled deep learning | Near-Transformer accuracy, fast | Reduced accuracy vs full Transformer |

**Expected result:** XGBoost will likely win on Composite Deployment Score (best F1 + fastest CPU inference). The Transformer will have the highest raw F1 but will exceed the 100ms latency budget.

---

## 📊 The Three-Pillar Evaluation Framework

Every model is evaluated on exactly the same three pillars:

### Pillar 1 — Prediction Performance
- F1 Macro (overall), F1 per attack class (7 classes), ROC-AUC Macro OvR, PR-AUC Macro

### Pillar 2 — Explainability Quality
- SHAP stability score, LIME-SHAP rank correlation, Analyst utility composite score

### Pillar 3 — Operational Fitness
- Inference latency P50/P95/P99 (ms), throughput (events/sec), memory (MB)
- **Composite Deployment Score:**
  ```
  CDS = 0.40 × norm(F1) + 0.35 × norm(1/latency_p99) + 0.25 × norm(1/memory_mb)
  ```

---

## 🗓️ Realistic Time Estimate (Student Working Part-Time)

| Layer | Estimated Hours | Notes |
|-------|----------------|-------|
| L1 Foundation (P1–P8) | 20–30 hours | Most of L1 is already done in this project |
| L2 Data Engineering (P9–P17) | 40–60 hours | EDA is iterative. Budget extra time for data quality issues |
| L3 Features + Tracking (P18–P25) | 30–40 hours | Feature engineering + DVC setup |
| L4 ML Research (P26–P39) | 60–100 hours | Training 6 models + HPO. GPU access helps for deep learning |
| L5 XAI + Backend + Frontend (P40–P63) | 80–120 hours | Large engineering surface area |
| **Total** | **~300 hours** | ~6 months at 10–15 hours/week |

> **Paper-only shortcut:** Complete L1–L4 and XAI phases P39–P43 (~150 hours). This produces all evidence needed for a conference paper.

---

## 🧪 The Research Datasets

| Dataset | Records | Features | Primary Challenge |
|---------|---------|----------|-------------------|
| **NSL-KDD** | ~148K train / ~23K test | 41 | Train/test distribution mismatch |
| **CICIDS-2017** | ~2.8M | 78 | Severe class imbalance, data quality |
| **UNSW-NB15** | ~257K | 49 | Different taxonomy, modern attacks |
| **BETH** | Variable | 14 | Real temporal drift, feature sparsity |

---

## 🔑 Key Tools You Will Learn

| Tool | Purpose | Phase |
|------|---------|-------|
| **DVC** | Data version control | P9, P24 |
| **MLflow** | Experiment tracking | P25, all training phases |
| **Optuna** | Hyperparameter optimisation | P26–P36 |
| **SHAP** | Model explanation | P39 |
| **LIME** | Local linear explanation | P40 |
| **PyTorch Lightning** | Deep learning training | P30, P33 |
| **FastAPI** | Production API | P46–P53 |
| **Celery** | Async XAI task queue | P46 |
| **Next.js** | Analyst dashboard | P55–P56 |
| **Terraform** | Infrastructure as code | P62 |

---

## 🚀 Where to Start

1. **Read** `docs/01-project-foundation.md` — understand the design decisions already made
2. **Review** `docs/research-statement.md` and `docs/evaluation-framework.md` — your methodology
3. **Begin** `docs/02-data-engineering.md` Phase 9 — download the datasets

> **Environment setup first:** `pnpm install && docker-compose -f infrastructure/docker-compose.yml up -d`
> See `CONTRIBUTING.md` for the full 10-step setup guide.

---

*Good luck. This project is ambitious — but every phase is designed to be completable step by step. The most important thing is to understand each concept before moving on. Use the Learning Checkpoints honestly.*
