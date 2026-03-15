from fastapi_users import schemas
from pydantic import EmailStr
from typing import Optional


class UserRead(schemas.BaseUser[str]):
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    email: Optional[EmailStr] = None
    password: Optional[str] = None