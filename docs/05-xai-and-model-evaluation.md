# 05 — Transformer Architecture & XAI Evaluation

> **Phases 33–39** | Transformer Encoder, Transformer training, Lightweight Transformer with knowledge distillation, quantisation and deployment profiling, cross-model comparative analysis, statistical significance testing, and SHAP implementation.
>
> **Prompt Engineering Format:** Each subphase includes Role, Context, Task, Stack, and Outcome.

---

## Phase 33 — Transformer Encoder Architecture

**Context:** The Transformer Encoder is the most powerful model in the benchmark. Its self-attention mechanism produces the richest XAI signal via Attention Rollout.

#### Subphase 33.1 — Multi-Head Self-Attention Block

> **🎭 Role:** Senior Deep Learning Architect with Transformer expertise
> **📍 Context:** The Transformer processes event sequences. Each position in the sequence attends to all others. Attention weights are stored during forward passes for XAI extraction.
> **🔧 Task:** Implement `ml/src/models/transformer/attention.py`. `MultiHeadSelfAttention(d_model: int, n_heads: int, dropout: float)` PyTorch Module. Standard scaled dot-product attention: `Q, K, V` projections as `nn.Linear`; attention scores `QK^T / sqrt(d_k)` with softmax; dropout on attention weights. Crucially: store the attention weight matrix in `self.last_attention_weights` during every forward pass (for XAI). This must work with `torch.no_grad()` context. `n_heads` must divide `d_model` exactly (raise `ValueError` otherwise). Add pre-layer norm (`nn.LayerNorm`) following the Pre-LN Transformer architecture for training stability.
> **📦 Stack:** torch 2.3, numpy
> **✅ Outcome:** `attention.last_attention_weights` has shape `(batch, n_heads, seq_len, seq_len)` after every forward pass. Attention weights sum to 1.0 along the last dimension (within 1e-5).

#### Subphase 33.2 — Transformer Encoder Block

> **🎭 Role:** Senior Deep Learning Engineer
> **📍 Context:** A single Encoder block is the composable unit. Stacking N blocks creates the full Transformer.
> **🔧 Task:** Implement `TransformerEncoderBlock(d_model, n_heads, d_ff, dropout)` in `ml/src/models/transformer/encoder.py`. Architecture: Pre-LN Multi-Head Self-Attention with residual connection; Pre-LN Feed-Forward `Linear(d_model, d_ff) → GELU → Dropout → Linear(d_ff, d_model)` with residual connection. Implement `TransformerEncoder(n_layers, d_model, n_heads, d_ff, dropout, n_classes, n_features, max_seq_len)` that: (1) projects input features to d_model; (2) adds positional encoding; (3) passes through N encoder blocks; (4) takes the mean-pooled output (not CLS token) as the sequence representation; (5) classifies with a linear head.
> **📦 Stack:** torch 2.3
> **✅ Outcome:** Forward pass with input `(32, 10, 50)` produces output `(32, 7)`. All residual connections are correct (verified by gradient flow test).

#### Subphase 33.3 — Attention Weight Extraction for XAI

> **🎭 Role:** XAI Research Engineer
> **📍 Context:** Attention Rollout (Abnar & Zuidema, 2020) computes how much each input token contributed to the output by recursively combining attention weights across layers. This requires access to per-layer attention weights.
> **🔧 Task:** Implement `AttentionRolloutExtractor` in `ml/src/models/transformer/attention_rollout.py`. Method `extract(model: TransformerEncoder, X_seq: torch.Tensor) -> np.ndarray`: (1) run forward pass; (2) collect `last_attention_weights` from all N encoder blocks; (3) apply Attention Rollout algorithm: rollout = I + A for each layer; normalise; matrix multiply across layers; extract the final rollout vector per sequence position. Return shape `(n_samples, seq_len)` — the importance score of each event in the sequence window.
> **📦 Stack:** torch, numpy
> **✅ Outcome:** Rollout scores sum to approximately 1.0 per sample. The most important timestep (highest score) corresponds to the event most likely to contain the attack signal.

