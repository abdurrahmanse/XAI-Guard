from __future__ import annotations

"""
services/api/app/modules/events/deduplication.py
================================================
Event deduplication using Redis.
Prevents the same network flow from generating multiple alerts.
"""

import hashlib
from typing import Any

from redis.asyncio.client import Redis


class EventDeduplicator:
    """
    Computes deterministic hashes for events and checks Redis for duplicates.
    Uses pipelining for O(1) network round-trips regardless of batch size.
    """

    @staticmethod
    def compute_hash(event_dict: dict[str, Any]) -> str:
        """
        Compute SHA-256 deduplication hash from core event identifiers.
        
        Fields used: source_ip | destination_ip | timestamp | protocol
        """
        # Convert timestamp to int for deterministic hashing
        ts = int(event_dict.get("timestamp", 0))
        src = event_dict.get("source_ip", "")
        dst = event_dict.get("destination_ip", "")
        proto = event_dict.get("protocol", "")
        
        raw = f"{src}|{dst}|{ts}|{proto}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @staticmethod
    async def check_and_mark_duplicates(
        hashes: list[str],
        redis: Redis,
        ttl_seconds: int = 300
    ) -> list[bool]:
        """
        Check which hashes already exist, and mark the new ones.
        
        Executes in exactly 2 Redis round-trips using pipelines:
        1. MGET to check all hashes simultaneously.
        2. SET NX PX on the non-duplicate hashes.
        
        Returns:
            list[bool]: True if the hash was a duplicate, False if it was new.
        """
        if not hashes:
            return []

        # Ensure unique keys for Redis
        redis_keys = [f"dedup:event:{h}" for h in hashes]
        
        # Round-trip 1: MGET to check existence
        exists_results = await redis.mget(redis_keys)
        
        is_duplicate = [val is not None for val in exists_results]
        
        # Identify new keys that need to be set
        new_keys = [
            key for idx, key in enumerate(redis_keys) 
            if not is_duplicate[idx]
        ]
        
        # Round-trip 2: Pipeline SET NX PX for new keys
        if new_keys:
            pipe = redis.pipeline()
            for key in new_keys:
                pipe.set(key, "1", nx=True, ex=ttl_seconds)
            await pipe.execute()
            
        return is_duplicate

