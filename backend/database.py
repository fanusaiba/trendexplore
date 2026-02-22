from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.models import User
from fastapi_users_db_beanie import BeanieUserDatabase

DATABASE_URL = "mongodb://localhost:27017"
DATABASE_NAME = "trendexplore"

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

