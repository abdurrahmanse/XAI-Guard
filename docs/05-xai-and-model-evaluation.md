# 05 — Transformer Models, Comparative Analysis & XAI

> **Phases 33–39** | Transformer Encoder architecture and training, Lightweight Transformer with knowledge distillation, cross-model comparative analysis, statistical significance testing, and SHAP explainability implementation.
>
> **How to use:** Pick one subphase. Copy its **Prompt** into your AI code editor. Implement it. Move to the next subphase.

---

## Phase 33 — Transformer Encoder Architecture

**Context:** The Transformer Encoder is the primary research model. Self-attention allows it to model relationships between all events in a sequence simultaneously, unlike LSTM's sequential processing. Building the architecture correctly before training avoids costly rewrites.

#### Subphase 33.1 — Positional Encoding Module
> **Prompt:** Implement the sinusoidal positional encoding module for XAI-Guard Transformer. The module adds a fixed positional pattern to each position in the input sequence so the model can distinguish event ordering. It must support configurable embedding dimension and maximum sequence length. Write a unit test that verifies different positions produce different encoding vectors and that the module can be applied to a batch of sequences without error.

#### Subphase 33.2 — Transformer Encoder Block
> **Prompt:** Implement the Transformer encoder block for XAI-Guard. The block consists of a multi-head self-attention layer followed by a position-wise feed-forward network, with residual connections and layer normalisation applied in the pre-norm style. The block must be configurable by the number of attention heads, feed-forward hidden dimension, and dropout rate. Store the raw attention weights during the forward pass so they can be extracted for the attention explainability module in Phase 41.

#### Subphase 33.3 — Full Transformer Model
> **Prompt:** Implement the full XAI-Guard Transformer model following the common base interface from Phase 26. The model stacks N encoder blocks, applies a pooling strategy over the sequence dimension (configurable between CLS token pooling and mean pooling), passes the result through a classification head. The model must accept the sequence input format produced by the sequence builder from Phase 23 and be fully configurable via a parameter dictionary.

#### Subphase 33.4 — Attention Weight Extraction
> **Prompt:** Implement the attention weight extraction interface for the XAI-Guard Transformer. Add a method that runs a forward pass and returns both the prediction and the raw attention weight tensors from every encoder block. These weights are used by the attention explainability module in Phase 41 and by the attention rollout algorithm. Write a unit test confirming the attention weight shape is (batch, n_heads, seq_len, seq_len) for each layer.

#### Subphase 33.5 — Architecture Unit Tests
> **Prompt:** Write comprehensive unit tests for the XAI-Guard Transformer architecture. Verify: forward pass produces the correct output shape for various batch sizes, sequence lengths, and number of features; the model handles sequence length 1 (single event) without error; gradient flow is verified through all layers on the first backward pass; the attention weights for each layer sum to one across the key dimension; and the model can be saved and loaded with identical parameter values.

---

## Phase 34 — Transformer Encoder Training

**Context:** Train the Transformer with a warm-up learning rate schedule and Optuna-based hyperparameter search. The Transformer requires more careful optimisation than classical models due to its sensitivity to learning rate and warm-up duration.

#### Subphase 34.1 — PyTorch Lightning Trainer
> **Prompt:** Implement the PyTorch Lightning trainer for the XAI-Guard Transformer Encoder. Define training_step, validation_step, and test_step. Implement configure_optimizers with AdamW and a linear warm-up followed by cosine annealing schedule, which is the standard Transformer training recipe. Configure early stopping on validation F1 macro with patience of 10 epochs (higher than LSTM because Transformers converge more slowly). Log all metrics to MLflow at every epoch.

#### Subphase 34.2 — Warm-Up Learning Rate Scheduler
> **Prompt:** Implement the linear warm-up with cosine annealing learning rate scheduler for XAI-Guard Transformer training. The scheduler linearly increases the learning rate from zero to the target learning rate over the first W warm-up steps, then decays it following a cosine curve to a minimum learning rate at the end of training. W is a tunable hyperparameter. This scheduler is critical for Transformer convergence stability. Plot the learning rate curve for the default configuration as part of the training documentation.

