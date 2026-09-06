# 02 — Data Engineering

> **Phases 9–17** | Dataset acquisition, EDA across four benchmark datasets, cross-dataset schema mapping, cleaning pipeline, encoding, scaling, and class imbalance handling.
>
> **Prompt Engineering Format:** Each subphase prompt contains a **Role** (who the AI acts as), **Context** (what already exists), **Task** (what to build precisely), **Stack** (exact packages), and **Outcome** (what done looks like).

---

## Phase 9 — Dataset Strategy & Acquisition

**Context:** Establish the data foundation before any analysis. Incorrect or corrupted data invalidates all downstream experiments.

#### Subphase 9.1 — Dataset Download & Integrity Verification

> **🎭 Role:** Senior Data Engineer and ML Research Infrastructure Engineer
> **📍 Context:** The XAI-Guard evaluation framework (Phase 1) requires four benchmark datasets. Nothing has been downloaded yet. All ML experiments depend on exactly these versions of these datasets.
> **🔧 Task:** Write an automated dataset acquisition script using `httpx` for async HTTP downloads with progress bars via `rich.progress`. For each dataset (NSL-KDD, CICIDS-2017, UNSW-NB15, BETH): download from the official source URL, verify the SHA-256 checksum against the documented value (fail loudly if mismatch), extract the archive if compressed, log the file size and row count to MLflow as data provenance tags. Make the script idempotent: skip already-downloaded and verified files. Use `typer` for the CLI interface with a `--dataset` filter flag.
> **📦 Stack:** httpx, rich, typer, mlflow 2.x, hashlib (stdlib)
> **✅ Outcome:** `uv run python ml/scripts/download_datasets.py` downloads all four datasets. Re-running it skips already-verified files. MLflow shows data provenance tags for the run.

#### Subphase 9.2 — DVC Initialisation & Remote Configuration

> **🎭 Role:** MLOps Engineer with DVC and S3-compatible storage expertise
> **📍 Context:** Datasets are downloaded. They must immediately be placed under DVC version control so all future experiments reference a specific, reproducible data version. MinIO is the DVC remote (configured in Phase 4).
> **🔧 Task:** Initialise DVC in the `ml/` directory. Configure the DVC remote to use the MinIO S3-compatible endpoint with credentials from the environment. Add all four raw dataset directories to DVC tracking with `dvc add`. Run `dvc push` to upload to MinIO. Commit the DVC pointer files (`.dvc` files and `.dvcignore`) to git. Tag the commit as `data-v1.0`. Verify reproducibility: delete the local data, run `dvc pull`, confirm byte-identical files.
> **📦 Stack:** dvc[s3] 3.51, boto3 (used by DVC internally), MinIO
> **✅ Outcome:** `git checkout data-v1.0 && dvc pull` reproduces the exact data state on any machine with DVC remote access. `dvc status` shows no changes.

#### Subphase 9.3 — DVC Pipeline Stage Definitions

> **🎭 Role:** MLOps Pipeline Architect
> **📍 Context:** DVC version controls data. Now define the full processing pipeline as DVC stages so every output is reproducible and only re-runs when its inputs change.
> **🔧 Task:** Write `ml/dvc.yaml` defining pipeline stages with explicit `deps`, `outs`, `params`, and `metrics` declarations: `download` stage (deps: download script; outs: raw/ directories); `clean` stage (deps: raw/ + cleaning script; outs: interim/; metrics: cleaning_report.json); `encode` stage (deps: interim/ + encoding script; outs: processed/; params: ml/configs/preprocessing.yaml); `features` stage (deps: processed/ + feature engineering scripts; outs: features/); `select` stage (deps: features/ + selection config; outs: selected/); `split` stage (deps: selected/; outs: splits/train, splits/val, splits/test). Configure `dvc params` to track all hyperparameters from YAML configs.
> **📦 Stack:** dvc[s3] 3.51, PyYAML
> **✅ Outcome:** `dvc repro` runs the full pipeline from scratch. Modifying `ml/configs/preprocessing.yaml` causes only the `encode` stage and its descendants to re-run. `dvc dag` shows the correct pipeline graph.

#### Subphase 9.4 — Data Validation Schema

> **🎭 Role:** Data Quality Engineer
> **📍 Context:** Raw datasets have known quality issues: CICIDS-2017 has infinite values, NSL-KDD has label inconsistencies, UNSW-NB15 has schema differences across partition files. A validation schema catches regressions.
> **🔧 Task:** Write a data validation module using `pandera` that runs immediately after download. Define a `DatasetSchema` for each of the four datasets specifying: required columns with data types, valid value ranges for numeric features (e.g., packet count >= 0), allowed categorical values for label columns, null rate threshold per column, and duplicate row threshold. The validator runs as the first DVC stage and produces a `validation_report.json` artifact logged to MLflow. It fails the pipeline if any critical check fails.
> **📦 Stack:** pandera 0.19, pandas 2.x, mlflow 2.x
> **✅ Outcome:** `uv run python ml/src/data/validate.py --dataset cicids2017` produces a validation report. A corrupted dataset causes a clear, actionable error message that identifies the failing column and check.

#### Subphase 9.5 — Data Directory Structure & Gitignore

