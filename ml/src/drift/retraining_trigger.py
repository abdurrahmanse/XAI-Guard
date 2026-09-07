"""
ml/src/drift/retraining_trigger.py — Retraining Trigger (Phase 45.3)
====================================================================
When CRITICAL drift is detected, the ML layer must trigger the API layer
to dispatch a Celery retraining task. This decouples the detector from
the orchestration engine using Redis pub/sub.

Key design decisions:
- Cooldown logic: 6-hour TTL prevents flooding the system with retraining
  requests if traffic stays drifted while the new model trains.
"""
from __future__ import annotations

import logging
from redis.asyncio.client import Redis

logger = logging.getLogger("xaiguard.drift")


class DriftRetrigger:
    """
    Publishes retraining requests to Redis pub/sub.
    Includes a 6-hour cooldown to prevent retraining storms.
    """
    CHANNEL = "xaiguard:retraining"
    COOLDOWN_SECONDS = 6 * 3600  # 6 hours

    def __init__(self, redis_client: Redis) -> None:
        self.redis = redis_client

    async def trigger(self, model_family: str, mmd_score: float) -> bool:
        """
        Trigger retraining if cooldown allows.
        
        Returns True if triggered, False if skipped due to cooldown.
        """
        cooldown_key = f"drift:cooldown:{model_family}"
        
        # Check if already in cooldown
        is_cooling = await self.redis.exists(cooldown_key)
        if is_cooling:
            logger.warning(
                f"Skipping retraining for {model_family} (MMD={mmd_score:.4f}): "
                "Retraining triggered within last 6 hours."
            )
            return False

        # Publish the event
        payload = f"drift:critical:{model_family}:{mmd_score:.4f}"
        await self.redis.publish(self.CHANNEL, payload)
        
        # Set cooldown lock
        await self.redis.setex(cooldown_key, self.COOLDOWN_SECONDS, "locked")
        
        logger.info(f"Retraining triggered for {model_family} (MMD={mmd_score:.4f}). Cooldown activated.")
        return True

