import os
import yaml

os.makedirs('docs', exist_ok=True)
os.makedirs('ml/configs/hpo', exist_ok=True)

# 1.1 Research Statement
with open('docs/research-statement.md', 'w') as f:
    f.write("""# XAI-Guard Research Statement

## 1. Motivation
Modern cybersecurity operations centres (SOCs) are overwhelmed by alert fatigue. While Deep Learning models can detect zero-day attacks with high accuracy, their "black-box" nature prevents analysts from trusting them. Classical machine learning models are interpretable but often fail to capture complex, temporally distributed attack vectors. XAI-Guard seeks to bridge this gap by systematically evaluating the trade-offs between prediction performance, explainability, and operational fitness.

## 2. Problem Statement
**Central Research Question:** *Which AI model offers the best balance of accuracy, recall, false-positive control, explainability, inference latency, computational cost, and human usefulness for real-world cybersecurity threat detection?*

Currently, no consensus exists on whether the accuracy gains of Transformer-based architectures justify their high inference latency and computational cost in real-time Intrusion Detection Systems (IDS), nor which eXplainable AI (XAI) method provides the most actionable context for human analysts.

## 3. Research Objectives
1. Systematically compare classical ML, recurrent networks, and attention mechanisms on modern IDS benchmarks.
2. Quantify the stability and analyst-utility of three distinct XAI methods: SHAP, LIME, and Attention Rollout.
3. Establish a reproducible operational fitness metric that penalises models for high inference latency and memory bloat.

## 4. Scope
- **Six Competing Models:** Logistic Regression, Random Forest, XGBoost, LSTM, Transformer Encoder, Lightweight Transformer.
- **Four Benchmark Datasets:** NSL-KDD, CICIDS-2017, UNSW-NB15, BETH.
- **Three Evaluation Pillars:** Prediction Performance, Explainability Quality, Operational Fitness.

## 5. Expected Contributions
- A rigorous, open-source benchmarking framework for IDS models.
- A novel Composite Deployment Score (CDS) that balances F1, P99 Latency, and Memory usage.
- Empirical evidence on the correlation between XAI stability and prediction confidence.
""")

# 1.2 Research Questions
with open('docs/research-questions.md', 'w') as f:
    f.write("""# Eight Research Sub-Questions

## RQ1: Classical ML vs Deep Learning
- **H₀:** Deep learning models do not significantly improve F1-Macro compared to tree-based ensembles (XGBoost/RF).
- **Metric:** F1-Macro Delta.
- **Test:** McNemar's Test (p < 0.05).

## RQ2: Sequence Detection (LSTM vs Transformer)
- **H₀:** Transformer models do not outperform LSTMs on temporally distributed attacks (e.g., slowloris, advanced persistent threats).
- **Metric:** Recall on sequence-dependent attack classes.
- **Test:** Wilcoxon Signed-Rank Test.

## RQ3: Transformer Cost-Benefit
- **H₀:** The accuracy gain of a full Transformer Encoder does not justify its GPU-hour training cost compared to a Lightweight Transformer.
- **Metric:** Training GPU-hours / F1-Macro gain ratio.
- **Test:** Threshold Analysis (Must exceed 0.01 F1 per 10 GPU-hours).

## RQ4: Analyst-Actionable XAI
- **H₀:** There is no significant difference in analyst utility between SHAP and LIME explanations.
- **Metric:** Analyst utility composite score (survey/heuristic based).
- **Test:** Kruskal-Wallis H Test.

## RQ5: Accuracy vs Explainability Trade-off
- **H₀:** Highly accurate models do not exhibit lower XAI stability scores than simpler models.
- **Metric:** Pearson correlation between ROC-AUC and SHAP stability score.
- **Test:** Pearson's r significance test.

## RQ6: CPU-Only Operational Efficiency
- **H₀:** No deep learning model can achieve a P99 inference latency of < 100ms on CPU-only infrastructure.
- **Metric:** P99 Inference Latency (ms).
- **Test:** Empirical Benchmark.

## RQ7: Cross-Dataset Generalisation
- **H₀:** Model rankings by F1-Macro are inconsistent across NSL-KDD, CICIDS-2017, UNSW-NB15, and BETH.
- **Metric:** F1-Macro Variance.
- **Test:** Friedman Test.

## RQ8: Robustness to Data Drift
- **H₀:** Complex deep learning models degrade faster under temporal data drift (BETH dataset) than classical tree-based models.
- **Metric:** Maximum Mean Discrepancy (MMD) correlation with F1 decay rate.
- **Test:** Spearman's Rank Correlation.
""")

