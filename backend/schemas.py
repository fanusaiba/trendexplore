from fastapi_users import schemas
from beanie import PydanticObjectId


# Response model
class UserRead(schemas.BaseUser[PydanticObjectId]):
    pass

# Registration model
class UserCreate(schemas.BaseUserCreate):
    pass

# Update model
class UserUpdate(schemas.BaseUserUpdate):
    pass

