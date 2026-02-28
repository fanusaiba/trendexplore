from beanie import Document
from fastapi_users import schemas
from fastapi_users.db import BeanieUserDatabase
from pydantic import EmailStr
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel


class User(Document):
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Settings:
        name = "users"