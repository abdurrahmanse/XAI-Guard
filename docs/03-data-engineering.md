# 03 — Feature Engineering & Experiment Tracking

> **Phases 18–25** | Network, temporal, and behavioral feature engineering; threat intelligence stubs; feature selection; sequence construction for deep learning; DVC pipeline; and MLflow tracking.
>
> **Prompt Engineering Format:** Each subphase includes Role, Context, Task, Stack, and Outcome.

---

## Phase 18 — Network Feature Engineering

**Context:** Raw network flow statistics alone are insufficient for high-precision IDS. Domain-specific engineered features provide security-relevant signal that models can detect and that SHAP can explain to analysts.

#### Subphase 18.1 — Bytes-Per-Packet & Packet Rate Features

> **🎭 Role:** Senior Network Security Data Scientist
> **📍 Context:** The preprocessing pipeline from Phase 16 produces a clean numeric feature matrix. Domain features are computed from this clean matrix and appended as additional columns. All features must be computable at inference time in the production API from a single SecurityEvent.
> **🔧 Task:** Implement `ml/src/features/network_features.py`. `bytes_per_packet(total_bytes, packet_count)`: total_bytes / packet_count; handle zero-packet division by returning 0.0; this is a strong DDoS amplification signal. `packet_rate(packet_count, duration_ms)`: packets / (duration_ms / 1000); handle zero-duration by returning 0.0. `bytes_rate(total_bytes, duration_ms)`: similar. For each feature, write a docstring explaining its security interpretation and which attack types it is most relevant for. Register all features in a `NETWORK_FEATURES: list[FeatureSpec]` registry using a `FeatureSpec` dataclass.
> **📦 Stack:** numpy, pandas, pytest
> **✅ Outcome:** All three features produce correct values on unit test inputs. Zero-division edge cases return 0.0 without warnings. The `FeatureSpec` registry enables automatic documentation generation.

#### Subphase 18.2 — Port Entropy Feature

> **🎭 Role:** Senior Network Security Data Scientist
> **📍 Context:** Port scanning attacks generate connections to many different destination ports from the same source IP. Shannon entropy of the destination port distribution over a rolling window quantifies this scanning behaviour.
> **🔧 Task:** Implement `port_entropy(source_ip_events: pd.DataFrame, window_size: int = 100)` in `network_features.py`. Sort events by timestamp, group by source IP, compute Shannon entropy of destination port distribution over the last `window_size` events per IP. Handle the cold-start case (fewer than `window_size` events: use all available). Scale: entropy=0 means single destination port (legitimate), entropy=log2(65535) ≈ 16 means perfectly uniform port distribution (extreme scanning). Add a rolling window implementation using pandas `.rolling(window=window_size).apply()`. Write unit tests with a simulated port scan sequence and a legitimate single-service sequence.
> **📦 Stack:** numpy, pandas, scipy, pytest
> **✅ Outcome:** A simulated port scan of 100 unique ports produces entropy > 5.0. A single-service client produces entropy = 0.0. The rolling window boundary is tested.

#### Subphase 18.3 — TCP Flag Ratio & Connection Duration Z-Score

> **🎭 Role:** Senior Network Security Data Scientist
> **📍 Context:** SYN flood attacks send many SYN packets without completing the TCP handshake. Anomalous connection duration relative to an IP's historical baseline indicates automated attack behaviour.
> **🔧 Task:** Implement two more features. `syn_ratio(source_ip_events: pd.DataFrame, window: int = 100)`: compute ratio of SYN-flagged packets to total packets for each source IP in the rolling window. SYN ratio > 0.8 is a SYN flood indicator. `duration_zscore(connection_duration_ms: float, source_ip_history: pd.Series)`: compute z-score of current connection duration relative to the source IP's historical connections. Cold-start (fewer than 5 historical connections): return 0.0. Handle zero standard deviation by returning 0.0. Write comprehensive unit tests.
> **📦 Stack:** numpy, pandas, pytest
> **✅ Outcome:** All features pass unit tests including edge cases. The `NETWORK_FEATURES` registry now contains 5 features total.

#### Subphase 18.4 — Network Feature Integration Tests

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** Network features must be valid on real data, not just synthetic unit test inputs. CICIDS-2017 contains known edge cases.
> **🔧 Task:** Write `ml/tests/test_network_features.py` applying all 5 network features to a 10,000-row sample of real CICIDS-2017 data. Verify: no NaN values in any feature output; all features produce float32 dtype; all values are in domain-valid ranges (entropy [0, 16], ratios [0, 1], z-score unconstrained but typically [-5, 5]); features for known DDoS events show elevated packet_rate and syn_ratio compared to BENIGN events. Run this test in CI.
> **📦 Stack:** pytest, pandas, numpy
> **✅ Outcome:** The integration test passes on real CICIDS-2017 data. DDoS events show statistically higher engineered feature values than BENIGN events.

