# 02 — Data Engineering

> **Phases 9–17** | Dataset acquisition, exploratory data analysis across four datasets, cross-dataset schema mapping, preprocessing pipeline, encoding, scaling, and class imbalance handling.
>
> **How to use:** Pick one subphase. Copy its **Prompt** into your AI code editor. Implement it. Move to the next subphase.

---

## Phase 9 — Dataset Strategy & Acquisition

**Context:** Define where the four benchmark datasets come from, how they are stored, and how data integrity is verified before any analysis begins.

#### Subphase 9.1 — Dataset Download Plan
> **Prompt:** Write the dataset acquisition plan for XAI-Guard. Document the official download sources and direct URLs for NSL-KDD, CICIDS-2017, UNSW-NB15, and BETH. Include the SHA-256 checksums to verify download integrity, the expected file sizes, and the license terms for each dataset. The plan should be a runnable reference that any developer can follow to reproduce the exact data used in the research.

#### Subphase 9.2 — Data Directory Structure & Gitignore
> **Prompt:** Define the data directory structure for the XAI-Guard ML module. Raw downloaded data goes into one directory, cleaned intermediate data into another, fully processed feature matrices into a third, and train/test splits into a fourth. All data directories must be excluded from git via .gitignore because they will be tracked by DVC instead. Document this structure so all ML pipeline stages write their outputs to the correct location.

#### Subphase 9.3 — Automated Download Script
> **Prompt:** Create an automated dataset download script for XAI-Guard that downloads all four datasets from their official sources, verifies each file's SHA-256 checksum, extracts archives where necessary, and reports success or failure for each dataset. The script should be idempotent — re-running it skips already-downloaded and verified files.

#### Subphase 9.4 — Data Validation Baseline
> **Prompt:** Create a data validation script for XAI-Guard that runs immediately after download and produces a baseline quality report for each raw dataset. The report should record: total row count, column count, null count per column, duplicate row count, class label distribution, and any columns containing infinite values. This baseline is compared at every subsequent pipeline stage to catch regressions.

#### Subphase 9.5 — DVC Data Tracking Setup
> **Prompt:** Set up DVC tracking for the XAI-Guard datasets immediately after the initial download. Add all four raw dataset directories to DVC tracking, configure the DVC remote to point to the MinIO artifact store bucket, and push the initial data version. Commit the DVC pointer files to git and tag this initial state as data-v1.0. This establishes the reproducibility baseline for all future experiments.

---

## Phase 10 — NSL-KDD Exploratory Data Analysis

**Context:** NSL-KDD is the established IDS benchmark used to set the performance baseline. Understanding its characteristics before training prevents common mistakes like using its known train/test distribution mismatch naively.

#### Subphase 10.1 — Dataset Loading & Profiling
> **Prompt:** Create a Jupyter notebook for NSL-KDD exploratory data analysis in XAI-Guard. Load the KDDTrain+ and KDDTest+ files, display the schema with data types, count nulls and duplicates, and generate a full statistical profile of all 41 features using ydata-profiling. The profiling report should be saved as an HTML artifact for reference.

#### Subphase 10.2 — Class Distribution Analysis
> **Prompt:** Extend the NSL-KDD EDA notebook with a class distribution analysis. Visualise the attack category distribution in both the training set and the test set using bar charts. Compute the ratio of each attack type to the total. Document the known train/test distribution mismatch: NSL-KDD test set contains novel attack subtypes not present in training, which is a key research challenge this project addresses.

#### Subphase 10.3 — Feature Correlation Analysis
> **Prompt:** Add feature correlation analysis to the NSL-KDD EDA notebook. Compute and visualise the Pearson correlation matrix for all numeric features. Identify feature pairs with absolute correlation above 0.95 as candidates for removal during feature selection. Plot the top 20 features by variance and the top 20 by mutual information with the attack label.

