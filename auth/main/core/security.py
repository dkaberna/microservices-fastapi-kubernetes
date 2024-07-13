from typing import Any
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

import jwt
from main.core.config import get_app_settings
#from main.schemas.token import TokenPayload

from main.core.exceptions import (
    InvalidUserCredentialsException,
    InvalidTokenException
)
from fastapi import status
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from main.core.logger import logger

settings = get_app_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Convert user password to hash string.
    """
    return pwd_context.hash(secret=password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check if the user password from request is valid.
    """
    return pwd_context.verify(secret=plain_password, hash=hashed_password)

def create_access_token(subject: str | Any) -> str:
    """
    Create access token
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, key=settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_access_token(token: str)->str:
    """
    Verify access token and return token payload
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        # Using this will require I use FastAPI/sqlmodel.  Not ready for that yet
        #token_data = TokenPayload(**payload)
        username: str = payload.get("sub")

    except(InvalidTokenError, ValidationError):
        logger.warning("Invalid token: %s", ValidationError)
        raise InvalidTokenException(
            message="Invalid token", status_code=status.HTTP_400_BAD_REQUEST
        )
    return username