---

## Phase 19 — Temporal Feature Engineering

**Context:** Many attack patterns are invisible in individual connection features but obvious in the sequence of events over time. Temporal features expose these patterns to all six models.

#### Subphase 19.1 — Rolling Event Rate Features

> **🎭 Role:** Senior ML Feature Engineer with temporal data expertise
> **📍 Context:** Network features from Phase 18 are computed from single events. Temporal features require time-ordered event sequences grouped by source IP. The feature must be computable in production with only the event history available in the Redis feature cache.
> **🔧 Task:** Implement `ml/src/features/temporal_features.py`. `events_per_minute(source_ip_history: pd.DataFrame, window_seconds: int = 60)`: count events from the same source IP in the past `window_seconds`. `failed_auth_rate(source_ip_history: pd.DataFrame, window_seconds: int = 300)`: count events with `service` matching auth services (SSH, FTP, HTTP-AUTH) and `connection_state` indicating failure. `session_gap_seconds(current_event_timestamp, last_event_timestamp)`: time elapsed since the previous connection from the same source IP; handle first-connection cold-start by returning -1. For each feature, document the attack types it primarily detects.
> **📦 Stack:** pandas, numpy, pytest
> **✅ Outcome:** `events_per_minute` correctly counts only events within the time window. `session_gap_seconds` returns -1 for first connections.

#### Subphase 19.2 — Circular Time Encoding & Temporal Tests

> **🎭 Role:** Senior ML Feature Engineer
> **📍 Context:** Hour-of-day is an important signal (attacks peak at night or on weekends) but is a circular feature — hour 23 and hour 0 are adjacent. Linear encoding destroys this adjacency.
> **🔧 Task:** Implement `time_of_day_sin_cos(timestamp: datetime)` returning two features: `sin(2π × hour/24)` and `cos(2π × hour/24)`. Similarly implement `day_of_week_sin_cos`. Register all temporal features in `TEMPORAL_FEATURES` registry. Write tests confirming: hour 0 and hour 24 produce identical values; hour 12 produces sin=0, cos=-1; the features are all float32. Then write an integration test applying all temporal features to CICIDS-2017 data and verifying no NaN values.
> **📦 Stack:** numpy, pandas, pytest, datetime (stdlib)
> **✅ Outcome:** The circular encoding test passes. Hour 23 and hour 0 have Euclidean distance < 0.3 in the encoded space.

---

## Phase 20 — Behavioral Feature Engineering

**Context:** Behavioral features characterise how a source IP behaves across many connections, revealing patterns like port scanning and lateral movement that are invisible in per-connection analysis.

#### Subphase 20.1 — Unique Destination Features

> **🎭 Role:** Senior Network Security Data Scientist
> **📍 Context:** Port scanning involves a single source IP targeting many destination ports or IPs. Counting unique destinations in a rolling window directly measures scanning breadth.
> **🔧 Task:** Implement `ml/src/features/behavioral_features.py`. `unique_dst_ports(source_ip_history, window_seconds=60)`: count unique destination ports in the window. `unique_dst_ips(source_ip_history, window_seconds=60)`: count unique destination IPs. `protocol_switch_rate(source_ip_history, window=50)`: fraction of consecutive connection pairs where protocol changes. Register all in `BEHAVIORAL_FEATURES`. Write unit tests with a simulated port scan sequence (100 unique ports in 30 seconds) and a legitimate client (always port 443).
> **📦 Stack:** pandas, numpy, pytest
> **✅ Outcome:** Port scan simulation produces `unique_dst_ports` > 50. Legitimate client produces `unique_dst_ports` = 1.

#### Subphase 20.2 — Source IP Request Volume Percentile

> **🎭 Role:** Senior ML Feature Engineer
> **📍 Context:** In any time window, a small fraction of source IPs generate a disproportionate share of traffic (Pareto principle). Source IPs in the top 1% by request volume are high-suspicion candidates.
> **🔧 Task:** Implement `request_volume_percentile(source_ip_events_count: int, all_ips_counts: np.ndarray)` that computes the percentile rank of a source IP's event count relative to all active IPs in the time window using `scipy.stats.percentileofscore`. Write tests confirming the top 1% threshold (percentile > 99) correctly identifies the highest-volume IP in a 100-IP simulation. Add an integration test on CICIDS-2017 data.
> **📦 Stack:** numpy, scipy, pytest
> **✅ Outcome:** The percentile computation matches `numpy.percentile` reference values. The integration test shows DDoS source IPs have higher percentile ranks than BENIGN.

