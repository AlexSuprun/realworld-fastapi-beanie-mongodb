from datetime import datetime, timezone

from beanie import Document, PydanticObjectId


class Comment(Document):
    body: str
    author_id: PydanticObjectId
    article_id: PydanticObjectId
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "comments"
