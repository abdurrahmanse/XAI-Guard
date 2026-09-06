# 06 — LIME, XAI Evaluation & Backend Core

> **Phases 40–47** | LIME explainability, attention explainability, XAI stability analysis, human-centred evaluation, robustness testing, drift detection, modular monolith core layer, and authentication module.
>
> **How to use:** Pick one subphase. Copy its **Prompt** into your AI code editor. Implement it. Move to the next subphase.

---

## Phase 40 — LIME Explainability

**Context:** LIME is model-agnostic and provides local explanations by fitting a linear model around each prediction. It is slower than SHAP but works identically on all six models without requiring gradient access.

#### Subphase 40.1 — LIME Explainer Design
> **Prompt:** Design and implement the LIME explainer for XAI-Guard. Wrap lime.lime_tabular.LimeTabularExplainer with a clean interface matching the unified SHAP explainer design from Phase 39. The explainer must accept any model that implements the common interface predict_proba method, making it fully model-agnostic. Configure it with a background training sample for kernel density estimation and the feature names from the selected feature list.

#### Subphase 40.2 — Local LIME Computation
> **Prompt:** Implement the local LIME explanation computation for XAI-Guard. Run LIME explanations for the same 50 test samples used for SHAP local explanations to enable direct comparison. For each sample extract the top 5 contributing features with their coefficient values and direction. Store the results in the same structured format as SHAP explanations so the XAI panel in the dashboard can display either method interchangeably.

#### Subphase 40.3 — LIME Stability Testing
> **Prompt:** Implement LIME stability testing for XAI-Guard using the same methodology as SHAP stability testing from Phase 39. Run LIME 10 times on the same 100 test samples and compute the stability score per model. Document and compare LIME stability against SHAP stability. LIME is expected to be less stable due to random neighbourhood sampling — document the magnitude of this difference.

#### Subphase 40.4 — SHAP-LIME Agreement Scoring
> **Prompt:** Compute the SHAP-LIME explanation agreement score for XAI-Guard. For each of the 50 evaluation samples compute the Spearman rank correlation between the SHAP feature importance ranking and the LIME feature importance ranking for the same prediction. Average the correlation across all 50 samples per model to get a per-model agreement score. High agreement means both methods tell the same story to the analyst.

#### Subphase 40.5 — LIME Analysis Notebook
> **Prompt:** Create the LIME analysis Jupyter notebook for XAI-Guard. Include: LIME explanation bar charts for three representative samples (DDoS, BruteForce, Normal) shown side-by-side with the corresponding SHAP waterfall charts; LIME stability score comparison across all six models; the SHAP-LIME agreement score bar chart; and a timing comparison showing SHAP versus LIME explanation generation time per sample for each model.

---

## Phase 41 — Attention Explainability

**Context:** Attention weights are the Transformer's intrinsic explanation mechanism showing which time steps the model focused on during prediction. This provides a third XAI method exclusive to the two Transformer models.

#### Subphase 41.1 — Attention Weight Extraction
> **Prompt:** Implement the raw attention weight extraction interface for XAI-Guard using the method added to the Transformer in Phase 33. Extract attention weight tensors for a batch of sequence inputs and aggregate across attention heads by taking the mean to produce a single attention matrix per layer. Write a unit test confirming the output shape and that attention weights sum to one across the key dimension.

#### Subphase 41.2 — Attention Rollout Implementation
> **Prompt:** Implement the Attention Rollout algorithm for XAI-Guard following Abnar and Zuidema 2020. Attention Rollout multiplies attention matrices across all encoder layers with residual connection corrections to produce a single importance score per input time step. This produces more reliable attributions than raw last-layer attention. Write a unit test confirming the output sums to one and produces different values for different inputs.

#### Subphase 41.3 — SHAP-Attention Agreement Scoring
> **Prompt:** Compute the SHAP-Attention agreement score for XAI-Guard Transformer models. For each of the 50 evaluation samples compute the Spearman rank correlation between the SHAP GradientExplainer feature importance rankings and the Attention Rollout time-step importance scores mapped to feature positions. This measures whether the model's internal attention agrees with the theoretically grounded SHAP attribution.

