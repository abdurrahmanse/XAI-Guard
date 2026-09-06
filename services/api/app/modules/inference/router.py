from fastapi import APIRouter

router = APIRouter(prefix="/inference", tags=["inference"])


@router.post("/predict")
def predict():
    return {"status": "ok", "prediction": "Normal", "confidence": 0.99}


@router.post("/explain")
def explain():
    return {"task_id": "1234-abcd"}
