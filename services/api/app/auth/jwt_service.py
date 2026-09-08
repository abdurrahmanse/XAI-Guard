"""
services/api/app/auth/jwt_service.py — JWT Token Management (Phase 47.1)
========================================================================
HS256-signed JWT access tokens (30-min expiry) and refresh tokens
(7-day, stored as SHA-256 hash in Redis for revocation).

Key security properties:
- jti (JWT ID) UUID4 in every token → enables per-token revocation
- Refresh token stored as sha256(token) in Redis, NOT the token itself
  → if Redis is compromised, tokens cannot be forged
- Access tokens are stateless (not stored) → validate by signature + claims only
- Refresh token rotation: using a refresh token invalidates it and issues a new one

TOKEN CLAIMS:
    sub       — user UUID
    username  — for logging (not authorisation)
    role      — used by RBAC checks in all module dependencies
    exp       — expiry timestamp
    iat       — issued-at timestamp
    jti       — UUID4 for revocation

USAGE:
    service = JWTService()
    access_token = service.create_access_token("user-id", "alice", "analyst")
    payload = service.verify_access_token(access_token)
    print(payload.role)  # "analyst"
"""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from typing import Literal

from pydantic import BaseModel


class TokenPayload(BaseModel):
    """
    Decoded JWT access token payload.

    All fields are validated by Pydantic — an invalid token raises
    immediately during model_validate(), not somewhere in the handler.
    """

    sub: str  # user UUID (string form)
    username: str
    role: Literal["admin", "analyst", "readonly"]
    exp: datetime
    iat: datetime
    jti: str  # UUID4 string


class TokenResponse(BaseModel):
    """Returned by POST /v1/auth/login and POST /v1/auth/refresh."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in_seconds: int


class JWTService:
    """
    JWT token creation, verification, and refresh token management.

    Parameters
    ----------
    secret_key : str
        HS256 signing secret. Must be > 32 chars in production.
    algorithm : str
        Signing algorithm. Default "HS256".
    access_expire_minutes : int
        Access token lifetime. Default 30.
    refresh_expire_days : int
        Refresh token lifetime. Default 7.
    """

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_expire_minutes: int = 30,
        refresh_expire_days: int = 7,
    ) -> None:
        try:
            from jose import jwt as jose_jwt

            self._jwt = jose_jwt
        except ImportError as exc:
            raise ImportError(
                "python-jose[cryptography] required: pip install python-jose[cryptography]"
            ) from exc

        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_expire_minutes = access_expire_minutes
        self.refresh_expire_days = refresh_expire_days

    def create_access_token(
        self,
        user_id: str,
        username: str,
        role: str,
        expire_minutes: int | None = None,
    ) -> str:
        """
        Create a signed JWT access token.

        Returns
        -------
        str
            The encoded JWT string. Store this nowhere — it is stateless.
        """
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=expire_minutes or self.access_expire_minutes
        )
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "username": username,
            "role": role,
            "exp": expire,
            "iat": now,
            "jti": str(uuid.uuid4()),
        }
        return self._jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: str) -> tuple[str, str]:
        """
        Create a refresh token and return (token_string, jti).

        The caller must store sha256(token_string) in Redis keyed by jti.

        Returns
        -------
        tuple[str, str]
            (refresh_token, jti)
        """
        jti = str(uuid.uuid4())
        expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_expire_days)
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "jti": jti,
        }
        token = self._jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token, jti

    def verify_access_token(self, token: str) -> TokenPayload:
        """
        Decode and validate a JWT access token.

        Raises
        ------
        CredentialsException
            If the token is expired, malformed, missing required claims,
            or signed with the wrong secret.
        """
        from jose import JWTError

        from app.core.exceptions import CredentialsException

        try:
            raw = self._jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError as exc:
            raise CredentialsException(
                detail=f"Token validation failed: {exc}", instance="/v1/auth"
            ) from exc

        try:
            return TokenPayload.model_validate(raw)
        except Exception as exc:
            raise CredentialsException(
                detail="Token payload is missing required claims", instance="/v1/auth"
            ) from exc

    @staticmethod
    def _hash_token(token: str) -> str:
        """SHA-256 hash of a refresh token for safe Redis storage."""
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def redis_key(jti: str) -> str:
        """Redis key for a refresh token by its jti."""
        return f"refresh:{jti}"

    async def store_refresh_token(self, jti: str, token: str, redis_client) -> None:
        """
        Store sha256(token) in Redis with 7-day TTL.

        We store the HASH not the token — so Redis exposure does not
        allow forging tokens.
        """
        ttl_seconds = self.refresh_expire_days * 86400
        await redis_client.setex(
            self.redis_key(jti),
            ttl_seconds,
            self._hash_token(token),
        )

    async def is_refresh_token_valid(self, jti: str, token: str, redis_client) -> bool:
        """
        Validate a refresh token by comparing its hash to the stored hash.

        Returns False if the token was revoked or never stored.
        """
        stored_hash = await redis_client.get(self.redis_key(jti))
        if not stored_hash:
            return False
        return stored_hash == self._hash_token(token)

    async def revoke_refresh_token(self, jti: str, redis_client) -> None:
        """Delete the refresh token from Redis (logout / token rotation)."""
        await redis_client.delete(self.redis_key(jti))