#### Subphase 41.4 — Attention Visualisation Notebook
> **Prompt:** Create the attention explainability Jupyter notebook for XAI-Guard. Include: attention heatmaps for three representative samples showing weight distribution across sequence positions and encoder layers; Attention Rollout importance scores as bar charts; side-by-side comparison of raw attention versus Attention Rollout for one BruteForce sequence; and the SHAP-Attention agreement score for both Transformer variants.

---

## Phase 42 — XAI Stability & Cross-Method Agreement

**Context:** Synthesise all XAI evaluations into a unified assessment. An explanation is trustworthy only if it is both stable and consistent across different methods.

#### Subphase 42.1 — Unified Stability Comparison
> **Prompt:** Produce the unified XAI stability comparison for XAI-Guard. Compile the stability scores for SHAP and LIME across all six models into a single comparison table. Compute the average stability across methods per model. Document the threshold: a stability score above 0.90 is considered sufficient for analyst trust. Create a bar chart grouped by model showing SHAP and LIME stability side-by-side.

#### Subphase 42.2 — Cross-Method Agreement Matrix
> **Prompt:** Build the cross-method agreement matrix for XAI-Guard. For each model the matrix cell (method_A, method_B) contains the mean Spearman correlation between those two methods top-5 feature rankings across the 50 evaluation samples. Include SHAP vs LIME, SHAP vs Attention (Transformer only), and LIME vs Attention (Transformer only). High agreement across all pairs indicates robust explanations.

#### Subphase 42.3 — Explanation Latency Trade-Off Analysis
> **Prompt:** Produce the explanation latency trade-off analysis for XAI-Guard. Measure explanation generation time per model per XAI method. Compute the latency overhead ratio relative to prediction time. Create a scatter plot with explanation quality on the y-axis and explanation latency on the x-axis for all method-model combinations. This plot directly answers research question 5 about the performance-explanation trade-off.

---

## Phase 43 — Human-Centred XAI Evaluation

**Context:** An explanation is only valuable if a security analyst can act on it. This phase evaluates XAI outputs from the analyst perspective using defined utility metrics, directly answering research questions 4 and 5.

#### Subphase 43.1 — Analyst Utility Metric Definitions
> **Prompt:** Define the five analyst utility metrics for XAI-Guard. Actionability measures whether the explanation suggests a specific remediation action on a rubric of 1 to 5. Completeness measures what fraction of ground-truth causal features appear in the top 5 explanation features. Fidelity measures whether the explanation correctly identifies actual causal features using leave-one-out sensitivity. Consistency is the stability score from Phase 42. Conciseness is a binary flag indicating whether the top 5 features are sufficient to classify the attack. Document the measurement procedure for each metric.

#### Subphase 43.2 — Evaluation Dataset Construction
> **Prompt:** Build the XAI-Guard analyst evaluation dataset of 50 manually labelled threat scenarios. For each scenario document: the attack type, the feature values that make it a genuine example, the ground-truth causal features that actually caused the classification, the expected recommended analyst action, and which model explanations are expected to correctly identify the causal features. Distribute the 50 scenarios evenly across the five most common attack types.

#### Subphase 43.3 — Automated Scoring Implementation
> **Prompt:** Implement the automated XAI utility scorer for XAI-Guard. The scorer takes an explanation and a ground-truth scenario and computes all five analyst utility metrics. Actionability uses a keyword presence rubric. Completeness computes overlap between explanation top-5 features and ground-truth causal features. Fidelity uses leave-one-out prediction sensitivity. Implement the scorer for both SHAP and LIME explanation formats.

