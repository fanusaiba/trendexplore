import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from backend.app.models.user import User
from fastapi_users.db import BeanieUserDatabase
load_dotenv()

DATABASE_URL = os.getenv("MONGO_URL")
DATABASE_NAME = "trendexplore"

client = AsyncIOMotorClient(DATABASE_URL)
db = client[DATABASE_NAME]

# ✅ ADD THIS BACK
messages_collection = db["messages"]

async def init_db():
    await init_beanie(
        database=db,
        document_models=[User],
    )