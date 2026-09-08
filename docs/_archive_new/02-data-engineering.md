# 02 — Data Engineering

> **Phases 9–17** | Dataset acquisition, EDA across four benchmark datasets, cross-dataset schema mapping, cleaning pipeline, encoding, scaling, and class imbalance handling.

## 🗺️ Research Paper Map

Every phase in this document produces a specific artefact that maps directly to your research paper:

| Phase | What You Build | Paper Section | Paper Artefact |
|-------|---------------|---------------|----------------|
| P9 | Download + validate 4 datasets | §3 Datasets | Table 1: Dataset Statistics |
| P10 | NSL-KDD EDA | §3.1 NSL-KDD | Fig 1a: Class Distribution |
| P12 | UNSW-NB15 EDA | §3.3 UNSW-NB15 | Fig 1c, EMD ranking table |
| P13 | BETH EDA | §3.4 BETH | Fig 1d, drift windows |
| P14 | Cross-dataset schema | §3.5 Unified Schema | Table 2: Feature Schema |
| P15 | Cleaning pipeline | §4.1 Preprocessing | Reproducibility statement |
| P16 | Encoding + splitting | §4.1 Preprocessing | Train/val/test sizes |
| P17 | Imbalance handling | §4.1 Preprocessing | SMOTE rationale paragraph |

> **How to use this doc:** Read the 📖 Concept section before each phase. Complete the ✅ Learning Checkpoint before moving on. Every figure you generate here should be saved to `ml/notebooks/figures/` — they go directly into your paper.

---

---

## Phase 9 — Dataset Strategy & Acquisition

**Context:** Establish the data foundation before any analysis. Incorrect or corrupted data invalidates all downstream experiments.

### 🎓 What You Will Learn in Phase 9


This is equivalent to citing the exact URL and checksum of a dataset in your paper's footnote, but enforced programmatically. It eliminates the classic reproducibility failure: "I can't reproduce your results because the download URL changed."

### ⚠️ Common Mistakes — Dataset Acquisition
- **Not verifying checksums**: If the download is corrupted or the dataset was updated, your results will differ from the literature. Always verify SHA-256.



#### Subphase 9.1 — Dataset Download & Integrity Verification

> **🎭 Role:** Senior Data Engineer and ML Research Infrastructure Engineer
> **📍 Context:** The XAI-Guard evaluation framework (Phase 1) requires four benchmark datasets. Nothing has been downloaded yet. All ML experiments depend on exactly these versions of these datasets.
> **📦 Stack:** httpx, rich, typer, mlflow 2.x, hashlib (stdlib)




> **🔧 Task:** Write `ml/dvc.yaml` defining pipeline stages with explicit `deps`, `outs`, `params`, and `metrics` declarations: `download` stage (deps: download script; outs: raw/ directories); `clean` stage (deps: raw/ + cleaning script; outs: interim/; metrics: cleaning_report.json); `encode` stage (deps: interim/ + encoding script; outs: processed/; params: ml/configs/preprocessing.yaml); `features` stage (deps: processed/ + feature engineering scripts; outs: features/); `select` stage (deps: features/ + selection config; outs: selected/); `split` stage (deps: selected/; outs: splits/train, splits/val, splits/test). Configure `dvc params` to track all hyperparameters from YAML configs.
> **📦 Stack:** dvc[s3] 3.51, PyYAML
> **✅ Outcome:** `dvc repro` runs the full pipeline from scratch. Modifying `ml/configs/preprocessing.yaml` causes only the `encode` stage and its descendants to re-run. `dvc dag` shows the correct pipeline graph.

#### Subphase 9.4 — Data Validation Schema

> **🎭 Role:** Data Quality Engineer
> **✅ Outcome:** `uv run python ml/src/data/validate.py --dataset cicids2017` produces a validation report. A corrupted dataset causes a clear, actionable error message that identifies the failing column and check.

#### Subphase 9.5 — Data Directory Structure & Gitignore

> **🎭 Role:** ML Infrastructure Engineer
> **📍 Context:** A clean, documented directory structure prevents data files from being committed to git and ensures all pipeline stages write outputs to the correct location.
> **📦 Stack:** pydantic-settings, pathlib (stdlib)
> **✅ Outcome:** `DataPaths().raw_dir / "cicids2017"` resolves to the correct path. `git status` shows no data files. `dvc pull` populates all directories.

