"""
services/api/app/core/exceptions.py — RFC 7807 Error Handlers (Phase 46.2)
===========================================================================
All API errors return RFC 7807 ProblemDetail JSON responses. Unhandled
exceptions are caught before stack traces can leak to clients. Every
error response includes the request_id for log correlation.

RFC 7807 format:
    {
        "type": "https://xaiguard.local/errors/not-found",
        "title": "Resource Not Found",
        "status": 404,
        "detail": "ModelVersion with id=abc123 was not found.",
        "instance": "/v1/registry/abc123",
        "request_id": "550e8400-e29b-41d4-a716-446655440000"
    }
"""

from __future__ import annotations

import traceback
import uuid
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# ── Domain Exceptions ─────────────────────────────────────────────────────────


class XAIGuardException(Exception):
    """Base exception for all XAI-Guard domain errors."""

    status_code: int = 500
    error_type: str = "https://xaiguard.local/errors/internal"
    title: str = "Internal Server Error"

    def __init__(self, detail: str, instance: str = "/") -> None:
        self.detail = detail
        self.instance = instance
        super().__init__(detail)


class ResourceNotFoundException(XAIGuardException):
    """HTTP 404 — The requested resource does not exist."""

    status_code = 404
    error_type = "https://xaiguard.local/errors/not-found"
    title = "Resource Not Found"


class ValidationException(XAIGuardException):
    """HTTP 422 — Request payload failed domain validation."""

    status_code = 422
    error_type = "https://xaiguard.local/errors/validation"
    title = "Validation Error"


class PermissionDeniedException(XAIGuardException):
    """HTTP 403 — Authenticated user lacks required role."""

    status_code = 403
    error_type = "https://xaiguard.local/errors/forbidden"
    title = "Forbidden"


class RateLimitExceededException(XAIGuardException):
    """HTTP 429 — Too many requests from this client."""

    status_code = 429
    error_type = "https://xaiguard.local/errors/rate-limit"
    title = "Too Many Requests"


class ServiceUnavailableException(XAIGuardException):
    """HTTP 503 — Downstream dependency (DB, Redis, model) unavailable."""

    status_code = 503
    error_type = "https://xaiguard.local/errors/service-unavailable"
    title = "Service Unavailable"


class CredentialsException(XAIGuardException):
    """HTTP 401 — Missing, expired, or invalid authentication credentials."""

    status_code = 401
    error_type = "https://xaiguard.local/errors/unauthorized"
    title = "Unauthorized"


# ── RFC 7807 ProblemDetail schema ─────────────────────────────────────────────


class ProblemDetail(BaseModel):
    """
    RFC 7807 Problem Detail response schema.

    The `request_id` field is added by XAI-Guard — it matches the
    X-Request-ID response header and links this error to all log lines
    for the same request.
    """

    type: str
    title: str
    status: int
    detail: str
    instance: str
    request_id: str


def _get_request_id(request: Request) -> str:
    """Extract request ID from the request state (set by RequestIDMiddleware)."""
    return getattr(request.state, "request_id", str(uuid.uuid4()))


def _make_problem(exc: XAIGuardException, request: Request) -> JSONResponse:
    """Build an RFC 7807 response from a domain exception."""
    problem = ProblemDetail(
        type=exc.error_type,
        title=exc.title,
        status=exc.status_code,
        detail=exc.detail,
        instance=str(request.url.path),
        request_id=_get_request_id(request),
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=problem.model_dump(),
        headers={"Content-Type": "application/problem+json"},
    )


# ── Exception handler registration ───────────────────────────────────────────


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all exception handlers on the FastAPI application.

    Call this in create_application() AFTER creating the app instance.

    Handlers registered:
    1. XAIGuardException → RFC 7807 ProblemDetail with correct status code
    2. RequestValidationError → 422 with per-field error details
    3. Exception → generic 500 (never leaks internals in production)
    """

    @app.exception_handler(XAIGuardException)
    async def xaiguard_exception_handler(
        request: Request, exc: XAIGuardException
    ) -> JSONResponse:
        return _make_problem(exc, request)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        errors = []
        for err in exc.errors():
            errors.append(
                {
                    "field": " → ".join(str(loc) for loc in err["loc"]),
                    "message": err["msg"],
                    "type": err["type"],
                }
            )
        problem = ProblemDetail(
            type="https://xaiguard.local/errors/validation",
            title="Request Validation Error",
            status=422,
            detail=f"{len(errors)} validation error(s)",
            instance=str(request.url.path),
            request_id=_get_request_id(request),
        )
        return JSONResponse(
            status_code=422,
            content={**problem.model_dump(), "errors": errors},
            headers={"Content-Type": "application/problem+json"},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        # Log full traceback internally — never expose to client
        import logging

        logger = logging.getLogger("xaiguard.api")
        logger.error(
            "Unhandled exception",
            extra={
                "request_id": _get_request_id(request),
                "path": str(request.url.path),
                "method": request.method,
                "exc": repr(exc),
                "traceback": traceback.format_exc(),
            },
        )
        from app.core.config import get_settings

        settings = get_settings()
        problem = ProblemDetail(
            type="https://xaiguard.local/errors/internal",
            title="Internal Server Error",
            status=500,
            detail="An unexpected error occurred."
            if settings.is_production
            else repr(exc),
            instance=str(request.url.path),
            request_id=_get_request_id(request),
        )
        return JSONResponse(
            status_code=500,
            content=problem.model_dump(),
            headers={"Content-Type": "application/problem+json"},
        )
