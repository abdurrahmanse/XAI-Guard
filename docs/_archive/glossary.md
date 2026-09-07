# XAI-Guard Domain Glossary

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
