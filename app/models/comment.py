from datetime import datetime, timezone

from beanie import Document, PydanticObjectId
from pydantic import Field


class Comment(Document):
    body: str
    author_id: PydanticObjectId = Field(alias="authorId")
    article_id: PydanticObjectId = Field(alias="articleId")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), alias="createdAt")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), alias="updatedAt")

    class Settings:
        name = "comments"

    model_config = {"populate_by_name": True}