#### Subphase 34.3 — Optuna Hyperparameter Search
> **Prompt:** Configure and run the Optuna hyperparameter search for the XAI-Guard Transformer Encoder. The search space covers: number of encoder layers from 1 to 4, number of attention heads across 2 4 and 8, feed-forward dimension as a multiple of the embedding dimension, dropout rate from 0.1 to 0.4, learning rate on a log scale, warm-up fraction from 0.05 to 0.20 of total training steps, and batch size across 64 128 and 256. Run 50 trials with early pruning after 15 epochs.

#### Subphase 34.4 — Full Training Run & Metrics
> **Prompt:** Run the full XAI-Guard Transformer training with the best hyperparameters from the Optuna study. Log complete training curves to MLflow. After training, evaluate on the held-out test set using the standard metrics harness, compute per-attack-type F1 breakdown, profile inference latency at four batch sizes, and save the model artifact with the attention weight extraction method intact. Register the model as a candidate in the MLflow Model Registry.

#### Subphase 34.5 — Attention Weight Saving
> **Prompt:** Add attention weight artifact saving to the XAI-Guard Transformer training script. After the final model is trained, run the forward pass on 200 test samples with attention weight extraction enabled, save the resulting attention tensors as a NumPy artifact to MLflow, and log metadata about the attention patterns: the mean attention entropy per layer (high entropy means distributed attention, low entropy means focused attention). These saved weights are used by the attention explainability phase.

#### Subphase 34.6 — Transformer Analysis Notebook
> **Prompt:** Create a Jupyter analysis notebook for the XAI-Guard Transformer Encoder. Include: training and validation loss curves, the Optuna trial history, confusion matrix, per-attack-type F1 comparison against XGBoost and LSTM, latency-vs-batch-size comparison showing all three models, and attention heatmap visualisations for three example sequences covering DDoS, BruteForce, and Normal traffic. The attention heatmaps are key research paper figures.

---

## Phase 35 — Lightweight Transformer & Knowledge Distillation

**Context:** The Lightweight Transformer answers RQ3 and RQ6: can we get near-Transformer performance at near-XGBoost cost? Knowledge distillation trains the smaller model to match the larger Transformer's soft predictions, improving accuracy beyond training from scratch.

#### Subphase 35.1 — Lightweight Architecture Design
> **Prompt:** Design the Lightweight Transformer architecture for XAI-Guard. The model is a reduced version of the full Transformer: a maximum of 2 encoder blocks, a smaller embedding dimension, and a smaller feed-forward dimension. The architecture must be at least 5 times smaller than the full Transformer in parameter count and must meet the inference latency budget of P99 under 100 milliseconds on CPU hardware. Document the exact architecture choices and their rationale.

#### Subphase 35.2 — Scratch Training Baseline
> **Prompt:** Train the XAI-Guard Lightweight Transformer from scratch on the same dataset as the full Transformer, using the same training recipe but without any knowledge distillation. This establishes the baseline performance of the smaller architecture. Log all metrics to MLflow and compare against the full Transformer to quantify the accuracy cost of reducing model size.

#### Subphase 35.3 — Knowledge Distillation Loss
> **Prompt:** Implement the knowledge distillation loss function for XAI-Guard. The loss combines: cross-entropy loss between the student model's predictions and the true labels, weighted by (1 - alpha); and Kullback-Leibler divergence between the student's softened output probabilities and the teacher Transformer's softened output probabilities at temperature T, weighted by alpha. Both alpha and temperature T are configurable hyperparameters. Write a unit test that verifies the loss is lower when the student and teacher agree than when they disagree.