#### Subphase 33.4 — Transformer Unit Tests

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** Transformer attention is notoriously easy to implement incorrectly. Unit tests catch subtle bugs before expensive training.
> **🔧 Task:** Write `ml/tests/test_transformer.py`. Test: (1) output shape is `(batch, n_classes)` for various batch sizes; (2) attention weights sum to 1.0 per head and position; (3) `last_attention_weights` are populated after `torch.no_grad()` forward pass; (4) Attention Rollout produces scores summing to approximately 1.0; (5) gradient flow reaches the input projection layer; (6) Pre-LN architecture: layer norm is applied before attention, not after (verify by checking norm layer position in the module graph); (7) `n_heads` validation raises ValueError for non-divisible d_model.
> **📦 Stack:** pytest, torch, numpy
> **✅ Outcome:** All 7 Transformer unit tests pass. The gradient flow test specifically verifies the Pre-LN architecture.

---

## Phase 34 — Transformer Encoder Training

**Context:** Train the Transformer with a warm-up learning rate schedule and Optuna search. This is the computationally most expensive training phase.

#### Subphase 34.1 — Warm-Up Cosine Scheduler

> **🎭 Role:** Senior Deep Learning Engineer
> **📍 Context:** Transformers require a warm-up phase where the learning rate starts low and increases linearly to prevent instability in the early training stages.
> **🔧 Task:** Implement `WarmupCosineScheduler(optimizer, n_warmup_steps: int, n_total_steps: int)` in `ml/src/training/schedulers.py`. Linear warm-up from `lr/n_warmup_steps` to `lr` over `n_warmup_steps` steps. Cosine annealing from `lr` to `lr/100` over the remaining steps. Step the scheduler per batch (not per epoch). Log the current learning rate to MLflow every 100 steps. Write a unit test that plots the LR schedule over 1000 steps and verifies the peak occurs at step `n_warmup_steps`.
> **📦 Stack:** torch, mlflow, matplotlib
> **✅ Outcome:** The LR peaks at `n_warmup_steps` and decays to `lr/100` by step `n_total_steps`. The schedule plot is logged as an MLflow artifact.

#### Subphase 34.2 — Optuna Transformer Search

> **🎭 Role:** Senior ML Research Engineer
> **📍 Context:** The Transformer has more hyperparameters than the LSTM. The search space includes architecture parameters (d_model, n_heads, n_layers) and training parameters.
> **🔧 Task:** Write `ml/scripts/train_transformer.py`. Optuna objective: suggest `d_model` ∈ [64, 128, 256] (must be divisible by n_heads), `n_heads` ∈ [4, 8] (enforced to divide d_model), `n_layers` ∈ [2, 4, 6], `d_ff` = 4 × d_model (fixed ratio), `dropout` [0.1, 0.3], `n_warmup_steps` [100, 1000], `learning_rate` log-uniform [1e-5, 1e-3], `weight_decay` log-uniform [1e-5, 1e-2]. Run 20 Optuna trials. After best trial, save attention weights for the full test set as a NumPy artifact for Phase 39 and Phase 41.
> **📦 Stack:** optuna, pytorch-lightning, torch, mlflow
> **✅ Outcome:** 20 trials complete. Best Transformer model is registered. Attention weights for the test set are saved as an MLflow artifact.

---

## Phase 35 — Lightweight Transformer & Knowledge Distillation

**Context:** The full Transformer may be too slow for production. Knowledge distillation trains a smaller student model to mimic the large teacher, achieving similar accuracy at lower latency cost.

#### Subphase 35.1 — Lightweight Transformer Architecture

> **🎭 Role:** Senior Deep Learning Engineer with model compression expertise
> **📍 Context:** The Lightweight Transformer uses fewer layers and smaller d_model than the full Transformer. It will be trained from scratch first (baseline) and then with distillation.
> **🔧 Task:** Implement `LightweightTransformerModel(XAIGuardModel)` in `ml/src/models/lightweight_transformer.py`. Fixed architecture: `d_model=64, n_heads=4, n_layers=2, d_ff=256`. This model is intentionally small to fit the P99 ≤ 100ms CPU latency budget. Reuse all building blocks from Phase 33. Verify the model has fewer than 500K parameters using `sum(p.numel() for p in model.parameters())`. Log the parameter count and model file size to MLflow.
> **📦 Stack:** torch 2.3
> **✅ Outcome:** The lightweight model has fewer than 500K parameters. The interface contract tests all pass.

