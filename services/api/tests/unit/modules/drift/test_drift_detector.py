"""Unit tests for drift detection — PSI calculation and threshold rules."""
import math


# ── PSI (Population Stability Index) computation ──────────────────────────────
# Mirrors the production drift detector logic.
# PSI < 0.10  → No significant drift (stable)
# PSI 0.10–0.25 → Moderate drift (monitor)
# PSI > 0.25  → Significant drift (retrain)

PSI_STABLE_THRESHOLD    = 0.10
PSI_MODERATE_THRESHOLD  = 0.25


def _compute_psi(expected: list[float], actual: list[float], epsilon: float = 1e-6) -> float:
    """
    Computes Population Stability Index between two distributions.
    Both lists must be normalised (sum to 1.0) probability distributions.
    """
    assert len(expected) == len(actual), "Distributions must have same length"
    psi = 0.0
    for e, a in zip(expected, actual):
        e = max(e, epsilon)
        a = max(a, epsilon)
        psi += (a - e) * math.log(a / e)
    return psi


def test_identical_distributions_psi_is_zero():
    dist = [0.25, 0.25, 0.25, 0.25]
    psi = _compute_psi(dist, dist)
    assert psi < PSI_STABLE_THRESHOLD


def test_slightly_shifted_distribution_is_stable():
    expected = [0.70, 0.20, 0.10]
    actual   = [0.68, 0.21, 0.11]
    psi = _compute_psi(expected, actual)
    assert psi < PSI_STABLE_THRESHOLD, f"Expected stable PSI, got {psi:.4f}"


def test_significantly_different_distribution_triggers_drift():
    # Training: 80% benign. Production: 40% benign → clear distribution shift
    expected = [0.80, 0.12, 0.08]
    actual   = [0.40, 0.35, 0.25]
    psi = _compute_psi(expected, actual)
    assert psi > PSI_MODERATE_THRESHOLD, f"Expected drift PSI, got {psi:.4f}"


def test_psi_is_non_negative():
    expected = [0.50, 0.30, 0.20]
    actual   = [0.45, 0.35, 0.20]
    psi = _compute_psi(expected, actual)
    assert psi >= 0.0


def test_psi_thresholds_are_correctly_ordered():
    assert PSI_STABLE_THRESHOLD < PSI_MODERATE_THRESHOLD

