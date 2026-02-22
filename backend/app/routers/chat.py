# app/routers/chat.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict

router = APIRouter()

# ---------------------
# CONNECTION MANAGER
# ---------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.rooms: Dict[str, List[WebSocket]] = {"global": []}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket
        self.rooms.setdefault("global", []).append(websocket)
        await self.broadcast_room("global", {"type": "join", "username": username})

    def disconnect(self, username: str):
        ws = self.active_connections.pop(username, None)
        if ws:
            for room in self.rooms.values():
                if ws in room:
                    room.remove(ws)

    async def send_personal_message(self, message: dict, username: str):
        if username in self.active_connections:
            await self.active_connections[username].send_json(message)

    async def broadcast_room(self, room: str, message: dict):
        for connection in self.rooms.get(room, []):
            await connection.send_json(message)


manager = ConnectionManager()

# ---------------------
# WEBSOCKET ENDPOINT
# ---------------------
@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            if action == "message":
                msg = {
                    "type": "message",
                    "from": username,
                    "text": data["text"],
                    "room": data.get("room", "global"),
                    "to": data.get("to")
                }

                if msg["to"]:
                    # Private message
                    await manager.send_personal_message(msg, msg["to"])
                    await manager.send_personal_message(msg, username)
                else:
                    # Group message
                    await manager.broadcast_room(msg["room"], msg)

            elif action == "join_room":
                room = data["room"]
                manager.rooms.setdefault(room, []).append(websocket)
                await manager.broadcast_room(room, {"type": "info", "msg": f"{username} joined {room}"})

    except WebSocketDisconnect:
        manager.disconnect(username)
        await manager.broadcast_room("global", {"type": "leave", "username": username})