#### Subphase 35.2 — Knowledge Distillation Training

> **🎭 Role:** Senior Deep Learning Engineer specialising in model compression
> **📍 Context:** Knowledge distillation trains the student to match the teacher's soft probability outputs (logits) rather than just the hard labels. This transfers knowledge beyond what the labels alone convey.
> **🔧 Task:** Implement the distillation training objective in `ml/scripts/train_lightweight_transformer.py`. `DistillationLoss = α * KL(student_softmax/T || teacher_softmax/T) + (1-α) * CrossEntropy(student, hard_labels)`. Default: `T=4` (temperature), `α=0.7`. The teacher is the best full Transformer from Phase 34, loaded from MLflow and frozen. Train for 50 epochs. Log: distillation loss, cross-entropy loss, and KL divergence separately to MLflow per epoch to diagnose distillation quality.
> **📦 Stack:** torch, pytorch-lightning, mlflow
> **✅ Outcome:** Distilled lightweight Transformer achieves F1 within 3% of the full Transformer. KL divergence converges. Both loss components are logged separately.

---

## Phase 36 — Quantisation & Deployment Profiling

**Context:** Quantisation reduces model size and CPU inference latency. Deployment profiling determines the composite deployment score for all six models.

#### Subphase 36.1 — INT8 Quantisation

> **🎭 Role:** Senior ML Inference Optimisation Engineer
> **📍 Context:** INT8 quantisation reduces weights from float32 to int8, typically achieving 2-4× speedup on CPU with < 1% accuracy loss for classification tasks.
> **🔧 Task:** Apply PyTorch dynamic INT8 quantisation to the Lightweight Transformer model. Use `torch.quantization.quantize_dynamic(model, {nn.Linear}, dtype=torch.qint8)`. Measure and compare: model file size (MB) before and after quantisation; F1 macro before and after (verify F1 loss < 1%); inference latency P99 before and after on 5000 single-event batches. Log all comparisons to MLflow. If F1 loss exceeds 1%, try `torch.quantization.prepare_qat` for quantisation-aware training instead.
> **📦 Stack:** torch 2.3, mlflow, numpy
> **✅ Outcome:** Quantised model is smaller and faster. F1 loss is < 1%. Size and latency comparisons are logged.

#### Subphase 36.2 — Composite Deployment Score Computation

> **🎭 Role:** MLOps Architect and Research Lead
> **📍 Context:** The CDS formula from Phase 1 combines F1, latency, and memory into a single deployment fitness score. Computing it for all six models determines which model wins on Pillar 3.
> **🔧 Task:** Implement `ml/src/evaluation/deployment_score.py`. `CompositeDeploymentScorer` with method `score(models_metrics: list[ThreePillarMetrics]) -> list[DeploymentScore]`. For each model: normalise F1 to [0, 1] across all six models (min-max); normalise 1/latency_p99; normalise 1/memory_mb. Apply CDS formula: `CDS = 0.40 × norm_f1 + 0.35 × norm_speed + 0.25 × norm_memory`. Produce a Pareto frontier plot: F1 vs latency scatter with model family labels. Log the CDS table and Pareto plot to MLflow.
> **📦 Stack:** numpy, matplotlib, mlflow, pydantic v2
> **✅ Outcome:** CDS scores are computed for all six models. The Pareto frontier plot is saved as a publishable figure.

---

## Phase 37 — Cross-Model Comparative Analysis

**Context:** The master comparison table is the central deliverable of the ML research phase. It answers all eight research questions and determines the Champion.

#### Subphase 37.1 — Master Comparison Table

> **🎭 Role:** Lead ML Research Scientist
> **📍 Context:** All six models have been trained and evaluated. MLflow contains all metrics. The comparison table collects them into the definitive ranked comparison.
> **🔧 Task:** Create `ml/notebooks/analysis/01_master_comparison.ipynb`. Load all six models' `ThreePillarMetrics` from MLflow using the `mlflow.search_runs` API. Build the master comparison DataFrame: rows are model families, columns are all metrics from all three pillars. Sort by CDS descending. Apply conditional formatting: highlight max value per column in green, min value in red. Export as: (1) styled HTML for the research paper; (2) CSV for the admin panel ReportGenerator; (3) Markdown for the CONTRIBUTING guide. Log all three to MLflow.
> **📦 Stack:** mlflow, pandas, matplotlib
> **✅ Outcome:** The master comparison table is exported in all three formats. The CSV is the source of truth that the admin panel's ReportGenerator loads.

