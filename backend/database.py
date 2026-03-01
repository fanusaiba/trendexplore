import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi_users_db_beanie import BeanieUserDatabase

from app.models.user import User

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = "trendexplore"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

messages_collection = db["messages"]


async def init_db():
    await init_beanie(database=db, document_models=[User])


async def get_user_db():
    yield BeanieUserDatabase(User)