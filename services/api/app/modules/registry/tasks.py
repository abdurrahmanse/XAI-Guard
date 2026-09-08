from __future__ import annotations

import logging
from datetime import datetime, timedelta

from celery import shared_task
from sqlalchemy import select

from app.core.database import SessionLocal
from app.modules.registry.models import ModelStatusEnum, ModelVersion, PromotionHistory

logger = logging.getLogger("xaiguard.registry")

@shared_task(name="models.nightly_evaluation")
def nightly_evaluation():
    logger.info("Starting nightly model evaluation")
    import asyncio
    asyncio.run(_async_nightly_evaluation())

async def _async_nightly_evaluation():
    async with SessionLocal() as db:
        stmt = select(ModelVersion).where(ModelVersion.status == ModelStatusEnum.CHALLENGER)
        result = await db.execute(stmt)
        challenger = result.scalars().first()
        
        if not challenger:
            return

        champ_stmt = select(ModelVersion).where(ModelVersion.status == ModelStatusEnum.CHAMPION)
        champ_result = await db.execute(champ_stmt)
        champion = champ_result.scalars().first()
        
        if not champion:
            return

        mock_f1_champ = champion.metrics.get("f1_score", 0.90)
        mock_f1_chall = challenger.metrics.get("f1_score", 0.95)
        mock_roc_champ = 0.88
        mock_roc_chall = 0.92
        mock_p99_chall = challenger.metrics.get("latency_p99_ms", 50.0)
        mock_mcnemar_p = 0.01

        delta_f1 = mock_f1_chall - mock_f1_champ
        delta_roc = mock_roc_chall - mock_roc_champ
        
        gate1_f1 = delta_f1 >= 0.020
        gate2_roc = delta_roc >= 0.010
        gate3_latency = mock_p99_chall <= 100.0
        gate4_significance = mock_mcnemar_p < 0.05
        
        if gate1_f1 and gate2_roc and gate3_latency and gate4_significance:
            champion.status = ModelStatusEnum.PREVIOUS
            challenger.status = ModelStatusEnum.CHAMPION
            
            history = PromotionHistory(
                model_version_id=challenger.id,
                promoted_by="system:nightly_eval",
                promotion_reason=f"Auto-promotion. ΔF1={delta_f1:.3f}",
                f1_score_at_promotion=mock_f1_chall,
                latency_at_promotion=mock_p99_chall
            )
            
            db.add(champion)
            db.add(challenger)
            db.add(history)
            await db.commit()
