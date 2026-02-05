from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.wsConnectionManger import ConnectionManager

router = APIRouter(prefix="/ws-dashboard", tags=["Dashboard-WS"])
manager = ConnectionManager()


@router.websocket("/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"Client {session_id} said: {data}", session_id)

    except WebSocketDisconnect:
        await manager.disconnect(websocket, session_id)
