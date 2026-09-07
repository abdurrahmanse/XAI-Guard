"""Unit tests for security event ingestion — protocol enums and field validation."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../.."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../../app"))

from app.modules.events.models import ProtocolEnum, DatasetSourceEnum


def test_protocol_enum_covers_common_protocols():
    values = {p.value for p in ProtocolEnum}
    assert "TCP" in values
    assert "UDP" in values
    assert "ICMP" in values
    assert "OTHER" in values  # catch-all for unknown protocols


def test_dataset_source_covers_all_four_benchmarks():
    """All four research datasets must be represented."""
    values = {d.value for d in DatasetSourceEnum}
    assert "NSL_KDD" in values
    assert "CICIDS_2017" in values
    assert "UNSW_NB15" in values
    assert "BETH" in values


def test_dataset_source_includes_live():
    """Production live traffic must be a valid source."""
    assert "LIVE" in {d.value for d in DatasetSourceEnum}


def test_protocol_enum_values_are_uppercase():
    for p in ProtocolEnum:
        assert p.value == p.value.upper()


def test_security_event_required_fields():
    from app.modules.events.models import SecurityEvent
    # SQLAlchemy uses __mapper__.columns for the real field list
    column_names = {c.key for c in SecurityEvent.__mapper__.columns}
    required = ["source_ip", "destination_ip", "source_port",
                "destination_port", "protocol", "features", "dataset_source"]
    for field in required:
        assert field in column_names, f"SecurityEvent missing: {field}"