#### Subphase 43.4 — XAI Trade-Off Matrix
> **Prompt:** Construct the XAI Trade-Off Matrix for XAI-Guard. The matrix has rows for each model-method combination (six models times two methods plus two Transformer attention rows) and columns for each analyst utility metric plus explanation latency. Populate by running the automated scorer across all 50 evaluation scenarios. Save as a CSV artifact and as a formatted heatmap visualisation.

#### Subphase 43.5 — Analyst Evaluation Notebook
> **Prompt:** Create the human-centred XAI evaluation Jupyter notebook for XAI-Guard. Include: a radar chart showing all five utility metrics per model for SHAP explanations; a scatter plot of F1 macro versus composite XAI utility score for all six models visualising the prediction-explanation trade-off; and the XAI Trade-Off Matrix heatmap. Label the Pareto-optimal model-method combinations on the scatter plot.

#### Subphase 43.6 — XAI Evaluation Report
> **Prompt:** Write the XAI evaluation report for XAI-Guard that summarises findings for security analyst teams. Answer: which XAI method produces the most actionable explanations; which model-method combination is recommended per attack type; what the performance-explanation trade-off means in practice; and the recommended analyst workflow for using explanations in threat triage. Save this as a deliverable document.

---

## Phase 44 — Robustness Testing

**Context:** Production models face inputs different from training data. Models trained on CICIDS-2017 must handle UNSW-NB15 patterns, and attackers deliberately craft evasive inputs.

#### Subphase 44.1 — Cross-Dataset Evaluation
> **Prompt:** Implement cross-dataset robustness evaluation for XAI-Guard. Train each model on CICIDS-2017 and evaluate on UNSW-NB15 and NSL-KDD without fine-tuning. Compute the generalisation gap as the drop in F1 macro from in-distribution to out-of-distribution evaluation. Create a generalisation gap bar chart for all six models. A smaller gap indicates higher cross-dataset robustness and directly answers research question 7.

#### Subphase 44.2 — Attack-Type Holdout Evaluation
> **Prompt:** Implement attack-type holdout evaluation for XAI-Guard. For each of the five attack types train a model variant without any samples of that type then evaluate its ability to detect the held-out attack type. This measures zero-shot generalisation to unseen attack families. Run this for the XGBoost Champion and the best Transformer model. Document which attack types each model can detect without training examples.

#### Subphase 44.3 — Feature Perturbation Evaluation
> **Prompt:** Implement feature perturbation robustness evaluation for XAI-Guard. Inject Gaussian noise at three standard deviation levels into the numeric features of the test set and measure F1 macro degradation for each model at each level. Create a line chart showing F1 degradation versus noise level for all six models. A gradual rather than sharp degradation indicates a more robust model.

#### Subphase 44.4 — Adversarial Attack Evaluation
> **Prompt:** Implement adversarial attack evaluation for XAI-Guard LSTM and Transformer models using the Adversarial Robustness Toolbox. Apply Fast Gradient Sign Method at three epsilon values. Measure the accuracy degradation curve versus epsilon for both deep models. Document why classical models are inherently more robust to gradient-based attacks on tabular data due to their non-differentiable inference path.

#### Subphase 44.5 — Robustness Report
> **Prompt:** Write the XAI-Guard robustness report consolidating all robustness testing results. Document which model is most robust to cross-dataset shift, feature perturbation, and adversarial perturbation. Provide the recommended model for deployment environments where attack patterns evolve rapidly. This report directly answers research questions 7 and 8.

---

## Phase 45 — Drift Detection System

**Context:** The drift detector is a live component monitoring incoming event distributions and triggering retraining when significant shift is detected. It is a critical production safety mechanism.

#### Subphase 45.1 — MMD Drift Detector
> **Prompt:** Implement the Maximum Mean Discrepancy drift detector for XAI-Guard using alibi-detect. The detector is initialised with a reference dataset representing the expected feature distribution. It accepts a batch of new events and computes the MMD statistic between the reference and new batch. Configure a WARNING threshold at MMD above 0.05 and a CRITICAL threshold at MMD above 0.10. Return a structured drift report including the score, detection status, and threshold level.