> **🎭 Role:** ML Infrastructure Engineer
> **📍 Context:** A clean, documented directory structure prevents data files from being committed to git and ensures all pipeline stages write outputs to the correct location.
> **🔧 Task:** Define and document the complete `ml/data/` directory structure: `raw/{dataset_name}/` (DVC-tracked, git-ignored), `interim/{dataset_name}/` (DVC-tracked, after cleaning), `processed/{dataset_name}/` (DVC-tracked, after encoding), `features/` (DVC-tracked, engineered features), `splits/{train,val,test}/` (DVC-tracked, final splits). Write `ml/data/.gitignore` excluding all data files. Write `ml/data/README.md` documenting each directory's purpose, the DVC command to access it, and which pipeline stage produces it. Create a `DataPaths` configuration class using `pydantic-settings` that resolves all paths from a configurable base directory.
> **📦 Stack:** pydantic-settings, pathlib (stdlib)
> **✅ Outcome:** `DataPaths().raw_dir / "cicids2017"` resolves to the correct path. `git status` shows no data files. `dvc pull` populates all directories.

---

## Phase 10 — NSL-KDD Exploratory Data Analysis

**Context:** NSL-KDD is the established IDS benchmark that sets the performance floor. Understanding its train/test distribution mismatch is critical to interpreting model results.

#### Subphase 10.1 — Dataset Loading & Statistical Profiling

> **🎭 Role:** Senior Data Scientist with IDS benchmark expertise
> **📍 Context:** NSL-KDD datasets are downloaded and validated. This EDA notebook is the first human-readable analysis of the data and informs all preprocessing decisions.
> **🔧 Task:** Create `ml/notebooks/eda/01_nslkdd_eda.ipynb`. Load KDDTrain+ and KDDTest+ using pandas with explicit dtype specification. Generate a full ydata-profiling HTML report and save as an artifact. Compute and display: dataset shape, schema with dtypes, null counts per column, duplicate row count, memory usage. Use `rich` tables for clean console output. Log the profile report path to MLflow as a run artifact.
> **📦 Stack:** pandas 2.x, ydata-profiling, rich, mlflow 2.x
> **✅ Outcome:** The notebook runs end-to-end without errors. The profiling report HTML file is committed as a git-tracked artifact. MLflow shows the artifact link.

#### Subphase 10.2 — Class Distribution & Train/Test Mismatch Analysis

> **🎭 Role:** Senior Data Scientist
> **📍 Context:** NSL-KDD has a well-documented train/test distribution mismatch: the test set contains attack subtypes absent from training. Quantifying this is essential for interpreting per-class recall.
> **🔧 Task:** Extend the NSL-KDD EDA notebook. Compute: attack category distribution in KDDTrain+ and KDDTest+ as percentage tables using pandas. Visualise both distributions as side-by-side Recharts-ready JSON (for the research paper) and as matplotlib bar charts (for the notebook). Identify attack subtypes present in the test set but absent from training. Compute the Jensen-Shannon divergence between train and test label distributions. Map all native labels to the unified XAI-Guard taxonomy from Phase 1 and show the mapping table.
> **📦 Stack:** pandas 2.x, matplotlib, scipy, numpy
> **✅ Outcome:** The notebook outputs a markdown table of train/test distribution mismatch ready to paste into the research paper. All native labels are correctly mapped to the taxonomy enum.

#### Subphase 10.3 — Feature Correlation & Importance Analysis

> **🎭 Role:** Senior Data Scientist and Feature Engineer
> **📍 Context:** NSL-KDD has 41 features, many highly correlated. Identifying redundant features now reduces dimensionality and improves SHAP explanation conciseness.
> **🔧 Task:** Extend the NSL-KDD EDA notebook. Compute the Pearson correlation matrix for all 41 numeric features. Plot a seaborn heatmap. Flag all feature pairs with |r| > 0.95 as redundancy candidates. Compute mutual information scores between each feature and the attack type label using `sklearn.feature_selection.mutual_info_classif`. Plot top 20 features by mutual information. Save a JSON file `ml/configs/nslkdd_feature_candidates.json` listing the recommended features to investigate for removal.
> **📦 Stack:** pandas, seaborn, sklearn 1.5, numpy
> **✅ Outcome:** The notebook produces a publishable correlation heatmap figure. The feature candidates JSON is committed to the repository and referenced by the feature selection phase.

#### Subphase 10.4 — EDA Findings Documentation

> **🎭 Role:** ML Research Lead
> **📍 Context:** EDA findings must be documented as structured decisions, not just notebook observations, so they directly inform the preprocessing pipeline in Phases 15–16.
> **🔧 Task:** Add a final section to the NSL-KDD EDA notebook that produces a structured findings YAML file `ml/configs/nslkdd_eda_findings.yaml`. Include: null_columns (list of columns with > 5% nulls), duplicate_count, high_correlation_pairs (list of {col_a, col_b, r} for |r|>0.95), low_resource_classes (attack subtypes with < 100 training samples), train_test_js_divergence, recommended_preprocessing_actions (list of action strings). This YAML is read by the cleaning and encoding pipeline scripts.
> **📦 Stack:** pandas, PyYAML
> **✅ Outcome:** `ml/configs/nslkdd_eda_findings.yaml` exists and is valid YAML. The cleaning pipeline script loads it to configure preprocessing decisions.

---

## Phase 11 — CICIDS-2017 Exploratory Data Analysis

**Context:** CICIDS-2017 is the primary training dataset — the most realistic and the most challenging due to severe class imbalance and data quality issues that must be fully understood before training.

#### Subphase 11.1 — Multi-File Loading & Profiling

