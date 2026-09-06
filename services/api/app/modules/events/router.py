from fastapi import APIRouter

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/")
async def get_events():
    return {"message": "events router active"}