---

## Phase 21 — Threat Intelligence Feature Stubs

**Context:** Threat intelligence enrichment will be live in Phase 53. Create type-safe stubs now so the feature pipeline is complete and model training can proceed with the correct feature schema.

#### Subphase 21.1 — Threat Intel Stub Implementation

> **🎭 Role:** Senior Backend + ML Integration Engineer
> **📍 Context:** The unified feature schema includes two threat intelligence features: `is_known_malicious_ip` and `is_tor_exit_node`. Both will be live API calls in Phase 53. Stubs return 0.0 with the exact same signature and return type as the live implementation.
> **🔧 Task:** Create `ml/src/features/threat_intel_stubs.py`. Implement `async def is_known_malicious_ip(ip: str) -> float` returning 0.0 with a docstring: `# STUB: Phase 53 replaces with AbuseIPDB live lookup. Returns confidence score 0.0-1.0.` Implement `async def is_tor_exit_node(ip: str) -> bool` returning False. Add `THREAT_INTEL_FEATURES: list[FeatureSpec]` registry entry for both. Write tests that verify the stubs return the correct types and do not raise exceptions for any valid IP address including IPv4, IPv6, and loopback addresses.
> **📦 Stack:** asyncio, pytest-asyncio, ipaddress (stdlib)
> **✅ Outcome:** The stubs are importable and pass tests. The code comment is a clear reminder for Phase 53.

---

## Phase 22 — Feature Selection & Validation

**Context:** After engineering, the feature set may exceed 100 features. Feature selection removes redundant and non-informative features, reducing overfitting risk and improving SHAP explanation conciseness.

#### Subphase 22.1 — Three-Stage Feature Selection Pipeline

> **🎭 Role:** Senior ML Feature Engineer and Research Scientist
> **📍 Context:** Feature selection runs as the `select` DVC stage. Three stages applied in sequence: variance filtering, mutual information ranking, and correlation redundancy removal. Each stage is independently configurable from YAML.
> **🔧 Task:** Implement `ml/src/features/feature_selection.py` with three sklearn-compatible transformers: `VarianceThresholdSelector(threshold: float = 0.01)` wrapping sklearn's `VarianceThreshold`; `MutualInformationSelector(n_features: int = 50)` using `sklearn.feature_selection.SelectKBest` with `mutual_info_classif`; `CorrelationRedundancyFilter(threshold: float = 0.95)` that computes Pearson correlation matrix, identifies clusters of correlated features, and retains the one with the highest MI score from each cluster. Chain them with `Pipeline`. Log selected feature names, removed features per stage, and final feature count to MLflow.
> **📦 Stack:** scikit-learn 1.5, numpy, pandas, mlflow
> **✅ Outcome:** `FeatureSelector().fit_transform(X_train, y_train)` reduces features to the configured target. `selector.selected_features_` attribute lists the final feature names.

#### Subphase 22.2 — Selected Feature Documentation

> **🎭 Role:** ML Research Lead
> **📍 Context:** The final selected feature list is a key research artefact. It must be versioned, documented, and referenced by all six model training scripts.
> **🔧 Task:** After running feature selection on CICIDS-2017, produce `ml/configs/selected_features.yaml` containing: `feature_names: list[str]`, `feature_count: int`, `selection_date: str`, `dataset_version: str` (DVC tag), `stages_applied: list[str]`, `removed_by_variance: list[str]`, `removed_by_mi: list[str]`, `removed_by_correlation: list[str]`. This file is committed to git and loaded by every model training script. Changing this file constitutes a new experiment version.
> **📦 Stack:** PyYAML, mlflow
> **✅ Outcome:** `ml/configs/selected_features.yaml` is committed. All six model training scripts load feature names from this file exclusively.

---

## Phase 23 — Sequence Data Construction

**Context:** LSTM and Transformer models require sequential input. The sequence builder converts time-sorted tabular events into fixed-length windows with proper handling of source IP boundaries.

#### Subphase 23.1 — Sequence Builder Implementation

