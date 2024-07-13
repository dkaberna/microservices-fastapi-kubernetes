import logging
from typing import Any, Dict, List  # This module provides runtime support for type hints

from main.core.settings.base import BaseAppSettings



class AppSettings(BaseAppSettings):
    """
    Base application settings
    """

    debug: bool = False
    rabbitmq_video_queue: str
    rabbitmq_mp3_queue: str
    pymongo_videos_collection: str
    pymongo_mp3s_collection: str
    mongo_client_address: str
    pika_connection_parameter: str
    logging_level: int = logging.INFO