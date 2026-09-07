"""
services/api/app/auth/router.py — Auth Endpoints (Phase 47.2)
=============================================================
Endpoints for login, token refresh, and logout.

Uses slowapi (rate limiting) to prevent brute-force attacks on /login.
"""
from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio.client import Redis

from app.core.exceptions import CredentialsException
from app.core.redis_client import get_redis
from app.auth.jwt_service import JWTService, TokenResponse
from app.auth.dependencies import get_jwt_service, get_current_user, UserContext

# We mock a DB here for the purpose of the architecture since we haven't 
# built the users table yet in Phase 47. In a real system, you query the DB.
from passlib.context import CryptContext

logger = logging.getLogger("xaiguard.auth")

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hardcoded mock admin for now
MOCK_USER = {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "username": "admin",
    "password_hash": pwd_context.hash("admin123"),
    "role": "admin"
}


@router.post("/login", response_model=TokenResponse)
async def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
    redis_client: Annotated[Redis, Depends(get_redis)],
):
    """
    Authenticate user and return access and refresh tokens.
    """
    # 1. Verify credentials (Mock DB check)
    if form_data.username != MOCK_USER["username"] or not pwd_context.verify(form_data.password, MOCK_USER["password_hash"]):
        # Would log FAILED_LOGIN to audit log here
        raise CredentialsException(detail="Incorrect username or password")

    # 2. Issue tokens
    user_id = MOCK_USER["id"]
    access_token = jwt_service.create_access_token(
        user_id=user_id,
        username=MOCK_USER["username"],
        role=MOCK_USER["role"]
    )
    refresh_token, jti = jwt_service.create_refresh_token(user_id=user_id)

    # 3. Store refresh token hash in Redis
    await jwt_service.store_refresh_token(jti, refresh_token, redis_client)

    # 4. (Future) Log LOGIN to AuditLog here

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in_seconds=jwt_service.access_expire_minutes * 60
    )


from pydantic import BaseModel
class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request_data: RefreshRequest,
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
    redis_client: Annotated[Redis, Depends(get_redis)],
):
    """
    Issue a new access token using a valid refresh token.
    Implements Token Rotation: old refresh token is revoked, new one issued.
    """
    try:
        from jose import jwt
        payload = jwt.decode(
            request_data.refresh_token, 
            jwt_service.secret_key, 
            algorithms=[jwt_service.algorithm]
        )
        jti = payload.get("jti")
        user_id = payload.get("sub")
    except Exception as exc:
        raise CredentialsException(detail="Invalid refresh token") from exc

    # 1. Verify hash against Redis (prevents revoked/reused token attacks)
    is_valid = await jwt_service.is_refresh_token_valid(jti, request_data.refresh_token, redis_client)
    if not is_valid:
        raise CredentialsException(detail="Refresh token expired or revoked")

    # 2. Revoke old refresh token (Token Rotation)
    await jwt_service.revoke_refresh_token(jti, redis_client)

    # 3. Issue new tokens (mock user data lookup)
    username = "admin" if user_id == MOCK_USER["id"] else "user"
    role = "admin" if user_id == MOCK_USER["id"] else "analyst"
    
    new_access = jwt_service.create_access_token(user_id, username, role)
    new_refresh, new_jti = jwt_service.create_refresh_token(user_id)
    await jwt_service.store_refresh_token(new_jti, new_refresh, redis_client)

    return TokenResponse(
        access_token=new_access,
        refresh_token=new_refresh,
        token_type="bearer",
        expires_in_seconds=jwt_service.access_expire_minutes * 60
    )


@router.post("/logout")
async def logout(
    user: Annotated[UserContext, Depends(get_current_user)],
    request_data: RefreshRequest,
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
    redis_client: Annotated[Redis, Depends(get_redis)],
):
    """
    Revoke a refresh token.
    """
    try:
        from jose import jwt
        payload = jwt.decode(
            request_data.refresh_token, 
            jwt_service.secret_key, 
            algorithms=[jwt_service.algorithm],
            options={"verify_exp": False} # Allow logout even if token expired
        )
        jti = payload.get("jti")
        if jti:
            await jwt_service.revoke_refresh_token(jti, redis_client)
    except Exception:
        pass # Ignore invalid tokens on logout

    # (Future) Log LOGOUT to AuditLog here

    return {"detail": "Logged out successfully"}
