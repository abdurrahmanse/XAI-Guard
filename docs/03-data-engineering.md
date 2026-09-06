# 03 — Feature Engineering & Experiment Tracking

> **Phases 18–25** | Domain-specific feature engineering, feature selection, sequence data construction for deep learning models, DVC pipeline versioning, and MLflow experiment tracking setup.
>
> **How to use:** Pick one subphase. Copy its **Prompt** into your AI code editor. Implement it. Move to the next subphase.

---

## Phase 18 — Network Feature Engineering

**Context:** Raw network flow statistics alone are insufficient for high-precision threat detection. Engineering domain-specific features gives models security-relevant signal and produces SHAP explanations that analysts can immediately understand.

#### Subphase 18.1 — Bytes-Per-Packet Feature
> **Prompt:** Implement the bytes-per-packet derived feature for XAI-Guard. This is computed as total bytes transferred divided by the packet count for each connection. It is a key signal for DDoS detection where amplification attacks show abnormally high bytes per packet. Handle the divide-by-zero case for zero-packet connections by imputing zero. Write a unit test confirming the calculation and edge case handling.

#### Subphase 18.2 — Packet Rate Feature
> **Prompt:** Implement the packet rate derived feature for XAI-Guard. This is computed as packet count divided by connection duration in seconds. It is a strong indicator of scanning and flooding attacks that generate many packets in short time windows. Handle the zero-duration edge case. Write a unit test with synthetic data covering normal, DDoS, and zero-duration cases.

#### Subphase 18.3 — Port Entropy Feature
> **Prompt:** Implement the port entropy derived feature for XAI-Guard. For each source IP, compute the Shannon entropy of the destination port distribution over a sliding time window of 100 recent connections. High port entropy indicates port scanning behaviour where the source IP is probing many different destination ports. Write a unit test that confirms high entropy for a simulated port scan and low entropy for a legitimate single-service connection.

#### Subphase 18.4 — TCP Flag Ratio Feature
> **Prompt:** Implement the TCP flag ratio feature for XAI-Guard. Compute the ratio of SYN packets to total packets for each source IP in a rolling time window. A high SYN ratio without corresponding ACK responses is a classic SYN flood DDoS indicator. Write a unit test confirming the ratio calculation and that it correctly flags a simulated SYN flood pattern.

#### Subphase 18.5 — Connection Duration Z-Score Feature
> **Prompt:** Implement the connection duration z-score feature for XAI-Guard. For each source IP, compute the z-score of the current connection's duration relative to that IP's historical connections. Abnormally short or long connections relative to the source IP's baseline are anomaly indicators. The baseline statistics are computed on a rolling window. Write a unit test covering the first-connection cold-start case and a clearly anomalous connection.

#### Subphase 18.6 — Network Feature Integration Tests
> **Prompt:** Write integration tests for all five XAI-Guard network features applied together to a sample of real CICIDS-2017 data. Verify that: no feature produces NaN or infinite values on real data; all features produce the expected data types; the feature values are in reasonable ranges; and the features can be added to the main feature DataFrame without column name conflicts.

---

## Phase 19 — Temporal Feature Engineering

**Context:** Many attack patterns are only visible when looking at the sequence of events over time, not just individual connections. Temporal features expose these patterns to models.

#### Subphase 19.1 — Events-Per-Minute Rolling Feature
> **Prompt:** Implement the events-per-minute rolling count feature for XAI-Guard. For each source IP, count the number of connection events in the preceding 60 seconds using a rolling time window. This feature detects flooding attacks and rapid scanning where a single source IP generates an anomalously high event rate. Write a unit test with a simulated event stream confirming correct window boundaries.

#### Subphase 19.2 — Failed Login Rate Feature
> **Prompt:** Implement the failed login rate rolling feature for XAI-Guard. For each source IP, count the number of failed authentication events in the preceding 5 minutes. A high failed login rate is the primary signal for credential brute-force attacks. This feature requires the dataset to have a service or flag column indicating authentication failure. Write a unit test simulating a brute-force sequence.

#### Subphase 19.3 — Session Gap Feature
> **Prompt:** Implement the session gap feature for XAI-Guard. For each source IP, compute the time elapsed since that IP's most recent previous connection. An unusually short gap indicates automated scanning or flooding. An unusually long gap followed by unusual activity can indicate a dormant compromised host becoming active. Write a unit test covering first-ever connection and normal revisit patterns.

#### Subphase 19.4 — Time-of-Day Circular Encoding
> **Prompt:** Implement time-of-day circular encoding for XAI-Guard. Extract the hour from the connection timestamp and encode it as two features: the sine and cosine of 2*pi*hour/24. This circular encoding correctly captures the cyclical nature of time so that hour 23 and hour 0 are treated as close together by linear models. Write a unit test confirming that hours 0 and 24 produce identical encoded values.

