from fastapi_users_db_beanie import BeanieBaseUser
from beanie import PydanticObjectId


class User(BeanieBaseUser[PydanticObjectId]):
    class Settings:
        name = "users"