#### Subphase 35.4 — Distillation Training Run
> **Prompt:** Implement the knowledge distillation training loop for XAI-Guard. Load the trained full Transformer as the frozen teacher model. Train the Lightweight Transformer student using the distillation loss from Phase 35.3. Search over alpha values of 0.3, 0.5, and 0.7, and temperature values of 2, 4, and 8, using a grid search. Log all distillation trial results to MLflow. Select the best configuration and compare the distilled student against the from-scratch baseline.

#### Subphase 35.5 — Distillation Improvement Analysis
> **Prompt:** Analyse the XAI-Guard knowledge distillation results. Compute the performance improvement from distillation over from-scratch training for the Lightweight Transformer: delta in F1 macro, delta in ROC-AUC, and delta in per-attack-type F1. Document which attack types benefit most from distillation. Register the best distilled Lightweight Transformer model in the MLflow Model Registry.

---

## Phase 36 — Quantisation & Deployment Profiling

**Context:** Before the comparative analysis, profile every model under production-like deployment conditions: CPU-only inference (no GPU), realistic batch sizes, and memory constraints. This answers RQ6 (cost-efficient deployment).

#### Subphase 36.1 — Dynamic INT8 Quantisation
> **Prompt:** Apply dynamic INT8 quantisation to the XAI-Guard LSTM and Transformer models using PyTorch's dynamic quantisation API. Measure the accuracy delta caused by quantisation: the difference in F1 macro and ROC-AUC before and after quantisation. The accuracy delta must be below 1% for the quantised model to be considered deployment-viable. Log the delta and the quantised model file size to MLflow.

#### Subphase 36.2 — CPU-Only Latency Profiling
> **Prompt:** Profile all six XAI-Guard models for CPU-only single-event inference latency, simulating the production deployment condition where GPU acceleration is not available. Measure P50, P95, and P99 latency in milliseconds at batch size 1 for 1000 warm predictions. Compare the results across all six models in a single table and document which models meet the P99 under 100 milliseconds budget.

#### Subphase 36.3 — Memory Footprint Measurement
> **Prompt:** Measure the peak memory footprint of each XAI-Guard model during inference. Use tracemalloc or memory_profiler to record peak RSS memory consumption when running inference on a batch of 256 samples. Record both the model loading memory and the additional memory consumed per batch. Document which models fit within a 1 GB memory budget for deployment on standard server hardware.

#### Subphase 36.4 — Composite Deployment Score
> **Prompt:** Compute the composite deployment score for all six XAI-Guard models. The score combines three components: normalised F1 macro (weight 40%), normalised inverse inference latency P99 (weight 35%), and normalised inverse peak memory (weight 25%). Normalise each component to a 0-to-1 scale across the six models. Log the composite scores to MLflow. This score is the primary axis for the Pareto frontier analysis.

#### Subphase 36.5 — Pareto Frontier Analysis
> **Prompt:** Perform Pareto frontier analysis for XAI-Guard comparing all six models on the accuracy-versus-efficiency trade-off. Plot F1 macro on the y-axis against composite operational cost on the x-axis. Identify the Pareto-optimal models: those where no other model is better on both axes simultaneously. Create a Jupyter notebook that produces this plot as a high-resolution figure for the research paper.

---

## Phase 37 — Cross-Model Comparative Analysis

**Context:** This is the central research output — a complete quantitative comparison of all six models across all metrics. The analysis directly answers all eight research questions.

#### Subphase 37.1 — Master Comparison Table
> **Prompt:** Build the XAI-Guard master model comparison table. Fetch all six models' logged metrics from MLflow using the MlflowClient API. Construct a pandas DataFrame with models as rows and all evaluation metrics as columns: F1 macro, ROC-AUC, PR-AUC, precision macro, recall macro, per-attack-type F1 for each class, inference latency P99, peak memory, training time, and composite deployment score. Save the table as both a CSV artifact and a formatted markdown table.

#### Subphase 37.2 — Per-Attack-Type Heatmap
> **Prompt:** Create the per-attack-type F1 performance heatmap for XAI-Guard. The heatmap shows models on one axis and attack types on the other, with F1 score as the cell value and a colour scale from red (poor) to green (excellent). This visualisation immediately reveals which models struggle with specific attack types. Create the heatmap as a high-resolution figure using seaborn and save it as a PNG artifact in MLflow.

#### Subphase 37.3 — Cross-Dataset Generalisation Evaluation
> **Prompt:** Evaluate the XAI-Guard cross-dataset generalisation of all six models. Train each model on CICIDS-2017 and evaluate on UNSW-NB15 without any fine-tuning. Compute the generalisation gap as the difference in F1 macro between in-distribution and out-of-distribution evaluation. Log generalisation gaps to MLflow and create a bar chart showing which models are most robust to dataset shift.

#### Subphase 37.4 — Challenger Model Selection
> **Prompt:** Select the XAI-Guard Challenger model based on the comparative analysis results. The Challenger must: outperform the XGBoost Champion by the promotion thresholds defined in Phase 1, be Pareto-optimal on the efficiency frontier, and have been tested on at least two datasets. Document the selection rationale in a findings document. Update the PostgreSQL model registry to mark the selected model as challenger with shadow evaluation status.

#### Subphase 37.5 — Research Findings Document Update
> **Prompt:** Update the XAI-Guard research findings document with the comparative analysis results. Write the analysis section that answers each of the eight research sub-questions with specific numbers from the comparison table. For each question, state the finding, the supporting metric, the magnitude of the effect, and whether the finding is statistically significant (to be confirmed in Phase 38). This document is the draft results section of the research paper.

#### Subphase 37.6 — Comparative Analysis Notebook
> **Prompt:** Create the master comparative analysis Jupyter notebook for XAI-Guard. Include all visualisations that appear in the research paper: the per-attack-type F1 heatmap from Phase 37.2, the Pareto frontier chart from Phase 36.5, a radar chart comparing all six models across F1/AUC/Latency/Memory on a normalised scale, and a summary table with colour-coded cells highlighting the best model per metric. This notebook is the single source of truth for all research paper figures.

---

## Phase 38 — Statistical Significance Testing

**Context:** Research claims about model performance differences must be statistically validated. Without significance testing, observed differences might be due to random variation in the train/test split.

#### Subphase 38.1 — McNemar's Test Implementation
> **Prompt:** Implement McNemar's test for XAI-Guard model comparison. McNemar's test compares two classifiers on the same test set by examining cases where the models disagree. It tests whether the difference in error rates between two models is statistically significant. Implement the test for every pair of the six models, producing a 6x6 p-value matrix. Use a significance level of 0.05 with Bonferroni correction for multiple comparisons.

#### Subphase 38.2 — Significance Matrix & Visualisation
> **Prompt:** Create the pairwise statistical significance matrix for XAI-Guard. For each pair of models, display the McNemar's test p-value and a boolean indicating whether the difference is statistically significant after Bonferroni correction. Visualise this as a heatmap with green cells for significant differences and red cells for non-significant differences. Include the actual p-values as cell annotations. Save as a high-resolution research paper figure.

#### Subphase 38.3 — Confidence Interval Estimation
> **Prompt:** Compute 95% confidence intervals for the F1 macro of each XAI-Guard model using bootstrap resampling. Draw 1000 bootstrap samples from the test set predictions, compute F1 macro for each, and report the 2.5th and 97.5th percentile as the confidence interval bounds. Models whose confidence intervals do not overlap are definitively different at the 95% confidence level. Plot the confidence intervals as error bars on the model comparison bar chart.

#### Subphase 38.4 — Statistical Findings Documentation
> **Prompt:** Update the XAI-Guard research findings document with the statistical significance results. For each performance claim in the comparative analysis (e.g., XGBoost outperforms Random Forest), add the McNemar's test p-value and whether the claim is statistically significant. Flag any claims that appear important visually but do not reach statistical significance. This section ensures the research paper meets peer review standards for statistical rigour.

---

## Phase 39 — SHAP Explainability Implementation

**Context:** SHAP provides theoretically grounded feature attributions using cooperative game theory. It is the primary XAI method for XAI-Guard because it supports all six model families through different explainer variants.