#### Subphase 9.6 — Train / Validation / Test Split Strategy

> **🎓 This is the most methodologically important subphase in the entire data layer.** An incorrect split strategy is the most common reason papers fail peer review on reproducibility and fairness grounds.

> **🎭 Role:** ML Research Methodologist
> **📍 Context:** Each dataset requires a different split strategy because they have different statistical properties. Using a random split on BETH would allow future data to leak into the past, making your drift evaluation artificially optimistic. Using the official NSL-KDD split is required to compare fairly with published baselines.
> **🔧 Task:** Document and implement the split strategy for each dataset in `ml/configs/split_strategy.yaml`:
> - **NSL-KDD:** Use the official `KDDTrain+.txt` / `KDDTest+.txt` split. Do NOT re-split. This is required to compare with published NSL-KDD baselines.
> - **UNSW-NB15:** Stratified random split: 70/15/15. Seed = 42. The official train/test split is unusable (test set has a different label distribution than documented).
> - **BETH:** **Temporal split** — train = first 70% of events by `timestamp`, val = next 15%, test = last 15%. Sort by timestamp BEFORE splitting. This prevents future knowledge from leaking into the past.
>
> Document in `split_strategy.yaml`:
> ```yaml
> nslkdd:
>   strategy: official
>   train_file: KDDTrain+.txt
>   test_file: KDDTest+.txt
>   val_fraction_of_train: 0.15  # held out from training set
> cicids2017:
>   strategy: stratified_random
>   train_frac: 0.70
>   val_frac: 0.15
>   test_frac: 0.15
>   seed: 42
>   stratify_on: unified_label
> unswnb15:
>   strategy: stratified_random
>   train_frac: 0.70
>   val_frac: 0.15
>   test_frac: 0.15
>   seed: 42
> beth:
>   strategy: temporal
>   train_frac: 0.70
>   val_frac: 0.15
>   test_frac: 0.15
>   sort_column: timestamp
>   sort_order: ascending
> ```
> **📦 Stack:** pandas, scikit-learn, PyYAML
> **✅ Outcome:** `ml/configs/split_strategy.yaml` is committed. Every split is justified in your paper's §4.1 with the rationale above. Your test sets are never touched until final evaluation.

### ✅ Learning Checkpoint — Phase 9
Before moving to EDA, answer these:
2. Why must SMOTE be applied AFTER splitting, not before? What would happen to your test F1 if you applied it before?

---



## Phase 10 — NSL-KDD Exploratory Data Analysis

**Context:** NSL-KDD is the established IDS benchmark that sets the performance floor. Understanding its train/test distribution mismatch is critical to interpreting model results.

### 🎓 What You Will Learn in Phase 10
You will learn how to conduct a rigorous Exploratory Data Analysis (EDA) that produces publishable figures — not just notebook observations. The NSL-KDD EDA teaches you: statistical profiling, class distribution analysis, feature correlation, and how to document EDA decisions as structured YAML configs that drive your preprocessing pipeline.

### 📄 Research Paper Connection
All figures from this phase go into **Paper Section 3.1 (NSL-KDD Dataset)**:
- Subphase 10.2 → **Figure 1a**: Class distribution bar chart (train vs test)
- Subphase 10.2 → **Table 1, Row 1**: Dataset statistics (rows, features, classes, imbalance ratio)
- Subphase 10.3 → **Figure 2a**: Feature correlation heatmap

### 📖 Concept: Jensen-Shannon Divergence
The Jensen-Shannon (JS) divergence measures how different two probability distributions are. In Subphase 10.2, you measure how different the attack class distribution is between NSL-KDD's training set and its test set.

Formula: `JS(P || Q) = 0.5 × KL(P || M) + 0.5 × KL(Q || M)` where `M = 0.5 × (P + Q)` and KL is the Kullback-Leibler divergence.

JS divergence is bounded [0, 1] (when using log base 2), making it easy to interpret:
- JS = 0.0 → identical distributions (train and test look the same)
- JS > 0.3 → significant distribution mismatch — models trained on this data will have lower test performance than validation performance

**Why it matters for your paper:** NSL-KDD is known to have train/test mismatch. Computing JS divergence lets you quantify this and explain in your paper why NSL-KDD test F1 scores are lower than expected.

