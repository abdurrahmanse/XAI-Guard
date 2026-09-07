"""
Composite Deployment Score (CDS) computation.
Pillar 3 summary metric: balances F1, latency, and memory footprint.

CDS = 0.40 × norm_f1 + 0.35 × norm_speed + 0.25 × norm_memory

Extracted from: ml/notebooks/28_quantisation_profiling.ipynb
"""

from __future__ import annotations

import numpy as np
from pydantic import BaseModel


class ThreePillarMetrics(BaseModel):
    """Raw evaluation metrics for a single model across all three pillars."""

    model_name: str
    f1_score: float
    latency_p99_ms: float
    memory_mb: float


class DeploymentScore(BaseModel):
    """Final Composite Deployment Score for a single model."""

    model_name: str
    cds: float
    norm_f1: float
    norm_speed: float
    norm_memory: float


class CompositeDeploymentScorer:
    """
    Computes the Composite Deployment Score (CDS) for a list of models.

    All three input dimensions are min-max normalised so they are on the same
    [0, 1] scale before weighting.  Latency and memory are inverted (lower is
    better), so the normalised scores represent *speed* and *compactness*.

    Args:
        weight_f1:    Weight for the accuracy pillar.  Default 0.40.
        weight_speed: Weight for the latency pillar.   Default 0.35.
        weight_mem:   Weight for the memory pillar.    Default 0.25.
    """

    def __init__(
        self,
        weight_f1: float = 0.40,
        weight_speed: float = 0.35,
        weight_mem: float = 0.25,
    ) -> None:
        assert abs(weight_f1 + weight_speed + weight_mem - 1.0) < 1e-6, (
            "Weights must sum to 1.0"
        )
        self.weight_f1 = weight_f1
        self.weight_speed = weight_speed
        self.weight_mem = weight_mem

    def _minmax(self, arr: np.ndarray) -> np.ndarray:
        rng = arr.max() - arr.min() + 1e-9
        return (arr - arr.min()) / rng

    def score(self, metrics_list: list[ThreePillarMetrics]) -> list[DeploymentScore]:
        """
        Compute CDS for every model in *metrics_list*.

        Returns a list of :class:`DeploymentScore` objects sorted by CDS
        descending (highest = best production fit).
        """
        f1_vec = np.array([m.f1_score for m in metrics_list])
        lat_vec = np.array([m.latency_p99_ms for m in metrics_list])
        mem_vec = np.array([m.memory_mb for m in metrics_list])

        norm_f1 = self._minmax(f1_vec)
        # Invert: lower latency → higher normalised speed
        norm_speed = self._minmax(1.0 / (lat_vec + 1e-9))
        # Invert: lower memory → higher normalised compactness
        norm_mem = self._minmax(1.0 / (mem_vec + 1e-9))

        cds = (
            self.weight_f1 * norm_f1
            + self.weight_speed * norm_speed
            + self.weight_mem * norm_mem
        )

        results = [
            DeploymentScore(
                model_name=metrics_list[i].model_name,
                cds=float(cds[i]),
                norm_f1=float(norm_f1[i]),
                norm_speed=float(norm_speed[i]),
                norm_memory=float(norm_mem[i]),
            )
            for i in range(len(metrics_list))
        ]
        return sorted(results, key=lambda x: x.cds, reverse=True)
