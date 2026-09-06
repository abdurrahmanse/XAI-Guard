from fastapi import APIRouter

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/")
async def get_alerts():
    return {"message": "alerts router active"}
