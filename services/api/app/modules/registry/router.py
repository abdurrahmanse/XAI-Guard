from __future__ import annotations

import logging
from typing import Annotated
import uuid

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
    mlflow_run_id: str
    mlflow_model_name: str
    framework: str
    status: str
    metrics: dict
    created_at: str

class PromotionRequest(BaseModel):
    challenger_id: str
    reason: str

@router.get("/", response_model=list[ModelVersionResponse])
async def list_models(
    db: Annotated[AsyncSession, Depends(get_db)],
    status: ModelStatusEnum | None = None
):
    stmt = select(ModelVersion)
    if status:
        stmt = stmt.where(ModelVersion.status == status)
    
    result = await db.execute(stmt)
    models = result.scalars().all()
    
    return [
        ModelVersionResponse(
            id=str(m.id),
            mlflow_run_id=m.mlflow_run_id,
            mlflow_model_name=m.mlflow_model_name,
            framework=m.framework.value,
            status=m.status.value,
            metrics=m.metrics,
            created_at=m.created_at.isoformat()
        )
        for m in models
    ]

@router.get("/champion", response_model=ModelVersionResponse)
async def get_champion(db: Annotated[AsyncSession, Depends(get_db)]):
    stmt = select(ModelVersion).where(ModelVersion.status == ModelStatusEnum.CHAMPION)
    result = await db.execute(stmt)
    m = result.scalars().first()
    if not m:
        return {} # Mock missing
        
    return ModelVersionResponse(
        id=str(m.id),
        mlflow_run_id=m.mlflow_run_id,
        mlflow_model_name=m.mlflow_model_name,
        framework=m.framework.value,
        status=m.status.value,
        metrics=m.metrics,
        created_at=m.created_at.isoformat()
    )

@router.post("/promote")
async def promote_model(
    request: PromotionRequest,
    admin: Annotated[UserContext, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    stmt = select(ModelVersion).where(ModelVersion.id == request.challenger_id)
    result = await db.execute(stmt)
    challenger = result.scalars().first()
    
    if not challenger or challenger.status != ModelStatusEnum.CHALLENGER:
        return {"error": "Model not found or not in CHALLENGER status"}, 422
        
    champ_stmt = select(ModelVersion).where(ModelVersion.status == ModelStatusEnum.CHAMPION)
    champ_result = await db.execute(champ_stmt)
    current_champion = champ_result.scalars().first()
    
    if current_champion:
        current_champion.status = ModelStatusEnum.PREVIOUS
        db.add(current_champion)
        
    challenger.status = ModelStatusEnum.CHAMPION
    db.add(challenger)
    
    history = PromotionHistory(
        model_version_id=challenger.id,
        promoted_by=admin.username,
        promotion_reason=request.reason,
        f1_score_at_promotion=challenger.metrics.get("f1_score", 0.0),
        latency_at_promotion=challenger.metrics.get("latency_p99_ms", 0.0)
    )
    db.add(history)
    
    await db.commit()
    return {"status": "success", "message": f"{challenger.mlflow_model_name} is now CHAMPION"}
