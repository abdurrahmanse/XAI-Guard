from fastapi import APIRouter, WebSocket

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/")
def get_alerts():
    return {"alerts": []}


@router.websocket("/ws")
async def websocket_alerts(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"event": "connected"})
