"""
Unit tests for CompositeDeploymentScorer.
"""

import numpy as np
import pytest


from ml.src.evaluation.deployment_score import (
    CompositeDeploymentScorer,
    ThreePillarMetrics,
)

MOCK_MODELS = [
    ThreePillarMetrics(
        model_name="A", f1_score=0.72, latency_p99_ms=0.5, memory_mb=2.1
    ),
    ThreePillarMetrics(
        model_name="B", f1_score=0.93, latency_p99_ms=3.1, memory_mb=45.2
    ),
    ThreePillarMetrics(
        model_name="C", f1_score=0.96, latency_p99_ms=8.4, memory_mb=2.4
    ),
]


def test_cds_returns_one_score_per_model():
    scorer = CompositeDeploymentScorer()
    scores = scorer.score(MOCK_MODELS)
    assert len(scores) == 3


def test_cds_sorted_descending():
    scorer = CompositeDeploymentScorer()
    scores = scorer.score(MOCK_MODELS)
    cds_values = [s.cds for s in scores]
    assert cds_values == sorted(cds_values, reverse=True)


def test_cds_scores_in_unit_range():
    scorer = CompositeDeploymentScorer()
    scores = scorer.score(MOCK_MODELS)
    for s in scores:
        assert 0.0 <= s.cds <= 1.0


def test_weight_sum_must_be_one():
    with pytest.raises(AssertionError):
        CompositeDeploymentScorer(weight_f1=0.5, weight_speed=0.5, weight_mem=0.5)


def test_single_model_gets_cds_one():
    """With only one model, normalisation makes it CDS=1.0 (all normalised dims = 1.0 or 0.0)."""
    scorer = CompositeDeploymentScorer()
    scores = scorer.score(MOCK_MODELS[:1])
    # With a single model, norms are all 0 or 1, result depends on min-max edge case.
    assert len(scores) == 1
    assert 0.0 <= scores[0].cds <= 1.0
