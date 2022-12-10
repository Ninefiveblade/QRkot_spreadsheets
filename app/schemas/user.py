from fastapi_users import schemas


class User(schemas.BaseUser):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
