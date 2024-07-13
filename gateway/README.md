FastAPI Gateway Microservice
====================

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://github.com/tiangolo/fastapi)

FastAPI gateway

### Stack:
- FastAPI
- Aio-Pika
- RabbitMQ
- PyMongo
- MongoDB
- Docker

Configuration
--------------

Replace `.env.example` with real `.env`, changing placeholders

```
AUTH_SVC_ADDRESS = "auth:5000"
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

If you want to run app in `Docker` rather than `localhost`, you will need to change `AUTH_SVC_ADDRESS`, `MONGO_CLIENT_ADDRESS`, and `PIKA_CONNECTION_PARAMETER` in `.env` based on your specific configuration

Run project in Docker:

    $ make docker_build

Stop project in Docker:

    $ make docker_down

To ensure microservice is running, run this command:

    $ curl -X "GET" http://0.0.0.0:8080/api/v1/status

Expected result:

```
{
  "success": true,
  "version": "<version>",
  "message": "Gateway Application"
}
```
### Unit-Testing

#### Register user:

To test user registration, use a valid email address and create a password:

    $ curl -X 'POST' \
        'http://0.0.0.0:8080/api/v1/user/register' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
            "username": "test-user",
            "email": "test@test.com",
            "password": "weakpassword"
        }'

If everything is fine, you will get this message back:
```
{
    "success": true,
    "data": {
        "username": "test-user",
        "email": "test@test.com"
    },
    "message": "The user was registered successfully",
    "errors": null
}
```
#### User Authentication:
You can then authenticate using the `login` route based on the credentials you created just now.

    $ curl -X 'POST' \
        'http://0.0.0.0:8080/api/v1/user/login' \
        -H 'Content-Type: application/x-www-form-urlencoded' \
        -d 'username=test-user&password=weakpassword'

If everything is fine, you will get this message back which contains your JWT:
```
{
    "success": true,
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjA4NDQwMzYsInN1YiI6InRlc3QtdXNlcjEifQ.-fPU-sXU-OJFKznilgJ5sbJFwUxIJdo5syVOjgnvTwM",
        "token_type": "bearer"
    },
    "message": "The user authenticated successfully",
    "errors": null
}
```
 
#### Video Conversion:
To test the video conversion to mp3 process, you will need to download a video from YouTube, and then run this using the JWT you obtained from authenticating:

    $ curl -X 'POST' \
        -F 'file=@./test.mp4' \
        -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjA4NDQwMzYsInN1YiI6InRlc3QtdXNlcjEifQ.-fPU-sXU-OJFKznilgJ5sbJFwUxIJdo5syVOjgnvTwM' http://0.0.0.0:8080/api/v1/user/uploadfile

If everything is fine, you will get this message back:
```
{
    "success": true,
    "data": {
        "video_fid": "6691f5cf912085e84301a70f"
    },
    "message": "PDF file uploaded successfully",
    "errors": null
}
```
You will also receive an email (make sure you use a legitimate email address when registering) with this message:
```
mp3 file_id: 6691f8a5ed737d568756efb7 is now ready!
```

Note: the ID above will be unique every time you upload a new video.

#### MP3 Download:

You can then download the newly converted mp3 file by using the mp3 file_id sent to your email using the GET API route:

    $ curl -X 'GET' \
        -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjA4NDQwMzYsInN1YiI6InRlc3QtdXNlcjEifQ.-fPU-sXU-OJFKznilgJ5sbJFwUxIJdo5syVOjgnvTwM' http://0.0.0.0:8080/api/v1/user/download/6691f8a5ed737d568756efb7

Web routes
----------
All routes are available on ``/`` or ``/redoc`` paths with Swagger or ReDoc.


Project structure
-----------------
Files related to application are in the ``main`` directory.
Application parts are:
```text
main
├── api
│   ├── __init__.py
│   ├── router.py
│   └── routes
│       ├── __init__.py
│       ├── status.py
│       └── user.py
├── app.py
├── core
│   ├── config.py
│   ├── exceptions.py
│   ├── __init__.py
│   ├── logger.py
│   ├── rabbit_connection.py
│   └── settings
│       ├── app.py
│       ├── base.py
│       ├── __init__.py
├── __init__.py
└── schemas
    ├── __init__.py
    ├── response.py
    ├── status.py
    └── user.py
```