#### Subphase 10.4 — Attack Category Breakdown
> **Prompt:** Add an attack category breakdown section to the NSL-KDD EDA notebook. NSL-KDD has four attack categories: DoS, Probe, R2L, and U2R. Map these to the XAI-Guard unified attack taxonomy defined in Phase 1. Visualise the sample counts per category and per specific attack subtype. Identify which subtypes have fewer than 100 training samples as they may cause poor per-class recall.

#### Subphase 10.5 — EDA Findings Documentation
> **Prompt:** Add a findings and conclusions section to the NSL-KDD EDA notebook. Summarise: the three most important data quality observations, the features identified for potential removal, the class imbalance severity, the train/test mismatch implications, and the recommended preprocessing decisions specific to NSL-KDD. These findings directly inform the preprocessing pipeline in Phases 15 and 16.

---

## Phase 11 — CICIDS-2017 Exploratory Data Analysis

**Context:** CICIDS-2017 is the primary training dataset — the most realistic and the most challenging due to severe class imbalance. Understanding its quirks is critical for model quality.

#### Subphase 11.1 — Dataset Loading & Profiling
> **Prompt:** Create a Jupyter notebook for CICIDS-2017 exploratory data analysis. Load all daily capture CSV files, concatenate them into a single DataFrame, display schema and statistics, and profile the dataset using ydata-profiling. Pay specific attention to columns containing NaN, infinity values, and negative values that are invalid for network flow features.

#### Subphase 11.2 — Class Imbalance Analysis
> **Prompt:** Add class imbalance analysis to the CICIDS-2017 EDA notebook. Compute the ratio of the majority class (BENIGN traffic) to each minority class. Visualise the distribution on both linear and log scales. Identify the most severely underrepresented attack classes and document the exact oversampling ratios that SMOTE will need to apply to reach a usable class balance.

#### Subphase 11.3 — Data Quality Investigation
> **Prompt:** Add a data quality investigation section to the CICIDS-2017 EDA notebook. Identify and count all rows containing infinite values. Identify columns with very high null rates. Identify columns that are constant across the entire dataset. Identify duplicate rows. For each issue, document the recommended remediation action that will be implemented in the cleaning pipeline.

#### Subphase 11.4 — Temporal Pattern Analysis
> **Prompt:** Add temporal pattern analysis to the CICIDS-2017 EDA notebook. CICIDS-2017 spans five capture days (Monday through Friday) with different attack types on each day. Plot the event count per hour and attack type distribution per capture day. Identify whether attack patterns change significantly across days, as this temporal variation is what the BETH dataset uses to test drift robustness.

#### Subphase 11.5 — Feature Multicollinearity Analysis
> **Prompt:** Add feature multicollinearity analysis to the CICIDS-2017 EDA notebook. CICIDS-2017 has 78 features, many of which are redundant combinations of the same underlying network statistics. Compute a correlation matrix and identify clusters of highly correlated features. Recommend which features from each correlated cluster to retain based on individual mutual information with the label. This reduces the feature space while preserving predictive power.

---

## Phase 12 — UNSW-NB15 Exploratory Data Analysis

**Context:** UNSW-NB15 covers nine modern attack types not all present in NSL-KDD. Its role is to test whether models trained on CICIDS-2017 generalise to a different attack taxonomy.

#### Subphase 12.1 — Dataset Loading & Profiling
> **Prompt:** Create a Jupyter notebook for UNSW-NB15 exploratory data analysis. Load all four CSV partition files and their ground-truth labels file, merge them into a unified DataFrame, display the schema and feature statistics, and generate a profiling report. UNSW-NB15 includes both a training set and a test set partitioned differently from NSL-KDD — document their sizes and label distributions separately.

#### Subphase 12.2 — Attack Category Taxonomy Mapping
> **Prompt:** Add attack category mapping to the UNSW-NB15 EDA notebook. UNSW-NB15 has nine attack categories: Fuzzers, Analysis, Backdoors, DoS, Exploits, Generic, Reconnaissance, Shellcode, and Worms. Map each category to the XAI-Guard unified attack taxonomy from Phase 1. Visualise the sample count per category and document any categories that have no equivalent in the unified taxonomy.

