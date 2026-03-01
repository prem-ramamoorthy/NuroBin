from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, List[WebSocket]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active.setdefault(user_id, []).append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket):
        if user_id in self.active:
            self.active[user_id] = [
                ws for ws in self.active[user_id] if ws != websocket
            ]
            if not self.active[user_id]:
                del self.active[user_id]

    async def broadcast(self, user_id: str, message: dict):
        for ws in self.active.get(user_id, []):
            await ws.send_json(message)

