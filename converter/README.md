Converter Microservice
====================

### Stack:
- Aio-Pika
- RabbitMQ
- PyMongo
- MongoDB
- moviepy.editor 
- Docker

Configuration
--------------

Replace `.env.example` with real `.env`, changing placeholders

```
MONGO_CLIENT_ADDRESS = "mongodb://admin:admin@mongo:27017/?authSource=admin"
PIKA_CONNECTION_PARAMETER = "rabbitmq"
```

Local install
-------------

Setup and activate a python3 virtualenv via your preferred method. e.g. and install production requirements:

    $ make venv

For remove virtualenv:

    $ make clean


Local run
-------------

Run server with settings:

    $ make runserver


Run in Docker
-------------

### !! Note:

If you want to run app in `Docker` rather than `localhost`, you will need to change `MONGO_CLIENT_ADDRESS` and `PIKA_CONNECTION_PARAMETER` in `.env` based on your specific configuration.

Run project in Docker:

    $ make docker_build

Stop project in Docker:

    $ make docker_down

Project structure
-----------------
Files related to application are in the ``main`` directory.
Application parts are:
```text
main
├── core
│   ├── config.py
│   ├── __init__.py
│   ├── logger.py
│   └── settings
│       ├── app.py
│       ├── base.py
│       ├── __init__.py
├── __init__.py
```