#### Subphase 12.3 — Feature Distribution Analysis
> **Prompt:** Add feature distribution analysis to the UNSW-NB15 EDA notebook. For each of the 49 features, visualise the distribution separated by benign vs malicious label. Identify features where the two distributions are clearly separable — these are high-value features. Identify features where distributions completely overlap — these are candidates for removal during feature selection.

#### Subphase 12.4 — Near-Zero Variance Detection
> **Prompt:** Add near-zero variance feature detection to the UNSW-NB15 EDA notebook. Compute the variance of every numeric feature and identify those below a threshold of 0.01 as candidates for removal. Also identify categorical features where one value accounts for more than 99% of rows. Document the list of features flagged for removal and the rationale.

---

## Phase 13 — BETH Dataset Exploratory Data Analysis

**Context:** BETH is real honeypot data from an enterprise environment. Its role is to test drift robustness and temporal generalisation. Its feature set is different from the other three datasets.

#### Subphase 13.1 — Dataset Loading & Temporal Overview
> **Prompt:** Create a Jupyter notebook for BETH dataset exploratory data analysis. Load the BETH dataset, display the schema and the 14 available features, and create a timeline visualisation showing event count per hour across the full capture period. BETH spans multiple weeks, making it the only dataset in XAI-Guard with significant temporal extent. Document the capture period start and end dates.

#### Subphase 13.2 — Label Distribution Over Time
> **Prompt:** Add temporal label distribution analysis to the BETH EDA notebook. Plot the ratio of malicious to benign events per day and per week across the full capture period. Identify time windows where the malicious event rate changes significantly, as these represent natural drift events. Document these time windows as they will be used to simulate temporal drift in the robustness testing phase.

#### Subphase 13.3 — Feature Availability & Schema Gap Analysis
> **Prompt:** Add a feature availability and schema gap analysis to the BETH EDA notebook. BETH has only 14 features compared to 41-78 in the other datasets. Map the 14 BETH features to the XAI-Guard unified event schema from Phase 14. Document which unified schema features have no BETH equivalent and how this gap will be handled: either imputing zeros, imputing the training set mean, or excluding BETH from experiments that require those features.

#### Subphase 13.4 — Drift Characterisation
> **Prompt:** Add a drift characterisation section to the BETH EDA notebook. For each feature, plot the distribution in the first week of capture versus the last week. Compute the statistical distance (KL divergence or Wasserstein distance) between these two distributions per feature. Identify the features with the highest drift magnitude. These are the features the drift detector will be most sensitive to.

---

## Phase 14 — Cross-Dataset Schema Mapping

**Context:** All four datasets must be normalised to the same unified feature schema before any model can be trained across them. This mapping is the foundation of the fair multi-dataset comparison.

#### Subphase 14.1 — Unified Event Schema Finalisation
> **Prompt:** Finalise the unified security event schema for XAI-Guard based on the EDA findings from Phases 10-13. The schema should include fields present in at least three of the four datasets. Document each field: its name in the unified schema, its data type, its meaning, and the valid range. For fields absent in some datasets, document the imputation strategy. Save this as a YAML schema definition file that the preprocessing pipeline validates against.

#### Subphase 14.2 — Dataset Column Mapping Configuration
> **Prompt:** Create the column mapping configuration files for XAI-Guard. For each of the four datasets, create a YAML file that maps each dataset's native column names to the unified schema field names. Include the data type coercion rules for each mapping and flag any fields that require computation from multiple source columns. These mapping files are loaded by the preprocessing pipeline to handle each dataset generically.

#### Subphase 14.3 — Schema Mapping Validation Tests
> **Prompt:** Write automated tests for the XAI-Guard dataset column mappings. For each dataset's mapping configuration, the test should: load a sample of raw data, apply the mapping, and validate that the output conforms to the unified schema with correct column names, data types, and no unexpected null values. The tests serve as a regression guard when the schema or mappings are updated.

