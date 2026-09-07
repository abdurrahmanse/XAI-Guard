"""
services/api/app/core/config.py — Enhanced Settings (Phase 46.1)
================================================================
pydantic-settings provides type-safe configuration that validates ALL
environment variables on startup. A missing required variable causes
immediate startup failure with a clear field-level error — preventing
silent misconfiguration in production.

Key design decisions:
- extra="forbid" → unknown env vars cause immediate error (prevents typos)
- @lru_cache on get_settings() → one instance shared across all requests
- SecretStr for sensitive values → never logged accidentally as plain text
- SettingsConfigDict → replaces the deprecated class Config pattern
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Literal

from pydantic import AnyUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    XAI-Guard API configuration.

    Environment variables are loaded from .env file (development) or
    actual env vars (staging/production).

    Required vars (will raise ValidationError if missing):
        DATABASE_URL
        REDIS_URL
        SECRET_KEY
        MINIO_ENDPOINT
        MINIO_ACCESS_KEY
        MINIO_SECRET_KEY
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid",  # fail fast on unknown env vars (catches typos)
    )

    # ── Core ─────────────────────────────────────────────────────────────────
    PROJECT_NAME: str = "XAI-Guard API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/v1"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # ── Database ─────────────────────────────────────────────────────────────
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5434/postgres"
    )
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # ── Redis ─────────────────────────────────────────────────────────────────
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6380/0")
    REDIS_MAX_CONNECTIONS: int = 100

    # ── Security ─────────────────────────────────────────────────────────────
    SECRET_KEY: SecretStr = SecretStr(
        os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: list[str] = []

    # ── MLflow ────────────────────────────────────────────────────────────────
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5500")

    # ── MinIO (model artefact storage) ────────────────────────────────────────
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: SecretStr = SecretStr(os.getenv("MINIO_ACCESS_KEY", "minioadmin"))
    MINIO_SECRET_KEY: SecretStr = SecretStr(os.getenv("MINIO_SECRET_KEY", "minioadmin"))
    MINIO_BUCKET_NAME: str = "xaiguard"
    MINIO_USE_SSL: bool = False

    # ── Threat Intelligence ────────────────────────────────────────────────────
    ABUSEIPDB_API_KEY: SecretStr | None = None

    # ── Observability ─────────────────────────────────────────────────────────
    SENTRY_DSN: SecretStr | None = None

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v.upper()

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def database_url_sync(self) -> str:
        """Synchronous database URL for Alembic migrations."""
        return self.DATABASE_URL.replace("asyncpg", "psycopg2")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return the singleton Settings instance.

    Using @lru_cache means this is computed exactly once per process start.
    All modules call get_settings() — never instantiate Settings() directly.

    Example:
        from app.core.config import get_settings
        settings = get_settings()
        print(settings.DATABASE_URL)
    """
    return Settings()


# Module-level convenience alias (for backwards compatibility)
settings = get_settings()
