FastAPI User Authentication Microservice
====================

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://github.com/tiangolo/fastapi)

FastAPI user authentication using JWT.

### Stack:
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker

Configuration
--------------

Replace `.env.example` with real `.env`, changing placeholders

```
DATABASE_URL=postgresql://postgres:postgres@db/auth
POSTGRES_PORT = 5432
POSTGRES_PASSWORD = postgres
POSTGRES_DB = auth
POSTGRES_USER = postgres
SECRET_KEY = changeme
```

Local install
-------------

Setup and activate a python3 virtualenv via your preferred method. e.g. and install production requirements:

    $ make venv

For remove virtualenv:

    $ make clean


Local run
-------------
Run migration to create tables

    $ make migrate

Run pre-start script to check database:

    $  make check_db

Run server with settings:

    $ make runserver


Run in Docker
-------------

### !! Note:

If you want to run app in `Docker`, change host in `DATABASE_URL` in `.env` file to name of docker db service:

`DATABASE_URL=postgresql://postgres:postgres@db/auth`

Run project in Docker:

    $ make docker_build

Stop project in Docker:

    $ make docker_down

## Register user:

To ensure microservice is running, run this command:

    $ curl -X "GET" http://0.0.0.0:5000/api/v1/status

Expected result:

```
{
  "success": true,
  "version": "<version>",
  "message": "Auth Application"
}
```

To test user registration, run this command:

    $ curl -X 'POST' \
        'http://0.0.0.0:5000/api/v1/user/register' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
            "username": "test-user",
            "email": "test@test.com",
            "password": "weakpassword"
        }'

If everything is fine, you will get this message back:
```
{"success":true,"data":{"username":"test-user","email":"test@test.com"},"message":"The user was registered successfully","errors":null}
```


### Migrations

As during local development your app directory is mounted as a volume inside the container, you can also run the migrations with `alembic` commands inside the container and the migration code will be in your app directory (instead of being only inside the container). So you can add it to your git repository.

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in your database. Otherwise, your application will have errors.

* Start an interactive session in the backend container:

```console
$ docker compose exec backend bash
```

* Alembic is already configured to import your SQLModel models from `./backend/app/models.py`.

* After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```

* Commit to the git repository the files generated in the alembic directory.

* After creating the revision, run the migration in the database (this is what will actually change the database):

```console
$ alembic upgrade head
```

If you don't want to use migrations at all, uncomment the following line in the file at `./db/session.py`:

```python
engine = create_engine(url=settings.database_url, echo=True, future=True)

```

and comment the line in the file `prestart.sh` that contains:

```console
$ alembic upgrade head
```

If you don't want to start with the default models and want to remove them / modify them, from the beginning, without having any previous revision, you can remove the revision files (`.py` Python files) under `./backend/app/alembic/versions/`. And then create a first migration as described above.

Web routes
----------
All routes are available on ``/`` or ``/redoc`` paths with Swagger or ReDoc.


Project structure
-----------------
Files related to application are in the ``main`` and ``alembic`` directory.
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
├── backend_pre_start.py
├── core
│   ├── config.py
│   ├── dependencies.py
│   ├── exceptions.py
│   ├── __init__.py
│   ├── logger.py
│   ├── security.py
│   └── settings
│       ├── app.py
│       ├── base.py
│       ├── __init__.py
├── db
│   ├── base_class.py
│   ├── base.py
│   ├── __init__.py
│   ├── repositories
│   │   ├── base.py
│   │   ├── __init__.py
│   │   └── users.py
│   └── session.py
├── __init__.py
├── models
│   ├── __init__.py
│   └── user.py
├── schemas
│   ├── __init__.py
│   ├── response.py
│   ├── status.py
│   ├── token.py
│   └── user.py
└── services
    ├── __init__.py
    └── user.py
```
```
alembic
├── env.py
├── README
├── script.py.mako
└── versions
    ├── 6e563dceb4cf_initial_create.py
```