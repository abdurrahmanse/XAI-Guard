from __future__ import annotations

"""
services/api/app/modules/events/storage.py
==========================================
Bulk PostgreSQL insertion for security events.
"""

import logging
import time
import uuid
from typing import Any

import asyncpg
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ServiceUnavailableException
from app.modules.events.models import SecurityEvent

logger = logging.getLogger("xaiguard.events")


class EventStorageService:
    """
    Handles bulk insertion of security events to PostgreSQL.
    """

    @staticmethod
    async def bulk_insert(
        events_data: list[dict[str, Any]], 
        db: AsyncSession
    ) -> list[uuid.UUID]:
        """
        Bulk insert events using PostgreSQL ON CONFLICT DO NOTHING.
        Returns the list of UUIDs that were successfully inserted.
        """
        if not events_data:
            return []

        t0 = time.perf_counter()
        
        try:
            stmt = insert(SecurityEvent).values(events_data)
            # Conflict resolution: if the dedup_hash already exists in the DB
            # (e.g. from an older batch that survived Redis TTL), ignore it.
            stmt = stmt.on_conflict_do_nothing(index_elements=["dedup_hash"])
            # Return the inserted IDs
            stmt = stmt.returning(SecurityEvent.id)
            
            result = await db.execute(stmt)
            inserted_ids = [row[0] for row in result.fetchall()]
            
            await db.commit()
            
            elapsed_ms = (time.perf_counter() - t0) * 1000
            conflict_count = len(events_data) - len(inserted_ids)
            
            logger.info(
                "Bulk insert completed",
                extra={
                    "inserted_count": len(inserted_ids),
                    "conflict_count": conflict_count,
                    "elapsed_ms": round(elapsed_ms, 2)
                }
            )
            return inserted_ids
            
        except asyncpg.exceptions.PostgresError as exc:
            await db.rollback()
            logger.error(f"Database error during bulk insert: {exc}")
            raise ServiceUnavailableException(
                detail="Database unavailable for bulk insertion",
                instance="/v1/events/ingest"
            ) from exc
        except Exception as exc:
            await db.rollback()
            logger.error(f"Unexpected error during bulk insert: {exc}")
            raise ServiceUnavailableException(
                detail="Unexpected error during bulk insertion",
                instance="/v1/events/ingest"
            ) from exc

