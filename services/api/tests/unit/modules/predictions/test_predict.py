"""Unit tests for prediction domain — SeverityEnum and XAIStatusEnum."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../.."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../../app"))

from app.modules.inference.models import SeverityEnum, XAIStatusEnum, XAIMethodEnum


def test_severity_enum_has_four_levels():
    assert set(SeverityEnum) == {SeverityEnum.LOW, SeverityEnum.MEDIUM,
                                  SeverityEnum.HIGH, SeverityEnum.CRITICAL}


def test_severity_enum_values_are_strings():
    for level in SeverityEnum:
        assert isinstance(level.value, str)
        assert level.value == level.value.upper()


def test_severity_ordering_by_name():
    """CRITICAL must be the most severe — verify name ordering."""
    names = [s.value for s in SeverityEnum]
    assert "CRITICAL" in names
    assert "LOW" in names


def test_xai_status_transitions():
    """Verify all expected XAI lifecycle states exist."""
    assert XAIStatusEnum.PENDING.value == "PENDING"
    assert XAIStatusEnum.COMPUTING.value == "COMPUTING"
    assert XAIStatusEnum.COMPLETE.value == "COMPLETE"
    assert XAIStatusEnum.FAILED.value == "FAILED"


def test_xai_method_enum_covers_all_explainers():
    methods = {m.value for m in XAIMethodEnum}
    assert "SHAP" in methods
    assert "LIME" in methods
    assert "ATTENTION" in methods

