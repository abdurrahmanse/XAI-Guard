# 05 — XAI & Model Evaluation

> **Phases 17 · 18 · 19 · 20** — SHAP, LIME, attention explainability, human-centred evaluation, and robustness testing.

---

## Phase 17 — SHAP Explainability Implementation

**Goal:** Produce SHAP explanations for every model; validate their correctness, stability, and analyst utility; answer RQ4.

**Context:** SHAP (SHapley Additive exPlanations) provides theoretically grounded feature attributions based on cooperative game theory. It is the current industry standard for ML explainability. Different model families require different SHAP explainer variants: `TreeExplainer` (exact, fast) for RF/XGBoost; `DeepExplainer` (approximation) for LSTM; `GradientExplainer` (gradient-based) for Transformer; `LinearExplainer` (exact) for LR. Explanation stability (consistency across repeated runs on the same input) is critical for analyst trust.

**Tools:** `shap==0.45`, matplotlib, mlflow, PostgreSQL (`xai_explanations` table)

**Tasks:**

- [ ] 17.1 Write `ml/src/explainability/shap_explainer.py` — `SHAPExplainer` unified class:
  ```python
  class SHAPExplainer:
      def __init__(self, model, model_type: Literal["lr","rf","xgb","lstm","transformer","lightweight_transformer"]):
          # dispatch: lr → LinearExplainer, rf/xgb → TreeExplainer,
          #           lstm → DeepExplainer, transformer* → GradientExplainer
          ...
      def explain_local(self, X_sample, feature_names) → SHAPExplanation:
          # returns: shap_values, base_value, feature_names, prediction, confidence
          ...
      def explain_global(self, X_test, feature_names) → GlobalSHAPExplanation:
          # returns: mean(|shap_values|) per feature → global importance ranking
          ...
      def stability_score(self, X_sample, n_runs=10) → float:
          # run explain_local n_runs times on same sample
          # return 1 - mean(std(shap_values across runs) / mean(|shap_values|))
          # 1.0 = perfectly stable, 0.0 = completely unstable
          ...
  ```
- [ ] 17.2 Define `SHAPExplanation` Pydantic model:
  ```python
  class SHAPExplanation(BaseModel):
      feature_names: list[str]
      shap_values: list[float]  # one per feature
      base_value: float
      prediction: int
      confidence: float
      top_k_factors: list[dict]  # [{name, value, direction: pos|neg}, ...] top 5
  ```
- [ ] 17.3 Compute global SHAP explanations for all six models on 1000 test samples each; store in `ml/artifacts/shap/`
- [ ] 17.4 Compute local SHAP for 50 representative test samples; store in PostgreSQL `xai_explanations` table (via `services/api`)
- [ ] 17.5 Run stability test on all 6 models: 10 runs per model on 100 samples; report mean stability score per model
- [ ] 17.6 Compare SHAP global feature rankings across models: compute Spearman rank correlation between each pair of models’ feature importance rankings. High correlation = models agree on what matters.
- [ ] 17.7 Measure SHAP computation time per model (samples/second) — this is the latency cost of explainability
- [ ] 17.8 Write `ml/notebooks/13-shap-analysis.ipynb`:
  - Beeswarm plot per model
  - Waterfall plot for 3 representative samples (DDoS, BruteForce, Normal)
  - Global bar chart (top 20 features)
  - Stability score comparison bar chart
  - Spearman correlation heatmap between models

**Output:** `SHAPExplainer` module; 1000 explanations per model stored; stability scores; SHAP analysis notebook

---

## Phase 18 — LIME & Attention Explainability

**Goal:** Implement two additional explanation methods (LIME, Attention) and measure cross-method agreement to answer RQ4 comprehensively.

**Context:** LIME provides model-agnostic local explanations by fitting a linear surrogate model around the prediction neighbourhood. It is slower than SHAP but works on any model without gradient access. Attention weights from the Transformer provide a third, intrinsic explanation modality — directly from the model’s internal computation. Cross-method agreement (SHAP vs LIME vs Attention) measures explanation consistency, a key RQ5 dimension.

**Tools:** `lime` (lime_tabular), Captum (PyTorch XAI), matplotlib

**Tasks:**

- [ ] 18.1 Write `ml/src/explainability/lime_explainer.py` — `LIMEExplainer` class:
  ```python
  class LIMEExplainer:
      def __init__(self, X_train, feature_names, class_names):
          self.explainer = lime.lime_tabular.LimeTabularExplainer(
              training_data=X_train,
              feature_names=feature_names,
              class_names=class_names,
              mode='classification',
              kernel_width='auto'
          )
      def explain_local(self, model_predict_fn, X_sample, n_samples=1000) → LIMEExplanation:
          ...
      def stability_score(self, model_predict_fn, X_sample, n_runs=10) → float:
          ...
  ```
