from fastapi import APIRouter

router = APIRouter()


@router.post("/predict")
def predict():
    """Primary inference endpoint for network events."""
    return {"status": "ok", "prediction": "Normal", "confidence": 0.99}


@router.post("/explain")
def explain():
    """Async explanation request."""
    return {"task_id": "1234-abcd"}
