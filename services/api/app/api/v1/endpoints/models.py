from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_models():
    """Model registry overview."""
    return {"champion": "XGBoost", "challengers": []}
