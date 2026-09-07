"""
Analyst Utility Score (AUS) — Pillar 2 summary metric.

AUS = 0.25 × Conciseness + 0.25 × Consistency + 0.20 × Speed
    + 0.20 × SHAP_LIME_Agreement + 0.10 × Additivity

Extracted from: ml/notebooks/xai/02_lime_shap_correlation.ipynb
"""

from __future__ import annotations

from pydantic import BaseModel


class AnalystUtilityMetrics(BaseModel):
    """Raw sub-metrics for a single model's XAI evaluation."""

    model_name: str
    conciseness: float  # fraction where top-5 features explain >80% |SHAP|
    consistency: float  # same top-5 features for same attack type across samples
    speed_norm: float  # relative XAI computation time, normalised [0, 1]
    shap_lime_agreement: float  # mean Spearman ρ from Phase 39.4
    additivity_compliance: float  # binary check: 1.0 = pass, 0.0 = fail


class AnalystUtilityScore(BaseModel):
    """Final AUS composite score for a single model."""

    model_name: str
    aus: float
    conciseness: float
    consistency: float
    speed_norm: float
    shap_lime_agreement: float
    additivity_compliance: float


class AnalystUtilityScorer:
    """
    Compute the Analyst Utility Score (AUS) for each model.

    Weights follow the Phase 1.3 evaluation framework spec:
      - Conciseness:          0.25
      - Consistency:          0.25
      - Speed:                0.20
      - SHAP-LIME Agreement:  0.20
      - Additivity:           0.10
    """

    WEIGHTS = {
        "conciseness": 0.25,
        "consistency": 0.25,
        "speed_norm": 0.20,
        "shap_lime_agreement": 0.20,
        "additivity_compliance": 0.10,
    }

    def score(
        self, metrics_list: list[AnalystUtilityMetrics]
    ) -> list[AnalystUtilityScore]:
        """Compute AUS for every model in *metrics_list*."""
        results = []
        for m in metrics_list:
            aus = (
                self.WEIGHTS["conciseness"] * m.conciseness
                + self.WEIGHTS["consistency"] * m.consistency
                + self.WEIGHTS["speed_norm"] * m.speed_norm
                + self.WEIGHTS["shap_lime_agreement"] * m.shap_lime_agreement
                + self.WEIGHTS["additivity_compliance"] * m.additivity_compliance
            )
            results.append(
                AnalystUtilityScore(
                    model_name=m.model_name,
                    aus=round(aus, 4),
                    conciseness=m.conciseness,
                    consistency=m.consistency,
                    speed_norm=m.speed_norm,
                    shap_lime_agreement=m.shap_lime_agreement,
                    additivity_compliance=m.additivity_compliance,
                )
            )
        return sorted(results, key=lambda x: x.aus, reverse=True)
