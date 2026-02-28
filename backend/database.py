import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi_users_db_beanie import BeanieUserDatabase
from backend.app.models import User

client = None
db = None


async def init_db():
    global client, db

    mongo_url = os.getenv("MONGO_URL")

    if not mongo_url:
        raise ValueError("MONGO_URL is not set")

    client = AsyncIOMotorClient(mongo_url)
    db = client["trendexplore"]

    await init_beanie(
        database=db,
        document_models=[User],
    )

    print("✅ MongoDB connected successfully")


async def get_user_db():
    yield BeanieUserDatabase(User)