import os
import asyncio
import random
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError
from textblob import TextBlob

from database import init_db, messages_collection
from users import fastapi_users, auth_backend, current_user
from schemas import UserRead, UserCreate

SECRET = os.getenv("SECRET", "change_me")

app = FastAPI(title="TrendExplore API")

# ---------------------------
# CORS (IMPORTANT)
# ---------------------------
origins = [
    "https://trendexplore.vercel.app",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
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


# ---------------------------
# ROOT
# ---------------------------
@app.get("/")
def root():
    return {"message": "TrendExplore backend running 🚀"}


# ---------------------------
# TRENDS API
# ---------------------------
@app.get("/api/trends")
def get_trends(
    country: str = "US",
    category: str = "All",
    user=Depends(current_user),
):
    data = [
        {"title": "AI replacing developers?", "source": "Twitter", "country": "US", "score": 98},
        {"title": "Apple Vision Pro 2", "source": "Google", "country": "US", "score": 90},
        {"title": "OpenAI vs Google war", "source": "News", "country": "UK", "score": 85},
    ]

    filtered = [
        t for t in data
        if (category == "All" or t["source"] == category)
        and t["country"] == country
    ]

    return {"user": user.email, "trends": filtered}


# ---------------------------
# WEBSOCKET CHAT
# ---------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.rooms: Dict[str, List[WebSocket]] = {"global": []}

    async def connect(self, websocket: WebSocket, username: str):
        self.active_connections[username] = websocket
        self.rooms.setdefault("global", []).append(websocket)

    def disconnect(self, username: str):
        ws = self.active_connections.pop(username, None)
        if ws:
            for room in self.rooms.values():
                if ws in room:
                    room.remove(ws)

    async def broadcast(self, room: str, message: dict):
        for ws in self.rooms.get(room, []).copy():
            try:
                await ws.send_json(message)
            except Exception:
                if ws in self.rooms.get(room, []):
                    self.rooms[room].remove(ws)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    token = websocket.cookies.get("trend_auth")

    if not token:
        await websocket.close(code=1008)
        return

    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        username = payload.get("sub")

        if not username:
            await websocket.close(code=1008)
            return

    except JWTError:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, username)

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            if action == "message":
                room = data.get("room", "global")
                text = data.get("text", "")

                msg = {
                    "type": "message",
                    "room": room,
                    "sender": username,
                    "text": text
                }

                await manager.broadcast(room, msg)

    except WebSocketDisconnect:
        manager.disconnect(username)
        await manager.broadcast("global", {"type": "leave", "username": username})


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