# XAI-Guard: Eight Formal Research Sub-Questions

This document decomposes the core XAI-Guard research statement into eight formally testable sub-questions. Every experiment conducted in the MLOps pipeline is designed to generate empirical evidence that maps directly back to confirming or rejecting these null hypotheses.

---

## RQ1: Classical Machine Learning vs. Deep Learning Predictive Delta
**Context:** Modern SOCs often default to classical models (e.g., Random Forest, XGBoost) due to ease of deployment. It must be empirically proven whether deep learning architectures offer a statistically significant improvement in detecting minority attack classes.
- **Null Hypothesis (H₀):** Deep learning architectures (LSTM, Transformer) do not yield a statistically significant improvement in F1-Macro scores compared to tree-based ensemble methods (XGBoost, Random Forest) when evaluated on heterogeneous network traffic.
- **Alternative Hypothesis (H₁):** Deep learning architectures yield a statistically significant improvement in F1-Macro scores compared to tree-based ensemble methods.
- **Evaluation Metric:** F1-Macro Delta (ΔF1-Macro).
- **Statistical Test:** McNemar's Test for marginal homogeneity (with Bonferroni correction for multiple comparisons, α = 0.05).

## RQ2: Sequential Dependency Detection (LSTM vs. Transformer)
**Context:** Many APTs and slow-rate attacks (e.g., Slowloris, low-and-slow brute force) rely on temporal sequences. We must determine if the self-attention mechanism in Transformers captures these patterns better than the recurrent memory cells of LSTMs.
- **Null Hypothesis (H₀):** Transformer Encoders do not demonstrate a statistically higher Recall on sequence-dependent attack classes (e.g., Botnet, Infiltration) compared to Long Short-Term Memory (LSTM) networks.
- **Alternative Hypothesis (H₁):** Transformer Encoders demonstrate a statistically higher Recall on sequence-dependent attack classes compared to LSTM networks.
- **Evaluation Metric:** Class-specific Recall and PR-AUC on temporally distributed attack taxonomy labels.
- **Statistical Test:** Wilcoxon Signed-Rank Test across chronological sequence windows.

## RQ3: Transformer Cost-Benefit Analysis
**Context:** Transformers are notoriously computationally expensive. This question evaluates if their predictive superiority mathematically justifies their exorbitant carbon and hardware costs in a security context.
- **Null Hypothesis (H₀):** The marginal increase in F1-Macro achieved by a Full Transformer Encoder does not exceed the predefined cost-benefit threshold of 0.01 F1 per 10 GPU-hours of training time when compared to a Lightweight Edge Transformer.
- **Alternative Hypothesis (H₁):** The marginal increase in F1-Macro exceeds the predefined cost-benefit threshold.
- **Evaluation Metric:** GPU-Hour Training Cost / ΔF1-Macro Efficiency Ratio.
- **Statistical Test:** Threshold Analysis against baseline empirical measurements.

## RQ4: Analyst-Actionable Interpretability (XAI)
**Context:** Explanations must be easily interpreted by a Tier-1 SOC analyst under time pressure. We evaluate whether permutation-based or gradient/attention-based methods yield more actionable context.
- **Null Hypothesis (H₀):** There is no statistically significant difference in the Analyst Utility Composite Score between Shapley Additive exPlanations (SHAP), Local Interpretable Model-agnostic Explanations (LIME), and Attention Rollout.
- **Alternative Hypothesis (H₁):** There is a statistically significant difference in the Analyst Utility Composite Score between the evaluated XAI methods.
- **Evaluation Metric:** Analyst Utility Composite Score (a heuristic measuring explanation sparsity, feature comprehensibility mapping, and temporal relevance).
- **Statistical Test:** Kruskal-Wallis H Test for independent non-parametric group comparisons.

## RQ5: The Accuracy vs. Explainability Trade-off
**Context:** Highly parameterized models (like Transformers) are highly accurate but theoretically harder to explain consistently. This evaluates if increasing a model's complexity mathematically degrades the stability of its explanations.
- **Null Hypothesis (H₀):** There is no significant negative correlation between a model’s predictive performance (ROC-AUC) and the mathematical stability of its generated XAI feature contributions.
- **Alternative Hypothesis (H₁):** There is a significant negative correlation between predictive performance and XAI stability.
- **Evaluation Metric:** Pearson correlation coefficient ($r$) comparing ROC-AUC vs. SHAP Stability Score (calculated as $1 - CV$ across 10 identical explanation perturbations).
- **Statistical Test:** Pearson's $r$ significance test (p < 0.05).

## RQ6: CPU-Only Operational Efficiency at the Edge
**Context:** Many real-world IDSs are deployed on edge firewalls or CPU-only Kubernetes clusters where inference latency is paramount to preventing network bottlenecks.
- **Null Hypothesis (H₀):** No evaluated deep learning model (LSTM, Full Transformer, Lightweight Transformer) can sustain a P99 Inference Latency of strictly less than 100 milliseconds (ms) when executing on commodity CPU-only infrastructure under a load of 1,000 events/second.
- **Alternative Hypothesis (H₁):** At least one evaluated deep learning model can sustain a P99 Inference Latency of < 100ms under the specified conditions.
- **Evaluation Metric:** P99 Inference Latency (ms) and Peak RSS Memory (MB).
- **Statistical Test:** Empirical Load Testing Benchmark.

## RQ7: Cross-Dataset Generalisation and Consistency
**Context:** A model that excels on CICIDS-2017 but fails on UNSW-NB15 is overfit to a specific network topology. We evaluate ranking consistency across multiple heterogeneous networks.
- **Null Hypothesis (H₀):** Model performance rankings (by F1-Macro) are statistically inconsistent and exhibit high variance when evaluated across NSL-KDD, CICIDS-2017, UNSW-NB15, and BETH.
- **Alternative Hypothesis (H₁):** Model performance rankings remain statistically consistent across all four benchmark datasets.
- **Evaluation Metric:** F1-Macro variance and Rank Correlation across datasets.
- **Statistical Test:** Friedman Test for repeated measures on non-parametric rank data.

## RQ8: Robustness to Concept and Temporal Data Drift
**Context:** The BETH dataset contains enterprise honeypot data that drifts temporally. We evaluate which model architecture is most resilient to zero-day shifts in adversary behavior.
- **Null Hypothesis (H₀):** Complex deep learning architectures do not demonstrate a faster rate of F1-Macro degradation under temporal data drift compared to classical tree-based ensembles.
- **Alternative Hypothesis (H₁):** Complex deep learning architectures demonstrate a significantly faster rate of F1-Macro degradation under temporal data drift.
- **Evaluation Metric:** Spearman's Rank Correlation between the Maximum Mean Discrepancy (MMD) drift score and the chronological F1-Macro decay rate.
- **Statistical Test:** Spearman's Rank Correlation ($rs$) significance test.
