from datetime import datetime, timezone

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field


class Article(Document):
    title: str
    slug: Indexed(str, unique=True)
    description: str
    body: str
    tag_list: list[str] = Field(default=[], alias="tagList")
    favourited_user_ids: list[PydanticObjectId] = Field(default=[], alias="favouritedUserIds")
    author_id: PydanticObjectId = Field(alias="authorId")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), alias="createdAt")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), alias="updatedAt")

    class Settings:
        name = "articles"

    model_config = {"populate_by_name": True}
