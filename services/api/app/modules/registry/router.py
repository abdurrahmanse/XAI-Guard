from fastapi import APIRouter

router = APIRouter(prefix="/models", tags=["registry"])


@router.get("/")
def get_models():
    return {"champion": "XGBoost", "challengers": []}
