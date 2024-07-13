import pika, sys, os, time, json
import asyncio
import aio_pika

# Import the email modules we'll need
from email.message import EmailMessage
from aio_pika import Message
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustChannel, DeliveryMode

from main.core.config import get_app_settings
from main.core.logger import logger
from main.core.emailer import notifier

settings = get_app_settings()


async def main():
    PARALLEL_TASKS = 10

    async def on_message(message: AbstractIncomingMessage) -> None:
        async with message.process():
            # Call notification function
            logger.info("Calling notification function")
            notifier.send_email(message)

    connection = await aio_pika.connect_robust(host=settings.pika_connection_parameter, login='guest', password='guest', port=5672)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=PARALLEL_TASKS)
        queue = await channel.declare_queue(settings.rabbitmq_mp3_queue, durable=True)
        await queue.consume(on_message)

        try:
            logger.info("Running await asyncio.Future()")
            await asyncio.Future()
        finally:
            await connection.close()

    logger.info("Waiting for messages. To exit press CTRL+C")


if __name__ == "__main__":
    try:
        logger.info('Starting notification service...')
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
