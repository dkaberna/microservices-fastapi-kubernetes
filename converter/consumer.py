import pika
import sys
import os
import json
import tempfile
import gridfs
import asyncio
import aio_pika
import moviepy.editor 

from pymongo import MongoClient
from bson.objectid import ObjectId
from main.core.config import get_app_settings
from main.core.logger import logger
from aio_pika import Message
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustChannel, DeliveryMode

settings = get_app_settings()

async def convert_to_mp3(message, fs_videos: gridfs, fs_mp3s: gridfs, channel: AbstractRobustChannel) -> None:
    """
    Convert youtube file to mp3 and publish onto queue
    """
    message = json.loads(message.body.decode())

    # empty temp file
    tf = tempfile.NamedTemporaryFile()
    # video contents
    out = fs_videos.get(ObjectId(message["video_fid"]))
    # add video contents to empty file
    tf.write(out.read())
    # create audio from temp video file
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    # write audio to the file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)
    logger.info("Running convert to mp3 function using video fid: %s", message["video_fid"])

    # save file to mongo
    with open(tf_path, mode="rb") as f:
        try:
            data = f.read()
            fid = fs_mp3s.put(data)
        except Exception as err:
            logger.error("Exception occurred during saving to pymongo: %s", err)
            #print(err)
        finally:
            os.remove(tf_path)

    message["mp3_fid"] = str(fid)
    message = Message(
            body=json.dumps(message).encode(), delivery_mode=DeliveryMode.PERSISTENT,
        )

    try:
        # Sending the message
        await channel.default_exchange.publish(
            message, str(settings.rabbitmq_mp3_queue),
        )
        logger.info("Message to mp3 queue successfully sent with mp3 fid: %s",str(fid))

    except Exception as err:
        fs_mp3s.delete(fid)
        logger.error("Failed to publish message to mp3 queue, %s", err)

async def main():
    """
    Main entry point.
    """
    client = MongoClient(settings.mongo_client_address)
    # Check if videos/mp3s collection exists, create it if not
    videos_db = client[settings.pymongo_videos_collection]
    mp3s_db = client[settings.pymongo_mp3s_collection]

    fs_videos = gridfs.GridFS(videos_db)
    fs_mp3s = gridfs.GridFS(mp3s_db)

    PARALLEL_TASKS = 10


    async def on_message(message: AbstractIncomingMessage) -> None:
        async with message.process():
            await convert_to_mp3(message, fs_videos, fs_mp3s, channel)

    connection = await aio_pika.connect_robust(host=settings.pika_connection_parameter, login='guest', password='guest', port=5672)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=PARALLEL_TASKS)
        queue = await channel.declare_queue(settings.rabbitmq_video_queue, durable=True)
        await queue.consume(on_message)

        try:
            await asyncio.Future()
        finally:
            await connection.close()

    logger.info("Waiting for messages. To exit press CTRL+C")

if __name__ == "__main__":
    try:
        logger.info('Starting converter service...')
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)