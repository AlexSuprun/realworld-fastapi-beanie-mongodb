from beanie import Document, Indexed, PydanticObjectId
from pydantic import EmailStr


class User(Document):
    email: Indexed(EmailStr, unique=True)
    username: Indexed(str, unique=True)
    password: str
    bio: str = ""
    image: str | None = None
    followers_ids: list[PydanticObjectId] = []
    following_ids: list[PydanticObjectId] = []
    articles_liked_ids: list[PydanticObjectId] = []

    class Settings:
        name = "users"
