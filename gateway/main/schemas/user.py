from pydantic import BaseModel, EmailStr

class UserToken(BaseModel):
    """
    UserToken Schema
    """
    access_token: str
    token_type: str = "bearer"

class UserRegistration(BaseModel):
    """
    User Registration Schema
    """
    username: str
    email: EmailStr | None = None
    password: str