> **🎭 Role:** Senior ML Engineer with deep learning data pipeline expertise
> **📍 Context:** Tabular preprocessing from Phase 16 produces a 2D feature matrix. Deep learning models need a 3D array of shape (n_sequences, window_length, n_features). The builder must never mix events from different source IPs into the same window.
> **🔧 Task:** Implement `ml/src/features/sequence_builder.py`. `SequenceBuilder(window_size: int = 10, stride: int = 1, pad_value: float = 0.0)` class. `build(X: np.ndarray, y: np.ndarray, source_ips: np.ndarray, timestamps: np.ndarray) -> tuple[np.ndarray, np.ndarray]`: sort by source IP then timestamp, apply sliding window per source IP group, handle short histories with zero-padding (pad at the start), assign the label of the last event in each window. Returns arrays of shape `(n_sequences, window_size, n_features)` and `(n_sequences,)`. Include a `verify_no_ip_mixing` flag that adds an assertion.
> **📦 Stack:** numpy, pytest
> **✅ Outcome:** The output shape is correct for all valid inputs. The IP-mixing assertion never fires on real data. Zero-padding is at the start (not end) of the sequence.

#### Subphase 23.2 — PyTorch Datasets & DataLoaders

> **🎭 Role:** Senior ML Engineer with PyTorch expertise
> **📍 Context:** The sequence builder produces NumPy arrays. PyTorch training requires Dataset and DataLoader classes with proper dtype handling.
> **🔧 Task:** Implement `ml/src/data/pytorch_datasets.py`. `TabularDataset(X: np.ndarray, y: np.ndarray)`: returns float32 features and long labels. `SequenceDataset(X_seq: np.ndarray, y: np.ndarray)`: returns float32 3D tensor and long labels. `create_dataloaders(train_X, train_y, val_X, val_y, test_X, test_y, batch_size, num_workers, seed) -> tuple[DataLoader, DataLoader, DataLoader]`: creates reproducible DataLoaders with `worker_init_fn` for seed propagation. Implement `collate_fn` with proper float32 casting. Write unit tests for tensor shapes, dtypes, and DataLoader batch sizes.
> **📦 Stack:** torch 2.3, numpy, pytest
> **✅ Outcome:** `next(iter(train_loader))` returns `(features_tensor.float(), labels_tensor.long())` with the correct batch shape.

#### Subphase 23.3 — Sinusoidal Positional Encoding

> **🎭 Role:** Senior Deep Learning Engineer
> **📍 Context:** The Transformer Encoder requires positional encoding to distinguish event ordering. The sinusoidal encoding is deterministic (no learned parameters) and generalises to sequence lengths not seen during training.
> **🔧 Task:** Implement `SinusoidalPositionalEncoding(d_model: int, max_len: int = 5000, dropout: float = 0.1)` as a PyTorch Module in `ml/src/models/transformer/positional_encoding.py`. Compute the standard sinusoidal formula: `PE(pos, 2i) = sin(pos/10000^(2i/d_model))`, `PE(pos, 2i+1) = cos(pos/10000^(2i/d_model))`. Register the encoding as a buffer (not a parameter) so it is included in `state_dict` but not updated by the optimiser. Write unit tests: different positions produce different vectors; position 0 always produces a zero vector (after dropout disabled); the module handles d_model=64, 128, 256.
> **📦 Stack:** torch 2.3, numpy, pytest
> **✅ Outcome:** The positional encoding unit tests pass. The module is included in `torch.save` without error.

---

## Phase 24 — DVC Pipeline Execution & Validation

**Context:** The DVC pipeline defined in Phase 9 must now be fully executed, validated for reproducibility, and tagged as the baseline data version.

#### Subphase 24.1 — Full Pipeline Execution

> **🎭 Role:** MLOps Engineer
> **📍 Context:** All pipeline stages (download, clean, encode, features, select, split) are defined in `dvc.yaml`. Running `dvc repro` executes the full pipeline. This is the first complete end-to-end data run.
> **🔧 Task:** Execute `dvc repro` on the full CICIDS-2017 pipeline. Monitor each stage output for errors. Verify: all expected output files exist; the selected features YAML is produced; train/val/test split sizes are as expected; no NaN values in any output array (spot-check with a verification script `scripts/verify_pipeline_outputs.py` that loads each `.npz` and checks for NaN/inf). Log total pipeline execution time. Push all outputs to DVC remote. Tag as `pipeline-v1.0`.
> **📦 Stack:** dvc, numpy, rich
> **✅ Outcome:** `dvc repro` completes without errors. `dvc status` shows no uncommitted changes. `git tag pipeline-v1.0` is pushed.

#### Subphase 24.2 — Reproducibility Validation

