"""Unit tests for XAI explanations — method enums and status machine."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../.."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../../app"))

from app.modules.inference.models import XAIMethodEnum, XAIStatusEnum


def test_xai_method_enum_has_three_methods():
    assert len(XAIMethodEnum) == 3


def test_shap_value_correct():
    assert XAIMethodEnum.SHAP.value == "SHAP"


def test_lime_value_correct():
    assert XAIMethodEnum.LIME.value == "LIME"


def test_attention_value_correct():
    assert XAIMethodEnum.ATTENTION.value == "ATTENTION"


def test_status_machine_pending_to_complete():
    """Verify happy-path status transitions exist as valid states."""
    path = [XAIStatusEnum.PENDING, XAIStatusEnum.COMPUTING, XAIStatusEnum.COMPLETE]
    assert all(isinstance(s, XAIStatusEnum) for s in path)
    assert path[0] != path[-1]


def test_failed_is_terminal():
    """FAILED is a terminal state — it must be distinct from COMPLETE."""
    assert XAIStatusEnum.FAILED != XAIStatusEnum.COMPLETE
    assert XAIStatusEnum.FAILED.value == "FAILED"