#### Subphase 19.5 — Temporal Feature Tests
> **Prompt:** Write comprehensive tests for all XAI-Guard temporal features applied to a time-sorted event DataFrame. Verify that rolling window features respect the time ordering of events and do not leak future information into past windows. Verify that the features produce correct values at the window boundaries. Verify that all features remain valid after the cleaning and encoding pipeline has been applied to the data.

---

## Phase 20 — Behavioral Feature Engineering

**Context:** Behavioral features characterise how a source IP behaves across multiple connections, revealing patterns like port scanning and lateral movement that are invisible in individual connection features.

#### Subphase 20.1 — Unique Destination Ports Per Source
> **Prompt:** Implement the unique destination ports per source IP feature for XAI-Guard. For each source IP, count the number of distinct destination ports contacted in the preceding 60 seconds. A high count is the primary signal for horizontal port scanning. Write a unit test that confirms a simulated port scanner produces a high value while a legitimate single-service client produces a value of one.

#### Subphase 20.2 — Source IP Request Volume Percentile
> **Prompt:** Implement the source IP request volume percentile rank feature for XAI-Guard. For a given time window, rank all active source IPs by their total connection count and compute each IP's percentile rank. IPs in the top 1% of request volume are high-suspicion candidates for automated attacks. Write a unit test with a simulated distribution of source IPs confirming correct percentile computation.

#### Subphase 20.3 — Protocol Switch Rate
> **Prompt:** Implement the protocol switch rate feature for XAI-Guard. For each source IP, compute the fraction of consecutive connection pairs where the protocol changes (e.g., TCP to UDP to ICMP). Legitimate clients typically use one protocol per service. Attackers probing a network switch protocols frequently. Write a unit test with a simulated mixed-protocol sequence.

#### Subphase 20.4 — Behavioral Feature Tests
> **Prompt:** Write integration tests for all three XAI-Guard behavioral features applied together to a sample of real UNSW-NB15 data. Verify that features correctly distinguish between the behavioral patterns of the Reconnaissance attack class (high port count, high request volume) and normal traffic. Confirm no information leakage between time windows.

---

## Phase 21 — Threat Intelligence Feature Stubs

**Context:** Threat intelligence features will be wired to live APIs in Phase 53 (Threat Intelligence Module). Create stubs now so the feature pipeline is complete and model training can proceed. The stubs return zero but have the same interface as the live implementation.

#### Subphase 21.1 — Known Malicious IP Flag Stub
> **Prompt:** Implement the known malicious IP flag stub feature for XAI-Guard. The function accepts an IP address and returns zero as a stub value. Add a clear code comment documenting that this stub will be replaced in Phase 53 when the AbuseIPDB integration is wired. The function signature and return type must match exactly what the live implementation will provide so no calling code needs to change.

#### Subphase 21.2 — Tor Exit Node Flag Stub
> **Prompt:** Implement the Tor exit node flag stub feature for XAI-Guard. The function accepts an IP address and returns zero as a stub value. Add documentation explaining that this will be replaced in Phase 53 with a real lookup against the TorDNSEL list cached in Redis. The stub ensures all features referenced in model training are available during development even before the threat intelligence integrations are built.

#### Subphase 21.3 — Stub Documentation
> **Prompt:** Write a stub documentation file for XAI-Guard explaining all feature stubs, their purpose, their current behaviour, and the phase in which they will be replaced with live implementations. Include a test that verifies each stub returns the correct data type and does not raise any exception when given a valid IP address. This documentation serves as a reminder and handoff document for Phase 53.

---

## Phase 22 — Feature Selection & Validation

**Context:** With domain features added, the full feature set may exceed 100 features. Feature selection removes redundant and non-informative features, reduces overfitting risk, and improves XAI explanation conciseness.

#### Subphase 22.1 — Variance Threshold Filtering
> **Prompt:** Implement the variance threshold filter for XAI-Guard feature selection. Remove any feature whose variance across the training set is below 0.01, as near-constant features contain no discriminative information. Log the list of removed features and their variances to MLflow. Apply this as the first step in the feature selection pipeline.

#### Subphase 22.2 — Mutual Information Ranking
> **Prompt:** Implement mutual information-based feature ranking for XAI-Guard. Compute the mutual information score between each feature and the attack type label using scikit-learn's mutual_info_classif. Rank all features by their score. Log the full ranked list to MLflow. Use the mutual information scores to select the top N features where N is a configurable hyperparameter defaulting to 50.