#### Subphase 45.2 — Drift Policy Implementation
> **Prompt:** Implement the drift response policy for XAI-Guard. When a WARNING drift report is generated the policy logs it to the drift_reports database table and sends a monitoring alert. When CRITICAL drift is detected the policy additionally triggers the Challenger evaluation Celery task immediately. If the Challenger wins auto-promotion is applied. Document this policy as a state machine with clear transitions.

#### Subphase 45.3 — Temporal Drift Simulation
> **Prompt:** Implement the temporal drift simulation for XAI-Guard. Split CICIDS-2017 by capture date: train on days 1 through 3, evaluate on days 4 and 5. Compute F1 macro for all six models at each capture day to produce temporal performance degradation curves. Plot F1 versus capture day for all models. This simulation directly answers research question 8 about drift robustness.

#### Subphase 45.4 — Reference Distribution Update
> **Prompt:** Implement the reference distribution update mechanism for the XAI-Guard drift detector. After a successful Champion model promotion the drift detector must update its reference distribution to reflect the new expected input distribution. Implement this as a Celery task that recomputes reference statistics from the most recent processed events and logs the update metadata to the drift_reports table.

#### Subphase 45.5 — Drift Detection Notebook
> **Prompt:** Create the drift detection Jupyter notebook for XAI-Guard. Include: MMD drift score over the simulated temporal scenario; a demonstration of the detector firing at the configured threshold; F1 degradation curves across capture days for all six models; and a feature-level drift analysis showing which features drift most over time. These figures appear in the research paper robustness section.

---

## Phase 46 — Modular Monolith Core Layer

**Context:** The core layer is the shared infrastructure foundation of the FastAPI modular monolith. All eight domain modules depend on it. It must be built before any module implementation.

#### Subphase 46.1 — Application Configuration
> **Prompt:** Implement the XAI-Guard application configuration system for the modular monolith core layer. Use Pydantic Settings to load all configuration from environment variables with type validation. Group into sections: database, Redis, MinIO artifact storage, MLflow, JWT security, rate limiting, and CORS settings. The configuration object is a singleton loaded at startup and injected as a FastAPI dependency where needed.

#### Subphase 46.2 — Async Database Session Factory
> **Prompt:** Implement the async database session factory for the XAI-Guard modular monolith core layer. Create the SQLAlchemy async engine from configuration, the async session factory, and the FastAPI dependency function that provides a session per request with automatic commit on success and rollback on exception. All eight domain modules use this single shared session dependency.

#### Subphase 46.3 — Redis Client Setup
> **Prompt:** Implement the Redis client setup for the XAI-Guard modular monolith core layer. Create an async Redis connection pool from the Redis URL configuration. Provide a FastAPI dependency returning an async Redis client from the pool. Implement three utility functions used across modules: cache_get with automatic JSON deserialisation, cache_set with TTL, and publish for Redis pub/sub channels used by the WebSocket alert broadcasting system.

#### Subphase 46.4 — Structured Logging Configuration
> **Prompt:** Configure structured logging for the XAI-Guard modular monolith using structlog. Set up JSON output for production and human-readable coloured output for development. Configure standard fields on every log line: service name, environment, request ID, user ID when authenticated, and timestamp. Add a FastAPI middleware that generates a unique request ID per request and injects it into the logging context.

#### Subphase 46.5 — Base Exception Classes
> **Prompt:** Define the base exception hierarchy for the XAI-Guard modular monolith core layer. Create a base application exception with status code, error code, and detail message. Extend into: NotFoundError (404), ValidationError (422), AuthenticationError (401), AuthorisationError (403), and ConflictError (409). Register FastAPI exception handlers that convert these to RFC 7807 Problem Details JSON responses.

#### Subphase 46.6 — Prometheus Metrics Registry
> **Prompt:** Set up the Prometheus metrics registry for the XAI-Guard modular monolith. Register all custom metrics: prediction counter labelled by model attack type and severity; prediction latency histogram with defined buckets; confidence score histogram; drift score gauge labelled by model; champion model info gauge; Celery queue depth gauge; and active alerts gauge. Expose all metrics at the /metrics endpoint. Domain modules increment their relevant metrics through this shared registry.

