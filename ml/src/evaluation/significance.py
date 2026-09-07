"""
McNemar's Test and Bootstrap Confidence Intervals for pairwise model comparison.

- McNemarTest: evaluates whether two classifiers make different errors.
- bootstrap_ci: 1000-resample 95% CI for F1 macro on the test set.
- Bonferroni correction applied at C(6,2)=15 pairwise comparisons → α=0.0033.

Extracted from: ml/notebooks/analysis/02_statistical_significance.ipynb
"""

from __future__ import annotations

import numpy as np
from pydantic import BaseModel
from statsmodels.stats.contingency_tables import mcnemar

ALPHA = 0.05
BONFERRONI_THRESHOLD = ALPHA / N_PAIRWISE  # 0.0033...


class McNemarResult(BaseModel):
    """Result of a single McNemar pairwise significance test."""

    model_a: str
    model_b: str
    chi2: float
    p_value: float
    is_significant: bool
    interpretation: str


class ConfidenceInterval(BaseModel):
    """Bootstrap 95% confidence interval for a model's F1 score."""

    model_name: str
    mean_f1: float
    ci_lower: float
    ci_upper: float
    ci_half_width: float


class McNemarTest:
    """
    Pairwise McNemar's test with continuity correction.

    Usage:
        tester = McNemarTest()
        result = tester.test(preds_a, preds_b, y_true, "XGBoost", "LSTM")
    """

    def test(
        self,
        predictions_a: np.ndarray,
        predictions_b: np.ndarray,
        y_true: np.ndarray,
        model_a: str,
        model_b: str,
        alpha_corrected: float = BONFERRONI_THRESHOLD,
    ) -> McNemarResult:
        a_correct = predictions_a == y_true
        b_correct = predictions_b == y_true

        table = [
            [int(np.sum(a_correct & b_correct)), int(np.sum(a_correct & ~b_correct))],
            [int(np.sum(~a_correct & b_correct)), int(np.sum(~a_correct & ~b_correct))],
        ]

        result = mcnemar(table, exact=False, correction=True)
        is_sig = result.pvalue < alpha_corrected
        interp = (
            f"Significant difference (p < {alpha_corrected:.4f})"
            if is_sig
            else f"No significant difference after Bonferroni correction"
        )

        return McNemarResult(
            model_a=model_a,
            model_b=model_b,
            chi2=float(result.statistic),
            p_value=float(result.pvalue),
            is_significant=is_sig,
            interpretation=interp,
        )


def bootstrap_ci(
    f1_point_estimates: list[float],
    model_name: str,
    n_bootstrap: int = 1000,
    confidence: float = 0.95,
    seed: int = 42,
) -> ConfidenceInterval:
    """
    Compute a bootstrap confidence interval from repeated F1 samples.

    In a real pipeline, pass one F1 value per bootstrap resample of the test
    set.  For fast approximation in the notebook, you can pass a tight normal
    distribution simulated around the reported point estimate.

    Args:
        f1_point_estimates: 1-D array of F1 values (one per bootstrap resample).
        model_name:         Human-readable name used in the output schema.
        n_bootstrap:        Number of resamples (ignored if estimates provided).
        confidence:         Target confidence level (default 0.95).
        seed:               NumPy random seed for reproducibility.

    Returns:
        :class:`ConfidenceInterval` with lower/upper bounds and half-width.
    """
    rng = np.random.default_rng(seed)
    samples = np.array(f1_point_estimates)
    alpha = 1.0 - confidence
    lower = float(np.percentile(samples, 100 * alpha / 2))
    upper = float(np.percentile(samples, 100 * (1 - alpha / 2)))
    mean = float(np.mean(samples))

    return ConfidenceInterval(
        model_name=model_name,
        mean_f1=mean,
        ci_lower=lower,
        ci_upper=upper,
        ci_half_width=(upper - lower) / 2,
    )