> **🎭 Role:** Senior Data Engineer
> **📍 Context:** CICIDS-2017 is distributed across 8 daily capture CSV files with inconsistent column names and header formats. Loading it correctly is non-trivial.
> **🔧 Task:** Create `ml/notebooks/eda/02_cicids2017_eda.ipynb`. Write a robust multi-file loader that: standardises column names (strip whitespace, lowercase, replace spaces with underscores), handles the header inconsistency across files, concatenates with a `capture_day` column added, detects and counts all infinite values (replace with NaN for profiling), handles negative values in non-negative feature columns. Generate a ydata-profiling minimal report (not full, for speed). Log the combined dataset shape and null counts to MLflow.
> **📦 Stack:** pandas 2.x, numpy, ydata-profiling, mlflow 2.x
> **✅ Outcome:** The notebook loads all 8 files into a single 2.8M-row DataFrame without errors. Column names are consistent. Infinite value counts are reported per column.

#### Subphase 11.2 — Class Imbalance Severity Analysis

> **🎭 Role:** Senior Data Scientist specialising in imbalanced learning
> **📍 Context:** CICIDS-2017 has extreme class imbalance: BENIGN traffic accounts for 83% of samples. Models trained naively optimise accuracy by predicting BENIGN, producing near-zero recall on rare attack classes.
> **🔧 Task:** Extend the CICIDS-2017 notebook with a class imbalance analysis. Compute: class distribution as percentage table, imbalance ratio (majority count / each minority count), and required SMOTE oversampling ratios to reach 10:1 maximum imbalance. Plot the distribution on both linear and log-10 scales side by side. Identify the two most severely underrepresented attack classes. Document the target class distribution after resampling as `target_distribution: dict[str, float]` in `ml/configs/cicids2017_eda_findings.yaml`.
> **📦 Stack:** pandas, matplotlib, imbalanced-learn 0.12
> **✅ Outcome:** The imbalance analysis plot is saved as `ml/notebooks/figures/cicids2017_class_imbalance.png`. The target distribution is documented for the resampling phase.

#### Subphase 11.3 — Data Quality Investigation

> **🎭 Role:** Data Quality Engineer
> **📍 Context:** CICIDS-2017 is known to contain features with infinite values, negative values in non-negative feature columns, and near-zero variance features. These must be catalogued before cleaning.
> **🔧 Task:** Extend the notebook with a data quality section. For each column compute: count of +inf, count of -inf, count of NaN, count of negative values where the feature is inherently non-negative (packet counts, byte counts, durations). Identify constant columns (single unique value). Flag all columns exceeding the pandera thresholds from Phase 9. Document all issues in `ml/configs/cicids2017_eda_findings.yaml` with the recommended fix (clip, replace, drop, impute). Save a quality report CSV with one row per column and columns for each issue type.
> **📦 Stack:** pandas, numpy
> **✅ Outcome:** The quality report CSV is committed. The YAML findings file contains a `data_quality_issues` key consumed by the cleaning pipeline.

#### Subphase 11.4 — Temporal Pattern Analysis

> **🎭 Role:** Senior Data Scientist
> **📍 Context:** CICIDS-2017 spans five capture days with different attack types on each day. This temporal structure is used to simulate data drift in Phase 45 and must be characterised now.
> **🔧 Task:** Extend the notebook with temporal analysis. Group by `capture_day` and compute: event count per day, attack type distribution per day, mean values of key features per day. Plot a stacked bar chart of attack type counts per capture day. Compute the Jensen-Shannon divergence between each pair of consecutive days' feature distributions. Identify the day pair with the largest distribution shift — this becomes the drift simulation split point. Save the split point as `temporal_drift_split_day` in the EDA findings YAML.
> **📦 Stack:** pandas, matplotlib, scipy
> **✅ Outcome:** The temporal analysis figure is saved. The drift split point is documented for Phase 45.

#### Subphase 11.5 — Feature Multicollinearity & Selection Candidates

> **🎭 Role:** Feature Engineering Lead
> **📍 Context:** CICIDS-2017 has 78 features, many of which are linear combinations of the same underlying network statistics. Reducing to a non-redundant set improves model generalisation and SHAP explanation quality.
> **🔧 Task:** Extend the notebook with multicollinearity analysis. Compute the Pearson correlation matrix for all 78 numeric features. Identify correlated clusters with |r| > 0.95. Within each cluster, retain the feature with the highest mutual information with the label and flag the rest for removal. Also identify near-zero variance features (variance < 0.01). Save the removal candidate list as `removal_candidates: list[str]` in `ml/configs/cicids2017_eda_findings.yaml`.
> **📦 Stack:** pandas, seaborn, sklearn
> **✅ Outcome:** The correlation heatmap with cluster annotations is saved as a figure. The removal candidates YAML key reduces the feature count by approximately 20–25 features.

---

## Phase 12 — UNSW-NB15 Exploratory Data Analysis

**Context:** UNSW-NB15 provides nine modern attack categories. It tests whether models trained on CICIDS-2017 generalise to a different attack taxonomy with different network characteristics.

#### Subphase 12.1 — Multi-Partition Loading & Profiling

> **🎭 Role:** Senior Data Engineer
> **📍 Context:** UNSW-NB15 is split across four CSV partition files plus a separate ground-truth labels file. The merge requires careful key alignment.
> **🔧 Task:** Create `ml/notebooks/eda/03_unswnb15_eda.ipynb`. Write a loader that reads all four partition CSV files, loads the ground-truth labels file, merges on the correct key columns, validates the merge produced no NaN labels, and adds a `split` column indicating the official train/test partition assignment. Generate a profiling report. Log dataset characteristics to MLflow.
> **📦 Stack:** pandas, ydata-profiling, mlflow
> **✅ Outcome:** The notebook produces a single unified DataFrame with all features and correct labels. The merge key alignment is validated with an assertion.

