from beanie import Document
from pydantic import EmailStr
from fastapi_users.db import BeanieUserDatabase

class User(Document):
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Settings:
        name = "users"