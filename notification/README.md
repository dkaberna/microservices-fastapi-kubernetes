Notification Microservice
====================

### Stack:
- Aio-Pika
- RabbitMQ
- google.oauth2
- Docker

Configuration
--------------

Replace `.env.example` with real `.env`, changing placeholders

```
GMAIL_ADMIN_EMAIL_ADDRESS = 'youremail@example.com'
PIKA_CONNECTION_PARAMETER = "rabbitmq"
```

Using OAuth 2.0 to Access Google APIs
--------------
This microservice sends notification emails using Google's Gmail service.  In order to use Gmail, you must follow the directions outlined in this link: https://developers.google.com/identity/protocols/oauth2.

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

If you want to run app in `Docker` rather than `localhost`, you will need to change `PIKA_CONNECTION_PARAMETER` in `.env` based on your specific configuration.

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
│   ├── emailer.py
│   ├── __init__.py
│   ├── logger.py
│   ├── requirements.txt
│   ├── settings
│   │   ├── app.py
│   │   ├── base.py
│   │   ├── __init__.py
│   └── token.pickle
├── __init__.py
```