from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from main.api.router import router as api_router
from main.core.config import get_app_settings
from main.core.exceptions import add_exceptions_handlers
from main.core.rabbit_connection import rabbit_connection
from main.core.logger import logger

@asynccontextmanager
async def lifespan(_: FastAPI):
    await rabbit_connection.connect()
    logger.info ("Calling rabbit_connection.connect()")
    yield
    await rabbit_connection.disconnect()
    logger.info ("Calling rabbit_connection.disconnect()")

def create_app() -> FastAPI:
    """
    Application factory, used to create application.
    """
    settings = get_app_settings()

    application = FastAPI(**settings.fastapi_kwargs, lifespan=lifespan)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix=settings.api_prefix)

    add_exceptions_handlers(app=application)

    return application



app = create_app()
