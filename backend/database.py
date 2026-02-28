import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from backend.app.models.user import User


async def init_db():
    client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    db = client["trendexplore"]
    await init_beanie(database=db, document_models=[User])