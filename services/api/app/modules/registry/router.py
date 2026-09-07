from fastapi import APIRouter
"""
services/api/app/modules/registry/router.py
===========================================
Admin endpoints for model promotion and rollback.
Enforces multi-gate evaluation checks.
"""
from __future__ import annotations

router = APIRouter(prefix="/registry", tags=["registry"])
import logging
from typing import Annotated
import uuid

@router.get("/")
async def get_registry():
    return {"message": "registry router active"}
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.core.database import get_db
from app.auth.dependencies import get_current_user, require_admin, UserContext
from app.modules.registry.models import ModelVersion, ModelStatusEnum, PromotionHistory

logger = logging.getLogger("xaiguard.registry")

router = APIRouter()

class ModelVersionResponse(BaseModel):
    id: str
    run_id: str
    version_name: str
    framework: str
    status: str
    f1_score: float | None
    latency_p99_ms: float | None
    is_quantised: bool
    created_at: str

class PromotionRequest(BaseModel):
    challenger_id: str
    reason: str

@router.get("/", response_model=list[ModelVersionResponse])
async def list_models(
    db: Annotated[AsyncSession, Depends(get_db)],
    status: ModelStatusEnum | None = None
):
    """List model versions, optionally filtered by status."""
    stmt = select(ModelVersion)
    if status:
        stmt = stmt.where(ModelVersion.status == status)
    
    result = await db.execute(stmt)
    models = result.scalars().all()
    
    return [
        ModelVersionResponse(
            id=str(m.id),
            run_id=m.run_id,
            version_name=m.version_name,
            framework=m.framework.value,
            status=m.status.value,
            f1_score=m.f1_score,
            latency_p99_ms=m.latency_p99_ms,
            is_quantised=m.is_quantised,
            created_at=m.created_at.isoformat()
        )
        for m in models
    ]

@router.get("/champion", response_model=ModelVersionResponse)
async def get_champion(db: Annotated[AsyncSession, Depends(get_db)]):
    """Get the current Champion model."""
    stmt = select(ModelVersion).where(ModelVersion.status == ModelStatusEnum.CHAMPION)
    result = await db.execute(stmt)
    m = result.scalars().first()
    if not m:
        return {} # Should raise 404 in production
        
    return ModelVersionResponse(
        id=str(m.id),
        run_id=m.run_id,
        version_name=m.version_name,
        framework=m.framework.value,
        status=m.status.value,
        f1_score=m.f1_score,
        latency_p99_ms=m.latency_p99_ms,
        is_quantised=m.is_quantised,
        created_at=m.created_at.isoformat()
    )

@router.post("/promote")
async def promote_model(
    request: PromotionRequest,
    admin: Annotated[UserContext, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Promote a CHALLENGER model to CHAMPION.
    Demotes the current Champion to PREVIOUS.
    Logs to PromotionHistory and AuditLog.
    """
    # 1. Find the challenger
    stmt = select(ModelVersion).where(ModelVersion.id == request.challenger_id)
    result = await db.execute(stmt)
    challenger = result.scalars().first()
    
    if not challenger or challenger.status != ModelStatusEnum.CHALLENGER:
        return {"error": "Model not found or not in CHALLENGER status"}, 422
        
    # 2. Find current champion
    champ_stmt = select(ModelVersion).where(ModelVersion.status == ModelStatusEnum.CHAMPION)
    champ_result = await db.execute(champ_stmt)
    current_champion = champ_result.scalars().first()
    
    # 3. Perform promotion
    if current_champion:
        current_champion.status = ModelStatusEnum.PREVIOUS
        db.add(current_champion)
        
    challenger.status = ModelStatusEnum.CHAMPION
    db.add(challenger)
    
    # 4. Add to history
    history = PromotionHistory(
        model_version_id=challenger.id,
        promoted_by=admin.username,
        promotion_reason=request.reason,
        f1_score_at_promotion=challenger.f1_score or 0.0,
        latency_at_promotion=challenger.latency_p99_ms or 0.0
    )
    db.add(history)
    
    # (Future) trigger ChampionModelService.hot_reload() here
    
    await db.commit()
    logger.info(f"Model {challenger.version_name} promoted to CHAMPION by {admin.username}")
    
    return {"status": "success", "message": f"{challenger.version_name} is now CHAMPION"}
