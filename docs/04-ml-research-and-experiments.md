# 04 — Classical ML & Sequence Model Experiments

> **Phases 26–32** | Common model interface, Logistic Regression baseline, Random Forest, XGBoost + Champion registration, LSTM architecture, LSTM training, and LSTM evaluation.

## 🗺️ Research Paper Map

| Phase | What You Build | Paper Section | Paper Artefact |
|-------|---------------|---------------|----------------|
| P26 | Common Model Interface + Evaluation Harness | §4.1 Experimental Setup | "All models implement identical interface..." |
| P27 | Logistic Regression baseline | §4.3 Table 4, Row 1 | F1 performance floor |
| P28 | Random Forest | §4.3 Table 4, Row 2 | LR vs RF comparison |
| P29 | XGBoost (Initial Champion) | §4.3 Table 4, Row 3 | Champion selection + SHAP beeswarm |
| P30 | BiLSTM architecture | §4.3 Deep Learning Setup | Architecture description |
| P31 | LSTM training + HPO | §4.3 Table 4, Row 4 | LSTM metrics + hidden states |
| P32 | LSTM evaluation + cross-dataset transfer | §4.3, §4.5 | Table 7 — generalisation gap |

> **Core Research Claims This Doc Produces:**
> - **RQ1** (classical vs deep): "XGBoost outperforms LR baseline by +ΔF1 but LSTM provides +ΔF1 on sequential attacks at 8× latency cost"
> - **RQ7** (cross-dataset generalisation): zero-shot UNSW-NB15 transfer results for classical models (completed in Subphase 32.4)

---


## Phase 26 — Common Model Interface Design

**Context:** All six models must implement an identical interface so evaluation, serialisation, and production serving are model-agnostic. Define the interface before writing a single model.


### 🎓 What You Will Learn in Phase 26
Before writing a single model, you design the interface that ALL six models share. This is foundational ML engineering for research: a Common Model Interface (CMI) guarantees your evaluation harness, XAI code, and production API are model-agnostic. It is also the reason your comparison is methodologically valid.

### 📖 Concept: Why Abstract Base Classes in ML Research?
When comparing 6 models, you need a guarantee that all are evaluated identically. Without a shared interface, you might compute F1 differently for different models — an invisible bug that makes the comparison unfair and the paper unsubmittable.

The Abstract Base Class (ABC) pattern enforces this: any class inheriting from `XAIGuardModel` MUST implement `fit`, `predict`, `predict_proba`, `save`, and `load`. If it doesn't, Python raises a `TypeError` at import time — before any experiment runs.

**In your paper (§4.1):** "All six models implement a common `XAIGuardModel` interface, ensuring evaluation conditions are identical. No model-specific code appears in the evaluation harness."

### 📖 Concept: Bayesian Hyperparameter Optimisation (Optuna TPE)
Most models in this project use Optuna with the TPE (Tree-structured Parzen Estimator) sampler. Grid search tests every combination — computationally infeasible for large spaces. Random search picks randomly — wastes trials on bad regions. TPE learns from previous trials, building a probabilistic model of which hyperparameters produce good results, sampling more from promising regions. This makes it 3–10× more efficient than random search.

**In your paper (§4.1):** "We used Optuna's TPE sampler with MedianPruner for hyperparameter search. We ran N trials per model, early-stopping unpromising trials at 10 epochs."

### ⚠️ Common Mistakes — Model Interface & Evaluation
- **Computing metrics differently per model**: Always use the harness. Never compute F1 manually in a notebook and compare with harness-computed F1 from another model.
- **Using test set for hyperparameter selection**: Optuna optimises on VALIDATION set F1. The test set is touched exactly once, at the very end, for the final reported table.
- **Reporting overall accuracy on imbalanced data**: CICIDS-2017 is 83% BENIGN. A model predicting all-BENIGN gets 83% accuracy but 0% recall on attacks. Always report F1 Macro AND per-class F1.

#### Subphase 26.1 — Abstract Model Interface

> **🎭 Role:** Principal ML Platform Architect
> **📍 Context:** Six model families will be trained and evaluated. The evaluation harness, the Champion/Challenger promotion logic, and the production inference service all depend on a shared interface. Defining it first prevents interface divergence.
> **🔧 Task:** Define `ml/src/models/base_model.py`. Abstract base class `XAIGuardModel(ABC)` with these abstract methods: `fit(X_train, y_train, X_val, y_val) -> TrainingResult`; `predict(X) -> np.ndarray` (class labels); `predict_proba(X) -> np.ndarray` (class probabilities, shape n_samples x n_classes); `save(path: Path) -> None`; `classmethod load(path: Path) -> XAIGuardModel`; `property feature_names: list[str]`; `property model_family: ModelFamily` (StrEnum). Define `TrainingResult` Pydantic v2 dataclass: `model_family`, `training_time_seconds`, `best_params`, `validation_f1_macro`, `mlflow_run_id`. All implementations must raise `NotFittedError` from sklearn if `predict` is called before `fit`.
> **📦 Stack:** abc, numpy, pydantic v2, scikit-learn, Python StrEnum
> **✅ Outcome:** `issubclass(XGBoostModel, XAIGuardModel)` is True for all six model classes. `isinstance(model, XAIGuardModel)` works for runtime type checking in the production inference service.