#### Subphase 12.2 — Nine-Category Taxonomy Mapping

> **🎭 Role:** Cybersecurity Data Scientist
> **📍 Context:** UNSW-NB15 has nine attack categories (Fuzzers, Analysis, Backdoors, DoS, Exploits, Generic, Reconnaissance, Shellcode, Worms) that must map to the XAI-Guard unified taxonomy for cross-dataset evaluation.
> **🔧 Task:** Extend the notebook with taxonomy mapping. Create the complete mapping from UNSW-NB15 categories to the XAI-Guard unified taxonomy enum. For categories with no direct equivalent (Shellcode, Worms), document the mapping rationale. Compute the sample count per original category and per unified taxonomy class. Flag classes with fewer than 100 samples as `low_resource_classes`. Save the mapping as a Python dict in `ml/configs/unswnb15_taxonomy_mapping.yaml`.
> **📦 Stack:** pandas, PyYAML
> **✅ Outcome:** Every UNSW-NB15 sample has a valid unified taxonomy label. The mapping YAML is consumed by the label encoding step in Phase 16.

#### Subphase 12.3 — Feature Distribution & Near-Zero Variance

> **🎭 Role:** Senior Data Scientist
> **📍 Context:** UNSW-NB15 features have different statistical properties from CICIDS-2017. Understanding their distributions guides scaler selection and identifies low-information features.
> **🔧 Task:** Extend the notebook. For each of the 49 features: compute variance, mean, skewness, kurtosis. Flag features with variance < 0.01 as near-constant. For the top 10 highest-variance features, plot the distribution separately for benign and malicious classes to visualise separability. Compute the Earth Mover's Distance (Wasserstein-1) between benign and malicious distributions per feature. Rank features by EMD (higher = more separable). Save the EMD ranking as `emd_feature_ranking: list[str]` in `ml/configs/unswnb15_eda_findings.yaml`.
> **📦 Stack:** pandas, scipy, matplotlib, numpy
> **✅ Outcome:** The EMD ranking is saved. The top 10 separability plots are saved as figure files referenced in the research paper.

#### Subphase 12.4 — EDA Findings & Cross-Dataset Comparison Stub

> **🎭 Role:** ML Research Lead
> **📍 Context:** UNSW-NB15 EDA findings feed Phase 14 (cross-dataset schema mapping). A comparison table stub makes Phase 14 straightforward.
> **🔧 Task:** Add a final section to the UNSW-NB15 notebook that produces: (1) `ml/configs/unswnb15_eda_findings.yaml` with null_columns, near_zero_variance_features, emd_feature_ranking, low_resource_classes, taxonomy_mapping path; (2) A cross-dataset comparison table stub as a pandas DataFrame comparing NSL-KDD and UNSW-NB15 on: record count, feature count, null rate %, duplicate rate %, class count, and primary preprocessing challenge. Save as CSV for Phase 14 to extend.
> **📦 Stack:** pandas, PyYAML
> **✅ Outcome:** Both the YAML and the comparison table CSV exist. Phase 14 can load the CSV and append CICIDS-2017 and BETH rows.

---

## Phase 13 — BETH Dataset Exploratory Data Analysis

**Context:** BETH is real enterprise honeypot data spanning weeks. Its temporal extent makes it the only dataset that can demonstrate genuine data drift over time.

#### Subphase 13.1 — Temporal Loading & Timeline Visualisation

> **🎭 Role:** Senior Data Scientist with temporal data expertise
> **📍 Context:** BETH contains 14 features and spans multiple weeks of real network activity. The temporal ordering is critical — future information must never leak into the past.
> **🔧 Task:** Create `ml/notebooks/eda/04_beth_eda.ipynb`. Load BETH with correct timestamp parsing as UTC-aware datetime. Sort by timestamp ascending (enforce chronological order). Plot event count per hour across the full capture period as a timeline using matplotlib. Annotate the chart with the total capture duration in days. Compute basic statistics: total records, date range, records per day (mean, std, min, max), null rate per column.
> **📦 Stack:** pandas, matplotlib, numpy
> **✅ Outcome:** The timeline plot shows the full capture period with no gaps in the timestamp axis. The notebook cannot produce out-of-order timestamps.

#### Subphase 13.2 — Label Distribution Over Time & Drift Windows

> **🎭 Role:** Senior Data Scientist specialising in temporal ML
> **📍 Context:** The ratio of malicious to benign events changes over the capture period as attack patterns evolve. Identifying these natural drift windows is the key research value of BETH.
> **🔧 Task:** Extend the BETH notebook. Compute the malicious event rate (proportion of malicious events) per day and per week across the full capture period. Plot as a line chart with a rolling 7-day average. Identify time windows where the malicious rate changes by more than 2 standard deviations from the mean — these are natural drift events. Log their start/end timestamps to `ml/configs/beth_drift_windows.yaml`. These windows are used as the drift simulation scenarios in Phase 45.
> **📦 Stack:** pandas, matplotlib, numpy, PyYAML
> **┅ Outcome:** `ml/configs/beth_drift_windows.yaml` contains at least 2 identified drift windows. The drift simulation in Phase 45 loads these windows directly.

#### Subphase 13.3 — Feature Gap Analysis & Imputation Strategy