### ⚠️ Common Mistakes — EDA
- **Only looking at overall accuracy or F1, not per-class**: A model with 97% overall accuracy can have 0% recall on the rarest attack class. Always generate per-class breakdowns.
- **Not saving figures in publication quality**: Use `plt.savefig('figure.png', dpi=300, bbox_inches='tight')`. A 72-DPI notebook screenshot is not acceptable in a paper.
- **Treating EDA as optional exploration**: Every EDA decision ("we removed features with |r| > 0.95") must be traceable to a YAML config. If you make decisions in a notebook without saving them, you can't reproduce the preprocessing later.

#### Subphase 10.1 — Dataset Loading & Statistical Profiling


> **🎭 Role:** Senior Data Scientist with IDS benchmark expertise
> **📍 Context:** NSL-KDD datasets are downloaded and validated. This EDA notebook is the first human-readable analysis of the data and informs all preprocessing decisions.
> **📦 Stack:** pandas 2.x, ydata-profiling, rich, mlflow 2.x

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

### 🎓 What You Will Learn in Phase 11

### 📄 Research Paper Connection
- Subphase 11.2 → **Figure 1b**: Class imbalance bar chart (log scale)
- Subphase 11.4 → **Figure 3**: Temporal attack distribution (feeds §4.5 Temporal Robustness)
- Subphase 11.5 → **Table 2 footnote**: Feature reduction from 78 → ~55 features

### 📖 Concept: Class Imbalance in Security Datasets

Two main strategies:
1. **SMOTE (Synthetic Minority Over-sampling Technique)**: Generates synthetic minority-class samples by interpolating between real samples in feature space. Adds training data — the model sees more attack examples.
2. **Class Weights**: Instead of adding data, you increase the loss penalty for minority class errors. The model is "punished more" for missing a rare attack than for a false alarm.

**Research implication:** You must report WHICH strategy you used and test both. Your paper's §4.1 should compare F1 with and without class balancing to justify your choice.

### ⚠️ Common Mistakes — Multi-file Loading
- **Mixing capture days without a `day` column**: Without tracking which CSV file each row came from, you cannot do the temporal analysis in Subphase 11.4.
- **Using pandas default dtype inference on large files**: Specify `dtype` explicitly for large files to avoid silent integer overflow.

#### Subphase 11.1 — Multi-File Loading & Profiling


> **🎭 Role:** Senior Data Engineer
> **📦 Stack:** pandas 2.x, numpy, ydata-profiling, mlflow 2.x
> **✅ Outcome:** The notebook loads all 8 files into a single 2.8M-row DataFrame without errors. Column names are consistent. Infinite value counts are reported per column.

#### Subphase 11.2 — Class Imbalance Severity Analysis

> **🎭 Role:** Senior Data Scientist specialising in imbalanced learning
> **📦 Stack:** pandas, matplotlib, imbalanced-learn 0.12
> **✅ Outcome:** The imbalance analysis plot is saved as `ml/notebooks/figures/cicids2017_class_imbalance.png`. The target distribution is documented for the resampling phase.

#### Subphase 11.3 — Data Quality Investigation

> **🎭 Role:** Data Quality Engineer
> **📦 Stack:** pandas, numpy
> **✅ Outcome:** The quality report CSV is committed. The YAML findings file contains a `data_quality_issues` key consumed by the cleaning pipeline.

#### Subphase 11.4 — Temporal Pattern Analysis

> **🎭 Role:** Senior Data Scientist
> **🔧 Task:** Extend the notebook with temporal analysis. Group by `capture_day` and compute: event count per day, attack type distribution per day, mean values of key features per day. Plot a stacked bar chart of attack type counts per capture day. Compute the Jensen-Shannon divergence between each pair of consecutive days' feature distributions. Identify the day pair with the largest distribution shift — this becomes the drift simulation split point. Save the split point as `temporal_drift_split_day` in the EDA findings YAML.
> **📦 Stack:** pandas, matplotlib, scipy
> **✅ Outcome:** The temporal analysis figure is saved. The drift split point is documented for Phase 45.

#### Subphase 11.5 — Feature Multicollinearity & Selection Candidates

