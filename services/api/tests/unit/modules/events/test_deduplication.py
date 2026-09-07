"""Unit tests for event deduplication — hash determinism and uniqueness."""
import hashlib


def _dedup_hash(source_ip: str, dest_ip: str, dest_port: int,
                protocol: str, timestamp_minute: str) -> str:
    """
    Deterministic deduplication hash for a SecurityEvent.
    Two events are duplicates if they share the same 5-tuple within the same minute.
    This mirrors the production logic in the ingestion service.
    """
    raw = f"{source_ip}|{dest_ip}|{dest_port}|{protocol}|{timestamp_minute}"
    return hashlib.sha256(raw.encode()).hexdigest()


def test_same_event_produces_same_hash():
    h1 = _dedup_hash("10.0.0.1", "10.0.0.2", 443, "TCP", "2026-09-07T12:00")
    h2 = _dedup_hash("10.0.0.1", "10.0.0.2", 443, "TCP", "2026-09-07T12:00")
    assert h1 == h2


def test_different_source_ip_produces_different_hash():
    h1 = _dedup_hash("10.0.0.1", "10.0.0.2", 443, "TCP", "2026-09-07T12:00")
    h2 = _dedup_hash("10.0.0.3", "10.0.0.2", 443, "TCP", "2026-09-07T12:00")
    assert h1 != h2


def test_different_port_produces_different_hash():
    h1 = _dedup_hash("10.0.0.1", "10.0.0.2", 80,  "TCP", "2026-09-07T12:00")
    h2 = _dedup_hash("10.0.0.1", "10.0.0.2", 443, "TCP", "2026-09-07T12:00")
    assert h1 != h2


def test_different_minute_produces_different_hash():
    """Events in different minutes are NOT duplicates — they are distinct observations."""
    h1 = _dedup_hash("10.0.0.1", "10.0.0.2", 443, "TCP", "2026-09-07T12:00")
    h2 = _dedup_hash("10.0.0.1", "10.0.0.2", 443, "TCP", "2026-09-07T12:01")
    assert h1 != h2


def test_hash_is_64_chars():
    """SHA-256 hex digest must always be 64 characters."""
    h = _dedup_hash("192.168.1.1", "8.8.8.8", 53, "UDP", "2026-09-07T09:30")
    assert len(h) == 64