> **🎭 Role:** Feature Engineer
> **📍 Context:** BETH has only 14 features while the unified schema may have 50+. The feature gap strategy determines how BETH samples can be used in cross-dataset evaluation.
> **🔧 Task:** Extend the BETH notebook. Map BETH's 14 features to the unified schema from Phase 14 using the YAML mapping format. Identify features in the unified schema that have no BETH equivalent. For each missing feature, document the imputation strategy: zeros for features that represent counts (0 = no packets of that type seen), training-set median for features that represent rates, and explicit exclusion for features with no meaningful BETH equivalent. Save the imputation strategy as `ml/configs/beth_feature_gaps.yaml`.
> **📦 Stack:** pandas, PyYAML
> **┅ Outcome:** Every BETH sample can be transformed to the unified schema using the imputation strategy. No features are silently dropped.

#### Subphase 13.4 — Per-Feature Drift Characterisation

> **🎭 Role:** ML Research Scientist with distribution shift expertise
> **📍 Context:** The drift detector in Phase 45 will be tuned using BETH as the primary drift benchmark. Understanding which features drift most helps configure the MMD detector.
> **🔧 Task:** Extend the BETH notebook. For each of the 14 features, compute the Wasserstein-1 distance between the distribution in the first identified drift window and the last drift window. Rank features by drift magnitude (highest to lowest). Plot the top 5 drifting features' distribution shift as overlapping KDE plots (before vs. after). Save the drift magnitude ranking as `feature_drift_ranking: list[str]` in `ml/configs/beth_eda_findings.yaml`. This ranking informs the MMD detector feature weighting in Phase 45.
> **📦 Stack:** pandas, scipy, seaborn
> **┅ Outcome:** The KDE comparison plots are saved as publishable figures. The drift ranking is available for Phase 45 MMD configuration.

---

## Phase 14 — Cross-Dataset Schema Mapping

**Context:** All four datasets must speak the same language. The unified schema is the translation layer that makes cross-dataset training and evaluation possible.

#### Subphase 14.1 — Unified Feature Schema Definition

> **🎭 Role:** Principal Data Architect and Feature Engineer
> **📍 Context:** EDA on all four datasets is complete. The unified schema must include all features present in at least three of four datasets. This is the final feature vocabulary for the entire project.
> **🔧 Task:** Write `ml/configs/unified_schema.yaml` defining the final unified feature schema. For each feature: `name` (snake_case, descriptive), `dtype` (float32/int32/bool/categorical), `description`, `valid_range` ({min, max} for numeric), `imputation_strategy` (median/zero/mode/exclude), `present_in` (list of dataset names). Features must be present in at least 3 of 4 datasets to be included. Also define `label_column: attack_class`, `label_dtype: int8`, `taxonomy_mapping` reference. The schema is loaded by the Pydantic `UnifiedSchema` class that validates every processed DataFrame.
> **📦 Stack:** PyYAML, Pydantic v2, pandas
> **┅ Outcome:** `UnifiedSchema.validate(df)` passes for each dataset after mapping. `len(UnifiedSchema.features)` is documented as the final feature count used in all experiments.

#### Subphase 14.2 — Per-Dataset Column Mapping Configs

> **🎭 Role:** Data Engineer
> **📍 Context:** Each dataset uses different column names and sometimes combines what should be separate features. The mapping configs make the preprocessing pipeline generic.
> **🔧 Task:** Create four YAML mapping files, one per dataset: `ml/configs/mappings/{dataset}_column_mapping.yaml`. Each file maps `{native_column_name}: {unified_schema_name}` with an optional `transform` key for computed fields (e.g., `"bytes_per_packet": {"formula": "total_bytes / packet_count"}`). Document columns that are dropped (not mapped). Include data type coercion rules. Write a unit test that applies each mapping config to a 10-row fixture DataFrame and validates the output against the unified schema.
> **📦 Stack:** PyYAML, pandas, pytest
> **┅ Outcome:** The four mapping YAML files exist. The mapping unit tests pass. Any change to a mapping is caught by CI.

#### Subphase 14.3 — Unified Statistics Summary

> **🎭 Role:** ML Research Lead
> **📍 Context:** The research paper's methodology section requires a dataset comparison table. Generate it automatically from the EDA findings YAML files so it stays in sync.
> **🔧 Task:** Write `ml/notebooks/eda/05_cross_dataset_summary.ipynb`. Load all four EDA findings YAML files and produce: (1) a pandas DataFrame comparison table with columns for each dataset and rows for: record count, feature count after mapping, null rate %, duplicate rate %, class count after taxonomy mapping, imbalance ratio, and primary challenge; (2) export the table as Markdown (for the research paper) and as a styled HTML table; (3) log the Markdown table to MLflow as a run note.
> **📦 Stack:** pandas, tabulate, mlflow
> **┅ Outcome:** The Markdown table can be pasted directly into the research paper's methodology section without manual editing.

#### Subphase 14.4 — Schema Mapping Test Suite

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** The column mapping is a critical transformation. Errors here silently corrupt every downstream experiment. A comprehensive test suite catches regressions.
> **🔧 Task:** Write `ml/tests/test_schema_mapping.py` using pytest. Use `factory-boy` factories to generate synthetic DataFrames matching each dataset's raw schema. For each dataset: test that applying the column mapping produces a DataFrame matching the unified schema exactly; test that the label mapping produces valid taxonomy enum integers; test that applying the mapping to a DataFrame with a new unknown column raises a clear ValueError; test that the mapping is idempotent (applying it twice produces the same result). All four dataset mapping tests must pass in CI.
> **📦 Stack:** pytest, factory-boy, pandas, pandera
> **┅ Outcome:** `uv run pytest ml/tests/test_schema_mapping.py -v` passes all tests. Adding a new column to a dataset's raw schema without updating the mapping file causes a test failure.