> **🎭 Role:** MLOps Engineer
> **📍 Context:** The pipeline must be byte-identical reproducible from the git tag and DVC remote alone. This is a hard requirement for research paper credibility.
> **🔧 Task:** Validate reproducibility: (1) delete all local pipeline outputs; (2) `dvc pull` from the remote to restore them; (3) compare the restored files byte-for-byte with the originals using SHA-256 checksums; (4) alternatively, run `dvc repro` from scratch on a fresh environment and compare outputs. Document the exact commands in `docs/reproducibility-validation.md`. Record any sources of non-determinism (random seeds must be fixed) and their mitigations.
> **📦 Stack:** dvc, hashlib, bash
> **✅ Outcome:** SHA-256 checksums of the reproduced pipeline outputs match the original outputs. `docs/reproducibility-validation.md` confirms the validation was performed.

---

## Phase 25 — MLflow Experiment Tracking Setup

**Context:** MLflow is the source of truth for all experiment results. The tracking setup must be complete before any model training begins.

#### Subphase 25.1 — MLflow Logger Utility

> **🎭 Role:** MLOps Engineer with MLflow expertise
> **📍 Context:** Six model families will each run dozens of Optuna trials. Every trial must log the same standard set of metrics, parameters, and tags. A centralised logger utility prevents inconsistency.
> **🔧 Task:** Implement `ml/src/tracking/mlflow_logger.py`. `XAIGuardLogger` class with methods: `start_run(experiment_name, run_name, tags)` that adds standard tags (dataset_version from DVC, git_sha, hardware: cpu/gpu, random_seed); `log_params(params: dict)`; `log_metrics(metrics: dict, step: int | None)`; `log_three_pillar_metrics(metrics: ThreePillarMetrics)` that logs all metrics from the evaluation framework; `log_model_artifact(model, preprocessing_pipeline, feature_list, framework)`; `end_run(status)`. Use context manager protocol (`__enter__`/`__exit__`) for safe run management.
> **📦 Stack:** mlflow 2.14, structlog
> **✅ Outcome:** `with XAIGuardLogger() as logger:` correctly starts and ends an MLflow run. All standard tags appear on every run. The model artifact is accessible from the MLflow UI.

#### Subphase 25.2 — Standard Metrics Computation Function

> **🎭 Role:** ML Research Engineer
> **📍 Context:** All six models are evaluated with the same metrics. A single function ensures all models are compared fairly and no metric is accidentally skipped.
> **🔧 Task:** Implement `ml/src/evaluation/metrics.py`. `compute_three_pillar_metrics(model, X_test, y_test, feature_names, latency_profiler) -> ThreePillarMetrics`. Pillar 1: `sklearn.metrics` for all classification metrics including per-class F1. Pillar 2: call SHAP explainer sanity check. Pillar 3: call `LatencyProfiler.profile(model, X_test)` returning P50/P95/P99. Define `ThreePillarMetrics` as a Pydantic v2 model with all metric fields and a `to_mlflow_dict()` method for logging.
> **📦 Stack:** sklearn 1.5, pydantic v2, numpy
> **✅ Outcome:** `compute_three_pillar_metrics(model, X_test, y_test, feature_names, profiler)` returns a `ThreePillarMetrics` with all fields populated.

#### Subphase 25.3 — Experiment Registry & Verification

> **🎭 Role:** MLOps Engineer
> **📍 Context:** Six experiments must be created in MLflow before training begins so all runs are organised correctly.
> **🔧 Task:** Write `ml/scripts/setup_mlflow_experiments.py` that creates or gets these MLflow experiments: `xaiguard_logistic_regression`, `xaiguard_random_forest`, `xaiguard_xgboost`, `xaiguard_lstm`, `xaiguard_transformer`, `xaiguard_lightweight_transformer`. For each experiment set tags: `model_family`, `pillar1_primary_metric=f1_macro`, `dataset=cicids2017`. Run a smoke-test experiment that logs a mock metric and verifies it appears in the MLflow UI. Write a verification script that asserts all six experiments exist and have the correct tags.
> **📦 Stack:** mlflow 2.14, typer
> **✅ Outcome:** `uv run python ml/scripts/setup_mlflow_experiments.py` creates all six experiments. The verification script passes.

---

## Phase Map

| Phase | Title | Subphases |
|-------|-------|-----------|
| P18 | Network Feature Engineering | 4 |
| P19 | Temporal Feature Engineering | 2 |
| P20 | Behavioral Feature Engineering | 2 |
| P21 | Threat Intel Feature Stubs | 1 |
| P22 | Feature Selection & Validation | 2 |
| P23 | Sequence Data Construction | 3 |
| P24 | DVC Pipeline Execution | 2 |
| P25 | MLflow Experiment Tracking Setup | 3 |

**Previous ←** [02 — Data Engineering](02-data-engineering.md) | **Next →** [04 — Classical ML & Sequence Models](04-ml-research-and-experiments.md)

---
