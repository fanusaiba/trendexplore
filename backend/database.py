import os
from dotenv import load_dotenv
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.models import User
from fastapi_users_db_beanie import BeanieUserDatabase

# Load environment variables (for local development)
load_dotenv()

# Get MongoDB URL from environment variable
DATABASE_URL = os.getenv("MONGO_URL")
DATABASE_NAME = "trendexplore"

# Create MongoDB client
client = AsyncIOMotorClient(DATABASE_URL)
db = client[DATABASE_NAME]

messages_collection = db["messages"]

async def init_db():
    await init_beanie(
        database=db,
        document_models=[User],
    )

async def get_user_db():
    yield BeanieUserDatabase(User)
