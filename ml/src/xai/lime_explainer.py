"""
ml/src/xai/lime_explainer.py
============================
Production LIME explainer for XAI-Guard.

LIME (Local Interpretable Model-Agnostic Explanations) approximates the model
locally by perturbing the input and fitting a simple linear surrogate model.

Key design decisions:
- random_state=42 is ALWAYS fixed in production → deterministic results
- n_perturbations=5000 minimum for 50+ feature spaces (too few → unreliable)
- discretize_continuous=False → preserves the RobustScaler output distribution
- Returns the same FeatureContribution schema as the SHAP explainer

Usage:
    from xai.lime_explainer import XAIGuardLIMEExplainer, LIMEExplanation
    explainer = XAIGuardLIMEExplainer(X_train, feature_names)
    result: LIMEExplanation = explainer.explain(model, X_test[0])
"""

from __future__ import annotations

import time
import warnings
from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np

warnings.filterwarnings("ignore", category=FutureWarning)


@dataclass
class FeatureContribution:
    """Single feature's contribution to a LIME explanation."""

    feature_name: str
    contribution: float  # signed — positive pushes toward predicted class
    abs_contribution: float  # |contribution| — used for ranking


@dataclass
class LIMEExplanation:
    """
    Complete LIME explanation for a single prediction.

    Attributes
    ----------
    predicted_class : int
        The class predicted by the model for this sample.
    predicted_proba : float
        Confidence score (probability) for the predicted class.
    feature_contributions : list[FeatureContribution]
        Sorted descending by abs_contribution — top features first.
    computation_time_ms : float
        Wall-clock time for this explanation (important for latency budgeting).
    n_perturbations : int
        Number of perturbations used — higher = more reliable but slower.
    random_state : int
        The seed used — must be 42 in production for determinism.
    intercept : float
        The local linear model's intercept term.
    local_r2 : float
        R² of the local linear surrogate — measures explanation faithfulness.
        Values below 0.5 indicate the surrogate did not fit well (caution!).
    """

    predicted_class: int
    predicted_proba: float
    feature_contributions: list[FeatureContribution]
    computation_time_ms: float
    n_perturbations: int
    random_state: int
    intercept: float
    local_r2: float

    def top_k(self, k: int = 10) -> list[FeatureContribution]:
        """Return the top-k most important features."""
        return self.feature_contributions[:k]

    def as_dict(self) -> dict[str, Any]:
        """Serialise to a plain dict (for MLflow logging and API responses)."""
        return {
            "predicted_class": self.predicted_class,
            "predicted_proba": round(self.predicted_proba, 4),
            "top_features": [
                {"name": fc.feature_name, "contribution": round(fc.contribution, 6)}
                for fc in self.top_k(10)
            ],
            "computation_time_ms": round(self.computation_time_ms, 2),
            "n_perturbations": self.n_perturbations,
            "local_r2": round(self.local_r2, 4),
        }


class XAIGuardLIMEExplainer:
    """
    Production-grade LIME explainer for XAI-Guard.

    Why LIME alongside SHAP?
    ------------------------
    SHAP is mathematically exact (Shapley values). LIME is model-agnostic and
    faster. When SHAP and LIME agree on the top features, analyst trust increases.
    When they disagree, it signals the model may be relying on non-intuitive
    feature interactions worth investigating.

    Parameters
    ----------
    X_train : np.ndarray
        Training data distribution used as the background for perturbations.
        LIME perturbs around the training distribution — this must be the same
        data the model was trained on.
    feature_names : list[str]
        Names of the features in the same order as X_train columns.
    n_perturbations : int
        Number of perturbed samples for the local surrogate. Min 5000 for 50+
        feature spaces. More = reliable but slower.
    random_state : int
        Fixed to 42 in production. Changing this changes feature rankings —
        never expose as a user parameter in the production API.
    class_names : list[str] | None
        Human-readable class names for the prediction (e.g. ["BENIGN", "ATTACK"]).
    """

    def __init__(
        self,
        X_train: np.ndarray,
        feature_names: list[str],
        n_perturbations: int = 5000,
        random_state: int = 42,
        class_names: list[str] | None = None,
    ) -> None:
        try:
            from lime.lime_tabular import LimeTabularExplainer
        except ImportError as exc:
            raise ImportError(
                "lime is not installed. Run: pip install lime==0.2.0.1"
            ) from exc

        self.feature_names = feature_names
        self.n_perturbations = n_perturbations
        self.random_state = random_state
        self.class_names = class_names or [str(i) for i in range(10)]

        # Build the LIME explainer once (expensive — reuse for all predictions)
        self._lime_explainer = LimeTabularExplainer(
            training_data=X_train,
            feature_names=feature_names,
            class_names=self.class_names,
            mode="classification",
            discretize_continuous=False,  # preserve RobustScaler output
            random_state=random_state,
        )

    def explain(
        self,
        predict_fn: Callable[[np.ndarray], np.ndarray],
        X_sample: np.ndarray,
        label: int = 1,
    ) -> LIMEExplanation:
        """
        Compute a LIME explanation for a single sample.

        Parameters
        ----------
        predict_fn : callable
            A function that accepts X (n_samples, n_features) and returns
            a probability matrix (n_samples, n_classes). Typically model.predict_proba.
        X_sample : np.ndarray
            A single sample, shape (n_features,).
        label : int
            The class label to explain (default 1 = attack class).

        Returns
        -------
        LIMEExplanation
            Sorted descending by |contribution| — top features first.

        Notes
        -----
        local_r2 < 0.5 means the linear surrogate did not fit the local
        decision boundary well. Treat explanations with low R² with caution.
        """
        if X_sample.ndim == 2:
            X_sample = X_sample[0]

        t0 = time.perf_counter()

        exp = self._lime_explainer.explain_instance(
            data_row=X_sample,
            predict_fn=predict_fn,
            num_features=len(self.feature_names),
            num_samples=self.n_perturbations,
            labels=(label,),
        )

        elapsed_ms = (time.perf_counter() - t0) * 1000

        # Extract contributions for the requested label
        raw_contributions: list[tuple[str, float]] = exp.as_list(label=label)

        # Sort by absolute value descending
        contributions = sorted(
            [
                FeatureContribution(
                    feature_name=name,
                    contribution=value,
                    abs_contribution=abs(value),
                )
                for name, value in raw_contributions
            ],
            key=lambda fc: fc.abs_contribution,
            reverse=True,
        )

        # Extract predicted class and probability
        proba_vector = predict_fn(X_sample.reshape(1, -1))[0]
        predicted_class = int(np.argmax(proba_vector))
        predicted_proba = float(proba_vector[predicted_class])

        # Local R² measures surrogate faithfulness
        local_r2 = float(exp.score) if hasattr(exp, "score") else 0.0
        intercept = float(exp.intercept[label]) if hasattr(exp, "intercept") else 0.0

        return LIMEExplanation(
            predicted_class=predicted_class,
            predicted_proba=predicted_proba,
            feature_contributions=contributions,
            computation_time_ms=elapsed_ms,
            n_perturbations=self.n_perturbations,
            random_state=self.random_state,
            intercept=intercept,
            local_r2=local_r2,
        )

    def explain_batch(
        self,
        predict_fn: Callable[[np.ndarray], np.ndarray],
        X_batch: np.ndarray,
        label: int = 1,
    ) -> list[LIMEExplanation]:
        """Explain multiple samples. Returns explanations in the same order."""
        return [self.explain(predict_fn, row, label) for row in X_batch]
