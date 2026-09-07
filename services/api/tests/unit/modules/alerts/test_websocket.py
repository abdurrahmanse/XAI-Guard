"""Unit tests for WebSocket alert messages — schema structure and payload."""
import json
import time


def _build_alert_message(prediction_id: str, severity: str,
                          predicted_class: str, confidence: float) -> dict:
    """Builds the WebSocket alert message payload."""
    return {
        "type": "ALERT",
        "prediction_id": prediction_id,
        "severity_level": severity,
        "predicted_class": predicted_class,
        "confidence_score": confidence,
        "timestamp": time.time(),
    }


def test_alert_message_type_is_correct():
    msg = _build_alert_message("pred-001", "CRITICAL", "DDoS", 0.98)
    assert msg["type"] == "ALERT"


def test_alert_message_has_all_required_fields():
    msg = _build_alert_message("pred-001", "HIGH", "PortScan", 0.87)
    for field in ["type", "prediction_id", "severity_level",
                   "predicted_class", "confidence_score", "timestamp"]:
        assert field in msg, f"Missing field: {field}"


def test_alert_message_is_json_serialisable():
    msg = _build_alert_message("pred-002", "MEDIUM", "BruteForce", 0.74)
    serialised = json.dumps(msg)
    recovered = json.loads(serialised)
    assert recovered["prediction_id"] == "pred-002"


def test_confidence_score_is_in_valid_range():
    msg = _build_alert_message("pred-003", "LOW", "BENIGN", 0.55)
    assert 0.0 <= msg["confidence_score"] <= 1.0


def test_timestamp_is_recent():
    msg = _build_alert_message("pred-004", "HIGH", "Infiltration", 0.91)
    # Timestamp must be within the last 5 seconds
    assert abs(msg["timestamp"] - time.time()) < 5

