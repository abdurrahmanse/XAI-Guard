# 04 — Classical ML & Sequence Models

> **Phases 26–32** | Common model interface design, Logistic Regression baseline, Random Forest, XGBoost (initial Champion), LSTM architecture and training, and LSTM evaluation.
>
> **How to use:** Pick one subphase. Copy its **Prompt** into your AI code editor. Implement it. Move to the next subphase.

---

## Phase 26 — Common Model Interface Design

**Context:** All six models must share a single interface so that the inference service, evaluation harness, and XAI modules can treat every model identically. Design this interface before implementing any model.

#### Subphase 26.1 — Model Interface Specification
> **Prompt:** Write the formal specification for the common XAI-Guard model interface that all six models must implement. The interface defines five methods: fit for training on a feature matrix and label vector, predict for returning class predictions, predict_proba for returning class probability distributions, save for serialising the fitted model to a versioned artifact file, and load as a class method for deserialising from a file. Define the exact input and output types for each method and the contract that predict_proba must always return probabilities that sum to one per sample.

#### Subphase 26.2 — Base Model Class
> **Prompt:** Implement the abstract base model class for XAI-Guard that all six model implementations inherit from. The base class enforces the common interface by declaring abstract methods for fit, predict, predict_proba, save, and load. It also provides concrete implementations of shared utility methods: get_model_name returning the model's registry name, get_framework returning the ML framework used, and a validate_interface method that verifies the implementing class has correctly implemented all required methods before training begins.

#### Subphase 26.3 — Standard Metrics Computation Harness
> **Prompt:** Implement the standard metrics computation harness for XAI-Guard. Given any model implementing the common interface and a test set, the harness computes and returns the full metrics dictionary: accuracy, precision macro, recall macro, F1 macro, ROC-AUC macro OvR, PR-AUC macro, and F1 score per attack class. The harness handles the multi-class case correctly for all metrics. This is the single function called by all six model training scripts after training completes.

#### Subphase 26.4 — Inference Latency Profiler
> **Prompt:** Implement the inference latency profiler for XAI-Guard. The profiler measures the end-to-end prediction time for a given model and batch of samples. It runs five warm-up predictions to eliminate JIT compilation overhead, then times 1000 predictions in batches of 1, 16, 64, and 256 samples. For each batch size it reports P50, P95, and P99 latency in milliseconds. This profiler is called by all six model training scripts and results are logged to MLflow.

#### Subphase 26.5 — Model Serialization Contract
> **Prompt:** Define and implement the model serialization contract for XAI-Guard. Every serialised model artifact must include: the model weights or parameters file, the model configuration as a JSON file, the git commit SHA at training time, the DVC data tag used for training, the MLflow run ID, and the feature list the model was trained on. Implement a model artifact packager that creates a versioned ZIP file containing all of these components, and a corresponding unpacker used at inference time.

---

## Phase 27 — Logistic Regression Baseline

**Context:** Logistic Regression is the interpretability gold standard. Its coefficients are directly readable as feature weights without any XAI tool. Its performance sets the floor — any more complex model must beat it significantly to justify its added cost.

#### Subphase 27.1 — Model Implementation
> **Prompt:** Implement the Logistic Regression model for XAI-Guard following the common base interface from Phase 26. The model wraps scikit-learn's LogisticRegression with the saga solver which supports all regularisation penalties. Implement the get_feature_importance method that returns a dictionary mapping feature names to their coefficient values, representing the model's native interpretability without any XAI tool.

#### Subphase 27.2 — Hyperparameter Search Configuration
> **Prompt:** Configure the Logistic Regression hyperparameter search for XAI-Guard. The search space covers: regularisation strength C over five values from 0.001 to 10; regularisation penalty across L1, L2, and elastic net; and the elastic net L1 ratio for three values. Use exhaustive GridSearchCV with 5-fold StratifiedKFold cross-validation scoring on F1 macro. Log every trial's parameters and validation F1 to MLflow for full transparency.

#### Subphase 27.3 — Training & Metrics Logging
> **Prompt:** Implement the full training script for the XAI-Guard Logistic Regression model. The script runs the GridSearchCV, extracts the best estimator, evaluates it on the held-out test set using the standard metrics harness from Phase 26, logs all metrics and the best hyperparameters to MLflow, profiles inference latency with the latency profiler from Phase 26, and saves the model artifact using the serialization contract. The script is fully reproducible given the same data version and random seed.

