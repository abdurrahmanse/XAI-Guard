# 05 — Transformer Architecture & XAI Evaluation

> **Phases 33–39** | Transformer Encoder, Transformer training, Lightweight Transformer with knowledge distillation, quantisation and deployment profiling, cross-model comparative analysis, statistical significance testing, and SHAP implementation.

## 🗺️ Research Paper Map

| Phase | What You Build | Paper Section | Paper Artefact |
|-------|---------------|---------------|----------------|
| P33 | Transformer architecture | §4.3 Deep Learning Models | Architecture description + diagram |
| P34 | Transformer training + HPO | §4.3 Table 4, Row 5 | Transformer metrics |
| P35 | Lightweight Transformer (distillation) | §4.3 Table 4, Row 6 | LT metrics + distillation analysis |
| P36 | Quantisation + CDS | §6 Operational Fitness | Table 6: Latency, Figure 5: Pareto |
| P37 | Master comparison table | §4.3 Table 4 (complete) | Central result of the entire paper |
| P38 | Statistical significance | §5 Statistical Analysis | McNemar matrix, CIs, effect sizes |
| P39 | SHAP implementation | §4.4 Explainability | Figure 3: SHAP, stability scores |

> **This document contains the two most important phases in the entire project:** P37 (master comparison) and P38 (statistical significance). Without P38, your paper cannot make statistically valid claims about model superiority. Without P37, there is no central result.

---

---

## Phase 33 — Transformer Encoder Architecture

**Context:** The Transformer Encoder is the most powerful model in the benchmark. Its self-attention mechanism produces the richest XAI signal via Attention Rollout.


### 🎓 What You Will Learn in Phase 33
You will implement the Transformer Encoder architecture from the ground up in PyTorch. This is the most architecturally complex model in your benchmark. You will learn: scaled dot-product attention, multi-head attention, Pre-Layer Norm (Pre-LN) transformers, and Attention Rollout for XAI.

### 📄 Research Paper Connection
- Phase 33.1–33.2 → **§4.3 Architecture**: "The Transformer Encoder uses N Pre-LN encoder blocks with H attention heads and d_model dimensions. Attention weights are stored at each layer for Attention Rollout XAI extraction (Abnar & Zuidema, 2020)."
- Phase 33.3 → **§4.4 Explainability**: Attention Rollout is your third XAI method alongside SHAP and LIME

### 📖 Concept: Scaled Dot-Product Attention
The core operation of a Transformer. Each event (query Q) looks at all other events (keys K) and decides how much to attend to each:
1. `scores = QKᵀ / √d_k` (scale prevents vanishing gradients)
2. `attention_weights = softmax(scores)` — each row sums to 1.0
3. `output = attention_weights × V`

**Security intuition:** When predicting whether event_10 is malicious, attention allows it to strongly attend to event_3 (where the port scan began) even though they are 7 steps apart. This long-range dependency is impossible for LSTM to model as effectively.

**Multi-head attention:** Run H attention operations in parallel (each on a d_model/H subspace), then concatenate. Each head can focus on different aspects — one head on temporal proximity, another on port patterns.

### 📖 Concept: Pre-LN vs Post-LN Transformers
Original Transformer (Vaswani et al., 2017) used Post-LN: LayerNorm AFTER the residual connection. This is hard to train — requires careful warm-up. Pre-LN (used here): LayerNorm BEFORE the attention/FFN operation. Produces more stable gradients. (Liu et al., 2020)

**In your paper:** "We use the Pre-LN Transformer architecture (Liu et al., 2020) for improved training stability."

### ⚠️ Common Mistakes — Transformer Architecture
- **n_heads must divide d_model**: If d_model=128 and n_heads=6 → 21.3 dims/head. Always validate: `assert d_model % n_heads == 0`.
- **Not storing attention weights**: Use `self.last_attention_weights = attention_weights.detach()` inside `torch.no_grad()`.
- **Not calling `model.eval()`**: Dropout is active during training. Always call `model.eval()` before inference.

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


### 🎓 What You Will Learn in Phase 34
You will train the full Transformer with a cosine warm-up learning rate schedule and Optuna search. This is the most compute-expensive phase — budget accordingly. You will learn why Transformers need warm-up and how to save attention weights as research artefacts.

### 📄 Research Paper Connection
- Phase 34 → **Table 4, Row 5**: Full Transformer three-pillar metrics
- Phase 34.2 Attention weights → Used in **Phase 41** (Attention Rollout XAI) → **Figure 3d** (attention heatmap)

