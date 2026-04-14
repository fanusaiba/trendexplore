import os
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob
from dotenv import load_dotenv

from database import init_db, messages_collection
from users import fastapi_users, auth_backend
from schemas import UserRead, UserCreate
from app.models.trend import router as trend_router

load_dotenv()
SECRET = os.getenv("SECRET", "change_me")

app = FastAPI(title="TrendExplore API")


# ---------------------------
# CORS
# ---------------------------
origins = [
    "https://trendexplore.vercel.app",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------
# STARTUP
# ---------------------------
@app.on_event("startup")
async def startup():
    await init_db()


# ---------------------------
# AUTH ROUTES
# ---------------------------
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(trend_router)


# ---------------------------
# ROOT
# ---------------------------
@app.get("/")
def root():
    return {"message": "TrendExplore backend running 🚀"}


# ---------------------------
# WEBSOCKET CHAT
# ---------------------------
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


@app.websocket("/ws/{username}")
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


# ---------------------------
# CHAT HISTORY
# ---------------------------
@app.get("/api/rooms/{room_name}/messages")
async def get_room_messages(room_name: str):
    cursor = messages_collection.find({"room": room_name}).sort("timestamp", 1)

    results = []

    async for msg in cursor:
        results.append({
            "from": msg.get("sender"),
            "text": msg.get("text"),
            "to": msg.get("to"),
            "timestamp": msg.get("timestamp").isoformat() if msg.get("timestamp") else None
        })

    return results


# ---------------------------
# TREND SENTIMENT
# ---------------------------
@app.post("/api/analyze")
def analyze_trend(data: dict):
    title = data.get("title", "")

    if not title:
        return {"error": "No title provided"}

    blob = TextBlob(title)
    polarity = blob.sentiment.polarity

    if polarity > 0.2:
        sentiment = "Positive 😊"
    elif polarity < -0.2:
        sentiment = "Negative 😟"
    else:
        sentiment = "Neutral 😐"

    summary = f"This trend reflects growing public interest in '{title.split()[0]}'."

    return {
        "title": title,
        "sentiment": sentiment,
        "summary": summary
    }