#### Subphase 27.4 — Per-Attack-Type Breakdown
> **Prompt:** Extend the Logistic Regression evaluation in XAI-Guard to include per-attack-type F1 breakdown. Compute the F1 score separately for each attack class: DDoS, PortScan, BruteForce, Botnet, WebAttack, Infiltration, and Normal. Log these per-class metrics to MLflow under standardised key names. This breakdown is the primary data for the per-attack-type heatmap in the comparative analysis phase.

#### Subphase 27.5 — Model Registration
> **Prompt:** Register the best XAI-Guard Logistic Regression model in the MLflow Model Registry. Transition its status to Staging and log the registration metadata including the training dataset DVC tag, git commit SHA, and all evaluation metrics. This registered model will be compared against the other five models in the Champion selection phase.

#### Subphase 27.6 — Analysis Notebook
> **Prompt:** Create a Jupyter analysis notebook for the XAI-Guard Logistic Regression baseline. The notebook should include: the ROC curve, the precision-recall curve, the confusion matrix, a bar chart of the top 20 features by absolute coefficient value, and a table comparing training performance vs test performance to identify overfitting. The notebook is a research paper figure source and must be reproducible.

---

## Phase 28 — Random Forest Model

**Context:** Random Forest tests whether ensemble tree methods significantly outperform linear models. It is robust to outliers, handles non-linear interactions, and produces native feature importance via mean decrease in impurity.

#### Subphase 28.1 — Model Implementation
> **Prompt:** Implement the Random Forest model for XAI-Guard following the common base interface. The model wraps scikit-learn's RandomForestClassifier. Implement the get_feature_importance method returning MDI (mean decrease in impurity) feature importances. Add an additional get_oob_score method that returns the out-of-bag score when the model is trained with oob_score enabled, providing an unbiased performance estimate without a separate validation set.

#### Subphase 28.2 — Randomized Search Configuration
> **Prompt:** Configure the Random Forest hyperparameter search for XAI-Guard. Use RandomizedSearchCV with 50 iterations and 5-fold StratifiedKFold to search over: number of estimators in a range from 100 to 500, maximum depth across None and values from 10 to 30, minimum samples to split across values 2 5 and 10, and class weight across balanced and balanced_subsample. Log all 50 trials to MLflow.

#### Subphase 28.3 — Training, Metrics & Latency
> **Prompt:** Implement the full training script for the XAI-Guard Random Forest model. Run RandomizedSearchCV, evaluate the best estimator on the test set with the standard metrics harness, compute the OOB score, log all metrics and hyperparameters to MLflow, profile inference latency at four batch sizes, measure total training time in minutes, and save the model artifact. Compare the best F1 against the Logistic Regression baseline in the MLflow run description.

#### Subphase 28.4 — Per-Attack-Type Breakdown & Registration
> **Prompt:** Add per-attack-type F1 breakdown to the XAI-Guard Random Forest evaluation and register the best model in the MLflow Model Registry. Log the per-class F1 metrics using the same standardised keys as the Logistic Regression model to enable direct comparison in the comparative analysis notebook.

#### Subphase 28.5 — Analysis Notebook
> **Prompt:** Create a Jupyter analysis notebook for the XAI-Guard Random Forest model. Include: ROC curve overlaid with the Logistic Regression curve for visual comparison, feature importance bar chart showing the top 25 features by MDI score, confusion matrix, and a learning curve showing training F1 vs validation F1 as the number of estimators increases. The feature importance chart is a key research paper figure.

---

## Phase 29 — XGBoost Model & Champion Registration

**Context:** XGBoost consistently wins on tabular data across industry and research. It becomes the initial Champion model in the registry. All deep learning models must beat it to justify their computational cost, making this the most important baseline.

#### Subphase 29.1 — Model Implementation
> **Prompt:** Implement the XGBoost model for XAI-Guard following the common base interface. The model uses xgboost's native API with DMatrix for efficient data loading. Implement the get_feature_importance method returning gain-based feature importance scores, which are compatible with the SHAP TreeExplainer used in Phase 39. Add support for the scale_pos_weight parameter to handle class imbalance at the model level as an alternative to SMOTE.

