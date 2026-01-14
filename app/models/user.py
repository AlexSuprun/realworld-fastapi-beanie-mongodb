from beanie import Document, Indexed, PydanticObjectId
from pydantic import EmailStr, Field


class User(Document):
    email: Indexed(EmailStr, unique=True)
    username: Indexed(str, unique=True)
    password: str
    bio: str = ""
    image: str | None = None
    followers_ids: list[PydanticObjectId] = Field(default=[], alias="followersIds")
    following_ids: list[PydanticObjectId] = Field(default=[], alias="followingIds")
    articles_liked_ids: list[PydanticObjectId] = Field(default=[], alias="articlesLikedIds")

    class Settings:
        name = "users"

    model_config = {"populate_by_name": True}