#### Subphase 26.2 — Three-Pillar Metrics Harness

> **🎭 Role:** Senior ML Evaluation Engineer
> **📍 Context:** Every model is evaluated with the same metrics. A shared harness ensures all models are compared on identical grounds and no metric is accidentally computed differently.
> **🔧 Task:** Implement `ml/src/evaluation/harness.py`. `ModelEvaluationHarness` class with method `evaluate(model: XAIGuardModel, X_test: np.ndarray, y_test: np.ndarray) -> ThreePillarMetrics`. Pillar 1 implementation: `sklearn.metrics.f1_score(average="macro")`, `roc_auc_score(multi_class="ovr")`, `average_precision_score`, `classification_report` as a dict, per-class F1 for each of the 7 taxonomy classes. Pillar 2: call the SHAP sanity checker from Phase 39 stub (returns placeholder until Phase 39). Pillar 3: call `LatencyProfiler` from Subphase 26.3 with 1000 warmup + 5000 timed runs. Return fully populated `ThreePillarMetrics` Pydantic model.
> **📦 Stack:** sklearn 1.5, numpy, pydantic v2
> **✅ Outcome:** `harness.evaluate(any_xaiguard_model, X_test, y_test)` returns a `ThreePillarMetrics` with all fields populated. No model-specific code in the harness.

#### Subphase 26.3 — Latency Profiler

> **🎭 Role:** Senior Performance Engineering Specialist
> **📍 Context:** P99 inference latency is the latency budget gate for Champion/Challenger promotion. It must be measured consistently across all models using the same methodology.
> **🔧 Task:** Implement `ml/src/evaluation/latency_profiler.py`. `LatencyProfiler(warmup_runs: int = 1000, measurement_runs: int = 5000, batch_size: int = 1, device: str = "cpu")`. The `profile(model: XAIGuardModel, X_sample: np.ndarray) -> LatencyProfile` method: runs warmup (discarded), runs measurement, records wall-clock time per prediction using `time.perf_counter_ns` (nanosecond precision), computes P50/P95/P99/max in milliseconds, computes throughput (events/sec). For PyTorch models, set `torch.no_grad()` and `model.eval()`. For CPU measurements, pin to a single CPU core using `os.sched_setaffinity` if available. Return `LatencyProfile` Pydantic model.
> **📦 Stack:** time (stdlib), numpy, torch, pydantic v2
> **✅ Outcome:** `profiler.profile(lr_model, X[0:1])` returns a `LatencyProfile` with P99 < 5ms for a simple logistic regression model. P99 measurements are stable across repeated calls (CV < 5%).

#### Subphase 26.4 — Serialisation Contract & Tests

> **🎭 Role:** Senior ML Platform Engineer
> **📍 Context:** Production model serving loads models from MLflow artifact storage. The serialisation contract must guarantee that a loaded model produces byte-identical predictions to the original.
> **🔧 Task:** Write `ml/tests/test_model_interface.py`. Test the interface contract for all six model families using test fixtures. For each model: (1) `model.predict(X)` before `fit` raises `NotFittedError`; (2) after `fit`, `predict` returns integer labels with shape `(n_samples,)`; (3) `predict_proba` returns float32 probabilities summing to 1.0 per row; (4) `save` + `load` produces a model whose `predict` output is byte-identical to the original; (5) `feature_names` returns the same list before and after serialisation; (6) `model_family` returns the correct StrEnum value. Use pytest parametrize over all six model families.
> **📦 Stack:** pytest, numpy, joblib
> **✅ Outcome:** All six model families pass the 6 interface contract tests. The parametrized test matrix is visible in CI output.

#### Subphase 26.5 — Optuna Study Configuration

> **🎭 Role:** Senior ML Research Engineer with Optuna expertise
> **📍 Context:** Each model family uses Optuna for hyperparameter search. A shared Optuna configuration ensures studies are reproducible, use the same pruner, and log correctly to MLflow.
> **🔧 Task:** Implement `ml/src/training/optuna_config.py`. `create_study(model_family: str, direction: str = "maximize", n_trials: int = 50, seed: int = 42) -> optuna.Study`. Configure: `TPESampler(seed=seed, multivariate=True)` for correlated hyperparameter spaces; `MedianPruner(n_startup_trials=10, n_warmup_steps=5)` to kill unpromising trials early; `MLflowCallback(tracking_uri, metric_name="val_f1_macro")` to log each trial as an MLflow child run. Return the configured study. Document the Optuna objective function pattern that all six training scripts follow.
> **📦 Stack:** optuna 3.6, optuna-integration[mlflow], mlflow 2.14
> **✅ Outcome:** `create_study("xgboost")` returns a configured study. Running 5 trials creates 5 child MLflow runs under the parent experiment. The best trial is promoted to the parent run.

---

## Phase 27 — Logistic Regression Baseline

**Context:** Logistic Regression sets the performance floor. Any model that does not significantly outperform it on all three pillars does not justify its additional complexity.


