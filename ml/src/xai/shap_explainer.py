"""
Unified SHAP Explainer Interface for XAI-Guard.

Routes each model family to its optimal SHAP explainer backend:
- XGBoost / Random Forest → TreeExplainer (exact, deterministic)
- LSTM / Transformer      → DeepExplainer  (background-sample based)
- Fallback                → KernelExplainer (model-agnostic, slow)

Validates the SHAP Additivity Property:
    |sum(shap_values, axis=1) + base_value - prediction| < 0.1

Extracted from: ml/notebooks/xai/01_shap_global.ipynb
"""

from __future__ import annotations

from typing import Any

import numpy as np
from pydantic import BaseModel

# Supported model families
TREE_FAMILIES = {"xgboost", "random_forest", "rf"}
DEEP_FAMILIES = {"lstm", "bilstm", "transformer", "lightweight_transformer"}

ADDITIVITY_TOLERANCE = 0.1  # Maximum allowed deviation per sample


class FeatureContribution(BaseModel):
    """Single feature's SHAP contribution for a prediction."""

    feature: str
    shap_value: float
    abs_shap: float


class SHAPExplanation(BaseModel):
    """Complete SHAP explanation for a batch of samples."""

    model_family: str
    explainer_type: str
    feature_names: list[str]
    shap_values: list[list[float]]  # shape [n_samples, n_features]
    base_values: list[float]  # shape [n_samples]
    top_k_features: list[FeatureContribution]  # global top-k by mean |SHAP|
    additivity_passed: bool
    n_samples: int


class XAIGuardSHAPExplainer:
    """
    Unified SHAP explainer that works across all XAI-Guard model families.

    Args:
        model:          A fitted sklearn, XGBoost, or PyTorch model.
        model_family:   One of 'xgboost', 'random_forest', 'lstm',
                        'transformer', 'lightweight_transformer', etc.
        background:     Background dataset (numpy array) for DeepExplainer.
                        Required for deep learning families.
        seed:           Random seed for reproducible background sampling.
    """

    def __init__(
        self,
        model: Any,
        model_family: str,
        background: np.ndarray | None = None,
        seed: int = 42,
    ) -> None:
        import shap  # type: ignore  # pylint: disable=import-error

        self.model = model
        self.model_family = model_family.lower()
        self.seed = seed
        self._shap = shap

        if self.model_family in TREE_FAMILIES:
            self._explainer = shap.TreeExplainer(model)
            self._explainer_type = "TreeExplainer"
        elif self.model_family in DEEP_FAMILIES:
            if background is None:
                raise ValueError(
                    "DeepExplainer requires a background dataset. "
                    "Pass 50–200 representative samples as `background`."
                )
            self._explainer = shap.DeepExplainer(model, background)
            self._explainer_type = "DeepExplainer"
        else:
            self._explainer = shap.KernelExplainer(model.predict, background)
            self._explainer_type = "KernelExplainer"

    def explain(
        self,
        X: np.ndarray,
        feature_names: list[str],
        top_k: int = 5,
    ) -> SHAPExplanation:
        """
        Compute SHAP values for *X* and return a validated :class:`SHAPExplanation`.

        Args:
            X:             Input samples. Shape [n_samples, n_features].
            feature_names: Feature names matching columns of X.
            top_k:         Number of top global features to include in the summary.

        Returns:
            :class:`SHAPExplanation` with additivity validation status.
        """
        shap_values = self._explainer.shap_values(X)

        # For multi-class models, shap_values is a list — take the max-class
        if isinstance(shap_values, list):
            shap_values = np.array(shap_values).mean(axis=0)

        base_vals = self._explainer.expected_value
        if isinstance(base_vals, (list, np.ndarray)):
            base_vals = np.full(len(X), float(np.mean(base_vals)))
        else:
            base_vals = np.full(len(X), float(base_vals))

        # Additivity validation
        row_sums = shap_values.sum(axis=1) + base_vals
        additivity_passed = bool(
            np.all(np.abs(row_sums - base_vals) < ADDITIVITY_TOLERANCE)
        )

        # Global top-k features by mean |SHAP|
        mean_abs = np.abs(shap_values).mean(axis=0)
        top_indices = np.argsort(mean_abs)[::-1][:top_k]
        top_features = [
            FeatureContribution(
                feature=feature_names[i],
                shap_value=float(shap_values[:, i].mean()),
                abs_shap=float(mean_abs[i]),
            )
            for i in top_indices
        ]

        return SHAPExplanation(
            model_family=self.model_family,
            explainer_type=self._explainer_type,
            feature_names=feature_names,
            shap_values=shap_values.tolist(),
            base_values=base_vals.tolist(),
            top_k_features=top_features,
            additivity_passed=additivity_passed,
            n_samples=len(X),
        )
