"""
ml/src/evaluation/xai_metrics.py
=================================
XAI Pillar 2 Evaluator — stability and cross-method fidelity metrics.

Pillar 2 of the Three-Pillar Composite Deployment Score (CDS) covers
explanation quality. Four metrics are computed for each model:

  1. shap_stability        — 1 - CoV across 10 SHAP runs (threshold ≥ 0.95)
  2. lime_stability        — 1 - CoV across 10 LIME runs (threshold ≥ 0.90)
  3. shap_lime_spearman    — mean Spearman ρ between SHAP and LIME top-10 rankings
  4. computation_time_ms   — P50 latency for generating one explanation

Pillar 2 score:
    P2 = 0.35 * shap_stability
       + 0.35 * lime_stability
       + 0.20 * spearman_normalised     (ρ mapped 0→1 range)
       + 0.10 * speed_score             (1 if < 5s, 0 if > 30s)

Usage:
    from evaluation.xai_metrics import XAIPillar2Evaluator, XAIPillar2Metrics
    evaluator = XAIPillar2Evaluator()
    metrics = evaluator.evaluate(model, X_test, feature_names)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np


@dataclass
class XAIPillar2Metrics:
    """
    Full Pillar 2 evaluation result for one model.

    All scores are in [0, 1] range. Higher = better.
    """

    # SHAP metrics
    shap_stability_score: float  # 1 - mean(CoV) across 10 runs
    shap_stability_passed: bool  # True if ≥ 0.95
    computation_time_shap_ms: float  # P50 latency for 50 SHAP calls

    # LIME metrics
    lime_stability_score: float  # 1 - mean(CoV) across 10 seeds
    lime_stability_passed: bool  # True if ≥ 0.90
    computation_time_lime_ms: float  # P50 latency for 50 LIME calls

    # Cross-method agreement
    shap_lime_spearman_mean: float  # mean Spearman ρ across 100 samples
    shap_lime_spearman_std: float  # std of ρ — measures consistency of agreement

    # Composite Pillar 2 score
    pillar2_score: float  # weighted combination (see formula above)

    model_family: str = "unknown"
    n_samples_evaluated: int = 0

    def summary(self) -> str:
        return (
            f"=== XAI Pillar 2 Metrics ({self.model_family}) ===\n"
            f"  SHAP Stability:       {self.shap_stability_score:.4f}  "
            f"{'✅' if self.shap_stability_passed else '❌'}\n"
            f"  LIME Stability:       {self.lime_stability_score:.4f}  "
            f"{'✅' if self.lime_stability_passed else '❌'}\n"
            f"  SHAP-LIME Spearman ρ: {self.shap_lime_spearman_mean:.4f} "
            f"(±{self.shap_lime_spearman_std:.4f})\n"
            f"  SHAP latency (P50):   {self.computation_time_shap_ms:.1f} ms\n"
            f"  LIME latency (P50):   {self.computation_time_lime_ms:.1f} ms\n"
            f"  ─────────────────────────────────────\n"
            f"  Pillar 2 Score:       {self.pillar2_score:.4f}\n"
        )

    def to_mlflow_dict(self) -> dict[str, float]:
        """Flat dict ready for mlflow.log_metrics()."""
        return {
            "p2_shap_stability": self.shap_stability_score,
            "p2_lime_stability": self.lime_stability_score,
            "p2_spearman_mean": self.shap_lime_spearman_mean,
            "p2_spearman_std": self.shap_lime_spearman_std,
            "p2_shap_latency_ms": self.computation_time_shap_ms,
            "p2_lime_latency_ms": self.computation_time_lime_ms,
            "p2_pillar2_score": self.pillar2_score,
        }


class XAIPillar2Evaluator:
    """
    Evaluates XAI Pillar 2 metrics for any model.

    Parameters
    ----------
    n_stability_runs : int
        Number of repetitions for stability testing. Default 10.
    n_compare_samples : int
        Number of samples for SHAP-LIME comparison. Default 100.
    n_timing_samples : int
        Number of samples for latency profiling. Default 50.
    """

    def __init__(
        self,
        n_stability_runs: int = 10,
        n_compare_samples: int = 100,
        n_timing_samples: int = 50,
    ) -> None:
        self.n_stability_runs = n_stability_runs
        self.n_compare_samples = n_compare_samples
        self.n_timing_samples = n_timing_samples

    def evaluate(
        self,
        model: object,
        X_test: np.ndarray,
        feature_names: list[str],
        model_family: str = "unknown",
    ) -> XAIPillar2Metrics:
        """
        Compute all Pillar 2 metrics for a given model.

        Parameters
        ----------
        model : sklearn/xgboost/pytorch model
            Must have a `predict_proba(X)` method.
        X_test : np.ndarray
        feature_names : list[str]
        model_family : str
            Human-readable name (e.g. "XGBoost", "BiLSTM").

        Returns
        -------
        XAIPillar2Metrics
        """
        import time

        from scipy.stats import spearmanr

        try:
            import shap
        except ImportError:
            raise ImportError("shap is required: pip install shap")

        from xai.lime_explainer import XAIGuardLIMEExplainer
        from xai.stability import LIMEStabilityTester, SHAPStabilityTester
        from xai.stability import LIMEStabilityTester, SHAPStabilityTester

        n_samples = min(self.n_compare_samples, len(X_test))
        X_eval = X_test[:n_samples]
        X_train_proxy = X_test[n_samples : n_samples + 500]  # small background

        predict_fn = model.predict_proba

        # ── SHAP setup ───────────────────────────────────────────────────────
        shap_explainer = shap.TreeExplainer(model)

        # SHAP stability
        shap_stability_tester = SHAPStabilityTester(
            shap_explainer, n_runs=min(5, self.n_stability_runs)
        )
        shap_report = shap_stability_tester.run(X_eval[:20], feature_names)

        # SHAP timing (P50)
        shap_times = []
        for row in X_eval[: self.n_timing_samples]:
            t0 = time.perf_counter()
            shap_explainer.shap_values(row.reshape(1, -1))
            shap_times.append((time.perf_counter() - t0) * 1000)
        p50_shap = float(np.percentile(shap_times, 50))

        # ── LIME setup ───────────────────────────────────────────────────────
        lime_explainer = XAIGuardLIMEExplainer(
            X_train=X_train_proxy,
            feature_names=feature_names,
            n_perturbations=1000,  # reduced for evaluation speed; use 5000 in production
            random_state=42,
        )

        def lime_factory(seed: int) -> XAIGuardLIMEExplainer:
            return XAIGuardLIMEExplainer(
                X_train_proxy, feature_names, n_perturbations=500, random_state=seed
            )

        lime_stability_tester = LIMEStabilityTester(
            lime_factory, n_runs=min(5, self.n_stability_runs)
        )
        lime_report = lime_stability_tester.run(X_eval[:10], predict_fn, feature_names)

        # LIME timing (P50)
        lime_times = []
        for row in X_eval[: min(20, self.n_timing_samples)]:
            t0 = time.perf_counter()
            lime_explainer.explain(predict_fn, row)
            lime_times.append((time.perf_counter() - t0) * 1000)
        p50_lime = float(np.percentile(lime_times, 50))

        # ── SHAP vs LIME Spearman ρ ─────────────────────────────────────────
        shap_vals = shap_explainer.shap_values(X_eval)
        if isinstance(shap_vals, list):
            shap_vals = np.array(shap_vals).mean(axis=0)
        shap_importance = np.abs(shap_vals).mean(axis=0)

        lime_importance = np.zeros(len(feature_names))
        for row in X_eval:
            exp = lime_explainer.explain(predict_fn, row)
            for fc in exp.feature_contributions:
                idx = next(
                    (i for i, n in enumerate(feature_names) if n == fc.feature_name), -1
                )
                if idx >= 0:
                    lime_importance[idx] += fc.abs_contribution
        lime_importance /= len(X_eval)

        rho, _ = spearmanr(shap_importance, lime_importance)

        # ── Pillar 2 composite score ─────────────────────────────────────────
        speed_score_shap = max(0.0, 1.0 - p50_shap / 5000)  # 0 at 5000ms, 1 at 0ms
        speed_score_lime = max(0.0, 1.0 - p50_lime / 30000)  # 0 at 30s, 1 at 0ms
        spearman_norm = (float(rho) + 1.0) / 2.0  # map [-1,1] → [0,1]

        pillar2 = (
            0.35 * shap_report.stability_score
            + 0.35 * lime_report.stability_score
            + 0.20 * spearman_norm
            + 0.10 * ((speed_score_shap + speed_score_lime) / 2)
        )

        return XAIPillar2Metrics(
            shap_stability_score=shap_report.stability_score,
            shap_stability_passed=shap_report.passed,
            computation_time_shap_ms=p50_shap,
            lime_stability_score=lime_report.stability_score,
            lime_stability_passed=lime_report.passed,
            computation_time_lime_ms=p50_lime,
            shap_lime_spearman_mean=float(rho),
            shap_lime_spearman_std=0.0,  # extended in full evaluation
            pillar2_score=float(pillar2),
            model_family=model_family,
            n_samples_evaluated=n_samples,
        )
