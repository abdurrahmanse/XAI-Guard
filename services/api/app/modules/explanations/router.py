"""
services/api/app/modules/explanations/router.py
===============================================
Endpoints for requesting and polling async explanations.
"""
from __future__ import annotations

import logging
import uuid

from fastapi import APIRouter
from pydantic import BaseModel

# In a real setup, we would import the Celery task and `AsyncResult`
# from app.modules.explanations.tasks import compute_shap_explanation

logger = logging.getLogger("xaiguard.explanations")

router = APIRouter(prefix="/explanations", tags=["Explanations"])

class ExplanationRequest(BaseModel):
    prediction_id: str
    method: str = "SHAP"

class ExplanationRequestResponse(BaseModel):
    task_id: str
    status: str
    estimated_seconds: int

@router.post("/request", response_model=ExplanationRequestResponse)
async def request_explanation(req: ExplanationRequest):
    """
    Dispatch async XAI task.
    Returns immediately with a task_id to poll.
    """
    task_id = str(uuid.uuid4())
    
    # Check DB if COMPLETE first to return cache hit.
    # Otherwise:
    # compute_shap_explanation.apply_async(args=[req.prediction_id], task_id=task_id)
    
    logger.info(f"Dispatched {req.method} explanation task {task_id} for prediction {req.prediction_id}")
    
    return ExplanationRequestResponse(
        task_id=task_id,
        status="PENDING",
        estimated_seconds=5 if req.method == "SHAP" else 2
    )

@router.get("/{task_id}")
async def poll_explanation(task_id: str):
    """
    Polls the status of an explanation task.
    """
    # result = AsyncResult(task_id)
    # if result.state == "PENDING" ...
    
    # Mocking response
    return {
        "task_id": task_id,
        "status": "processing"
    }