### 🎓 What You Will Learn in Phase 27
Logistic Regression is intentionally simple. Its purpose is to establish the **performance floor** — the baseline that all other models are measured against. If a complex model doesn't significantly outperform LR, it doesn't justify its additional complexity, cost, or latency.

### 📖 Concept: Why Logistic Regression as Baseline?
LR makes one strong assumption: the decision boundary between classes is linear in feature space. If your engineered features are good, LR should do reasonably well even with this constraint.

The performance gap between LR and XGBoost tells you: **how much of your accuracy comes from feature engineering vs model complexity?** If LR achieves 0.88 F1 and XGBoost achieves 0.96 F1, the 0.08 gap is the value of XGBoost's non-linear learning. If LR achieves 0.94, the gap is small and XGBoost's extra complexity is less justified.

This directly answers **RQ5** in your research: "Is there a measurable trade-off between prediction accuracy and model complexity?"

### ⚠️ Common Mistakes — LR Training
- **Not using `class_weight='balanced'`**: On CICIDS-2017, LR without class weights will predict BENIGN for everything. Always use balanced weights.
- **Convergence warnings**: If you see `ConvergenceWarning`, increase `max_iter`. With 2.8M rows, LR may need 2000+ iterations.
- **Reporting only overall F1**: The LR analysis MUST include per-class F1. Reviewers will ask: "What is LR's recall on the rarest attack class?"

#### Subphase 27.1 — LR Implementation

> **🎭 Role:** Senior ML Engineer
> **📍 Context:** Logistic Regression is the simplest possible model. It establishes the baseline that all other models are measured against.
> **🔧 Task:** Implement `ml/src/models/logistic_regression.py`. `LogisticRegressionModel(XAIGuardModel)`: wraps `sklearn.linear_model.LogisticRegression(multi_class="multinomial", solver="lbfgs", max_iter=1000, n_jobs=-1, class_weight="balanced")`. Load class weights from `ClassWeightCalculator` if `use_class_weights=True`. Implement all interface methods. For serialisation use `joblib.dump`. The `fit` method logs: convergence status, number of iterations, training time, and validation F1 to MLflow. The `predict_proba` output uses the fitted class label order exposed as `model.classes_`.
> **📦 Stack:** scikit-learn 1.5, joblib, mlflow, numpy
> **✅ Outcome:** `LogisticRegressionModel().fit(X_train, y_train, X_val, y_val)` completes on CICIDS-2017 in under 60 seconds. All interface contract tests pass.

#### Subphase 27.2 — LR Grid Search & Training

> **🎭 Role:** Senior ML Research Engineer
> **📍 Context:** Logistic Regression has few tunable hyperparameters. GridSearchCV is more appropriate than Optuna for this model given the small search space.
> **🔧 Task:** Write `ml/scripts/train_logistic_regression.py`. Run GridSearchCV over: `C` ∈ [0.001, 0.01, 0.1, 1.0, 10.0], `penalty` ∈ ["l1", "l2"] (l1 requires `solver="saga"`). Use 5-fold StratifiedKFold. Score on `f1_macro`. After the best params are found, retrain on the full training set. Run evaluation harness. Log all GridSearchCV results as a DataFrame artifact to MLflow. Register the trained model in MLflow Model Registry with the `REGISTERED` status.
> **📦 Stack:** scikit-learn, mlflow, pandas
> **✅ Outcome:** The script produces an MLflow run with CV results, best params, and all three-pillar metrics. The model is registered in MLflow.

#### Subphase 27.3 — LR Per-Attack Analysis

> **🎭 Role:** ML Research Scientist
> **📍 Context:** Overall F1 macro can mask poor recall on specific attack classes. Per-attack analysis identifies which classes Logistic Regression struggles with.
> **🔧 Task:** Create `ml/notebooks/experiments/01_lr_analysis.ipynb`. Load the best LR model from MLflow. Generate: confusion matrix heatmap, per-class F1 bar chart with colour coding (green ≥ 0.9, yellow 0.7–0.9, red < 0.7), ROC curves per class (one-vs-rest), calibration curve. Write a markdown section titled "LR Research Findings" identifying: which attack classes it fails on, the model's speed advantage, and whether class weights meaningfully improved minority class recall. Log the notebook as an MLflow artifact.
> **📦 Stack:** matplotlib, seaborn, sklearn, mlflow
> **✅ Outcome:** The notebook runs end-to-end. The per-class F1 chart is saved as a publishable figure.

---

## Phase 28 — Random Forest Model

**Context:** Random Forest provides strong non-linear performance and native feature importance. It is the classical ML champion before XGBoost and deep learning are compared.


### 🎓 What You Will Learn in Phase 28
Random Forest introduces ensemble learning: combining many weak learners (decision trees) into one strong learner. You will learn RandomizedSearchCV as an efficient alternative to grid search, and how to use Out-of-Bag (OOB) score as a free validation metric.

### 📖 Concept: Random Forest and Feature Importance
Random Forest trains N decision trees, each on a random subset of training samples and features. Prediction is by majority vote. Because each tree is different, the ensemble is more robust than any single tree.