---

## Phase 15 — Data Cleaning Pipeline

**Context:** Build the first reproducible pipeline stage. Every cleaning decision is traceable to an EDA finding, and all fitted parameters are serialised for production reuse.

#### Subphase 15.1 — Cleaning Transformer: Missing & Infinite Values

> **🎭 Role:** Senior ML Engineer with scikit-learn pipeline expertise
> **📍 Context:** EDA findings are documented in YAML files. The cleaning transformer reads these configs, not hardcoded values. The transformer must be scikit-learn compatible (fit/transform interface) for pipeline composition.
> **🔧 Task:** Implement `ml/src/preprocessing/cleaners.py` with these scikit-learn transformers: `MissingValueImputer(strategy_config: dict)` that fits column medians (numeric) and column modes (categorical) on the training set only; `InfiniteValueReplacer` that replaces +inf with the column 99th percentile and -inf with the 1st percentile, both fitted on training; `NegativeValueClipper(non_negative_columns: list[str])` that clips identified columns to zero minimum. Each transformer implements `__sklearn_tags__` for scikit-learn 1.5 compatibility. Write unit tests for each transformer covering the edge cases: all-null column, single-value column, empty DataFrame.
> **📦 Stack:** scikit-learn 1.5, numpy, pandas, joblib, pytest
> **┅ Outcome:** All three transformers pass scikit-learn's `check_estimator()` validation. Fitted parameters are accessible as attributes (e.g., `imputer.fill_values_`). The test suite covers all edge cases.

#### Subphase 15.2 — Cleaning Transformer: Duplicates & Outliers

> **🎭 Role:** Senior ML Engineer
> **📍 Context:** Duplicate removal must be training-only. Outlier clipping preserves extreme attack values rather than removing them, because extreme network statistics are often genuine attack signals.
> **🔧 Task:** Implement two more transformers in `cleaners.py`. `DuplicateRemover(subset: list[str] | None = None)` that removes exact duplicate rows only during `fit_transform` on training data; the `transform` method (applied to validation/test) is a no-op that logs a warning if duplicates are found. `IQROutlierClipper(multiplier: float = 1.5)` that computes per-column IQR on the training set, clips to [Q1 - k·IQR, Q3 + k·IQR] bounds, and fits those bounds for production reuse. Log the number of duplicates removed and the number of clipped values per column to MLflow.
> **📦 Stack:** scikit-learn 1.5, numpy, pandas, mlflow
> **┅ Outcome:** `DuplicateRemover().fit_transform(train_df)` removes duplicates. `DuplicateRemover().transform(test_df)` returns unchanged test data with a logged warning if duplicates found.

#### Subphase 15.3 — Cleaning Pipeline Composition

> **🎭 Role:** Senior ML Engineer
> **📍 Context:** Individual transformers exist. Composing them into a single serialisable scikit-learn Pipeline object completes the cleaning stage and enables DVC caching.
> **🔧 Task:** Compose all cleaning transformers into a single scikit-learn `Pipeline` object in `ml/src/preprocessing/cleaning_pipeline.py`. Pipeline order: DuplicateRemover → InfiniteValueReplacer → NegativeValueClipper → MissingValueImputer → IQROutlierClipper. Load the transformer configurations from the dataset's EDA findings YAML. Fit the pipeline on the training split only. Serialise the fitted pipeline using `joblib.dump` to `ml/artifacts/pipelines/cleaning_pipeline_{dataset}_{version}.pkl`. Log the serialised path, pipeline version, and all fitted parameters to MLflow as a run artifact.
> **📦 Stack:** scikit-learn, joblib, mlflow, PyYAML
> **┅ Outcome:** The fitted pipeline can be loaded with `joblib.load` and correctly transforms new data. The MLflow run artifact shows the pipeline file.

#### Subphase 15.4 — Cleaning Pipeline Test Suite

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** The cleaning pipeline is the foundation of all ML experiments. Regressions here corrupt every downstream result. The test suite must be comprehensive and fast.
> **🔧 Task:** Write `ml/tests/test_cleaning_pipeline.py`. Use `factory-boy` to generate synthetic DataFrames with known data quality issues. Test: (1) Pipeline removes exactly N duplicates from the training set and 0 from the test set; (2) Infinite values are replaced with the correct percentile values fitted on training; (3) Negative values in non-negative columns are clipped to 0; (4) Missing values are imputed with training medians (not test medians); (5) The serialised and deserialised pipeline produces byte-identical output to the original; (6) The pipeline raises `ValueError` when `transform` is called before `fit`. Achieve 100% branch coverage on all transformer classes.
> **📦 Stack:** pytest, factory-boy, pandas, numpy, joblib
> **┅ Outcome:** All tests pass. `coverage report` shows 100% branch coverage for `cleaners.py`.

---

## Phase 16 — Encoding & Scaling Pipeline

**Context:** Convert cleaned data into the numeric feature matrices required by all six model families. All fitted parameters must be serialised for production reuse.

#### Subphase 16.1 — Categorical Encoding

