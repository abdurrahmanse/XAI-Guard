"""
services/api/app/core/middleware.py — Observability & Security (Phase 46.4)
===========================================================================
Three middleware layers that every request passes through:

1. RequestIDMiddleware   — injects UUID4 X-Request-ID header
2. RequestTimingMiddleware — adds X-Process-Time-Ms header
3. SecurityHeadersMiddleware — OWASP security headers

Middleware execution order (LIFO — last registered = first executed):
    register: Security → Timing → RequestID
    execution: RequestID → Timing → Security → route handler

The request_id is stored in a ContextVar so it's accessible from any
async function in the call stack without passing it explicitly.
"""

from __future__ import annotations

import contextvars
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# ── ContextVar — holds the current request ID for the lifetime of one request ─
request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default=""
)


def get_request_id() -> str:
    """Get the current request ID from context. Returns empty string if not set."""
    return request_id_var.get("")


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Generates a UUID4 request ID for every incoming request.

    - Stores in request.state.request_id
    - Stores in ContextVar (accessible from Celery tasks, log formatters)
    - Adds X-Request-ID response header for client correlation

    If the client sends an X-Request-ID header, we use that value instead
    of generating one — this supports end-to-end request tracing.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # Honour client-provided request IDs (for distributed tracing)
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        # Store in request state and ContextVar
        request.state.request_id = request_id
        token = request_id_var.set(request_id)

        try:
            response = await call_next(request)
        finally:
            request_id_var.reset(token)

        response.headers["X-Request-ID"] = request_id
        return response


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """
    Measures wall-clock processing time per request.

    Adds X-Process-Time-Ms header in milliseconds (float, 2 decimal places).
    This header is consumed by the Prometheus scrape and by the admin dashboard.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        t0 = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)
        response.headers["X-Process-Time-Ms"] = str(elapsed_ms)
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds OWASP-recommended security headers to every response.

    Headers added:
    - X-Content-Type-Options: nosniff
        Prevents MIME-type sniffing attacks.
    - X-Frame-Options: DENY
        Prevents clickjacking by disallowing iframe embedding.
    - Strict-Transport-Security (HSTS): max-age=31536000; includeSubDomains
        Forces HTTPS for 1 year. Only added in non-development environments.
    - X-XSS-Protection: 0
        Disables the broken browser XSS filter — modern CSP is better.
    - Referrer-Policy: strict-origin-when-cross-origin
        Leaks minimal referrer info for cross-origin requests.
    - Permissions-Policy
        Restricts access to browser APIs (camera, mic, geolocation).
    """

    def __init__(self, app, environment: str = "development") -> None:
        super().__init__(app)
        self.environment = environment

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "0"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=()"
        )

        # HSTS only in non-development (HTTP in dev, HTTPS in production)
        if self.environment != "development":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        return response


def register_middleware(app, settings) -> None:
    """
    Register all middleware on the FastAPI app in the correct order.

    Order matters — Starlette middleware is executed LIFO (last added = first run).
    We add Security last so it runs first (outermost layer).
    We add RequestID first so it runs last (innermost, after auth and routing).

    Final execution order (outer → inner):
        SecurityHeaders → Timing → RequestID → route handler
    """
    # Added first → runs last (innermost)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(RequestTimingMiddleware)
    # Added last → runs first (outermost)
    app.add_middleware(SecurityHeadersMiddleware, environment=settings.ENVIRONMENT)
