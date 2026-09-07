# Champion & Challenger Status

This document explicitly tracks the current reigning models in the XAI-Guard ecosystem based on empirical evaluation (Table 4 / Composite Deployment Score).

## 🏆 Current Champion: Transformer (Quantised)
The INT8 Quantised Lightweight Transformer is our ultimate Champion.
* **F1 Macro:** 0.957
* **Latency (P99):** 8.4 ms
* **Memory Footprint:** 2.4 MB
* **CDS (Composite Score):** 0.947

**Selection Justification:** By utilizing Knowledge Distillation and INT8 Quantisation, this model completely shattered the Pareto Frontier. It mathematically achieves Deep Learning sequence-detection accuracy while effortlessly fitting within the strict 100ms CPU latency budget, annihilating all other networks on the Composite Deployment Score (CDS).

## ⚔️ Current Challenger: XGBoost
XGBoost remains the undisputed king of Classical Machine Learning and serves as our production fallback.
* **F1 Macro:** 0.931
* **Latency (P99):** 3.1 ms
* **Memory Footprint:** 45.2 MB
* **CDS (Composite Score):** 0.884

**Selection Justification:** XGBoost was selected as the Challenger because it possesses the highest F1 among all non-Deep Learning models. It has zero vanishing gradient issues, trains in seconds via Optuna, and achieves blistering 3.1 ms latency speeds. It serves as the ultimate baseline to justify the computational cost of the Transformer.
