from fastapi_users_db_beanie import BeanieBaseUser
from beanie import Document


class User(BeanieBaseUser,Documents):
    class Settings:
        name = "users"