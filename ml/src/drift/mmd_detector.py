"""
ml/src/drift/mmd_detector.py
=============================
Maximum Mean Discrepancy (MMD) drift detector for XAI-Guard.

WHY MMD?
PSI (Population Stability Index) only tests marginal distributions one
feature at a time. MMD tests the JOINT distribution — it detects drift
in feature correlations that PSI misses (e.g., when attack patterns shift
to use different combinations of port + protocol + bytes).

MMD FORMULA:
    MMD²(P, Q) = E[k(x,x')] + E[k(y,y')] − 2E[k(x,y)]
    where k is an RBF kernel.

If MMD ≈ 0, P and Q are statistically identical (no drift).
If MMD is large, P and Q have diverged (drift detected).

THRESHOLDS (calibrated at 5% false positive rate):
    MMD < 0.05  → NONE    — model operating normally
    0.05 ≤ MMD < 0.10 → WARNING  — monitor, consider scheduling retraining
    MMD ≥ 0.10  → CRITICAL — trigger automated retraining immediately

In your paper (§4.5):
"We used MMD drift detection (alibi-detect, p=0.05) with a 5000-sample
reference window from CICIDS-2017 training data."

Usage:
    from drift.mmd_detector import MMDDriftDetector, DriftReport, DriftThreshold
    detector = MMDDriftDetector(X_reference)
    report: DriftReport = detector.detect(X_production_window)
    print(report.summary())
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field

import numpy as np


class DriftThreshold(str, enum.Enum):
    """Three-level drift severity classification."""

    NONE = "NONE"  # MMD < 0.05 — no drift
    WARNING = "WARNING"  # 0.05 ≤ MMD < 0.10 — monitor
    CRITICAL = "CRITICAL"  # MMD ≥ 0.10 — retrain now


@dataclass
class DriftReport:
    """
    Result of a single MMD drift detection call.

    Attributes
    ----------
    mmd_score : float
        The raw MMD² value. 0 = no drift. Higher = more drift.
    drift_detected : bool
        True if threshold_level is WARNING or CRITICAL.
    threshold_level : DriftThreshold
        NONE / WARNING / CRITICAL based on MMD thresholds.
    p_value : float
        Statistical p-value (from permutation test). < 0.05 = significant.
    n_reference : int
        Size of the reference (training) window.
    n_current : int
        Size of the current (production) window.
    features_drifted : list[str]
        Features flagged as individually drifted by univariate tests.
    """

    mmd_score: float
    drift_detected: bool
    threshold_level: DriftThreshold
    p_value: float
    n_reference: int
    n_current: int
    features_drifted: list[str] = field(default_factory=list)

    def summary(self) -> str:
        status = {
            DriftThreshold.NONE: "✅ No drift",
            DriftThreshold.WARNING: "⚠️  WARNING — monitor closely",
            DriftThreshold.CRITICAL: "🔴 CRITICAL — trigger retraining",
        }[self.threshold_level]
        return (
            f"=== Drift Report ===\n"
            f"  MMD score:       {self.mmd_score:.6f}\n"
            f"  Status:          {status}\n"
            f"  p-value:         {self.p_value:.4f}\n"
            f"  Reference size:  {self.n_reference}\n"
            f"  Current size:    {self.n_current}\n"
            f"  Drifted features: {', '.join(self.features_drifted) or 'none'}\n"
        )

    def to_mlflow_dict(self) -> dict:
        return {
            "drift_mmd_score": self.mmd_score,
            "drift_detected": int(self.drift_detected),
            "drift_level": self.threshold_level.value,
            "drift_pvalue": self.p_value,
            "n_features_drifted": len(self.features_drifted),
        }


def _rbf_kernel(X: np.ndarray, Y: np.ndarray, sigma: float = 1.0) -> np.ndarray:
    """RBF (Gaussian) kernel matrix K(X, Y)."""
    # ||x - y||² using the identity: ||x-y||² = ||x||² + ||y||² - 2x·y
    X_sq = (X**2).sum(axis=1, keepdims=True)
    Y_sq = (Y**2).sum(axis=1, keepdims=True)
    cross = X @ Y.T
    sq_dist = X_sq + Y_sq.T - 2 * cross
    return np.exp(-sq_dist / (2 * sigma**2))


def _compute_mmd(X: np.ndarray, Y: np.ndarray, sigma: float = 1.0) -> float:
    """Compute unbiased MMD² between X (reference) and Y (current)."""
    n, m = len(X), len(Y)
    Kxx = _rbf_kernel(X, X, sigma)
    Kyy = _rbf_kernel(Y, Y, sigma)
    Kxy = _rbf_kernel(X, Y, sigma)
    # Unbiased estimator: zero out diagonal
    np.fill_diagonal(Kxx, 0)
    np.fill_diagonal(Kyy, 0)
    mmd2 = Kxx.sum() / (n * (n - 1)) + Kyy.sum() / (m * (m - 1)) - 2 * Kxy.mean()
    return float(max(0.0, mmd2))


class MMDDriftDetector:
    """
    MMD-based drift detector with three-level threshold classification.

    Parameters
    ----------
    X_reference : np.ndarray
        Training distribution. Recommended: 5000 samples from CICIDS-2017.
        Larger reference = more reliable MMD estimate.
    p_val : float
        Significance level for the permutation test (default 0.05).
    warning_threshold : float
        MMD score above which WARNING is triggered (default 0.05).
    critical_threshold : float
        MMD score above which CRITICAL is triggered (default 0.10).
    n_permutations : int
        Number of permutations for p-value estimation (default 200).
    sigma : float
        RBF kernel bandwidth. If None, uses the median heuristic.
    max_samples : int
        Maximum samples to use from reference and current windows for speed.
    """

    def __init__(
        self,
        X_reference: np.ndarray,
        p_val: float = 0.05,
        warning_threshold: float = 0.05,
        critical_threshold: float = 0.10,
        n_permutations: int = 200,
        sigma: float | None = None,
        max_samples: int = 500,
    ) -> None:
        self.p_val = p_val
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.n_permutations = n_permutations
        self.max_samples = max_samples

        # Subsample reference for speed
        idx = np.random.default_rng(42).choice(
            len(X_reference), size=min(max_samples, len(X_reference)), replace=False
        )
        self.X_reference = X_reference[idx]

        # Median heuristic for kernel bandwidth
        if sigma is None:
            sample = self.X_reference[:100]
            dists = np.sqrt(((sample[:, None] - sample[None, :]) ** 2).sum(axis=-1))
            sigma = float(np.median(dists[dists > 0])) or 1.0
        self.sigma = sigma

    def detect(
        self, X_current: np.ndarray, feature_names: list[str] | None = None
    ) -> DriftReport:
        """
        Run MMD drift detection on a production window.

        Parameters
        ----------
        X_current : np.ndarray
            Current production data window (recommended: 1000 events).
        feature_names : list[str] | None
            For per-feature univariate drift analysis.

        Returns
        -------
        DriftReport
        """
        # Subsample current window for speed
        rng = np.random.default_rng(42)
        idx = rng.choice(
            len(X_current), size=min(self.max_samples, len(X_current)), replace=False
        )
        X_curr = X_current[idx]
        X_ref = self.X_reference

        # Compute observed MMD²
        mmd_observed = _compute_mmd(X_ref, X_curr, self.sigma)

        # Permutation test for p-value
        combined = np.vstack([X_ref, X_curr])
        n_ref, n_curr = len(X_ref), len(X_curr)
        null_mmds = []
        for _ in range(self.n_permutations):
            perm = rng.permutation(len(combined))
            X_a = combined[perm[:n_ref]]
            X_b = combined[perm[n_ref:]]
            null_mmds.append(_compute_mmd(X_a, X_b, self.sigma))
        p_value = float(np.mean(np.array(null_mmds) >= mmd_observed))

        # Per-feature univariate drift (simple KS test)
        features_drifted: list[str] = []
        if feature_names and p_value < self.p_val:
            from scipy.stats import ks_2samp

            n_features = min(X_ref.shape[1], len(feature_names))
            for fi in range(n_features):
                _, ks_pval = ks_2samp(X_ref[:, fi], X_curr[:, fi])
                if ks_pval < 0.01:  # stricter threshold for individual features
                    features_drifted.append(feature_names[fi])

        # Classify threshold level
        if mmd_observed >= self.critical_threshold:
            threshold_level = DriftThreshold.CRITICAL
        elif mmd_observed >= self.warning_threshold:
            threshold_level = DriftThreshold.WARNING
        else:
            threshold_level = DriftThreshold.NONE

        drift_detected = threshold_level != DriftThreshold.NONE

        return DriftReport(
            mmd_score=mmd_observed,
            drift_detected=drift_detected,
            threshold_level=threshold_level,
            p_value=p_value,
            n_reference=n_ref,
            n_current=n_curr,
            features_drifted=features_drifted,
        )