#### Subphase 14.4 — Dataset Statistics Summary Report
> **Prompt:** Create the unified dataset statistics summary notebook for XAI-Guard that aggregates findings from all four EDA notebooks. Produce a comparison table showing: dataset name, record count, feature count after mapping, null rate, duplicate rate, class distribution, and the key preprocessing challenge for each. This summary is referenced in the research paper methodology section.

---

## Phase 15 — Data Cleaning Pipeline

**Context:** Build the first stage of the reproducible preprocessing pipeline: a cleaning module that handles all data quality issues identified in the EDA phases.

#### Subphase 15.1 — Missing Value Handling
> **Prompt:** Implement the missing value handler for the XAI-Guard data cleaning pipeline. Numeric missing values are imputed with the column median computed on the training set only and then applied to validation and test sets. Categorical missing values are imputed with the column mode. The fitted imputation values are serialised so the exact same values are applied at inference time in production.

#### Subphase 15.2 — Duplicate Row Removal
> **Prompt:** Implement the duplicate row removal step for the XAI-Guard data cleaning pipeline. Remove exact duplicate rows based on all feature columns excluding the timestamp. Log the number of duplicates removed per dataset to MLflow as a preprocessing metric. Apply this step only to training data — test sets are never deduplicated as that would inflate test metrics.

#### Subphase 15.3 — Infinite & Invalid Value Replacement
> **Prompt:** Implement the infinite and invalid value replacement step for the XAI-Guard data cleaning pipeline. Replace positive infinity values with the column's 99th percentile value and negative infinity values with the column's 1st percentile value, both computed on the training set. Replace any negative values in features that are inherently non-negative (byte counts, packet counts, durations) with zero.

#### Subphase 15.4 — Outlier Clipping Strategy
> **Prompt:** Implement the outlier clipping step for the XAI-Guard data cleaning pipeline. Use the IQR method with a multiplier of 1.5 to compute upper and lower bounds per feature on the training set. Clip values to these bounds rather than removing rows, because in security data extreme values are often genuine attack signals and removing them would cause information loss.

#### Subphase 15.5 — Cleaning Pipeline Composition
> **Prompt:** Compose all cleaning steps into a single scikit-learn Pipeline object for XAI-Guard. The pipeline applies steps in order: duplicate removal, infinite value replacement, missing value imputation, and outlier clipping. The fitted pipeline is serialised with joblib to a versioned artifact file. Log the pipeline version and all fitted parameter summaries to MLflow.

#### Subphase 15.6 — Cleaning Pipeline Tests
> **Prompt:** Write unit tests for every cleaning step in the XAI-Guard preprocessing pipeline. For each transformer, test that it correctly handles: all-null columns, no-null columns, columns with only one unique value, columns with extreme outliers, and an empty DataFrame. Test the full pipeline composition end-to-end with a synthetic DataFrame that has all of the above issues simultaneously. All tests must pass without raising exceptions.

---

## Phase 16 — Encoding & Scaling Pipeline

**Context:** Convert cleaned data into the numeric feature matrices required by ML models. Build this as the second pipeline stage, compatible with the output of the cleaning pipeline.

#### Subphase 16.1 — Categorical Encoding
> **Prompt:** Implement the categorical feature encoder for XAI-Guard. Use ordinal encoding for low-cardinality categorical features (protocol type, TCP flags, service type). For high-cardinality categorical features, use a hash encoder with a fixed output dimension to prevent dimensionality explosion. The encoder must be fitted on training data only and then applied identically to validation, test, and production inference data.

#### Subphase 16.2 — Numeric Feature Scaling
> **Prompt:** Implement the numeric feature scaler for XAI-Guard. Use RobustScaler as the primary scaler because network security data contains extreme outliers from attack traffic that would skew StandardScaler's mean and variance. RobustScaler uses median and IQR, making it resistant to outliers. Fit the scaler on training data only and serialize the fitted scaler with all other pipeline artifacts.

#### Subphase 16.3 — Label Encoding
> **Prompt:** Implement the label encoder for XAI-Guard that maps the unified attack taxonomy string labels to integer class indices. Create a consistent class-to-index mapping that is identical across all datasets and all models. Serialise the mapping so that the same integer labels are used at training time, evaluation time, and inference time. Log the class mapping to MLflow as a run artifact.

