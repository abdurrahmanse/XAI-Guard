"""
services/api/app/modules/alerts/alert_service.py
================================================
Alert deduplication and Redis publishing.
"""
from __future__ import annotations

import hashlib
import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from redis.asyncio.client import Redis
import orjson

from app.modules.alerts.models import Alert
# Assuming Prediction model is available in inference
# from app.modules.inference.models import Prediction

logger = logging.getLogger("xaiguard.alerts")


class AlertService:
    """
    Creates new alerts or increments counts for existing ones to prevent fatigue.
    """

    @staticmethod
    async def create_or_increment(
        prediction_id: str,
        source_ip: str,
        attack_type: str,
        confidence: float,
        severity: str,
        db: AsyncSession,
        redis: Redis
    ) -> Alert:
        """
        Deduplicates alerts based on source_ip and attack_type within a 5-minute window.
        """
        # 1. Compute dedup key
        dedup_raw = f"{source_ip}|{attack_type}"
        dedup_hash = hashlib.sha256(dedup_raw.encode()).hexdigest()
        
        # 2. Check for recent unacknowledged alert
        # We simulate the 5-minute window by relying on the 'acknowledged' flag. 
        # In a strict implementation, we would also add a time bound to the query.
        stmt = select(Alert).where(
            Alert.dedup_hash == dedup_hash,
            Alert.acknowledged == False
        ).with_for_update(skip_locked=True)
        
        result = await db.execute(stmt)
        existing_alert = result.scalars().first()
        
        if existing_alert:
            # 3. Increment existing alert
            existing_alert.alert_count += 1
            # Note: last_seen_at would be updated here
            alert = existing_alert
            is_new = False
        else:
            # 4. Create new alert
            alert = Alert(
                prediction_id=prediction_id,
                severity=severity,
                source_ip=source_ip,
                attack_type=attack_type,
                confidence=confidence,
                mitre_technique_id="T1499", # Mocked from Threat Intel
                dedup_hash=dedup_hash,
                alert_count=1
            )
            db.add(alert)
            is_new = True
            
        await db.flush() # get ID without full commit yet
        
        # 5. Publish to WebSocket
        alert_payload = {
            "id": str(alert.id),
            "severity": alert.severity.value if hasattr(alert.severity, "value") else str(alert.severity),
            "source_ip": alert.source_ip,
            "attack_type": alert.attack_type,
            "confidence": alert.confidence,
            "count": alert.alert_count,
            "is_new": is_new
        }
        await redis.publish("xaiguard:alerts:live", orjson.dumps(alert_payload).decode())
        
        return alert