> **🎭 Role:** Feature Engineering Lead
> **🔧 Task:** Extend the notebook with multicollinearity analysis. Compute the Pearson correlation matrix for all 78 numeric features. Identify correlated clusters with |r| > 0.95. Within each cluster, retain the feature with the highest mutual information with the label and flag the rest for removal. Also identify near-zero variance features (variance < 0.01). Save the removal candidate list as `removal_candidates: list[str]` in `ml/configs/cicids2017_eda_findings.yaml`.
> **📦 Stack:** pandas, seaborn, sklearn
> **✅ Outcome:** The correlation heatmap with cluster annotations is saved as a figure. The removal candidates YAML key reduces the feature count by approximately 20–25 features.

---

## Phase 12 — UNSW-NB15 Exploratory Data Analysis


### 🎓 What You Will Learn in Phase 12
UNSW-NB15 tests whether your models generalise to a different attack taxonomy. You will learn: cross-dataset taxonomy mapping (translating different label vocabularies to a unified schema), the Earth Mover's Distance (EMD/Wasserstein distance) as a feature separability metric, and how to produce a cross-dataset comparison table for your paper.

### 📄 Research Paper Connection
- Subphase 12.3 → **Figure 2b**: Feature separability (EMD ranking, top 10 features for UNSW-NB15)
- Subphase 12.4 → **Table 1**: Cross-dataset comparison (first rows completed)

### 📖 Concept: Earth Mover's Distance (Wasserstein-1 Distance)
The Earth Mover's Distance (EMD) — also called the Wasserstein-1 distance — measures how much "work" it takes to transform one distribution into another. Think of it as: if distribution A is a pile of dirt and distribution B is a hole, how far do you need to move the dirt to fill the hole?

In Subphase 12.3, you compute EMD between the benign and malicious distributions of each feature. A **high EMD** means the feature clearly separates attacks from normal traffic — it is a useful feature. A **low EMD** means the feature looks the same for attacks and normal traffic — it may be worth removing.

Formula (for 1D discrete distributions): `W1(P, Q) = sum(|CDF_P(x) - CDF_Q(x)|)` over all x.

**Python:** `scipy.stats.wasserstein_distance(benign_values, malicious_values)`

**Why it matters:** The EMD ranking gives you a model-free feature importance measure that you can compare against SHAP importance in Phase 39. If the rankings disagree strongly, it tells you the model is learning unexpected patterns.

#### Subphase 12.1 — Multi-Partition Loading & Profiling


> **🎭 Role:** Senior Data Engineer
> **📍 Context:** UNSW-NB15 is split across four CSV partition files plus a separate ground-truth labels file. The merge requires careful key alignment.
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
> **🔧 Task:** Extend the notebook. For each of the 49 features: compute variance, mean, skewness, kurtosis. Flag features with variance < 0.01 as near-constant. For the top 10 highest-variance features, plot the distribution separately for benign and malicious classes to visualise separability. Compute the Earth Mover's Distance (Wasserstein-1) between benign and malicious distributions per feature. Rank features by EMD (higher = more separable). Save the EMD ranking as `emd_feature_ranking: list[str]` in `ml/configs/unswnb15_eda_findings.yaml`.
> **📦 Stack:** pandas, scipy, matplotlib, numpy
> **✅ Outcome:** The EMD ranking is saved. The top 10 separability plots are saved as figure files referenced in the research paper.

#### Subphase 12.4 — EDA Findings & Cross-Dataset Comparison Stub

> **🎭 Role:** ML Research Lead
> **📍 Context:** UNSW-NB15 EDA findings feed Phase 14 (cross-dataset schema mapping). A comparison table stub makes Phase 14 straightforward.
> **🔧 Task:** Add a final section to the UNSW-NB15 notebook that produces: (1) `ml/configs/unswnb15_eda_findings.yaml` with null_columns, near_zero_variance_features, emd_feature_ranking, low_resource_classes, taxonomy_mapping path; (2) A cross-dataset comparison table stub as a pandas DataFrame comparing NSL-KDD and UNSW-NB15 on: record count, feature count, null rate %, duplicate rate %, class count, and primary preprocessing challenge. Save as CSV for Phase 14 to extend.
> **📦 Stack:** pandas, PyYAML

---

## Phase 13 — BETH Dataset Exploratory Data Analysis

**Context:** BETH is real enterprise honeypot data spanning weeks. Its temporal extent makes it the only dataset that can demonstrate genuine data drift over time.

