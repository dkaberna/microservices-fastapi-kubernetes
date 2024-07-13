from fastapi import APIRouter

from main.api.routes import status, user

router = APIRouter()

router.include_router(router=status.router, tags=["Status"], prefix="/status")
router.include_router(router=user.router, tags=["User"], prefix="/user")
