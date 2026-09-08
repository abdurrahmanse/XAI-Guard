from __future__ import annotations

"""
services/api/app/modules/inference/feature_cache.py
===================================================
Redis-based feature caching for O(1) latency on identical packets/flows.
"""


import hashlib
import logging
from typing import Any

import orjson
from redis.asyncio.client import Redis

logger = logging.getLogger("xaiguard.inference")


class FeatureCache:
    """
    Caches processed feature vectors to bypass re-computation for identical network flows.
    """

    @staticmethod
    async def get_or_compute(
        event_dict: dict[str, Any],
        redis: Redis,
        compute_fn: Any,  # Callable that takes event and returns feature array
    ) -> tuple[list[float], bool]:
        """
        Check cache. If miss, compute and store.
        Returns: (features, is_cache_hit)
        """
        # Serialize event identically to get deterministic hash
        # Remove timestamp and unique IDs to cache strictly on flow characteristics
        cacheable_event = {
            k: v
            for k, v in event_dict.items()
            if k not in ["timestamp", "id", "features"]
        }

        event_json = orjson.dumps(cacheable_event, option=orjson.OPT_SORT_KEYS)
        cache_key = f"features:{hashlib.sha256(event_json).hexdigest()}"

        try:
            cached_data = await redis.get(cache_key)
            if cached_data:
                # Cache HIT
                features = orjson.loads(cached_data)
                return features, True
        except Exception as e:
            logger.warning(f"Redis cache get failed: {e}")

        # Cache MISS -> Compute
        features = compute_fn(event_dict)

        try:
            # Store with 60-second TTL
            await redis.setex(cache_key, 60, orjson.dumps(features))
        except Exception as e:
            logger.warning(f"Redis cache set failed: {e}")

        return features, False
