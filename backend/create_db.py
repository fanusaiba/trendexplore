import asyncio
from .database import Base, engine

async def init():
    async with engine.begin() as conn:
        print("🧱 Creating database tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Database created successfully!")

if __name__ == "__main__":
    asyncio.run(init())

