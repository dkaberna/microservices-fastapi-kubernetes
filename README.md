# Microservice Architecture and System Design with Python, FastAPI & Kubernetes
====================

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://github.com/tiangolo/fastapi)

### Project Description
Purpose of this project is to showcase a fairly complex microservice architecture using the following technology stack:

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
    - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
    - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database for user registration and authentication.
    - ⚗️  [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migration and versioning.
- 🏘 [MongoDB](https://www.mongodb.com) as the NOSQL database for storing video/mp3 files during the conversion process.
- 🐇 [RabbitMQ](https://www.rabbitmq.com/) for message queuing.
- 🐋 [Docker Compose](https://www.docker.com) for development and testing.
- 🔒 Secure password hashing by default.
- 🔑 JWT (JSON Web Token) authentication.
- 📫 Email notifications using [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2).
- ☸️ [Kubernetes](https://www.kubernetes.io) for production.

### How to Setup
The project is broken down into five discrete microservice components - each of which has their own specific configuration and deployment instructions:
- [Authorization](https://github.com/dkaberna/microservices-fastapi-kubernetes/tree/main/auth)
- [Gateway](https://github.com/dkaberna/microservices-fastapi-kubernetes/tree/main/gateway)
- [Converter](https://github.com/dkaberna/microservices-fastapi-kubernetes/tree/main/converter)
- [Notification](https://github.com/dkaberna/microservices-fastapi-kubernetes/tree/main/notification)
- [RabbitMQ Server](https://github.com/dkaberna/microservices-fastapi-kubernetes/tree/main/rabbit)

## Local Docker and Kubernetes Deployment

You will need to follow the local install and configuration instructions on each of the five microservice components (links provided above) before attempting to run an end-to-end system test in Docker or deploying to a local Kubernetes install.

### Docker
Build the images and spin up the containers using the instructions in each of the microservice components linked above.

To test end-to-end, follow the instructions outlined in [Gateway](link).

### Kubernetes

#### Minikube

Install and run [Minikube](https://kubernetes.io/docs/setup/minikube/):

1. Install and Set Up [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to deploy and manage apps on Kubernetes
2. Install [Minikube](https://github.com/kubernetes/minikube/releases)
3. Install [K9s](https://k9scli.io/)

Start the cluster:

```sh
$ minikube start
$ sudo minikube tunnel
$ k9s
```
To deploy to a local kubernetes install, you will need your own docker hub, and will need to upload the following docker containers to your own docker hub: Auth, Converter, Gateway, and Notification. You will then need to edit the following manifest files with the information on your uploaded docker containers:

1. gateway-deploy.yaml
2. notification-deploy.yaml
3. converter-deploy.yaml
4. auth-deploy.yaml

Apply all manifest files:

```sh
$ make deploy
```
### End-to-End Smoke Testing
To ensure microservice is running, run this command:

    $ curl -X "GET" http://mp3converter.com/api/v1/status

Expected result:

```
{
  "success": true,
  "version": "<version>",
  "message": "Gateway Application"
}
```

#### Register user:

To test user registration, use a valid email address and create a password:

    $ curl -X 'POST' \
        'http://mp3converter.com/api/v1/user/register' \
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
        'http://mp3converter.com/api/v1/user/login' \
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
        -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjA4NDQwMzYsInN1YiI6InRlc3QtdXNlcjEifQ.-fPU-sXU-OJFKznilgJ5sbJFwUxIJdo5syVOjgnvTwM' http://mp3converter.com/api/v1/user/uploadfile

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
        -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjA4NDQwMzYsInN1YiI6InRlc3QtdXNlcjEifQ.-fPU-sXU-OJFKznilgJ5sbJFwUxIJdo5syVOjgnvTwM' http://mp3converter.com/api/v1/user/download/6691f8a5ed737d568756efb7