### 📖 Concept: Learning Rate Warm-Up
Transformers are sensitive to learning rate at the start of training. Warm-up solution: start with a very small LR, increase linearly to the target over N_warmup steps, then decay via cosine schedule.

```
Step 0 → N_warmup:        lr = target_lr × (step / N_warmup)
Step N_warmup → N_total:  lr = target_lr × cos(π × step / N_total)
```

**Intuition:** Warm-up lets the model build reasonable initial representations before applying the full learning rate. Once stable, cosine decay gradually refines them without large destructive updates.

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


### 🎓 What You Will Learn in Phase 35
Knowledge distillation trains a small "student" model to mimic a large "teacher" model. You will learn: soft targets, temperature scaling, and distillation loss. This produces the Lightweight Transformer — which may fit within the 100ms production latency budget while retaining most accuracy.

### 📄 Research Paper Connection
- Phase 35 → **Table 4, Row 6**: Lightweight Transformer metrics
- Phase 35 → **§4.3**: "Knowledge distillation (Hinton et al., 2015) was used to compress the full Transformer into a model with <500K parameters..."
- Phase 35 answers **RQ3**: "Does the Transformer accuracy gain exceed its GPU-hour cost?"

### 📖 Concept: Knowledge Distillation and Temperature Scaling
Key insight (Hinton et al., 2015): the teacher's **soft probability outputs** contain more information than hard labels. The teacher might predict `{BENIGN: 0.85, DDoS: 0.12}` — the soft probabilities tell the student "this event has some DDoS characteristics," which the hard label "BENIGN" does not.

**Temperature T:** `softmax(logits / T)` — higher T → more uniform → more "dark knowledge" in secondary predictions.

**Distillation loss:**
`L = α × KL(student_probs/T || teacher_probs/T) + (1−α) × CrossEntropy(student, hard_labels)`

Default α=0.7, T=4. Use T=1 (standard softmax) at evaluation time.

### ⚠️ Common Mistakes — Knowledge Distillation
- **Not freezing the teacher**: Always `teacher.eval()` with no gradients during distillation.
- **Using temperature at evaluation**: Only use T during training for the distillation loss — T=1 at test time.

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


### 🎓 What You Will Learn in Phase 36
You will apply INT8 quantisation to the Lightweight Transformer and compute the Composite Deployment Score (CDS) for all six models. The CDS is your Pillar 3 summary metric. The Pareto frontier plot is Figure 5 of your paper.

### 📄 Research Paper Connection
- Phase 36.1 → **Table 6**: Before/after quantisation (size, speed, F1)
- Phase 36.2 → **Figure 5**: Pareto frontier — the key operational trade-off visualisation
- Phase 36 answers **RQ3** (accuracy vs GPU-hour trade-off) and **RQ6** (most cost-efficient model)

### 📖 Concept: INT8 Quantisation
Standard neural networks use float32 (32 bits per weight). INT8 converts to 8-bit integers: 4× smaller model, 2–4× faster inference on modern CPUs, typically <1% F1 loss for classification tasks.

`torch.quantization.quantize_dynamic(model, {nn.Linear}, dtype=torch.qint8)`

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


### 🎓 What You Will Learn in Phase 37
This is the most important phase in the entire project. You will build the master comparison table that is the central result of your research paper. You will learn: how to load results from MLflow programmatically, pandas conditional formatting for publication tables, and how to make the Champion/Challenger selection decision with documented justification.

### 📄 Research Paper Connection
- Phase 37.1 → **Table 4 (complete)**: The entire master comparison table — the primary result of your paper
- Phase 37.2 → **Figure 2**: Per-attack-class F1 heatmap
- Phase 37.3 → **§4.3 Champion Selection**: Justification text for why XGBoost is Champion

### ⚠️ Common Mistakes — Master Comparison Table
- **Mixing validation F1 with test F1**: Table 4 must use TEST SET metrics only. Validation metrics are for hyperparameter selection.
- **Not normalising before CDS**: The CDS formula requires min-max normalisation across all six models. Don't compute CDS from raw F1/latency values.
- **Reporting too many decimal places**: Report F1 to 3 decimal places (e.g., 0.941) and latency to 1 decimal (e.g., 12.4 ms). More precision implies false confidence.


### 🎓 What You Will Learn in Phase 37
This is the most important phase in the entire project. You will build the master comparison table that is the central result of your research paper. You will learn: programmatic MLflow result loading, pandas conditional formatting for publication tables, and how to make the Champion selection decision with documented justification.

