from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from textblob import TextBlob
from pydantic import BaseModel
import asyncio
import random
from datetime import datetime
from jose import jwt,JWTError

# ✅ Local imports
from .database import init_db, messages_collection
from .users import fastapi_users, current_user, auth_backend
from .schemas import UserRead, UserCreate
import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from backend.app.models import User

SECRET = "this_is_my_super_secret_key_that_is_very_long_12345"

# 🚀 App Initialization
app = FastAPI(title="TrendExplore API")


@app.on_event("startup")
async def app_init():
    client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    await init_beanie(
        database=client["trendexplore"],
        document_models=[User]
    )

# 🌐 CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        
        "https://trendexplore.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Auth Routers (ONLY ONCE)
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


# ✅ Health Check
@app.get("/")
def root():
    return {"message": "TrendExplore backend running 🚀"}


# ✅ Trends API (protected)
@app.get("/api/trends")
def get_trends(
    country: str = "US",
    category: str = "All",
    user=Depends(current_user)  # ✅ requires login cookie
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
# 💬 WebSocket Chat (Rooms + MongoDB Save)
# ---------------------------

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.rooms: Dict[str, List[WebSocket]] = {"global": []}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket

        # join global by default
        self.rooms.setdefault("global", []).append(websocket)

        await self.broadcast("global", {"type": "join", "username": username})

    def disconnect(self, username: str):
        ws = self.active_connections.pop(username, None)
        if ws:
            for room in self.rooms.values():
                if ws in room:
                    room.remove(ws)

    async def send_personal(self, username: str, message: dict):
        ws = self.active_connections.get(username)
        if ws:
            await ws.send_json(message)

    async def broadcast(self, room: str, message: dict):
        connections = self.rooms.get(room, []).copy()
        for ws in connections:
            try:
                await ws.send_json(message)
            except Exception:
                if room in self.rooms and ws in self.rooms[room]:
                    self.rooms[room].remove(ws)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    # Accept connection first
    await websocket.accept()

    # Get JWT cookie
    token = websocket.cookies.get("trend_auth")

    if not token:
        await websocket.close(code=1008)
        return

    # Validate JWT
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        username = payload.get("sub")

        if not username:
            await websocket.close(code=1008)
            return

    except JWTError:
        await websocket.close(code=1008)
        return

    # Connect user to manager
    await manager.connect(websocket, username)

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            # ===============================
            # KEEP YOUR EXISTING LOGIC HERE
            # (join_room, send_message, etc.)
            # ===============================

            if action == "join_room":
                room = data.get("room", "global")
                manager.rooms.setdefault(room, [])
                manager.rooms[room].append(websocket)

                await manager.broadcast(
                    room,
                    {
                        "type": "info",
                        "msg": f"{username} joined {room}"
                    }
                )

            elif action == "message":
                room = data.get("room", "global")
                text = data.get("text")

                msg = {
                    "type": "message",
                    "room": room,
                    "sender": username,
                    "text": text,
                }

                await manager.broadcast(room, msg)

    except WebSocketDisconnect:
        manager.disconnect(username)
        await manager.broadcast(
            "global",
            {"type": "leave", "username": username}
)
# ✅ Chat history API
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
# 🔥 Simulated Trend Updates
# ---------------------------
async def simulate_trend_updates():
    while True:
        await asyncio.sleep(5)

        fake_trend = {
            "type": "trend_update",
            "trend": {
                "title": f"Live Trend {random.randint(1, 100)}",
                "source": "Google",
                "score": random.randint(50, 100)
            }
        }

        await manager.broadcast("global", fake_trend)


# ---------------------------
# 🧠 Sentiment API
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
    return {"title": title, "sentiment": sentiment, "summary": summary}

class User(BaseModel):
    email: str
    password: str


@app.post("/auth/register")
def register(user: User):
    # For now simple response (we will improve later)
    return {
        "message": "User registered successfully",
        "email": user.email
    }
@app.post("/auth/login")
def login(user: User):
    # Dummy login validation
    return {
        "message": "Login successful",
        "email": user.email
    }

