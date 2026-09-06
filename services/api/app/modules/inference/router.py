from fastapi import APIRouter

router = APIRouter(prefix="/inference", tags=["inference"])

@router.get("/")
async def get_inference():
    return {"message": "inference router active"}