#### Subphase 37.2 — Per-Attack F1 Heatmap

> **🎭 Role:** ML Research Scientist
> **📍 Context:** Overall F1 macro hides per-attack-class performance differences. The heatmap reveals which models excel at specific attack types.
> **🔧 Task:** In the comparison notebook, generate a seaborn heatmap: x-axis = 7 attack taxonomy classes, y-axis = 6 model families. Cell values = per-class F1. Colour scale from red (0.0) to green (1.0). Annotate each cell with the F1 value. This heatmap is Figure 2 of the research paper. Save as a high-resolution PNG.
> **📦 Stack:** seaborn, matplotlib
> **✅ Outcome:** The per-attack heatmap is saved as a 300 DPI publication-quality figure.

#### Subphase 37.3 — Challenger Selection & Champion Confirmation

> **🎭 Role:** MLOps Lead and Research Director
> **📍 Context:** Based on the comparative analysis, the best non-XGBoost model becomes the Challenger. The research must justify both the Champion selection and the Challenger selection.
> **🔧 Task:** Write a structured decision document in the notebook. Champion justification: XGBoost wins on CDS because [specific numbers from P36]. Challenger selection: [Model X] is selected as Challenger because it has the highest F1 among non-Champions with acceptable latency. Update MLflow Model Registry: set the Challenger model alias to `CHALLENGER`. Update `docs/champion-challenger-status.md` with the current Champion and Challenger, their metrics, and the selection justification.
> **📦 Stack:** mlflow
> **✅ Outcome:** MLflow shows exactly one CHAMPION and one CHALLENGER alias. The status document is committed.

---

## Phase 38 — Statistical Significance Testing

**Context:** Research claims about model superiority must be statistically validated. Without significance testing, apparent differences may be random variation.

#### Subphase 38.1 — McNemar's Test Implementation

> **🎭 Role:** ML Research Scientist with statistical testing expertise
> **📍 Context:** McNemar's test evaluates whether two classifiers differ in their errors on the same test set. It is the appropriate test for paired binary classification results.
> **🔧 Task:** Implement `ml/src/evaluation/significance.py`. `McNemarTest` class: `test(predictions_a: np.ndarray, predictions_b: np.ndarray, y_true: np.ndarray) -> McNemarResult` using `statsmodels.stats.contingency_tables.mcnemar`. `McNemarResult` Pydantic model: `chi2`, `p_value`, `is_significant` (p < 0.05 / n_comparisons with Bonferroni correction for 15 pairwise tests), `interpretation: str`. Run the test for all 15 pairwise model comparisons (6 choose 2). Build the 6×6 significance matrix as a pandas DataFrame.
> **📦 Stack:** statsmodels, numpy, pandas, pydantic v2
> **✅ Outcome:** All 15 pairwise McNemar tests are computed. The significance matrix shows which model pairs differ significantly after Bonferroni correction.

#### Subphase 38.2 — Confidence Intervals

> **🎭 Role:** ML Research Scientist
> **📍 Context:** Point estimates of F1 do not communicate uncertainty. Bootstrap confidence intervals quantify the precision of each model's performance estimate.
> **🔧 Task:** Implement bootstrap confidence intervals for all six models in `significance.py`. `bootstrap_ci(model: XAIGuardModel, X_test: np.ndarray, y_test: np.ndarray, metric: str, n_bootstrap: int = 1000, confidence: float = 0.95) -> ConfidenceInterval`. Resample test set with replacement N times; compute metric each time; report [2.5th, 97.5th percentile] as the CI. Add results to the master comparison table as `f1_macro_ci_lower` and `f1_macro_ci_upper` columns. Present as mean ± (CI half-width).
> **📦 Stack:** numpy, sklearn
> **✅ Outcome:** Each model has a 95% bootstrap CI for F1 macro. The CI widths indicate which model's performance estimate is most reliable.