### 🎓 What You Will Learn in Phase 13
BETH is real honeypot data spanning weeks — it is the only dataset in your benchmark that allows genuine temporal drift analysis. You will learn: chronological data loading, drift window identification, and feature gap analysis (how to handle a dataset that is missing many features from your unified schema). These skills are essential for answering RQ8 (temporal robustness).

### 📄 Research Paper Connection
- Subphase 13.2 → **Figure 4**: Malicious event rate over time (feeds §4.5)
- Subphase 13.2 → Drift windows config → used in Phase 45 MMD experiments → **Table 4**: Drift Detection Results
- Subphase 13.3 → **Appendix A**: BETH feature gap analysis

### 📖 Concept: Concept Drift in Production ML
Data drift (also called concept drift) happens when the statistical distribution of your input data changes over time. In cybersecurity, this is inevitable: new attack tools emerge, network behaviour evolves, and the model's training distribution becomes stale.

There are two types:
1. **Feature drift**: The distribution of X (input features) changes — e.g., typical packet sizes shift due to new protocols.
2. **Label drift**: The relationship between X and Y changes — e.g., an attack that previously produced high byte counts now uses a different technique.

Your research uses **Maximum Mean Discrepancy (MMD)** in Phase 45 to detect both types. BETH is your ground truth: you know drift occurred (from the real capture timeline) and you can verify whether your detector caught it.

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

### 🎓 What You Will Learn in Phase 14
Four datasets with different schemas need to speak the same language. You will learn how to design a unified feature schema — a central vocabulary that enables cross-dataset training and evaluation. This is the most architecturally important decision in the data layer and is what makes cross-dataset evaluation possible (required for RQ7).

### 📄 Research Paper Connection
- Subphase 14.1 → **Table 2**: Unified feature schema (feature name, type, present-in datasets)
- Subphase 14.3 → **Table 1**: Complete cross-dataset comparison table (all 4 rows)

### 📖 Concept: Feature Schema Design for Multi-Dataset Research
When evaluating on multiple datasets, you face the challenge that each dataset measured different features. Your unified schema must answer: "which features do we include, and what do we do when a dataset doesn't have them?"

Decision rule: **Include features present in at least 3 of 4 datasets.** Rationale: if a feature only appears in one dataset, it cannot contribute to cross-dataset evaluation and may introduce dataset-specific bias.

For missing features, two strategies:
1. **Imputation**: Fill with zero (counts, binary flags) or training-set median (rates)
2. **Exclusion**: Drop the dataset-specific feature — simpler but loses information

Your `unified_schema.yaml` makes this decision explicit and auditable. Any reviewer can see exactly which features were included and why.

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

#### Subphase 14.3 — Unified Statistics Summary

> **🎭 Role:** ML Research Lead
> **📍 Context:** The research paper's methodology section requires a dataset comparison table. Generate it automatically from the EDA findings YAML files so it stays in sync.
> **📦 Stack:** pandas, tabulate, mlflow
> **┅ Outcome:** The Markdown table can be pasted directly into the research paper's methodology section without manual editing.

#### Subphase 14.4 — Schema Mapping Test Suite

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** The column mapping is a critical transformation. Errors here silently corrupt every downstream experiment. A comprehensive test suite catches regressions.
> **┅ Outcome:** `uv run pytest ml/tests/test_schema_mapping.py -v` passes all tests. Adding a new column to a dataset's raw schema without updating the mapping file causes a test failure.

---

## Phase 15 — Data Cleaning Pipeline

**Context:** Build the first reproducible pipeline stage. Every cleaning decision is traceable to an EDA finding, and all fitted parameters are serialised for production reuse.

### 🎓 What You Will Learn in Phase 15
You will build a production-grade cleaning pipeline using scikit-learn's Pipeline and Transformer API. The key insight: all fitted parameters (medians, percentiles, IQR bounds) must be fitted on training data only and then applied unchanged to validation and test data. This prevents data leakage — the most critical correctness requirement in ML research.

### 📄 Research Paper Connection
- Subphase 15.3 → **§4.1 Preprocessing**: "We trained a scikit-learn Pipeline on the training set... all transformations were fitted exclusively on training data and applied to held-out sets."
- Subphases 15.1–15.4 → **Reproducibility statement**: The serialised pipeline is the reproducibility artefact.