**Gini Feature Importance:** For each feature, RF measures how much it reduces impurity (Gini index) across all trees. This is a fast, built-in alternative to SHAP — but it has known biases toward high-cardinality features and correlated features.

**Why this matters for your paper:** In Phase 28.3, you compare RF Gini importance vs SHAP importance. If they agree, great. If they disagree, that's an interesting finding suggesting the model uses features differently from what Gini importance implies.

#### Subphase 28.1 — RF Implementation

> **🎭 Role:** Senior ML Engineer
> **📍 Context:** Random Forest is implemented using the same XAIGuardModel interface as LR.
> **🔧 Task:** Implement `ml/src/models/random_forest.py`. `RandomForestModel(XAIGuardModel)` wrapping `sklearn.ensemble.RandomForestClassifier(n_jobs=-1, class_weight="balanced_subsample", random_state=42)`. Use joblib for serialisation. The `fit` method logs: `n_estimators`, `max_depth`, feature importances as a JSON artifact, training time, and OOB score if `oob_score=True`. After training, compute and log the top 20 features by Gini importance.
> **📦 Stack:** scikit-learn, joblib, mlflow
> **✅ Outcome:** All interface contract tests pass. Feature importances are logged and visible in the MLflow artifact viewer.

#### Subphase 28.2 — RF Randomized Search & Latency Profiling

> **🎭 Role:** Senior ML Research Engineer
> **📍 Context:** Random Forest has a large hyperparameter space. RandomizedSearchCV is more efficient than grid search here. Latency profiling is critical because large forests are slow at inference time.
> **🔧 Task:** Write `ml/scripts/train_random_forest.py`. Use `RandomizedSearchCV` with 30 iterations over: `n_estimators` ∈ [100, 200, 500, 1000], `max_depth` ∈ [None, 10, 20, 30], `min_samples_leaf` ∈ [1, 2, 4], `max_features` ∈ ["sqrt", "log2", 0.3]. After finding best params, retrain on the full training set. Run evaluation harness and latency profiler with batch_size=1 (single-event inference as in production). Log inference P99, the number of trees, and the model file size. Register in MLflow.
> **📦 Stack:** scikit-learn, mlflow, numpy
> **✅ Outcome:** The training script produces an MLflow run. Latency P99 is logged. The RF model is registered.

#### Subphase 28.3 — RF Analysis Notebook

> **🎭 Role:** ML Research Scientist
> **📍 Context:** Random Forest provides native feature importance, unlike LR, providing a first XAI comparison point before SHAP is computed in Phase 39.
> **🔧 Task:** Create `ml/notebooks/experiments/02_rf_analysis.ipynb`. Load the best RF from MLflow. Generate: per-class F1 comparison with LR (grouped bar chart); Gini importance vs SHAP importance correlation stub (placeholder for Phase 39); the memory footprint of the RF model file vs LR model file; a latency comparison table (LR P99 vs RF P99). Write "RF Research Findings" section identifying: accuracy gain over LR, the latency-accuracy trade-off, and which features the RF considers most important.
> **📦 Stack:** matplotlib, mlflow, pandas
> **✅ Outcome:** Notebook runs end-to-end. The LR vs RF comparison table is saved for the research paper.

---

## Phase 29 — XGBoost Champion Registration

**Context:** XGBoost is the expected Champion model — the best balance of accuracy, speed, and explainability for tabular network security data. It becomes the initial Champion after training.


### 🎓 What You Will Learn in Phase 29
XGBoost is your expected Champion model. You will learn: gradient boosting theory, Optuna-based hyperparameter search at scale (100 trials), SHAP sanity checking, and how to register a model as Champion in MLflow. This is the most complete training workflow in the project.

### 📄 Research Paper Connection
- Phase 29 → **Table 4, Row 3 (XGBoost)**: The full three-pillar evaluation
- Phase 29.3 SHAP sanity check → **§4.4**: "XGBoost SHAP values satisfy the additivity property..."
- Phase 29.4 Analysis Notebook → **Figure 7**: LR vs RF vs XGBoost F1 comparison, Optuna history
- Phase 29 answers **RQ1** (classical ML vs deep learning) from the classical side

### 📖 Concept: How XGBoost Works
XGBoost (Extreme Gradient Boosting) builds trees sequentially: each new tree tries to correct the errors made by all previous trees. This is gradient boosting — each tree is fitted on the gradient of the loss function with respect to current predictions.

Key advantages for security data:
1. **Handles class imbalance** via `sample_weight` array
2. **Early stopping**: if validation F1 hasn't improved for 20 rounds, training stops automatically — prevents overfitting
3. **Native SHAP support**: `shap.TreeExplainer(xgboost_model)` is the fastest and most accurate SHAP method
4. **Fast inference**: single tree traversal, very low P99 latency

### ⚠️ Common Mistakes — XGBoost Training
- **Not using early stopping**: XGBoost can overfit if trained for too many rounds. Always provide a validation set and `early_stopping_rounds`.
- **Forgetting to retrain on full training set**: After Optuna finds the best hyperparameters, retrain on ALL training data (train+val). Optuna runs only use val to find params.
- **Not saving the SHAP beeswarm plot immediately**: This is Figure 7 of your paper. Always log it to MLflow right after training.

