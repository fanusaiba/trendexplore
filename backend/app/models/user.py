from beanie import Document
from fastapi_users_db_beanie import BeanieBaseUser
from uuid import UUID, uuid4
from pydantic import Field


class User(BeanieBaseUser, Document):
    id: UUID = Field(default_factory=uuid4)

    class Settings:
        name = "users"