### 📖 Concept: Data Leakage
Data leakage is when information from your test set contaminates your training process. It is the most common source of over-optimistic results in ML papers.

**Example of leakage:** You compute the mean of a feature across the entire dataset (train + test), then subtract it. Your test set's mean values subtly influenced the feature transform — so the model "saw" the test data during training.

**How to prevent it:** Always use the `fit_transform(X_train)` / `transform(X_test)` pattern. The `fit` step computes statistics from training data only. The `transform` step applies those statistics to any set.

**Scikit-learn Pipelines enforce this:** When you call `pipeline.fit(X_train, y_train)`, every transformer's `fit` runs only on training data. When you call `pipeline.transform(X_test)`, it applies the fitted transforms without refitting.

### ⚠️ Common Mistakes — Data Cleaning
- **Removing outliers from test data**: Outlier removal is a training-time decision. Test data must be passed through the fitted pipeline unchanged — even if it contains extreme values. Those extreme values may be real attack signatures.
- **Imputing before splitting**: If you compute imputation medians on the full dataset (train+test), your test data leaks information into your imputation values. Always split first.
- **Dropping columns by looking at test data**: Any feature selection decision must be based solely on training data analysis.

#### Subphase 15.1 — Cleaning Transformer: Missing & Infinite Values


> **🎭 Role:** Senior ML Engineer with scikit-learn pipeline expertise
> **📍 Context:** EDA findings are documented in YAML files. The cleaning transformer reads these configs, not hardcoded values. The transformer must be scikit-learn compatible (fit/transform interface) for pipeline composition.
> **🔧 Task:** Implement `ml/src/preprocessing/cleaners.py` with these scikit-learn transformers: `MissingValueImputer(strategy_config: dict)` that fits column medians (numeric) and column modes (categorical) on the training set only; `InfiniteValueReplacer` that replaces +inf with the column 99th percentile and -inf with the 1st percentile, both fitted on training; `NegativeValueClipper(non_negative_columns: list[str])` that clips identified columns to zero minimum. Each transformer implements `__sklearn_tags__` for scikit-learn 1.5 compatibility. Write unit tests for each transformer covering the edge cases: all-null column, single-value column, empty DataFrame.
> **📦 Stack:** scikit-learn 1.5, numpy, pandas, joblib, pytest
> **┅ Outcome:** All three transformers pass scikit-learn's `check_estimator()` validation. Fitted parameters are accessible as attributes (e.g., `imputer.fill_values_`). The test suite covers all edge cases.

#### Subphase 15.2 — Cleaning Transformer: Duplicates & Outliers

> **🎭 Role:** Senior ML Engineer
> **📍 Context:** Duplicate removal must be training-only. Outlier clipping preserves extreme attack values rather than removing them, because extreme network statistics are often genuine attack signals.
> **📦 Stack:** scikit-learn 1.5, numpy, pandas, mlflow
> **┅ Outcome:** `DuplicateRemover().fit_transform(train_df)` removes duplicates. `DuplicateRemover().transform(test_df)` returns unchanged test data with a logged warning if duplicates found.

#### Subphase 15.3 — Cleaning Pipeline Composition

> **🎭 Role:** Senior ML Engineer
> **📦 Stack:** scikit-learn, joblib, mlflow, PyYAML

#### Subphase 15.4 — Cleaning Pipeline Test Suite

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** The cleaning pipeline is the foundation of all ML experiments. Regressions here corrupt every downstream result. The test suite must be comprehensive and fast.
> **🔧 Task:** Write `ml/tests/test_cleaning_pipeline.py`. Use `factory-boy` to generate synthetic DataFrames with known data quality issues. Test: (1) Pipeline removes exactly N duplicates from the training set and 0 from the test set; (2) Infinite values are replaced with the correct percentile values fitted on training; (3) Negative values in non-negative columns are clipped to 0; (4) Missing values are imputed with training medians (not test medians); (5) The serialised and deserialised pipeline produces byte-identical output to the original; (6) The pipeline raises `ValueError` when `transform` is called before `fit`. Achieve 100% branch coverage on all transformer classes.
> **📦 Stack:** pytest, factory-boy, pandas, numpy, joblib
> **┅ Outcome:** All tests pass. `coverage report` shows 100% branch coverage for `cleaners.py`.

---

## Phase 16 — Encoding & Scaling Pipeline