#### Subphase 29.1 — XGBoost Implementation

> **🎭 Role:** Senior ML Engineer with XGBoost expertise
> **📍 Context:** XGBoost is the strong tabular baseline. It natively supports multi-class, sparse data, and sample weights.
> **🔧 Task:** Implement `ml/src/models/xgboost_model.py`. `XGBoostModel(XAIGuardModel)` wrapping `xgboost.XGBClassifier(tree_method="hist", device="cpu", eval_metric=["mlogloss", "merror"], enable_categorical=False, random_state=42)`. The `fit` method: applies class weights as `sample_weight` array, uses early stopping with validation set (patience=20 rounds), logs the learning curve (train_loss, val_loss per boosting round) as an MLflow metric per step, and logs the best iteration. The `save`/`load` uses `model.save_model(path)` / `model.load_model(path)` for XGBoost's native format.
> **📦 Stack:** xgboost 2.0.3, mlflow, numpy
> **✅ Outcome:** All interface contract tests pass. Early stopping fires correctly. The learning curve is visible in the MLflow metrics tab.

#### Subphase 29.2 — Optuna Hyperparameter Search

> **🎭 Role:** Senior ML Research Engineer
> **📍 Context:** XGBoost has many hyperparameters and Optuna's TPE sampler is the most effective search strategy for it.
> **🔧 Task:** Write `ml/scripts/train_xgboost.py`. Define the Optuna objective: suggest `n_estimators` ∈ [100, 2000], `max_depth` ∈ [3, 12], `learning_rate` log-uniform [0.001, 0.3], `subsample` [0.5, 1.0], `colsample_bytree` [0.5, 1.0], `reg_alpha` log-uniform [1e-8, 1.0], `reg_lambda` log-uniform [1e-8, 1.0]. Run 100 Optuna trials with MedianPruner. After the best trial, retrain on the full training set with the best params. Run evaluation harness and register in MLflow as `CHAMPION` status (the first Champion).
> **📦 Stack:** optuna 3.6, xgboost, mlflow
> **✅ Outcome:** 100 Optuna trials complete. Best params are logged. The XGBoost model is registered in MLflow Model Registry with the CHAMPION alias.

#### Subphase 29.3 — SHAP Sanity Check

> **🎭 Role:** ML Research Scientist
> **📍 Context:** XGBoost's SHAP values are computed natively by the XGBoost library. A sanity check now validates that SHAP values are sensible before the full SHAP analysis in Phase 39.
> **🔧 Task:** In the training script, after training completes: compute SHAP values for 100 test samples using `shap.TreeExplainer(model)`. Verify: SHAP values sum to the prediction log-odds for each sample (|sum(SHAP) + base_value - predict_log_odds| < 0.01 for all samples). Plot a SHAP beeswarm summary for the top 10 features and log as an MLflow artifact. Log the mean absolute SHAP value per feature as metrics.
> **📦 Stack:** shap 0.45, matplotlib, mlflow
> **✅ Outcome:** The SHAP additivity check passes for all 100 test samples. The beeswarm plot is visible as an MLflow artifact.

#### Subphase 29.4 — XGBoost Analysis Notebook

> **🎭 Role:** ML Research Scientist
> **📍 Context:** XGBoost is the Champion. Its analysis notebook is the most detailed and serves as the primary reference for the research paper.
> **🔧 Task:** Create `ml/notebooks/experiments/03_xgboost_analysis.ipynb`. Generate: per-class F1 comparison table for LR, RF, XGBoost; feature importance comparison (XGBoost Gain vs SHAP); Optuna optimisation history plot; learning curve (train vs val loss); calibration curve; latency distribution histogram (5000 single-event predictions); model file size comparison. Write "XGBoost Research Findings" with the answers to RQ1 (classical vs deep learning) and RQ6 (cost-efficiency) from the XGBoost perspective.
> **📦 Stack:** optuna, shap, matplotlib, mlflow
> **✅ Outcome:** Notebook runs end-to-end. The three-model comparison table is production-quality for the research paper.

---

## Phase 30 — LSTM Architecture

**Context:** LSTM is the first deep learning model. It processes event sequences to detect attack patterns that span multiple connections, a capability tabular models cannot match.


### 🎓 What You Will Learn in Phase 30
You will implement a Bidirectional LSTM from scratch using PyTorch Lightning. This is the first deep learning model in your benchmark. You will learn: LSTM cell mechanics, bidirectionality, gradient clipping, and mixed-precision training.

### 📄 Research Paper Connection
- Phase 30 → **§4.3 Architecture Description**: "Our BiLSTM processes 10-event sequences from each source IP, reading forward and backward to capture temporal context."
- Phase 30.3 Unit Tests → **Reproducibility statement**: "Architecture correctness is verified by 7 unit tests including gradient flow and serialisation parity."

### 📖 Concept: Why Bidirectional LSTM?
A standard LSTM processes a sequence left-to-right (past to present). A **Bidirectional** LSTM runs two LSTMs: one forward (past to present) and one backward (present to past). Their hidden states are concatenated.