> **🎭 Role:** Senior ML Engineer with feature engineering expertise
> **📍 Context:** Categorical features (protocol type, TCP flags, service type) must be converted to numeric. The encoding strategy balances information preservation with model compatibility.
> **🔧 Task:** Implement `ml/src/preprocessing/encoders.py`. `OrdinalEncoder(columns: list[str])` for low-cardinality categoricals (cardinality ≤ 20) that maps each unique value to an integer and stores the mapping for production. `HashEncoder(columns: list[str], n_components: int = 16)` for high-cardinality categoricals (cardinality > 20) using sklearn's `FeatureHasher` with consistent output dimensions. `LabelEncoder(taxonomy_mapping: dict)` that maps attack class strings to integer indices using the unified taxonomy and is the single source of truth for the class→integer mapping used in all six model training scripts. Each encoder is scikit-learn compatible.
> **📦 Stack:** scikit-learn 1.5, pandas, numpy
> **┅ Outcome:** `LabelEncoder().transform(["DDOS", "NORMAL"])` returns `[0, 6]` (consistent integers). The ordinal mapping is accessible as an attribute for SHAP explanation feature names.

#### Subphase 16.2 — Feature Scaling

> **🎭 Role:** Senior ML Engineer
> **📍 Context:** Network security data contains extreme outliers from attack traffic. Standard scaling is distorted by these outliers. RobustScaler is the correct choice and must be fitted on training data only.
> **🔧 Task:** Implement `RobustFeatureScaler` in `encoders.py` wrapping `sklearn.preprocessing.RobustScaler`. The wrapper: validates that the scaler is fitted before transforming (raises `NotFittedError` otherwise), logs the median and IQR per feature to MLflow after fitting, implements `inverse_transform` for debugging, and includes an `exclude_columns` parameter for features that should not be scaled (e.g., binary indicator features). Write unit tests confirming the training set median maps to 0.0 after scaling.
> **📦 Stack:** scikit-learn, mlflow, numpy
> **┅ Outcome:** `RobustFeatureScaler().fit_transform(X_train)` produces a scaled matrix where the median of each column is approximately 0.0. Applying it to `X_test` uses the training medians.

#### Subphase 16.3 — Full Preprocessing Pipeline

> **🎭 Role:** Senior ML Engineer
> **📍 Context:** Cleaning and encoding are separate pipeline stages in DVC. Within the Python code they are composed into a single ColumnTransformer for efficient application.
> **🔧 Task:** Implement the full preprocessing pipeline in `ml/src/preprocessing/full_pipeline.py` using `sklearn.compose.ColumnTransformer`. The transformer applies: OrdinalEncoder to low-cardinality categoricals, HashEncoder to high-cardinality categoricals, RobustFeatureScaler to numeric features, passthrough for binary features. Chain it after the cleaning pipeline using sklearn `Pipeline`. Serialise the complete fitted pipeline to `ml/artifacts/pipelines/full_pipeline_{dataset}_{version}.pkl`. Log the output feature dimension, feature names list, and the artifact path to MLflow.
> **📦 Stack:** scikit-learn, joblib, mlflow
> **┅ Outcome:** The pipeline output is a 2D float32 NumPy array with `len(feature_names)` columns. The feature names list is stored as a pipeline attribute for SHAP explanation labels.

#### Subphase 16.4 — Train/Validation/Test Split

> **🎭 Role:** ML Research Engineer
> **📍 Context:** The split strategy must prevent data leakage, be reproducible given the same seed, and handle the temporal ordering required for BETH.
> **🔧 Task:** Implement `ml/src/preprocessing/splitter.py`. For NSL-KDD: use the official KDDTrain+/KDDTest+ split (not random). For CICIDS-2017 and UNSW-NB15: use stratified random split with ratio 70/15/15. For BETH: use temporal split (train=first 70% by timestamp, val=next 15%, test=last 15%) to prevent future leakage. Accept a `random_seed` parameter. Save splits as compressed NumPy arrays (`.npz`) to the DVC-tracked splits directory. Log split sizes and class distributions per split to MLflow.
> **📦 Stack:** scikit-learn, numpy, mlflow
> **┅ Outcome:** The BETH temporal split preserves chronological order. NSL-KDD uses the official split. All three splits are saved as `.npz` files.

#### Subphase 16.5 — Encoding Pipeline Tests

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** Encoding errors silently corrupt model training. Test coverage must be comprehensive.
> **🔧 Task:** Write `ml/tests/test_encoding_pipeline.py`. Test: (1) Categorical encoding produces integer output for all categories seen during training; (2) An unseen category at inference time is handled gracefully (hash encoding) or raises a clear error (ordinal encoding, which must be caught and defaulted); (3) Numeric scaling applies training medians to test data; (4) The full pipeline output has no NaN values; (5) The pipeline is deterministic — same input produces identical output on repeated calls; (6) The BETH temporal split test set contains only timestamps after the validation set. Achieve ≥90% branch coverage.
> **📦 Stack:** pytest, numpy, pandas, factory-boy
> **┅ Outcome:** All encoding tests pass. The coverage threshold is enforced in CI.

---

## Phase 17 — Class Imbalance Handling

**Context:** Recall on minority attack classes is the safety-critical metric. Without proper imbalance handling, models achieve high accuracy by predicting the majority (BENIGN) class and produce dangerously low recall on actual attacks.

#### Subphase 17.1 — Imbalance Severity Analysis Module