---

## Phase 39 — SHAP Explainability Implementation

**Context:** SHAP is the primary XAI method. It provides theoretically grounded feature importance values for every prediction, enabling the analyst dashboard's Threat Detection card.

#### Subphase 39.1 — Unified SHAP Explainer Interface

> **🎭 Role:** Senior XAI Research Engineer
> **📍 Context:** Three SHAP explainer variants are needed: TreeExplainer for XGBoost/RF, DeepExplainer for LSTM/Transformer, and GradientExplainer as a fallback. They must be unified behind the same interface.
> **🔧 Task:** Implement `ml/src/xai/shap_explainer.py`. `XAIGuardSHAPExplainer` class with `explain(model: XAIGuardModel, X: np.ndarray, n_samples: int = 100) -> SHAPExplanation`. Internally: if `model_family` in [RF, XGBoost] → use `shap.TreeExplainer`; if [LSTM, Transformer, LT] → use `shap.DeepExplainer` with 50 background samples; fallback → `shap.GradientExplainer`. Return `SHAPExplanation` Pydantic model: `shap_values: np.ndarray`, `base_values: np.ndarray`, `feature_names: list[str]`, `top_k_features: list[FeatureContribution]` (top 5 by absolute SHAP). Validate additivity: `|sum(shap_values, axis=1) + base_value - log_odds| < 0.1` for each sample.
> **📦 Stack:** shap 0.45, torch, sklearn, pydantic v2
> **✅ Outcome:** `explainer.explain(xgboost_model, X_test[:100])` returns a `SHAPExplanation` with correct shapes. The additivity validation passes for all samples.

#### Subphase 39.2 — Global SHAP Analysis

> **🎭 Role:** ML Research Scientist
> **📍 Context:** Global SHAP analysis explains which features drive the model's decisions across all predictions, not just individual ones. This is Figure 3 of the research paper.
> **🔧 Task:** Create `ml/notebooks/xai/01_shap_global.ipynb`. Compute SHAP values for 1000 test samples across all six models. For each model: (1) beeswarm summary plot (feature impact direction and magnitude); (2) mean absolute SHAP bar chart (global importance); (3) SHAP dependence plot for the top 3 features; (4) SHAP interaction values for XGBoost (pairwise feature interaction heatmap). Compare the feature importance rankings across all six models as a rank correlation matrix using Spearman's ρ.
> **📦 Stack:** shap, matplotlib, seaborn, scipy
> **✅ Outcome:** All SHAP plots are saved as publication-quality figures. The Spearman rank correlation matrix quantifies agreement between model families' feature importance.

#### Subphase 39.3 — SHAP Stability Testing

> **🎭 Role:** XAI Research Engineer
> **📍 Context:** SHAP explanations must be stable: the same input should produce the same top features across repeated calls. Unstable explanations would undermine analyst trust.
> **🔧 Task:** Implement `ml/src/xai/stability.py`. `SHAPStabilityTester` that runs the SHAP explainer 10 times on the same 50 test samples and computes the coefficient of variation (CV) of SHAP values per feature per sample. `stability_score = 1 - mean(CV_across_features)`. A stability score > 0.95 is acceptable. For stochastic models (DeepExplainer uses random background samples), fix the random seed. Log stability scores per model to MLflow.
> **📦 Stack:** shap, numpy, mlflow
> **✅ Outcome:** All deterministic models (LR, RF, XGBoost) have stability score = 1.0. Deep learning models have stability score > 0.95 with fixed seed.

---

## Phase Map

| Phase | Title | Subphases |
|-------|-------|-----------|
| P33 | Transformer Encoder Architecture | 4 |
| P34 | Transformer Encoder Training | 2 |
| P35 | Lightweight Transformer & Distillation | 2 |
| P36 | Quantisation & Deployment Profiling | 2 |
| P37 | Cross-Model Comparative Analysis | 3 |
| P38 | Statistical Significance Testing | 2 |
| P39 | SHAP Explainability Implementation | 3 |

**Previous ←** [04 — Classical ML & Sequence Models](04-ml-research-and-experiments.md) | **Next →** [06 — LIME, XAI Evaluation & Backend Core](06-backend-and-frontend-engineering.md)