**Context:** Convert cleaned data into the numeric feature matrices required by all six model families. All fitted parameters must be serialised for production reuse.

### 🎓 What You Will Learn in Phase 16
You will build the encoding and scaling pipeline and, most critically, implement the correct train/validation/test split for each dataset. You will learn why RobustScaler is better than StandardScaler for network security data, and how to properly encode categorical features without leaking test information.

### 📖 Concept: Why RobustScaler for Security Data?
StandardScaler normalises using `(x - mean) / std`. The problem: one DDoS attack generating 10 million packets will dominate the mean and std, making the scaled values meaningless for all other events.

RobustScaler normalises using `(x - median) / IQR` (interquartile range). The median and IQR are resistant to outliers — a small fraction of extreme values don't distort the scaling. This makes it ideal for security data where attack traffic is extreme by definition.

**Intuition:** After RobustScaling, normal traffic clusters around 0.0, and attack traffic appears as large positive values. This is exactly what you want.

#### Subphase 16.1 — Categorical Encoding


> **🎭 Role:** Senior ML Engineer with feature engineering expertise
> **📍 Context:** Categorical features (protocol type, TCP flags, service type) must be converted to numeric. The encoding strategy balances information preservation with model compatibility.
> **🔧 Task:** Implement `ml/src/preprocessing/encoders.py`. `OrdinalEncoder(columns: list[str])` for low-cardinality categoricals (cardinality ≤ 20) that maps each unique value to an integer and stores the mapping for production. `HashEncoder(columns: list[str], n_components: int = 16)` for high-cardinality categoricals (cardinality > 20) using sklearn's `FeatureHasher` with consistent output dimensions. `LabelEncoder(taxonomy_mapping: dict)` that maps attack class strings to integer indices using the unified taxonomy and is the single source of truth for the class→integer mapping used in all six model training scripts. Each encoder is scikit-learn compatible.
> **📦 Stack:** scikit-learn 1.5, pandas, numpy
> **┅ Outcome:** `LabelEncoder().transform(["DDOS", "NORMAL"])` returns `[0, 6]` (consistent integers). The ordinal mapping is accessible as an attribute for SHAP explanation feature names.

#### Subphase 16.2 — Feature Scaling

> **🎭 Role:** Senior ML Engineer
> **📍 Context:** Network security data contains extreme outliers from attack traffic. Standard scaling is distorted by these outliers. RobustScaler is the correct choice and must be fitted on training data only.
> **📦 Stack:** scikit-learn, mlflow, numpy
> **┅ Outcome:** `RobustFeatureScaler().fit_transform(X_train)` produces a scaled matrix where the median of each column is approximately 0.0. Applying it to `X_test` uses the training medians.

#### Subphase 16.3 — Full Preprocessing Pipeline

> **🎭 Role:** Senior ML Engineer
> **📦 Stack:** scikit-learn, joblib, mlflow
> **┅ Outcome:** The pipeline output is a 2D float32 NumPy array with `len(feature_names)` columns. The feature names list is stored as a pipeline attribute for SHAP explanation labels.

#### Subphase 16.4 — Train/Validation/Test Split

> **🎭 Role:** ML Research Engineer
> **📍 Context:** The split strategy must prevent data leakage, be reproducible given the same seed, and handle the temporal ordering required for BETH.
> **📦 Stack:** scikit-learn, numpy, mlflow
> **┅ Outcome:** The BETH temporal split preserves chronological order. NSL-KDD uses the official split. All three splits are saved as `.npz` files.

#### Subphase 16.5 — Encoding Pipeline Tests

> **🎭 Role:** Senior Test Engineer
> **📍 Context:** Encoding errors silently corrupt model training. Test coverage must be comprehensive.
> **🔧 Task:** Write `ml/tests/test_encoding_pipeline.py`. Test: (1) Categorical encoding produces integer output for all categories seen during training; (2) An unseen category at inference time is handled gracefully (hash encoding) or raises a clear error (ordinal encoding, which must be caught and defaulted); (3) Numeric scaling applies training medians to test data; (4) The full pipeline output has no NaN values; (5) The pipeline is deterministic — same input produces identical output on repeated calls; (6) The BETH temporal split test set contains only timestamps after the validation set. Achieve ≥90% branch coverage.
> **📦 Stack:** pytest, numpy, pandas, factory-boy

