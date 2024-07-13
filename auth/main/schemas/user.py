from datetime import datetime
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """
    User Schema
    """
    username: str
    email: EmailStr | None = None
    

class UserInCreate(User):
    """
    UserInCreate Schema
    """
    password: str


class UserOut(BaseModel):
    """
    UserOut Schema
    """
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


###########################################################################################
class UserLogin(BaseModel):
    """
    UserLogin Schema
    """
    username: str
    password: str

    class Config:
        schema_extra = {"example": {"username": "user", "password": "weakpassword"}}



class UserInDB(User):
    """
    UserInDB Schema
    """
    class Config:
        # Pydantic's orm_mode will tell the Pydantic model to read the data
        # even if it is not a dict, but an ORM model (or any other arbitrary object with attributes)
        orm_mode = True

class UserToken(BaseModel):
    """
    UserToken Schema
    """
    access_token: str
    token_type: str = "bearer"

class UserInUpdate(User):
    """
    UserInUpdate Schema
    """
    password: str | None
