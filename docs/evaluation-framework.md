# Three-Pillar Evaluation Framework

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
