from typing import Any
from fastapi import WebSocket
import json


class ConnectionManager:
    def __init__(self) -> None:
        self.active_sessions: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, ses_id: str):
        await websocket.accept()
        if ses_id not in self.active_sessions:
            self.active_sessions[ses_id] = []
        self.active_sessions[ses_id].append(websocket)

    async def disconnect(self, websocket: WebSocket, ses_id: str):
        if ses_id in self.active_sessions:
            self.active_sessions[ses_id].remove(websocket)
            if not self.active_sessions[ses_id]:
                del self.active_sessions[ses_id]

    async def send_message(self, msg: str, ses_id: str):
        if ses_id in self.active_sessions:
            for socket in self.active_sessions[ses_id]:
                await socket.send_text(msg)

    async def send_payload(self, payload: dict[str, Any], ses_id: str):
        if ses_id in self.active_sessions:
            for socket in self.active_sessions[ses_id]:
                await socket.send_json(payload)
