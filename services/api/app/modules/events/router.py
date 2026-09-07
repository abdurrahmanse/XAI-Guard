from __future__ import annotations
from fastapi import APIRouter
"""
services/api/app/modules/events/router.py
=========================================
Event ingestion endpoints.
"""

router = APIRouter(prefix="/events", tags=["events"])
import logging
from typing import Annotated

@router.get("/")
async def get_events():
    return {"message": "events router active"}
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio.client import Redis

from app.core.database import get_db
from app.core.redis_client import get_redis
from app.modules.events.deduplication import EventDeduplicator
from app.modules.events.storage import EventStorageService
from app.modules.events.queue import EventQueuePublisher
from app.modules.events.models import ProtocolEnum

logger = logging.getLogger("xaiguard.events")

router = APIRouter(prefix="/events", tags=["Events"])


class SecurityEventInput(BaseModel):
    """Input payload for a single security event."""
    model_config = {"extra": "forbid"}

    timestamp: float
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: ProtocolEnum
    bytes_in: int
    bytes_out: int
    duration_ms: int
    features: dict[str, float] = Field(default_factory=dict)


class BatchEventRequest(BaseModel):
    """Batch ingestion request containing up to 1000 events."""
    model_config = {"extra": "forbid"}

    events: list[SecurityEventInput] = Field(..., max_length=1000, min_length=1)


class BatchIngestionResponse(BaseModel):
    """Response detailing the result of a batch ingestion."""
    accepted_count: int
    duplicate_count: int
    error_count: int
    accepted_event_ids: list[str]


@router.post("/ingest", response_model=BatchIngestionResponse)
async def ingest_events(
    request: BatchEventRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    redis: Annotated[Redis, Depends(get_redis)]
):
    """
    Ingest a batch of security events.
    Validates, deduplicates via Redis, bulk inserts to PostgreSQL,
    and publishes accepted events to a Redis Stream for prediction queuing.
    """
    # 1. Validation is already handled by Pydantic Model (BatchEventRequest)
    
    # 2. Compute deduplication hashes
    event_dicts = [e.model_dump() for e in request.events]
    hashes = [EventDeduplicator.compute_hash(e) for e in event_dicts]
    
    for i, e_dict in enumerate(event_dicts):
        e_dict["dedup_hash"] = hashes[i]
        
    # 3. Deduplicate via Redis
    is_duplicate = await EventDeduplicator.check_and_mark_duplicates(hashes, redis)
    
    unique_events = [
        event_dicts[i] for i in range(len(event_dicts)) 
        if not is_duplicate[i]
    ]
    duplicate_count = sum(is_duplicate)
    
    accepted_ids = []
    
    if unique_events:
        # 4. Bulk insert unique events to DB
        inserted_uuids = await EventStorageService.bulk_insert(unique_events, db)
        accepted_ids = [str(uid) for uid in inserted_uuids]
        
        # 5. Publish to Redis Stream for inference
        await EventQueuePublisher.publish_batch(inserted_uuids, redis)

    return BatchIngestionResponse(
        accepted_count=len(accepted_ids),
        duplicate_count=duplicate_count,
        error_count=0, # Errors are handled by exceptions or validation failures
        accepted_event_ids=accepted_ids
    )