**Why does backward context help?** Consider a 10-event window where events 1–8 are normal but events 9–10 are the beginning of an attack. A forward LSTM sets its hidden state to "normal" from events 1–8 and may under-weight events 9–10. A backward LSTM starts from event 10 (the attack start) and propagates that context back through the sequence.

**Limitation:** In production, you can't read the future. Bidirectionality only works because you're using a fixed-length window of **past** events — all 10 events are already available before predicting.

### 📖 Concept: Gradient Clipping
Deep RNNs like LSTMs are prone to "exploding gradients": during backpropagation, the gradient can grow exponentially through many time steps. Gradient clipping prevents this: if the gradient norm exceeds a threshold (usually 1.0), it is rescaled to have exactly that norm. This keeps training stable without preventing learning.

**In PyTorch:** `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)` — called before `optimizer.step()` each iteration.

### ⚠️ Common Mistakes — LSTM Architecture
- **Mixing events from different source IPs in one sequence**: The sequence builder must never put IP_A and IP_B events in the same window. The LSTM would learn meaningless cross-IP patterns.
- **Label assignment**: Assign the label of the LAST event in the window (not first, not majority). You're predicting whether the current event is malicious given its context.
- **Not using `model.eval()` during inference**: Dropout is active during training but must be disabled during evaluation. Always call `model.eval()` before any `predict` call.

#### Subphase 30.1 — BiLSTM Architecture

> **🎭 Role:** Senior Deep Learning Engineer
> **📍 Context:** A bidirectional LSTM reads the event sequence in both directions, capturing context from both past and future events in the window.
> **🔧 Task:** Implement `ml/src/models/lstm_model.py`. `BiLSTMModel(XAIGuardModel)` as a PyTorch Lightning Module. Architecture: input projection `Linear(n_features, hidden_dim)` + GELU; `nn.LSTM(hidden_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.3, bidirectional=True)`; classification head `Sequential(Linear(2*hidden_dim, hidden_dim), GELU, Dropout(0.3), Linear(hidden_dim, n_classes))`. Use `nn.CrossEntropyLoss(weight=class_weights)`. Training loop with gradient clipping (`nn.utils.clip_grad_norm_` at 1.0). `predict_proba` uses `F.softmax` on the output.
> **📦 Stack:** torch 2.3, pytorch-lightning, numpy
> **✅ Outcome:** Forward pass with input shape `(batch=32, seq=10, features=50)` produces output shape `(32, 7)`. Gradient clipping prevents NaN loss on adversarial inputs.

#### Subphase 30.2 — PyTorch Lightning Trainer Config

> **🎭 Role:** Senior Deep Learning Engineer
> **📍 Context:** PyTorch Lightning abstracts the training loop, checkpointing, and logging. The trainer configuration controls overfitting prevention and hardware utilisation.
> **🔧 Task:** Implement the Lightning Trainer configuration for LSTM training. Configure: `ModelCheckpoint(monitor="val_f1_macro", mode="max", save_top_k=1)` to save the best checkpoint by validation F1; `EarlyStopping(monitor="val_f1_macro", mode="max", patience=10)` to stop training when validation F1 stops improving for 10 epochs; `MLFlowLogger(experiment_name=experiment_name, run_name=run_name)` for automatic metric logging per epoch; precision `bf16-mixed` if CUDA is available, `32` otherwise. Maximum epochs: 100.
> **📦 Stack:** pytorch-lightning, mlflow
> **✅ Outcome:** The trainer saves the best checkpoint automatically. `val_f1_macro` is logged per epoch in MLflow. Early stopping fires after 10 epochs without improvement.

#### Subphase 30.3 — LSTM Unit Tests

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** Deep learning models have more failure modes than classical models. Unit tests catch architectural errors before expensive training.
> **🔧 Task:** Write `ml/tests/test_lstm.py`. Test: (1) forward pass produces correct output shape; (2) `predict_proba` output sums to 1.0 per sample (within 1e-5); (3) gradient flow: all parameter gradients are non-None after a backward pass; (4) `save` + `load` produces byte-identical `predict` output; (5) the model raises `NotFittedError` if `predict` is called before `fit`; (6) gradient clipping prevents gradient norm exceeding 1.0 during training; (7) the bidirectional flag doubles the hidden dimension correctly.
> **📦 Stack:** pytest, torch, numpy
> **✅ Outcome:** All 7 LSTM unit tests pass in under 30 seconds on CPU.

---

## Phase 31 — LSTM Training & Optimisation

**Context:** Train the LSTM with Optuna hyperparameter search and register the best model for comparison with XGBoost.


### 🎓 What You Will Learn in Phase 31
You will train the LSTM with Optuna search. GPU training introduces new considerations: memory management and mixed precision. You will also extract hidden states for the XAI analysis in Phase 41.

### 📖 Concept: Mixed Precision Training
By default, PyTorch uses 32-bit floating point (float32). Mixed precision training uses 16-bit floats (bfloat16) for most computations, keeping only critical operations in float32. Benefits: ~2× speedup, ~2× memory reduction on CUDA GPUs. PyTorch Lightning handles this with `precision='bf16-mixed'`. If training on CPU, use `precision=32`.

