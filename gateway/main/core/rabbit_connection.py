import json
from dataclasses import dataclass
from aio_pika import connect_robust, Message, DeliveryMode
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel

from main.core.logger import logger
from main.core.config import get_app_settings

settings = get_app_settings()


@dataclass
class RabbitConnection:
    connection: AbstractRobustConnection | None = None
    channel: AbstractRobustChannel | None = None

    def status(self) -> bool:
        """
            Checks if connection established

            :return: True if connection established
        """
        if self.connection.is_closed or self.channel.is_closed:
            return False
        return True

    async def _clear(self) -> None:
        if not self.channel.is_closed:
            await self.channel.close()
        if not self.connection.is_closed:
            await self.connection.close()

        self.connection = None
        self.channel = None

    async def connect(self) -> None:
        """
        Establish connection with the RabbitMQ

        :return: None
        """
        logger.info('Connecting to the RabbitMQ...')
        try:
            self.connection = await connect_robust(host=settings.pika_connection_parameter, login='guest', password='guest', port=5672)
            self.channel = await self.connection.channel(publisher_confirms=False)
            logger.info('Successfully connected to the RabbitMQ!')
        except Exception as e:
            await self._clear()
            logger.error(e.__dict__)

    async def disconnect(self) -> None:
        """
        Disconnect and clear connections from RabbitMQ

        :return: None
        """
        await self._clear()

    async def send_messages(
            self,
            message_body: list | dict,
            routing_key: str
    ) -> None:
        """
            Public message or messages to the RabbitMQ queue.

            :param messages: list or dict with messages objects.
            :param routing_key: Routing key of RabbitMQ, not required. Tip: the same as in the consumer.
        """
        if not self.channel:
            logger.error('The message could not be sent because the connection with RabbitMQ is not established')
            raise RuntimeError('The message could not be sent because the connection with RabbitMQ is not established')

        if isinstance(message_body, dict):
            message_body = [message_body]
        else:
            logger.error('Error creating messagse_body')
        
        # Use transactions with async context manager
        async with self.channel.transaction():
            for message in message_body:
                message = Message(
                    body=json.dumps(message).encode(), delivery_mode=DeliveryMode.PERSISTENT
                )
                logger.info("Attempting to send message to RabbitMQ..")
                await self.channel.default_exchange.publish(
                    message, routing_key=routing_key,
                )
                logger.info("Message sent to rabbitmq")


rabbit_connection = RabbitConnection()
