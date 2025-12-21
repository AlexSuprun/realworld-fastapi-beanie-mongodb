from datetime import datetime, timezone

from beanie import Document, Indexed, PydanticObjectId


class Article(Document):
    title: str
    slug: Indexed(str, unique=True)
    description: str
    body: str
    tag_list: list[str] = []
    favourited_user_ids: list[PydanticObjectId] = []
    author_id: PydanticObjectId
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "articles"