#### Subphase 46.7 — Application Middleware Stack
> **Prompt:** Implement the FastAPI middleware stack for the XAI-Guard modular monolith. Apply middleware in order: CORS middleware with explicit allowed origins, HTTPS redirect for production, request timing middleware logging total duration, request ID injection, and Prometheus instrumentation. Register all middleware in the FastAPI application factory function.

---

## Phase 47 — Auth Module

**Context:** The auth module owns all identity and access concerns for the XAI-Guard modular monolith. It is a self-contained module with its own router and service layer. No other module implements authentication logic.

#### Subphase 47.1 — User Model & Password Hashing
> **Prompt:** Implement the user data model and password hashing for the XAI-Guard auth module. Define the users table with username, hashed password, role (analyst or admin), active status, and timestamps. Use passlib with bcrypt for password hashing. Implement the user service with methods for creating users, verifying credentials, and fetching by username. The auth module owns this service exclusively — no other module accesses the users table directly.

#### Subphase 47.2 — JWT Token Generation
> **Prompt:** Implement JWT access and refresh token generation for the XAI-Guard auth module. Access tokens expire in 15 minutes and contain user ID, username, and role as claims. Refresh tokens expire in 7 days and are stored in Redis keyed by user ID. Use python-jose with HS256 algorithm. The signing secret is loaded from the configuration system established in Phase 46.

#### Subphase 47.3 — Token Validation Dependency
> **Prompt:** Implement the JWT token validation FastAPI dependency for the XAI-Guard auth module. The dependency extracts the Bearer token from the Authorization header, verifies signature and expiry using python-jose, and returns the authenticated user. If invalid or expired raise an AuthenticationError that the exception handler converts to a 401 response. This dependency is used by all protected endpoints across all eight modules.

#### Subphase 47.4 — Login & Refresh Endpoints
> **Prompt:** Implement the login and token refresh endpoints for the XAI-Guard auth module. The POST login endpoint validates credentials, creates access and refresh tokens, stores the refresh token in Redis, and returns both. The POST refresh endpoint validates the refresh token from Redis, issues a new access token, and rotates the refresh token. Both endpoints log authentication events using the structured logging configured in Phase 46.

#### Subphase 47.5 — RBAC Dependency
> **Prompt:** Implement the role-based access control dependency for the XAI-Guard auth module. Create a require_role factory that accepts allowed roles and returns a FastAPI dependency chaining on the token validation dependency. Raise AuthorisationError if the authenticated user role is not in the allowed list. Use this to protect the model promotion endpoint and rollback endpoint as admin-only operations.

#### Subphase 47.6 — Auth Module Tests
> **Prompt:** Write comprehensive tests for the XAI-Guard auth module. Test the complete flow: create a user, log in and receive tokens, call a protected endpoint with the access token, use an expired token and receive 401, use an analyst token on an admin endpoint and receive 403, refresh the access token, and verify refresh token is invalidated after use. Use an in-memory test database so tests do not require a running PostgreSQL instance.

---

## Phase Map

| Phase | Title | Subphases |
|-------|-------|-----------|
| P40 | LIME Explainability | 5 |
| P41 | Attention Explainability | 4 |
| P42 | XAI Stability & Cross-Method Agreement | 3 |
| P43 | Human-Centred XAI Evaluation | 6 |
| P44 | Robustness Testing | 5 |
| P45 | Drift Detection System | 5 |
| P46 | Modular Monolith Core Layer | 7 |
| P47 | Auth Module | 6 |

**Previous ←** [05 — Transformer Models, Comparative Analysis & XAI](05-xai-and-model-evaluation.md) | **Next →** [07 — Backend Domain Modules & Dashboard](07-mlops-security-testing-and-performance.md)
