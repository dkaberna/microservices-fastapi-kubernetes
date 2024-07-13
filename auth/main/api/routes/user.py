from typing import Annotated
from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm
from main.core.dependencies import get_current_active_user
#from main.models.user import User
from main.schemas.response import Response
from main.schemas.user import User, UserInCreate, UserInDB, UserLogin, UserToken, UserOut

from main.services.user import UserService

router = APIRouter()


@router.post("/register", response_model=Response[UserInDB])
def register_user(
    user: UserInCreate, user_service: UserService = Depends()
) -> Response:
    """
    Process user registration.
    """
    user = user_service.register_user(user_create=user)
    return Response(data=user, message="The user was registered successfully")


@router.post("/login", response_model=Response[UserToken])
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends())->Response:
    """
    Process user login. Returns JWT if valid
    """
    token = user_service.login_user(form_data)
    return Response(data=token, message="The user authenticated successfully")

#Testing only
#**********************
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
@router.get("/verify_current_user_test")#, response_model=Response[UserOut])
def verify_current_user_test(
    token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Validate request from gateway. Returns user if it exists in database and is active.
    """
    return token
#**********************


@router.get("/verify_current_user", response_model=Response[UserOut])
def verify_current_user(
    current_user = Depends(get_current_active_user))-> Response:
    """
    Validate request from gateway. Returns user if it exists in database and is active.
    """
    if current_user:
        return Response(data=current_user)
