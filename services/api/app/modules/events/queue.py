from __future__ import annotations
"""
services/api/app/modules/events/queue.py
========================================
Redis Streams integration for durable event queuing.
"""

import logging
import uuid
from datetime import datetime, timezone

from redis.asyncio.client import Redis
from redis.exceptions import ResponseError

logger = logging.getLogger("xaiguard.events")


class EventQueuePublisher:
    """
    Publishes ingested events to a Redis Stream for asynchronous processing.
    """
    STREAM_NAME = "events:pending"
    CONSUMER_GROUP = "predictions_worker"

    @classmethod
    async def ensure_group(cls, redis: Redis) -> None:
        """
        Create the consumer group and stream if they do not exist.
        """
        try:
            # MKSTREAM creates the stream if it doesn't exist
            await redis.xgroup_create(
                name=cls.STREAM_NAME, 
                groupname=cls.CONSUMER_GROUP, 
                id="0", 
                mkstream=True
            )
        except ResponseError as e:
            # BUSYGROUP means the consumer group already exists. Safe to ignore.
            if "BUSYGROUP" not in str(e):
                raise

    @classmethod
    async def publish_batch(cls, event_ids: list[uuid.UUID], redis: Redis) -> None:
        """
        Publish a batch of event IDs to the Redis stream using a pipeline.
        """
        if not event_ids:
            return
            
        await cls.ensure_group(redis)
        
        now_iso = datetime.now(timezone.utc).isoformat()
        
        pipe = redis.pipeline()
        for event_id in event_ids:
            pipe.xadd(
                cls.STREAM_NAME,
                {"event_id": str(event_id), "timestamp": now_iso}
            )
            
        await pipe.execute()
        logger.debug(f"Published {len(event_ids)} events to {cls.STREAM_NAME}")

    @classmethod
    async def acknowledge(cls, stream_id: str, redis: Redis) -> None:
        """
        Acknowledge a processed message so it's removed from pending entries.
        """
        await redis.xack(cls.STREAM_NAME, cls.CONSUMER_GROUP, stream_id)

