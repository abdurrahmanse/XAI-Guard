from fastapi import APIRouter

router = APIRouter(prefix="/registry", tags=["registry"])

@router.get("/")
async def get_registry():
    return {"message": "registry router active"}