# 1.3 Evaluation Framework
with open('docs/evaluation-framework.md', 'w') as f:
    f.write("""# Three-Pillar Evaluation Framework

## Pillar 1 — Prediction Performance
The core ability of the model to distinguish malicious from benign traffic.
- **Metrics:** Accuracy, Precision (Macro), Recall (Macro), F1 (Macro), ROC-AUC (Macro OvR), PR-AUC (Macro).
- **Class-Level Metrics:** F1 per attack class (DDoS, PortScan, BruteForce, Botnet, WebAttack, Infiltration, Normal).

## Pillar 2 — Explainability Quality
The reliability and usefulness of the generated explanations.
- **SHAP Stability Score:** Calculated as `1 - Coefficient of Variation (CV)` across 10 identical explanation runs.
- **LIME-SHAP Rank Correlation:** Spearman rank correlation between top-5 features identified by LIME vs SHAP.
- **Attention-SHAP Rank Correlation:** (For Transformers) Correlation between attention weights and SHAP values.
- **Analyst Utility:** A composite heuristic evaluating sparsity, feature comprehensibility, and temporal relevance.

## Pillar 3 — Operational Fitness
The viability of deploying the model to a production CPU-only edge node.
- **Inference Latency:** P50, P95, and P99 measured in milliseconds (ms).
- **Throughput:** Processed events per second.
- **Memory Footprint:** Peak RSS Memory in MB during inference.
- **Training Cost:** GPU-hours required to converge.
- **Artifact Size:** MB size of the saved model weights.

## Composite Deployment Score (CDS)
A single metric used for automated Champion/Challenger promotion.
`CDS = 0.40 × norm(F1) + 0.35 × norm(1/latency_p99) + 0.25 × norm(1/memory_mb)`

*(Normalisation is performed using Min-Max scaling against baseline Logistic Regression values).*
""")

# 1.4 Dataset Strategy
with open('docs/dataset-strategy.md', 'w') as f:
    f.write("""# Dataset Strategy & Attack Taxonomy

## 1. NSL-KDD
- **Context:** The established historical benchmark for IDS.
- **Profile:** 40 features, balanced classes.
- **Challenge:** Solved dataset, used primarily for baseline verification.

## 2. CICIDS-2017
- **Context:** Modern network flows with realistic background traffic.
- **Profile:** 80 features, severe class imbalance (Normal traffic dominates).
- **Challenge:** Detecting low-frequency attacks like Infiltration and WebAttacks.

## 3. UNSW-NB15
- **Context:** Comprehensive attack taxonomy representing modern CVEs.
- **Profile:** 49 features, 9 detailed attack families.
- **Challenge:** Multi-class classification complexity.

## 4. BETH
- **Context:** Real enterprise-scale honeypot data with heavy temporal drift.
- **Challenge:** Evaluating model robustness to concept drift over time.

## Unified Attack Taxonomy
To train a single unified platform, all dataset-specific labels are mapped to the following standard `Enum`:
1. `DDOS`
2. `PORT_SCAN`
3. `BRUTE_FORCE`
4. `BOTNET`
5. `WEB_ATTACK`
6. `INFILTRATION`
7. `NORMAL`

*(Attack subtypes with fewer than 100 samples are flagged for SMOTE/ADASYN augmentation).*
""")

# 1.4 Taxonomy Config
taxonomy = {
    "taxonomy": ["DDOS", "PORT_SCAN", "BRUTE_FORCE", "BOTNET", "WEB_ATTACK", "INFILTRATION", "NORMAL"],
    "mappings": {
        "nsl_kdd": {"neptune": "DDOS", "smurf": "DDOS", "portsweep": "PORT_SCAN", "ipsweep": "PORT_SCAN", "guess_passwd": "BRUTE_FORCE", "normal": "NORMAL"},
        "cicids_2017": {"DDoS": "DDOS", "PortScan": "PORT_SCAN", "FTP-Patator": "BRUTE_FORCE", "SSH-Patator": "BRUTE_FORCE", "Bot": "BOTNET", "Web Attack": "WEB_ATTACK", "Infiltration": "INFILTRATION", "BENIGN": "NORMAL"},
        "unsw_nb15": {"DoS": "DDOS", "Reconnaissance": "PORT_SCAN", "Fuzzers": "BRUTE_FORCE", "Backdoors": "BOTNET", "Normal": "NORMAL"}
    }
}
with open('ml/configs/taxonomy.yaml', 'w') as f:
    yaml.dump(taxonomy, f, sort_keys=False)

