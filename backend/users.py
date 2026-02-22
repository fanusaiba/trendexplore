# backend/users.py

from fastapi import Depends
from fastapi_users import FastAPIUsers, BaseUserManager
from fastapi_users.authentication import (
    CookieTransport,
    AuthenticationBackend,
    JWTStrategy,
)
from fastapi_users_db_beanie import BeanieUserDatabase

from backend.app.models import User
from .database import get_user_db
from beanie import PydanticObjectId



SECRET = "this_is_my_super_secret_key_that_is_very_long_12345"


# =========================
# User Manager
# =========================

class UserManager(BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    def parse_id(self, value: str) -> PydanticObjectId:
        return PydanticObjectId(value)

async def get_user_manager(
    user_db: BeanieUserDatabase[User] = Depends(get_user_db),
):
    yield UserManager(user_db)


# =========================
# Cookie transport
# =========================

cookie_transport = CookieTransport(
    cookie_name="trend_auth",
    cookie_max_age=3600,
)


# =========================
# JWT strategy
# =========================

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


# =========================
# Auth backend
# =========================

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


# =========================
# FastAPI Users instance
# =========================

fastapi_users = FastAPIUsers[User, str](
    get_user_manager,
    [auth_backend],
)

# Current user dependency
current_user = fastapi_users.current_user()
