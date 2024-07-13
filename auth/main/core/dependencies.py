from typing import Annotated
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer

from main.core.exceptions import (
    InactiveUserAccountException,
)
from main.core.config import get_app_settings
from main.models.user import User
from main.services.user import UserService

settings = get_app_settings()

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: Annotated[str, Depends(reusable_oauth2)],
    user_service: Annotated[UserService, Depends()]) -> User:
    """
    Return current user.
    """
    user = user_service.get_user_by_token(token)
    if not user:
        raise InactiveUserAccountException(
            message="Invalid token in get_current_user", status_code=status.HTTP_400_BAD_REQUEST
        )
    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends()]
) -> User:
    """
    Return current active user.
    """
    if not user_service.check_is_active(user=current_user):
        raise InactiveUserAccountException(
            message="Inactive user in get_current_user", status_code=status.HTTP_400_BAD_REQUEST
        )
    return current_user
