"""
services/api/app/auth/audit.py — Audit Log (Phase 47.4)
=======================================================
Every security-sensitive action is recorded in the audit log.

The audit log is:
- Append-only (no UPDATE, no DELETE)
- Timestamped in UTC
- IP-aware (handles X-Forwarded-For for reverse proxies)
- JSONB details field for arbitrary event context

Actions tracked:
    LOGIN            — successful user login
    LOGOUT           — user logout (token revoked)
    PROMOTE_MODEL    — Champion model changed
    ROLLBACK_MODEL   — Previous champion restored
    ACKNOWLEDGE_ALERT — SOC analyst acknowledged an alert

Usage:
    await AuditLogger.log_action(
        db=db,
        user_id=current_user.id,
        action=AuditAction.LOGIN,
        resource_type="user",
        resource_id=str(current_user.id),
        request=request,
        details={"ip": client_ip}
    )
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.orm import Mapped, mapped_column


class AuditAction(str, enum.Enum):
    """All auditable actions in the system."""

    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    PROMOTE_MODEL = "PROMOTE_MODEL"
    ROLLBACK_MODEL = "ROLLBACK_MODEL"
    ACKNOWLEDGE_ALERT = "ACKNOWLEDGE_ALERT"
    TOKEN_REFRESH = "TOKEN_REFRESH"
    FAILED_LOGIN = "FAILED_LOGIN"


class AuditLog(Base, PrimaryKeyMixin, TimestampMixin):
    """
    Append-only audit log record.

    Never UPDATE or DELETE rows in this table.
    Add new rows only via AuditLogger.log_action().
    """

    __tablename__ = "audit_logs"

    user_id: Mapped[str] = mapped_column(String(36), index=True)
    username: Mapped[str] = mapped_column(String(255))
    action: Mapped[AuditAction] = mapped_column(SQLEnum(AuditAction), index=True)
    resource_type: Mapped[str] = mapped_column(String(64))
    resource_id: Mapped[str] = mapped_column(String(255))
    client_ip: Mapped[str] = mapped_column(String(45))  # IPv6 max length
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class AuditLogger:
    """
    Async audit logger — writes AuditLog records to PostgreSQL.

    All methods are class methods (no instance state needed).
    Inject via FastAPI dependency or call directly in route handlers.
    """

    @classmethod
    async def log_action(
        cls,
        db,  # AsyncSession
        user_id: str,
        username: str,
        action: AuditAction,
        resource_type: str,
        resource_id: str,
        request,  # FastAPI Request
        details: dict[str, Any] | None = None,
    ) -> AuditLog:
        """
        Create and persist an AuditLog record.

        IP extraction priority:
        1. X-Forwarded-For header (first IP, for reverse proxy setups)
        2. X-Real-IP header (nginx single-proxy setups)
        3. request.client.host (direct connection fallback)
        """
        client_ip = cls._extract_client_ip(request)
        user_agent = request.headers.get("User-Agent")

        log_entry = AuditLog(
            user_id=str(user_id),
            username=username,
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id),
            client_ip=client_ip,
            user_agent=user_agent[:500] if user_agent else None,
            details=details,
        )
        db.add(log_entry)
        await db.flush()  # get the ID without committing yet
        return log_entry

    @staticmethod
    def _extract_client_ip(request) -> str:
        """
        Extract the real client IP from the request.

        Handles:
        - X-Forwarded-For: client, proxy1, proxy2 → returns 'client'
        - X-Real-IP: single IP from nginx
        - request.client.host: direct TCP connection
        """
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take the first IP in the chain (the actual client)
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()

        if request.client:
            return request.client.host

        return "unknown"