- [ ] 18.2 Compute LIME explanations for the same 50 test samples used for SHAP (ensures comparability)
- [ ] 18.3 Run LIME stability test (same methodology as SHAP); report stability scores
- [ ] 18.4 Write `ml/src/explainability/attention_explainer.py` — `AttentionExplainer` class (Transformer + Lightweight Transformer only):
  ```python
  class AttentionExplainer:
      def explain_local(self, model, X_sample) → AttentionExplanation:
          # extract last-layer attention weights (batch=1, nhead, seq_len, seq_len)
          # aggregate: mean over heads → (seq_len, seq_len) attention matrix
          # row-normalize → attention scores per token (time step)
          ...
      def attention_rollout(self, model, X_sample) → AttentionExplanation:
          # Abnar & Zuidema (2020) Attention Rollout for more faithful attribution
          # multiply attention matrices across layers with residual connections
          ...
  ```
- [ ] 18.5 Compute agreement scores between methods for the 50-sample evaluation set:
  - SHAP vs LIME: Spearman rank correlation of feature importance per sample, averaged over 50 samples
  - SHAP vs Attention (Transformer): correlation between SHAP feature importances and attention-weighted feature positions
- [ ] 18.6 Write `ml/notebooks/14-lime-attention-analysis.ipynb`:
  - LIME explanation plot for 3 attack scenarios
  - Attention heatmap (time step × time step) for 2 Transformer examples
  - Side-by-side comparison: SHAP bar chart vs LIME bar chart for same sample
  - Agreement score table: model × method-pair

**Output:** `LIMEExplainer`, `AttentionExplainer` modules; agreement scores table; notebook

---

## Phase 19 — Human-Centred Evaluation Framework

**Goal:** Evaluate XAI outputs from the security analyst’s perspective — not just technical correctness, but practical usefulness. This directly answers RQ4 and RQ5.

**Context:** An explanation is valuable only if a human analyst can act on it. Technically correct SHAP values are useless if they reference 40 features with unintelligible names. The human-centred evaluation framework defines analyst utility metrics and applies them to score each model’s explanations systematically. For a research project, this is implemented as a structured expert rubric applied to a curated evaluation dataset.

**Tools:** Python, pandas, matplotlib (radar charts), custom scoring rubric

**Analyst Utility Metrics:**

| Metric | Definition | Measurement |
|--------|-----------|-------------|
| **Actionability** | Can the explanation guide a specific remediation action? | Rubric score 1–5 per scenario |
| **Completeness** | Does it cover all contributing factors? | Fraction of ground-truth factors mentioned |
| **Fidelity** | Does it correctly reflect the model’s reasoning? | Correlation with leave-one-out sensitivity |
| **Consistency** | Same inputs → same explanation? | = Stability score (Phase 17/18) |
| **Conciseness** | ≤5 key factors shown? | Binary: top-5 sufficient to classify? |

**Tasks:**

- [ ] 19.1 Build the analyst evaluation dataset: 50 manually labelled threat scenarios (10 per attack type) with:
  - Ground-truth explanation: which features are truly causal (e.g., for BruteForce: `failed_login_rate_5min`, `events_per_minute`, `unique_dest_ports_per_src`)
  - Expected recommended action (e.g., “Block source IP temporarily, investigate user account”)
  - Save as `ml/data/analyst_eval/scenarios.json`
- [ ] 19.2 Write `ml/src/evaluation/analyst_evaluation.py` — `AnalystEvaluator` class:
  ```python
  class AnalystEvaluator:
      def score_explanation(
          self,
          explanation: SHAPExplanation | LIMEExplanation,
          ground_truth: ScenarioGroundTruth
      ) → AnalystScore:
          # returns: {actionability, completeness, fidelity, consistency, conciseness, composite}
          ...
      def evaluate_model(
          self, model, explainer, scenarios: list[Scenario]
      ) → list[AnalystScore]:
          ...
  ```
- [ ] 19.3 Run automated evaluation: score each model’s SHAP, LIME, and (where applicable) Attention explanations against ground-truth scenarios
- [ ] 19.4 Produce the XAI Trade-off Matrix (save as `ml/artifacts/xai_tradeoff_matrix.csv`):

  | Model | SHAP-Fidelity | SHAP-Stability | SHAP-Actionability | LIME-Actionability | Attn-Fidelity | Expl-Latency-ms |
  |-------|--------------|----------------|--------------------|--------------------|---------------|------------------|

- [ ] 19.5 Write `ml/notebooks/15-analyst-evaluation.ipynb`:
  - Radar chart: 5 analyst metrics per model (for SHAP)
  - Scatter plot: F1_macro (x-axis) vs Composite XAI Score (y-axis) — answers RQ5 (trade-off)
  - Bar chart: Actionability score per model per explanation method
  - Conclusion: which model+method combination is most useful for analysts?
