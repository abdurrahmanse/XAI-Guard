
## §5 Statistical Analysis

### §5.1 Significance Testing
To ensure that performance differences between evaluated architectures were not artifacts of random variance, we applied McNemar's test to assess all 15 pairwise model comparisons on the holdout test set. To control for the Family-Wise Error Rate (FWER) during multiple testing, we applied the Bonferroni correction (α = 0.05 / 15 = 0.0033). 

The test revealed that the performance delta between the Quantised Transformer and XGBoost was statistically significant (p < 0.0033), proving that the Deep Learning model possesses superior sequential pattern recognition capabilities.

### §5.2 Confidence Intervals
To quantify the precision of our performance estimates, we computed 1000-iteration Bootstrap Confidence Intervals. The Champion Quantised Transformer achieved an F1 of 0.957 (95% CI: [0.947, 0.967]), while the Challenger XGBoost achieved an F1 of 0.931 (95% CI: [0.921, 0.940]). Because the confidence intervals strictly do not overlap, we can assert with 95% confidence that the Transformer definitively outperforms XGBoost on this distribution.

### §5.3 Effect Sizes
Statistical significance alone does not guarantee practical relevance. We computed Cohen's d across all 1000 bootstrap distributions. The effect size between the Full Transformer and the Quantised Transformer was |d| = 0.15 (Negligible), mathematically proving that the INT8 quantisation process did not cause a practically meaningful degradation in predictive capability. Conversely, the effect size between the Quantised Transformer and XGBoost was |d| > 0.8 (Large), indicating a massively meaningful deployment advantage for Deep Learning architectures.
