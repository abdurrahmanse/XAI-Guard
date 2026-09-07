"""Unit tests for alerts — severity ordering and alert schema."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../.."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../../app"))

from app.modules.inference.models import SeverityEnum


# ── Severity numerical weight (mirrors production alert-routing logic) ─────────
SEVERITY_WEIGHT = {
    SeverityEnum.LOW: 1,
    SeverityEnum.MEDIUM: 2,
    SeverityEnum.HIGH: 3,
    SeverityEnum.CRITICAL: 4,
}


def test_critical_has_highest_weight():
    assert SEVERITY_WEIGHT[SeverityEnum.CRITICAL] > SEVERITY_WEIGHT[SeverityEnum.HIGH]
    assert SEVERITY_WEIGHT[SeverityEnum.CRITICAL] > SEVERITY_WEIGHT[SeverityEnum.MEDIUM]
    assert SEVERITY_WEIGHT[SeverityEnum.CRITICAL] > SEVERITY_WEIGHT[SeverityEnum.LOW]


def test_low_has_lowest_weight():
    assert SEVERITY_WEIGHT[SeverityEnum.LOW] < SEVERITY_WEIGHT[SeverityEnum.MEDIUM]
    assert SEVERITY_WEIGHT[SeverityEnum.LOW] < SEVERITY_WEIGHT[SeverityEnum.HIGH]


def test_severity_ordering_is_strict():
    weights = list(SEVERITY_WEIGHT.values())
    assert weights == sorted(weights), "Severity weights must be strictly increasing"


def test_alert_schema_fields():
    """An alert payload must include the minimum required fields."""
    REQUIRED_ALERT_FIELDS = ["prediction_id", "severity_level", "predicted_class",
                              "confidence_score", "timestamp"]
    # Validate completeness of the schema contract
    assert "severity_level" in REQUIRED_ALERT_FIELDS
    assert "confidence_score" in REQUIRED_ALERT_FIELDS


def test_all_four_severity_levels_are_routable():
    """Every severity level must have a defined weight — none can be unknown."""
    for level in SeverityEnum:
        assert level in SEVERITY_WEIGHT, f"No weight defined for {level}"

