RabbitMQ Microservice
====================

### Stack:
- RabbitMQ
- Docker

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

Run project in Docker:

    $ make docker_build

Stop project in Docker:

    $ make docker_down