#### Subphase 29.2 — Optuna Study Configuration
> **Prompt:** Configure the Optuna hyperparameter study for XAI-Guard XGBoost. Define the search space covering: number of estimators from 50 to 500, max depth from 3 to 10, learning rate on a log scale from 0.001 to 0.3, subsample from 0.6 to 1.0, column sample by tree from 0.6 to 1.0, L1 regularisation from 0 to 1, and L2 regularisation from 0.5 to 2. Use the TPE sampler with MedianPruner for efficient search. Configure the MLflow callback to log every trial automatically.

#### Subphase 29.3 — Optuna Training Loop
> **Prompt:** Implement the Optuna training loop for XAI-Guard XGBoost. The objective function creates a trial-specific XGBoost model, trains it with early stopping on a validation split, and returns the validation F1 macro as the optimisation target. Run 100 trials. After the study completes, retrieve the best trial's parameters, retrain the final model on the full training set with those parameters, and evaluate on the held-out test set.

#### Subphase 29.4 — SHAP Sanity Check
> **Prompt:** Add a SHAP sanity check to the XAI-Guard XGBoost training script. After the final model is trained, compute SHAP values for 100 test samples using TreeExplainer and verify that the top three features by mean absolute SHAP value make domain sense for cybersecurity threat detection. Log the top 10 SHAP feature importances to MLflow as a run artifact. This serves as an early XAI validation before the full XAI phase.

#### Subphase 29.5 — Champion Model Registration
> **Prompt:** Register the best XGBoost model as the initial Champion in the XAI-Guard model registry. Transition its status to Production in the MLflow Model Registry and record its status as champion in the PostgreSQL model_registry table. Update the champion model alias in MLflow so the inference service can load it by alias rather than by version number. Log the promotion event in the model promotion history table.

#### Subphase 29.6 — Optuna & Analysis Notebook
> **Prompt:** Create a Jupyter analysis notebook for the XAI-Guard XGBoost model and Optuna study. Include: the Optuna parallel coordinates plot showing hyperparameter relationships with trial objective values, the Optuna hyperparameter importance chart, the XGBoost training and validation loss curves, the confusion matrix, per-attack-type F1 bar chart, and the SHAP summary beeswarm plot for the 100 sanity-check samples.

---

## Phase 30 — LSTM Architecture

**Context:** LSTM tests whether sequential event modelling captures temporal attack patterns that tabular models miss — for example a port scan followed by a targeted exploit. This phase builds and validates the architecture before training.

#### Subphase 30.1 — BiLSTM Model Design
> **Prompt:** Design and implement the bidirectional LSTM model for XAI-Guard following the common base interface. The architecture processes input sequences of shape (batch, sequence_length, n_features) through a configurable-depth BiLSTM, takes the last hidden state from both directions, applies dropout, and passes through a linear classification head. The model must be configurable via a parameter dictionary covering hidden size, number of layers, dropout rate, and whether to use bidirectional processing.

#### Subphase 30.2 — PyTorch Lightning Trainer
> **Prompt:** Implement the PyTorch Lightning trainer module for XAI-Guard LSTM. Define training_step, validation_step, and test_step methods. Implement configure_optimizers using AdamW with a CosineAnnealingLR scheduler. Add early stopping on validation F1 macro with a patience of 5 epochs. Add model checkpointing that saves the epoch with the highest validation F1. Log training loss, validation loss, validation F1, and validation AUC to MLflow at every epoch.

#### Subphase 30.3 — Training Configuration
> **Prompt:** Define the training configuration for the XAI-Guard LSTM model. Specify the default hyperparameters: maximum 50 epochs with early stopping, batch size as a tunable parameter, gradient clipping at 1.0 to prevent exploding gradients in deep LSTM layers, a warm-up period of 5 epochs before the cosine learning rate decay begins, and the random seed for reproducibility. Store this configuration as a YAML file that is loaded by the training script and logged to MLflow.

#### Subphase 30.4 — LSTM Architecture Tests
> **Prompt:** Write unit tests for the XAI-Guard LSTM architecture. Verify: the forward pass produces output of the correct shape for various batch sizes and sequence lengths; the model correctly handles sequences of length 1; the model's parameter count matches the expected value for the default configuration; gradient flow is correct (no vanishing gradients on the first backward pass with random input); and the model can be saved and loaded with identical weights.

