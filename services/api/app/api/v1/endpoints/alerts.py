from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.get("/")
def get_alerts():
    """Paginated alert feed."""
    return {"alerts": []}


@router.websocket("/ws")
async def websocket_alerts(websocket: WebSocket):
    """WebSocket real-time alert stream."""
    await websocket.accept()
    await websocket.send_json({"event": "connected"})
    # Keep connection open for real-time pushing
    # await websocket.close()