#### Subphase 31.1 — Optuna LSTM Search

> **🎭 Role:** Senior ML Research Engineer
> **📍 Context:** LSTM training is GPU-hours expensive. The Optuna search must be efficient: pruning unpromising trials early to save compute.
> **🔧 Task:** Write `ml/scripts/train_lstm.py`. Define the Optuna objective: suggest `hidden_dim` ∈ [64, 128, 256, 512], `num_layers` ∈ [1, 2, 3], `dropout` [0.1, 0.5], `learning_rate` log-uniform [1e-5, 1e-2], `batch_size` ∈ [128, 256, 512], `weight_decay` log-uniform [1e-6, 1e-3]. Use `MedianPruner`. Run 30 Optuna trials (reduced from XGBoost due to GPU cost). After the best trial, retrain for the full 100 epochs (or until early stopping). Log GPU memory usage per trial as an MLflow metric.
> **📦 Stack:** optuna, pytorch-lightning, mlflow, torch
> **✅ Outcome:** 30 trials complete. GPU memory is logged. Best LSTM model is registered in MLflow.

#### Subphase 31.2 — Attention Weight Extraction

> **🎭 Role:** Senior Deep Learning Engineer
> **📍 Context:** While LSTM does not have Transformer-style attention, its hidden state sequence can be used for a form of temporal attribution. Saving hidden states enables the Phase 41 attention-based XAI analysis.
> **🔧 Task:** Add a `predict_with_hidden_states(X_seq) -> tuple[np.ndarray, np.ndarray]` method to `BiLSTMModel`. This method returns both the predicted probabilities and the full LSTM hidden state sequence of shape `(n_samples, seq_len, 2*hidden_dim)`. These hidden states are used in Phase 41 to compute temporal attention scores using the method from "Attention is not Explanation" (Jain & Wallace, 2019). Log the average hidden state norm per timestep for the 100 test samples to MLflow.
> **📦 Stack:** torch, numpy, mlflow
> **✅ Outcome:** `model.predict_with_hidden_states(X_seq)` returns correct shapes. Hidden state norms are logged.

---

## Phase 32 — LSTM Evaluation & Research Findings

**Context:** Evaluate LSTM against XGBoost on all three pillars to answer RQ1 (classical vs deep learning) and RQ2 (LSTM vs Transformer).


### 🎓 What You Will Learn in Phase 32
This is the evaluation and research findings phase for LSTM. You will learn how to write structured research findings that map directly to your paper's Results section, and how to conduct a sequence length sensitivity analysis. You will also implement cross-dataset transfer evaluation — critical for answering RQ7.

### 📄 Research Paper Connection
- Subphase 32.1 → **Table 4, Row 4 (LSTM)** + **Figure 8**: LSTM vs XGBoost comparison
- Subphase 32.2 → **Appendix C**: Sequence length sensitivity
- **New Subphase 32.3** → **§4.3 Research Findings** writing template (direct text for paper)
- **New Subphase 32.4** → **Table 7**: Cross-dataset transfer results (RQ7)

#### Subphase 32.1 — Sequence vs Tabular Analysis

> **🎭 Role:** ML Research Scientist
> **📍 Context:** LSTM uses 10-event sequences. XGBoost uses single events. The sequence advantage is measured only if the sequence models are evaluated on the same events as the tabular models.
> **🔧 Task:** Create `ml/notebooks/experiments/04_lstm_analysis.ipynb`. Compare LSTM vs XGBoost on: (1) overall F1 macro; (2) per-class F1 (grouped bar chart); (3) latency (LSTM will be 3-10x slower — quantify the gap); (4) memory footprint. Specifically analyse: attacks that require sequence context to detect (BruteForce, PortScan) vs attacks detectable from single events (DDoS volume). Write "LSTM vs XGBoost Research Findings" answering RQ1 with specific numbers.
> **📦 Stack:** matplotlib, mlflow, pandas, numpy
> **✅ Outcome:** The notebook produces a publishable comparison table with LSTM vs XGBoost across all three pillars.

#### Subphase 32.2 — Sequence Length Sensitivity Analysis

> **🎭 Role:** ML Research Scientist
> **📍 Context:** The sequence window length (default 10) is an architectural choice. Testing multiple window lengths reveals the optimal setting and informs the Transformer architecture in Phase 33.
> **🔧 Task:** Add a sensitivity analysis section to the LSTM notebook. Train three additional LSTM variants with `window_size` = 5, 20, 30 (using the best hyperparameters from Phase 31). Compare F1 macro, BruteForce F1, PortScan F1, and latency P99 across all four window sizes. Plot as a 4-panel figure with window size on the x-axis. Determine the optimal window size. Document the recommendation in `ml/configs/sequence_config.yaml`.
> **📦 Stack:** pytorch-lightning, matplotlib, mlflow
> **✅ Outcome:** The sensitivity analysis determines the optimal window size. `ml/configs/sequence_config.yaml` is updated with the recommended value.

---