---

## Phase 31 — LSTM Training & Optimisation

**Context:** Tune the LSTM's hyperparameters using Optuna, run the full training, compute comprehensive metrics, and profile inference latency across batch sizes.

#### Subphase 31.1 — Optuna Hyperparameter Search
> **Prompt:** Configure and run the Optuna hyperparameter search for XAI-Guard LSTM. The search space covers: hidden size in a range from 64 to 256, number of LSTM layers from 1 to 3, dropout rate from 0.1 to 0.5, learning rate on a log scale, batch size across 64 128 and 256, and sequence length across 5 10 and 20. Run 50 trials. Use the MLflow callback to log every trial. Prune unpromising trials after 10 epochs using the MedianPruner.

#### Subphase 31.2 — Full Training Run
> **Prompt:** Implement the full LSTM training run for XAI-Guard. After the Optuna study identifies the best hyperparameters, retrain the LSTM on the full training set (not just the search validation split) using those hyperparameters with early stopping. Log the complete training curves (loss and F1 per epoch) to MLflow. Save the best checkpoint using the PyTorch Lightning ModelCheckpoint callback.

#### Subphase 31.3 — Metrics Computation & Registration
> **Prompt:** Evaluate the trained XAI-Guard LSTM on the held-out test set using the standard metrics harness from Phase 26. Compute per-attack-type F1 breakdown. Profile inference latency at batch sizes 1, 16, 64, and 256 on both CPU and GPU if available. Log all metrics and latency profiles to MLflow. Register the model in the MLflow Model Registry and record it as a candidate challenger in the PostgreSQL model registry table.

#### Subphase 31.4 — LSTM Analysis Notebook
> **Prompt:** Create a Jupyter analysis notebook for the XAI-Guard LSTM model. Include: training and validation loss curves across epochs, the Optuna trial history showing improvement over trials, confusion matrix on the test set, per-attack-type F1 bar chart compared with XGBoost, and a latency-vs-batch-size line chart for both CPU and GPU. This notebook is a key source for the comparative analysis in Phase 37.

---

## Phase 32 — LSTM Evaluation

**Context:** Interpret the LSTM results in the context of the research questions. Document whether and by how much LSTM outperforms XGBoost, and what temporal patterns it captures that tabular models miss.

#### Subphase 32.1 — Sequence vs Tabular Performance Analysis
> **Prompt:** Write the sequence-versus-tabular performance analysis for XAI-Guard LSTM. Compare LSTM's F1 macro, ROC-AUC, and per-attack-type F1 against XGBoost's results on the same test split. Identify specific attack types where LSTM outperforms XGBoost significantly and document the hypothesis for why sequence modelling helps for those specific attack patterns. Identify attack types where XGBoost wins and document why.

#### Subphase 32.2 — Sensitivity to Sequence Length
> **Prompt:** Run a sensitivity analysis on the XAI-Guard LSTM's sequence length hyperparameter. Train the LSTM with sequence lengths of 5, 10, 15, and 20 events while holding all other hyperparameters at their optimal values. Plot F1 macro and inference latency against sequence length. Document the optimal trade-off point and the rate at which performance saturates as sequence length increases.

#### Subphase 32.3 — Phase Findings Documentation
> **Prompt:** Write the LSTM research findings section for XAI-Guard. Document: the best LSTM architecture configuration, the performance delta versus XGBoost, the specific attack types where temporal modelling helps, the computational cost (training time, inference latency, memory) relative to XGBoost, and a preliminary assessment of whether the LSTM should be considered as the Challenger model or whether the Transformer architecture is needed. This feeds directly into the comparative analysis in Phase 37.

---

## Phase Map

| Phase | Title | Subphases |
|-------|-------|-----------|
| P26 | Common Model Interface Design | 5 |
| P27 | Logistic Regression Baseline | 6 |
| P28 | Random Forest Model | 5 |
| P29 | XGBoost Model & Champion Registration | 6 |
| P30 | LSTM Architecture | 4 |
| P31 | LSTM Training & Optimisation | 4 |
| P32 | LSTM Evaluation | 3 |

**Previous ←** [03 — Feature Engineering & Experiment Tracking](03-data-engineering.md) | **Next →** [05 — Transformer Models & Comparative Analysis](05-xai-and-model-evaluation.md)