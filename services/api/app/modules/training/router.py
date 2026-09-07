from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.modules.training.tasks import run_training_pipeline

router = APIRouter()

class TriggerResponse(BaseModel):
    message: str
    task_id: str

class TriggerRequest(BaseModel):
    force_repro: bool = False

@router.post("/trigger", response_model=TriggerResponse)
async def trigger_training(req: TriggerRequest):
    """
    Manually triggers the Automated ML Training Pipeline via Celery.
    This endpoint is called by the Admin Console when an admin clicks "Retrain Model".
    """
    try:
        # Dispatch to Celery worker
        task = run_training_pipeline.delay(force=req.force_repro)
        
        return TriggerResponse(
            message="Training pipeline triggered successfully.",
            task_id=task.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
