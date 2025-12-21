from fastapi import APIRouter

from app.api.users import router as users_router
from app.api.user import router as user_router
from app.api.articles import router as articles_router
from app.api.comments import router as comments_router
from app.api.profiles import router as profiles_router
from app.api.tags import router as tags_router

api_router = APIRouter()

api_router.include_router(users_router)
api_router.include_router(user_router)
api_router.include_router(articles_router)
api_router.include_router(comments_router)
api_router.include_router(profiles_router)
api_router.include_router(tags_router)