> **🎭 Role:** Senior ML Engineer specialising in imbalanced learning
> **📍 Context:** The imbalance ratio varies dramatically per dataset and per attack class. SMOTE parameters must be computed automatically from the measured ratios, not hardcoded.
> **🔧 Task:** Implement `ml/src/preprocessing/imbalance.py`. `ImbalanceAnalyser` class: given a label array, computes per-class imbalance ratio (majority count / class count), identifies classes below the target ratio threshold, computes SMOTE oversampling targets to reach a configurable maximum imbalance ratio (default 10:1), and returns a `SamplingConfig` dataclass with `oversampling_targets: dict[int, int]`, `undersampling_target: int`, `minority_classes: list[int]`. Log the before/after class distribution to MLflow.
> **📦 Stack:** imbalanced-learn 0.12, numpy, mlflow
> **┅ Outcome:** `ImbalanceAnalyser(target_ratio=10).analyse(y_train)` returns a `SamplingConfig` with the correct targets. Logging shows the before/after class distribution in MLflow.

#### Subphase 17.2 — SMOTE Oversampling

> **🎭 Role:** Senior ML Engineer
> **📍 Context:** SMOTE generates synthetic minority class samples by interpolating between real samples in feature space. It must be applied only to training data, never to validation or test sets.
> **🔧 Task:** Implement `SMOTEResampler` in `imbalance.py` using `imbalanced-learn`'s `SMOTE` with `k_neighbors=5`. The resampler accepts a `SamplingConfig` from the analyser and applies the computed oversampling targets. Implement a guard that raises `ValueError` if called with a dataset flagged as test or validation. After resampling, verify that no synthetic sample is an exact duplicate of a real sample (assert). Log: number of synthetic samples generated per class, total training set size before/after, class distribution after resampling.
> **📦 Stack:** imbalanced-learn, numpy, mlflow
> **┅ Outcome:** `SMOTEResampler().fit_resample(X_train, y_train, config)` produces a balanced training set. The no-duplicates assertion passes. The guard raises on test data.

#### Subphase 17.3 — Class Weight Alternative

> **🎭 Role:** Senior ML Engineer
> **📍 Context:** SMOTE adds computational cost and creates synthetic samples. Class weights are simpler and work natively in scikit-learn and XGBoost. Both strategies are evaluated in the model comparison.
> **🔧 Task:** Implement `ClassWeightCalculator` in `imbalance.py`. Compute class weights inversely proportional to class frequency: `weight_i = n_samples / (n_classes * count_i)`. Return a dict mapping class integer to weight, compatible with `sklearn`'s `class_weight` parameter and XGBoost's `scale_pos_weight`. Also compute the XGBoost `scale_pos_weight` for binary classification (sum of negative / sum of positive). Log all computed weights to MLflow.
> **📦 Stack:** numpy, sklearn, mlflow
> **┅ Outcome:** `ClassWeightCalculator().compute(y_train)` returns a dict. Passing this dict to `LogisticRegression(class_weight=weights)` is equivalent to manually upsampling minority classes.

#### Subphase 17.4 — Resampling Tests

> **🎭 Role:** Test Engineer
> **📍 Context:** Resampling bugs silently cause data leakage from test to train. Guard tests are critical.
> **🔧 Task:** Write `ml/tests/test_imbalance.py`. Test: (1) SMOTE increases minority class counts to within 10% of the target ratio; (2) SMOTE applied to training data changes class counts; (3) SMOTE raises `ValueError` when `is_test=True` flag is set; (4) No synthetic SMOTE sample is an exact duplicate of a real training sample; (5) Class weights sum to `n_classes` (sklearn convention); (6) The resampling is reproducible given the same random seed; (7) The combined strategy (SMOTE + undersampling) produces a final class distribution within the target range.
> **📦 Stack:** pytest, numpy, factory-boy
> **┅ Outcome:** All 7 tests pass. The SMOTE guard test is the most important: it prevents the most catastrophic data leakage bug.

#### Subphase 17.5 — Preprocessing Integration Test

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** The full preprocessing pipeline (cleaning → encoding → splitting → resampling) must work end-to-end on real data before any model training begins.
> **🔧 Task:** Write `ml/tests/test_preprocessing_integration.py` that runs the full preprocessing pipeline on a 1000-row sample of real CICIDS-2017 data (loaded from the DVC-tracked fixture dataset). Verify: (1) The pipeline completes without error; (2) The output feature matrix has the correct shape `(n_samples, n_features)`; (3) No NaN or infinite values in the output; (4) The label array contains only valid taxonomy integer values; (5) SMOTE increases the training set size; (6) The test set is untouched by resampling; (7) The fitted pipeline can be serialised and deserialised with joblib and produces identical output. Run this test as part of the CI ML pipeline workflow.
> **📦 Stack:** pytest, joblib, numpy, pandas
> **┅ Outcome:** The integration test passes in CI using the DVC fixture dataset. Any breaking change to the pipeline is caught before it reaches the training phase.

---

## Phase Map

| Phase | Title | Subphases |
|-------|-------|-----------|
| P9 | Dataset Strategy & Acquisition | 5 |
| P10 | NSL-KDD EDA | 4 |
| P11 | CICIDS-2017 EDA | 5 |
| P12 | UNSW-NB15 EDA | 4 |
| P13 | BETH EDA | 4 |
| P14 | Cross-Dataset Schema Mapping | 4 |
| P15 | Data Cleaning Pipeline | 4 |
| P16 | Encoding & Scaling Pipeline | 5 |
| P17 | Class Imbalance Handling | 5 |

**Previous ←** [01 — Project Foundation](01-project-foundation.md) | **Next →** [03 — Feature Engineering & Experiment Tracking](03-data-engineering.md)

---