#### Subphase 32.3 — Research Findings Writing Template

> **🎭 Role:** ML Research Scientist and Technical Writer
> **📍 Context:** After completing model training and evaluation, you must document findings in a consistent format. This subphase produces the text that goes directly into your paper's §4.3 Results section. Every model (P27–P36) follows this template.
> **🔧 Task:** Add a final markdown cell to EVERY model analysis notebook (01_lr_analysis.ipynb through 04_lstm_analysis.ipynb) with the following structure:
>
> ```markdown
> ## Research Findings: [Model Name]
>
> ### RQ Answers from This Model
> - **RQ1 (Classical vs Deep Learning):** [How does this model compare to LR baseline? Specific F1 numbers.]
> - **RQ6 (Cost Efficiency):** [Latency P99 = X ms. Memory = Y MB. Cost assessment.]
>
> ### Key Numbers for Table 4
> | Metric | Value |
> |--------|-------|
> | F1 Macro | ? |
> | F1 (BruteForce) | ? |
> | F1 (PortScan) | ? |
> | F1 (DDoS) | ? |
> | Latency P99 (ms) | ? |
> | Memory (MB) | ? |
>
> ### Narrative (1 paragraph for the paper)
> "[Model] achieved F1 macro = X on CICIDS-2017, compared to the LR baseline of Y (+Z improvement).
> The model particularly excelled at [attack type] detection (F1=A) but struggled with [attack type] (F1=B).
> At P99 latency of C ms, it [meets/exceeds] the 100ms production budget.
> This [confirms/refutes] H1 from RQ1."
> ```
>
> Fill in every `?` and `[...]` with real numbers from MLflow. The narrative paragraph IS the actual text submitted to the paper.
> **📦 Stack:** Jupyter Markdown, MLflow
> **✅ Outcome:** Every model notebook has a completed "Research Findings" section with real numbers. The narrative paragraphs from all 6 model notebooks become the draft of §4.3 in your paper.

#### Subphase 32.4 — Cross-Dataset Transfer Evaluation

> **🎭 Role:** ML Research Scientist
> **📍 Context:** RQ7 asks: "Is per-attack-type F1 consistent across four datasets?" To answer this, evaluate models trained on CICIDS-2017 against UNSW-NB15 test data (zero-shot transfer). A model with high CICIDS-2017 F1 but low UNSW-NB15 transfer F1 has overfit to dataset-specific artefacts. Run this for all 3 classical models here; deep learning models complete their rows in P34 and P35.
> **🔧 Task:** Create `ml/notebooks/analysis/02_cross_dataset_transfer.ipynb`. For each trained classical model (LR, RF, XGBoost): (1) load the UNSW-NB15 test split (preprocessed with the CICIDS-2017 fitted pipeline using the BETH feature gap imputation strategy from Phase 13.3); (2) run `harness.evaluate(model, X_unswnb15_test, y_unswnb15_test)` using the mapped taxonomy labels; (3) record F1 macro, per-class F1 for overlapping taxonomy classes; (4) compute the **generalisation gap**: `F1_cicids − F1_unswnb15` per model.
>
> Build **Table 7** (for paper's §4.5):
> | Model | CICIDS-2017 F1 | UNSW-NB15 F1 | Generalisation Gap |
> |-------|----------------|--------------|-------------------|
> | LR | ? | ? | ? |
> | RF | ? | ? | ? |
> | XGBoost | ? | ? | ? |
>
> Write a "Cross-Dataset Transfer Findings" section: "Classical models showed a generalisation gap of X–Y F1 points when evaluated zero-shot on UNSW-NB15. [Model] showed the smallest gap (X), suggesting [interpretation]."
> **📦 Stack:** sklearn, mlflow, pandas, matplotlib
> **✅ Outcome:** Table 7 (cross-dataset transfer) is completed for classical models. The deep learning models complete their rows in P34.2 and P35.3. The generalisation gap analysis informs the paper's RQ7 answer.

### ✅ Learning Checkpoint — Phases 26–32
1. You train XGBoost with Optuna for 100 trials. After finding the best hyperparameters, should you retrain on (a) training set only, (b) training + validation set, or (c) training + validation + test set? Why?
2. Your LSTM achieves F1=0.94 on CICIDS-2017 but F1=0.71 on UNSW-NB15. What does this tell you about the LSTM's generalisation? What would you investigate first?
3. What is the difference between: (a) the model's validation F1 during Optuna search, and (b) the model's test F1 reported in Table 4? Why must they be computed on different data?

---


## Phase Map

| Phase | Title | Subphases |
|-------|-------|-----------|
| P26 | Common Model Interface Design | 5 |
| P27 | Logistic Regression Baseline | 3 |
| P28 | Random Forest Model | 3 |
| P29 | XGBoost Champion Registration | 4 |
| P30 | LSTM Architecture | 3 |
| P31 | LSTM Training & Optimisation | 2 |
| P32 | LSTM Evaluation & Research Findings | 2 |

**Previous ←** [03 — Feature Engineering](03-data-engineering.md) | **Next →** [05 — Transformer & XAI Evaluation](05-xai-and-model-evaluation.md)