- [ ] 19.6 Write `docs/xai-evaluation-report.md` — findings and recommendations for security analyst teams:
  - Which XAI method is most actionable per attack type
  - Recommended analyst workflow: when to use SHAP vs LIME vs Attention
  - The Performance vs Explainability trade-off finding (RQ5 answer)

**Output:** `AnalystEvaluator` module; XAI Trade-off Matrix; evaluation notebook; `docs/xai-evaluation-report.md`

---

## Phase 20 — Robustness & Drift Detection

**Goal:** Measure every model’s robustness to adversarial inputs, data drift, and distribution shift — and build the drift detection system that triggers the Champion/Challenger retraining cycle.

**Context:** Production models degrade as attack patterns evolve (data drift) and as attackers adapt to bypass detection (adversarial robustness). RQ7 tests cross-attack generalisation. RQ8 tests drift robustness. The `DriftDetector` is a live component wired into the serving layer — when drift exceeds threshold, it triggers the retraining pipeline from Phase 26.

**Tools:** `alibi-detect` (drift detection), `adversarial-robustness-toolbox` (ART), MLflow

**Tasks:**

- [ ] 20.1 Write `ml/src/evaluation/robustness_evaluator.py` — `RobustnessEvaluator` class:
  ```python
  class RobustnessEvaluator:
      def cross_dataset_eval(self, model, X_train_src, y_train_src, X_test_target, y_test_target) → RobustnessResult:
          # train on source dataset, evaluate on target dataset; report metric drop as generalisation_gap
          ...
      def attack_type_holdout_eval(self, model, attack_type_to_hold: AttackType) → RobustnessResult:
          # train without the held-out attack type; test only on that type
          # measures zero-shot generalisation to unseen attack families
          ...
      def feature_perturbation_eval(self, model, X_test, noise_std=0.1) → RobustnessResult:
          # inject Gaussian noise (std=0.1) into numeric features
          # measure F1 degradation vs clean test set
          ...
  ```
- [ ] 20.2 Run adversarial attacks with ART on LSTM and Transformer:
  - FGSM (Fast Gradient Sign Method) at epsilon = [0.01, 0.05, 0.1]
  - Measure accuracy degradation curve vs epsilon
  - Classical models (LR, RF, XGBoost) are inherently adversarial-resistant for tabular data — document why
- [ ] 20.3 Write `ml/src/evaluation/drift_detector.py` — `DriftDetector` class:
  ```python
  class DriftDetector:
      def __init__(self, X_reference: np.ndarray, threshold: float = 0.05):
          # fit MMD (Maximum Mean Discrepancy) detector from alibi-detect
          self.detector = MMDDrift(X_reference, p_val=threshold, backend='pytorch')
      def detect(self, X_new: np.ndarray) → DriftReport:
          # returns: {drift_detected: bool, drift_score: float, p_value: float}
          ...
      def update_reference(self, X_new: np.ndarray): ...
  ```
- [ ] 20.4 Simulate temporal drift: split CICIDS-2017 by capture date → train on Day 1-3, test on Day 4-5; plot F1 degradation over time per model
- [ ] 20.5 Define drift-triggered retraining policy:
  - `drift_score > 0.05` → WARNING: monitor closely
  - `drift_score > 0.10` → CRITICAL: trigger Challenger evaluation run immediately
  - If Challenger outperforms Champion → auto-promote (Phase 22)
- [ ] 20.6 Write `ml/notebooks/16-robustness-drift.ipynb`:
  - Cross-dataset generalisation gap bar chart (all models)
  - Attack-type holdout heatmap
  - Adversarial degradation curve (accuracy vs epsilon)
  - Temporal drift simulation plot
  - Drift detection demo: show detector firing on injected drift
- [ ] 20.7 Write `docs/robustness-report.md` — which model is most robust to each threat type (answers RQ7 and RQ8)

**Output:** `RobustnessEvaluator`, `DriftDetector` modules; robustness report; drift threshold configured; temporal drift simulation results

---

## Phase Map

| Phase | Title | Key Question Answered |
|-------|-------|-----------------------|
| P17 | SHAP Explainability | Foundation for RQ4, RQ5 |
| P18 | LIME & Attention | RQ4: Method comparison; cross-method agreement |
| P19 | Human-Centred Evaluation | RQ4: Most useful method; RQ5: Performance vs explanation trade-off |
| P20 | Robustness & Drift | RQ7: Cross-attack generalisation; RQ8: Drift robustness |

**Previous:** ← [04 — ML Research & Experiments](04-ml-research-and-experiments.md) | **Next:** → [06 — Backend & Frontend Engineering](06-backend-and-frontend-engineering.md)
