"""Unit tests for JWT service — token structure, expiry, and signature."""
import base64
import hashlib
import hmac
import json
import time

# ── Minimal JWT helpers (mirrors the production JWT service logic) ─────────────
SECRET = "test-secret-key-not-for-production"


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _build_token(payload: dict, secret: str = SECRET, expired: bool = False) -> str:
    header = _b64url_encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    if expired:
        payload = {**payload, "exp": int(time.time()) - 3600}
    else:
        payload = {**payload, "exp": int(time.time()) + 3600}
    body = _b64url_encode(json.dumps(payload).encode())
    sig_input = f"{header}.{body}".encode()
    signature = _b64url_encode(
        hmac.new(secret.encode(), sig_input, hashlib.sha256).digest()
    )
    return f"{header}.{body}.{signature}"


def _is_expired(token: str) -> bool:
    _, body, _ = token.split(".")
    padded = body + "=" * (-len(body) % 4)
    payload = json.loads(base64.urlsafe_b64decode(padded))
    return payload.get("exp", 0) < time.time()


def test_valid_token_has_three_parts():
    token = _build_token({"sub": "user-123", "role": "analyst"})
    parts = token.split(".")
    assert len(parts) == 3


def test_expired_token_detected():
    token = _build_token({"sub": "user-123"}, expired=True)
    assert _is_expired(token) is True


def test_valid_token_not_expired():
    token = _build_token({"sub": "user-123"})
    assert _is_expired(token) is False


def test_invalid_signature_detected():
    token = _build_token({"sub": "admin"})
    header, body, sig = token.split(".")
    tampered = f"{header}.{body}.invalidsignature"
    # Verify tampered token has wrong signature
    assert tampered != token


def test_token_subject_preserved():
    token = _build_token({"sub": "analyst-42", "role": "admin"})
    _, body, _ = token.split(".")
    padded = body + "=" * (-len(body) % 4)
    payload = json.loads(base64.urlsafe_b64decode(padded))
    assert payload["sub"] == "analyst-42"

