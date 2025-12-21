from datetime import datetime

from pydantic import BaseModel

from app.schemas.profile import ProfileDto


class ArticleForCreateDto(BaseModel):
    title: str
    description: str
    body: str
    tagList: list[str] = []


class CreateArticleRequest(BaseModel):
    article: ArticleForCreateDto


class ArticleForUpdateDto(BaseModel):
    title: str | None = None
    description: str | None = None
    body: str | None = None


class UpdateArticleRequest(BaseModel):
    article: ArticleForUpdateDto


class ArticleDto(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tagList: list[str] = []
    favoritesCount: int = 0
    author: ProfileDto
    favorited: bool = False
    createdAt: datetime
    updatedAt: datetime


class ArticleResponse(BaseModel):
    article: ArticleDto


class ArticlesResponse(BaseModel):
    articles: list[ArticleDto]
    articlesCount: int
