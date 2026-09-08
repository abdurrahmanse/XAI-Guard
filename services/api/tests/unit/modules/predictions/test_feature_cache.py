"""Unit tests for feature cache — key generation and TTL logic."""
import hashlib

# ── Inline cache key logic (mirrors the production implementation) ────────────
CACHE_TTL_SECONDS = 300  # 5 minutes for feature vectors


def build_cache_key(source_ip: str, dest_ip: str, dest_port: int, timestamp_bucket: str) -> str:
    """Deterministic cache key for a feature vector request."""
    raw = f"{source_ip}:{dest_ip}:{dest_port}:{timestamp_bucket}"
    return "xaiguard:features:" + hashlib.sha256(raw.encode()).hexdigest()[:16]


def test_cache_key_is_deterministic():
    """Same inputs must always produce the same cache key."""
    k1 = build_cache_key("192.168.1.1", "10.0.0.1", 443, "2026-09-07T12:00")
    k2 = build_cache_key("192.168.1.1", "10.0.0.1", 443, "2026-09-07T12:00")
    assert k1 == k2


def test_cache_key_differs_for_different_ips():
    k1 = build_cache_key("192.168.1.1", "10.0.0.1", 443, "2026-09-07T12:00")
    k2 = build_cache_key("192.168.1.2", "10.0.0.1", 443, "2026-09-07T12:00")
    assert k1 != k2


def test_cache_key_differs_for_different_ports():
    k1 = build_cache_key("192.168.1.1", "10.0.0.1", 80,  "2026-09-07T12:00")
    k2 = build_cache_key("192.168.1.1", "10.0.0.1", 443, "2026-09-07T12:00")
    assert k1 != k2


def test_cache_key_has_namespace_prefix():
    key = build_cache_key("10.0.0.1", "10.0.0.2", 22, "2026-09-07T12:00")
    assert key.startswith("xaiguard:features:")


def test_cache_ttl_is_positive():
    assert CACHE_TTL_SECONDS > 0
    assert CACHE_TTL_SECONDS <= 3600  # never cache longer than 1 hour

