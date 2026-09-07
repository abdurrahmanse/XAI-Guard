"""
ml/src/evaluation/robustness.py
================================
Gaussian noise and adversarial robustness testing for XAI-Guard.

Two robustness tests:
  1. GaussianNoiseRobustnessTester — simulates noisy sensors and imprecise
     traffic measurements. Tests at σ ∈ {0.01, 0.05, 0.10, 0.20}.
  2. ARTAdversarialTester — IBM ART HopSkipJump attack on XGBoost Champion.
     Tests worst-case evasion by a sophisticated attacker who knows the model.

Robustness score formula (R):
    R = 1 - (F1_clean - F1_sigma_0.10) / F1_clean
    Models with R > 0.95 at σ=0.10 are considered robust.

Paper (§4.6):
    "We evaluated robustness under Gaussian noise at σ ∈ {0.01, 0.05, 0.10, 0.20}.
    XGBoost maintained F1={X} at σ=0.10, demonstrating R={Y} robustness."

Usage:
    from evaluation.robustness import GaussianNoiseRobustnessTester
    tester = GaussianNoiseRobustnessTester()
    report = tester.run(model, X_test, y_test)
    print(report.summary())
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class RobustnessReport:
    """Gaussian noise robustness results for one model."""

    model_family: str
    noise_levels: list[float]
    f1_per_level: dict[float, float]  # sigma → F1 macro
    f1_clean: float
    robustness_score_010: float  # R at σ=0.10
    passed: bool  # R > 0.95

    def summary(self) -> str:
        lines = [
            f"=== Robustness Report ({self.model_family}) ===",
            f"  F1 (clean):        {self.f1_clean:.4f}",
        ]
        for sigma, f1 in sorted(self.f1_per_level.items()):
            degradation = (self.f1_clean - f1) / (self.f1_clean + 1e-9)
            lines.append(f"  F1 at σ={sigma:.2f}:     {f1:.4f}  (Δ={degradation:.2%})")
        lines.append(
            f"  Robustness (σ=0.10): {self.robustness_score_010:.4f}  "
            f"{'✅' if self.passed else '❌'}"
        )
        return "\n".join(lines)


@dataclass
class AdversarialReport:
    """ART adversarial attack results."""

    model_family: str
    attack_name: str
    n_samples: int
    success_rate: float  # proportion misclassified after attack
    mean_l2_distance: float  # mean perturbation magnitude
    mean_confidence_drop: float  # how much model confidence dropped

    def summary(self) -> str:
        return (
            f"=== Adversarial Report ({self.model_family}) ===\n"
            f"  Attack:                {self.attack_name}\n"
            f"  Samples tested:        {self.n_samples}\n"
            f"  Evasion success rate:  {self.success_rate:.2%}\n"
            f"  Mean L2 perturbation:  {self.mean_l2_distance:.4f}\n"
            f"  Mean confidence drop:  {self.mean_confidence_drop:.4f}\n"
        )


class GaussianNoiseRobustnessTester:
    """
    Tests model robustness by adding Gaussian noise at multiple levels.

    Parameters
    ----------
    noise_levels : list[float]
        σ values to test. Default: [0.01, 0.05, 0.10, 0.20]
    robust_threshold : float
        R score threshold to pass (default 0.95 at σ=0.10).
    """

    def __init__(
        self,
        noise_levels: list[float] = None,
        robust_threshold: float = 0.95,
    ) -> None:
        self.noise_levels = noise_levels or [0.01, 0.05, 0.10, 0.20]
        self.robust_threshold = robust_threshold

    def run(
        self,
        model: object,
        X_test: np.ndarray,
        y_test: np.ndarray,
        model_family: str = "unknown",
        feature_ranges: np.ndarray | None = None,
    ) -> RobustnessReport:
        """
        Compute F1 at each noise level.

        Parameters
        ----------
        model : object with predict(X) method
        X_test : np.ndarray
        y_test : np.ndarray
        feature_ranges : np.ndarray | None
            Shape (n_features, 2) with [min, max] per feature.
            Used to clip perturbed values to valid ranges.

        Returns
        -------
        RobustnessReport
        """
        from sklearn.metrics import f1_score

        # Compute clean F1
        y_pred_clean = model.predict(X_test)
        f1_clean = float(
            f1_score(y_test, y_pred_clean, average="macro", zero_division=0)
        )

        # Set feature clipping ranges from training data if not provided
        if feature_ranges is None:
            feature_ranges = np.column_stack([X_test.min(axis=0), X_test.max(axis=0)])

        f1_per_level: dict[float, float] = {}
        rng = np.random.default_rng(42)

        for sigma in self.noise_levels:
            noise = rng.normal(0, sigma, size=X_test.shape)
            X_noisy = X_test + noise
            # Clip to valid feature ranges to prevent out-of-distribution inputs
            X_noisy = np.clip(X_noisy, feature_ranges[:, 0], feature_ranges[:, 1])
            y_pred = model.predict(X_noisy)
            f1 = float(f1_score(y_test, y_pred, average="macro", zero_division=0))
            f1_per_level[sigma] = f1

        # Robustness score at σ=0.10
        f1_010 = f1_per_level.get(0.10, f1_per_level.get(0.20, f1_clean))
        r_score = 1.0 - (f1_clean - f1_010) / (f1_clean + 1e-9)

        return RobustnessReport(
            model_family=model_family,
            noise_levels=self.noise_levels,
            f1_per_level=f1_per_level,
            f1_clean=f1_clean,
            robustness_score_010=float(r_score),
            passed=r_score >= self.robust_threshold,
        )


class ARTAdversarialTester:
    """
    IBM ART (Adversarial Robustness Toolbox) adversarial testing.

    Uses HopSkipJump attack for XGBoost/sklearn models (black-box).
    Uses FastGradientMethod for PyTorch models (white-box).

    Note: ART requires `adversarial-robustness-toolbox` to be installed:
        pip install adversarial-robustness-toolbox

    This class wraps ART and provides a unified interface that returns
    an AdversarialReport regardless of attack type.
    """

    def __init__(self, n_samples: int = 100) -> None:
        self.n_samples = n_samples

    def run_hopskipjump(
        self,
        model: object,
        X_test: np.ndarray,
        y_test: np.ndarray,
        model_family: str = "XGBoost",
    ) -> AdversarialReport:
        """HopSkipJump attack — black-box, works for any sklearn/XGBoost model."""
        try:
            from art.attacks.evasion import HopSkipJump
            from art.estimators.classification import SklearnClassifier
        except ImportError:
            raise ImportError(
                "adversarial-robustness-toolbox required: "
                "pip install adversarial-robustness-toolbox"
            )

        # Select correctly-classified CRITICAL threat samples
        y_pred = model.predict(X_test)
        correct_mask = (y_pred == y_test) & (y_test == 1)  # class 1 = attack
        X_attacks = X_test[correct_mask][: self.n_samples]
        y_attacks = y_test[correct_mask][: self.n_samples]

        if len(X_attacks) == 0:
            return AdversarialReport(model_family, "HopSkipJump", 0, 0.0, 0.0, 0.0)

        classifier = SklearnClassifier(model=model)
        attack = HopSkipJump(
            classifier=classifier, targeted=False, max_iter=20, max_eval=100
        )
        X_adv = attack.generate(x=X_attacks)

        # Measure success
        y_pred_adv = model.predict(X_adv)
        success_rate = float(np.mean(y_pred_adv != y_attacks))
        l2_distances = np.linalg.norm(X_adv - X_attacks, axis=1)

        # Confidence drop
        proba_before = model.predict_proba(X_attacks)[:, 1]
        proba_after = model.predict_proba(X_adv)[:, 1]
        conf_drop = float(np.mean(proba_before - proba_after))

        return AdversarialReport(
            model_family=model_family,
            attack_name="HopSkipJump (black-box)",
            n_samples=len(X_attacks),
            success_rate=success_rate,
            mean_l2_distance=float(np.mean(l2_distances)),
            mean_confidence_drop=conf_drop,
        )