### 📄 Research Paper Connection
- Phase 37.1 → **Table 4 (complete)**: The primary result of your paper — all 6 models × all metrics
- Phase 37.2 → **Figure 2**: Per-attack-class F1 heatmap
- Phase 37.3 → **§4.3 Champion Selection**: Justification text for why XGBoost is Champion

### ⚠️ Common Mistakes — Master Comparison Table
- **Mixing validation and test F1**: Table 4 must use TEST SET metrics only.
- **Not normalising before CDS**: CDS formula requires min-max normalisation across all 6 models.
- **Reporting too many decimal places**: F1 to 3 decimal places (0.941), latency to 1 decimal (12.4 ms).

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


### 🎓 What You Will Learn in Phase 38
Statistical significance testing is what separates a research paper from a blog post. You will learn McNemar's test, bootstrap confidence intervals, and effect size computation. Without Phase 38, your claims of model superiority are statistically unsubstantiated.

### 📄 Research Paper Connection
- Phase 38.1 → **§5 Statistical Analysis**: McNemar significance matrix (15 pairwise comparisons)
- Phase 38.2 → **Table 4** (each F1 gets ± CI): "XGBoost F1=0.941 (95% CI: [0.937, 0.945])"
- **New Subphase 38.3** → Effect sizes (Cohen's d)
- **New Subphase 38.4** → Writing the complete statistical results section

### 📖 Concept: McNemar's Test
McNemar's test answers: "Do models A and B make DIFFERENT errors?" For a pair of models, build a 2×2 contingency table of correct/incorrect predictions, then: `χ² = (|n01 − n10| − 1)² / (n01 + n10)` → compare to chi-squared distribution.

**Bonferroni correction:** You do C(6,2)=15 pairwise comparisons. Use threshold α/15 = 0.0033 per test.

**In your paper:** "We applied McNemar's test (α=0.05, Bonferroni-corrected, threshold p<0.0033) to assess all 15 pairwise model comparisons."

### 📖 Concept: Bootstrap Confidence Intervals
1. Resample test set WITH replacement 1000 times
2. Compute F1 on each resample
3. Report 2.5th and 97.5th percentile → 95% CI

Narrow CI = large test set, stable estimates. Wide CI = small test set, results may vary.

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


#### Subphase 38.3 — Effect Size Computation

> **🎭 Role:** ML Research Scientist with statistical expertise
> **📍 Context:** Statistical significance (p-value) tells you whether a difference is real. Effect size tells you whether it is MEANINGFUL. A model statistically significantly better by 0.001 F1 is real — but practically negligible. Reviewers increasingly require effect sizes alongside p-values.
> **🔧 Task:** Implement `ml/src/evaluation/effect_size.py`. For each of the 15 pairwise model comparisons: compute Cohen's d = `(mean_A − mean_B) / pooled_std` using 1000 bootstrap F1 distributions. Interpret: |d| < 0.2 = negligible, 0.2–0.5 = small, 0.5–0.8 = medium, >0.8 = large. Also compute Cliff's delta (non-parametric) as robustness check. Build a 6×6 effect size matrix. Save as `ml/artifacts/effect_sizes.csv`.
> **📦 Stack:** numpy, scipy, pandas
> **✅ Outcome:** Effect size matrix shows which comparisons are practically meaningful. Comparisons with |d| < 0.2 are reported as "statistically significant but practically negligible."

#### Subphase 38.4 — Writing the Statistical Results Section

> **🎭 Role:** ML Research Scientist and Technical Writer
> **📍 Context:** Statistical results must be reported in specific academic format. This subphase produces the complete text of §5 (Statistical Analysis) of your paper.
> **🔧 Task:** Create `ml/notebooks/analysis/03_statistical_results_writing.ipynb`. Write §5.1 Significance Testing, §5.2 Confidence Intervals, and §5.3 Effect Sizes using the templates from the concept sections above. Fill in all placeholders with real numbers from the effect_sizes.csv and bootstrap CI CSVs. The notebook's markdown output IS your paper's §5.
> **📦 Stack:** Jupyter Markdown, pandas
> **✅ Outcome:** A complete draft of §5 (Statistical Analysis) ready for inclusion in the paper.


---

## Phase 39 — SHAP Explainability Implementation

**Context:** SHAP is the primary XAI method. It provides theoretically grounded feature importance values for every prediction, enabling the analyst dashboard's Threat Detection card.


### 🎓 What You Will Learn in Phase 39
SHAP (SHapley Additive exPlanations) is your primary XAI method. You will learn: the Shapley value game-theoretic foundation, the three SHAP explainer variants (TreeExplainer, DeepExplainer, GradientExplainer), global vs local explanations, and SHAP stability testing.

### 📄 Research Paper Connection
- Phase 39.1–39.2 → **Figure 3**: SHAP beeswarm plots for all 6 models (panels a–f)
- Phase 39.2 Spearman ρ → **§4.4**: "Feature importance rankings showed Spearman correlation of ρ=X across model families..."
- Phase 39.3 Stability → **Table 8**: XAI stability comparison per model
- **New Subphase 39.4** → **Figure 4**: LIME vs SHAP correlation (answers RQ4)
- **New Subphase 39.5** → **Table 9**: Analyst Utility Composite Score per model (completes Pillar 2)

### 📖 Concept: SHAP — Why Shapley Values?
Based on Shapley values from cooperative game theory (Shapley, 1953). For each feature i, the Shapley value is the average marginal contribution across all possible feature orderings. This ensures: (1) SHAP values sum to the prediction (additivity); (2) equal-contribution features get equal values (symmetry); (3) useless features get SHAP=0 (dummy); (4) same framework for all 6 models (model-agnostic).

**Reference:** Lundberg & Lee, 2017 "A Unified Approach to Interpreting Model Predictions" (NeurIPS 2017)

### ⚠️ Common Mistakes — SHAP Analysis
- **Confusing global and local SHAP**: Local SHAP explains one prediction. Global SHAP (mean |SHAP|) explains the model overall. Your paper needs both.
- **Not verifying additivity**: SHAP values must sum to `prediction − base_value` for each sample. If not (within 0.1 tolerance), your explainer is misconfigured.
- **Computing SHAP on the full test set**: SHAP is slow. Use 1000 stratified-by-class representative test samples for global analysis.

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


#### Subphase 39.4 — LIME vs SHAP Correlation Analysis

> **🎭 Role:** XAI Research Scientist
> **📍 Context:** RQ4 asks which XAI method produces more analyst-actionable explanations. As a first step, compute the agreement between LIME and SHAP on the same predictions — high correlation means both agree; low correlation means conflicting explanations (a problem for analysts who must decide which to trust).
> **🔧 Task:** Create `ml/notebooks/xai/02_lime_shap_correlation.ipynb`. For 200 test samples (balanced across 7 classes): compute SHAP and LIME top-10 feature rankings. Compute Spearman's rank correlation (ρ) per sample. Report mean ρ, median ρ, ρ per attack class. Build LIME-SHAP correlation Table 8 for all 6 models. Save Figure 4 (SHAP rank vs LIME rank scatter) at 300 DPI.
> **📦 Stack:** shap, lime, scipy, matplotlib, pandas
> **✅ Outcome:** Table 8 (LIME-SHAP correlation) is complete. Figure 4 is publication-quality. This directly answers RQ4.

#### Subphase 39.5 — Analyst Utility Composite Score

> **🎭 Role:** XAI Research Scientist and Human Factors Researcher
> **📍 Context:** The evaluation framework (Phase 1.3) defines Pillar 2's analyst utility composite score with 5 sub-metrics. This completes Pillar 2. Without this, the XAI evaluation section is missing its summary metric.
> **🔧 Task:** Implement `ml/src/evaluation/analyst_utility.py`. `AnalystUtilityScorer` computing for each model: (1) Feature Conciseness — fraction where top-5 features explain >80% of |SHAP|; (2) Explanation Consistency — same features in top-5 for same attack type; (3) Explanation Speed — relative XAI computation time; (4) SHAP-LIME Agreement — mean ρ from Subphase 39.4; (5) Additivity Compliance — binary check. Composite: `AUS = 0.25×C1 + 0.25×C2 + 0.20×C3 + 0.20×C4 + 0.10×C5`. Log all sub-metrics and AUS to MLflow.
> **📦 Stack:** numpy, shap, lime, mlflow, pydantic v2
> **✅ Outcome:** All 6 models have an AUS score. This completes Pillar 2 of the evaluation framework and produces Table 9 of the paper.

### ✅ Learning Checkpoint — Phases 33–39
1. McNemar's test gives p=0.04 for the XGBoost vs LSTM comparison. After Bonferroni correction for 15 tests (threshold p<0.0033), is this significant? What does this mean for your paper's claim?
2. Your Transformer achieves F1=0.955 but latency P99=240ms. The production budget is 100ms. Can it be the Champion? What is the CDS score telling you?
3. A student reports "SHAP shows that bytes_per_packet is the most important feature." What is the difference between saying this for a specific prediction (local SHAP) vs for the model overall (global SHAP)? Why does this distinction matter for an analyst?

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
