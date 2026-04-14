import os
from typing import Optional
from uuid import UUID

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users_db_beanie import BeanieUserDatabase

from app.models.user import User
from database import get_user_db

SECRET = os.getenv("SECRET", "change_me")


class UserManager(BaseUserManager[User, UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_manager(
    user_db: BeanieUserDatabase = Depends(get_user_db),
):
    yield UserManager(user_db)


cookie_transport = CookieTransport(
    cookie_name="trend_auth",
    cookie_max_age=3600,
    cookie_secure=True,
    cookie_samesite="none",
    cookie_path="/",
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()