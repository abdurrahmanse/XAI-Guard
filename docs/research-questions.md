# Eight Research Sub-Questions

## RQ1: Classical ML vs Deep Learning
- **H₀:** Deep learning models do not significantly improve F1-Macro compared to tree-based ensembles (XGBoost/RF).
- **Metric:** F1-Macro Delta.
- **Test:** McNemar's Test (p < 0.05).

## RQ2: Sequence Detection (LSTM vs Transformer)
- **H₀:** Transformer models do not outperform LSTMs on temporally distributed attacks (e.g., slowloris, advanced persistent threats).
- **Metric:** Recall on sequence-dependent attack classes.
- **Test:** Wilcoxon Signed-Rank Test.

## RQ3: Transformer Cost-Benefit
- **H₀:** The accuracy gain of a full Transformer Encoder does not justify its GPU-hour training cost compared to a Lightweight Transformer.
- **Metric:** Training GPU-hours / F1-Macro gain ratio.
- **Test:** Threshold Analysis (Must exceed 0.01 F1 per 10 GPU-hours).

## RQ4: Analyst-Actionable XAI
- **H₀:** There is no significant difference in analyst utility between SHAP and LIME explanations.
- **Metric:** Analyst utility composite score (survey/heuristic based).
- **Test:** Kruskal-Wallis H Test.

## RQ5: Accuracy vs Explainability Trade-off
- **H₀:** Highly accurate models do not exhibit lower XAI stability scores than simpler models.
- **Metric:** Pearson correlation between ROC-AUC and SHAP stability score.
- **Test:** Pearson's r significance test.

## RQ6: CPU-Only Operational Efficiency
- **H₀:** No deep learning model can achieve a P99 inference latency of < 100ms on CPU-only infrastructure.
- **Metric:** P99 Inference Latency (ms).
- **Test:** Empirical Benchmark.

## RQ7: Cross-Dataset Generalisation
- **H₀:** Model rankings by F1-Macro are inconsistent across NSL-KDD, CICIDS-2017, UNSW-NB15, and BETH.
- **Metric:** F1-Macro Variance.
- **Test:** Friedman Test.

## RQ8: Robustness to Data Drift
- **H₀:** Complex deep learning models degrade faster under temporal data drift (BETH dataset) than classical tree-based models.
- **Metric:** Maximum Mean Discrepancy (MMD) correlation with F1 decay rate.
- **Test:** Spearman's Rank Correlation.
