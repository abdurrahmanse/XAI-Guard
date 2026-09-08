from __future__ import annotations

import logging
import uuid
import time
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger("xaiguard.explanations")

router = APIRouter(prefix="/explanations", tags=["Explanations"])

class ExplanationRequest(BaseModel):
    prediction_id: str
    method: Literal["SHAP", "LIME", "ATTENTION", "NLG"] = "SHAP"

class ExplanationRequestResponse(BaseModel):
    task_id: str
    status: str
    estimated_seconds: int
    method: str

@router.post("/request", response_model=ExplanationRequestResponse)
async def request_explanation(req: ExplanationRequest):
    """
    Dispatch async XAI task (SHAP, LIME, Transformer Attention, or NLG).
    Returns immediately with a task_id to poll.
    """
    task_id = str(uuid.uuid4())

    # Mock dispatching Celery tasks for different XAI methods
    logger.info(
        f"Dispatched {req.method} explanation task {task_id} for prediction {req.prediction_id}"
    )

    estimated = {
        "SHAP": 5,
        "LIME": 3,
        "ATTENTION": 2,
        "NLG": 1
    }

    return ExplanationRequestResponse(
        task_id=task_id,
        status="PENDING",
        estimated_seconds=estimated.get(req.method, 5),
        method=req.method
    )

@router.get("/{task_id}")
async def poll_explanation(task_id: str):
    """
    Polls the status of an explanation task.
    """
    # Mocking response
    return {
        "task_id": task_id, 
        "status": "COMPLETE", 
        "result": {
            "features": [{"name": "tcp.flags.syn", "shap": 2.45}],
            "nlg_text": "The model flagged this as DDoS due to high tcp.flags.syn."
        }
    }
