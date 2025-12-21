# Conduit API - FastAPI + Beanie + MongoDB

RealWorld "Conduit" backend implementation using modern Python stack.

## Tech Stack

- **Python** 3.12+
- **FastAPI** - Modern async web framework
- **Beanie** - Async MongoDB ODM (built on Pydantic v2)
- **Motor** - Async MongoDB driver
- **python-jose** - JWT tokens
- **passlib** - Password hashing with Argon2
- **uv** - Fast Python package manager

## Setup

### Prerequisites

- Python 3.12+
- MongoDB running on localhost:27017
- uv package manager

### Installation

```bash
# Install dependencies
uv sync

# Copy environment file
cp .env.example .env

# Edit .env with your settings (DATABASE_URL, SECRET)
```

### Running

```bash
# Development server with auto-reload
uv run uvicorn app.main:app --reload --port 3333

# Or without reload
uv run uvicorn app.main:app --port 3333
```

The API will be available at:
- API: http://localhost:3333/api
- Swagger docs: http://localhost:3333/docs
- ReDoc: http://localhost:3333/redoc

## API Endpoints

### Authentication
- `POST /api/users` - Register
- `POST /api/users/login` - Login

### User
- `GET /api/user` - Get current user
- `PUT /api/user` - Update current user

### Articles
- `GET /api/articles` - List articles
- `GET /api/articles/feed` - Get feed
- `GET /api/articles/:slug` - Get article
- `POST /api/articles` - Create article
- `PUT /api/articles/:slug` - Update article
- `DELETE /api/articles/:slug` - Delete article
- `POST /api/articles/:slug/favorite` - Favorite
- `DELETE /api/articles/:slug/favorite` - Unfavorite

### Comments
- `GET /api/articles/:slug/comments` - Get comments
- `POST /api/articles/:slug/comments` - Add comment
- `DELETE /api/articles/:slug/comments/:id` - Delete comment

### Profiles
- `GET /api/profiles/:username` - Get profile
- `POST /api/profiles/:username/follow` - Follow
- `DELETE /api/profiles/:username/follow` - Unfollow

### Tags
- `GET /api/tags` - Get all tags

## Project Structure

```
fastapi/
├── app/
│   ├── main.py           # FastAPI app entry point
│   ├── config.py         # Settings management
│   ├── database.py       # MongoDB/Beanie setup
│   ├── models/           # Beanie document models
│   ├── schemas/          # Pydantic DTOs
│   ├── api/              # Route handlers
│   ├── services/         # Business logic
│   └── core/             # Security, dependencies
├── tests/
├── pyproject.toml
└── .env.example
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | MongoDB connection string | `mongodb://localhost:27017/conduit` |
| `SECRET` | JWT signing secret | `your-jwt-secret-key` |
