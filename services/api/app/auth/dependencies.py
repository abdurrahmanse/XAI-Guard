"""
services/api/app/auth/dependencies.py — Auth FastAPI Dependencies (Phase 47.2)
==============================================================================
Provides standard dependencies for protecting routes.

Usage:
    from app.auth.dependencies import get_current_user, require_admin

    @router.get("/me")
    def get_me(user: UserContext = Depends(get_current_user)):
        ...

    @router.post("/promote")
    def promote_model(user: UserContext = Depends(require_admin)):
        ...
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer

from app.core.config import get_settings
from app.core.exceptions import CredentialsException, PermissionDeniedException
from app.auth.jwt_service import JWTService, TokenPayload

logger = logging.getLogger("xaiguard.auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{get_settings().API_V1_STR}/auth/login")


@dataclass
class UserContext:
    """The authenticated user extracted from the JWT."""
    id: str
    username: str
    role: str


def get_jwt_service() -> JWTService:
    settings = get_settings()
    return JWTService(
        secret_key=settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM,
        access_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_expire_days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )


async def get_current_user(
    request: Request,
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
) -> UserContext:
    """
    Decodes the JWT access token and returns the UserContext.
    Raises 401 if the token is invalid or expired.
    """
    payload: TokenPayload = jwt_service.verify_access_token(token)
    
    # Store user context in request state for structured logging/audit
    user_ctx = UserContext(id=payload.sub, username=payload.username, role=payload.role)
    request.state.user = user_ctx
    return user_ctx


async def require_admin(
    user: Annotated[UserContext, Depends(get_current_user)]
) -> UserContext:
    """
    Enforces RBAC: returns the user if admin, otherwise raises 403.
    """
    if user.role != "admin":
        logger.warning(f"Access denied for user {user.username} (role: {user.role})")
        raise PermissionDeniedException(
            detail="This action requires administrator privileges."
        )
    return user