#### Subphase 22.3 — Correlation-Based Redundancy Filter
> **Prompt:** Implement the correlation-based redundancy filter for XAI-Guard. Among the features surviving the mutual information threshold, identify pairs with absolute Pearson correlation above 0.95. From each correlated pair, remove the feature with the lower mutual information score. Log the removed features and their correlation partners to MLflow. This step ensures the final feature set contains no redundant features.

#### Subphase 22.4 — Selected Feature List Documentation
> **Prompt:** After running the full feature selection pipeline on CICIDS-2017, produce and document the final selected feature list for XAI-Guard. Save the list as a YAML artifact committed to the repository. This list defines the exact features used in all model training. Any future change to this list constitutes a new experiment version and must be tracked as a new DVC pipeline run.

#### Subphase 22.5 — Feature Importance Visualisation Notebook
> **Prompt:** Create a feature importance visualisation notebook for XAI-Guard that shows: a bar chart of all features ranked by mutual information score, a correlation heatmap of the final selected features, and a comparison between engineered features and raw network features by their mutual information rank. This notebook is referenced in the research paper's feature engineering section.

---

## Phase 23 — Sequence Data Construction

**Context:** LSTM and Transformer models require sequential input data. The sequence builder converts sorted tabular events into fixed-length windows that these models can process.

#### Subphase 23.1 — Sliding Window Design
> **Prompt:** Design and document the sliding window strategy for XAI-Guard sequence construction. Events must be sorted by source IP and then by timestamp before windowing. A window of N consecutive events from the same source IP becomes one sequence sample. The label of the sequence is the label of the last event in the window. Document the default window size of 10 events and stride of 1, and why these defaults were chosen based on typical attack sequence lengths.

#### Subphase 23.2 — Sequence Builder Implementation
> **Prompt:** Implement the sequence builder for XAI-Guard that converts the preprocessed tabular feature matrix into a 3D array of shape (number of sequences, window length, number of features) and a corresponding label array of shape (number of sequences). The builder sorts events by source IP and timestamp, applies the sliding window with the configured stride, and handles the edge case where a source IP has fewer events than the window size by padding with zeros.

#### Subphase 23.3 — Positional Encoding for Transformer
> **Prompt:** Implement sinusoidal positional encoding for XAI-Guard Transformer input. The positional encoding adds a fixed pattern to each position in the input sequence that allows the Transformer's self-attention mechanism to distinguish the order of events. Implement the standard sinusoidal encoding formula with configurable d_model and max_len parameters. Write a unit test confirming that different positions produce different encoding vectors.

#### Subphase 23.4 — PyTorch Dataset Wrappers
> **Prompt:** Implement PyTorch Dataset classes for both tabular and sequence data in XAI-Guard. The TabularDataset wraps a 2D NumPy array and label vector. The SequenceDataset wraps the 3D sequence array and label vector. Both datasets return tensors of the correct dtype: float32 for features and long for class labels. Write unit tests confirming correct tensor shapes and dtypes.

#### Subphase 23.5 — DataLoader Configuration
> **Prompt:** Implement the DataLoader factory for XAI-Guard that creates train, validation, and test DataLoaders from a dataset with a reproducible train/validation split. Configure the default batch size, shuffle behaviour (shuffle only training), number of worker processes, and pin_memory for GPU transfers. The factory accepts a random seed for reproducible splits. Write a test confirming the split sizes sum to the full dataset size.

#### Subphase 23.6 — Sequence Builder Tests
> **Prompt:** Write comprehensive tests for the XAI-Guard sequence builder. Verify: the output shape is correct for a given window size and stride; events from different source IPs are never mixed into the same window; the label assigned to each window matches the last event in that window; zero-padding is correctly applied for short source IP histories; and the sequence builder output is reproducible given the same sorted input.

---

## Phase 24 — DVC Pipeline Setup

**Context:** DVC (Data Version Control) makes every dataset version and pipeline output reproducible from a git commit. This is non-negotiable for a research project whose results must be reproducible by others.

#### Subphase 24.1 — DVC Initialisation
> **Prompt:** Initialise DVC in the XAI-Guard ML module. Run dvc init, configure the DVC remote storage to point to the MinIO artifact store bucket using the S3-compatible endpoint, and verify the connection. Commit the DVC configuration files to git. Establish the convention that all data files are tracked by DVC and excluded from git.

#### Subphase 24.2 — Data Directory Tracking
> **Prompt:** Add all XAI-Guard data directories to DVC tracking. Track the raw dataset directories for all four datasets, the interim cleaned data directory, the processed feature matrix directory, and the train/test split directories. Push the initial data state to the MinIO remote. The DVC pointer files are committed to git so that anyone can reproduce the exact data state with dvc pull.

