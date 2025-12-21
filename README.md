# ![RealWorld Example App](logo.png)

> ### FastAPI codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.


### [Demo](https://demo.realworld.io/)&nbsp;&nbsp;&nbsp;&nbsp;[RealWorld](https://github.com/gothinkster/realworld)


This codebase was created to demonstrate a fully fledged fullstack application built with FastAPI including CRUD operations, authentication, routing, pagination, and more.

We've gone to great lengths to adhere to the Python community styleguides & best practices.

For more information on how this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.


# How it works

This implementation uses FastAPI connected to a MongoDB database. Database operations are handled with Beanie ODM (async MongoDB ODM built on Pydantic v2).

# Getting started

## Prerequisites

- Python 3.12+
- Docker (recommended) or MongoDB installed locally
- uv package manager

## Environment Configuration

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | MongoDB connection string | `mongodb://localhost:27017/conduit` |
| `SECRET` | JWT secret key for authentication | `your-secret-key` |

## MongoDB Setup (Docker - Recommended)

Start MongoDB using Docker:

```bash
docker run -d --name mongo-conduit -p 27017:27017 mongo:8
```

### With Replica Set (required for transactions)

If you need transaction support, run MongoDB as a replica set:

```bash
docker run -d --name mongo-conduit -p 27017:27017 mongo:8 --replSet rs0 && sleep 2 && docker exec mongo-conduit mongosh --eval "rs.initiate()"
```

Update your connection string in `.env`:

```
DATABASE_URL=mongodb://localhost:27017/conduit?replicaSet=rs0
```

### Managing the container

To stop MongoDB:

```bash
docker stop mongo-conduit
```

To start it again:

```bash
docker start mongo-conduit
```

## Installation

```bash
uv sync
```

## Running the app

```bash
# development (watch mode)
uv run uvicorn app.main:app --reload --port 3333

# production mode
uv run uvicorn app.main:app --port 3333
```

The API will be available at `http://localhost:3333/api`

## API Documentation

This project includes Swagger/OpenAPI documentation. Once the server is running, access the interactive API documentation at:

- **Swagger UI**: http://localhost:3333/docs
- **ReDoc**: http://localhost:3333/redoc
- **OpenAPI JSON**: http://localhost:3333/openapi.json

The Swagger UI allows you to explore and test all API endpoints directly from your browser.

## Test

```bash
# unit tests
uv run pytest

# test coverage
uv run pytest --cov=app
```
