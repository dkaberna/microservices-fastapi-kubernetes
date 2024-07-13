import logging
from typing import Any, Dict, List  # This module provides runtime support for type hints

from main.core.settings.base import BaseAppSettings
from version import response


class AppSettings(BaseAppSettings):
    """
    Base application settings
    """

    debug: bool = False
    docs_url: str = "/"
    #lifespan: str = "lifespan"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = response["message"]
    version: str = response["version"]

    auth_svc_address: str

    mongo_client_address: str
    pika_connection_parameter: str
    
    rabbitmq_video_queue: str
    rabbitmq_mp3_queue: str

    pymongo_videos_collection: str
    pymongo_mp3s_collection: str

    api_prefix: str = "/api/v1"

    allowed_hosts: List[str] = ["*"] # Wildcard for now, but not best practice

    logging_level: int = logging.INFO

    min_connection_count: int = 5
    max_connection_count: int = 10

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]: # the str can be "arbitrary", meaning it can be a string key of anything
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }