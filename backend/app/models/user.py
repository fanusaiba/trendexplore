from beanie import Document
from fastapi_users_db_beanie import BeanieBaseUser
from pydantic import Field
from typing import Optional
from uuid import UUID, uuid4


class User(BeanieBaseUser, Document):
    id: UUID = Field(default_factory=uuid4)

    class Settings:
        name = "users"