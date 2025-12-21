from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


async def init_db():
    client = AsyncIOMotorClient(settings.database_url)

    from app.models.user import User
    from app.models.article import Article
    from app.models.comment import Comment

    await init_beanie(
        database=client.get_default_database(),
        document_models=[User, Article, Comment],
    )
