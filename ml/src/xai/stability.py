"""
ml/src/xai/stability.py
=======================
SHAP and LIME stability testers for XAI-Guard Pillar 2 metrics.

Stability measures how consistent an explainer is when run multiple times
on identical inputs. Unstable explanations cannot be trusted for analyst
decisions — if running LIME twice gives different top features, the analyst
cannot reliably act on either result.

Metric:
    stability_score = 1 - mean(CoV per feature)
    CoV (Coefficient of Variation) = std(values) / mean(|values|)

Threshold (from Phase 39 specification):
    SHAP: stability_score > 0.95  (strict — SHAP is deterministic for tree models)
    LIME: stability_score > 0.90  (looser — LIME has inherent stochasticity)

Usage:
    from xai.stability import SHAPStabilityTester, LIMEStabilityTester

    shap_tester = SHAPStabilityTester(explainer, n_runs=10)
    score = shap_tester.run(X_test[:50], model)

    lime_tester = LIMEStabilityTester(lime_explainer, n_runs=10)
    score = lime_tester.run(X_test[:50], model.predict_proba)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass
class StabilityReport:
    """
    Stability test result for one explainer on one model.

    Attributes
    ----------
    stability_score : float
        1 - mean(CoV). Range [0, 1]. Higher = more stable.
    threshold : float
        The minimum acceptable stability_score for production use.
    passed : bool
        True if stability_score >= threshold.
    n_runs : int
        Number of repetitions per sample.
    n_samples : int
        Number of samples tested.
    per_feature_cov : dict[str, float]
        Coefficient of variation per feature — identifies which specific
        features are unstable across runs.
    """

    stability_score: float
    threshold: float
    passed: bool
    n_runs: int
    n_samples: int
    per_feature_cov: dict[str, float]

    def summary(self) -> str:
        status = "✅ PASSED" if self.passed else "❌ FAILED"
        return (
            f"Stability Score: {self.stability_score:.4f}  {status}\n"
            f"Threshold: {self.threshold}  |  Runs: {self.n_runs}  |  Samples: {self.n_samples}\n"
            f"Most unstable feature: {max(self.per_feature_cov, key=self.per_feature_cov.get)} "
            f"(CoV={max(self.per_feature_cov.values()):.4f})"
        )


class SHAPStabilityTester:
    """
    Tests SHAP explanation stability by running the explainer N times
    on the same samples and measuring coefficient of variation.

    For TreeExplainer, SHAP is deterministic → stability should be ~1.0.
    For KernelExplainer or DeepExplainer, stability may be lower.

    Parameters
    ----------
    shap_explainer : shap.Explainer
        An already-initialised SHAP explainer.
    n_runs : int
        Number of times to run the explainer per sample. 10 is standard.
    threshold : float
        Minimum stability_score to pass. Default 0.95 for SHAP.
    """

    THRESHOLD = 0.95

    def __init__(self, shap_explainer: object, n_runs: int = 10) -> None:
        self.explainer = shap_explainer
        self.n_runs = n_runs

    def run(
        self, X_samples: np.ndarray, feature_names: list[str] | None = None
    ) -> StabilityReport:
        """
        Run stability test on X_samples.

        Returns
        -------
        StabilityReport
        """
        n_samples, n_features = X_samples.shape
        feature_names = feature_names or [f"feature_{i}" for i in range(n_features)]

        # Collect SHAP values across runs: shape (n_runs, n_samples, n_features)
        all_runs: list[np.ndarray] = []
        for _ in range(self.n_runs):
            sv = self.explainer.shap_values(X_samples)
            if isinstance(sv, list):
                sv = np.array(sv).mean(axis=0)  # average over classes
            all_runs.append(np.abs(sv))

        runs_array = np.array(all_runs)  # (n_runs, n_samples, n_features)

        # CoV per feature: std across runs / mean across runs (per sample, then average)
        per_feature_cov: dict[str, float] = {}
        for fi, fname in enumerate(feature_names):
            values_across_runs = runs_array[:, :, fi]  # (n_runs, n_samples)
            mean_val = values_across_runs.mean()
            std_val = values_across_runs.std()
            cov = std_val / (mean_val + 1e-9)
            per_feature_cov[fname] = float(cov)

        mean_cov = float(np.mean(list(per_feature_cov.values())))
        stability_score = max(0.0, 1.0 - mean_cov)

        return StabilityReport(
            stability_score=stability_score,
            threshold=self.THRESHOLD,
            passed=stability_score >= self.THRESHOLD,
            n_runs=self.n_runs,
            n_samples=n_samples,
            per_feature_cov=per_feature_cov,
        )


class LIMEStabilityTester:
    """
    Tests LIME explanation stability by running with different random seeds.

    LIME is inherently stochastic — different seeds produce different perturbation
    sets, which can change feature rankings. Production LIME always uses seed=42,
    but this test quantifies the worst-case variation an analyst might see if
    seeds were not fixed.

    Parameters
    ----------
    lime_explainer_factory : callable
        A factory function that accepts random_state and returns a new
        XAIGuardLIMEExplainer. This is needed because LIME bakes the seed
        into the explainer object at construction time.
    n_runs : int
        Number of different seeds to try. 10 is standard.
    threshold : float
        Minimum stability_score to pass. Default 0.90 (looser than SHAP).
    """

    THRESHOLD = 0.90

    def __init__(
        self, lime_explainer_factory: Callable[[int], object], n_runs: int = 10
    ) -> None:
        self.factory = lime_explainer_factory
        self.n_runs = n_runs

    def run(
        self,
        X_samples: np.ndarray,
        predict_fn: Callable[[np.ndarray], np.ndarray],
        feature_names: list[str] | None = None,
    ) -> StabilityReport:
        """Run stability test on X_samples with N different seeds."""
        n_samples, n_features = X_samples.shape
        feature_names = feature_names or [f"feature_{i}" for i in range(n_features)]

        # Use seeds 0–(n_runs-1) to measure seed sensitivity
        seeds = list(range(self.n_runs))
        all_runs: list[np.ndarray] = []

        for seed in seeds:
            explainer = self.factory(seed)
            run_values = np.zeros((n_samples, n_features))
            for i, row in enumerate(X_samples):
                result = explainer.explain(predict_fn, row)
                # Build a feature-indexed importance vector
                contrib_map = {
                    fc.feature_name: fc.abs_contribution
                    for fc in result.feature_contributions
                }
                for fi, fname in enumerate(feature_names):
                    run_values[i, fi] = contrib_map.get(fname, 0.0)
            all_runs.append(run_values)

        runs_array = np.array(all_runs)  # (n_runs, n_samples, n_features)

        per_feature_cov: dict[str, float] = {}
        for fi, fname in enumerate(feature_names):
            values = runs_array[:, :, fi]
            mean_val = values.mean()
            std_val = values.std()
            cov = std_val / (mean_val + 1e-9)
            per_feature_cov[fname] = float(cov)

        mean_cov = float(np.mean(list(per_feature_cov.values())))
        stability_score = max(0.0, 1.0 - mean_cov)

        return StabilityReport(
            stability_score=stability_score,
            threshold=self.THRESHOLD,
            passed=stability_score >= self.THRESHOLD,
            n_runs=self.n_runs,
            n_samples=n_samples,
            per_feature_cov=per_feature_cov,
        )
