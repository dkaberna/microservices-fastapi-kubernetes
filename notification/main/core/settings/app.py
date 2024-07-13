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
    pika_connection_parameter: str
    logging_level: int = logging.INFO
    token_file: str
    credentials_file: str
    gmail_admin_email_address: str
