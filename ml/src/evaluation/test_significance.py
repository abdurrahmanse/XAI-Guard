"""
Unit tests for McNemarTest and bootstrap_ci.
"""

import numpy as np
import pytest

from ml.src.evaluation.significance import (
    BONFERRONI_THRESHOLD,
    McNemarTest,
    bootstrap_ci,
)
                                            bootstrap_ci)

np.random.seed(42)
N = 5000
y_true = np.ones(N, dtype=int)

# Model A: 93% accurate
preds_a = np.where(np.random.rand(N) < 0.93, 1, 0)
# Model B: also ~93% but different errors
preds_b = np.where(np.random.rand(N) < 0.93, 1, 0)
# Model C: only 72% accurate — clearly worse
preds_c = np.where(np.random.rand(N) < 0.72, 1, 0)


def test_mcnemar_returns_result():
    tester = McNemarTest()
    result = tester.test(preds_a, preds_b, y_true, "A", "B")
    assert result.model_a == "A"
    assert result.model_b == "B"
    assert result.chi2 >= 0.0
    assert 0.0 <= result.p_value <= 1.0


def test_mcnemar_clearly_different_models_is_significant():
    """Model A (93%) vs Model C (72%) should be highly significant."""
    tester = McNemarTest()
    result = tester.test(preds_a, preds_c, y_true, "A", "C")
    assert result.is_significant is True


def test_bootstrap_ci_correct_ordering():
    """CI lower must be <= mean <= upper."""
    f1_samples = list(np.random.normal(0.93, 0.005, 1000))
    ci = bootstrap_ci(f1_samples, "XGBoost")
    assert ci.ci_lower <= ci.mean_f1 <= ci.ci_upper


def test_bootstrap_ci_half_width_positive():
    f1_samples = list(np.random.normal(0.93, 0.005, 1000))
    ci = bootstrap_ci(f1_samples, "XGBoost")
    assert ci.ci_half_width > 0


def test_bonferroni_threshold_value():
    """Ensure the Bonferroni constant is correctly computed for 15 pairwise comparisons."""
    assert abs(BONFERRONI_THRESHOLD - 0.05 / 15) < 1e-10