#### Subphase 24.3 — DVC Pipeline Stage Definition
> **Prompt:** Define the XAI-Guard DVC pipeline stages in a dvc.yaml file. Create stages for: download (fetches raw datasets), clean (runs the cleaning pipeline), encode (runs encoding and scaling), features (runs feature engineering), select (runs feature selection), and split (creates reproducible train/validation/test splits). Each stage declares its dependencies and outputs so DVC can determine which stages need to re-run when inputs change.

#### Subphase 24.4 — Pipeline Execution & Caching
> **Prompt:** Configure DVC pipeline execution caching for XAI-Guard. DVC caches the output of each stage so that stages with unchanged inputs are not re-run. Test the full pipeline by running dvc repro from scratch and verifying all stage outputs are produced. Then modify one upstream stage and re-run to verify only the affected downstream stages re-execute. Document the expected pipeline execution time for fresh runs and cached runs.

#### Subphase 24.5 — Reproducibility Validation
> **Prompt:** Validate full reproducibility of the XAI-Guard DVC pipeline. Check out a specific git commit, run dvc pull to retrieve the matching data state, run dvc repro, and verify the output feature matrices are byte-identical to the originally produced artifacts. Tag the validated pipeline state as data-v1.0 in both git and DVC. Document the exact commands needed to reproduce any experiment from only a git tag.

---

## Phase 25 — MLflow Experiment Tracking Setup

**Context:** MLflow tracks every training run: parameters, metrics, and model artifacts. Combined with DVC, it ensures every result in the research paper can be traced back to the exact code, data, and configuration that produced it.

#### Subphase 25.1 — Experiment Registry Definition
> **Prompt:** Define the MLflow experiment registry for XAI-Guard. Create a YAML configuration file listing all six experiments by name: one per model family. Define the experiment naming convention, the standard tags applied to every run (dataset version from DVC, git commit SHA, random seed, hardware used), and the required run parameters that must be logged for every experiment to enable cross-experiment comparison.

#### Subphase 25.2 — MLflow Logger Utility
> **Prompt:** Implement the MLflow logger utility class for XAI-Guard that provides a clean interface for all ML modules to use. The class wraps MLflow run management and exposes methods for starting a run with the standard tags, logging parameters, logging metrics with optional step numbers, logging the fitted model artifact to the registry, logging additional file artifacts, and ending the run cleanly. All model training scripts use this utility rather than calling MLflow directly.

#### Subphase 25.3 — Standard Metrics Logging Convention
> **Prompt:** Define and implement the standard metrics logging convention for XAI-Guard. Every training run must log: accuracy, precision macro, recall macro, F1 macro, ROC-AUC macro, PR-AUC macro, F1 per attack class, training time in seconds, inference latency at P50/P95/P99 in milliseconds, peak memory usage in MB, and model file size in MB. Implement a utility function that computes all of these from a fitted model and test set and logs them in a single call.

#### Subphase 25.4 — Model Registration Convention
> **Prompt:** Define the MLflow model registration convention for XAI-Guard. Every trained model that meets the minimum performance threshold is registered in the MLflow Model Registry under a consistent naming pattern. The registration includes the model artifact, the preprocessing pipeline artifact, the feature list artifact, and the evaluation metrics. Document the transition states: from None to Staging when registered, to Production when promoted as Champion, and to Archived when replaced.

#### Subphase 25.5 — Experiment UI Verification
> **Prompt:** Write a verification procedure for the XAI-Guard MLflow experiment tracking setup. Run a minimal dummy training experiment that logs mock parameters and metrics, registers a mock model, and transitions it through the staging state. Verify the experiment appears correctly in the MLflow UI with all required fields. Confirm that running dvc pull followed by the dummy experiment produces identical results on a different machine. Document this as the reproducibility smoke test.

---

## Phase Map

| Phase | Title | Subphases |
|-------|-------|-----------|
| P18 | Network Feature Engineering | 6 |
| P19 | Temporal Feature Engineering | 5 |
| P20 | Behavioral Feature Engineering | 4 |
| P21 | Threat Intel Feature Stubs | 3 |
| P22 | Feature Selection & Validation | 5 |
| P23 | Sequence Data Construction | 6 |
| P24 | DVC Pipeline Setup | 5 |
| P25 | MLflow Experiment Tracking | 5 |

**Previous ←** [02 — Data Engineering](02-data-engineering.md) | **Next →** [04 — Classical ML & Sequence Models](04-ml-research-and-experiments.md)
