"""Unit tests for model registry — framework enums and version schema."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../.."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../../app"))

from app.modules.registry.models import ModelFrameworkEnum, ModelStatusEnum


def test_framework_enum_covers_all_model_families():
    """Every model family in XAI-Guard must map to a framework."""
    values = {f.value for f in ModelFrameworkEnum}
    # Logistic Regression, Random Forest → SKLEARN
    assert "SKLEARN" in values
    # XGBoost → XGBOOST (has its own serialisation format .json)
    assert "XGBOOST" in values
    # LSTM, Transformer → PYTORCH
    assert "PYTORCH" in values


def test_framework_enum_values_are_uppercase():
    for fw in ModelFrameworkEnum:
        assert fw.value == fw.value.upper()


def test_status_enum_values_are_uppercase():
    for st in ModelStatusEnum:
        assert st.value == st.value.upper()


def test_model_version_required_fields():
    """Verify the domain model has all fields required by the API contract."""
    from app.modules.registry.models import ModelVersion
    column_names = {c.key for c in ModelVersion.__mapper__.columns}
    required = ["mlflow_run_id", "framework", "metrics", "status", "git_sha"]
    for field in required:
        assert field in column_names, f"ModelVersion missing required field: {field}"


def test_xgboost_has_dedicated_framework():
    """XGBoost saves as .json natively — it must not be lumped into SKLEARN."""
    assert ModelFrameworkEnum.XGBOOST != ModelFrameworkEnum.SKLEARN
