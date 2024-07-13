from typing import Optional
from datetime import timedelta

from fastapi import Depends, status
from fastapi.security import HTTPBasicCredentials

from main.core.exceptions import (
    InvalidUserCredentialsException,
    UserAlreadyExistException,
    UserNotFoundException,
    InactiveUserAccountException,
    InvalidTokenException
)
from main.core.logger import logger
from main.core.security import create_access_token, verify_password, verify_access_token
from main.db.repositories.users import UsersRepository, get_users_repository
from main.models.user import User
from main.schemas.user import UserInCreate, UserLogin, UserToken



class UserService:
    def __init__(
        self, user_repo: UsersRepository = Depends(get_users_repository)
    ) -> None:
        self.user_repo = user_repo

    def login_user(self, user: UserLogin) -> UserToken:
        """
        Authenticate user with provided credentials.
        """
        logger.info("Try to login user: %s", user.username)
        self.authenticate(username=user.username, password=user.password)
        access_token = (create_access_token(user.username))
        return UserToken(access_token=access_token)

    def register_user(self, user_create: UserInCreate) -> User:
        """
        Register user in application.
        """
        logger.info(f"Try to find user: {user_create.username}")
        db_user = self.user_repo.get_by_username(username=user_create.username)
        if db_user:
            raise UserAlreadyExistException(
                message=f"User with username: `{user_create.username}` already exists",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        logger.info(f"Creating user: {user_create.username}")
        user = self.user_repo.create(obj_create=user_create)
        return user

    def get_user_by_token(self, token: str) -> Optional[User]:
        """
        Retrieve current user info by JWT Token.
        """
        logger.info("Looking up user by token_data: %s", token)
        token_data: str = verify_access_token(token)
        if not token_data:
            logger.warning("Invalid token")
            raise InvalidTokenException(
                message="Invalid token", status_code=status.HTTP_400_BAD_REQUEST
        )
        return self.user_repo.get_by_username(username=token_data)
    
    def get_user(self, credentials: HTTPBasicCredentials) -> Optional[User]:
        """
        Retrieve current user info by login credentials.
        """
        logger.info("Getting user: %s", credentials.username)
        return self.user_repo.get_by_username(username=credentials.username)

    def authenticate(self, username: str, password: str) -> User:
        """
        Authenticate user.
        """
        logger.info("Try to authenticate user: %s", username)
        user: User = self.user_repo.get_by_username(username=username)
        if not user:
            logger.warning(f"User with username: `{username}` not found")
            raise UserNotFoundException(
                message=f"User with username: `{username}` not found",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        if not verify_password(
            plain_password=password, hashed_password=user.password
        ):
            logger.warning("Invalid credentials")
            raise InvalidUserCredentialsException(
                message="Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED
            )
        return user

    def check_is_active(self, user: User) -> bool:
        """
        Check if user account is active.
        """
        if user.disabled:
            logger.warning("Invalid credentials")
            raise InactiveUserAccountException(
                message="Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED
            )
        return self.user_repo.is_active(user=user)