# 1.5 Promotion Policy
with open('docs/champion-challenger-policy.md', 'w') as f:
    f.write("""# Champion/Challenger Promotion Policy

## 1. State Machine
- `TRAINING` → Model is actively training in MLflow.
- `REGISTERED` → Training complete, artifact saved to Model Registry.
- `CHALLENGER` → Selected for shadow deployment.
- `CHAMPION` → Actively serving production API traffic.
- `ARCHIVED` → Deprecated model, retained for rollback.

## 2. Shadow Evaluation Mode
The Challenger model receives a 100% mirrored copy of all live incoming events via Celery. It computes predictions asynchronously. These predictions are logged to the database but NEVER returned to the API caller.

## 3. Automated Comparison Window
A nightly scheduled job (02:00 UTC) aggregates the last 24 hours of Shadow (Challenger) vs Live (Champion) predictions against ground-truth labels (if available) or evaluates concept drift metrics.

## 4. Promotion Gates (The "AND" Rule)
To trigger an auto-promotion, the Challenger MUST pass ALL gates:
1. **Performance Gate:** `ΔF1-Macro ≥ +0.020` AND `ΔROC-AUC ≥ +0.010`
2. **Latency Gate:** `P99 Latency ≤ 100ms`
3. **Statistical Significance Gate:** McNemar's Test `p < 0.05` (with Bonferroni correction for multi-class).

## 5. Rollback Procedure
If a Champion model's MMD Drift Score crosses the `CRITICAL` threshold or P99 Latency breaches 200ms, an automatic rollback is triggered to the most recent `ARCHIVED` model.
""")

# 1.6 HPO Configs
def create_hpo(name, config):
    with open(f'ml/configs/hpo/{name}.yaml', 'w') as f:
        yaml.dump(config, f, sort_keys=False)

create_hpo('logistic_regression', {
    "optimizer": "GridSearchCV",
    "validation": "5-fold StratifiedKFold",
    "params": {
        "C": {"type": "float", "choices": [0.01, 0.1, 1.0, 10.0, 100.0], "scale": "log"},
        "penalty": {"type": "categorical", "choices": ["l1", "l2"]},
        "solver": {"type": "categorical", "choices": ["liblinear", "saga"]}
    }
})

create_hpo('random_forest', {
    "optimizer": "Optuna",
    "trials": 50,
    "validation": "5-fold StratifiedKFold",
    "params": {
        "n_estimators": {"type": "int", "range": [100, 500]},
        "max_depth": {"type": "int", "range": [5, 50]},
        "min_samples_split": {"type": "int", "range": [2, 10]}
    }
})

create_hpo('xgboost', {
    "optimizer": "Optuna",
    "trials": 50,
    "validation": "5-fold StratifiedKFold",
    "early_stopping_rounds": 20,
    "params": {
        "learning_rate": {"type": "float", "range": [0.01, 0.3], "scale": "log"},
        "max_depth": {"type": "int", "range": [3, 10]},
        "subsample": {"type": "float", "range": [0.5, 1.0]},
        "colsample_bytree": {"type": "float", "range": [0.5, 1.0]}
    }
})

create_hpo('lstm', {
    "optimizer": "Optuna",
    "trials": 30,
    "validation": "Epoch-based",
    "early_stopping_patience": 5,
    "params": {
        "hidden_size": {"type": "int", "choices": [64, 128, 256]},
        "num_layers": {"type": "int", "range": [1, 3]},
        "learning_rate": {"type": "float", "range": [1e-4, 1e-2], "scale": "log"},
        "dropout": {"type": "float", "range": [0.1, 0.5]},
        "batch_size": {"type": "int", "choices": [128, 256, 512]}
    }
})

create_hpo('transformer', {
    "optimizer": "Optuna",
    "trials": 30,
    "validation": "Epoch-based",
    "early_stopping_patience": 5,
    "mixed_precision": True,
    "gradient_clipping": 1.0,
    "params": {
        "d_model": {"type": "int", "choices": [128, 256, 512]},
        "nhead": {"type": "int", "choices": [4, 8]},
        "num_layers": {"type": "int", "range": [2, 6]},
        "learning_rate": {"type": "float", "range": [1e-5, 1e-3], "scale": "log"},
        "warmup_steps": {"type": "int", "range": [500, 2000]}
    }
})

create_hpo('lightweight_transformer', {
    "optimizer": "Optuna",
    "trials": 30,
    "validation": "Epoch-based",
    "early_stopping_patience": 5,
    "mixed_precision": True,
    "params": {
        "d_model": {"type": "int", "choices": [32, 64]},
        "nhead": {"type": "int", "choices": [2, 4]},
        "num_layers": {"type": "int", "range": [1, 2]},
        "learning_rate": {"type": "float", "range": [1e-4, 5e-3], "scale": "log"}
    }
})

print("Successfully generated all Phase 1 documents and configurations.")
