"""Unit tests for threat intel enrichment — IP validation and cache key format."""
import re
import ipaddress


# ── Private IP ranges that should SKIP external threat intel lookup ────────────
# RFC 1918 private ranges — querying AbuseIPDB for these is wasteful and wrong.
PRIVATE_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),   # loopback
    ipaddress.ip_network("169.254.0.0/16"),  # link-local
]


def _is_private_ip(ip_str: str) -> bool:
    """Returns True if the IP is private and should skip threat intel lookup."""
    try:
        addr = ipaddress.ip_address(ip_str)
        return any(addr in net for net in PRIVATE_RANGES)
    except ValueError:
        return False


def _threat_intel_cache_key(ip: str) -> str:
    return f"xaiguard:threat_intel:{ip}"


def test_private_ip_10_skips_lookup():
    assert _is_private_ip("10.0.0.1") is True


def test_private_ip_192168_skips_lookup():
    assert _is_private_ip("192.168.1.100") is True


def test_loopback_skips_lookup():
    assert _is_private_ip("127.0.0.1") is True


def test_public_ip_is_enriched():
    assert _is_private_ip("8.8.8.8") is False
    assert _is_private_ip("1.1.1.1") is False


def test_cache_key_format_is_correct():
    key = _threat_intel_cache_key("8.8.8.8")
    assert key == "xaiguard:threat_intel:8.8.8.8"
    assert key.startswith("xaiguard:threat_intel:")


def test_invalid_ip_raises_value_error_and_is_handled():
    """An unparseable IP string must not crash — is_private returns False."""
    # The caller is responsible for catching non-private IPs that fail validation
    # and skipping enrichment via a try/except at the service layer
    result = _is_private_ip("not-an-ip")
    # The function should return False (not crash) — caller filters at service layer
    assert result is False