---

## Phase 17 — Class Imbalance Handling

**Context:** Recall on minority attack classes is the safety-critical metric. Without proper imbalance handling, models achieve high accuracy by predicting the majority (BENIGN) class and produce dangerously low recall on actual attacks.

### 🎓 What You Will Learn in Phase 17
You will learn two approaches to class imbalance (SMOTE and class weights) and understand the trade-offs between them. This is a direct contribution to your paper: you must justify your choice, and your paper should include a comparison of the two strategies in an ablation table.

### 📄 Research Paper Connection
- Subphases 17.1–17.3 → **§4.1 Imbalance Handling**: Justification for SMOTE vs class weights choice
- Subphase 17.4 → Unit tests → **Reproducibility statement**: "Resampling was applied exclusively to the training fold"

### 📖 Concept: SMOTE — How Does It Create Synthetic Samples?
SMOTE (Synthetic Minority Over-sampling Technique) works in feature space, not raw data:
1. Pick a minority-class sample `x`
2. Find its `k` nearest neighbours (also minority-class)
3. Pick one neighbour `x_neighbour` at random
4. Generate a new sample: `x_new = x + random(0,1) × (x_neighbour - x)`

This creates samples BETWEEN existing minority-class points, rather than duplicating them. The intuition: you're filling in the gaps between real attack examples with plausible synthetic attack examples.

**Limitation:** SMOTE works in raw feature space. If your features are not normalised, SMOTE is dominated by high-magnitude features. Always apply RobustScaler BEFORE SMOTE.

### ✅ Learning Checkpoint — Phases 15–17
1. You compute imputation medians on the full dataset before splitting. Which split (train, val, test) has leaked information into which other split?
3. After running your cleaning pipeline, you check the test set and find some infinite values. Is this a bug? What should you do?

#### Subphase 17.1 — Imbalance Severity Analysis Module


> **🎭 Role:** Senior ML Engineer specialising in imbalanced learning
> **📍 Context:** The imbalance ratio varies dramatically per dataset and per attack class. SMOTE parameters must be computed automatically from the measured ratios, not hardcoded.
> **📦 Stack:** imbalanced-learn 0.12, numpy, mlflow

#### Subphase 17.2 — SMOTE Oversampling

> **🎭 Role:** Senior ML Engineer
> **📍 Context:** SMOTE generates synthetic minority class samples by interpolating between real samples in feature space. It must be applied only to training data, never to validation or test sets.
> **🔧 Task:** Implement `SMOTEResampler` in `imbalance.py` using `imbalanced-learn`'s `SMOTE` with `k_neighbors=5`. The resampler accepts a `SamplingConfig` from the analyser and applies the computed oversampling targets. Implement a guard that raises `ValueError` if called with a dataset flagged as test or validation. After resampling, verify that no synthetic sample is an exact duplicate of a real sample (assert). Log: number of synthetic samples generated per class, total training set size before/after, class distribution after resampling.
> **📦 Stack:** imbalanced-learn, numpy, mlflow
> **┅ Outcome:** `SMOTEResampler().fit_resample(X_train, y_train, config)` produces a balanced training set. The no-duplicates assertion passes. The guard raises on test data.

#### Subphase 17.3 — Class Weight Alternative

> **🎭 Role:** Senior ML Engineer
> **📍 Context:** SMOTE adds computational cost and creates synthetic samples. Class weights are simpler and work natively in scikit-learn and XGBoost. Both strategies are evaluated in the model comparison.
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
> **📦 Stack:** pytest, joblib, numpy, pandas

---

## Phase Map

| Phase | Title | Subphases |
|-------|-------|-----------|
| P9 | Dataset Strategy & Acquisition | 5 |
| P10 | NSL-KDD EDA | 4 |
| P11 | CICIDS-2017 EDA | 4 |
| P12 | UNSW-NB15 EDA | 4 |
| P13 | BETH EDA | 4 |
| P14 | Cross-Dataset Schema Mapping | 4 |
| P15 | Data Cleaning Pipeline | 4 |
| P16 | Encoding & Scaling Pipeline | 5 |
| P17 | Class Imbalance Handling | 5 |

**Previous ←** [01 — Project Foundation](01-project-foundation.md) | **Next →** [03 — Feature Engineering & Experiment Tracking](03-data-engineering.md)

---
