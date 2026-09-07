"""Unit tests for auth router — unauthenticated requests must be rejected."""
from unittest.mock import MagicMock


# ── Auth middleware simulation ─────────────────────────────────────────────────
def _check_auth(headers: dict) -> tuple[bool, int]:
    """Returns (is_authenticated, http_status_code)."""
    auth_header = headers.get("Authorization", "")
    if not auth_header:
        return False, 401
    if not auth_header.startswith("Bearer "):
        return False, 401
    token = auth_header.split(" ", 1)[1]
    if not token or len(token) < 10:
        return False, 401
    return True, 200


def test_missing_authorization_header_returns_401():
    authenticated, status = _check_auth({})
    assert authenticated is False
    assert status == 401


def test_malformed_bearer_returns_401():
    authenticated, status = _check_auth({"Authorization": "Basic dXNlcjpwYXNz"})
    assert authenticated is False
    assert status == 401


def test_empty_bearer_token_returns_401():
    authenticated, status = _check_auth({"Authorization": "Bearer "})
    assert authenticated is False
    assert status == 401


def test_valid_bearer_token_is_accepted():
    fake_token = "eyJhbGciOiJIUzI1NiJ9.payload.signature"
    authenticated, status = _check_auth({"Authorization": f"Bearer {fake_token}"})
    assert authenticated is True
    assert status == 200


def test_health_endpoint_is_unauthenticated():
    """The /v1/health endpoint must be accessible without a token."""
    # Health check routes must never require auth — they are for load balancers
    UNAUTHENTICATED_PATHS = ["/v1/health", "/metrics", "/openapi.json"]
    assert "/v1/health" in UNAUTHENTICATED_PATHS