#### Subphase 39.1 — Unified SHAP Explainer Design
> **Prompt:** Design the unified SHAP explainer interface for XAI-Guard that dispatches to the correct SHAP explainer variant based on model type. The interface exposes three methods: explain_local for computing SHAP values for a single prediction, explain_global for computing mean absolute SHAP values across a test set to represent global feature importance, and stability_score for measuring explanation consistency across repeated runs on the same input. Define the return types for each method as structured Pydantic models.

#### Subphase 39.2 — TreeExplainer for Classical Models
> **Prompt:** Implement the SHAP TreeExplainer integration for XAI-Guard covering Logistic Regression using LinearExplainer, Random Forest using TreeExplainer, and XGBoost using TreeExplainer. These explainers are exact (not approximate) and are the fastest of the SHAP variants. Write unit tests confirming that the sum of SHAP values plus the base value equals the model's raw prediction score for each model type.

#### Subphase 39.3 — DeepExplainer for LSTM
> **Prompt:** Implement the SHAP DeepExplainer integration for XAI-Guard LSTM. DeepExplainer uses a background dataset of representative samples to approximate SHAP values using the DeepLIFT algorithm. Configure the background dataset size to 100 samples. Handle the sequence input format correctly by reshaping the 3D sequence tensor into the format expected by DeepExplainer. Write a unit test confirming output shape and that values are in a reasonable range.

#### Subphase 39.4 — GradientExplainer for Transformer Models
> **Prompt:** Implement the SHAP GradientExplainer integration for XAI-Guard covering both the full Transformer Encoder and the Lightweight Transformer. GradientExplainer computes SHAP values by integrating gradients using the integrated gradients approximation, requiring PyTorch gradients to be enabled. Configure it with a background dataset of 50 samples. Test that the explainer produces stable outputs across repeated runs on the same input.

#### Subphase 39.5 — Global SHAP Computation
> **Prompt:** Implement the global SHAP analysis pipeline for XAI-Guard. For each of the six models, compute SHAP values for 1000 test samples, compute mean absolute SHAP per feature to get global importance rankings, and compute the Spearman rank correlation between each pair of models' global importance rankings. High correlation means models agree on which features matter most. Log all global SHAP results to MLflow as artifacts.

#### Subphase 39.6 — SHAP Stability Testing
> **Prompt:** Implement SHAP explanation stability testing for XAI-Guard. For each model, run the local SHAP explainer 10 times on the same 100 test samples. Compute the stability score as one minus the mean coefficient of variation of SHAP values across the 10 runs. A stability score of 1.0 means perfectly consistent explanations. Log stability scores per model to MLflow and document which models have explanations stable enough for analyst trust.

#### Subphase 39.7 — SHAP Analysis Notebook
> **Prompt:** Create the SHAP analysis Jupyter notebook for XAI-Guard. Include: a SHAP beeswarm plot for each of the six models showing the distribution of SHAP values per feature; waterfall plots for three representative samples covering DDoS, BruteForce, and Normal predictions; the global feature importance bar chart comparing all six models side-by-side; the stability score comparison bar chart; and the Spearman correlation heatmap between model pairs' feature importance rankings. These are primary research paper figures.

---

## Phase Map

| Phase | Title | Subphases |
|-------|-------|-----------|
| P33 | Transformer Encoder Architecture | 5 |
| P34 | Transformer Encoder Training | 6 |
| P35 | Lightweight Transformer & Knowledge Distillation | 5 |
| P36 | Quantisation & Deployment Profiling | 5 |
| P37 | Cross-Model Comparative Analysis | 6 |
| P38 | Statistical Significance Testing | 4 |
| P39 | SHAP Explainability Implementation | 7 |

**Previous ←** [04 — Classical ML & Sequence Models](04-ml-research-and-experiments.md) | **Next →** [06 — LIME, XAI Evaluation & Backend Core](06-backend-and-frontend-engineering.md)
