# Champion/Challenger Promotion Policy

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