#### Subphase 16.4 — Full Preprocessing Pipeline Composition
> **Prompt:** Compose the complete XAI-Guard preprocessing pipeline by chaining the cleaning pipeline from Phase 15 with the encoding and scaling steps from Phase 16. The pipeline produces the final feature matrix ready for model training. Define the two output modes: tabular output for classical ML models and a flag that enables sequence construction for LSTM and Transformer models. Serialise the full fitted pipeline as a versioned artifact.

#### Subphase 16.5 — Encoding Pipeline Tests
> **Prompt:** Write unit tests for the XAI-Guard encoding and scaling pipeline. Test that: categorical features are correctly encoded to integers; numeric features are scaled such that the training set median maps to zero; the full pipeline output has no NaN values; the pipeline produces identical output when applied to the same input twice; and the pipeline can be serialised and deserialised with joblib without losing any fitted state.

---

## Phase 17 — Class Imbalance Handling

**Context:** Security datasets are severely imbalanced: benign traffic vastly outnumbers attack traffic. Without handling this, models optimise for the majority class and produce poor recall on attacks — which is the most safety-critical metric.

#### Subphase 17.1 — Imbalance Severity Analysis
> **Prompt:** Create an imbalance severity analysis module for XAI-Guard that quantifies the class imbalance ratio for each dataset after preprocessing. Compute the imbalance ratio as the count of the majority class divided by the count of each minority class. Log these ratios to MLflow. Use these ratios to automatically configure SMOTE and undersampling parameters for each dataset independently.

#### Subphase 17.2 — SMOTE Oversampling Implementation
> **Prompt:** Implement SMOTE oversampling for XAI-Guard using imbalanced-learn. Apply SMOTE only to the training split, never to validation or test sets. Configure k_neighbors=5 as the default and use the automatically computed ratios from the severity analysis to determine the target class distribution. Log the before and after class counts to MLflow so the effect of oversampling is tracked per experiment.

#### Subphase 17.3 — Majority Class Undersampling
> **Prompt:** Implement majority class undersampling for XAI-Guard as a complement to SMOTE. RandomUnderSampler reduces the majority class to a target ratio after SMOTE has boosted minority classes. Configure the combined resampling strategy so the final training class distribution achieves the target balance while retaining as many majority-class samples as possible. The combined strategy is applied as a single step after the full preprocessing pipeline.

#### Subphase 17.4 — Resampling Strategy Tests
> **Prompt:** Write tests for the XAI-Guard class resampling strategy. Verify that: SMOTE is never applied to the test set; the output class distribution after combined resampling is within the target ratio range; SMOTE does not create exact duplicates of existing samples; and the resampling step is reproducible given the same random seed. Log the random seed used to MLflow for full reproducibility.

#### Subphase 17.5 — Class Weight Alternative Strategy
> **Prompt:** Implement a class weight alternative strategy for XAI-Guard as a comparison to resampling. Compute class weights inversely proportional to class frequency and apply them to models that support sample weighting natively: scikit-learn classifiers via the class_weight parameter and XGBoost via scale_pos_weight. This provides a second approach to imbalance handling whose results can be compared against SMOTE in the model evaluation phase.

---

## Phase Map

| Phase | Title | Subphases |
|-------|-------|-----------|
| P9 | Dataset Strategy & Acquisition | 5 |
| P10 | NSL-KDD EDA | 5 |
| P11 | CICIDS-2017 EDA | 5 |
| P12 | UNSW-NB15 EDA | 4 |
| P13 | BETH EDA | 4 |
| P14 | Cross-Dataset Schema Mapping | 4 |
| P15 | Data Cleaning Pipeline | 6 |
| P16 | Encoding & Scaling Pipeline | 5 |
| P17 | Class Imbalance Handling | 5 |

**Previous ←** [01 — Project Foundation](01-project-foundation.md) | **Next →** [03 — Feature Engineering & Experiment Tracking](03-data-engineering.md)
