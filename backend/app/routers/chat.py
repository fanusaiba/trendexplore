from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.rooms: Dict[str, List[WebSocket]] = {"global": []}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket
        self.rooms.setdefault("global", []).append(websocket)

        await self.broadcast_room("global", {
            "type": "join",
            "username": username,
            "text": f"{username} joined the chat"
        })

    def disconnect(self, username: str):
        ws = self.active_connections.pop(username, None)
        if ws:
            for room in self.rooms.values():
                if ws in room:
                    room.remove(ws)

    async def broadcast_room(self, room: str, message: dict):
        dead_connections = []

        for connection in self.rooms.get(room, []):
            try:
                await connection.send_json(message)
            except:
                dead_connections.append(connection)

        for dead in dead_connections:
            if dead in self.rooms.get(room, []):
                self.rooms[room].remove(dead)

manager = ConnectionManager()

@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("action") == "message":
                text = data.get("text", "").strip()

                if text:
                    await manager.broadcast_room("global", {
                        "type": "message",
                        "username": username,
                        "text": text
                    })

    except WebSocketDisconnect:
        manager.disconnect(username)
        await manager.broadcast_room("global", {
            "type": "leave",
            "username": username,
            "text": f"{username} left the chat"
        })