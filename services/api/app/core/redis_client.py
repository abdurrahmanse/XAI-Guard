"""
services/api/app/core/redis_client.py — Redis async pool & caching (Phase 46.3)
================================================================================
Multiple domain modules use Redis: deduplication hashes, feature caching,
pub/sub (drift retraining triggers), and rate limiting (slowapi).

A shared connection pool prevents fragmentation.

Usage:
    from app.core.redis_client import get_redis, cache_set, cache_get

    @router.get("/")
    async def endpoint(redis: AsyncRedis = Depends(get_redis)):
        await cache_set("key", my_pydantic_model, ttl=3600, client=redis)
"""
from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from typing import Type, TypeVar

try:
    import orjson
except ImportError:
    import json as orjson

import redis.asyncio as redis
from pydantic import BaseModel
from redis.asyncio.client import Redis

from app.core.config import get_settings

logger = logging.getLogger("xaiguard.redis")

T = TypeVar("T", bound=BaseModel)

# Global connection pool instance
_redis_pool: redis.ConnectionPool | None = None


def init_redis_pool() -> None:
    """Initialize the global Redis connection pool. Call on app startup."""
    global _redis_pool
    settings = get_settings()
    _redis_pool = redis.ConnectionPool.from_url(
        settings.REDIS_URL,
        max_connections=settings.REDIS_MAX_CONNECTIONS,
        decode_responses=True,
    )
    logger.info("Redis connection pool initialized")


async def close_redis_pool() -> None:
    """Close the Redis pool. Call on app shutdown."""
    global _redis_pool
    if _redis_pool:
        await _redis_pool.disconnect()
        logger.info("Redis connection pool closed")


async def get_redis() -> AsyncGenerator[Redis, None]:
    """FastAPI dependency to get a Redis client from the pool."""
    if not _redis_pool:
        init_redis_pool()
    client = redis.Redis(connection_pool=_redis_pool)
    try:
        yield client
    finally:
        await client.close()


async def cache_set(key: str, value: BaseModel, ttl: int, client: Redis) -> None:
    """
    Serialize a Pydantic model and store in Redis.
    Uses orjson for high performance.
    """
    try:
        # Pydantic v2 model_dump returns a dict, orjson.dumps is fast
        json_bytes = orjson.dumps(value.model_dump(mode="json"))
        await client.setex(key, ttl, json_bytes.decode("utf-8"))
    except Exception as exc:
        logger.warning("Failed to cache set key=%s: %s", key, exc)


async def cache_get(key: str, model_class: type[T], client: Redis) -> T | None:
    """
    Retrieve and deserialize a Pydantic model from Redis.
    """
    try:
        data = await client.get(key)
        if not data:
            return None
        return model_class.model_validate_json(data)
    except Exception as exc:
        logger.warning("Failed to cache get key=%s: %s", key, exc)
        return None


async def publish(channel: str, message: dict, client: Redis) -> None:
    """Publish a JSON message to a Redis pub/sub channel."""
    try:
        payload = orjson.dumps(message).decode("utf-8")
        await client.publish(channel, payload)
    except Exception as exc:
        logger.warning("Failed to publish to channel=%s: %s", channel, exc)
